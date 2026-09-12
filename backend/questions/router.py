from fastapi import APIRouter, Depends, HTTPException, status

from backend.adaptive.schemas import AdaptiveQuestionResponse
from backend.adaptive.service import AdaptiveService
from backend.auth.dependencies import get_current_user, get_database
from backend.database.connection import Database
from backend.lessons.repository import LessonRepository
from backend.questions.repository import QuestionRepository
from backend.questions.schemas import (
    AnswerRequest,
    AnswerResponse,
    PracticeSessionResponse,
)
from backend.questions.service import (
    PracticeLessonNotFoundError,
    QuestionNotFoundError,
    QuestionService,
)
from backend.topics.repository import TopicRepository
from backend.users.models import UserRecord

router = APIRouter(tags=["adaptive practice"])


@router.get(
    "/lessons/{lesson_id}/practice/next",
    response_model=AdaptiveQuestionResponse,
    response_model_exclude_none=True,
)
async def get_next_question(
    lesson_id: int,
    current_user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> AdaptiveQuestionResponse:
    result = await AdaptiveService(database).next_question(
        lesson_id, current_user.id, include_drafts=current_user.is_admin
    )
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson or practice question not found",
        )
    return result


def _service(database: Database) -> QuestionService:
    return QuestionService(
        QuestionRepository(database),
        LessonRepository(database),
        TopicRepository(database),
    )


@router.get(
    "/lessons/{lesson_id}/practice",
    response_model=PracticeSessionResponse,
    response_model_exclude_none=True,
)
async def get_practice_session(
    lesson_id: int,
    current_user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> PracticeSessionResponse:
    try:
        return await _service(database).get_practice_session(
            lesson_id,
            current_user.id,
            include_answers=current_user.is_admin,
        )
    except PracticeLessonNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Lesson not found"
        ) from exc


@router.post(
    "/practice/{question_id}/answer",
    response_model=AnswerResponse,
)
async def answer_question(
    question_id: int,
    payload: AnswerRequest,
    current_user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> AnswerResponse:
    try:
        return await _service(database).answer(
            question_id,
            current_user.id,
            payload.answer,
            include_drafts=current_user.is_admin,
        )
    except QuestionNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Question not found"
        ) from exc
