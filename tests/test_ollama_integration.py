import asyncio
import os

import pytest

from backend.ai_teacher.provider import OllamaProvider
from backend.config import Settings


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_OLLAMA_INTEGRATION_TESTS") != "1",
    reason="set RUN_OLLAMA_INTEGRATION_TESTS=1 with the Ollama service running",
)


def test_ollama_completion_and_streaming() -> None:
    settings = Settings.from_environment()
    provider = OllamaProvider(
        settings.ollama_base_url,
        settings.ollama_model,
        settings.ai_max_response_tokens,
    )

    async def exercise_provider() -> tuple[str, str]:
        completion = await provider.complete(
            instructions="You are a concise educational tutor.",
            input_text="/no_think\nReply with the single word READY.",
        )
        chunks = [
            chunk
            async for chunk in provider.stream(
                instructions="You are a concise educational tutor.",
                input_text=(
                    "/no_think\nExplain in one short sentence why 2 + 2 equals 4."
                ),
            )
        ]
        return completion, "".join(chunks)

    completion, streamed = asyncio.run(exercise_provider())
    assert completion.strip()
    assert streamed.strip()
