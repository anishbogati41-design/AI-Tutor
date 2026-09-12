from datetime import date

from pydantic import BaseModel, ConfigDict


class StudyPlanItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    study_plan_id: int
    title: str
    description: str
    scheduled_date: date
    position: int
    completed: bool


class StudyPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    items: tuple[StudyPlanItemResponse, ...]
