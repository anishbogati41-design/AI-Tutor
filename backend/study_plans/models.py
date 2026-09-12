from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class StudyPlanItemRecord:
    id: int
    study_plan_id: int
    title: str
    description: str
    scheduled_date: date
    position: int
    completed: bool


@dataclass(frozen=True, slots=True)
class StudyPlanRecord:
    id: int
    user_id: int
    items: tuple[StudyPlanItemRecord, ...] = ()


@dataclass(frozen=True, slots=True)
class LearningSignal:
    lesson_title: str
    topic_name: str
    mastery_percentage: float
    correct_count: int
    attempt_count: int
    weak_accuracy: float | None


@dataclass(frozen=True, slots=True)
class GeneratedStudyPlanItem:
    title: str
    description: str
    scheduled_date: date
    position: int
    completed: bool = False
