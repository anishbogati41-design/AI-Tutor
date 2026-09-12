from __future__ import annotations

from datetime import date, timedelta

from backend.study_plans.models import GeneratedStudyPlanItem, LearningSignal, StudyPlanRecord
from backend.study_plans.repository import StudyPlanRepository


class StudyPlanService:
    def __init__(self, repository: StudyPlanRepository) -> None:
        self._repository = repository

    async def get(self, user_id: int) -> StudyPlanRecord | None:
        return await self._repository.get_owned(user_id)

    async def refresh(
        self, user_id: int, *, start_date: date | None = None
    ) -> StudyPlanRecord:
        signals = await self._repository.learning_signals(user_id)
        items = build_study_plan(signals, start_date=start_date or date.today())
        return await self._repository.replace(user_id, items)


def build_study_plan(
    signals: list[LearningSignal], *, start_date: date
) -> list[GeneratedStudyPlanItem]:
    return [
        GeneratedStudyPlanItem(
            title=_title(signal),
            description=_description(signal),
            scheduled_date=start_date + timedelta(days=position),
            position=position,
        )
        for position, signal in enumerate(signals)
    ]


def _title(signal: LearningSignal) -> str:
    if signal.weak_accuracy is not None:
        return f"Practice: {signal.topic_name} — Weak Topic"
    if signal.attempt_count:
        return f"Review: {signal.lesson_title}"
    return f"Lesson: {signal.lesson_title}"


def _description(signal: LearningSignal) -> str:
    if signal.weak_accuracy is not None:
        return (
            f"Strengthen {signal.topic_name} with adaptive practice; "
            f"current accuracy is {signal.weak_accuracy:.0f}%."
        )
    if signal.attempt_count:
        accuracy = 100 * signal.correct_count / signal.attempt_count
        return (
            f"Review {signal.topic_name}; current mastery is "
            f"{signal.mastery_percentage:.0f}% and practice accuracy is {accuracy:.0f}%."
        )
    return f"Read the lesson sections and begin practicing {signal.topic_name}."
