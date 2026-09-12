from fastapi import APIRouter, Depends

from backend.auth.dependencies import get_current_user, get_database
from backend.database.connection import Database
from backend.progress.schemas import ProgressResponse
from backend.progress.service import ProgressService
from backend.users.models import UserRecord

router = APIRouter(tags=["progress"])


@router.get("/progress", response_model=ProgressResponse)
async def get_progress(
    current_user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> ProgressResponse:
    return await ProgressService(database).get(current_user.id)
