import pytest

from backend.config import Settings


def test_development_defaults_are_safe_for_local_use(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("APP_ENV", "SESSION_SECRET", "COOKIE_SECURE"):
        monkeypatch.delenv(name, raising=False)

    settings = Settings.from_environment()

    assert settings.app_env == "development"
    assert settings.cookie_secure is False
    assert settings.session_ttl_seconds > 0


def test_production_rejects_the_local_session_secret(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("SESSION_SECRET", raising=False)
    monkeypatch.setenv("COOKIE_SECURE", "true")

    with pytest.raises(ValueError, match="SESSION_SECRET"):
        Settings.from_environment()


def test_production_requires_secure_cookies(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("SESSION_SECRET", "a-production-secret")
    monkeypatch.setenv("COOKIE_SECURE", "false")

    with pytest.raises(ValueError, match="COOKIE_SECURE"):
        Settings.from_environment()
