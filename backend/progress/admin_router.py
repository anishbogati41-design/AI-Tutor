from fastapi import APIRouter, Depends, HTTPException, status

from backend.auth.dependencies import get_database, require_admin
from backend.database.connection import Database
from backend.progress.schemas import AdminStudentProgressResponse, AdminStudentResponse
from backend.progress.service import ProgressService, StudentNotFoundError
from backend.users.models import UserRecord

router = APIRouter(tags=["admin students"])


@router.get("/students", response_model=list[AdminStudentResponse])
async def list_students(
    _: UserRecord = Depends(require_admin),
    database: Database = Depends(get_database),
) -> list[AdminStudentResponse]:
    return await ProgressService(database).students()


@router.get("/students/{student_id}/progress", response_model=AdminStudentProgressResponse)
async def get_student_progress(
    student_id: int,
    _: UserRecord = Depends(require_admin),
    database: Database = Depends(get_database),
) -> AdminStudentProgressResponse:
    try:
        return await ProgressService(database).student_progress(student_id)
    except StudentNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found") from exc
