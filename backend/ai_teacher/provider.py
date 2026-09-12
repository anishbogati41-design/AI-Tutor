from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Protocol

import httpx


class AIProviderError(Exception):
    pass


class AIProvider(Protocol):
    def stream(self, *, instructions: str, input_text: str) -> AsyncIterator[str]: ...

    async def complete(self, *, instructions: str, input_text: str) -> str: ...


class ResponsesProvider:
    def __init__(
        self,
        *,
        url: str,
        model: str,
        max_output_tokens: int,
        provider_name: str,
        headers: dict[str, str] | None = None,
        timeout_seconds: float = 300,
    ) -> None:
        self._url = url
        self._headers = headers or {}
        self._model = model
        self._max_output_tokens = max_output_tokens
        self._provider_name = provider_name
        self._timeout_seconds = timeout_seconds

    def _payload(self, instructions: str, input_text: str) -> dict[str, object]:
        return {
            "model": self._model,
            "instructions": instructions,
            "input": input_text,
            "max_output_tokens": self._max_output_tokens,
            "store": False,
        }

    async def complete(self, *, instructions: str, input_text: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
                response = await client.post(
                    self._url,
                    headers=self._headers,
                    json=self._payload(instructions, input_text),
                )
                response.raise_for_status()
                data = response.json()
                output_text = data.get("output_text") or self._extract_output_text(data)
        except (httpx.HTTPError, ValueError) as exc:
            raise AIProviderError(f"{self._provider_name} request failed") from exc
        if not isinstance(output_text, str) or not output_text.strip():
            raise AIProviderError(f"{self._provider_name} returned no text")
        return output_text.strip()

    @staticmethod
    def _extract_output_text(data: dict[str, object]) -> str:
        parts: list[str] = []
        output = data.get("output")
        if not isinstance(output, list):
            return ""
        for item in output:
            if not isinstance(item, dict):
                continue
            contents = item.get("content")
            if not isinstance(contents, list):
                continue
            for content in contents:
                if isinstance(content, dict) and content.get("type") == "output_text":
                    text = content.get("text")
                    if isinstance(text, str):
                        parts.append(text)
        return "".join(parts)

    async def stream(
        self, *, instructions: str, input_text: str
    ) -> AsyncIterator[str]:
        payload = self._payload(instructions, input_text)
        payload["stream"] = True
        try:
            async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
                async with client.stream(
                    "POST", self._url, headers=self._headers, json=payload
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        event = json.loads(data)
                        event_type = event.get("type")
                        if event_type == "response.output_text.delta":
                            delta = event.get("delta")
                            if isinstance(delta, str) and delta:
                                yield delta
                        elif event_type in {"error", "response.failed"}:
                            raise AIProviderError(
                                f"{self._provider_name} stream failed"
                            )
        except (httpx.HTTPError, ValueError, json.JSONDecodeError) as exc:
            raise AIProviderError(f"{self._provider_name} stream failed") from exc


class OpenAIResponsesProvider(ResponsesProvider):
    def __init__(self, api_key: str, model: str, max_output_tokens: int) -> None:
        super().__init__(
            url="https://api.openai.com/v1/responses",
            headers={"Authorization": f"Bearer {api_key}"},
            model=model,
            max_output_tokens=max_output_tokens,
            provider_name="OpenAI",
            timeout_seconds=60,
        )


class OllamaProvider:
    def __init__(self, base_url: str, model: str, max_output_tokens: int) -> None:
        self._url = f"{base_url.rstrip('/')}/api/chat"
        self._model = model
        self._max_output_tokens = max_output_tokens

    def _payload(
        self, instructions: str, input_text: str, *, stream: bool
    ) -> dict[str, object]:
        return {
            "model": self._model,
            "messages": [
                {"role": "system", "content": instructions},
                {"role": "user", "content": input_text},
            ],
            "stream": stream,
            "think": False,
            "options": {"num_predict": self._max_output_tokens},
        }

    async def complete(self, *, instructions: str, input_text: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=300) as client:
                response = await client.post(
                    self._url,
                    json=self._payload(instructions, input_text, stream=False),
                )
                response.raise_for_status()
                message = response.json().get("message")
                output_text = (
                    message.get("content") if isinstance(message, dict) else None
                )
        except (httpx.HTTPError, ValueError) as exc:
            raise AIProviderError("Ollama request failed") from exc
        if not isinstance(output_text, str) or not output_text.strip():
            raise AIProviderError("Ollama returned no text")
        return output_text.strip()

    async def stream(
        self, *, instructions: str, input_text: str
    ) -> AsyncIterator[str]:
        try:
            async with httpx.AsyncClient(timeout=300) as client:
                async with client.stream(
                    "POST",
                    self._url,
                    json=self._payload(instructions, input_text, stream=True),
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line:
                            continue
                        event = json.loads(line)
                        if event.get("error"):
                            raise AIProviderError("Ollama stream failed")
                        message = event.get("message")
                        delta = (
                            message.get("content")
                            if isinstance(message, dict)
                            else None
                        )
                        if isinstance(delta, str) and delta:
                            yield delta
                        if event.get("done") is True:
                            break
        except (httpx.HTTPError, ValueError, json.JSONDecodeError) as exc:
            raise AIProviderError("Ollama stream failed") from exc
