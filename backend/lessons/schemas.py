from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class SectionType(StrEnum):
    INTRODUCTION = "INTRODUCTION"
    EXPLANATION = "EXPLANATION"
    EXAMPLE = "EXAMPLE"
    SUMMARY = "SUMMARY"


class LessonSectionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lesson_id: int
    section_type: SectionType
    title: str
    content: str
    position: int


class LessonResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str
    subtopic_id: int
    estimated_minutes: int
    is_published: bool


class LessonDetailResponse(LessonResponse):
    sections: tuple[LessonSectionResponse, ...]


class LessonSectionWriteRequest(BaseModel):
    section_type: SectionType
    title: str
    content: str
    position: int = Field(ge=0)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized or len(normalized) > 200:
            raise ValueError("title must contain 1 to 200 characters")
        return normalized

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("content must not be empty")
        return normalized


class LessonWriteRequest(BaseModel):
    title: str
    description: str = ""
    subtopic_id: int
    estimated_minutes: int = Field(gt=0, le=1440)
    is_published: bool = False
    sections: list[LessonSectionWriteRequest] = Field(default_factory=list)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized or len(normalized) > 200:
            raise ValueError("title must contain 1 to 200 characters")
        return normalized

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) > 5000:
            raise ValueError("description must be at most 5000 characters")
        return normalized

    @model_validator(mode="after")
    def validate_section_positions(self) -> "LessonWriteRequest":
        positions = sorted(section.position for section in self.sections)
        if positions != list(range(len(positions))):
            raise ValueError("section positions must be unique and contiguous from zero")
        return self
