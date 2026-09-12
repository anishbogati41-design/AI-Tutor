from fastapi import APIRouter, Depends

from backend.auth.dependencies import get_current_user, get_database
from backend.database.connection import Database
from backend.study_plans.models import StudyPlanRecord
from backend.study_plans.repository import StudyPlanRepository
from backend.study_plans.schemas import StudyPlanResponse
from backend.study_plans.service import StudyPlanService
from backend.users.models import UserRecord

router = APIRouter(prefix="/study-plan", tags=["study plans"])


def _service(database: Database) -> StudyPlanService:
    return StudyPlanService(StudyPlanRepository(database))


@router.get("", response_model=StudyPlanResponse | None)
async def get_study_plan(
    user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> StudyPlanRecord | None:
    return await _service(database).get(user.id)


@router.post("/refresh", response_model=StudyPlanResponse)
async def refresh_study_plan(
    user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> StudyPlanRecord:
    return await _service(database).refresh(user.id)
