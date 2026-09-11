# Adaptive Education Web App — Final Architecture Blueprint

## Download

[Download this blueprint](architet%20bleuprint.md)

## 1. Scope and constraints

This is a web-based adaptive education application for students, with an AI tutor and a small admin area. It is built around lessons, practice, static lesson-linked quizzes, adaptive learning signals, progress tracking, study plans, and accessibility preferences.

Only approved functionality is in scope. In particular:

- Text-to-speech is excluded.
- There is no human-teacher portal or multi-role permission system.
- Recommendations are generated from current learning data and are not stored as a separate resource.
- AI-generated practice questions are temporary; they are never written to the official question bank.
- Persistent chat history is retained, but a new AI conversation must not automatically use prior conversations as long-term memory.
- The MVP has no account-deletion endpoint, autoscaling, Helm, Kustomize, or Redis persistence.

## 2. System architecture

```text
Browser
  |
  | HTTPS; secure session cookie
  v
Next.js frontend
  |-- Student application
  |-- Admin application
  |-- Next.js route middleware
  |
  | REST API + Server-Sent Events for streamed AI replies
  v
FastAPI backend
  |-- authentication and authorization
  |-- lessons, topics, questions, quizzes, practice
  |-- adaptive learning and progress
  |-- study-plan rules and AI-readable plan generation
  |-- AI tutor and AI practice help
  |-- admin content and student-progress APIs
  |
  +------------------+-------------------+
  |                  |                   |
  v                  v                   v
PostgreSQL        Redis               OpenAI API
durable data      sessions,           tutor responses,
                  AI rate limits,     explanation styles,
                  daily AI counters   temporary practice items
```

## 3. Technology choices

| Layer | Approved implementation |
|---|---|
| Frontend | Next.js App Router with TypeScript |
| UI | Tailwind CSS and shadcn/ui |
| Server data | TanStack Query |
| Local UI state | React state |
| Forms | React Hook Form and Zod |
| Charts | Recharts |
| Backend | Python and FastAPI |
| API style | REST; Server-Sent Events for streamed AI chat |
| Primary database | PostgreSQL |
| In-memory store | Redis |
| AI provider | OpenAI API |
| Authentication | Email/password plus Redis-backed secure sessions |
| Logging | Python logging |
| Background work | FastAPI background tasks |

## 4. Frontend architecture

### 4.1 Route groups and pages

```text
frontend/src/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   └── register/
│   ├── (student)/
│   │   ├── dashboard/
│   │   ├── lessons/
│   │   ├── practice/
│   │   ├── quiz/
│   │   ├── chat/
│   │   ├── study-plan/
│   │   └── profile/
│   └── (admin)/
│       ├── dashboard/
│       ├── lessons/
│       ├── topics/
│       ├── questions/
│       ├── students/
│       └── student-progress/
├── features/
│   ├── lessons/
│   ├── practice/
│   ├── quiz/
│   ├── chat/
│   ├── progress/
│   └── admin/
├── components/
├── hooks/
├── lib/
│   └── api.ts
└── types/
```

`lib/api.ts` is the single custom wrapper around `fetch`. It must include credentials so the secure session cookie is sent to the backend.

### 4.2 Student experience

- Dashboard: current score, topic accuracy, mastery, weak topics, recent improvement, and study-plan preview.
- Lessons: section-based navigation through introduction, explanation, example, and summary content.
- Practice: one question at a time; after submission, show correctness, explanation, optional AI side panel, then the next question.
- Quiz: one question at a time, with numbered navigation, previous/next controls, and final submission.
- AI chat: ChatGPT-style layout with a conversation sidebar, previous chats, a new-chat action, streamed messages, and an input area.
- Study plan: day/task cards.
- Profile: name, email, and saved accessibility preferences.

Desktop navigation uses a sidebar. Mobile navigation uses a bottom navigation bar. Loading states use skeleton loaders; errors use toast notifications plus inline form errors.

### 4.3 Accessibility

The quick-access accessibility panel and profile/settings page both expose these saved preferences:

- `font_size`
- `readable_mode`
- `high_contrast`
- `dyslexia_mode`

No text-to-speech interface, speech API, or audio asset is included.

### 4.4 Access control

- FastAPI sets an HTTP-only secure session cookie after login.
- Next.js middleware guards student and admin route groups for navigation.
- FastAPI independently authorizes every protected request; frontend protection is never the sole enforcement point.
- Authorization uses `is_admin`: students and administrators are the only approved access levels.

## 5. Backend architecture

Use a feature-based backend. Every feature owns its router, schemas, service logic, and persistence code as needed.

```text
backend/
├── main.py
├── auth/
├── users/
├── lessons/
├── topics/
├── questions/
├── quizzes/
├── adaptive/
├── progress/
├── study_plans/
├── ai_teacher/
├── admin/
├── database/
└── logging/
```

Question-specific logic, including evaluation, stays in `questions/`. Adaptive selection and difficulty logic stays in `adaptive/`.

### 5.1 Authentication and sessions

1. Register with email and password.
2. Authenticate credentials on login.
3. Create a Redis session containing `user_id` and the admin flag.
4. Return the opaque session identifier in a secure session cookie.
5. Resolve the cookie on protected requests and enforce admin access where required.
6. Delete the Redis session on logout.

Redis has no persistence requirement. PostgreSQL remains the durable system of record.

### 5.2 Learning and adaptation rules

- One shared question system supports practice and quiz questions.
- Questions are typed as `MCQ`, `TRUE_FALSE`, or `SHORT_ANSWER`; their usage is `PRACTICE` or `QUIZ`.
- Practice is adaptive; quizzes remain static.
- A static quiz is lesson-linked: quiz questions are identified by the lesson and `question_usage = QUIZ`; no `quizzes` table is used.
- The next practice question is selected by topic and a difficulty band appropriate to the student's mastery.
- Global question difficulty is calculated from student results using:
  - 60% incorrect-answer rate;
  - 25% response-time factor;
  - 15% attempt reliability.
- Student mastery is used to select the next question, not to redefine a question's global difficulty.
- Mastery labels are: Beginner 0–29%, Developing 30–49%, Intermediate 50–69%, Proficient 70–89%, and Mastered 90–100%.
- Weak-topic records retain the metrics that caused the topic to be considered weak.

### 5.3 AI tutor safeguards

- The AI tutor supports multiple explanation styles and educational-only responses.
- General chat and practice-specific AI help are separate API capabilities.
- Chat replies stream to the browser with SSE.
- The backend rate-limits AI endpoints only. Redis maintains per-user short-window limits and daily usage counters.
- Each AI answer has a token limit, and each user has a daily AI request limit.
- Conversation and message records let students reopen prior chats. Old conversations are not injected into a new chat as persistent AI memory.
- FastAPI background tasks may handle approved asynchronous work, such as producing a study-plan presentation for the student.

## 6. Data architecture

### 6.1 PostgreSQL tables

| Table | Approved fields and purpose |
|---|---|
| `users` | `id`, `name`, `email`, `password_hash`, `is_admin`, `font_size`, `readable_mode`, `high_contrast`, `dyslexia_mode`. Stores accounts, admin marker, and accessibility preferences. |
| `topics` | `id`, `name`, `parent_topic_id`, `description`. Self-referencing hierarchy for topics and subtopics. |
| `lessons` | `id`, `title`, `description`, `subtopic_id`, `estimated_minutes`, `is_published`. Each lesson belongs primarily to one subtopic. |
| `lesson_sections` | `id`, `lesson_id`, `section_type`, `title`, `content`, `position`. Ordered structured lesson content. |
| `questions` | `id`, `lesson_id`, `topic_id`, `question_text`, `question_type`, `question_usage`, `difficulty_score`, `explanation`, `accepted_answers`. `accepted_answers` is PostgreSQL `TEXT[]` for short answers. |
| `question_options` | `id`, `question_id`, `option_text`, `is_correct`, `position`. Supports MCQ and True/False; True/False stores `True` and `False` here. |
| `quiz_attempts` | `id`, `user_id`, `lesson_id`, `score`, `total_questions`, `correct_answers`, `response_time_seconds`, `started_at`, `completed_at`. One row per completed quiz attempt. |
| `practice_attempts` | `id`, `user_id`, `lesson_id`, `correct_count`, `total_count`. Summary-level adaptive-practice history. |
| `mastery` | `id`, `user_id`, `topic_id`, `mastery_percentage`, `mastery_label`, `updated_at`. Current mastery only. |
| `weak_topics` | `id`, `user_id`, `topic_id`, `accuracy`, `attempt_count`, `average_difficulty`. Stored weak-topic state and supporting metrics. |
| `study_plans` | `id`, `user_id`. Current saved plan. |
| `study_plan_items` | `id`, `study_plan_id`, `title`, `description`, `scheduled_date`, `position`, `completed`. Ordered, completable plan tasks. |
| `conversations` | `id`, `user_id`, `title`, `created_at`, `updated_at`. Persistent chat index. |
| `messages` | `id`, `conversation_id`, `role`, `content`, `created_at`. `role` is `USER` or `ASSISTANT`. |

### 6.2 Redis key responsibilities

```text
session:{session_id}       -> user_id, is_admin
ai_rate:{user_id}          -> short-window AI request count
ai_daily:{user_id}         -> daily AI usage count
```

## 7. API contract

All endpoints are served by FastAPI. The frontend consumes them through the fetch wrapper.

### 7.1 Authentication and user endpoints

```text
POST /auth/register
POST /auth/login
POST /auth/logout
GET  /auth/me

GET  /users/me
PUT  /users/me
GET  /users/me/preferences
PUT  /users/me/preferences
```

### 7.2 Student learning endpoints

```text
GET  /lessons
GET  /lessons/{id}

GET  /topics
GET  /topics/{id}
GET  /topics/{id}/subtopics

GET  /lessons/{id}/practice
GET  /lessons/{id}/practice/next
POST /practice/{question_id}/answer

POST /lessons/{id}/quiz/start
POST /lessons/{id}/quiz/submit

GET  /progress
GET  /study-plan
POST /study-plan/refresh
```

`GET /progress` returns the combined dashboard payload, including score, topic accuracy, mastery, and weak topics.

### 7.3 AI and conversation endpoints

```text
POST /ai/chat
POST /lessons/{id}/ai-practice

POST   /conversations
GET    /conversations
GET    /conversations/{id}
POST   /conversations/{id}/messages
DELETE /conversations/{id}
```

The general chat endpoint streams response data as Server-Sent Events. The practice endpoint receives lesson/question context and powers the practice side panel.

### 7.4 Admin endpoints

```text
POST   /admin/lessons
PUT    /admin/lessons/{id}
DELETE /admin/lessons/{id}

POST   /admin/topics
PUT    /admin/topics/{id}
DELETE /admin/topics/{id}

POST   /admin/lessons/{id}/questions
PUT    /admin/lessons/{id}/questions/{question_id}
DELETE /admin/lessons/{id}/questions/{question_id}

GET /admin/students
GET /admin/students/{id}/progress
```

Admin lesson editing is section-based. The question editor is a single dynamic form that changes for MCQ, True/False, and short-answer questions.

## 8. Local development with Docker Compose

Docker Compose includes exactly four services:

```text
frontend
backend
postgres
redis
```

Requirements:

- The frontend has separate development and production Dockerfiles.
- The backend has separate development (`uvicorn --reload`) and production (`gunicorn` with Uvicorn workers) execution setups.
- PostgreSQL and Redis use explicitly pinned image versions; no `latest` tag.
- PostgreSQL uses a named persistent volume, `postgres_data`.
- Redis has no persistence volume.
- Services use the default Compose network and service names for internal resolution.
- Separate environment files support local and production configuration.
- Health checks cover backend, PostgreSQL, and Redis.

Required configuration values include database connection details, Redis URL, session secret, OpenAI API credential, backend/frontend URLs, application environment, and AI limit settings. Secrets must stay out of source control.

## 9. Kubernetes deployment

### 9.1 Operational topology

```text
Namespace: adaptive-education

Internet
  |
TLS-enabled Ingress
  |-- /     -> frontend Service -> frontend Deployment (1 replica)
  +-- /api  -> backend Service  -> backend Deployment  (1 replica)

Backend Deployment
  |-- managed PostgreSQL outside the cluster
  +-- Redis Deployment + Service inside the cluster
```

### 9.2 Kubernetes requirements

- Use a dedicated `adaptive-education` namespace.
- Use raw, flat YAML files in `k8s/`; do not use Helm or Kustomize.
- Frontend: Deployment, Service, Ingress routing, one replica, CPU/memory requests and limits, readiness and liveness probes.
- Backend: Deployment and Service, one replica, CPU/memory requests and limits, readiness and liveness probes.
- Redis: deployed inside Kubernetes with a Service; it is not a durable store.
- PostgreSQL: use a managed PostgreSQL service outside Kubernetes.
- Store sensitive values in Kubernetes Secrets and non-sensitive settings in a ConfigMap.
- Use HTTPS/TLS at the Ingress.
- Run database migrations as a Kubernetes Job before or as part of each application deployment.

Suggested flat layout:

```text
k8s/
├── namespace.yaml
├── frontend.yaml
├── backend.yaml
├── redis.yaml
├── ingress.yaml
├── configmap.yaml
├── secrets.yaml
└── migration-job.yaml
```

## 10. Delivery pipeline

GitHub Actions is the approved CI/CD system. The pipeline should:

1. Run frontend and backend tests.
2. Build frontend and backend container images.
3. Publish the images to the selected container registry.
4. Apply the raw Kubernetes manifests.
5. Run the migration Job and verify rollout readiness.

## 11. Implementation sequence

1. Create PostgreSQL schema and Redis session/rate-limit integration.
2. Build authentication, `/auth/me`, user profile, preferences, and backend authorization.
3. Implement topics, lessons, lesson sections, and admin content CRUD.
4. Implement shared questions, answer evaluation, static lesson quizzes, and practice summaries.
5. Implement mastery, weak-topic updates, and adaptive next-question selection.
6. Build student pages and admin pages, then connect them through TanStack Query and `lib/api.ts`.
7. Add persistent conversations, SSE AI chat, practice AI help, rate limits, and cost controls.
8. Build study-plan persistence and refresh logic.
9. Add Compose health checks and environment separation.
10. Deploy the one-replica MVP to Kubernetes through GitHub Actions.
