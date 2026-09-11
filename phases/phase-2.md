# Phase 2 — Authentication, Users, and Frontend Auth Surface

## Objective

Implement secure email/password authentication, Redis-backed browser sessions, user profile and accessibility preferences, and the corresponding Next.js pages requested for the `frontend/` directory.

## Approved scope

- `POST /auth/register`, `POST /auth/login`, `POST /auth/logout`, and `GET /auth/me`.
- `GET /users/me`, `PUT /users/me`, `GET /users/me/preferences`, and `PUT /users/me/preferences`.
- Password hashing with the Python standard library's scrypt implementation.
- Opaque session identifiers stored in Redis and sent only in an HTTP-only cookie.
- FastAPI authentication and administrator authorization dependencies.
- Credential-aware CORS for the configured frontend origin.
- Next.js registration, login, profile, preference, and logout interfaces.
- TanStack Query, React Hook Form, and Zod integration.
- Frontend navigation middleware based on session-cookie presence; FastAPI remains authoritative.
- A four-service Phase 2 Docker Compose runtime.

Lessons, topics, practice, progress, AI, study plans, and unrelated frontend pages remain in later phases.

## Dependencies

- Phase 1 backend and persistence foundation.
- The existing `users` PostgreSQL table.
- The existing Redis session operations.
- Next.js App Router with TypeScript.
- Tailwind CSS and local shadcn/ui-style components.
- TanStack Query, React Hook Form, and Zod.

## Implementation checklist

- [x] Add user schemas and persistence operations.
- [x] Add scrypt password hashing and verification.
- [x] Add registration, login, logout, and session resolution.
- [x] Add profile and accessibility-preference endpoints.
- [x] Add reusable authenticated-user and administrator dependencies.
- [x] Add credential-aware CORS and secure cookie settings.
- [x] Add backend unit and integration tests.
- [x] Create the Next.js frontend structure.
- [x] Add the shared credential-enabled API wrapper.
- [x] Add registration and login forms.
- [x] Add protected profile and accessibility-preference forms.
- [x] Add navigation middleware and logout behavior.
- [x] Add frontend development and production Dockerfiles.
- [x] Add and validate the four-service Phase 2 Compose runtime.
- [x] Build backend and frontend images with `ai-tutor-builder`.
- [x] Start locally and verify the complete browser/API session flow.
- [x] Update API documentation, README status, and this handoff.

## Validation commands

```bash
python -m compileall backend tests
docker compose -f compose.phase2.yaml run --rm backend python -m pytest -q
docker compose -f compose.phase2.yaml run --rm frontend npm run build
docker buildx build --builder ai-tutor-builder --load -f backend/Dockerfile.dev -t ai-tutor-backend:phase-2 .
docker buildx build --builder ai-tutor-builder --load -f frontend/Dockerfile.dev -t ai-tutor-frontend:phase-2 .
docker compose -f compose.phase2.yaml up -d --no-build --wait
```

## Handoff state

Status: Implemented and verified; awaiting approval to stage and commit.

### Delivered

- Eight Phase 2 REST endpoints for authentication, identity, profile, and accessibility preferences.
- Scrypt password hashing with random salts, constant-time digest comparison, bounded parameters, and uniform verification work for unknown accounts.
- Opaque Redis sessions carried by HTTP-only, `SameSite=Strict` cookies. Production configuration requires secure cookies.
- Reusable FastAPI authenticated-user and administrator dependencies.
- Credential-aware CORS restricted to the configured frontend origin.
- A Next.js App Router frontend with home, registration, login, and protected profile routes.
- React Hook Form and Zod validation, TanStack Query server-state handling, and a single credential-enabled fetch wrapper.
- A Next.js route proxy for navigation convenience; FastAPI remains the authorization authority.
- Development and standalone production Dockerfiles for the frontend.
- A four-service Phase 2 Compose runtime using the existing PostgreSQL volume and nonpersistent Redis.

### Validation results

- Python compilation: passed.
- Git whitespace/error check: passed.
- Compose configuration validation: passed.
- Backend unit suite: 8 passed, 2 integration tests skipped by default.
- Live PostgreSQL/Redis integration suite: 2 passed.
- Browser-equivalent auth smoke flow: registration `201`, login `200`, profile `200`, preference update `200`, logout `204`, and post-logout identity `401`.
- Credentialed CORS preflight: passed.
- Frontend strict TypeScript check: passed.
- Next.js production build: passed with Webpack.
- Development and production backend images: built successfully.
- Development and production frontend images: built successfully.
- Production Gunicorn configuration: passed.
- Local containers: frontend, backend, PostgreSQL, and Redis running; required health checks pass.

### Local runtime

- Frontend: <http://localhost:3000>
- Registration: <http://localhost:3000/register>
- Login: <http://localhost:3000/login>
- Profile and preferences: <http://localhost:3000/profile>
- API documentation: <http://localhost:8000/docs>
- Backend readiness: <http://localhost:8000/health/ready>
- Buildx builder: `ai-tutor-builder`.

No Phase 2 changes may be staged or committed without explicit user approval. Do not push or merge these changes.
