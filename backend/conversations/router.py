from fastapi import APIRouter, Depends, HTTPException, Response, status

from backend.auth.dependencies import get_current_user, get_database
from backend.conversations.models import ConversationRecord, MessageRecord
from backend.conversations.repository import ConversationRepository
from backend.conversations.schemas import (
    ConversationCreateRequest,
    ConversationDetailResponse,
    ConversationResponse,
    MessageCreateRequest,
    MessageResponse,
)
from backend.conversations.service import ConversationNotFoundError, ConversationService
from backend.database.connection import Database
from backend.users.models import UserRecord

router = APIRouter(prefix="/conversations", tags=["conversations"])


def _service(database: Database) -> ConversationService:
    return ConversationService(ConversationRepository(database))


@router.post(
    "", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED
)
async def create_conversation(
    payload: ConversationCreateRequest,
    user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> ConversationRecord:
    return await _service(database).create(user.id, payload.title)


@router.get("", response_model=list[ConversationResponse])
async def list_conversations(
    user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> list[ConversationRecord]:
    return await _service(database).list(user.id)


@router.get("/{conversation_id}", response_model=ConversationDetailResponse)
async def get_conversation(
    conversation_id: int,
    user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> ConversationRecord:
    try:
        return await _service(database).get(conversation_id, user.id)
    except ConversationNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Conversation not found") from exc


@router.post(
    "/{conversation_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_message(
    conversation_id: int,
    payload: MessageCreateRequest,
    user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> MessageRecord:
    try:
        return await _service(database).add_user_message(
            conversation_id, user.id, payload.content
        )
    except ConversationNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Conversation not found") from exc


@router.delete(
    "/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_conversation(
    conversation_id: int,
    user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> Response:
    try:
        await _service(database).delete(conversation_id, user.id)
    except ConversationNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Conversation not found") from exc
    return Response(status_code=status.HTTP_204_NO_CONTENT)
