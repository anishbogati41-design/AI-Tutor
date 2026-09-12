# Phase 8 — Study plans

Status: Implemented and verified

Owner: Primary implementation

## Goal

Generate and persist an ordered study plan from each student's current learning data, expose the two approved study-plan endpoints, and add the approved read-only study-plan interface.

## Dependencies

- Use the existing PostgreSQL `study_plans` and `study_plan_items` tables.
- Read current published lessons, mastery, weak-topic state, and practice summaries as generation inputs.
- Preserve the existing Phase 7 worktree changes; Phase 8 does not alter AI-provider behavior.

## Backend scope

- Implement owned study-plan models, schemas, repository, service, and router.
- Implement `GET /study-plan` and `POST /study-plan/refresh`.
- Return `null` when the current student has not generated a plan.
- Replace the current student's plan items atomically on refresh.
- Prioritize weak topics, then lower mastery and lower practice coverage.
- Generate ordered dated items from current learning data only.
- Store the plan and its items, but do not create a separate recommendation resource.

## Frontend scope

- Add `/study-plan` with loading, error, empty, populated, and refresh states.
- Group ordered items by `scheduled_date`.
- Confirm before replacing the current plan and keep it visible if refresh fails.
- Display the stored completion state as read-only; do not add an unapproved completion endpoint.
- Add Study Plan to authenticated student navigation and middleware protection.
- Populate the dashboard's existing study-plan preview from the generated plan items.

## Approved endpoints

- `GET /study-plan`
- `POST /study-plan/refresh`

## Explicit exclusions

- Do not add a recommendation table or endpoint.
- Do not add `PATCH /study-plan/items/{id}` or another completion mutation.
- Do not add action fields or lesson foreign keys absent from the approved durable schema.
- Do not use AI-provider calls to generate the plan.
- Do not change FastAPI, PostgreSQL, Redis, authentication, or frontend architecture.

## Validation

- Test recommendation ordering and generated item content.
- Test owned plan retrieval and atomic replacement with PostgreSQL.
- Test authentication boundaries for both endpoints.
- Run backend unit/integration tests, frontend typecheck, and the production build.

## Git handoff

The repository owner explicitly approved staging, committing, and pushing the remaining work after validation.

## Validation result

- Backend unit and live PostgreSQL/Redis/Ollama integration suite: `33 passed`.
- Study-plan authentication, ownership, recommendation ordering, retrieval, and atomic replacement: passed against live PostgreSQL.
- Frontend TypeScript check: passed.
- Production Next.js build: passed and generated `/study-plan`.
- The five-service Docker stack is running; backend readiness reports PostgreSQL and Redis healthy, and the local Ollama model is ready.
- Python compilation and `git diff --check`: passed.
