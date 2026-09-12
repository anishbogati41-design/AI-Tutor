from __future__ import annotations

import logging

import psycopg

from backend.auth.passwords import hash_password
from backend.config import get_settings
from backend.logging.config import configure_logging

logger = logging.getLogger(__name__)


def _seed_admin(connection: psycopg.Connection, email: str, password: str) -> None:
    password_hash = hash_password(password)
    connection.execute(
        """
        INSERT INTO users (name, email, password_hash, is_admin)
        VALUES ('Local Administrator', %s, %s, TRUE)
        ON CONFLICT (email) DO UPDATE
        SET is_admin = TRUE, password_hash = EXCLUDED.password_hash
        """,
        (email.strip().lower(), password_hash),
    )


def _topic_id(
    connection: psycopg.Connection,
    name: str,
    parent_topic_id: int | None,
    description: str,
) -> int:
    cursor = connection.execute(
        """
        SELECT id
        FROM topics
        WHERE name = %s AND parent_topic_id IS NOT DISTINCT FROM %s
        ORDER BY id
        LIMIT 1
        """,
        (name, parent_topic_id),
    )
    row = cursor.fetchone()
    if row:
        return row[0]
    return connection.execute(
        """
        INSERT INTO topics (name, parent_topic_id, description)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (name, parent_topic_id, description),
    ).fetchone()[0]


def _lesson_id(connection: psycopg.Connection, subtopic_id: int) -> int:
    row = connection.execute(
        """
        SELECT id
        FROM lessons
        WHERE title = 'Introduction to Algebra' AND subtopic_id = %s
        ORDER BY id
        LIMIT 1
        """,
        (subtopic_id,),
    ).fetchone()
    if row:
        connection.execute(
            "UPDATE lessons SET is_published = TRUE WHERE id = %s", (row[0],)
        )
        return row[0]
    return connection.execute(
        """
        INSERT INTO lessons (
            title, description, subtopic_id, estimated_minutes, is_published
        )
        VALUES (
            'Introduction to Algebra',
            'Learn variables, expressions, and the steps used to solve a simple equation.',
            %s,
            20,
            TRUE
        )
        RETURNING id
        """,
        (subtopic_id,),
    ).fetchone()[0]


def _seed_sections(connection: psycopg.Connection, lesson_id: int) -> None:
    existing = connection.execute(
        "SELECT 1 FROM lesson_sections WHERE lesson_id = %s LIMIT 1", (lesson_id,)
    ).fetchone()
    if existing:
        return
    sections = (
        (
            "INTRODUCTION",
            "What algebra helps us do",
            "Algebra uses symbols to represent values. A letter such as x can stand for a number we do not know yet.",
            0,
        ),
        (
            "EXPLANATION",
            "Keep an equation balanced",
            "An equation says that two expressions are equal. Whatever operation you apply to one side must also be applied to the other side.",
            1,
        ),
        (
            "EXAMPLE",
            "Solve 2x + 4 = 10",
            "Subtract 4 from both sides to get 2x = 6. Then divide both sides by 2. The result is x = 3.",
            2,
        ),
        (
            "SUMMARY",
            "Review",
            "Use inverse operations one step at a time, keep both sides balanced, and check the result in the original equation.",
            3,
        ),
    )
    for section_type, title, content, position in sections:
        connection.execute(
            """
            INSERT INTO lesson_sections (
                lesson_id, section_type, title, content, position
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (lesson_id, section_type, title, content, position),
        )


def _question_id(
    connection: psycopg.Connection,
    lesson_id: int,
    topic_id: int,
    question_text: str,
    question_type: str,
    difficulty_score: float,
    explanation: str,
    accepted_answers: list[str] | None = None,
) -> tuple[int, bool]:
    row = connection.execute(
        """
        SELECT id FROM questions
        WHERE lesson_id = %s AND question_text = %s
        ORDER BY id
        LIMIT 1
        """,
        (lesson_id, question_text),
    ).fetchone()
    if row:
        return row[0], False
    question_id = connection.execute(
        """
        INSERT INTO questions (
            lesson_id, topic_id, question_text, question_type,
            difficulty_score, explanation, accepted_answers
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            lesson_id,
            topic_id,
            question_text,
            question_type,
            difficulty_score,
            explanation,
            accepted_answers,
        ),
    ).fetchone()[0]
    return question_id, True


def _seed_questions(
    connection: psycopg.Connection, lesson_id: int, topic_id: int
) -> None:
    mcq_id, created = _question_id(
        connection,
        lesson_id,
        topic_id,
        "Solve 2x + 4 = 10. What is x?",
        "MCQ",
        25,
        "Subtract 4 from both sides, then divide by 2: 2x = 6, so x = 3.",
    )
    if created:
        for position, (text, correct) in enumerate(
            (("2", False), ("3", True), ("4", False), ("7", False))
        ):
            connection.execute(
                """
                INSERT INTO question_options (
                    question_id, option_text, is_correct, position
                ) VALUES (%s, %s, %s, %s)
                """,
                (mcq_id, text, correct, position),
            )

    true_false_id, created = _question_id(
        connection,
        lesson_id,
        topic_id,
        "You must perform the same operation on both sides of an equation.",
        "TRUE_FALSE",
        20,
        "Applying the same operation to both sides keeps the equation balanced.",
    )
    if created:
        for position, (text, correct) in enumerate(
            (("True", True), ("False", False))
        ):
            connection.execute(
                """
                INSERT INTO question_options (
                    question_id, option_text, is_correct, position
                ) VALUES (%s, %s, %s, %s)
                """,
                (true_false_id, text, correct, position),
            )

    _question_id(
        connection,
        lesson_id,
        topic_id,
        "Solve x + 5 = 12.",
        "SHORT_ANSWER",
        30,
        "Subtract 5 from both sides. The answer is x = 7.",
        ["7", "seven"],
    )


def seed() -> None:
    settings = get_settings()
    if settings.app_env != "development":
        raise RuntimeError("Local starter content can only be seeded in development")
    configure_logging(settings.log_level)
    with psycopg.connect(settings.database_url) as connection:
        if settings.admin_seed_email and settings.admin_seed_password:
            _seed_admin(
                connection, settings.admin_seed_email, settings.admin_seed_password
            )
        mathematics_id = _topic_id(
            connection,
            "Mathematics",
            None,
            "The study of numbers, structures, patterns, and change.",
        )
        algebra_id = _topic_id(
            connection,
            "Algebra",
            mathematics_id,
            "Use symbols and equations to describe and solve relationships.",
        )
        lesson_id = _lesson_id(connection, algebra_id)
        _seed_sections(connection, lesson_id)
        _seed_questions(connection, lesson_id, algebra_id)
    logger.info("Local starter content and configured administrator are ready")


if __name__ == "__main__":
    seed()
