# Architecture Decision Log

## ADR-001 — Selectable local and hosted AI providers

- Date: 2026-09-12
- Status: Approved
- Applies to: Phase 7 — AI tutor and conversations

### Decision record

APPROVED: Ollama as the default local AI provider.

APPROVED: OpenAI remains an optional provider.

REJECTED: Making paid OpenAI API access mandatory for local development.

### Approved architecture

- Keep the existing `AIProvider` abstraction.
- Support `ollama` and `openai` implementations selected explicitly through `AI_PROVIDER`.
- Default local development to `AI_PROVIDER=ollama` and `OLLAMA_MODEL=qwen3:4b`.
- Configure the local endpoint with `OLLAMA_BASE_URL`.
- Require `OPENAI_API_KEY` only when `AI_PROVIDER=openai`; it must not be required when Ollama is active.
- Do not automatically fall back from Ollama to OpenAI, because that could trigger unapproved paid usage.
- Preserve FastAPI, PostgreSQL, Redis, REST endpoints, SSE streaming, conversations, authentication, AI rate limits, educational safeguards, output limits, temporary AI practice content, and conversation isolation.
- Preserve the frontend architecture and its existing API contracts.

### Consequences

- Local Phase 7 development can run without a paid API account.
- Ollama becomes the fifth local Compose service and stores `qwen3:4b` model data in a named local volume.
- OpenAI remains available only through explicit configuration and a separately supplied secret.
- Selecting a provider changes only the backend provider implementation; it does not change the public REST or SSE contracts.
- Running Ollama inside Kubernetes is not approved by this decision and requires separate infrastructure and resource approval.
