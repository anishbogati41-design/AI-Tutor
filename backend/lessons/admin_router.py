from fastapi import APIRouter, Depends, HTTPException, Response, status

from backend.auth.dependencies import get_database, require_admin
from backend.database.connection import Database
from backend.lessons.models import LessonDetailRecord
from backend.lessons.repository import LessonInUseError, LessonRepository
from backend.lessons.schemas import LessonDetailResponse, LessonWriteRequest
from backend.lessons.service import (
    InvalidLessonSubtopicError,
    LessonNotFoundError,
    LessonService,
)
from backend.topics.repository import TopicRepository
from backend.users.models import UserRecord

router = APIRouter(prefix="/lessons", tags=["administrator content"])


def _service(database: Database) -> LessonService:
    return LessonService(LessonRepository(database), TopicRepository(database))


@router.post("", response_model=LessonDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_lesson(
    payload: LessonWriteRequest,
    admin: UserRecord = Depends(require_admin),
    database: Database = Depends(get_database),
) -> LessonDetailRecord:
    del admin
    try:
        return await _service(database).create(payload)
    except InvalidLessonSubtopicError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="subtopic_id must identify a child topic",
        ) from exc


@router.put("/{lesson_id}", response_model=LessonDetailResponse)
async def update_lesson(
    lesson_id: int,
    payload: LessonWriteRequest,
    admin: UserRecord = Depends(require_admin),
    database: Database = Depends(get_database),
) -> LessonDetailRecord:
    del admin
    try:
        return await _service(database).update(lesson_id, payload)
    except InvalidLessonSubtopicError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="subtopic_id must identify a child topic",
        ) from exc
    except LessonNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found") from exc


@router.delete(
    "/{lesson_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def delete_lesson(
    lesson_id: int,
    admin: UserRecord = Depends(require_admin),
    database: Database = Depends(get_database),
) -> Response:
    del admin
    try:
        deleted = await LessonRepository(database).delete(lesson_id)
    except LessonInUseError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Lesson is still referenced by a learning record",
        ) from exc
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
