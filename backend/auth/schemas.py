from pydantic import BaseModel, field_validator

from backend.users.schemas import UserProfileUpdate


class RegisterRequest(UserProfileUpdate):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if len(value) < 8 or len(value) > 128:
            raise ValueError("password must contain 8 to 128 characters")
        return value


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if (
            len(normalized) > 320
            or normalized.count("@") != 1
            or not all(normalized.split("@"))
        ):
            raise ValueError("email must be a valid address")
        return normalized

    @field_validator("password")
    @classmethod
    def validate_password_length(cls, value: str) -> str:
        if not value or len(value) > 128:
            raise ValueError("password must contain 1 to 128 characters")
        return value


class AdminLoginRequest(LoginRequest):
    pin: str

    @field_validator("pin")
    @classmethod
    def validate_pin(cls, value: str) -> str:
        if len(value) < 4 or len(value) > 64:
            raise ValueError("pin must contain 4 to 64 characters")
        return value
