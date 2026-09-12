ALTER TABLE practice_attempts
ADD CONSTRAINT practice_attempts_user_lesson_unique UNIQUE (user_id, lesson_id);
