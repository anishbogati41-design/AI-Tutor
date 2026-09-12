import os
import uuid

import psycopg
import pytest
from fastapi.testclient import TestClient

from backend.config import get_settings
from backend.main import app


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="set RUN_INTEGRATION_TESTS=1 with PostgreSQL and Redis available",
)


def test_owned_study_plan_generation_and_atomic_refresh() -> None:
    settings = get_settings()
    suffix = uuid.uuid4().hex
    email = f"phase8-{suffix}@example.test"
    other_email = f"phase8-other-{suffix}@example.test"
    ids: dict[str, int] = {}

    try:
        with TestClient(app) as client:
            assert client.get("/study-plan").status_code == 401
            registration = client.post(
                "/auth/register",
                json={
                    "name": "Phase Eight Student",
                    "email": email,
                    "password": "student-password",
                },
            )
            assert registration.status_code == 201
            ids["student"] = registration.json()["id"]
            assert client.post(
                "/auth/login",
                json={"email": email, "password": "student-password"},
            ).status_code == 200

            with psycopg.connect(settings.database_url) as connection:
                parent = connection.execute(
                    "INSERT INTO topics (name) VALUES (%s) RETURNING id",
                    (f"Phase 8 parent {suffix}",),
                ).fetchone()
                ids["parent"] = parent[0]
                weak_topic = connection.execute(
                    """
                    INSERT INTO topics (name, parent_topic_id)
                    VALUES (%s, %s) RETURNING id
                    """,
                    (f"Fractions {suffix}", ids["parent"]),
                ).fetchone()
                ids["weak_topic"] = weak_topic[0]
                fresh_topic = connection.execute(
                    """
                    INSERT INTO topics (name, parent_topic_id)
                    VALUES (%s, %s) RETURNING id
                    """,
                    (f"Geometry {suffix}", ids["parent"]),
                ).fetchone()
                ids["fresh_topic"] = fresh_topic[0]
                weak_lesson = connection.execute(
                    """
                    INSERT INTO lessons (
                        title, subtopic_id, estimated_minutes, is_published
                    ) VALUES (%s, %s, 10, TRUE) RETURNING id
                    """,
                    ("Equivalent Fractions", ids["weak_topic"]),
                ).fetchone()
                ids["weak_lesson"] = weak_lesson[0]
                fresh_lesson = connection.execute(
                    """
                    INSERT INTO lessons (
                        title, subtopic_id, estimated_minutes, is_published
                    ) VALUES (%s, %s, 10, TRUE) RETURNING id
                    """,
                    ("Triangle Basics", ids["fresh_topic"]),
                ).fetchone()
                ids["fresh_lesson"] = fresh_lesson[0]
                connection.execute(
                    """
                    INSERT INTO practice_attempts (
                        user_id, lesson_id, correct_count, total_count
                    ) VALUES (%s, %s, 1, 4)
                    """,
                    (ids["student"], ids["weak_lesson"]),
                )
                connection.execute(
                    """
                    INSERT INTO mastery (
                        user_id, topic_id, mastery_percentage, mastery_label
                    ) VALUES (%s, %s, 25, 'BEGINNER')
                    """,
                    (ids["student"], ids["weak_topic"]),
                )
                connection.execute(
                    """
                    INSERT INTO weak_topics (
                        user_id, topic_id, accuracy, attempt_count,
                        average_difficulty
                    ) VALUES (%s, %s, 25, 4, 30)
                    """,
                    (ids["student"], ids["weak_topic"]),
                )

            assert client.get("/study-plan").json() is None
            generated = client.post("/study-plan/refresh")
            assert generated.status_code == 200
            first_plan = generated.json()
            assert first_plan["user_id"] == ids["student"]
            assert len(first_plan["items"]) >= 2
            assert first_plan["items"][0]["title"] == (
                f"Practice: Fractions {suffix} — Weak Topic"
            )
            assert [item["position"] for item in first_plan["items"]] == list(
                range(len(first_plan["items"]))
            )
            first_item_ids = {item["id"] for item in first_plan["items"]}
            assert client.get("/study-plan").json() == first_plan

            replaced = client.post("/study-plan/refresh")
            assert replaced.status_code == 200
            second_plan = replaced.json()
            assert second_plan["id"] == first_plan["id"]
            assert first_item_ids.isdisjoint(
                {item["id"] for item in second_plan["items"]}
            )

            client.cookies.clear()
            other = client.post(
                "/auth/register",
                json={
                    "name": "Other Phase Eight Student",
                    "email": other_email,
                    "password": "student-password",
                },
            )
            assert other.status_code == 201
            ids["other"] = other.json()["id"]
            assert client.post(
                "/auth/login",
                json={"email": other_email, "password": "student-password"},
            ).status_code == 200
            assert client.get("/study-plan").json() is None
    finally:
        with psycopg.connect(settings.database_url) as connection:
            for key in ("student", "other"):
                if key in ids:
                    connection.execute("DELETE FROM users WHERE id = %s", (ids[key],))
            for key in ("weak_lesson", "fresh_lesson"):
                if key in ids:
                    connection.execute("DELETE FROM lessons WHERE id = %s", (ids[key],))
            for key in ("weak_topic", "fresh_topic"):
                if key in ids:
                    connection.execute("DELETE FROM topics WHERE id = %s", (ids[key],))
            if "parent" in ids:
                connection.execute("DELETE FROM topics WHERE id = %s", (ids["parent"],))
