import os
import uuid

import psycopg
import pytest
from fastapi.testclient import TestClient

from backend.auth.passwords import hash_password
from backend.config import get_settings
from backend.main import app


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="set RUN_INTEGRATION_TESTS=1 with PostgreSQL and Redis available",
)


def test_topic_lesson_visibility_and_admin_crud() -> None:
    settings = get_settings()
    suffix = uuid.uuid4().hex
    admin_email = f"phase3-admin-{suffix}@example.test"
    student_email = f"phase3-student-{suffix}@example.test"
    admin_id: int | None = None
    student_id: int | None = None
    parent_id: int | None = None
    child_id: int | None = None
    lesson_id: int | None = None

    try:
        with psycopg.connect(settings.database_url) as connection:
            cursor = connection.execute(
                """
                INSERT INTO users (name, email, password_hash, is_admin)
                VALUES (%s, %s, %s, TRUE)
                RETURNING id
                """,
                ("Phase Three Admin", admin_email, hash_password("admin-password")),
            )
            admin_id = cursor.fetchone()[0]

        with TestClient(app) as client:
            admin_login = client.post(
                "/auth/login",
                json={"email": admin_email, "password": "admin-password"},
            )
            assert admin_login.status_code == 200
            admin_session = client.cookies.get(settings.session_cookie_name)
            assert admin_session

            parent = client.post(
                "/admin/topics",
                json={"name": "Mathematics", "description": "Number studies"},
            )
            assert parent.status_code == 201
            parent_id = parent.json()["id"]

            child = client.post(
                "/admin/topics",
                json={
                    "name": "Algebra",
                    "description": "Symbols and equations",
                    "parent_topic_id": parent_id,
                },
            )
            assert child.status_code == 201
            child_id = child.json()["id"]

            lesson_payload = {
                "title": "Linear equations",
                "description": "Solve equations with one variable",
                "subtopic_id": child_id,
                "estimated_minutes": 20,
                "is_published": False,
                "sections": [
                    {
                        "section_type": "INTRODUCTION",
                        "title": "What is an equation?",
                        "content": "An equation states that two expressions are equal.",
                        "position": 0,
                    },
                    {
                        "section_type": "SUMMARY",
                        "title": "Review",
                        "content": "Use inverse operations to isolate the variable.",
                        "position": 1,
                    },
                ],
            }
            lesson = client.post("/admin/lessons", json=lesson_payload)
            assert lesson.status_code == 201
            lesson_id = lesson.json()["id"]
            assert [item["position"] for item in lesson.json()["sections"]] == [0, 1]

            admin_list = client.get("/lessons", params={"search": "linear"})
            assert admin_list.status_code == 200
            assert [item["id"] for item in admin_list.json()] == [lesson_id]

            client.cookies.clear()
            registration = client.post(
                "/auth/register",
                json={
                    "name": "Phase Three Student",
                    "email": student_email,
                    "password": "student-password",
                },
            )
            assert registration.status_code == 201
            student_id = registration.json()["id"]
            assert client.post(
                "/auth/login",
                json={"email": student_email, "password": "student-password"},
            ).status_code == 200
            student_session = client.cookies.get(settings.session_cookie_name)
            assert student_session

            assert client.get("/lessons").json() == []
            assert client.get(f"/lessons/{lesson_id}").status_code == 404
            assert client.post(
                "/admin/topics", json={"name": "Forbidden"}
            ).status_code == 403
            topics = client.get("/topics")
            assert topics.status_code == 200
            assert {item["id"] for item in topics.json()} >= {parent_id, child_id}
            subtopics = client.get(f"/topics/{parent_id}/subtopics")
            assert [item["id"] for item in subtopics.json()] == [child_id]

            client.cookies.clear()
            client.cookies.set(settings.session_cookie_name, admin_session)
            lesson_payload["is_published"] = True
            lesson_payload["sections"] = list(reversed(lesson_payload["sections"]))
            lesson_payload["sections"][0]["position"] = 1
            lesson_payload["sections"][1]["position"] = 0
            updated = client.put(f"/admin/lessons/{lesson_id}", json=lesson_payload)
            assert updated.status_code == 200
            assert [item["position"] for item in updated.json()["sections"]] == [0, 1]

            cycle = client.put(
                f"/admin/topics/{parent_id}",
                json={
                    "name": "Mathematics",
                    "description": "Number studies",
                    "parent_topic_id": child_id,
                },
            )
            assert cycle.status_code == 422
            assert client.delete(f"/admin/topics/{child_id}").status_code == 409

            client.cookies.clear()
            client.cookies.set(settings.session_cookie_name, student_session)
            published = client.get("/lessons", params={"topic_id": child_id})
            assert [item["id"] for item in published.json()] == [lesson_id]
            detail = client.get(f"/lessons/{lesson_id}")
            assert detail.status_code == 200
            assert [item["position"] for item in detail.json()["sections"]] == [0, 1]

            client.cookies.clear()
            client.cookies.set(settings.session_cookie_name, admin_session)
            assert client.delete(f"/admin/lessons/{lesson_id}").status_code == 204
            lesson_id = None
            assert client.delete(f"/admin/topics/{child_id}").status_code == 204
            child_id = None
            assert client.delete(f"/admin/topics/{parent_id}").status_code == 204
            parent_id = None
    finally:
        with psycopg.connect(settings.database_url) as connection:
            if lesson_id is not None:
                connection.execute("DELETE FROM lessons WHERE id = %s", (lesson_id,))
            if child_id is not None:
                connection.execute("DELETE FROM topics WHERE id = %s", (child_id,))
            if parent_id is not None:
                connection.execute("DELETE FROM topics WHERE id = %s", (parent_id,))
            for user_id in (student_id, admin_id):
                if user_id is not None:
                    connection.execute("DELETE FROM users WHERE id = %s", (user_id,))
