1. Design Foundation

1.1 Color System
text

┌─────────────────────────────────────────────────────────────────┐
│                        COLOR PALETTE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Primary (Indigo)                                               │
│  ┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐                     │
│  │  50  ││ 100  ││ 500  ││ 600  ││ 700  │                     │
│  │#EEF2F││#E0E7F││#6366F││#4F46E││#4338C│                     │
│  │ bg   ││hover ││main  ││hover ││active│                     │
│  └──────┘└──────┘└──────┘└──────┘└──────┘                     │
│                                                                 │
│  Success          Warning          Error           Info         │
│  ┌──────┐         ┌──────┐         ┌──────┐        ┌──────┐   │
│  │#10B98│         │#F59E0│         │#EF444│        │#3B82F│   │
│  │Green │         │Amber │         │Red   │        │Blue  │   │
│  └──────┘         └──────┘         └──────┘        └──────┘   │
│                                                                 │
│  Neutrals                                                       │
│  ┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐   │
│  │  50  ││ 100  ││ 200  ││ 400  ││ 600  ││ 800  ││ 950  │   │
│  │#F9FAF││#F3F4F││#E5E7E││#9CA3A││#4B556││#1F293││#030712│   │
│  │page  ││card  ││border││muted ││body  ││head  ││darkbg│   │
│  └──────┘└──────┘└──────┘└──────┘└──────┘└──────┘└──────┘   │
│                                                                 │
│  Mastery Levels (from GET /progress → mastery[].label)         │
│  ┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐                     │
│  │Begin ││Devel ││Inter ││Profi ││Maste │                     │
│  │#EF444││#F97316││#EAB308││#22C55E││#6366F1│                  │
│  │0-29% ││30-49%││50-69%││70-89%││90-100│                     │
│  └──────┘└──────┘└──────┘└──────┘└──────┘                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

1.2 Typography Scale
text

┌─────────────────────────────────────────────────────────────────┐
│                      TYPOGRAPHY SCALE                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Font Family: Inter (default) / OpenDyslexic (dyslexia mode)   │
│  Controlled by GET /users/me/preferences → dyslexia_mode        │
│                                                                 │
│  ┌─────────┬──────────┬────────┬──────────────────────────┐    │
│  │ Token   │ Default  │ Large  │ Usage                    │    │
│  ├─────────┼──────────┼────────┼──────────────────────────┤    │
│  │ h1      │ 30px/700 │ 36px   │ Page titles              │    │
│  │ h2      │ 24px/600 │ 28px   │ Section headers          │    │
│  │ h3      │ 20px/600 │ 24px   │ Card titles              │    │
│  │ body    │ 16px/400 │ 20px   │ Body text                │    │
│  │ body-sm │ 14px/400 │ 18px   │ Secondary text           │    │
│  │ caption │ 12px/500 │ 16px   │ Labels, badges           │    │
│  └─────────┴──────────┴────────┴──────────────────────────┘    │
│                                                                 │
│  Line Height: 1.6 (body), 1.3 (headings)                       │
│  Readable Mode: max-width 680px, line-height 1.8               │
│  (Driven by preferences.readable_mode + font_size)             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

1.3 Spacing & Radius
text

┌──────────────────────────────────────┐
│           SPACING TOKENS             │
├──────────────────────────────────────┤
│  4px   xs   (icon padding)          │
│  8px   sm   (inline gaps)           │
│  12px  md   (card padding inner)    │
│  16px  lg   (section gaps)          │
│  24px  xl   (card padding)          │
│  32px  2xl  (section spacing)       │
│  48px  3xl  (page section gaps)     │
├──────────────────────────────────────┤
│           BORDER RADIUS              │
├──────────────────────────────────────┤
│  4px   sm   (badges, chips)         │
│  8px   md   (buttons, inputs)       │
│  12px  lg   (cards)                 │
│  16px  xl   (modals, panels)        │
│  9999  full (avatars, dots)         │
└──────────────────────────────────────┘

2. Layout System

2.1 Desktop Layout (≥1024px)
text

┌──────────────────────────────────────────────────────────────────────┐
│ ┌────────────┐ ┌──────────────────────────────────────────────────┐ │
│ │            │ │  Header Bar                              🔔 👤  │ │
│ │   ┌────┐   │ │  (👤 name from GET /auth/me)                    │ │
│ │   │logo│   │ ├──────────────────────────────────────────────────┤ │
│ │   └────┘   │ │                                                  │ │
│ │            │ │                                                  │ │
│ │  ━━━━━━━━  │ │                                                  │ │
│ │  📊 Dash   │ │              MAIN CONTENT AREA                   │ │
│ │  📚 Learn  │ │                                                  │ │
│ │  ✏️ Pract  │ │           max-width: 1200px                      │ │
│ │  🤖 Chat   │ │           padding: 24px                          │ │
│ │  📅 Plan   │ │                                                  │ │
│ │  ━━━━━━━━  │ │                                                  │ │
│ │  👤 Prof   │ │                                                  │ │
│ │  ♿ A11y   │ │                                                  │ │
│ │            │ │                                                  │ │
│ │  w: 260px  │ │                                                  │ │
│ └────────────┘ └──────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘

2.2 Mobile Layout (<1024px)
text

┌──────────────────────────┐
│  ☰  App Name     🔔  👤  │  ← Top bar with hamburger
├──────────────────────────┤
│                          │
│                          │
│    MAIN CONTENT AREA     │
│                          │
│    Full width            │
│    padding: 16px         │
│                          │
│                          │
├──────────────────────────┤
│ 📊   📚   ✏️   🤖   ≡  │  ← Bottom navigation bar
│Dash  Learn Prac Chat More│     56px height
└──────────────────────────┘

2.3 Sidebar Detail
text

┌──────────────────┐
│                  │
│   ┌──────────┐   │
│   │  ◆ Edu   │   │  Logo + app name
│   │  Adapt   │   │
│   └──────────┘   │
│                  │
│ ─────────────── │
│                  │
│  ┌──────────────┐│
│  │ 📊 Dashboard ││  → /dashboard (GET /progress)
│  └──────────────┘│
│  ┌──────────────┐│
│  │ 📚 Lessons   ││  → /lessons (GET /lessons)
│  └──────────────┘│
│  ┌──────────────┐│
│  │ ✏️ Practice  ││  → /lessons (pick lesson to practice)
│  └──────────────┘│
│  ┌──────────────┐│
│  │ 🤖 AI Tutor  ││  → /chat (GET /conversations)
│  └──────────────┘│
│  ┌──────────────┐│
│  │ 📅 Plan      ││  → /study-plan (GET /study-plan)
│  └──────────────┘│
│                  │
│ ─────────────── │
│                  │
│  ┌──────────────┐│
│  │ 👤 Profile   ││  → /profile (GET /users/me)
│  └──────────────┘│
│  ┌──────────────┐│
│  │ ♿ Access.   ││  → Opens A11y panel (uses prefs API)
│  └──────────────┘│
│                  │
│ ─────────────── │
│  ┌──────────────┐│
│  │ 🚪 Logout    ││  → POST /auth/logout
│  └──────────────┘│
└──────────────────┘

Active state: bg primary-50, left border 3px primary-500,
              text primary-700
Default:      text neutral-600, hover bg neutral-100

3. Authentication Pages

3.1 Login Page
API: POST /auth/login → sets session cookie → redirect to /dashboard

text

┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│                      bg: gradient primary-50 to white                │
│                                                                      │
│                         ┌──────────────────┐                         │
│                         │    ◆ EduAdapt    │                         │
│                         │                  │                         │
│                         │  Welcome back!   │                         │
│                         │  Sign in to      │                         │
│                         │  continue your   │                         │
│                         │  learning.       │                         │
│                         │                  │                         │
│                         │ ┌──────────────┐ │                         │
│                         │ │ 📧 Email     │ │                         │
│                         │ └──────────────┘ │                         │
│                         │                  │                         │
│                         │ ┌──────────────┐ │                         │
│                         │ │ 🔒 Password  │ │                         │
│                         │ │          👁️  │ │                         │
│                         │ └──────────────┘ │                         │
│                         │                  │                         │
│                         │ ┌──────────────┐ │                         │
│                         │ │   Sign In    │ │  → POST /auth/login    │
│                         │ └──────────────┘ │                         │
│                         │                  │                         │
│                         │  Don't have an   │                         │
│                         │  account?        │                         │
│                         │  Register →      │                         │
│                         │                  │                         │
│                         │  Card: 420px     │                         │
│                         │  shadow-lg       │                         │
│                         │  rounded-xl      │                         │
│                         └──────────────────┘                         │
└──────────────────────────────────────────────────────────────────────┘

3.2 Register Page
API: POST /auth/register → auto-login → redirect to /dashboard

text

┌──────────────────────────────────────────────────────────────────────┐
│                         ┌──────────────────┐                         │
│                         │    ◆ EduAdapt    │                         │
│                         │                  │                         │
│                         │  Create your     │                         │
│                         │  account         │                         │
│                         │                  │                         │
│                         │ ┌──────────────┐ │                         │
│                         │ │ 👤 Full Name │ │  → payload.name         │
│                         │ └──────────────┘ │                         │
│                         │ ┌──────────────┐ │                         │
│                         │ │ 📧 Email     │ │  → payload.email        │
│                         │ └──────────────┘ │                         │
│                         │ ┌──────────────┐ │                         │
│                         │ │ 🔒 Password  │ │  → payload.password     │
│                         │ └──────────────┘ │                         │
│                         │                  │                         │
│                         │  Password must:  │  ← Zod-validated        │
│                         │  ✅ 8+ chars     │     client-side only    │
│                         │  ✅ 1 uppercase  │                         │
│                         │  ❌ 1 number     │                         │
│                         │                  │                         │
│                         │ ┌──────────────┐ │                         │
│                         │ │ 🔒 Confirm   │ │  ← client-side compare  │
│                         │ └──────────────┘ │                         │
│                         │                  │                         │
│                         │ ┌──────────────┐ │                         │
│                         │ │  Register    │ │  → POST /auth/register  │
│                         │ └──────────────┘ │                         │
│                         │                  │                         │
│                         │  Already have    │                         │
│                         │  an account?     │                         │
│                         │  Sign in →       │                         │
│                         └──────────────────┘                         │
└──────────────────────────────────────────────────────────────────────┘

3.3 Form Validation States
text

  Default Input                  Error Input                   Success Input
┌──────────────────┐          ┌──────────────────┐          ┌──────────────────┐
│ 📧 Email         │          │ 📧 Email         │          │ 📧 Email       ✓ │
│ border: gray-300 │          │ border: red-500  │          │ border: green-500│
└──────────────────┘          ├──────────────────┤          └──────────────────┘
                              │ ⚠ Invalid email  │
                              │   format         │
                              └──────────────────┘
                                text: red-600
                                font: caption

Error text may come from:
  - Client (Zod): "Invalid email format"
  - Server (ApiError.message from POST /auth/login 401)

4. Student Dashboard

Primary API: GET /progress returns the combined payload:

JSON

{
  "overall_score": 78,
  "topic_accuracy": [...],
  "mastery": [{ "topic_id, topic_name, mastery_percentage, mastery_label" }],
  "weak_topics": [{ "topic_id, topic_name, accuracy, attempt_count, average_difficulty" }]
}
Secondary API: GET /study-plan for the plan preview widget.

4.1 Full Dashboard Layout
text

┌─────────┐┌──────────────────────────────────────────────────────────┐
│         ││ Dashboard                                    🔔  👤 Ali │
│ Sidebar ││──────────────────────────────────────────────────────────│
│         ││                                                          │
│         ││ Welcome back, {user.name}! 👋                            │
│         ││ Here's your learning overview.                           │
│         ││                                                          │
│         ││ ┌──────────────────┐ ┌──────────────────┐               │
│         ││ │ 🎯 Overall Score │ │ 📚 Topics        │               │
│         ││ │                  │ │    Tracked       │               │
│         ││ │      78%         │ │       12         │               │
│         ││ │ from /progress   │ │ mastery[].length │               │
│         ││ └──────────────────┘ └──────────────────┘               │
│         ││                                                          │
│         ││ ┌──────────────────┐ ┌──────────────────┐               │
│         ││ │ ⚠️  Weak Topics   │ │ 🏆 Mastered      │               │
│         ││ │                  │ │    Topics        │               │
│         ││ │        2         │ │       3          │               │
│         ││ │ weak_topics.len  │ │ mastery≥90 count │               │
│         ││ └──────────────────┘ └──────────────────┘               │
│         ││                                                          │
│         ││ ┌────────────────────────────┐ ┌────────────────────────┐│
│         ││ │  Topic Mastery Overview    │ │  Weak Topics           ││
│         ││ │  (from mastery[])          │ │  (from weak_topics[])  ││
│         ││ │                            │ │                        ││
│         ││ │  Algebra              85%  │ │  ⚠️ Quadratic Eqns    ││
│         ││ │  ████████████░░░  Profic.  │ │  Accuracy: 42%        ││
│         ││ │                            │ │  Attempts: 8          ││
│         ││ │  Geometry             65%  │ │  Avg Diff: 0.6        ││
│         ││ │  ██████████░░░░  Interm.   │ │  ┌──────────────┐     ││
│         ││ │                            │ │  │ Practice Now │     ││
│         ││ │  Calculus             35%  │ │  └──────────────┘     ││
│         ││ │  █████░░░░░░░░  Developing │ │  → /lessons filtered  ││
│         ││ │                            │ │    by topic_id        ││
│         ││ │  Statistics           92%  │ │                        ││
│         ││ │  █████████████  Mastered   │ │  ⚠️ Trigonometry       ││
│         ││ │                            │ │  Accuracy: 38%        ││
│         ││ │                            │ │  Attempts: 5          ││
│         ││ │                            │ │  Avg Diff: 0.5        ││
│         ││ │                            │ │  ┌──────────────┐     ││
│         ││ │                            │ │  │ Practice Now │     ││
│         ││ │                            │ │  └──────────────┘     ││
│         ││ └────────────────────────────┘ └────────────────────────┘│
│         ││                                                          │
│         ││ ┌────────────────────────────┐ ┌────────────────────────┐│
│         ││ │  Topic Accuracy            │ │  Study Plan Preview    ││
│         ││ │  (from topic_accuracy[])   │ │  (from GET /study-plan)││
│         ││ │  ┌──────────────────────┐  │ │                        ││
│         ││ │  │    Recharts Bar      │  │ │  📅 Next 3 tasks       ││
│         ││ │  │  █ █ █ █ █ █ █      │  │ │  □ Review Quadratics   ││
│         ││ │  │  Alg Geo Cal ...     │  │ │  □ Practice: Algebra   ││
│         ││ │  └──────────────────────┘  │ │  □ Lesson: Derivatives ││
│         ││ │                            │ │                        ││
│         ││ │  Accuracy per topic (%)    │ │  ┌──────────────┐     ││
│         ││ └────────────────────────────┘ │  │  View Plan   │     ││
│         ││                                │  └──────────────┘     ││
│         ││                                └────────────────────────┘│
│         │└──────────────────────────────────────────────────────────┘
└─────────┘

4.2 Stats Card Component
text

  ┌────────────────────────────┐
  │                            │
  │  ┌────┐                   │
  │  │ 🎯 │  Overall Score    │
  │  └────┘                   │
  │                            │
  │  78%                       │  ← progress.overall_score
  │                            │
  │  bg: white                 │
  │  shadow: sm                │
  │  rounded: lg               │
  │  padding: 24px             │
  │  border: 1px neutral-200   │
  └────────────────────────────┘

Note: "↑ 5% from last week" trend removed —
      /progress does not return historical deltas.

4.3 Mastery Bar Component
text

  Algebra                                             85%  Proficient
  ┌────────────────────────────────────────────────────────────────┐
  │████████████████████████████████████████████░░░░░░░░░░░░░░░░░░│
  └────────────────────────────────────────────────────────────────┘
  bg: neutral-100    fill: green-500 (Proficient)     rounded-full

  Data source: mastery[i].mastery_percentage + mastery[i].mastery_label

  Color mapping (label → color):
  Beginner     → red-500
  Developing   → orange-500
  Intermediate → yellow-500
  Proficient   → green-500
  Mastered     → indigo-500

5. Lessons Experience

5.1 Lesson List Page

API: GET /lessons (supports ?search=&topic_id= query params)

text

┌─────────┐┌──────────────────────────────────────────────────────────┐
│         ││ Lessons                                                   │
│ Sidebar ││──────────────────────────────────────────────────────────│
│         ││                                                          │
│         ││ ┌───────────────────────────────────────────────────────┐│
│         ││ │ 🔍 Search lessons...        (debounced ?search=)     ││
│         ││ └───────────────────────────────────────────────────────┘│
│         ││                                                          │
│         ││ Topic: All ▼    (options from GET /topics)               │
│         ││   → applies ?topic_id= filter                            │
│         ││                                                          │
│         ││ ┌─────────────────────┐  ┌─────────────────────┐        │
│         ││ │                     │  │                     │        │
│         ││ │  📘 Introduction    │  │  📘 Quadratic       │        │
│         ││ │     to Algebra      │  │     Equations       │        │
│         ││ │                     │  │                     │        │
│         ││ │  Topic: Algebra     │  │  Topic: Algebra     │        │
│         ││ │  ⏱ 15 min          │  │  ⏱ 25 min          │        │
│         ││ │  (from lesson.est_  │  │                     │        │
│         ││ │   estimated_minutes)│  │                     │        │
│         ││ │                     │  │                     │        │
│         ││ │  ┌───────────────┐  │  │  ┌───────────────┐  │        │
│         ││ │  │ View Lesson → │  │  │  │ View Lesson → │  │        │
│         ││ │  └───────────────┘  │  │  └───────────────┘  │        │
│         ││ │  → /lessons/{id}    │  │  → /lessons/{id}    │        │
│         ││ └─────────────────────┘  └─────────────────────┘        │
│         ││                                                          │
│         ││ ┌─────────────────────┐  ┌─────────────────────┐        │
│         ││ │  📘 Derivatives     │  │  📘 Probability     │        │
│         ││ │     Basics          │  │     Theory          │        │
│         ││ │  ...                │  │  ...                │        │
│         ││ └─────────────────────┘  └─────────────────────┘        │
│         │└──────────────────────────────────────────────────────────┘
└─────────┘

5.2 Lesson Viewer (Section-Based)

API: GET /lessons/{id} returns lesson + ordered sections[]

text

┌─────────┐┌──────────────────────────────────────────────────────────┐
│         ││ ← Back to Lessons                                        │
│ Sidebar ││──────────────────────────────────────────────────────────│
│         ││                                                          │
│         ││ ┌─────────┐┌─────────────────────────────────────────────┐
│         ││ │ Section ││ │                                            │
│         ││ │  Nav    ││ │  Introduction to Quadratic Equations      │
│         ││ │         ││ │                                            │
│         ││ │ ● Intro ││ │  ⏱ 25 min  •  Topic: Algebra             │
│         ││ │ ○ Expl. ││ │                                            │
│         ││ │ ○ Exampl││ │  ─────────────────────────────────────    │
│         ││ │ ○ Summ. ││ │                                            │
│         ││ │         ││ │  (Renders lesson.sections[current].content)│
│         ││ │ (Client ││ │                                            │
│         ││ │  side   ││ │  A quadratic equation is a second-        │
│         ││ │  index) ││ │  degree polynomial equation in a          │
│         ││ │         ││ │  single variable x:                       │
│         ││ │ ● = viewed│ │                                            │
│         ││ │   this  ││ │     ax² + bx + c = 0                      │
│         ││ │   session│ │                                            │
│         ││ │ ○ = not ││ │  ┌─────────────────────────────────┐      │
│         ││ │   yet   ││ │  │ 💡 Key Concept                  │      │
│         ││ │         ││ │  │                                 │      │
│         ││ │         ││ │  │ The graph of a quadratic        │      │
│         ││ │         ││ │  │ equation is always a parabola.  │      │
│         ││ │         ││ │  └─────────────────────────────────┘      │
│         ││ │         ││ │                                            │
│         ││ │         ││ │        ┌──────────┐  ┌──────────┐         │
│         ││ │         ││ │        │ ← Prev   │  │ Next →   │         │
│         ││ │         ││ │        └──────────┘  └──────────┘         │
│         ││ └─────────┘│ └──────────────────────────────────────────┘│
│         ││                                                          │
│         ││ After last section (client detects last index):          │
│         ││ ┌────────────────────────────────────────────────────────┐│
│         ││ │  🎉 You've reached the end of this lesson!             ││
│         ││ │                                                        ││
│         ││ │  ┌──────────────┐  ┌──────────────┐                   ││
│         ││ │  │  Practice    │  │ Back to      │                   ││
│         ││ │  │              │  │ Lessons      │                   ││
│         ││ │  └──────────────┘  └──────────────┘                   ││
│         ││ │  → /lessons/{id}      → /lessons                       ││
│         ││ │    /practice                                           ││
│         ││ └────────────────────────────────────────────────────────┘│
│         │└──────────────────────────────────────────────────────────┘
└─────────┘

5.3 Section Navigation (Mobile Collapsed)
text

  ┌──────────────────────────────────┐
  │  Sections                    ▼   │   ← Collapsible on mobile
  ├──────────────────────────────────┤
  │  ● 1. Introduction               │   ● = viewed this session
  │  ● 2. Explanation                │   ○ = not yet
  │  ○ 3. Examples                   │
  │  ○ 4. Summary                    │
  └──────────────────────────────────┘

6. Practice Mode

APIs used:

GET /lessons/{id}/practice — session/summary info
GET /lessons/{id}/practice/next — fetch next adaptive question
POST /practice/{question_id}/answer — submit answer, get result
POST /lessons/{id}/ai-practice — AI help for a specific question

6.1 Practice Session Layout
text

┌─────────┐┌──────────────────────────────────────────────────────────┐
│         ││ Practice: Quadratic Equations                             │
│ Sidebar ││──────────────────────────────────────────────────────────│
│         ││                                                          │
│         ││  Topic: Algebra  •  Difficulty: Medium                   │
│         ││  (question.topic + question.difficulty_score band)       │
│         ││                                                          │
│         ││  Session progress (client-tracked):                      │
│         ││  Answered: 4  •  Correct: 3                              │
│         ││  ┌──────────────────────────────────────────────────┐    │
│         ││  │(Local counter for this browser session only)      │    │
│         ││  └──────────────────────────────────────────────────┘    │
│         ││                                                          │
│         ││ ┌────────────────────────────────────────────────────────┐│
│         ││ │                                                        ││
│         ││ │  (question.question_text from                          ││
│         ││ │   GET /lessons/{id}/practice/next)                     ││
│         ││ │                                                        ││
│         ││ │  What is the discriminant of the quadratic equation    ││
│         ││ │  2x² + 5x - 3 = 0?                                     ││
│         ││ │                                                        ││
│         ││ │  (Component picks MCQ/TF/SA renderer based on          ││
│         ││ │   question.question_type)                              ││
│         ││ │                                                        ││
│         ││ │  ┌─────────────────────────────────────────┐          ││
│         ││ │  │  ○  A)  19                              │          ││
│         ││ │  └─────────────────────────────────────────┘          ││
│         ││ │  ┌─────────────────────────────────────────┐          ││
│         ││ │  │  ◉  B)  49                              │ ← selected│
│         ││ │  │      border: 2px primary-500            │          ││
│         ││ │  │      bg: primary-50                     │          ││
│         ││ │  └─────────────────────────────────────────┘          ││
│         ││ │  ┌─────────────────────────────────────────┐          ││
│         ││ │  │  ○  C)  -1                              │          ││
│         ││ │  └─────────────────────────────────────────┘          ││
│         ││ │  ┌─────────────────────────────────────────┐          ││
│         ││ │  │  ○  D)  31                              │          ││
│         ││ │  └─────────────────────────────────────────┘          ││
│         ││ │                                                        ││
│         ││ │          ┌──────────────────────┐                     ││
│         ││ │          │   Submit Answer      │                     ││
│         ││ │          └──────────────────────┘                     ││
│         ││ │  → POST /practice/{question_id}/answer                 ││
│         ││ │    { answer: selectedValue }                           ││
│         ││ │                                                        ││
│         ││ └────────────────────────────────────────────────────────┘│
│         │└──────────────────────────────────────────────────────────┘
└─────────┘

6.2 After Submission — Correct Answer
Response from POST /practice/{question_id}/answer:

JSON

{ "is_correct": true, "correct_answer": "49", "explanation": "..." }
text

│ ┌────────────────────────────────────────────────────────────────┐ │
│ │                                                                │ │
│ │  ✅ Correct!                                    ┌────────────┐ │ │
│ │                                                 │ 🤖 Ask AI  │ │ │
│ │  (result.is_correct === true)                   │   Tutor    │ │ │
│ │                                                 └────────────┘ │ │
│ │                                                 → opens 6.4     │ │
│ │                                                 slide-in panel  │ │
│ │                                                                │ │
│ │  ┌──────────────────────────────────────────────────────────┐  │ │
│ │  │ 💡 Explanation                                           │  │ │
│ │  │                                                          │  │ │
│ │  │ (result.explanation)                                     │  │ │
│ │  │                                                          │  │ │
│ │  │ The discriminant formula Δ = b² - 4ac determines the     │  │ │
│ │  │ nature of roots. When Δ > 0, the equation has two        │  │ │
│ │  │ distinct real roots.                                     │  │ │
│ │  │                                                          │  │ │
│ │  │ bg: green-50  border-left: 4px green-500                 │  │ │
│ │  └──────────────────────────────────────────────────────────┘  │ │
│ │                                                                │ │
│ │               ┌─────────────────────┐                          │ │
│ │               │   Next Question →   │                          │ │
│ │               └─────────────────────┘                          │ │
│ │  → GET /lessons/{id}/practice/next                             │ │
│ └────────────────────────────────────────────────────────────────┘ │

6.3 After Submission — Incorrect Answer
text

│ ┌────────────────────────────────────────────────────────────────┐ │
│ │                                                                │ │
│ │  ❌ Incorrect                                   ┌────────────┐ │ │
│ │                                                 │ 🤖 Ask AI  │ │ │
│ │  Your answer: A) 19                             │   Tutor    │ │ │
│ │  Correct answer: {result.correct_answer}        └────────────┘ │ │
│ │                                                                │ │
│ │  ┌──────────────────────────────────────────────────────────┐  │ │
│ │  │ 💡 Explanation                                           │  │ │
│ │  │                                                          │  │ │
│ │  │ (result.explanation)                                     │  │ │
│ │  │                                                          │  │ │
│ │  │ bg: red-50  border-left: 4px red-500                     │  │ │
│ │  └──────────────────────────────────────────────────────────┘  │ │
│ │                                                                │ │
│ │               ┌─────────────────────┐                          │ │
│ │               │   Next Question →   │                          │ │
│ │               └─────────────────────┘                          │ │
│ └────────────────────────────────────────────────────────────────┘ │

6.4 AI Practice Side Panel (Slide-in)
API: POST /lessons/{id}/ai-practice

JSON

Request:  { question_id, prompt }
Response: { response: "..." }
text

│ ┌──────────────────────────────┐┌──────────────────────────────┐ │
│ │                              ││  🤖 AI Practice Help     ✕  │ │
│ │   Question content           ││──────────────────────────────│ │
│ │   (compressed to ~60%)       ││                              │ │
│ │                              ││  I can help you understand   │ │
│ │                              ││  this question! What would   │ │
│ │                              ││  you like me to explain?     │ │
│ │                              ││                              │ │
│ │                              ││  Quick prompts (client-side):│ │
│ │                              ││  ┌───────────────────────┐   │ │
│ │                              ││  │ Explain the concept   │   │ │
│ │                              ││  └───────────────────────┘   │ │
│ │                              ││  ┌───────────────────────┐   │ │
│ │                              ││  │ Show me a similar     │   │ │
│ │                              ││  │ example               │   │ │
│ │                              ││  └───────────────────────┘   │ │
│ │                              ││  ┌───────────────────────┐   │ │
│ │                              ││  │ Break it down step    │   │ │
│ │                              ││  │ by step               │   │ │
│ │                              ││  └───────────────────────┘   │ │
│ │                              ││                              │ │
│ │                              ││  (Response bubble appears    │ │
│ │                              ││   here after POST returns)   │ │
│ │                              ││                              │ │
│ │                              ││  ┌──────────────────┐ ┌──┐  │ │
│ │                              ││  │ Type question... │ │➤ │  │ │
│ │                              ││  └──────────────────┘ └──┘  │ │
│ │                              ││  → POST /lessons/{id}/       │ │
│ │                              ││    ai-practice               │ │
│ │  width: ~60%                 ││  width: ~40%                 │ │
│ │                              ││  bg: neutral-50              │ │
│ │                              ││  border-left: 1px            │ │
│ └──────────────────────────────┘└──────────────────────────────┘ │

Note: This endpoint returns a single JSON response (not streamed).
      Only /ai/chat is SSE. Show a spinner while awaiting response.

6.5 Question Type Variants
Dispatch based on question.question_type from the API.

text

  ┌─ MCQ (question_type = "MCQ") ─────────────────────────────┐
  │  Options come from question.options[] with is_correct flag│
  │                                                           │
  │  ┌─────────────────────────────────────────────────────┐  │
  │  │ ○  A)  x = -b ± √(b² - 4ac) / 2a                  │  │
  │  └─────────────────────────────────────────────────────┘  │
  │  ┌─────────────────────────────────────────────────────┐  │
  │  │ ○  B)  x = -b / 2a                                 │  │
  │  └─────────────────────────────────────────────────────┘  │
  │  Submit: { answer: option.option_text }                   │
  └───────────────────────────────────────────────────────────┘

  ┌─ TRUE/FALSE (question_type = "TRUE_FALSE") ───────────────┐
  │  Options are always ["True", "False"] from the API        │
  │                                                           │
  │  ┌─────────────────────┐  ┌─────────────────────┐        │
  │  │     ○  True         │  │     ○  False        │        │
  │  └─────────────────────┘  └─────────────────────┘        │
  │  Submit: { answer: "True" | "False" }                     │
  └───────────────────────────────────────────────────────────┘

  ┌─ SHORT ANSWER (question_type = "SHORT_ANSWER") ───────────┐
  │  Backend evaluates against question.accepted_answers[]    │
  │                                                           │
  │  ┌─────────────────────────────────────────────────────┐  │
  │  │ Type your answer...                                 │  │
  │  └─────────────────────────────────────────────────────┘  │
  │  Submit: { answer: userInputString }                      │
  └───────────────────────────────────────────────────────────┘

7. AI Chat
APIs:

GET /conversations — sidebar list
POST /conversations — new chat
GET /conversations/{id} — load messages
POST /conversations/{id}/messages — persist user message
DELETE /conversations/{id} — delete
POST /ai/chat — SSE stream for AI reply

7.1 Chat Layout — ChatGPT-Style
text

┌─────────┐┌──────────────────────────────────────────────────────────┐
│         ││┌────────────────┐┌────────────────────────────────────────┐
│         │││ Conversations  ││  {conversation.title}                  │
│ Main    │││ GET /conv…     ││──────────────────────────────────────── │
│ Sidebar │││ ┌────────────┐ ││                                        │
│         │││ │ + New Chat  │ ││  (messages from                       │
│         │││ └────────────┘ ││   GET /conversations/{id})             │
│         │││ POST /conv…    ││                                        │
│         │││                ││  ┌────────────────────────────────────┐│
│         │││ (Grouped by    ││  │ 👤 Can you explain the quadratic   ││
│         │││  updated_at    ││  │    formula to me?                  ││
│         │││  client-side)  ││  │    (role = USER)                   ││
│         │││ Today          ││  │    bg: primary-50, align: right    ││
│         │││ ┌────────────┐ ││  └────────────────────────────────────┘│
│         │││ │ ⬤ Quadratic│ ││                                        │
│         │││ │   Equations│ ││  ┌────────────────────────────────────┐│
│         │││ │   Help     │ ││  │ 🤖 The quadratic formula...        ││
│         │││ └────────────┘ ││  │    (role = ASSISTANT)              ││
│         │││ ┌────────────┐ ││  │    bg: white, border, align: left  ││
│         │││ │ Derivative │ ││  └────────────────────────────────────┘│
│         │││ │ s Basics   │ ││                                        │
│         │││ └────────────┘ ││  ┌────────────────────────────────────┐│
│         │││                ││  │ 👤 Can you give me an example?     ││
│         │││ Yesterday      ││  └────────────────────────────────────┘│
│         │││ ┌────────────┐ ││                                        │
│         │││ │ Probabili  │ ││  ┌────────────────────────────────────┐│
│         │││ │ ty Quest.  │ ││  │ 🤖 ▍                               ││
│         │││ └────────────┘ ││  │    (SSE streaming from /ai/chat)   ││
│         │││                ││  └────────────────────────────────────┘│
│         │││ Hover a        ││                                        │
│         │││ conversation   ││                                        │
│         │││ → reveal 🗑️     ││  ┌──────────────────────────────┐ ┌──┐│
│         │││ → DELETE       ││  │ Ask about your lessons...    │ │➤ ││
│         │││   /conv/{id}   ││  └──────────────────────────────┘ └──┘│
│         │││                ││  On submit:                            │
│         │││                ││  1) POST /conversations/{id}/messages  │
│         │││                ││     (persists user msg)                │
│         │││                ││  2) POST /ai/chat (SSE, streams        │
│         │││                ││     assistant reply live)              │
│         │││                ││                                        │
│         │││                ││  ⚠️ AI responses are educational       │
│         │││                ││     and may not be perfect.            │
│         │││ w: 260px       ││                                        │
│         │││ bg: neutral-50 ││                                        │
│         │││ border-right   ││                                        │
│         ││└────────────────┘└────────────────────────────────────────┘
│         │└──────────────────────────────────────────────────────────┘
└─────────┘
Design changes:

7.2 Message Bubble Details
text

  User Message (message.role = "USER"):
  ┌──────────────────────────────────────────────────────────────┐
  │                  ┌──────────────────────────────────┐  ┌──┐  │
  │                  │ Can you explain derivatives?     │  │👤│  │
  │                  │                                  │  └──┘  │
  │                  │ bg: primary-50                   │        │
  │                  │ text: neutral-800                │        │
  │                  │ rounded: lg (top-right: sm)      │        │
  │                  │ max-width: 75%                   │        │
  │                  └──────────────────────────────────┘        │
  │                                            12:34 PM         │
  │                             (from message.created_at)       │
  └──────────────────────────────────────────────────────────────┘

  Assistant Message (message.role = "ASSISTANT"):
  ┌──────────────────────────────────────────────────────────────┐
  │  ┌──┐  ┌──────────────────────────────────┐                  │
  │  │🤖│  │ A derivative measures the rate    │                  │
  │  └──┘  │ of change of a function...        │                  │
  │        │ bg: white, border: 1px neutral-200│                  │
  │        │ rounded: lg (top-left: sm)        │                  │
  │        └──────────────────────────────────┘                  │
  │   12:35 PM                                                   │
  └──────────────────────────────────────────────────────────────┘

  Streaming State (accumulating buffer from SSE):
  ┌──────────────────────────────────┐
  │ 🤖 The quadratic formula ▍      │   ← Blinking cursor
  └──────────────────────────────────┘

  Typing Indicator (SSE opened, no data yet):
  ┌──────────────────────────┐
  │ 🤖  ● ● ●               │   ← Bouncing dots
  └──────────────────────────┘

  On stream close: invalidate GET /conversations/{id}
                   to persist final message from server

7.3 Chat Input Area
text

  ┌──────────────────────────────────────────────────────────────┐
  │  ┌──────────────────────────────────────────────────┐ ┌────┐ │
  │  │  Ask about your lessons...                       │ │ ➤  │ │
  │  │  Auto-resize textarea, max-height: 120px         │ │    │ │
  │  │  Enter to send, Shift+Enter for newline          │ │ bg:│ │
  │  └──────────────────────────────────────────────────┘ └────┘ │
  │                                                              │
  │  ⚠️ AI responses are educational and may not be perfect.     │
  │  (Static disclaimer — no rate limit counter.)                │
  └──────────────────────────────────────────────────────────────┘

Send flow:
  IF no conversation open:
    1) POST /conversations { title: firstMessage.slice(0,40) }
    2) Navigate to /chat/{new_id}
    3) Continue with step 4
  ELSE:
    4) POST /conversations/{id}/messages { content }
    5) Open SSE via POST /ai/chat { conversation_id, message }
    6) Buffer chunks into streaming bubble
    7) On [DONE]: invalidate query keys for the conversation

7.4 Mobile Chat Layout
text

┌──────────────────────────┐
│  ← Chats  Quadratic  ⋮  │  ← Back returns to /chat list
├──────────────────────────┤   ⋮ opens delete confirmation
│                          │
│ ┌────────────────────┐   │
│ │ 👤 Explain the     │   │
│ │    quadratic       │   │
│ │    formula         │   │
│ └────────────────────┘   │
│                          │
│   ┌────────────────────┐ │
│   │ 🤖 The quadratic  │ │
│   │    formula is...   │ │
│   └────────────────────┘ │
├──────────────────────────┤
│ ┌──────────────────┐ ┌─┐│
│ │ Type message...  │ │➤││
│ └──────────────────┘ └─┘│
├──────────────────────────┤
│ 📊   📚   ✏️   🤖   ≡  │
└──────────────────────────┘

8. Study Plan
APIs:

GET /study-plan — fetch current plan
POST /study-plan/refresh — regenerate plan
Important: There is no PATCH /study-plan/items/{id} endpoint. Tasks are read-only. To get a new plan, users click Refresh.

8.1 Study Plan Page
text

┌─────────┐┌──────────────────────────────────────────────────────────┐
│         ││ Study Plan                                   ┌──────────┐│
│ Sidebar ││                                              │🔄Refresh ││
│         ││──────────────────────────────────────────────└──────────┘│
│         ││                                              → POST      │
│         ││                                                /study-   │
│         ││                                                plan/     │
│         ││                                                refresh   │
│         ││                                                          │
│         ││  Your personalized study plan based on your progress.    │
│         ││  Refresh to generate a new plan.                         │
│         ││                                                          │
│         ││ ┌────────────────────────────────────────────────────────┐│
│         ││ │  (Items grouped client-side by                         ││
│         ││ │   study_plan.items[].scheduled_date)                   ││
│         ││ │                                                        ││
│         ││ │  📅 Monday, January 15                     TODAY       ││
│         ││ │  ─────────────────────────────────────────────────     ││
│         ││ │                                                        ││
│         ││ │  ┌─────────────────────────────────────────────────┐   ││
│         ││ │  │ 🔵  Review: Quadratic Formula                  │   ││
│         ││ │  │     Focus on discriminant analysis              │   ││
│         ││ │  │     (item.title + item.description)             │   ││
│         ││ │  └─────────────────────────────────────────────────┘   ││
│         ││ │                                                        ││
│         ││ │  ┌─────────────────────────────────────────────────┐   ││
│         ││ │  │ 🔵  Practice: Algebra — Weak Topic              │   ││
│         ││ │  │     Complete adaptive practice questions        │   ││
│         ││ │  │     ┌──────────────┐                            │   ││
│         ││ │  │     │ Start →      │                            │   ││
│         ││ │  │     └──────────────┘                            │   ││
│         ││ │  │  → If item.action_type = "practice":            │   ││
│         ││ │  │    navigate to /lessons/{id}/practice           │   ││
│         ││ │  │  → If item.action_type = "lesson":              │   ││
│         ││ │  │    navigate to /lessons/{id}                    │   ││
│         ││ │  └─────────────────────────────────────────────────┘   ││
│         ││ │                                                        ││
│         ││ │  ┌─────────────────────────────────────────────────┐   ││
│         ││ │  │ 🔵  Lesson: Introduction to Derivatives         │   ││
│         ││ │  │     Read all sections                           │   ││
│         ││ │  │     ┌──────────────┐                            │   ││
│         ││ │  │     │ Start →      │                            │   ││
│         ││ │  │     └──────────────┘                            │   ││
│         ││ │  └─────────────────────────────────────────────────┘   ││
│         ││ └────────────────────────────────────────────────────────┘│
│         ││                                                          │
│         ││ ┌────────────────────────────────────────────────────────┐│
│         ││ │  📅 Tuesday, January 16                               ││
│         ││ │  ─────────────────────────────────────────────────     ││
│         ││ │                                                        ││
│         ││ │  ┌─────────────────────────────────────────────────┐   ││
│         ││ │  │ 🔵  Practice: Trigonometry — Weak Topic         │   ││
│         ││ │  │     Focus on sin/cos/tan identities             │   ││
│         ││ │  └─────────────────────────────────────────────────┘   ││
│         ││ └────────────────────────────────────────────────────────┘│
│         │└──────────────────────────────────────────────────────────┘
└─────────┘
Design changes:

8.2 Study Plan Task Card
text

  Task Card (read-only, no completion state):
  ┌─────────────────────────────────────────────────────────────┐
  │                                                             │
  │  🔵  Practice: Algebra — Weak Topic                        │
  │      Complete adaptive practice questions                   │
  │                                                             │
  │      ┌──────────────┐                                       │
  │      │  Start →     │  → routes based on item.action_type   │
  │      └──────────────┘                                       │
  │                                                             │
  │  bg: white                                                  │
  │  border: 1px neutral-200                                    │
  │  rounded: lg                                                │
  │  hover: shadow-md transition                                │
  └─────────────────────────────────────────────────────────────┘

8.3 Refresh Interaction
text

On clicking 🔄 Refresh:
  1) Show confirmation dialog:
     "Generate a new study plan? Your current plan will be replaced."
     [ Cancel ]  [ Refresh Plan ]
  
  2) On confirm:
     → POST /study-plan/refresh
     → Show overlay spinner over plan area
     → On success: setQueryData(['study-plan'], newPlan) + toast success
     → On error: toast error, keep old plan visible

9. Profile & Accessibility
APIs:

GET /users/me · PUT /users/me — profile
GET /users/me/preferences · PUT /users/me/preferences — a11y prefs

9.1 Profile Page
text

┌─────────┐┌──────────────────────────────────────────────────────────┐
│         ││ Profile & Settings                                        │
│ Sidebar ││──────────────────────────────────────────────────────────│
│         ││                                                          │
│         ││ ┌────────────────────────────────────────────────────────┐│
│         ││ │  Personal Information                                  ││
│         ││ │  (from GET /users/me)                                  ││
│         ││ │                                                        ││
│         ││ │  ┌──────────────────────┐  ┌──────────────────────┐   ││
│         ││ │  │ 👤 Full Name         │  │ 📧 Email             │   ││
│         ││ │  │ Ali Hassan           │  │ ali@example.com      │   ││
│         ││ │  │ (editable)           │  │ (editable)           │   ││
│         ││ │  └──────────────────────┘  └──────────────────────┘   ││
│         ││ │                                                        ││
│         ││ │                         ┌──────────────────┐          ││
│         ││ │                         │   Save Changes   │          ││
│         ││ │                         └──────────────────┘          ││
│         ││ │  → PUT /users/me { name, email }                       ││
│         ││ └────────────────────────────────────────────────────────┘│
│         ││                                                          │
│         ││ ┌────────────────────────────────────────────────────────┐│
│         ││ │  ♿ Accessibility Preferences                          ││
│         ││ │  (from GET /users/me/preferences)                      ││
│         ││ │                                                        ││
│         ││ │  These settings are saved to your account and          ││
│         ││ │  applied across all devices.                           ││
│         ││ │                                                        ││
│         ││ │  Font Size (preferences.font_size)                     ││
│         ││ │  ┌──────────────────────────────────────────────┐     ││
│         ││ │  │  ( Default )  ( Large )  ( Extra Large )     │     ││
│         ││ │  └──────────────────────────────────────────────┘     ││
│         ││ │                                                        ││
│         ││ │  ┌──────────────────────────┐                         ││
│         ││ │  │ Readable Mode        [⬤]│  ← preferences.         ││
│         ││ │  │ Narrower text, more   on │    readable_mode        ││
│         ││ │  │ line spacing             │                         ││
│         ││ │  └──────────────────────────┘                         ││
│         ││ │                                                        ││
│         ││ │  ┌──────────────────────────┐                         ││
│         ││ │  │ High Contrast        [○]│  ← preferences.         ││
│         ││ │  │ Enhanced color       off │    high_contrast        ││
│         ││ │  │ contrast                 │                         ││
│         ││ │  └──────────────────────────┘                         ││
│         ││ │                                                        ││
│         ││ │  ┌──────────────────────────┐                         ││
│         ││ │  │ Dyslexia Mode        [○]│  ← preferences.         ││
│         ││ │  │ OpenDyslexic font,   off │    dyslexia_mode        ││
│         ││ │  │ adjusted spacing         │                         ││
│         ││ │  └──────────────────────────┘                         ││
│         ││ │                                                        ││
│         ││ │                         ┌──────────────────┐          ││
│         ││ │                         │ Save Preferences │          ││
│         ││ │                         └──────────────────┘          ││
│         ││ │  → PUT /users/me/preferences                           ││
│         ││ │    { font_size, readable_mode,                         ││
│         ││ │      high_contrast, dyslexia_mode }                    ││
│         ││ └────────────────────────────────────────────────────────┘│
│         │└──────────────────────────────────────────────────────────┘
└─────────┘
Design changes:

9.2 Quick-Access Accessibility Panel
text

Triggered from sidebar ♿ button

┌──────────────────────────────────────┐
│  ♿ Accessibility                ✕   │
│──────────────────────────────────────│
│                                      │
│  Font Size                           │
│  ┌────────┐┌────────┐┌────────────┐ │
│  │ Default ││ Large  ││ Extra Large│ │
│  │   Aa    ││  Aa    ││    Aa      │ │
│  └────────┘└────────┘└────────────┘ │
│                                      │
│  Readable Mode              [⬤ on]  │
│  High Contrast              [○ off] │
│  Dyslexia Mode              [○ off] │
│                                      │
│  ┌──────────────────────────────┐   │
│  │       Save Preferences       │   │
│  └──────────────────────────────┘   │
│  → PUT /users/me/preferences         │
│                                      │
│  Changes apply immediately on save.  │
│  Saved to your account.              │
│                                      │
│  position: fixed, right: 0, top: 0   │
│  width: 360px, height: 100vh         │
│  bg: white, shadow-2xl, z-50         │
│  slide-in animation                  │
└──────────────────────────────────────┘

10. Admin Pages
Admin access is gated by user.is_admin from GET /auth/me.

10.1 Admin Sidebar
text

┌──────────────────┐
│   ┌──────────┐   │
│   │ ◆ Admin  │   │
│   │  Panel   │   │
│   └──────────┘   │
│                  │
│ ─────────────── │
│  📊 Dashboard    │  → /admin/dashboard (client-aggregated)
│  📚 Lessons      │  → /admin/lessons (GET /lessons)
│  📂 Topics       │  → /admin/topics (GET /topics + admin CRUD)
│  ❓ Questions    │  → /admin/lessons (edit questions via lesson)
│  👥 Students     │  → /admin/students (GET /admin/students)
│                  │
│ ─────────────── │
│  ← Back to App   │  → /dashboard (student view)
│  🚪 Logout       │  → POST /auth/logout

└──────────────────┘

10.2 Admin Dashboard

text

┌─────────┐┌──────────────────────────────────────────────────────────┐
│  Admin  ││ Admin Dashboard                                          │
│ Sidebar ││──────────────────────────────────────────────────────────│
│         ││                                                          │
│         ││ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐         │
│         ││ │ 👥 Total    │ │ 📚 Total    │ │ 📂 Total    │         │
│         ││ │  Students   │ │  Lessons    │ │  Topics     │         │
│         ││ │             │ │             │ │             │         │
│         ││ │    156      │ │    20       │ │    12       │         │
│         ││ │ (GET /admin/│ │ (GET        │ │ (GET        │         │
│         ││ │  students   │ │  /lessons   │ │  /topics    │         │
│         ││ │  .length)   │ │  .length)   │ │  .length)   │         │
│         ││ └─────────────┘ └─────────────┘ └─────────────┘         │
│         ││                                                          │
│         ││ ┌────────────────────────────────────────────────────────┐│
│         ││ │  Quick Actions                                         ││
│         ││ │                                                        ││
│         ││ │  ┌─────────────────┐  ┌─────────────────┐              ││
│         ││ │  │ + New Lesson    │  │ + New Topic     │              ││
│         ││ │  └─────────────────┘  └─────────────────┘              ││
│         ││ │  → /admin/lessons/new   → /admin/topics                ││
│         ││ └────────────────────────────────────────────────────────┘│
│         ││                                                          │
│         │└──────────────────────────────────────────────────────────┘
└─────────┘

10.3 Admin Lesson Management

API: GET /lessons for listing, DELETE /admin/lessons/{id} for row actions.

text

┌─────────┐┌──────────────────────────────────────────────────────────┐
│  Admin  ││ Lessons Management                      ┌──────────────┐│
│ Sidebar ││                                         │ + New Lesson ││
│         ││─────────────────────────────────────────└──────────────┘│
│         ││                                         → /admin/lessons│
│         ││                                            /new         │
│         ││                                                          │
│         ││ ┌──────────────────────────────────────────────────────┐ │
│         ││ │ 🔍 Search... (debounced ?search=)  Topic ▼          │ │
│         ││ │                              (from GET /topics)      │ │
│         ││ └──────────────────────────────────────────────────────┘ │
│         ││                                                          │
│         ││ ┌──────────────────────────────────────────────────────┐ │
│         ││ │ Title            │ Topic    │ Status    │       ⚙️  │ │
│         ││ ├──────────────────┼──────────┼───────────┼────────────┤ │
│         ││ │ Intro to Algebra │ Algebra  │🟢 Published│    ⋮      │ │
│         ││ │ Quadratic Eqns   │ Algebra  │🟢 Published│    ⋮      │ │
│         ││ │ Derivatives      │ Calculus │🔴 Draft   │    ⋮      │ │
│         ││ │ Probability      │ Stats    │🟢 Published│    ⋮      │ │
│         ││ │  (lesson.        │          │(lesson.   │           │ │
│         ││ │   title)         │          │ is_       │           │ │
│         ││ │                  │          │ published)│           │ │
│         ││ └──────────────────────────────────────────────────────┘ │
│         ││                                                          │
│         │└──────────────────────────────────────────────────────────┘
└─────────┘

Row action menu (⋮):
┌──────────────┐
│ ✏️ Edit       │  → /admin/lessons/{id}
│ ❓ Questions  │  → /admin/lessons/{id}/questions
│ ─────────── │
│ 🗑️ Delete    │  → DELETE /admin/lessons/{id} (with confirm dialog)
└──────────────┘

APIs:

POST /admin/lessons (create)
PUT /admin/lessons/{id} (update — includes sections in payload)
GET /topics + GET /topics/{id}/subtopics (for subtopic dropdown)
text

┌─────────┐┌──────────────────────────────────────────────────────────┐
│  Admin  ││ Edit Lesson: Introduction to Algebra                      │
│ Sidebar ││──────────────────────────────────────────────────────────│
│         ││                                                          │
│         ││ ┌──── Lesson Details ────────────────────────────────────┐│
│         ││ │                                                        ││
│         ││ │  ┌──────────────────────┐  ┌──────────────────────┐   ││
│         ││ │  │ Title                │  │ Subtopic         ▼  │   ││
│         ││ │  │ Introduction to...   │  │ Linear Equations     │   ││
│         ││ │  └──────────────────────┘  └──────────────────────┘   ││
│         ││ │                            (options from GET /topics/  ││
│         ││ │                             {parent}/subtopics or      ││
│         ││ │                             flat GET /topics)          ││
│         ││ │                                                        ││
│         ││ │  ┌──────────────────────────────────────────────────┐  ││
│         ││ │  │ Description                                      │  ││
│         ││ │  │ Learn the fundamentals of algebraic...           │  ││
│         ││ │  └──────────────────────────────────────────────────┘  ││
│         ││ │                                                        ││
│         ││ │  ┌──────────────┐  ┌────────────────────┐             ││
│         ││ │  │ ⏱ Est. Min   │  │ ☐ Published        │             ││
│         ││ │  │ 15           │  └────────────────────┘             ││
│         ││ │  └──────────────┘   (lesson.is_published)             ││
│         ││ └────────────────────────────────────────────────────────┘│
│         ││                                                          │
│         ││ ┌──── Sections ─────────────────────── + Add Section ───┐│
│         ││ │  (Managed as nested array in the PUT payload)          ││
│         ││ │                                                        ││
│         ││ │  ┌─ ≡ ──────────────────────────────────── ✏️ 🗑️ ──┐  ││
│         ││ │  │  1. Introduction                                 │  ││
│         ││ │  │  ┌────────────────────────────────────────────┐   │  ││
│         ││ │  │  │ Type: Introduction ▼                       │   │  ││
│         ││ │  │  │  (Introduction / Explanation /             │   │  ││
│         ││ │  │  │   Example / Summary)                       │   │  ││
│         ││ │  │  └────────────────────────────────────────────┘   │  ││
│         ││ │  │  ┌────────────────────────────────────────────┐   │  ││
│         ││ │  │  │ Content (textarea)                         │   │  ││
│         ││ │  │  │ Algebra is a branch of mathematics...      │   │  ││
│         ││ │  │  └────────────────────────────────────────────┘   │  ││
│         ││ │  └──────────────────────────────────────────────────┘  ││
│         ││ │                                                        ││
│         ││ │  ┌─ ≡ ──────────────────────────────────── ✏️ 🗑️ ──┐  ││
│         ││ │  │  2. Explanation (collapsed — click to expand)    │  ││
│         ││ │  └──────────────────────────────────────────────────┘  ││
│         ││ │                                                        ││
│         ││ │  ≡ = drag handle (sets section.position on save)      ││
│         ││ └────────────────────────────────────────────────────────┘│
│         ││                                                          │
│         ││        ┌──────────────┐  ┌──────────────┐                │
│         ││        │   Cancel     │  │  Save Lesson │                │
│         ││        └──────────────┘  └──────────────┘                │
│         ││                          → PUT /admin/lessons/{id}       │
│         ││                            (or POST /admin/lessons       │
│         ││                             if new)                      │
│         │└──────────────────────────────────────────────────────────┘
└─────────┘
10.5 Question Editor (Dynamic Form)
APIs:

POST /admin/lessons/{id}/questions
PUT /admin/lessons/{id}/questions/{qid}
DELETE /admin/lessons/{id}/questions/{qid}
text

┌──────────────────────────────────────────────────────────────────┐
│  Add Question to: Introduction to Algebra                        │
│──────────────────────────────────────────────────────────────────│
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Question Text                                               │ │
│  │ What is the value of x in 2x + 6 = 12?                     │ │
│  │ → question.question_text                                    │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────┐                                          │
│  │ Type:   MCQ    ▼   │  Questions are always adaptive practice │
│  │ MCQ | TRUE_FALSE   │                                          │
│  │ | SHORT_ANSWER     │                                          │
│  └────────────────────┘                                          │
│                                                                  │
│  ┌────────────────────┐                                          │
│  │ Topic:  Algebra ▼  │  → question.topic_id                     │
│  │ (from GET /topics) │                                          │
│  └────────────────────┘                                          │
│                                                                  │
│  ─── Dynamic Section (changes based on Type) ───                │
│                                                                  │
│  ┌─ MCQ Options (question_type = "MCQ") ─────────────────────┐  │
│  │  Sent as question.options[] with is_correct boolean       │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────┐ ☑ Correct    │  │
│  │  │ A)  3                                   │              │  │
│  │  └─────────────────────────────────────────┘              │  │
│  │  ┌─────────────────────────────────────────┐ ☐            │  │
│  │  │ B)  6                                   │              │  │
│  │  └─────────────────────────────────────────┘              │  │
│  │  ┌─────────────────────────────────────────┐ ☐            │  │
│  │  │ C)  9                                   │              │  │
│  │  └─────────────────────────────────────────┘              │  │
│  │  ┌─────────────────────────────────────────┐ ☐            │  │
│  │  │ D)  12                                  │              │  │
│  │  └─────────────────────────────────────────┘              │  │
│  │                                                            │  │
│  │  + Add Option                                             │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ Explanation                                                 │ │
│  │ Subtract 6 from both sides: 2x = 6. Divide by 2: x = 3.    │ │
│  │ → question.explanation                                      │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                                                                  │
│           ┌──────────────┐  ┌──────────────┐                     │
│           │    Cancel    │  │ Save Question│                     │
│           └──────────────┘  └──────────────┘                     │
│                            → POST or PUT to                      │
│                              /admin/lessons/{id}/questions[/qid] │
└──────────────────────────────────────────────────────────────────┘


  ─── When Type = TRUE_FALSE ───

  ┌─ True/False ───────────────────────────────────────────────┐
  │  Backend stores as two options with is_correct flags       │
  │                                                            │
  │  Correct answer:                                           │
  │  ┌────────────┐  ┌────────────┐                           │
  │  │ ◉  True    │  │ ○  False   │                           │
  │  └────────────┘  └────────────┘                           │
  └────────────────────────────────────────────────────────────┘


  ─── When Type = SHORT_ANSWER ───

  ┌─ Accepted Answers ─────────────────────────────────────────┐
  │  Sent as question.accepted_answers[] (PostgreSQL TEXT[])   │
  │                                                            │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                │
  │  │ 3     ✕  │  │ three ✕  │  │ + Add    │                │
  │  └──────────┘  └──────────┘  └──────────┘                │
  └────────────────────────────────────────────────────────────┘

10.6 Admin Student Progress View
APIs:

GET /admin/students (list)
GET /admin/students/{id}/progress (detail)
text

┌─────────┐┌──────────────────────────────────────────────────────────┐
│  Admin  ││ Students                                                 │
│ Sidebar ││──────────────────────────────────────────────────────────│
│         ││                                                          │
│         ││ ┌──────────────────────────────────────────────────────┐ │
│         ││ │ 🔍 Search by name or email...                        │ │
│         ││ └──────────────────────────────────────────────────────┘ │
│         ││                                                          │
│         ││ ┌──────────────────────────────────────────────────────┐ │
│         ││ │ Name          │ Email                │ Actions       │ │
│         ││ ├───────────────┼──────────────────────┼───────────────┤ │
│         ││ │ Ali Hassan    │ ali@example.com      │ View Progress │ │
│         ││ │ Sara Ahmed    │ sara@example.com     │ View Progress │ │
│         ││ │ ...           │ ...                  │ ...           │ │
│         ││ └──────────────────────────────────────────────────────┘ │
│         ││   (from GET /admin/students; search filters client-side) │
│         │└──────────────────────────────────────────────────────────┘
└─────────┘

Clicking "View Progress" → /admin/students/{id}
Student Progress Detail (uses GET /admin/students/{id}/progress — same shape as /progress):

text

┌─────────┐┌──────────────────────────────────────────────────────────┐
│  Admin  ││ ← Back to Students                                       │
│ Sidebar ││ Student Progress: Ali Hassan                             │
│         ││──────────────────────────────────────────────────────────│
│         ││                                                          │
│         ││         ┌─────────────┐              ┌─────────────┐    │
│         ││         │ Overall     │              │ Weak Topics │    │
│         ││         │ Score: 78%  │              │      2      │    │
│         ││         └─────────────┘              └─────────────┘    │
│         ││    (overall_score)              (weak_topics.length)     │
│         ││                                                          │
│         ││ ┌────────────────────────────────────────────────────────┐│
│         ││ │  Topic Mastery                                         ││
│         ││ │  (from mastery[])                                      ││
│         ││ │                                                        ││
│         ││ │  Algebra         ████████████████░░░░  85% Proficient ││
│         ││ │  Geometry        ██████████████░░░░░░  65% Interm.    ││
│         ││ │  Calculus        ███████░░░░░░░░░░░░░  35% Developing ││
│         ││ │  Statistics      ████████████████████  92% Mastered   ││
│         ││ └────────────────────────────────────────────────────────┘│
│         ││                                                          │
│         ││ ┌────────────────────────────────────────────────────────┐│
│         ││ │  Weak Topics                                           ││
│         ││ │  (from weak_topics[])                                  ││
│         ││ │                                                        ││
│         ││ │  ⚠️ Quadratic Equations  Acc: 42%  Attempts: 8        ││
│         ││ │  ⚠️ Trigonometry         Acc: 38%  Attempts: 5        ││
│         ││ └────────────────────────────────────────────────────────┘│
│         ││                                                          │
│         ││ ┌────────────────────────────────────────────────────────┐│
│         ││ │  Topic Accuracy                                        ││
│         ││ │  (from topic_accuracy[] — Recharts bar chart)          ││
│         ││ │  ┌──────────────────────────────────────────────┐     ││
│         ││ │  │  █   █       █   █                           │     ││
│         ││ │  │  █   █   █   █   █   █                       │     ││
│         ││ │  │  Alg Geo Cal Sta Tri Pro                     │     ││
│         ││ │  └──────────────────────────────────────────────┘     ││
│         ││ └────────────────────────────────────────────────────────┘│
│         │└──────────────────────────────────────────────────────────┘
└─────────┘

10.7 Admin Topics Manager
APIs:

GET /topics (list — student endpoint reused; admin has read access)
POST /admin/topics (create)
PUT /admin/topics/{id} (update)
DELETE /admin/topics/{id} (delete)
text

┌─────────┐┌──────────────────────────────────────────────────────────┐
│  Admin  ││ Topics                                    ┌────────────┐│
│ Sidebar ││                                           │ + New Topic ││
│         ││───────────────────────────────────────────└────────────┘│
│         ││                                                          │
│         ││ ┌────────────────────────────────────────────────────────┐│
│         ││ │  📂 Mathematics                                        ││
│         ││ │     ├─ 📂 Algebra                            ✏️  🗑️  ││
│         ││ │     │  ├─ Linear Equations                   ✏️  🗑️  ││
│         ││ │     │  └─ Quadratic Equations                ✏️  🗑️  ││
│         ││ │     ├─ 📂 Geometry                           ✏️  🗑️  ││
│         ││ │     └─ 📂 Calculus                           ✏️  🗑️  ││
│         ││ │                                                        ││
│         ││ │  📂 Statistics                                          ││
│         ││ │     └─ Probability                           ✏️  🗑️  ││
│         ││ │                                                        ││
│         ││ │  (Tree built client-side from GET /topics              ││
│         ││ │   using parent_topic_id → children mapping)            ││
│         ││ └────────────────────────────────────────────────────────┘│
│         │└──────────────────────────────────────────────────────────┘
└─────────┘

Create/Edit modal:
┌──────────────────────────────────────────────┐
│  New Topic / Edit Topic              ✕      │
│──────────────────────────────────────────────│
│                                              │
│  Name                                        │
│  ┌────────────────────────────────────────┐ │
│  │ Algebra                                │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  Parent Topic (optional)                     │
│  ┌────────────────────────────────────────┐ │
│  │ Mathematics                        ▼   │ │
│  └────────────────────────────────────────┘ │
│                                              │
│  Description                                 │
│  ┌────────────────────────────────────────┐ │
│  │ Branch of mathematics dealing with...  │ │
│  └────────────────────────────────────────┘ │
│                                              │
│         ┌──────────┐  ┌──────────┐          │
│         │  Cancel  │  │   Save   │          │
│         └──────────┘  └──────────┘          │
│                       → POST or PUT          │
│                         /admin/topics[/id]   │
└──────────────────────────────────────────────┘

11. Component Library

11.1 Button Variants
text

  Primary:           Secondary:          Ghost:              Danger:
  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐   ┌──────────────┐
  │  Save        │   │  Cancel      │   │  View More   │   │  Delete      │
  │ bg: pri-600  │   │ bg: white    │   │ bg: transp.  │   │ bg: red-600  │
  │ text: white  │   │ border: gray │   │ text: pri-600│   │ text: white  │
  │ hover: -700  │   │ text: gray   │   │ hover: pri-50│   │ hover: -700  │
  │ rounded: md  │   │ hover: -50   │   │                │   │ rounded: md  │
  └──────────────┘   └──────────────┘   └──────────────┘   └──────────────┘

  Sizes:      sm (32px) · md (40px) · lg (48px)

  Loading State:
  ┌──────────────────┐
  │  ⟳  Saving...    │   ← spinner + disabled during mutation
  └──────────────────┘   (bound to useMutation.isPending)

11.2 Card Component
text

  Default Card:                    Interactive Card:
  ┌────────────────────────┐      ┌────────────────────────┐
  │  Card Title            │      │  Card Title         →  │
  │  Card content          │      │  Card content          │
  │  bg: white             │      │  hover: shadow-md      │
  │  border: 1px gray-200  │      │  hover: border-pri-200 │
  │  rounded: lg           │      │  cursor: pointer       │
  │  shadow: sm            │      │  transition: 200ms     │
  │  padding: 24px         │      │                        │
  └────────────────────────┘      └────────────────────────┘

11.3 Form Controls
text

  Text Input:
  ┌──────────────────────────────────────┐
  │ Label                                │
  │ ┌──────────────────────────────────┐ │
  │ │ Placeholder text...              │ │
  │ │ h: 44px, border: neutral-300     │ │
  │ │ focus: ring-2 primary-500        │ │
  │ └──────────────────────────────────┘ │
  │ Helper text or Zod/API error message │
  └──────────────────────────────────────┘

  Select:  (used for topic filters, subtopic pickers)
  ┌──────────────────────────────────────┐
  │ ┌──────────────────────────────────┐ │
  │ │ Selected option              ▼   │ │
  │ └──────────────────────────────────┘ │
  └──────────────────────────────────────┘

  Toggle Switch:  (used for a11y prefs, is_published)
  ┌──────────────────────────────────────┐
  │ Setting Name             ┌────────┐ │
  │ Description              │ ●────  │ │  ON
  │                          └────────┘ │
  └──────────────────────────────────────┘

  Radio Group (Segmented):  (used for font_size)
  ┌───────────────────────────────────────────────────┐
  │ ┌──────────┐┌──────────┐┌──────────────┐         │
  │ │ ◉Default ││  Large   ││ Extra Large  │         │
  │ └──────────┘└──────────┘└──────────────┘         │
  └───────────────────────────────────────────────────┘

11.4 Data Display
text

  Badge/Chip:  (for is_published status, weak-topic tags)
  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
  │ 🟢 Published│  │ 🔴 Draft    │  │ ⚠️ Weak     │
  └─────────────┘  └─────────────┘  └─────────────┘

  Progress Bar:  (for mastery)
  ┌──────────────────────────────────────────────────┐
  │██████████████████████████░░░░░░░░░░░░░░░░  65%  │
  │  h: 8px (small) / 12px (default)                │
  │  fill: mastery_label → color mapping             │
  │  rounded: full                                   │
  └──────────────────────────────────────────────────┘

  Empty State:
  ┌──────────────────────────────────────────────────┐
  │              ┌──────────┐                        │
  │              │    📭    │                        │
  │              └──────────┘                        │
  │         No lessons found                         │
  │    Try adjusting your search filters             │
  │         ┌──────────────────┐                     │
  │         │  Clear Filters   │                     │
  │         └──────────────────┘                     │
  └──────────────────────────────────────────────────┘

  Used when: API returns [], typically on filtered queries.

11.5 Navigation Components
text

  Breadcrumb:  (admin edit paths)
  ┌──────────────────────────────────────────────────┐
  │  Lessons  /  Introduction to Algebra  /  Edit    │
  │  link       link                        current  │
  └──────────────────────────────────────────────────┘

  Tabs:  (student progress detail view could split)
  ┌──────────────────────────────────────────────────┐
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
  │  │ Overview │  │ Mastery  │  │  Weak    │      │
  │  │ ━━━━━━━━ │  │          │  │  Topics  │      │
  │  └──────────┘  └──────────┘  └──────────┘      │
  │  border-bottom: 2px gray-200 (container)        │
  │  active: border-bottom: 2px primary-600          │
  └──────────────────────────────────────────────────┘

Note: Pagination component removed from library —
      no listing endpoint currently supports pagination.
      Add back when backend introduces ?page= support.

12. Responsive Behavior

12.1 Breakpoint System
text

┌────────────────────────────────────────────────────────────────┐
│                      BREAKPOINTS                               │
├────────────────────────────────────────────────────────────────┤
│  Mobile:   < 640px    │  Single column, bottom nav             │
│  Tablet:   640-1023px │  2-col grid, bottom nav                │
│  Desktop:  ≥ 1024px   │  Sidebar + content, full features      │
└────────────────────────────────────────────────────────────────┘

12.2 Dashboard — Mobile
text

┌──────────────────────────┐
│  ☰  Dashboard     🔔  👤 │
├──────────────────────────┤
│  Welcome, Ali! 👋        │
│                          │
│  ┌──────────────────────┐│
│  │ 🎯 Overall Score 78% ││  ← Stat cards from
│  └──────────────────────┘│    /progress payload
│  ┌──────────────────────┐│
│  │ 📚 Topics Tracked 12 ││
│  └──────────────────────┘│
│  ┌──────────────────────┐│
│  │ ⚠️ Weak Topics    2  ││
│  └──────────────────────┘│
│                          │
│  Topic Mastery           │
│  ┌──────────────────────┐│
│  │ Algebra    ████░ 85% ││
│  │ Geometry   ███░░ 65% ││
│  │ Calculus   ██░░░ 35% ││
│  └──────────────────────┘│
│                          │
│  Weak Topics             │
│  ┌──────────────────────┐│
│  │ ⚠️ Quadratic Eqns   ││
│  │ Acc: 42%             ││
│  │ ┌──────────────────┐ ││
│  │ │ Practice Now     │ ││
│  │ └──────────────────┘ ││
│  └──────────────────────┘│
├──────────────────────────┤
│ 📊   📚   ✏️   🤖   ≡  │
└──────────────────────────┘

12.3 Grid Behavior
text

  Desktop (≥1024px):
  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
  │ Card 1 │ │ Card 2 │ │ Card 3 │ │ Card 4 │   4 columns
  └────────┘ └────────┘ └────────┘ └────────┘

  Tablet (640-1023px):
  ┌────────────┐ ┌────────────┐                 2 columns
  │   Card 1   │ │   Card 2   │
  └────────────┘ └────────────┘

  Mobile (<640px):
  ┌──────────────────────────┐                  1 column
  │         Card 1           │
  └──────────────────────────┘

12.4 Mobile "More" Menu
text

Bottom nav shows 4 primary items + "More":
│ 📊   📚   ✏️   🤖   ≡  │
│Dash  Learn Prac Chat More│

Tapping "More" shows a slide-up sheet:
┌──────────────────────────┐
│  ─── (drag handle) ───   │
│                          │
│  📅  Study Plan          │
│  👤  Profile             │
│  ♿  Accessibility       │
│  🚪  Logout              │
│                          │
└──────────────────────────┘

13. Accessibility Modes
All modes are driven by GET/PUT /users/me/preferences and applied globally via CSS custom properties on <html>.

13.1 High Contrast Mode
Toggled by preferences.high_contrast.

text

  Normal:                              High Contrast:
  ┌────────────────────────┐          ┌────────────────────────┐
  │  Card Title            │          │  Card Title            │
  │  text: gray-800        │          │  text: black           │
  │  Description text      │          │  Description text      │
  │  text: gray-600        │          │  text: gray-900        │
  │  bg: white             │          │  bg: white             │
  │  border: gray-200      │          │  border: black (2px)   │
  │  ┌──────────────┐      │          │  ┌──────────────┐      │
  │  │  Button      │      │          │  │  Button      │      │
  │  │  bg: pri-600 │      │          │  │  bg: pri-800 │      │
  │  └──────────────┘      │          │  │  border: 2px │      │
  │                        │          │  └──────────────┘      │
  └────────────────────────┘          └────────────────────────┘

  Focus indicators become thicker (3px) and high-visibility.
  
13.2 Dyslexia Mode
Toggled by preferences.dyslexia_mode.

text

  Normal:                              Dyslexia Mode:
  ┌────────────────────────┐          ┌────────────────────────┐
  │  Regular Text          │          │  OpenDyslexic Text     │
  │  font: Inter           │          │  font: OpenDyslexic    │
  │  letter-spacing: 0     │          │  letter-spacing: 0.05em│
  │  word-spacing: normal  │          │  word-spacing: 0.1em   │
  │  line-height: 1.6      │          │  line-height: 1.8      │
  └────────────────────────┘          └────────────────────────┘

13.3 Readable Mode
Toggled by preferences.readable_mode.

text

  Normal:                              Readable Mode:
  ┌──────────────────────────────┐    ┌──────────────────────────────┐
  │  Content spans full          │    │     ┌──────────────────┐     │
  │  available width...          │    │     │ Content is       │     │
  │                              │    │     │ constrained to   │     │
  │  max-width: 1200px           │    │     │ max-width 680px  │     │
  │                              │    │     │ line-height 1.8  │     │
  │                              │    │     └──────────────────┘     │
  └──────────────────────────────┘    └──────────────────────────────┘

13.4 Font Size Comparison
Controlled by preferences.font_size (Default / Large / Extra Large).

text

  Default (16px):          Large (20px):            Extra Large (24px):
  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
  │ Regular body     │    │ Larger body      │    │ Extra large      │
  │ text at 16px.    │    │ text at 20px.    │    │ body text at     │
  │                  │    │                  │    │ 24px for max     │
  │ All sizes scale. │    │ All sizes scale. │    │ readability.     │
  └──────────────────┘    └──────────────────┘    └──────────────────┘

14. State & Feedback Patterns
14.1 Skeleton Loaders
Shown while any useQuery is isLoading.

text

  Card Skeleton:                    List Skeleton:
  ┌────────────────────────┐      ┌────────────────────────────┐
  │  ░░░░░░░░░░░           │      │ ┌──┐ ░░░░░░░░░░░░░░░░░░░░│
  │                        │      │ └──┘ ░░░░░░░░░░           │
  │  ░░░░░░░░░░░░░░░░░░   │      │                            │
  │  ░░░░░░░░░░░░░░       │      │ ┌──┐ ░░░░░░░░░░░░░░░░░░░░│
  │  ░░░░░░░░░░░░░░░░░░░░ │      │ └──┘ ░░░░░░░░░░░          │
  │  ░░░░░░░░              │      │                            │
  │  animate: pulse        │      │  animate: pulse            │
  │  bg: neutral-200       │      │  bg: neutral-200           │
  │  rounded: md           │      │  rounded: md               │
  └────────────────────────┘      └────────────────────────────┘

  Dashboard Skeleton:  (mirrors 4-column stat cards layout)
  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
  │ ░░░░        │ │ ░░░░        │ │ ░░░░        │ │ ░░░░        │
  │ ░░░░░░░     │ │ ░░░░░░░     │ │ ░░░░░░░     │ │ ░░░░░░░     │
  │ ░░░         │ │ ░░░         │ │ ░░░         │ │ ░░░         │
  └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘

14.2 Toast Notifications
Shown on useMutation success/error and for API-level warnings.

text

  Success (from mutation success handler):
  ┌──────────────────────────────────────────────┐
  │  ✅  Profile updated successfully       ✕   │
  │  border-left: 4px green-500                  │
  └──────────────────────────────────────────────┘

  Error (from ApiError caught in mutation):
  ┌──────────────────────────────────────────────┐
  │  ❌  Failed to save. Please try again.  ✕   │
  │  border-left: 4px red-500                    │
  └──────────────────────────────────────────────┘

  Rate-limit warning (thrown as ApiError with status 429):
  ┌──────────────────────────────────────────────┐
  │  ⚠️  Too many requests. Please slow down.✕  │
  │  border-left: 4px amber-500                  │
  └──────────────────────────────────────────────┘

  position: top-right, auto-dismiss: 5s, slide-in animation

14.3 Confirmation Dialogs
Required before any DELETE mutation.

text

  ┌──────────────────────────────────────────────┐
  │  🗑️  Delete Lesson?                          │
  │                                              │
  │  Are you sure you want to delete             │
  │  "Introduction to Algebra"?                  │
  │                                              │
  │  This action cannot be undone. All           │
  │  associated sections and questions           │
  │  will also be removed.                       │
  │                                              │
  │         ┌──────────┐  ┌───────────┐          │
  │         │  Cancel  │  │  Delete   │          │
  │         │  ghost   │  │ bg:red-600│          │
  │         └──────────┘  └───────────┘          │
  │                       → DELETE /admin/       │
  │                         lessons/{id}         │
  │                                              │
  │  backdrop: black/50 blur, max-w 440px        │
  └──────────────────────────────────────────────┘

Also used for:
  - DELETE /admin/topics/{id}
  - DELETE /admin/lessons/{id}/questions/{qid}
  - DELETE /conversations/{id}
  - POST /study-plan/refresh (destructive: replaces plan)

14.4 Error States
text

  API Error (Full Page — for isError on primary query):
  ┌──────────────────────────────────────────────────┐
  │              ┌──────────┐                        │
  │              │   ⚠️     │                        │
  │              └──────────┘                        │
  │                                                  │
  │     Something went wrong                         │
  │     {error.message}                              │
  │                                                  │
  │         ┌──────────────────┐                     │
  │         │    Try Again     │  → refetch()        │
  │         └──────────────────┘                     │
  └──────────────────────────────────────────────────┘

  Inline Form Error (from Zod or ApiError):
  ┌──────────────────────────────────────┐
  │ Email                                │
  │ ┌──────────────────────────────────┐ │
  │ │ invalid@                         │ │  ← border: red-500
  │ └──────────────────────────────────┘ │
  │ ⚠ Please enter a valid email address │  ← text: red-600
  └──────────────────────────────────────┘

  Session Expired (401 from any endpoint):
  ┌──────────────────────────────────────────────────┐
  │  Your session has expired. Please sign in again. │
  │                    ┌──────────────┐              │
  │                    │  Sign In →   │              │
  │                    └──────────────┘              │
  └──────────────────────────────────────────────────┘
  Global 401 handler in lib/api.ts clears query cache
  and routes to /login.
  
14.5 Loading & Interaction States
text

  Button Loading (bound to mutation.isPending):
  ┌──────────────────┐    ┌──────────────────┐
  │   Submit         │ →  │  ⟳ Submitting... │
  │   enabled        │    │   disabled       │
  │   bg: pri-600    │    │   bg: pri-400    │
  │                  │    │   cursor: wait   │
  └──────────────────┘    └──────────────────┘

  SSE Streaming (POST /ai/chat):
  ┌──────────────────────────────┐
  │ 🤖  ● ● ●                    │  ← Before first chunk arrives
  └──────────────────────────────┘
  ┌──────────────────────────────┐
  │ 🤖  The quadratic ▍          │  ← During streaming (buffer)
  └──────────────────────────────┘
  ┌──────────────────────────────┐
  │ 🤖  The quadratic formula    │  ← On [DONE], invalidate
  │     is used to find the      │     conversation query so
  │     solutions...             │     final message persists
  └──────────────────────────────┘

  Study Plan Refresh (POST /study-plan/refresh):
  ┌──────────────────────────────────────┐
  │  ┌────────────────────────────┐     │
  │  │  🔄 Generating your new    │     │  ← Overlay on plan area
  │  │     study plan...          │     │     bg: white/80
  │  │     ⟳ (spinner)            │     │
  │  └────────────────────────────┘     │
  └──────────────────────────────────────┘
Summary: Tailwind CSS Implementation Tokens
text

┌──────────────────────────────────────────────────────────────────┐
│                  TAILWIND CONFIG SUMMARY                         │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  colors.primary:   indigo palette (50-900)                       │
│  colors.success:   emerald-500                                   │
│  colors.warning:   amber-500                                     │
│  colors.danger:    red-500                                       │
│                                                                  │
│  colors.mastery: {                                               │
│    beginner:     '#EF4444',   // 0-29                            │
│    developing:   '#F97316',   // 30-49                           │
│    intermediate: '#EAB308',   // 50-69                           │
│    proficient:   '#22C55E',   // 70-89                           │
│    mastered:     '#6366F1',   // 90-100                          │
│  }                                                               │
│                                                                  │
│  fontFamily.sans:      ['Inter', ...defaultTheme.sans]           │
│  fontFamily.dyslexic:  ['OpenDyslexic', 'sans-serif']            │
│                                                                  │
│  screens.sm:  640px  │  screens.md:  768px                       │
│  screens.lg:  1024px │  screens.xl:  1280px                      │
│                                                                  │
│  CSS Custom Properties (from PUT /users/me/preferences):         │
│    --font-size-base:      16px | 20px | 24px                     │
│    --line-height-body:    1.6 | 1.8                              │
│    --content-max-width:   1200px | 680px (readable mode)         │
│    --font-family:         var(--font-inter | --font-dyslexic)    │
│                                                                  │
│  Classes toggled on <html>:                                      │
│    .high-contrast    (preferences.high_contrast)                 │
│    .readable-mode    (preferences.readable_mode)                 │
│    .dyslexia-mode    (preferences.dyslexia_mode)                 │
│                                                                  │
│  shadcn/ui components used:                                      │
│    Button, Card, Input, Select, Dialog, Sheet, Tabs,             │
│    DropdownMenu, Badge, Progress, Toggle, Toast (Sonner),        │
│    Skeleton, Avatar, Separator, Tooltip                          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
