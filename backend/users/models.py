from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class UserRecord:
    id: int
    name: str
    email: str
    password_hash: str
    is_admin: bool
    font_size: str
    readable_mode: bool
    high_contrast: bool
    dyslexia_mode: bool
