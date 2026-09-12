from __future__ import annotations

from backend.database.connection import Database
from backend.progress.schemas import (
    AdminStudentResponse,
    AdminStudentProgressResponse,
    CourseProgressResponse,
    MasteryResponse,
    ProgressResponse,
    StudyPlanPreviewItem,
    TopicAccuracyResponse,
    WeakTopicResponse,
)


class StudentNotFoundError(Exception):
    pass


class ProgressService:
    def __init__(self, database: Database) -> None:
        self._database = database

    async def get(self, user_id: int) -> ProgressResponse:
        async with self._database.connection() as connection:
            user_cursor = await connection.execute("SELECT 1 FROM users WHERE id = %s", (user_id,))
            if await user_cursor.fetchone() is None:
                raise StudentNotFoundError
            accuracy_cursor = await connection.execute(
                """
                SELECT t.id, t.name, COALESCE(SUM(pa.correct_count), 0),
                       COALESCE(SUM(pa.total_count), 0)
                FROM practice_attempts pa
                JOIN lessons l ON l.id = pa.lesson_id
                JOIN topics t ON t.id = l.subtopic_id
                WHERE pa.user_id = %s
                GROUP BY t.id, t.name ORDER BY t.name
                """,
                (user_id,),
            )
            accuracy_rows = await accuracy_cursor.fetchall()
            mastery_cursor = await connection.execute(
                """
                SELECT t.id, t.name, m.mastery_percentage, m.mastery_label
                FROM mastery m JOIN topics t ON t.id = m.topic_id
                WHERE m.user_id = %s ORDER BY t.name
                """,
                (user_id,),
            )
            mastery_rows = await mastery_cursor.fetchall()
            weak_cursor = await connection.execute(
                """
                SELECT t.id, t.name, w.accuracy, w.attempt_count,
                       w.average_difficulty
                FROM weak_topics w JOIN topics t ON t.id = w.topic_id
                WHERE w.user_id = %s ORDER BY w.accuracy, t.name
                """,
                (user_id,),
            )
            weak_rows = await weak_cursor.fetchall()
            plan_cursor = await connection.execute(
                """
                SELECT i.id, i.title, i.scheduled_date, i.completed
                FROM study_plan_items i
                JOIN study_plans p ON p.id = i.study_plan_id
                WHERE p.user_id = %s
                ORDER BY i.scheduled_date, i.position LIMIT 3
                """,
                (user_id,),
            )
            plan_rows = await plan_cursor.fetchall()
            courses_cursor = await connection.execute(
                """
                SELECT l.id, l.title, t.name,
                       COALESCE(pa.correct_count, 0),
                       COALESCE(pa.total_count, 0),
                       COUNT(q.id)
                FROM lessons l
                JOIN topics t ON t.id = l.subtopic_id
                LEFT JOIN practice_attempts pa
                  ON pa.lesson_id = l.id AND pa.user_id = %s
                LEFT JOIN questions q ON q.lesson_id = l.id
                WHERE l.is_published = TRUE
                GROUP BY l.id, l.title, t.name, pa.correct_count, pa.total_count
                ORDER BY l.title
                """,
                (user_id,),
            )
            course_rows = await courses_cursor.fetchall()

        correct = sum(row[2] for row in accuracy_rows)
        attempts = sum(row[3] for row in accuracy_rows)
        topic_accuracy = [
            TopicAccuracyResponse(
                topic_id=row[0], topic_name=row[1],
                accuracy=round(100 * row[2] / row[3], 2) if row[3] else 0,
                correct_count=row[2], attempt_count=row[3],
            ) for row in accuracy_rows
        ]
        return ProgressResponse(
            overall_score=round(100 * correct / attempts, 2) if attempts else 0,
            topic_accuracy=topic_accuracy,
            mastery=[MasteryResponse(topic_id=r[0], topic_name=r[1], mastery_percentage=float(r[2]), mastery_label=r[3]) for r in mastery_rows],
            weak_topics=[WeakTopicResponse(topic_id=r[0], topic_name=r[1], accuracy=float(r[2]), attempt_count=r[3], average_difficulty=float(r[4])) for r in weak_rows],
            recent_improvement=0,
            study_plan_preview=[StudyPlanPreviewItem(id=r[0], title=r[1], scheduled_date=r[2].isoformat(), completed=r[3]) for r in plan_rows],
            course_progress=[self._course_progress(row) for row in course_rows],
        )

    async def students(self) -> list[AdminStudentResponse]:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                "SELECT id, name, email FROM users WHERE is_admin = FALSE ORDER BY name, id"
            )
            rows = await cursor.fetchall()
        return [AdminStudentResponse(id=r[0], name=r[1], email=r[2]) for r in rows]

    async def student_progress(self, user_id: int) -> AdminStudentProgressResponse:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                "SELECT id, name, email FROM users WHERE id = %s AND is_admin = FALSE", (user_id,)
            )
            row = await cursor.fetchone()
            if row is None:
                raise StudentNotFoundError
        return AdminStudentProgressResponse(
            student=AdminStudentResponse(id=row[0], name=row[1], email=row[2]),
            progress=await self.get(user_id),
        )

    @staticmethod
    def _course_progress(row: tuple[object, ...]) -> CourseProgressResponse:
        correct_count = int(row[3])
        attempt_count = int(row[4])
        question_count = int(row[5])
        accuracy = round(100 * correct_count / attempt_count, 2) if attempt_count else 0
        progress = round(100 * min(attempt_count, question_count) / question_count, 2) if question_count else 0
        status = "COMPLETED" if progress == 100 else "IN_PROGRESS" if attempt_count else "NOT_STARTED"
        return CourseProgressResponse(
            lesson_id=int(row[0]), lesson_title=str(row[1]), topic_name=str(row[2]),
            correct_count=correct_count, attempt_count=attempt_count, accuracy=accuracy,
            progress_percentage=progress, status=status,
        )
