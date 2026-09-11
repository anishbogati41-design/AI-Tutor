CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
    font_size TEXT NOT NULL DEFAULT 'default',
    readable_mode BOOLEAN NOT NULL DEFAULT FALSE,
    high_contrast BOOLEAN NOT NULL DEFAULT FALSE,
    dyslexia_mode BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE topics (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    parent_topic_id BIGINT REFERENCES topics(id) ON DELETE RESTRICT,
    description TEXT NOT NULL DEFAULT '',
    CONSTRAINT topic_cannot_parent_itself CHECK (parent_topic_id IS NULL OR parent_topic_id <> id)
);

CREATE TABLE lessons (
    id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    subtopic_id BIGINT NOT NULL REFERENCES topics(id) ON DELETE RESTRICT,
    estimated_minutes INTEGER NOT NULL CHECK (estimated_minutes > 0),
    is_published BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE lesson_sections (
    id BIGSERIAL PRIMARY KEY,
    lesson_id BIGINT NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    section_type TEXT NOT NULL CHECK (
        section_type IN ('INTRODUCTION', 'EXPLANATION', 'EXAMPLE', 'SUMMARY')
    ),
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    position INTEGER NOT NULL CHECK (position >= 0),
    UNIQUE (lesson_id, position)
);

CREATE TABLE questions (
    id BIGSERIAL PRIMARY KEY,
    lesson_id BIGINT NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    topic_id BIGINT NOT NULL REFERENCES topics(id) ON DELETE RESTRICT,
    question_text TEXT NOT NULL,
    question_type TEXT NOT NULL CHECK (
        question_type IN ('MCQ', 'TRUE_FALSE', 'SHORT_ANSWER')
    ),
    difficulty_score NUMERIC(5, 2) NOT NULL DEFAULT 0 CHECK (
        difficulty_score >= 0 AND difficulty_score <= 100
    ),
    explanation TEXT NOT NULL DEFAULT '',
    accepted_answers TEXT[]
);

CREATE TABLE question_options (
    id BIGSERIAL PRIMARY KEY,
    question_id BIGINT NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
    position INTEGER NOT NULL CHECK (position >= 0),
    UNIQUE (question_id, position)
);

CREATE TABLE practice_attempts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    lesson_id BIGINT NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    correct_count INTEGER NOT NULL DEFAULT 0 CHECK (correct_count >= 0),
    total_count INTEGER NOT NULL DEFAULT 0 CHECK (total_count >= 0),
    CONSTRAINT practice_correct_not_above_total CHECK (correct_count <= total_count)
);

CREATE TABLE mastery (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id BIGINT NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    mastery_percentage NUMERIC(5, 2) NOT NULL CHECK (
        mastery_percentage >= 0 AND mastery_percentage <= 100
    ),
    mastery_label TEXT NOT NULL CHECK (
        mastery_label IN ('BEGINNER', 'DEVELOPING', 'INTERMEDIATE', 'PROFICIENT', 'MASTERED')
    ),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, topic_id)
);

CREATE TABLE weak_topics (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    topic_id BIGINT NOT NULL REFERENCES topics(id) ON DELETE CASCADE,
    accuracy NUMERIC(5, 2) NOT NULL CHECK (accuracy >= 0 AND accuracy <= 100),
    attempt_count INTEGER NOT NULL CHECK (attempt_count >= 0),
    average_difficulty NUMERIC(5, 2) NOT NULL CHECK (
        average_difficulty >= 0 AND average_difficulty <= 100
    ),
    UNIQUE (user_id, topic_id)
);

CREATE TABLE study_plans (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE study_plan_items (
    id BIGSERIAL PRIMARY KEY,
    study_plan_id BIGINT NOT NULL REFERENCES study_plans(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    description TEXT NOT NULL DEFAULT '',
    scheduled_date DATE NOT NULL,
    position INTEGER NOT NULL CHECK (position >= 0),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (study_plan_id, position)
);

CREATE TABLE conversations (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE messages (
    id BIGSERIAL PRIMARY KEY,
    conversation_id BIGINT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('USER', 'ASSISTANT')),
    content TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX topics_parent_topic_id_idx ON topics(parent_topic_id);
CREATE INDEX lessons_subtopic_id_idx ON lessons(subtopic_id);
CREATE INDEX questions_lesson_id_idx ON questions(lesson_id);
CREATE INDEX questions_topic_id_idx ON questions(topic_id);
CREATE INDEX practice_attempts_user_id_idx ON practice_attempts(user_id);
CREATE INDEX conversations_user_id_updated_at_idx ON conversations(user_id, updated_at DESC);
CREATE INDEX messages_conversation_id_created_at_idx ON messages(conversation_id, created_at);
