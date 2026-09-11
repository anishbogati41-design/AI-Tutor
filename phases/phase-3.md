# Phase 3 — Topics, Lessons, and Admin Content

## Objective

Implement the blueprint's hierarchical topic catalog, lessons with ordered sections, authenticated student read endpoints, and administrator content management endpoints.

## Approved scope

- Hierarchical topics with an optional parent topic.
- Lessons assigned to a subtopic.
- Ordered lesson sections using `INTRODUCTION`, `EXPLANATION`, `EXAMPLE`, or `SUMMARY`.
- Authenticated topic and lesson read endpoints.
- Lesson search and topic filtering.
- Draft lessons visible to administrators and published lessons visible to students.
- Administrator create, update, and delete operations for topics and lessons.
- Student lesson list and section-based lesson viewer in the Next.js frontend.
- Authenticated navigation between lessons and profile settings.
- Redirect to lessons after login and after saving accessibility preferences.
- A four-service Phase 3 Docker Compose runtime.

Questions, practice, progress, AI, study plans, quizzes, text-to-speech, and the remaining frontend pages stay outside this phase.

## Dependencies

- Phase 1 PostgreSQL schema and database connection pool.
- Phase 2 Redis-backed sessions and authenticated/admin dependencies.
- Existing `topics`, `lessons`, and `lesson_sections` tables.

## Implementation checklist

- [x] Add topic models, schemas, repository, service, and student router.
- [x] Add administrator topic CRUD with hierarchy validation.
- [x] Add lesson and lesson-section models and schemas.
- [x] Add lesson repository, service, and student read router.
- [x] Add administrator lesson CRUD with atomic section replacement.
- [x] Register Phase 3 routers with FastAPI.
- [x] Add the student lesson list with search and topic filtering.
- [x] Add the section-based lesson viewer and authenticated application shell.
- [x] Connect login and preference-save navigation to the lesson experience.
- [x] Apply saved accessibility preferences across authenticated pages.
- [x] Add focused unit and live integration coverage.
- [x] Update API and repository documentation.
- [x] Build the Phase 3 backend images with `ai-tutor-builder`.
- [x] Start the four-service local runtime and verify its health.
- [x] Report the completed phase and request approval before staging or committing.

## Validation commands

```bash
python -m compileall backend tests
docker compose -f compose.phase3.yaml run --rm backend python -m pytest -q
docker buildx build --builder ai-tutor-builder --load -f backend/Dockerfile.dev -t ai-tutor-backend:phase-3 .
docker buildx build --builder ai-tutor-builder --load -f backend/Dockerfile -t ai-tutor-backend:phase-3-production .
docker buildx build --builder ai-tutor-builder --load -f frontend/Dockerfile.dev -t ai-tutor-frontend:phase-3 .
docker buildx build --builder ai-tutor-builder --load -f frontend/Dockerfile -t ai-tutor-frontend:phase-3-production .
docker compose -f compose.phase3.yaml up -d --no-build --wait
```

## Handoff state

Status: Implemented and verified; awaiting approval to stage and commit.

### Delivered

- Five authenticated topic and lesson read endpoints.
- Six administrator content endpoints protected by the existing `is_admin` dependency.
- Hierarchical topic validation that rejects missing parents and hierarchy cycles.
- Published-only student lesson visibility while administrators can inspect drafts.
- Lesson search and direct-topic filtering.
- Section-based lesson writes with approved section types, contiguous positions, and atomic replacement on update.
- PostgreSQL conflict handling for topics that remain referenced.
- A responsive student lesson catalog with search, topic filtering, empty and error states.
- A lesson viewer with ordered section navigation and per-session viewed indicators.
- Shared authenticated navigation, logout, and account-wide accessibility styling.
- Login and preference-save redirects into the lesson catalog.
- Phase 3 unit and live integration coverage.
- Development and production backend and frontend images built with `ai-tutor-builder`.
- A four-service Phase 3 local runtime.

### Validation results

- Python compilation: passed.
- Git whitespace/error check: passed.
- Compose configuration validation: passed.
- Backend unit suite: 11 passed, 3 integration tests skipped by default.
- Live PostgreSQL/Redis suite: 14 passed.
- OpenAPI route check: all 11 Phase 3 routes registered.
- Frontend strict TypeScript check: passed.
- Next.js production build: passed.
- Development backend image: built successfully.
- Production backend image and Gunicorn configuration: passed.
- Development and production frontend images: built successfully.
- Frontend route smoke test: unauthenticated `/lessons` redirects to login; authenticated lesson list and viewer routes respond successfully.
- Local containers: frontend, backend, PostgreSQL, and Redis are running.
- Backend readiness: PostgreSQL and Redis both healthy.

### Local runtime

- Frontend: <http://localhost:3000>
- API documentation: <http://localhost:8000/docs>
- Backend readiness: <http://localhost:8000/health/ready>
- Buildx builder: `ai-tutor-builder`.

No Phase 3 changes may be staged or committed without explicit user approval. Do not push or merge these changes.
