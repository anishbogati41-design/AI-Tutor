# Phase 6 — Frontend applications

Status: Planned

Owner: Repository owner

## Goal

Complete the approved student and administrator frontend surfaces that are backed by APIs delivered through Phase 5. Preserve the blueprint's responsive layout, accessibility behavior, and feedback patterns.

## Dependencies

- Begin from the reviewed and committed Phase 5 baseline.
- Use the existing Next.js App Router, TypeScript, Tailwind CSS, TanStack Query, React Hook Form, Zod, and `frontend/lib/api.ts`.
- Consume the existing REST endpoints documented in `api.md`.

## Scope

- Build the administrator dashboard at `/admin/dashboard` by aggregating the existing students, lessons, and topics APIs on the client.
- Build administrator lesson management at `/admin/lessons`, including search, topic filtering, status display, deletion confirmation, and navigation to create/edit/question workflows.
- Build the create and edit lesson forms at `/admin/lessons/new` and `/admin/lessons/{id}` with ordered section editing.
- Move or adapt the existing question manager into the blueprint route `/admin/lessons/{id}/questions` while preserving all three approved practice-question types.
- Build the administrator topics manager at `/admin/topics` using the existing topic hierarchy and CRUD APIs.
- Complete the administrator sidebar and role-aware navigation.
- Add the approved quick-access accessibility panel and ensure saved preferences continue to control font size, readable mode, high contrast, and dyslexia mode.
- Finish responsive desktop/mobile navigation, loading states, empty states, error states, confirmation dialogs, and success feedback for the Phase 1–5 screens.
- Review the existing dashboard, lessons, practice, profile, administrator students, and administrator login pages against the frontend blueprint and correct incomplete layouts or navigation.

## Explicit exclusions

- Do not implement AI chat, conversations, SSE handling, or the practice AI side panel; these belong to Phase 7.
- Do not implement study-plan data or the study-plan page; these belong to Phase 8.
- Do not add quizzes, text-to-speech, a teacher portal, new roles, or new backend services.
- Do not add frontend libraries that are absent from the approved architecture.

## File ownership and coordination

- Phase 6 owns the general application shell, administrator shell/navigation, shared non-AI UI components, and administrator content pages.
- Coordinate before editing `frontend/components/app-shell.tsx`, `frontend/app/(student)/lessons/[id]/practice/page.tsx`, `README.md`, `api.md`, or Compose files because Phase 7 may also need them.
- Keep Phase 6 commits limited to frontend application completion and its documentation.

## Task order

1. Audit current routes and components against the frontend blueprint.
2. Complete role-aware student/admin navigation and responsive shells.
3. Implement the administrator dashboard.
4. Implement lesson list, create/edit, ordered sections, and deletion flow.
5. Implement the blueprint-aligned question route using the existing editor.
6. Implement topic hierarchy management.
7. Add accessibility quick controls and shared feedback/state components.
8. Review and polish all Phase 1–5 frontend screens at desktop and mobile widths.
9. Update documentation and record final validation.

## Validation

- Run `npm run typecheck` and the Next.js production build.
- Verify administrator authorization and student/admin navigation manually.
- Exercise topic, lesson, section, and question CRUD against the live backend.
- Verify high-contrast, readable, dyslexia, and font-size modes on the completed pages.
- Verify mobile navigation and core layouts at the blueprint breakpoints.
- Build Phase 6 development and production frontend images with `ai-tutor-builder`.
- Run the four-service stack locally and record all URLs and test results.

## Git handoff

Do not stage or commit without explicit approval. Do not push or merge unless separately requested.
