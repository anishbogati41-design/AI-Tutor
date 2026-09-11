# Adaptive Education API

This document catalogs every approved API endpoint. The architecture source of truth is [Architet design.md](Architet%20design.md). Quizzes and text-to-speech are outside the API scope.

## Conventions

- FastAPI serves the API as REST endpoints.
- The browser authenticates with an opaque, HTTP-only secure session cookie backed by Redis.
- Protected requests never use browser-stored bearer tokens.
- FastAPI enforces authentication and administrator authorization independently of the frontend.
- `POST /ai/chat` streams assistant output with Server-Sent Events (SSE).
- PostgreSQL stores durable records. Redis stores only sessions, short-window AI rate counters, and daily AI usage counters.
- IDs shown as `{id}` or `{question_id}` are path parameters.

Implementation status values:

- **Implemented** — available in the current backend.
- **Planned** — approved by the blueprint and assigned to a future phase.
- **Generated** — supplied automatically by FastAPI.

## Service and documentation endpoints

| Method | Path | Access | Phase | Status | Purpose |
|---|---|---|---:|---|---|
| `GET` | `/health/live` | Public | 1 | Implemented | Confirms that the backend process is running. |
| `GET` | `/health/ready` | Public | 1 | Implemented | Confirms that PostgreSQL and Redis are reachable. Returns `503` when either dependency is unavailable. |
| `GET` | `/docs` | Public | 1 | Generated | Interactive OpenAPI documentation. |
| `GET` | `/docs/oauth2-redirect` | Public | 1 | Generated | Swagger UI's generated OAuth redirect helper. It does not change the session-cookie authentication design. |
| `GET` | `/redoc` | Public | 1 | Generated | Alternative generated OpenAPI documentation. |
| `GET` | `/openapi.json` | Public | 1 | Generated | OpenAPI schema used by the documentation UI. |

## Authentication endpoints

| Method | Path | Access | Phase | Status | Purpose |
|---|---|---|---:|---|---|
| `POST` | `/auth/register` | Public | 2 | Implemented | Create a student account with email and password. |
| `POST` | `/auth/login` | Public | 2 | Implemented | Authenticate credentials, create a Redis session, and set the secure session cookie. |
| `POST` | `/auth/logout` | Session | 2 | Implemented | Delete the Redis session and clear the session cookie. |
| `GET` | `/auth/me` | Session | 2 | Implemented | Resolve the current authenticated identity and administrator flag. |

## User profile endpoints

| Method | Path | Access | Phase | Status | Purpose |
|---|---|---|---:|---|---|
| `GET` | `/users/me` | Session | 2 | Implemented | Return the current user's profile. |
| `PUT` | `/users/me` | Session | 2 | Implemented | Update the current user's approved profile fields. |
| `GET` | `/users/me/preferences` | Session | 2 | Implemented | Return saved accessibility preferences. |
| `PUT` | `/users/me/preferences` | Session | 2 | Implemented | Update `font_size`, `readable_mode`, `high_contrast`, and `dyslexia_mode`. |

## Topic and lesson endpoints

| Method | Path | Access | Phase | Status | Purpose |
|---|---|---|---:|---|---|
| `GET` | `/lessons` | Session | 3 | Implemented | List published lessons for students and all lessons for administrators. Supports `search` and `topic_id` filters. |
| `GET` | `/lessons/{id}` | Session | 3 | Implemented | Return one visible lesson and its ordered sections. |
| `GET` | `/topics` | Session | 3 | Implemented | List topics. |
| `GET` | `/topics/{id}` | Session | 3 | Implemented | Return one topic. |
| `GET` | `/topics/{id}/subtopics` | Session | 3 | Implemented | List the direct children of a topic. |

## Adaptive practice endpoints

| Method | Path | Access | Phase | Status | Purpose |
|---|---|---|---:|---|---|
| `GET` | `/lessons/{id}/practice` | Session | 4 | Planned | Return adaptive-practice information for a lesson. |
| `GET` | `/lessons/{id}/practice/next` | Session | 5 | Planned | Select the next practice question using topic mastery and the appropriate difficulty band. |
| `POST` | `/practice/{question_id}/answer` | Session | 4 | Planned | Evaluate an answer, return correctness and explanation, and update the practice summary. |

Practice questions support only `MCQ`, `TRUE_FALSE`, and `SHORT_ANSWER`. AI-generated practice questions remain temporary and are never added to the official question bank.

## Progress endpoint

| Method | Path | Access | Phase | Status | Purpose |
|---|---|---|---:|---|---|
| `GET` | `/progress` | Session | 5 | Planned | Return the combined dashboard payload: score, topic accuracy, mastery, weak topics, recent improvement, and study-plan preview. |

## Study-plan endpoints

| Method | Path | Access | Phase | Status | Purpose |
|---|---|---|---:|---|---|
| `GET` | `/study-plan` | Session | 8 | Planned | Return the current saved study plan and ordered items. |
| `POST` | `/study-plan/refresh` | Session | 8 | Planned | Regenerate the plan from current learning data. Recommendations are not stored as a separate resource. |

## AI tutor endpoints

| Method | Path | Access | Phase | Status | Purpose |
|---|---|---|---:|---|---|
| `POST` | `/ai/chat` | Session | 7 | Planned | Stream an educational AI tutor response through SSE. |
| `POST` | `/lessons/{id}/ai-practice` | Session | 7 | Planned | Return practice-specific AI help using lesson and question context. |

Both AI endpoints are subject to the per-user short-window request limit, daily request limit, and per-answer token limit. General chat and practice help remain separate capabilities.

## Conversation endpoints

| Method | Path | Access | Phase | Status | Purpose |
|---|---|---|---:|---|---|
| `POST` | `/conversations` | Session | 7 | Planned | Create a new conversation. Prior conversations are not injected as automatic long-term memory. |
| `GET` | `/conversations` | Session | 7 | Planned | List the current user's conversations. |
| `GET` | `/conversations/{id}` | Session | 7 | Planned | Return one owned conversation and its messages. |
| `POST` | `/conversations/{id}/messages` | Session | 7 | Planned | Add a user message to an owned conversation and produce the assistant response. |
| `DELETE` | `/conversations/{id}` | Session | 7 | Planned | Delete an owned conversation and its messages. |

## Administrator content endpoints

| Method | Path | Access | Phase | Status | Purpose |
|---|---|---|---:|---|---|
| `POST` | `/admin/lessons` | Admin | 3 | Implemented | Create a lesson with section-based content. |
| `PUT` | `/admin/lessons/{id}` | Admin | 3 | Implemented | Update a lesson and atomically replace its sections. |
| `DELETE` | `/admin/lessons/{id}` | Admin | 3 | Implemented | Delete a lesson. |
| `POST` | `/admin/topics` | Admin | 3 | Implemented | Create a topic or subtopic. |
| `PUT` | `/admin/topics/{id}` | Admin | 3 | Implemented | Update a topic or subtopic while preventing hierarchy cycles. |
| `DELETE` | `/admin/topics/{id}` | Admin | 3 | Implemented | Delete a topic when its relationships allow deletion. |
| `POST` | `/admin/lessons/{id}/questions` | Admin | 4 | Planned | Create an adaptive-practice question for a lesson. |
| `PUT` | `/admin/lessons/{id}/questions/{question_id}` | Admin | 4 | Planned | Update an adaptive-practice question. |
| `DELETE` | `/admin/lessons/{id}/questions/{question_id}` | Admin | 4 | Planned | Delete an adaptive-practice question. |
| `GET` | `/admin/students` | Admin | 5 | Planned | List students for the small admin area. |
| `GET` | `/admin/students/{id}/progress` | Admin | 5 | Planned | Return progress information for one student. |

## Endpoint count

- 2 implemented service endpoints.
- 4 generated documentation endpoints.
- 19 implemented product endpoints.
- 18 planned product endpoints.
- 43 endpoint paths in total.

No quiz, account-deletion, recommendation-resource, text-to-speech, teacher-portal, or expanded role-management endpoint is approved.
