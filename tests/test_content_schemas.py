import pytest
from pydantic import ValidationError

from backend.lessons.schemas import LessonWriteRequest
from backend.topics.schemas import TopicWriteRequest


def test_lesson_requires_contiguous_unique_section_positions() -> None:
    with pytest.raises(ValidationError, match="contiguous from zero"):
        LessonWriteRequest(
            title="A lesson",
            subtopic_id=2,
            estimated_minutes=10,
            sections=[
                {
                    "section_type": "INTRODUCTION",
                    "title": "Start",
                    "content": "Opening content",
                    "position": 1,
                }
            ],
        )


def test_lesson_accepts_the_approved_section_types_in_order() -> None:
    lesson = LessonWriteRequest(
        title="A lesson",
        subtopic_id=2,
        estimated_minutes=10,
        sections=[
            {
                "section_type": "INTRODUCTION",
                "title": "Start",
                "content": "Opening content",
                "position": 0,
            },
            {
                "section_type": "SUMMARY",
                "title": "Finish",
                "content": "Closing content",
                "position": 1,
            },
        ],
    )

    assert [section.position for section in lesson.sections] == [0, 1]


def test_topic_write_request_normalizes_text() -> None:
    topic = TopicWriteRequest(name="  Mathematics  ", description="  Numbers  ")

    assert topic.name == "Mathematics"
    assert topic.description == "Numbers"
