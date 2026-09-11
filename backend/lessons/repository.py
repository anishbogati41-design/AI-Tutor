from __future__ import annotations

from typing import Any

from psycopg import AsyncConnection
from psycopg.errors import ForeignKeyViolation

from backend.database.connection import Database
from backend.lessons.models import (
    LessonDetailRecord,
    LessonRecord,
    LessonSectionRecord,
)
from backend.lessons.schemas import LessonWriteRequest


class LessonInUseError(Exception):
    pass


class LessonRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    async def list_all(
        self,
        *,
        include_drafts: bool,
        search: str | None = None,
        topic_id: int | None = None,
    ) -> list[LessonRecord]:
        conditions: list[str] = []
        parameters: list[object] = []
        if not include_drafts:
            conditions.append("is_published = TRUE")
        if search:
            conditions.append("(title ILIKE %s OR description ILIKE %s)")
            term = f"%{search}%"
            parameters.extend((term, term))
        if topic_id is not None:
            conditions.append("subtopic_id = %s")
            parameters.append(topic_id)
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        async with self._database.connection() as connection:
            cursor = await connection.execute(
                f"""
                SELECT id, title, description, subtopic_id,
                       estimated_minutes, is_published
                FROM lessons
                {where_clause}
                ORDER BY title, id
                """,
                tuple(parameters),
            )
            rows = await cursor.fetchall()
        return [self._lesson_record(row) for row in rows]

    async def get_by_id(
        self, lesson_id: int, *, include_drafts: bool
    ) -> LessonDetailRecord | None:
        published_clause = "" if include_drafts else "AND is_published = TRUE"
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                f"""
                SELECT id, title, description, subtopic_id,
                       estimated_minutes, is_published
                FROM lessons
                WHERE id = %s {published_clause}
                """,
                (lesson_id,),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            sections = await self._get_sections(connection, lesson_id)
        lesson = self._lesson_record(row)
        return LessonDetailRecord(
            id=lesson.id,
            title=lesson.title,
            description=lesson.description,
            subtopic_id=lesson.subtopic_id,
            estimated_minutes=lesson.estimated_minutes,
            is_published=lesson.is_published,
            sections=tuple(sections),
        )

    async def create(self, payload: LessonWriteRequest) -> LessonDetailRecord:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                INSERT INTO lessons (
                    title, description, subtopic_id, estimated_minutes, is_published
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id, title, description, subtopic_id,
                          estimated_minutes, is_published
                """,
                (
                    payload.title,
                    payload.description,
                    payload.subtopic_id,
                    payload.estimated_minutes,
                    payload.is_published,
                ),
            )
            row = await cursor.fetchone()
            if row is None:
                raise RuntimeError("lesson insert did not return a row")
            lesson = self._lesson_record(row)
            await self._insert_sections(connection, lesson.id, payload)
            sections = await self._get_sections(connection, lesson.id)
        return self._detail_record(lesson, sections)

    async def update(
        self, lesson_id: int, payload: LessonWriteRequest
    ) -> LessonDetailRecord | None:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                UPDATE lessons
                SET title = %s,
                    description = %s,
                    subtopic_id = %s,
                    estimated_minutes = %s,
                    is_published = %s
                WHERE id = %s
                RETURNING id, title, description, subtopic_id,
                          estimated_minutes, is_published
                """,
                (
                    payload.title,
                    payload.description,
                    payload.subtopic_id,
                    payload.estimated_minutes,
                    payload.is_published,
                    lesson_id,
                ),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            await connection.execute(
                "DELETE FROM lesson_sections WHERE lesson_id = %s", (lesson_id,)
            )
            await self._insert_sections(connection, lesson_id, payload)
            sections = await self._get_sections(connection, lesson_id)
        return self._detail_record(self._lesson_record(row), sections)

    async def delete(self, lesson_id: int) -> bool:
        try:
            async with self._database.connection() as connection:
                cursor = await connection.execute(
                    "DELETE FROM lessons WHERE id = %s", (lesson_id,)
                )
                deleted = cursor.rowcount > 0
        except ForeignKeyViolation as exc:
            raise LessonInUseError from exc
        return deleted

    @staticmethod
    async def _insert_sections(
        connection: AsyncConnection, lesson_id: int, payload: LessonWriteRequest
    ) -> None:
        for section in sorted(payload.sections, key=lambda item: item.position):
            await connection.execute(
                """
                INSERT INTO lesson_sections (
                    lesson_id, section_type, title, content, position
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    lesson_id,
                    section.section_type.value,
                    section.title,
                    section.content,
                    section.position,
                ),
            )

    @staticmethod
    async def _get_sections(
        connection: AsyncConnection, lesson_id: int
    ) -> list[LessonSectionRecord]:
        cursor = await connection.execute(
            """
            SELECT id, lesson_id, section_type, title, content, position
            FROM lesson_sections
            WHERE lesson_id = %s
            ORDER BY position
            """,
            (lesson_id,),
        )
        return [LessonRepository._section_record(row) for row in await cursor.fetchall()]

    @staticmethod
    def _lesson_record(row: tuple[Any, ...]) -> LessonRecord:
        return LessonRecord(
            id=row[0],
            title=row[1],
            description=row[2],
            subtopic_id=row[3],
            estimated_minutes=row[4],
            is_published=row[5],
        )

    @staticmethod
    def _section_record(row: tuple[Any, ...]) -> LessonSectionRecord:
        return LessonSectionRecord(
            id=row[0],
            lesson_id=row[1],
            section_type=row[2],
            title=row[3],
            content=row[4],
            position=row[5],
        )

    @staticmethod
    def _detail_record(
        lesson: LessonRecord, sections: list[LessonSectionRecord]
    ) -> LessonDetailRecord:
        return LessonDetailRecord(
            id=lesson.id,
            title=lesson.title,
            description=lesson.description,
            subtopic_id=lesson.subtopic_id,
            estimated_minutes=lesson.estimated_minutes,
            is_published=lesson.is_published,
            sections=tuple(sections),
        )
