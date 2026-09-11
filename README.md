# Adaptive Education Web App

An adaptive education platform for students with structured lessons, adaptive practice, progress tracking, study plans, accessibility preferences, and an educational AI tutor. The main application API is a feature-based FastAPI backend backed by PostgreSQL and Redis.

The architecture source of truth is [architet bleuprint.md](architet%20bleuprint.md). Quizzes and text-to-speech are explicitly outside the approved scope.

The complete approved endpoint catalog is documented in [api.md](api.md).

## Implementation status

Phase 1 builds the backend and persistence foundation. Its durable handoff document is [phases/phase-1.md](phases/phase-1.md).

| Phase | Scope | Status |
|---|---|---|
| 1 | Backend and persistence foundation | Implemented; awaiting commit approval |
| 2 | Authentication and users | Not started |
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

The Phase 1 Compose file intentionally runs only the backend and its required data services. Phase 9 completes the blueprint's four-service environment after the Next.js frontend exists.

## Configuration

`.env.example` contains safe local defaults. `.env.production.example` lists production inputs without values for secrets. Real `.env` files are ignored by Git.

PostgreSQL is the durable system of record. Redis is restricted to opaque sessions, short-window AI request counters, and daily AI usage counters; Redis persistence is disabled.

## Repository workflow

Each implementation phase has a handoff file under `phases/`. Changes are staged and committed only after explicit approval. This repository must not be pushed or merged unless separately requested.
