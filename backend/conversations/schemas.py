from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class ConversationCreateRequest(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if not normalized or len(normalized) > 200:
            raise ValueError("title must contain 1 to 200 characters")
        return normalized


class MessageCreateRequest(BaseModel):
    content: str

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized or len(normalized) > 10000:
            raise ValueError("content must contain 1 to 10000 characters")
        return normalized


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime


class ConversationDetailResponse(ConversationResponse):
    messages: tuple[MessageResponse, ...]
