from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from backend.auth.dependencies import get_current_user, get_database
from backend.database.connection import Database
from backend.lessons.models import LessonDetailRecord, LessonRecord
from backend.lessons.repository import LessonRepository
from backend.lessons.schemas import LessonDetailResponse, LessonResponse
from backend.users.models import UserRecord

router = APIRouter(prefix="/lessons", tags=["lessons"])


@router.get("", response_model=list[LessonResponse])
async def list_lessons(
    current_user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
    search: Annotated[str | None, Query(max_length=200)] = None,
    topic_id: Annotated[int | None, Query(gt=0)] = None,
) -> list[LessonRecord]:
    normalized_search = search.strip() if search and search.strip() else None
    return await LessonRepository(database).list_all(
        include_drafts=current_user.is_admin,
        search=normalized_search,
        topic_id=topic_id,
    )


@router.get("/{lesson_id}", response_model=LessonDetailResponse)
async def get_lesson(
    lesson_id: int,
    current_user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> LessonDetailRecord:
    lesson = await LessonRepository(database).get_by_id(
        lesson_id, include_drafts=current_user.is_admin
    )
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found")
    return lesson
