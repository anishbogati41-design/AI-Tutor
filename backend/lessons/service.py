from backend.lessons.models import LessonDetailRecord
from backend.lessons.repository import LessonRepository
from backend.lessons.schemas import LessonWriteRequest
from backend.topics.repository import TopicRepository


class LessonNotFoundError(Exception):
    pass


class InvalidLessonSubtopicError(Exception):
    pass


class LessonService:
    def __init__(
        self, lesson_repository: LessonRepository, topic_repository: TopicRepository
    ) -> None:
        self._lesson_repository = lesson_repository
        self._topic_repository = topic_repository

    async def create(self, payload: LessonWriteRequest) -> LessonDetailRecord:
        await self._validate_subtopic(payload.subtopic_id)
        return await self._lesson_repository.create(payload)

    async def update(
        self, lesson_id: int, payload: LessonWriteRequest
    ) -> LessonDetailRecord:
        await self._validate_subtopic(payload.subtopic_id)
        updated = await self._lesson_repository.update(lesson_id, payload)
        if updated is None:
            raise LessonNotFoundError
        return updated

    async def _validate_subtopic(self, subtopic_id: int) -> None:
        topic = await self._topic_repository.get_by_id(subtopic_id)
        if topic is None or topic.parent_topic_id is None:
            raise InvalidLessonSubtopicError
