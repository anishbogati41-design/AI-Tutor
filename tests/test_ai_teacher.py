import asyncio
from types import SimpleNamespace

import pytest

from backend.ai_teacher.provider import OllamaProvider, OpenAIResponsesProvider
from backend.ai_teacher.router import get_ai_provider
from backend.ai_teacher.service import AIRateLimitError, AIService
from backend.config import Settings


class CounterStore:
    def __init__(self, *, rate: int, daily: int) -> None:
        self.rate = rate
        self.daily = daily

    async def increment_ai_rate(self, user_id: int, window_seconds: int) -> int:
        return self.rate

    async def increment_ai_daily(self, user_id: int) -> int:
        return self.daily


def make_service(store: CounterStore) -> AIService:
    settings = SimpleNamespace(
        ai_rate_limit_window_seconds=60,
        ai_rate_limit_requests=10,
        ai_daily_request_limit=100,
    )
    return AIService(None, None, None, store, settings, None)  # type: ignore[arg-type]


def test_ai_limits_allow_configured_boundary() -> None:
    asyncio.run(make_service(CounterStore(rate=10, daily=100))._enforce_limits(1))


@pytest.mark.parametrize(
    ("rate", "daily"),
    [(11, 1), (1, 101)],
)
def test_ai_limits_reject_excess_usage(rate: int, daily: int) -> None:
    with pytest.raises(AIRateLimitError):
        asyncio.run(make_service(CounterStore(rate=rate, daily=daily))._enforce_limits(1))


def test_openai_payload_caps_tokens_and_disables_provider_storage() -> None:
    provider = OpenAIResponsesProvider("test-key", "approved-model", 321)
    assert provider._payload("instructions", "input") == {
        "model": "approved-model",
        "instructions": "instructions",
        "input": "input",
        "max_output_tokens": 321,
        "store": False,
    }


def test_ollama_payload_disables_thinking_and_caps_output() -> None:
    provider = OllamaProvider("http://ollama:11434/", "qwen3:4b", 321)
    assert provider._url == "http://ollama:11434/api/chat"
    assert provider._payload("instructions", "input", stream=False) == {
        "model": "qwen3:4b",
        "messages": [
            {"role": "system", "content": "instructions"},
            {"role": "user", "content": "input"},
        ],
        "stream": False,
        "think": False,
        "options": {"num_predict": 321},
    }


def test_local_configuration_defaults_to_ollama_without_openai_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("AI_PROVIDER", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    settings = Settings.from_environment()

    assert settings.ai_provider == "ollama"
    assert settings.ollama_model == "qwen3:4b"
    assert settings.openai_api_key is None
    assert isinstance(get_ai_provider(settings), OllamaProvider)


def test_openai_remains_optional_and_requires_explicit_credentials() -> None:
    common = {
        "ai_provider": "openai",
        "ollama_base_url": "http://ollama:11434",
        "ollama_model": "qwen3:4b",
        "openai_model": "gpt-5-mini",
        "ai_max_response_tokens": 800,
    }
    assert get_ai_provider(SimpleNamespace(openai_api_key=None, **common)) is None
    assert isinstance(
        get_ai_provider(SimpleNamespace(openai_api_key="test-key", **common)),
        OpenAIResponsesProvider,
    )


def test_invalid_ai_provider_is_rejected(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("AI_PROVIDER", "automatic-paid-fallback")
    with pytest.raises(ValueError, match="AI_PROVIDER"):
        Settings.from_environment()
