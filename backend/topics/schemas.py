from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator


class TopicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    parent_topic_id: int | None
    description: str


class TopicWriteRequest(BaseModel):
    name: str
    parent_topic_id: int | None = None
    description: str = ""

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized or len(normalized) > 200:
            raise ValueError("name must contain 1 to 200 characters")
        return normalized

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) > 5000:
            raise ValueError("description must be at most 5000 characters")
        return normalized
