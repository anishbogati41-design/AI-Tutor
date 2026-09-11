from __future__ import annotations

from pydantic import BaseModel, ConfigDict, field_validator


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    is_admin: bool
    font_size: str
    readable_mode: bool
    high_contrast: bool
    dyslexia_mode: bool


class UserProfileUpdate(BaseModel):
    name: str
    email: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("name must not be empty")
        if len(normalized) > 100:
            raise ValueError("name must be at most 100 characters")
        return normalized

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if (
            len(normalized) > 320
            or normalized.count("@") != 1
            or not all(normalized.split("@"))
        ):
            raise ValueError("email must be a valid address")
        return normalized


class AccessibilityPreferences(BaseModel):
    font_size: str
    readable_mode: bool
    high_contrast: bool
    dyslexia_mode: bool

    @field_validator("font_size")
    @classmethod
    def validate_font_size(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized or len(normalized) > 32:
            raise ValueError("font_size must contain 1 to 32 characters")
        return normalized
