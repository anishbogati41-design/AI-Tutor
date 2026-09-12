from __future__ import annotations

import json
from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse

from backend.ai_teacher.provider import (
    AIProvider,
    OllamaProvider,
    OpenAIResponsesProvider,
)
from backend.ai_teacher.schemas import AIChatRequest, AIPracticeRequest, AIPracticeResponse
from backend.ai_teacher.service import (
    AIConversationStateError,
    AIRateLimitError,
    AIResourceNotFoundError,
    AIService,
    AIUnavailableError,
)
from backend.auth.dependencies import get_current_user, get_database, get_redis_store
from backend.config import Settings, get_settings
from backend.conversations.repository import ConversationRepository
from backend.database.connection import Database
from backend.lessons.repository import LessonRepository
from backend.questions.repository import QuestionRepository
from backend.redis_store.client import RedisStore
from backend.users.models import UserRecord

router = APIRouter(tags=["AI tutor"])


class EventStreamResponse(StreamingResponse):
    media_type = "text/event-stream"


def get_ai_provider(settings: Settings = Depends(get_settings)) -> AIProvider | None:
    if settings.ai_provider == "ollama":
        return OllamaProvider(
            settings.ollama_base_url,
            settings.ollama_model,
            settings.ai_max_response_tokens,
        )
    if not settings.openai_api_key:
        return None
    return OpenAIResponsesProvider(
        settings.openai_api_key,
        settings.openai_model,
        settings.ai_max_response_tokens,
    )


def _service(
    database: Database,
    redis_store: RedisStore,
    settings: Settings,
    provider: AIProvider | None,
) -> AIService:
    return AIService(
        ConversationRepository(database),
        LessonRepository(database),
        QuestionRepository(database),
        redis_store,
        settings,
        provider,
    )


def _raise_http(exc: Exception) -> None:
    if isinstance(exc, AIResourceNotFoundError):
        raise HTTPException(status_code=404, detail="AI resource not found") from exc
    if isinstance(exc, AIConversationStateError):
        raise HTTPException(
            status_code=409,
            detail="Save this message to the conversation before requesting a response",
        ) from exc
    if isinstance(exc, AIRateLimitError):
        raise HTTPException(
            status_code=429, detail="AI usage limit reached; try again later"
        ) from exc
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail="AI tutor is unavailable",
    ) from exc


@router.post("/ai/chat", response_class=EventStreamResponse)
async def chat(
    payload: AIChatRequest,
    user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
    redis_store: RedisStore = Depends(get_redis_store),
    settings: Settings = Depends(get_settings),
    provider: AIProvider | None = Depends(get_ai_provider),
) -> EventStreamResponse:
    service = _service(database, redis_store, settings, provider)
    try:
        conversation = await service.prepare_chat(user, payload)
    except (
        AIResourceNotFoundError,
        AIConversationStateError,
        AIRateLimitError,
        AIUnavailableError,
    ) as exc:
        _raise_http(exc)

    async def events() -> AsyncIterator[str]:
        try:
            async for delta in service.stream_chat(user, payload, conversation):
                yield f"event: delta\ndata: {json.dumps({'text': delta})}\n\n"
            yield "event: done\ndata: [DONE]\n\n"
        except Exception:
            yield (
                "event: error\ndata: "
                + json.dumps({"detail": "AI response failed"})
                + "\n\n"
            )

    return EventStreamResponse(events())


@router.post(
    "/lessons/{lesson_id}/ai-practice", response_model=AIPracticeResponse
)
async def practice_help(
    lesson_id: int,
    payload: AIPracticeRequest,
    user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
    redis_store: RedisStore = Depends(get_redis_store),
    settings: Settings = Depends(get_settings),
    provider: AIProvider | None = Depends(get_ai_provider),
) -> AIPracticeResponse:
    try:
        response = await _service(
            database, redis_store, settings, provider
        ).practice_help(lesson_id, user, payload)
    except (
        AIResourceNotFoundError,
        AIRateLimitError,
        AIUnavailableError,
    ) as exc:
        _raise_http(exc)
    return AIPracticeResponse(response=response)
