from __future__ import annotations

from typing import Any

from psycopg.errors import ForeignKeyViolation

from backend.database.connection import Database
from backend.topics.models import TopicRecord


class TopicInUseError(Exception):
    pass


class TopicRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    async def list_all(self) -> list[TopicRecord]:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                SELECT id, name, parent_topic_id, description
                FROM topics
                ORDER BY parent_topic_id NULLS FIRST, name, id
                """
            )
            rows = await cursor.fetchall()
        return [self._record(row) for row in rows]

    async def list_children(self, topic_id: int) -> list[TopicRecord]:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                SELECT id, name, parent_topic_id, description
                FROM topics
                WHERE parent_topic_id = %s
                ORDER BY name, id
                """,
                (topic_id,),
            )
            rows = await cursor.fetchall()
        return [self._record(row) for row in rows]

    async def get_by_id(self, topic_id: int) -> TopicRecord | None:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                SELECT id, name, parent_topic_id, description
                FROM topics
                WHERE id = %s
                """,
                (topic_id,),
            )
            row = await cursor.fetchone()
        return self._record(row) if row is not None else None

    async def create(
        self, name: str, parent_topic_id: int | None, description: str
    ) -> TopicRecord:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                INSERT INTO topics (name, parent_topic_id, description)
                VALUES (%s, %s, %s)
                RETURNING id, name, parent_topic_id, description
                """,
                (name, parent_topic_id, description),
            )
            row = await cursor.fetchone()
        if row is None:
            raise RuntimeError("topic insert did not return a row")
        return self._record(row)

    async def update(
        self,
        topic_id: int,
        name: str,
        parent_topic_id: int | None,
        description: str,
    ) -> TopicRecord | None:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                UPDATE topics
                SET name = %s, parent_topic_id = %s, description = %s
                WHERE id = %s
                RETURNING id, name, parent_topic_id, description
                """,
                (name, parent_topic_id, description, topic_id),
            )
            row = await cursor.fetchone()
        return self._record(row) if row is not None else None

    async def parent_would_create_cycle(
        self, topic_id: int, parent_topic_id: int
    ) -> bool:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                WITH RECURSIVE descendants AS (
                    SELECT id FROM topics WHERE id = %s
                    UNION ALL
                    SELECT child.id
                    FROM topics child
                    JOIN descendants parent ON child.parent_topic_id = parent.id
                )
                SELECT EXISTS(
                    SELECT 1 FROM descendants WHERE id = %s
                )
                """,
                (topic_id, parent_topic_id),
            )
            row = await cursor.fetchone()
        return bool(row and row[0])

    async def delete(self, topic_id: int) -> bool:
        try:
            async with self._database.connection() as connection:
                cursor = await connection.execute(
                    "DELETE FROM topics WHERE id = %s", (topic_id,)
                )
                deleted = cursor.rowcount > 0
        except ForeignKeyViolation as exc:
            raise TopicInUseError from exc
        return deleted

    @staticmethod
    def _record(row: tuple[Any, ...]) -> TopicRecord:
        return TopicRecord(
            id=row[0], name=row[1], parent_topic_id=row[2], description=row[3]
        )
