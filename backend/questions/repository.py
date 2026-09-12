from __future__ import annotations

from collections import defaultdict
from typing import Any

from psycopg import AsyncConnection

from backend.database.connection import Database
from backend.questions.models import (
    PracticeSessionRecord,
    PracticeSummaryRecord,
    QuestionOptionRecord,
    QuestionRecord,
)
from backend.questions.schemas import QuestionWriteRequest


class QuestionRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    @property
    def database(self) -> Database:
        return self._database

    async def get_practice_session(
        self, lesson_id: int, user_id: int, *, include_drafts: bool
    ) -> PracticeSessionRecord | None:
        published_clause = "" if include_drafts else "AND is_published = TRUE"
        async with self._database.connection() as connection:
            lesson_cursor = await connection.execute(
                f"""
                SELECT id, title
                FROM lessons
                WHERE id = %s {published_clause}
                """,
                (lesson_id,),
            )
            lesson = await lesson_cursor.fetchone()
            if lesson is None:
                return None
            questions = await self._get_for_lesson(connection, lesson_id)
            summary_cursor = await connection.execute(
                """
                SELECT correct_count, total_count
                FROM practice_attempts
                WHERE user_id = %s AND lesson_id = %s
                """,
                (user_id, lesson_id),
            )
            summary_row = await summary_cursor.fetchone()
        summary = PracticeSummaryRecord(
            lesson_id=lesson_id,
            correct_count=summary_row[0] if summary_row else 0,
            total_count=summary_row[1] if summary_row else 0,
        )
        return PracticeSessionRecord(
            lesson_id=lesson[0],
            lesson_title=lesson[1],
            summary=summary,
            questions=tuple(questions),
        )

    async def get_by_id(
        self, question_id: int, *, include_drafts: bool
    ) -> QuestionRecord | None:
        published_clause = "" if include_drafts else "AND l.is_published = TRUE"
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                f"""
                SELECT q.id, q.lesson_id, q.topic_id, q.question_text,
                       q.question_type, q.difficulty_score, q.explanation,
                       q.accepted_answers
                FROM questions q
                JOIN lessons l ON l.id = q.lesson_id
                WHERE q.id = %s {published_clause}
                """,
                (question_id,),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            options = await self._get_options(connection, [question_id])
        return self._question_record(row, options.get(question_id, []))

    async def create(
        self, lesson_id: int, payload: QuestionWriteRequest
    ) -> QuestionRecord:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                INSERT INTO questions (
                    lesson_id, topic_id, question_text, question_type,
                    difficulty_score, explanation, accepted_answers
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id, lesson_id, topic_id, question_text,
                          question_type, difficulty_score, explanation,
                          accepted_answers
                """,
                (
                    lesson_id,
                    payload.topic_id,
                    payload.question_text,
                    payload.question_type.value,
                    payload.difficulty_score,
                    payload.explanation,
                    payload.accepted_answers or None,
                ),
            )
            row = await cursor.fetchone()
            if row is None:
                raise RuntimeError("question insert did not return a row")
            await self._insert_options(connection, row[0], payload)
            options = await self._get_options(connection, [row[0]])
        return self._question_record(row, options.get(row[0], []))

    async def update(
        self, lesson_id: int, question_id: int, payload: QuestionWriteRequest
    ) -> QuestionRecord | None:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                UPDATE questions
                SET topic_id = %s,
                    question_text = %s,
                    question_type = %s,
                    difficulty_score = %s,
                    explanation = %s,
                    accepted_answers = %s
                WHERE id = %s AND lesson_id = %s
                RETURNING id, lesson_id, topic_id, question_text,
                          question_type, difficulty_score, explanation,
                          accepted_answers
                """,
                (
                    payload.topic_id,
                    payload.question_text,
                    payload.question_type.value,
                    payload.difficulty_score,
                    payload.explanation,
                    payload.accepted_answers or None,
                    question_id,
                    lesson_id,
                ),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            await connection.execute(
                "DELETE FROM question_options WHERE question_id = %s", (question_id,)
            )
            await self._insert_options(connection, question_id, payload)
            options = await self._get_options(connection, [question_id])
        return self._question_record(row, options.get(question_id, []))

    async def delete(self, lesson_id: int, question_id: int) -> bool:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                "DELETE FROM questions WHERE id = %s AND lesson_id = %s",
                (question_id, lesson_id),
            )
            return cursor.rowcount > 0

    async def record_answer(
        self, user_id: int, lesson_id: int, *, is_correct: bool
    ) -> PracticeSummaryRecord:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                INSERT INTO practice_attempts (
                    user_id, lesson_id, correct_count, total_count
                )
                VALUES (%s, %s, %s, 1)
                ON CONFLICT (user_id, lesson_id) DO UPDATE
                SET correct_count = practice_attempts.correct_count + EXCLUDED.correct_count,
                    total_count = practice_attempts.total_count + 1
                RETURNING correct_count, total_count
                """,
                (user_id, lesson_id, int(is_correct)),
            )
            row = await cursor.fetchone()
        if row is None:
            raise RuntimeError("practice summary update did not return a row")
        return PracticeSummaryRecord(
            lesson_id=lesson_id, correct_count=row[0], total_count=row[1]
        )

    async def _get_for_lesson(
        self, connection: AsyncConnection, lesson_id: int
    ) -> list[QuestionRecord]:
        cursor = await connection.execute(
            """
            SELECT id, lesson_id, topic_id, question_text, question_type,
                   difficulty_score, explanation, accepted_answers
            FROM questions
            WHERE lesson_id = %s
            ORDER BY id
            """,
            (lesson_id,),
        )
        rows = await cursor.fetchall()
        options = await self._get_options(connection, [row[0] for row in rows])
        return [self._question_record(row, options.get(row[0], [])) for row in rows]

    @staticmethod
    async def _get_options(
        connection: AsyncConnection, question_ids: list[int]
    ) -> dict[int, list[QuestionOptionRecord]]:
        if not question_ids:
            return {}
        cursor = await connection.execute(
            """
            SELECT id, question_id, option_text, is_correct, position
            FROM question_options
            WHERE question_id = ANY(%s)
            ORDER BY question_id, position
            """,
            (question_ids,),
        )
        options: dict[int, list[QuestionOptionRecord]] = defaultdict(list)
        for row in await cursor.fetchall():
            option = QuestionRepository._option_record(row)
            options[option.question_id].append(option)
        return options

    @staticmethod
    async def _insert_options(
        connection: AsyncConnection,
        question_id: int,
        payload: QuestionWriteRequest,
    ) -> None:
        for option in sorted(payload.options, key=lambda item: item.position):
            await connection.execute(
                """
                INSERT INTO question_options (
                    question_id, option_text, is_correct, position
                )
                VALUES (%s, %s, %s, %s)
                """,
                (question_id, option.option_text, option.is_correct, option.position),
            )

    @staticmethod
    def _question_record(
        row: tuple[Any, ...], options: list[QuestionOptionRecord]
    ) -> QuestionRecord:
        return QuestionRecord(
            id=row[0],
            lesson_id=row[1],
            topic_id=row[2],
            question_text=row[3],
            question_type=row[4],
            difficulty_score=float(row[5]),
            explanation=row[6],
            accepted_answers=tuple(row[7] or ()),
            options=tuple(options),
        )

    @staticmethod
    def _option_record(row: tuple[Any, ...]) -> QuestionOptionRecord:
        return QuestionOptionRecord(
            id=row[0],
            question_id=row[1],
            option_text=row[2],
            is_correct=row[3],
            position=row[4],
        )
