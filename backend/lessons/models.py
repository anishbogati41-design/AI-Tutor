from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class LessonSectionRecord:
    id: int
    lesson_id: int
    section_type: str
    title: str
    content: str
    position: int


@dataclass(frozen=True, slots=True)
class LessonRecord:
    id: int
    title: str
    description: str
    subtopic_id: int
    estimated_minutes: int
    is_published: bool


@dataclass(frozen=True, slots=True)
class LessonDetailRecord(LessonRecord):
    sections: tuple[LessonSectionRecord, ...]
