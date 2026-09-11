from backend.topics.models import TopicRecord
from backend.topics.repository import TopicRepository
from backend.topics.schemas import TopicWriteRequest


class TopicNotFoundError(Exception):
    pass


class InvalidTopicParentError(Exception):
    pass


class TopicService:
    def __init__(self, repository: TopicRepository) -> None:
        self._repository = repository

    async def create(self, payload: TopicWriteRequest) -> TopicRecord:
        await self._validate_parent(payload.parent_topic_id)
        return await self._repository.create(
            payload.name, payload.parent_topic_id, payload.description
        )

    async def update(
        self, topic_id: int, payload: TopicWriteRequest
    ) -> TopicRecord:
        if await self._repository.get_by_id(topic_id) is None:
            raise TopicNotFoundError
        await self._validate_parent(payload.parent_topic_id)
        if payload.parent_topic_id is not None and await self._repository.parent_would_create_cycle(
            topic_id, payload.parent_topic_id
        ):
            raise InvalidTopicParentError
        updated = await self._repository.update(
            topic_id, payload.name, payload.parent_topic_id, payload.description
        )
        if updated is None:
            raise TopicNotFoundError
        return updated

    async def _validate_parent(self, parent_topic_id: int | None) -> None:
        if parent_topic_id is not None and await self._repository.get_by_id(
            parent_topic_id
        ) is None:
            raise InvalidTopicParentError
