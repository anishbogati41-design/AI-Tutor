from backend.conversations.models import ConversationRecord, MessageRecord
from backend.conversations.repository import ConversationRepository


class ConversationNotFoundError(Exception):
    pass


class ConversationService:
    def __init__(self, repository: ConversationRepository) -> None:
        self._repository = repository

    async def create(self, user_id: int, title: str) -> ConversationRecord:
        return await self._repository.create(user_id, title)

    async def list(self, user_id: int) -> list[ConversationRecord]:
        return await self._repository.list_owned(user_id)

    async def get(self, conversation_id: int, user_id: int) -> ConversationRecord:
        conversation = await self._repository.get_owned(conversation_id, user_id)
        if conversation is None:
            raise ConversationNotFoundError
        return conversation

    async def add_user_message(
        self, conversation_id: int, user_id: int, content: str
    ) -> MessageRecord:
        message = await self._repository.add_message(
            conversation_id, user_id, "USER", content
        )
        if message is None:
            raise ConversationNotFoundError
        return message

    async def delete(self, conversation_id: int, user_id: int) -> None:
        if not await self._repository.delete_owned(conversation_id, user_id):
            raise ConversationNotFoundError
