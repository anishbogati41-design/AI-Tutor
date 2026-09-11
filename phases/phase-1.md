# Phase 1 — Backend and Persistence Foundation

## Objective

Create the smallest runnable backend foundation required by every later phase while preserving the architecture blueprint as the source of truth.

## Approved scope

- Feature-based FastAPI package and application lifecycle.
- Environment-driven local and production configuration.
- PostgreSQL connections and migrations for the approved durable schema.
- Redis access limited to sessions, short-window AI rate limits, and daily AI counters.
- Python logging.
- Liveness and dependency-aware readiness endpoints.
- Focused foundation tests.
- A backend Docker build and a Phase 1 local runtime with PostgreSQL and nonpersistent Redis.

Authentication endpoints, content APIs, adaptive behavior, AI calls, study-plan logic, frontend work, and deployment automation belong to later phases.

## Dependencies

- Python 3.13
- FastAPI
- Uvicorn for development execution
- Gunicorn with Uvicorn workers for production execution
- Psycopg for PostgreSQL access and connection pooling
- redis-py for asynchronous Redis access
- PostgreSQL 17
- Redis 8
- Docker with Buildx and Compose

## Implementation checklist

- [x] Create the backend package and approved feature directories.
- [x] Add validated environment configuration.
- [x] Add PostgreSQL lifecycle and migration runner.
- [x] Create the approved PostgreSQL tables and constraints.
- [x] Add narrowly scoped Redis operations and lifecycle.
- [x] Add logging, liveness, and readiness checks.
- [x] Add development and production backend Dockerfiles.
- [x] Add a Phase 1 Compose runtime.
- [x] Add focused tests.
- [x] Build with the project Docker builder.
- [x] Start locally and verify migrations and health endpoints.
- [x] Update this handoff with results and known follow-ups.

## Validation commands

```bash
python -m compileall backend tests
python -m pytest
docker buildx build --builder ai-tutor-builder --load -f backend/Dockerfile.dev -t ai-tutor-backend:phase-1 .
docker compose -f compose.phase1.yaml up -d
curl --fail http://localhost:8000/health/live
curl --fail http://localhost:8000/health/ready
```

## Handoff state

Status: Complete. Committed locally in `477a7db`.

### Delivered

- The FastAPI application manages PostgreSQL and Redis connections through its lifespan.
- `/health/live` checks the process and `/health/ready` checks both data services.
- Migration `001_initial_schema.sql` creates all 13 approved product tables. The migration runner tracks applied files in `schema_migrations`.
- Redis access exposes only session storage, AI short-window counters, and AI daily counters.
- Local and production configuration templates keep real secrets out of source control.
- Development and production backend images build successfully through `ai-tutor-builder`.
- The Phase 1 Compose runtime starts the backend, PostgreSQL, and nonpersistent Redis.

### Validation results

- Python compilation: passed.
- Git whitespace/error check: passed.
- Compose configuration validation: passed.
- Unit tests: 5 passed, 1 integration test skipped by default.
- Live PostgreSQL/Redis integration test: 1 passed.
- Development image build: passed.
- Production image build and Gunicorn configuration check: passed.
- Database migration: passed; 13 product tables plus `schema_migrations` verified.
- Redis persistence check: RDB snapshotting is empty and AOF is disabled.
- Container health: backend, PostgreSQL, and Redis are healthy.
- Local liveness and readiness requests: HTTP 200.

### Local runtime

- API documentation: <http://localhost:8000/docs>
- Liveness: <http://localhost:8000/health/live>
- Readiness: <http://localhost:8000/health/ready>
- Buildx builder: `ai-tutor-builder` using the `docker-container` driver.

### Known later-phase decision

The approved global question-difficulty formula uses per-question correctness, response time, and attempt reliability. The current source-of-truth schema stores only lesson-level practice summaries. Before Phase 4, the blueprint must define how the per-question measurements are retained or aggregated. Phase 1 does not invent an additional table or field.

Phase 1 was staged and committed with explicit user approval.
