# Phase 5 — Progress and adaptation

Status: Implemented and verified; awaiting Git approval

## Goal

Turn durable practice summaries into visible learning progress and use that progress to choose the next practice question.

## Backend scope

- Apply the approved mastery labels: Beginner, Developing, Intermediate, Proficient, and Mastered.
- Update `mastery` and `weak_topics` after each submitted practice answer.
- Recalculate global question difficulty from aggregate student results using the blueprint weights.
- Implement adaptive selection at `GET /lessons/{id}/practice/next`.
- Implement the combined student dashboard payload at `GET /progress`.
- Implement `GET /admin/students` and `GET /admin/students/{id}/progress`.

## Frontend scope

- Add the student dashboard and connect it to `GET /progress`.
- Change the practice session to request one adaptive question at a time.
- Add administrator student list and student progress views.
- Wire dashboard and student-management navigation and make the dashboard the post-login destination.

## Constraints

- PostgreSQL remains the durable store. Redis remains limited to sessions and later AI counters/rate limits.
- Authentication continues to use the secure Redis-backed session cookie.
- APIs remain REST-based. No quiz resource or text-to-speech feature is introduced.
- The approved summary-level `practice_attempts` schema does not store per-question timing. Until an approved schema supplies response times, the global difficulty calculation uses a neutral response-time factor and documents that behavior in `api.md`.

## Validation and completion

- [x] Add focused backend tests for mastery boundaries, progress aggregation, access control, and adaptive selection.
- [x] Run backend tests and frontend type/build checks.
- [x] Build Phase 5 images with the existing `ai-tutor-builder` Docker Buildx builder.
- [x] Run the Phase 5 stack locally and verify its health and core browser/API flows.
- [x] Update `README.md`, `api.md`, and this file with the delivered state and validation evidence.
- [x] Leave changes unstaged until the user explicitly approves staging and committing.

## Delivered

- Practice answers now update durable mastery and weak-topic state and recalculate the answered question's global difficulty.
- Adaptive practice selects a question nearest the difficulty target for the student's current mastery band.
- Student question payloads continue to hide explanations and correct-answer markers.
- `/progress` combines overall score, topic accuracy, mastery, weak topics, recent improvement, and study-plan preview fields.
- Administrator APIs list students and show the same progress shape for an individual student.
- Administrator sign-in requires email, password, and a private PIN held only in environment configuration; regular login rejects administrator accounts.
- Administrator student details show each published course, practice attempts, correct answers, accuracy, and summary-based progression.
- The frontend includes a real student dashboard, one-question-at-a-time adaptive practice, an administrator student list, and student progress detail.
- Login and saved-preference flows now lead to the dashboard, and the sidebar exposes every Phase 5 screen allowed by the current role.
- `compose.phase5.yaml` runs the Phase 5 frontend, backend, PostgreSQL, and Redis images.

## Validation results

- Python compilation: passed.
- Git whitespace/error check: passed.
- Compose configuration: passed.
- Default backend suite: 16 passed, 4 live integration tests skipped.
- Live PostgreSQL/Redis suite: 20 passed.
- Frontend strict TypeScript check: passed.
- Next.js production build: passed; dashboard and both administrator student routes generated.
- Backend, frontend, PostgreSQL, and Redis services: running and healthy.
- Live readiness, authentication, adaptive question, answer submission, and updated progress smoke flows: passed.
- Development and production backend/frontend images: built with `ai-tutor-builder`.

## Local runtime

- Frontend: <http://localhost:3000>
- Student dashboard: <http://localhost:3000/dashboard>
- Adaptive practice library: <http://localhost:3000/practice>
- Starter lesson practice: <http://localhost:3000/lessons/8/practice>
- Administrator sign in: <http://localhost:3000/admin-login>
- Administrator students: <http://localhost:3000/admin/students>
- API documentation: <http://localhost:8000/docs>
- Backend readiness: <http://localhost:8000/health/ready>
- Buildx builder: `ai-tutor-builder`

All Phase 5 files remain unstaged. Staging and committing require explicit user approval; pushing or merging requires a separate request.
