from __future__ import annotations

from collections.abc import AsyncIterator

from backend.ai_teacher.provider import AIProvider, AIProviderError
from backend.ai_teacher.schemas import AIChatRequest, AIPracticeRequest, ExplanationStyle
from backend.config import Settings
from backend.conversations.models import ConversationRecord
from backend.conversations.repository import ConversationRepository
from backend.lessons.repository import LessonRepository
from backend.questions.repository import QuestionRepository
from backend.redis_store.client import RedisStore
from backend.users.models import UserRecord


class AIUnavailableError(Exception):
    pass


class AIRateLimitError(Exception):
    pass


class AIResourceNotFoundError(Exception):
    pass


class AIConversationStateError(Exception):
    pass


class AIService:
    _base_instructions = (
        "You are an educational AI tutor. Answer only learning and study questions. "
        "Politely refuse unrelated requests. Explain accurately, safely, and at the "
        "student's level. Do not claim to have memory outside the supplied conversation."
    )

    def __init__(
        self,
        conversation_repository: ConversationRepository,
        lesson_repository: LessonRepository,
        question_repository: QuestionRepository,
        redis_store: RedisStore,
        settings: Settings,
        provider: AIProvider | None,
    ) -> None:
        self._conversations = conversation_repository
        self._lessons = lesson_repository
        self._questions = question_repository
        self._redis = redis_store
        self._settings = settings
        self._provider = provider

    async def prepare_chat(
        self, user: UserRecord, payload: AIChatRequest
    ) -> ConversationRecord:
        self._require_provider()
        conversation = await self._conversations.get_owned(
            payload.conversation_id, user.id
        )
        if conversation is None:
            raise AIResourceNotFoundError
        if (
            not conversation.messages
            or conversation.messages[-1].role != "USER"
            or conversation.messages[-1].content != payload.message
        ):
            raise AIConversationStateError
        await self._enforce_limits(user.id)
        return conversation

    async def stream_chat(
        self,
        user: UserRecord,
        payload: AIChatRequest,
        conversation: ConversationRecord,
    ) -> AsyncIterator[str]:
        provider = self._require_provider()
        input_text = self._conversation_input(conversation)
        parts: list[str] = []
        try:
            async for delta in provider.stream(
                instructions=self._instructions(payload.explanation_style),
                input_text=input_text,
            ):
                parts.append(delta)
                yield delta
        except AIProviderError as exc:
            raise AIUnavailableError from exc
        response = "".join(parts).strip()
        if not response:
            raise AIUnavailableError
        message = await self._conversations.add_message(
            payload.conversation_id, user.id, "ASSISTANT", response
        )
        if message is None:
            raise AIResourceNotFoundError

    async def practice_help(
        self, lesson_id: int, user: UserRecord, payload: AIPracticeRequest
    ) -> str:
        provider = self._require_provider()
        include_drafts = user.is_admin
        lesson = await self._lessons.get_by_id(
            lesson_id, include_drafts=include_drafts
        )
        question = await self._questions.get_by_id(
            payload.question_id, include_drafts=include_drafts
        )
        if lesson is None or question is None or question.lesson_id != lesson_id:
            raise AIResourceNotFoundError
        await self._enforce_limits(user.id)
        sections = "\n".join(
            f"{section.title}: {section.content}" for section in lesson.sections
        )
        options = "\n".join(
            f"- {option.option_text}" for option in question.options
        )
        correct_answers = [
            option.option_text for option in question.options if option.is_correct
        ] or list(question.accepted_answers)
        input_text = (
            f"Lesson: {lesson.title}\nDescription: {lesson.description}\n"
            f"Lesson content:\n{sections}\n\nQuestion: {question.question_text}\n"
            f"Options:\n{options or 'No options'}\n"
            f"Official answer: {', '.join(correct_answers) or 'Not provided'}\n"
            f"Official explanation: {question.explanation or 'Not provided'}\n\n"
            f"Student request: {payload.prompt}"
        )
        try:
            return await provider.complete(
                instructions=(
                    self._instructions(payload.explanation_style)
                    + " Help the student understand this practice question without "
                    "creating or saving an official question."
                ),
                input_text=input_text,
            )
        except AIProviderError as exc:
            raise AIUnavailableError from exc

    async def _enforce_limits(self, user_id: int) -> None:
        rate_count = await self._redis.increment_ai_rate(
            user_id, self._settings.ai_rate_limit_window_seconds
        )
        daily_count = await self._redis.increment_ai_daily(user_id)
        if (
            rate_count > self._settings.ai_rate_limit_requests
            or daily_count > self._settings.ai_daily_request_limit
        ):
            raise AIRateLimitError

    def _require_provider(self) -> AIProvider:
        if self._provider is None:
            raise AIUnavailableError
        return self._provider

    def _instructions(self, style: ExplanationStyle) -> str:
        styles = {
            ExplanationStyle.SIMPLE: "Use simple language and a short explanation.",
            ExplanationStyle.DETAILED: "Give a thorough explanation with useful context.",
            ExplanationStyle.STEP_BY_STEP: "Explain the reasoning in clear numbered steps.",
        }
        return f"{self._base_instructions} {styles[style]}"

    @staticmethod
    def _conversation_input(conversation: ConversationRecord) -> str:
        return "\n".join(
            f"{message.role.title()}: {message.content}"
            for message in conversation.messages
        )
