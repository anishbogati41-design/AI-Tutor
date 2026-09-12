from __future__ import annotations

from backend.adaptive.schemas import AdaptiveQuestionResponse
from backend.database.connection import Database
from backend.questions.repository import QuestionRepository
from backend.questions.schemas import QuestionOptionResponse, QuestionResponse


MASTERY_BANDS = (
    (30, "BEGINNER", 20.0),
    (50, "DEVELOPING", 40.0),
    (70, "INTERMEDIATE", 60.0),
    (90, "PROFICIENT", 80.0),
    (101, "MASTERED", 95.0),
)


def mastery_band(percentage: float) -> tuple[str, float]:
    for ceiling, label, target in MASTERY_BANDS:
        if percentage < ceiling:
            return label, target
    return "MASTERED", 95.0


def global_difficulty(incorrect_rate: float, attempt_count: int) -> float:
    """Apply blueprint weights; timing is neutral until timing data is approved."""
    response_time_factor = 0.5
    attempt_reliability = min(attempt_count / 10, 1.0)
    return round(
        100
        * (
            0.60 * min(max(incorrect_rate, 0), 1)
            + 0.25 * response_time_factor
            + 0.15 * attempt_reliability
        ),
        2,
    )


class AdaptiveService:
    def __init__(self, database: Database) -> None:
        self._database = database
        self._questions = QuestionRepository(database)

    async def update_after_answer(
        self, user_id: int, lesson_id: int, question_id: int
    ) -> None:
        async with self._database.connection() as connection:
            aggregate_cursor = await connection.execute(
                """
                SELECT l.subtopic_id,
                       COALESCE((
                         SELECT SUM(pa.correct_count)
                         FROM practice_attempts pa
                         JOIN lessons related ON related.id = pa.lesson_id
                         WHERE related.subtopic_id = l.subtopic_id AND pa.user_id = %s
                       ), 0),
                       COALESCE((
                         SELECT SUM(pa.total_count)
                         FROM practice_attempts pa
                         JOIN lessons related ON related.id = pa.lesson_id
                         WHERE related.subtopic_id = l.subtopic_id AND pa.user_id = %s
                       ), 0),
                       COALESCE((
                         SELECT AVG(q.difficulty_score)
                         FROM questions q WHERE q.topic_id = l.subtopic_id
                       ), 0)
                FROM lessons l
                WHERE l.id = %s
                """,
                (user_id, user_id, lesson_id),
            )
            row = await aggregate_cursor.fetchone()
            if row is None:
                return
            topic_id, correct_count, total_count, average_difficulty = row
            accuracy = round(100 * correct_count / total_count, 2) if total_count else 0
            label, _ = mastery_band(accuracy)
            await connection.execute(
                """
                INSERT INTO mastery (
                    user_id, topic_id, mastery_percentage, mastery_label
                ) VALUES (%s, %s, %s, %s)
                ON CONFLICT (user_id, topic_id) DO UPDATE
                SET mastery_percentage = EXCLUDED.mastery_percentage,
                    mastery_label = EXCLUDED.mastery_label,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (user_id, topic_id, accuracy, label),
            )
            if accuracy < 70:
                await connection.execute(
                    """
                    INSERT INTO weak_topics (
                        user_id, topic_id, accuracy, attempt_count, average_difficulty
                    ) VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (user_id, topic_id) DO UPDATE
                    SET accuracy = EXCLUDED.accuracy,
                        attempt_count = EXCLUDED.attempt_count,
                        average_difficulty = EXCLUDED.average_difficulty
                    """,
                    (user_id, topic_id, accuracy, total_count, average_difficulty),
                )
            else:
                await connection.execute(
                    "DELETE FROM weak_topics WHERE user_id = %s AND topic_id = %s",
                    (user_id, topic_id),
                )

            global_cursor = await connection.execute(
                """
                SELECT COALESCE(SUM(correct_count), 0), COALESCE(SUM(total_count), 0)
                FROM practice_attempts WHERE lesson_id = %s
                """,
                (lesson_id,),
            )
            global_row = await global_cursor.fetchone()
            if global_row and global_row[1]:
                incorrect_rate = 1 - global_row[0] / global_row[1]
                score = global_difficulty(incorrect_rate, global_row[1])
                await connection.execute(
                    "UPDATE questions SET difficulty_score = %s WHERE id = %s",
                    (score, question_id),
                )

    async def next_question(
        self, lesson_id: int, user_id: int, *, include_drafts: bool
    ) -> AdaptiveQuestionResponse | None:
        published_clause = "" if include_drafts else "AND l.is_published = TRUE"
        async with self._database.connection() as connection:
            mastery_cursor = await connection.execute(
                f"""
                SELECT l.subtopic_id, COALESCE(m.mastery_percentage, 0)
                FROM lessons l
                LEFT JOIN mastery m
                  ON m.topic_id = l.subtopic_id AND m.user_id = %s
                WHERE l.id = %s {published_clause}
                """,
                (user_id, lesson_id),
            )
            mastery_row = await mastery_cursor.fetchone()
            if mastery_row is None:
                return None
            percentage = float(mastery_row[1])
            label, target = mastery_band(percentage)
            question_cursor = await connection.execute(
                """
                SELECT id FROM questions
                WHERE lesson_id = %s
                ORDER BY ABS(difficulty_score - %s), random()
                LIMIT 1
                """,
                (lesson_id, target),
            )
            question_row = await question_cursor.fetchone()
        if question_row is None:
            return None
        question = await self._questions.get_by_id(
            question_row[0], include_drafts=include_drafts
        )
        if question is None:
            return None
        return AdaptiveQuestionResponse(
            mastery_percentage=percentage,
            mastery_label=label,
            target_difficulty=target,
            question=QuestionResponse(
                id=question.id,
                lesson_id=question.lesson_id,
                topic_id=question.topic_id,
                question_text=question.question_text,
                question_type=question.question_type,
                difficulty_score=question.difficulty_score,
                explanation=question.explanation if include_drafts else None,
                accepted_answers=question.accepted_answers if include_drafts else None,
                options=tuple(
                    QuestionOptionResponse(
                        id=option.id,
                        question_id=option.question_id,
                        option_text=option.option_text,
                        position=option.position,
                        is_correct=option.is_correct if include_drafts else None,
                    ) for option in question.options
                ),
            ),
        )
