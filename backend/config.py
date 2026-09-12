from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache


def _integer(name: str, default: int) -> int:
    raw_value = os.getenv(name, str(default))
    try:
        value = int(raw_value)
    except ValueError as exc:
        raise ValueError(f"{name} must be an integer") from exc
    if value <= 0:
        raise ValueError(f"{name} must be greater than zero")
    return value


def _boolean(name: str, default: bool) -> bool:
    raw_value = os.getenv(name, str(default)).strip().lower()
    if raw_value in {"1", "true", "yes", "on"}:
        return True
    if raw_value in {"0", "false", "no", "off"}:
        return False
    raise ValueError(f"{name} must be a boolean")


@dataclass(frozen=True, slots=True)
class Settings:
    app_env: str
    app_host: str
    app_port: int
    log_level: str
    database_url: str
    redis_url: str
    session_secret: str
    session_ttl_seconds: int
    session_cookie_name: str
    cookie_secure: bool
    backend_url: str
    frontend_url: str
    admin_login_pin: str | None
    admin_seed_email: str | None
    admin_seed_password: str | None
    openai_api_key: str | None
    ai_rate_limit_requests: int
    ai_rate_limit_window_seconds: int
    ai_daily_request_limit: int
    ai_max_response_tokens: int

    @classmethod
    def from_environment(cls) -> "Settings":
        app_env = os.getenv("APP_ENV", "development").strip().lower()
        if app_env not in {"development", "test", "production"}:
            raise ValueError("APP_ENV must be development, test, or production")

        session_secret = os.getenv(
            "SESSION_SECRET", "local-development-only-change-me"
        )
        cookie_secure = _boolean("COOKIE_SECURE", app_env == "production")
        if app_env == "production":
            if session_secret == "local-development-only-change-me":
                raise ValueError("SESSION_SECRET must be set in production")
            if not cookie_secure:
                raise ValueError("COOKIE_SECURE must be true in production")

        return cls(
            app_env=app_env,
            app_host=os.getenv("APP_HOST", "0.0.0.0"),
            app_port=_integer("APP_PORT", 8000),
            log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
            database_url=os.getenv(
                "DATABASE_URL",
                "postgresql://adaptive:adaptive@localhost:5432/adaptive_education",
            ),
            redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
            session_secret=session_secret,
            session_ttl_seconds=_integer("SESSION_TTL_SECONDS", 86400),
            session_cookie_name=os.getenv("SESSION_COOKIE_NAME", "adaptive_session"),
            cookie_secure=cookie_secure,
            backend_url=os.getenv("BACKEND_URL", "http://localhost:8000"),
            frontend_url=os.getenv("FRONTEND_URL", "http://localhost:3000"),
            admin_login_pin=os.getenv("ADMIN_LOGIN_PIN") or None,
            admin_seed_email=os.getenv("ADMIN_SEED_EMAIL") or None,
            admin_seed_password=os.getenv("ADMIN_SEED_PASSWORD") or None,
            openai_api_key=os.getenv("OPENAI_API_KEY") or None,
            ai_rate_limit_requests=_integer("AI_RATE_LIMIT_REQUESTS", 10),
            ai_rate_limit_window_seconds=_integer(
                "AI_RATE_LIMIT_WINDOW_SECONDS", 60
            ),
            ai_daily_request_limit=_integer("AI_DAILY_REQUEST_LIMIT", 100),
            ai_max_response_tokens=_integer("AI_MAX_RESPONSE_TOKENS", 800),
        )


@lru_cache
def get_settings() -> Settings:
    return Settings.from_environment()
