# Phase 7 — AI tutor and conversations

Status: Implemented and verified

Owner: Primary implementation

## Goal

Implement the approved educational AI tutor, persistent owned conversations, streamed chat responses, and contextual practice help without expanding the platform architecture.

## Dependencies

- Begin from the reviewed and committed Phase 6 baseline.
- PostgreSQL already contains the approved `conversations` and `messages` tables.
- Redis is restricted to sessions, short-window AI rate limits, and daily AI usage counters.
- Keep the approved `AIProvider` abstraction, with Ollama as the default local provider and OpenAI as an optional provider.
- Phase 7 may proceed alongside Phase 6 on a separate branch or worktree, then integrate after both branches pass their checks.

## Backend scope

- Implement owned conversation and message models, schemas, repositories, services, and routers.
- Implement `POST /conversations`, `GET /conversations`, `GET /conversations/{id}`, `POST /conversations/{id}/messages`, and `DELETE /conversations/{id}`.
- Enforce ownership on every conversation read, write, and delete operation.
- Implement `POST /ai/chat` with Server-Sent Events and persist the completed assistant response.
- Implement `POST /lessons/{id}/ai-practice` using the requested lesson/question context.
- Support the approved explanation styles and enforce educational-only behavior.
- Enforce the configured short-window request limit, daily request limit, and maximum response tokens.
- Keep AI-generated practice questions temporary and out of `questions` and `question_options`.
- Use only the active conversation's messages as chat context; never inject old conversations as automatic long-term memory.
- Handle upstream AI failures, interrupted streams, invalid ownership, unavailable configuration, and rate-limit responses without leaking secrets.

## Frontend scope

- Build `/chat` and `/chat/{id}` with the blueprint's conversation sidebar, new-chat action, previous conversations, delete confirmation, message list, streamed assistant bubble, and input area.
- Consume the SSE stream incrementally and refresh the active conversation after stream completion.
- Add the AI tutor navigation entry.
- Add the approved slide-in AI help panel to the practice screen and pass only the current lesson/question context.
- Provide loading, empty, streaming, rate-limit, and upstream-error states.

## Approved endpoints

- `POST /ai/chat`
- `POST /lessons/{id}/ai-practice`
- `POST /conversations`
- `GET /conversations`
- `GET /conversations/{id}`
- `POST /conversations/{id}/messages`
- `DELETE /conversations/{id}`

## Explicit exclusions

- Do not add WebSockets; chat streaming uses SSE.
- Do not store browser bearer tokens; authentication remains the Redis-backed HTTP-only session cookie.
- Do not persist generated practice questions in the official question bank.
- Do not introduce vector databases, background queues, providers beyond Ollama and OpenAI, long-term memory, text-to-speech, or quizzes.
- Do not implement study plans; those belong to Phase 8.

## File ownership and coordination

- Phase 7 owns `backend/ai_teacher/`, the new conversation backend module, AI-specific schemas/services/routers, and chat-specific frontend files.
- Coordinate before editing `backend/main.py`, `backend/config.py`, `backend/requirements*.txt`, `frontend/components/app-shell.tsx`, `frontend/app/(student)/lessons/[id]/practice/page.tsx`, `README.md`, `api.md`, or Compose files.
- Never commit `OPENAI_API_KEY` or any other secret. Store local values only in the ignored `.env` file.
- Keep Phase 7 commits focused so shared-file changes can be reviewed or cherry-picked cleanly.

## Task order

1. Define conversation/message contracts and ownership errors.
2. Implement PostgreSQL conversation persistence and REST endpoints.
3. Implement Redis-backed AI counters using only the approved key purposes.
4. Implement Ollama and OpenAI behind the shared provider boundary and educational prompt safeguards.
5. Implement SSE chat streaming and final assistant-message persistence.
6. Implement contextual practice help.
7. Build chat routes and streamed message UI.
8. Build the practice AI side panel and connect navigation.
9. Update API and local configuration documentation.
10. Validate failure handling, security boundaries, Docker images, and the live stack.

## Validation

- Test conversation ownership and administrator/student authentication boundaries.
- Test create/list/read/message/delete behavior with PostgreSQL.
- Test short-window and daily Redis counters and token limits.
- Test SSE event order, stream completion, persistence, and upstream failure behavior with a mocked provider boundary.
- Verify that one conversation never receives another conversation's history.
- Verify generated practice content is absent from the official question tables.
- Run backend unit/integration tests, frontend typecheck, and the production build.
- Build the Phase 7 images and run the local five-service stack, including Ollama with `qwen3:4b`.

## Git handoff

Do not stage or commit without the assigned developer's explicit approval. Do not push or merge unless separately requested by the repository owner.

## Delivery summary

- Added owned PostgreSQL conversation and message persistence through all five approved REST endpoints.
- Added native Ollama and optional OpenAI Responses API implementations behind the existing provider abstraction, explicit environment selection with no fallback, response-token caps, educational instructions, explanation styles, and safe upstream-error handling. OpenAI provider-side storage is disabled.
- Added Redis-backed per-user short-window and daily AI enforcement using the existing approved counter keys.
- Added SSE chat streaming, active-conversation-only context, completed assistant-message persistence, and practice help limited to the requested lesson and question.
- Added `/chat`, `/chat/{id}`, conversation history and deletion, incremental SSE rendering, AI tutor navigation, and the practice screen's slide-in AI help panel.
- Updated configuration templates, API documentation, README instructions, and the Phase 7 Compose stack without adding a database migration or any excluded capability.

## Validation result

- Backend unit and live PostgreSQL/Redis/Ollama integration suite: `33 passed`.
- Frontend TypeScript check: passed.
- Production Next.js build: passed and generated `/chat` plus `/chat/[id]`.
- Phase 7 development backend/frontend images: built with Docker's default builder.
- Local five-service stack: healthy at <http://localhost:3000> and <http://localhost:8000>, with the Ollama model stored in its named volume.
- Unauthenticated `/chat` request: redirects to `/login`; authenticated ownership, streaming persistence, isolated conversation context, upstream failure, and temporary practice-help behavior are covered by integration tests.
- Real local `qwen3:4b` completion and streaming: passed through the Ollama provider without a paid API request.
- No OpenAI credential is stored in tracked files. Local AI output defaults to Ollama with `qwen3:4b`; `OPENAI_API_KEY` applies only when `AI_PROVIDER=openai` is explicitly selected.
