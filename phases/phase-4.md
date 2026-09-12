# Phase 4 — Questions and Adaptive Practice Records

## Objective

Implement official practice questions, answer evaluation, durable per-lesson practice summaries, administrator question management, and the frontend screens required to use those capabilities.

## Approved scope

- Practice-only questions using `MCQ`, `TRUE_FALSE`, or `SHORT_ANSWER`.
- Ordered options for MCQ and True/False questions.
- Case-insensitive, whitespace-normalized answer evaluation.
- Durable per-user, per-lesson practice summaries in PostgreSQL.
- `GET /lessons/{id}/practice` and `POST /practice/{question_id}/answer`.
- Administrator question create, update, and delete endpoints.
- Student practice UI with one question at a time and answer feedback.
- Administrator dynamic question editor accessible from the authenticated frontend.
- Phase 4 navigation, Docker images, and a four-service local runtime.

Adaptive next-question selection, mastery, weak-topic updates, global difficulty recalculation, AI help, quizzes, and text-to-speech remain outside this phase.

## Dependencies

- Phase 1 PostgreSQL schema and migration runner.
- Phase 2 Redis-backed authentication and administrator authorization.
- Phase 3 topic, lesson, and authenticated frontend foundations.
- Existing `questions`, `question_options`, and `practice_attempts` tables.

## Implementation checklist

- [x] Add practice-attempt uniqueness migration.
- [x] Add question models, schemas, repository, and evaluation service.
- [x] Add practice session and answer endpoints.
- [x] Add administrator question CRUD.
- [x] Register Phase 4 routers with FastAPI.
- [x] Add student practice navigation and one-question-at-a-time UI.
- [x] Add the administrator dynamic question editor.
- [x] Add focused unit and live integration coverage.
- [x] Update the blueprint, API catalog, README, and handoff state.
- [x] Build backend and frontend images with `ai-tutor-builder`.
- [x] Start and verify the four-service Phase 4 local runtime.
- [x] Report the phase and request approval before staging or committing.

## Validation commands

```bash
docker compose -f compose.phase4.yaml run --rm backend python -m backend.database.migrate
docker compose -f compose.phase4.yaml run --rm backend python -m pytest -q
docker compose -f compose.phase4.yaml run --rm -e RUN_INTEGRATION_TESTS=1 backend python -m pytest -q
docker compose -f compose.phase4.yaml run --rm frontend npm run typecheck
docker compose -f compose.phase4.yaml run --rm frontend npm run build
docker buildx build --builder ai-tutor-builder --load -f backend/Dockerfile.dev -t ai-tutor-backend:phase-4 .
docker buildx build --builder ai-tutor-builder --load -f backend/Dockerfile -t ai-tutor-backend:phase-4-production .
docker buildx build --builder ai-tutor-builder --load -f frontend/Dockerfile.dev -t ai-tutor-frontend:phase-4 .
docker buildx build --builder ai-tutor-builder --load -f frontend/Dockerfile -t ai-tutor-frontend:phase-4-production .
docker compose -f compose.phase4.yaml up -d --no-build --wait
```

## Handoff state

Status: Complete; committed and pushed at the user's request.

### Delivered

- Strict question contracts for `MCQ`, `TRUE_FALSE`, and `SHORT_ANSWER`.
- Atomic question and ordered-option persistence in PostgreSQL.
- One durable practice summary per user and lesson, enforced by migration.
- An authenticated practice endpoint with official questions and the current summary.
- Case-insensitive, whitespace-normalized answer evaluation.
- Student payloads that withhold explanations and solution fields until submission.
- Administrator question create, update, and delete operations.
- A student practice library and one-question-at-a-time interface with feedback.
- A role-gated dynamic administrator question manager for all three question types.
- Lesson and sidebar navigation into the Phase 4 interfaces.
- Idempotent development-only starter content with one published lesson, four sections, and all three approved question types.
- Development and production images built with `ai-tutor-builder`.

### Validation results

- Python compilation: passed.
- Git whitespace/error check: passed.
- Compose configuration: passed.
- Default backend suite: 14 passed, 4 live integration tests skipped.
- Live PostgreSQL/Redis suite: 18 passed.
- Student solution-data protection: verified by integration test.
- Frontend strict TypeScript check: passed.
- Next.js production build: passed with all Phase 4 routes generated.
- Five Phase 4 API methods registered in live OpenAPI.
- Development and production backend images: built successfully.
- Production Gunicorn configuration: passed.
- Development and production frontend images: built successfully.
- Frontend authentication redirect, practice, and admin route smoke checks: passed.
- Local starter content after repeated seeding: one lesson, four sections, and three questions with no duplicates.
- Local frontend, backend, PostgreSQL, and Redis services are running.

### Local runtime

- Frontend: <http://localhost:3000>
- Practice library: <http://localhost:3000/practice>
- Practice session: `http://localhost:3000/lessons/{id}/practice`
- Administrator question manager: <http://localhost:3000/admin/questions>
- API documentation: <http://localhost:8000/docs>
- Backend readiness: <http://localhost:8000/health/ready>
- Buildx builder: `ai-tutor-builder`.

Phase 4 was staged, committed, and pushed after explicit user approval.
