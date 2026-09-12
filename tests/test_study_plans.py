from datetime import date

from backend.study_plans.models import LearningSignal
from backend.study_plans.service import build_study_plan


def test_plan_generation_preserves_learning_priority_and_dates() -> None:
    signals = [
        LearningSignal(
            lesson_title="Equivalent Fractions",
            topic_name="Fractions",
            mastery_percentage=35,
            correct_count=2,
            attempt_count=6,
            weak_accuracy=33.33,
        ),
        LearningSignal(
            lesson_title="Linear Equations",
            topic_name="Algebra",
            mastery_percentage=65,
            correct_count=3,
            attempt_count=4,
            weak_accuracy=None,
        ),
        LearningSignal(
            lesson_title="Introduction to Motion",
            topic_name="Physics",
            mastery_percentage=0,
            correct_count=0,
            attempt_count=0,
            weak_accuracy=None,
        ),
    ]

    items = build_study_plan(signals, start_date=date(2026, 9, 12))

    assert [item.position for item in items] == [0, 1, 2]
    assert [item.scheduled_date.isoformat() for item in items] == [
        "2026-09-12",
        "2026-09-13",
        "2026-09-14",
    ]
    assert items[0].title == "Practice: Fractions — Weak Topic"
    assert "33%" in items[0].description
    assert items[1].title == "Review: Linear Equations"
    assert "75%" in items[1].description
    assert items[2].title == "Lesson: Introduction to Motion"
    assert all(item.completed is False for item in items)


def test_plan_generation_allows_an_empty_curriculum() -> None:
    assert build_study_plan([], start_date=date(2026, 9, 12)) == []
