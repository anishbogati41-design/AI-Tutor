from __future__ import annotations

from datetime import date
from typing import Any

from psycopg import AsyncConnection

from backend.database.connection import Database
from backend.study_plans.models import (
    GeneratedStudyPlanItem,
    LearningSignal,
    StudyPlanItemRecord,
    StudyPlanRecord,
)


class StudyPlanRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    async def get_owned(self, user_id: int) -> StudyPlanRecord | None:
        async with self._database.connection() as connection:
            return await self._get_owned(connection, user_id)

    async def learning_signals(self, user_id: int) -> list[LearningSignal]:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                SELECT l.title,
                       t.name,
                       COALESCE(m.mastery_percentage, 0),
                       COALESCE(pa.correct_count, 0),
                       COALESCE(pa.total_count, 0),
                       w.accuracy
                FROM lessons l
                JOIN topics t ON t.id = l.subtopic_id
                LEFT JOIN mastery m
                  ON m.topic_id = l.subtopic_id AND m.user_id = %s
                LEFT JOIN practice_attempts pa
                  ON pa.lesson_id = l.id AND pa.user_id = %s
                LEFT JOIN weak_topics w
                  ON w.topic_id = l.subtopic_id AND w.user_id = %s
                WHERE l.is_published = TRUE
                ORDER BY (w.topic_id IS NULL),
                         COALESCE(w.accuracy, m.mastery_percentage, 0),
                         COALESCE(pa.total_count, 0),
                         t.name,
                         l.title,
                         l.id
                """,
                (user_id, user_id, user_id),
            )
            rows = await cursor.fetchall()
        return [
            LearningSignal(
                lesson_title=str(row[0]),
                topic_name=str(row[1]),
                mastery_percentage=float(row[2]),
                correct_count=int(row[3]),
                attempt_count=int(row[4]),
                weak_accuracy=float(row[5]) if row[5] is not None else None,
            )
            for row in rows
        ]

    async def replace(
        self, user_id: int, items: list[GeneratedStudyPlanItem]
    ) -> StudyPlanRecord:
        async with self._database.connection() as connection:
            plan_cursor = await connection.execute(
                """
                INSERT INTO study_plans (user_id)
                VALUES (%s)
                ON CONFLICT (user_id) DO UPDATE SET user_id = EXCLUDED.user_id
                RETURNING id
                """,
                (user_id,),
            )
            plan_row = await plan_cursor.fetchone()
            if plan_row is None:
                raise RuntimeError("study plan upsert did not return a row")
            plan_id = int(plan_row[0])
            await connection.execute(
                "DELETE FROM study_plan_items WHERE study_plan_id = %s", (plan_id,)
            )
            if items:
                async with connection.cursor() as cursor:
                    await cursor.executemany(
                        """
                        INSERT INTO study_plan_items (
                            study_plan_id, title, description, scheduled_date,
                            position, completed
                        ) VALUES (%s, %s, %s, %s, %s, %s)
                        """,
                        [
                            (
                                plan_id,
                                item.title,
                                item.description,
                                item.scheduled_date,
                                item.position,
                                item.completed,
                            )
                            for item in items
                        ],
                    )
            plan = await self._get_owned(connection, user_id)
        if plan is None:
            raise RuntimeError("replaced study plan could not be read")
        return plan

    @classmethod
    async def _get_owned(
        cls, connection: AsyncConnection[Any], user_id: int
    ) -> StudyPlanRecord | None:
        cursor = await connection.execute(
            "SELECT id, user_id FROM study_plans WHERE user_id = %s", (user_id,)
        )
        row = await cursor.fetchone()
        if row is None:
            return None
        plan_id = int(row[0])
        item_cursor = await connection.execute(
            """
            SELECT id, study_plan_id, title, description, scheduled_date,
                   position, completed
            FROM study_plan_items
            WHERE study_plan_id = %s
            ORDER BY scheduled_date, position, id
            """,
            (plan_id,),
        )
        items = tuple(cls._item(item) for item in await item_cursor.fetchall())
        return StudyPlanRecord(id=plan_id, user_id=int(row[1]), items=items)

    @staticmethod
    def _item(row: tuple[Any, ...]) -> StudyPlanItemRecord:
        scheduled_date = row[4]
        if not isinstance(scheduled_date, date):
            raise RuntimeError("study plan item returned an invalid date")
        return StudyPlanItemRecord(
            id=int(row[0]),
            study_plan_id=int(row[1]),
            title=str(row[2]),
            description=str(row[3]),
            scheduled_date=scheduled_date,
            position=int(row[5]),
            completed=bool(row[6]),
        )
