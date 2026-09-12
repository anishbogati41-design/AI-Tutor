from __future__ import annotations

from backend.lessons.repository import LessonRepository
from backend.questions.models import QuestionRecord
from backend.questions.repository import QuestionRepository
from backend.questions.schemas import (
    AnswerResponse,
    PracticeSessionResponse,
    PracticeSummaryResponse,
    QuestionOptionResponse,
    QuestionResponse,
    QuestionWriteRequest,
)
from backend.topics.repository import TopicRepository


class PracticeLessonNotFoundError(Exception):
    pass


class QuestionNotFoundError(Exception):
    pass


class InvalidQuestionRelationError(Exception):
    pass


class QuestionService:
    def __init__(
        self,
        question_repository: QuestionRepository,
        lesson_repository: LessonRepository,
        topic_repository: TopicRepository,
    ) -> None:
        self._questions = question_repository
        self._lessons = lesson_repository
        self._topics = topic_repository

    async def get_practice_session(
        self, lesson_id: int, user_id: int, *, include_answers: bool
    ) -> PracticeSessionResponse:
        session = await self._questions.get_practice_session(
            lesson_id, user_id, include_drafts=include_answers
        )
        if session is None:
            raise PracticeLessonNotFoundError
        return PracticeSessionResponse(
            lesson_id=session.lesson_id,
            lesson_title=session.lesson_title,
            summary=PracticeSummaryResponse.model_validate(
                session.summary, from_attributes=True
            ),
            questions=tuple(
                self.question_response(question, include_answers=include_answers)
                for question in session.questions
            ),
        )

    async def answer(
        self,
        question_id: int,
        user_id: int,
        answer: str,
        *,
        include_drafts: bool,
    ) -> AnswerResponse:
        question = await self._questions.get_by_id(
            question_id, include_drafts=include_drafts
        )
        if question is None:
            raise QuestionNotFoundError

        submitted = self._normalize(answer)
        if question.question_type == "SHORT_ANSWER":
            correct_answers = question.accepted_answers
        else:
            correct_answers = tuple(
                option.option_text for option in question.options if option.is_correct
            )
        is_correct = any(
            submitted == self._normalize(correct_answer)
            for correct_answer in correct_answers
        )
        await self._questions.record_answer(
            user_id, question.lesson_id, is_correct=is_correct
        )
        return AnswerResponse(
            is_correct=is_correct,
            correct_answer=correct_answers[0],
            explanation=question.explanation,
        )

    async def create(
        self, lesson_id: int, payload: QuestionWriteRequest
    ) -> QuestionResponse:
        await self._validate_relations(lesson_id, payload.topic_id)
        question = await self._questions.create(lesson_id, payload)
        return self.question_response(question, include_answers=True)

    async def update(
        self, lesson_id: int, question_id: int, payload: QuestionWriteRequest
    ) -> QuestionResponse:
        await self._validate_relations(lesson_id, payload.topic_id)
        question = await self._questions.update(lesson_id, question_id, payload)
        if question is None:
            raise QuestionNotFoundError
        return self.question_response(question, include_answers=True)

    async def _validate_relations(self, lesson_id: int, topic_id: int) -> None:
        lesson = await self._lessons.get_by_id(lesson_id, include_drafts=True)
        topic = await self._topics.get_by_id(topic_id)
        if lesson is None or topic is None:
            raise InvalidQuestionRelationError

    @staticmethod
    def question_response(
        question: QuestionRecord, *, include_answers: bool
    ) -> QuestionResponse:
        return QuestionResponse(
            id=question.id,
            lesson_id=question.lesson_id,
            topic_id=question.topic_id,
            question_text=question.question_text,
            question_type=question.question_type,
            difficulty_score=question.difficulty_score,
            explanation=question.explanation if include_answers else None,
            accepted_answers=(question.accepted_answers if include_answers else None),
            options=tuple(
                QuestionOptionResponse(
                    id=option.id,
                    question_id=option.question_id,
                    option_text=option.option_text,
                    position=option.position,
                    is_correct=option.is_correct if include_answers else None,
                )
                for option in question.options
            ),
        )

    @staticmethod
    def _normalize(value: str) -> str:
        return " ".join(value.split()).casefold()
