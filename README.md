# Adaptive Education Web App

An adaptive education platform for students with structured lessons, adaptive practice, progress tracking, study plans, accessibility preferences, and an educational AI tutor. The main application API is a feature-based FastAPI backend backed by PostgreSQL and Redis.

The architecture source of truth is [Architet design.md](Architet%20design.md). Quizzes and text-to-speech are explicitly outside the approved scope.

The complete approved endpoint catalog is documented in [api.md](api.md).

## Implementation status

Phase handoff documents record scope, validation, and continuation state:

- [Phase 1 — Backend and persistence foundation](phases/phase-1.md)
- [Phase 2 — Authentication, users, and frontend auth surface](phases/phase-2.md)
- [Phase 3 — Topics, lessons, and admin content](phases/phase-3.md)
- [Phase 4 — Questions and adaptive practice records](phases/phase-4.md)
- [Phase 5 — Progress and adaptation](phases/phase-5.md)
- [Phase 6 — Frontend applications](phases/phase-6.md)
- [Phase 7 — AI tutor and conversations](phases/phase-7.md)

| Phase | Scope | Status |
|---|---|---|
| 1 | Backend and persistence foundation | Complete |
| 2 | Authentication, users, and frontend auth surface | Complete |
| 3 | Topics, lessons, and admin content | Complete |
| 4 | Questions and adaptive practice records | Complete |
| 5 | Progress and adaptation | Implemented and verified; awaiting Git approval |
| 6 | Frontend applications | Not started |
| 7 | AI tutor and conversations | Not started |
| 8 | Study plans | Not started |
| 9 | Local production readiness | Not started |
| 10 | Kubernetes and delivery | Not started |

## Phase 1 local development

Copy the local environment template:

```bash
cp .env.example .env
```

Build and start the backend, PostgreSQL, and Redis:

```bash
docker compose -f compose.phase1.yaml up --build -d
```

The backend is then available at:

- API documentation: <http://localhost:8000/docs>
- Liveness: <http://localhost:8000/health/live>
- Readiness: <http://localhost:8000/health/ready>

Stop the Phase 1 environment with:

```bash
docker compose -f compose.phase1.yaml down
```

The Phase 1 Compose file intentionally runs only the backend and its required data services. Phase 2 introduces the four-service environment; Phase 9 completes its production-readiness work.

## Phase 2 local development

Build and start the frontend, backend, PostgreSQL, and Redis:

```bash
docker compose -f compose.phase2.yaml up --build -d --wait
```

The local services are available at:

- Frontend: <http://localhost:3000>
- Registration: <http://localhost:3000/register>
- Login: <http://localhost:3000/login>
- Profile and preferences: <http://localhost:3000/profile>
- API documentation: <http://localhost:8000/docs>
- Backend readiness: <http://localhost:8000/health/ready>

Stop the Phase 2 environment without removing PostgreSQL data:

```bash
docker compose -f compose.phase2.yaml down
```

## Phase 3 local development

Build and start the frontend, Phase 3 backend, PostgreSQL, and Redis:

```bash
docker compose -f compose.phase3.yaml up --build -d --wait
```

The frontend lesson catalog is available at <http://localhost:3000/lessons>. The API documentation is at <http://localhost:8000/docs>, and backend readiness is at <http://localhost:8000/health/ready>.

Stop the environment without removing PostgreSQL data:

```bash
docker compose -f compose.phase3.yaml down
```

## Phase 4 local development

Build and start the Phase 4 frontend, backend, PostgreSQL, and Redis:

```bash
docker compose -f compose.phase4.yaml up --build -d --wait
```

The Phase 4 interfaces are available at:

- Practice library: <http://localhost:3000/practice>
- Practice session: `http://localhost:3000/lessons/{id}/practice`
- Administrator question manager: <http://localhost:3000/admin/questions>
- API documentation: <http://localhost:8000/docs>
- Backend readiness: <http://localhost:8000/health/ready>

The development backend seeds one published algebra lesson with four sections and three practice questions. The seed is idempotent, runs only in development, and is never invoked by the production image.

Stop the environment without removing PostgreSQL data:

```bash
docker compose -f compose.phase4.yaml down
```

## Phase 5 local development

Build and start the Phase 5 frontend, backend, PostgreSQL, and Redis:

```bash
docker compose -f compose.phase5.yaml up --build -d --wait
```

The Phase 5 interfaces are available at:

- Student dashboard: <http://localhost:3000/dashboard>
- Adaptive practice library: <http://localhost:3000/practice>
- Administrator sign in: <http://localhost:3000/admin-login>
- Administrator students: <http://localhost:3000/admin/students>
- API documentation: <http://localhost:8000/docs>
- Backend readiness: <http://localhost:8000/health/ready>

Stop the environment without removing PostgreSQL data:

```bash
docker compose -f compose.phase5.yaml down
```

## Configuration

`.env.example` contains safe local defaults. `.env.production.example` lists production inputs without values for secrets. Real `.env` files are ignored by Git.

PostgreSQL is the durable system of record. Redis is restricted to opaque sessions, short-window AI request counters, and daily AI usage counters; Redis persistence is disabled.

Administrator sign-in requires email, password, and `ADMIN_LOGIN_PIN`. Local administrator credentials may be seeded with `ADMIN_SEED_EMAIL` and `ADMIN_SEED_PASSWORD`. Their values belong in the ignored `.env` file or deployment secrets and must never be committed.

## Repository workflow

Each implementation phase has a handoff file under `phases/`. Changes are staged and committed only after explicit approval. This repository must not be pushed or merged unless separately requested.
