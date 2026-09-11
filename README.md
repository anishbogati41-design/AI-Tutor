# Adaptive Education Web App

An adaptive education platform for students with structured lessons, adaptive practice, progress tracking, study plans, accessibility preferences, and an educational AI tutor. The main application API is a feature-based FastAPI backend backed by PostgreSQL and Redis.

The architecture source of truth is [architet bleuprint.md](architet%20bleuprint.md). Quizzes and text-to-speech are explicitly outside the approved scope.

The complete approved endpoint catalog is documented in [api.md](api.md).

## Implementation status

Phase handoff documents record scope, validation, and continuation state:

- [Phase 1 — Backend and persistence foundation](phases/phase-1.md)
- [Phase 2 — Authentication, users, and frontend auth surface](phases/phase-2.md)

| Phase | Scope | Status |
|---|---|---|
| 1 | Backend and persistence foundation | Complete |
| 2 | Authentication, users, and frontend auth surface | Implemented; awaiting commit approval |
| 3 | Topics, lessons, and admin content | Not started |
| 4 | Questions and adaptive practice records | Not started |
| 5 | Progress and adaptation | Not started |
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

## Configuration

`.env.example` contains safe local defaults. `.env.production.example` lists production inputs without values for secrets. Real `.env` files are ignored by Git.

PostgreSQL is the durable system of record. Redis is restricted to opaque sessions, short-window AI request counters, and daily AI usage counters; Redis persistence is disabled.

## Repository workflow

Each implementation phase has a handoff file under `phases/`. Changes are staged and committed only after explicit approval. This repository must not be pushed or merged unless separately requested.
