from enum import StrEnum

from pydantic import BaseModel, Field, field_validator


class ExplanationStyle(StrEnum):
    SIMPLE = "SIMPLE"
    DETAILED = "DETAILED"
    STEP_BY_STEP = "STEP_BY_STEP"


class AIChatRequest(BaseModel):
    conversation_id: int = Field(gt=0)
    message: str
    explanation_style: ExplanationStyle = ExplanationStyle.SIMPLE

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized or len(normalized) > 10000:
            raise ValueError("message must contain 1 to 10000 characters")
        return normalized


class AIPracticeRequest(BaseModel):
    question_id: int = Field(gt=0)
    prompt: str
    explanation_style: ExplanationStyle = ExplanationStyle.STEP_BY_STEP

    @field_validator("prompt")
    @classmethod
    def validate_prompt(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized or len(normalized) > 2000:
            raise ValueError("prompt must contain 1 to 2000 characters")
        return normalized


class AIPracticeResponse(BaseModel):
    response: str
