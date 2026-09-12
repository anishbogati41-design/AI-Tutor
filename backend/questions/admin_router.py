from fastapi import APIRouter, Depends, HTTPException, Response, status

from backend.auth.dependencies import get_database, require_admin
from backend.database.connection import Database
from backend.lessons.repository import LessonRepository
from backend.questions.repository import QuestionRepository
from backend.questions.schemas import QuestionResponse, QuestionWriteRequest
from backend.questions.service import (
    InvalidQuestionRelationError,
    QuestionNotFoundError,
    QuestionService,
)
from backend.topics.repository import TopicRepository
from backend.users.models import UserRecord

router = APIRouter(
    prefix="/lessons/{lesson_id}/questions", tags=["administrator content"]
)


def _service(database: Database) -> QuestionService:
    return QuestionService(
        QuestionRepository(database),
        LessonRepository(database),
        TopicRepository(database),
    )


@router.post("", response_model=QuestionResponse, status_code=status.HTTP_201_CREATED)
async def create_question(
    lesson_id: int,
    payload: QuestionWriteRequest,
    admin: UserRecord = Depends(require_admin),
    database: Database = Depends(get_database),
) -> QuestionResponse:
    del admin
    try:
        return await _service(database).create(lesson_id, payload)
    except InvalidQuestionRelationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="lesson_id and topic_id must identify existing content",
        ) from exc


@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    lesson_id: int,
    question_id: int,
    payload: QuestionWriteRequest,
    admin: UserRecord = Depends(require_admin),
    database: Database = Depends(get_database),
) -> QuestionResponse:
    del admin
    try:
        return await _service(database).update(lesson_id, question_id, payload)
    except InvalidQuestionRelationError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="lesson_id and topic_id must identify existing content",
        ) from exc
    except QuestionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        ) from exc


@router.delete(
    "/{question_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_question(
    lesson_id: int,
    question_id: int,
    admin: UserRecord = Depends(require_admin),
    database: Database = Depends(get_database),
) -> Response:
    del admin
    deleted = await QuestionRepository(database).delete(lesson_id, question_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
