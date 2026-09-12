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


def test_question_crud_answer_evaluation_and_practice_summary() -> None:
    settings = get_settings()
    suffix = uuid.uuid4().hex
    admin_email = f"phase4-admin-{suffix}@example.test"
    student_email = f"phase4-student-{suffix}@example.test"
    ids: dict[str, int] = {}

    try:
        with psycopg.connect(settings.database_url) as connection:
            cursor = connection.execute(
                """
                INSERT INTO users (name, email, password_hash, is_admin)
                VALUES (%s, %s, %s, TRUE)
                RETURNING id
                """,
                ("Phase Four Admin", admin_email, hash_password("admin-password")),
            )
            ids["admin"] = cursor.fetchone()[0]

        with TestClient(app) as client:
            assert client.post(
                "/auth/login",
                json={"email": admin_email, "password": "admin-password"},
            ).status_code == 403
            assert client.post(
                "/auth/admin-login",
                json={
                    "email": admin_email,
                    "password": "admin-password",
                    "pin": "incorrect-pin",
                },
            ).status_code == 401
            assert client.post(
                "/auth/admin-login",
                json={
                    "email": admin_email,
                    "password": "admin-password",
                    "pin": settings.admin_login_pin,
                },
            ).status_code == 200
            admin_session = client.cookies.get(settings.session_cookie_name)
            assert admin_session

            parent = client.post("/admin/topics", json={"name": "Science"})
            assert parent.status_code == 201
            ids["parent"] = parent.json()["id"]
            child = client.post(
                "/admin/topics",
                json={"name": "Physics", "parent_topic_id": ids["parent"]},
            )
            assert child.status_code == 201
            ids["child"] = child.json()["id"]
            lesson = client.post(
                "/admin/lessons",
                json={
                    "title": "Motion",
                    "subtopic_id": ids["child"],
                    "estimated_minutes": 15,
                    "is_published": True,
                    "sections": [],
                },
            )
            assert lesson.status_code == 201
            ids["lesson"] = lesson.json()["id"]

            mcq = client.post(
                f"/admin/lessons/{ids['lesson']}/questions",
                json={
                    "topic_id": ids["child"],
                    "question_text": "What is the SI unit of speed?",
                    "question_type": "MCQ",
                    "difficulty_score": 25,
                    "explanation": "Speed is measured in metres per second.",
                    "options": [
                        {"option_text": "m/s", "is_correct": True, "position": 0},
                        {"option_text": "kg", "is_correct": False, "position": 1},
                    ],
                },
            )
            assert mcq.status_code == 201
            ids["mcq"] = mcq.json()["id"]
            assert mcq.json()["options"][0]["is_correct"] is True

            short_answer = client.post(
                f"/admin/lessons/{ids['lesson']}/questions",
                json={
                    "topic_id": ids["child"],
                    "question_text": "Complete: metres per ___.",
                    "question_type": "SHORT_ANSWER",
                    "explanation": "The unit is metres per second.",
                    "accepted_answers": ["second", "seconds"],
                },
            )
            assert short_answer.status_code == 201
            ids["short"] = short_answer.json()["id"]

            updated = client.put(
                f"/admin/lessons/{ids['lesson']}/questions/{ids['mcq']}",
                json={
                    "topic_id": ids["child"],
                    "question_text": "Which is a unit of speed?",
                    "question_type": "TRUE_FALSE",
                    "explanation": "m/s is a unit of speed.",
                    "options": [
                        {"option_text": "True", "is_correct": True, "position": 0},
                        {"option_text": "False", "is_correct": False, "position": 1},
                    ],
                },
            )
            assert updated.status_code == 200
            assert updated.json()["question_type"] == "TRUE_FALSE"

            client.cookies.clear()
            registration = client.post(
                "/auth/register",
                json={
                    "name": "Phase Four Student",
                    "email": student_email,
                    "password": "student-password",
                },
            )
            assert registration.status_code == 201
            ids["student"] = registration.json()["id"]
            assert client.post(
                "/auth/login",
                json={"email": student_email, "password": "student-password"},
            ).status_code == 200

            practice = client.get(f"/lessons/{ids['lesson']}/practice")
            assert practice.status_code == 200
            assert practice.json()["summary"] == {
                "lesson_id": ids["lesson"],
                "correct_count": 0,
                "total_count": 0,
                "accuracy": 0.0,
            }
            for question in practice.json()["questions"]:
                assert "accepted_answers" not in question
                assert "explanation" not in question
                assert all("is_correct" not in option for option in question["options"])

            correct = client.post(
                f"/practice/{ids['mcq']}/answer", json={"answer": " true "}
            )
            assert correct.status_code == 200
            assert correct.json()["is_correct"] is True
            incorrect = client.post(
                f"/practice/{ids['short']}/answer", json={"answer": "minute"}
            )
            assert incorrect.status_code == 200
            assert incorrect.json()["is_correct"] is False
            assert incorrect.json()["correct_answer"] == "second"

            summary = client.get(f"/lessons/{ids['lesson']}/practice").json()[
                "summary"
            ]
            assert summary["correct_count"] == 1
            assert summary["total_count"] == 2
            assert summary["accuracy"] == 50.0

            adaptive = client.get(f"/lessons/{ids['lesson']}/practice/next")
            assert adaptive.status_code == 200
            assert adaptive.json()["mastery_percentage"] == 50.0
            assert adaptive.json()["mastery_label"] == "INTERMEDIATE"
            assert adaptive.json()["target_difficulty"] == 60.0
            assert "explanation" not in adaptive.json()["question"]
            assert all(
                "is_correct" not in option
                for option in adaptive.json()["question"]["options"]
            )

            progress = client.get("/progress")
            assert progress.status_code == 200
            assert progress.json()["overall_score"] == 50.0
            assert progress.json()["topic_accuracy"][0]["attempt_count"] == 2
            assert progress.json()["mastery"][0]["mastery_label"] == "INTERMEDIATE"
            assert progress.json()["weak_topics"][0]["accuracy"] == 50.0
            assert progress.json()["study_plan_preview"] == []
            assert client.get("/admin/students").status_code == 403

            client.cookies.clear()
            client.cookies.set(settings.session_cookie_name, admin_session)
            students = client.get("/admin/students")
            assert students.status_code == 200
            assert any(student["id"] == ids["student"] for student in students.json())
            student_progress = client.get(
                f"/admin/students/{ids['student']}/progress"
            )
            assert student_progress.status_code == 200
            assert student_progress.json()["student"]["id"] == ids["student"]
            assert student_progress.json()["progress"]["overall_score"] == 50.0
            course = student_progress.json()["progress"]["course_progress"]
            assert any(item["lesson_id"] == ids["lesson"] for item in course)
            assert client.delete(
                f"/admin/lessons/{ids['lesson']}/questions/{ids['short']}"
            ).status_code == 204
            ids.pop("short")
    finally:
        with psycopg.connect(settings.database_url) as connection:
            if "lesson" in ids:
                connection.execute("DELETE FROM lessons WHERE id = %s", (ids["lesson"],))
            if "child" in ids:
                connection.execute("DELETE FROM topics WHERE id = %s", (ids["child"],))
            if "parent" in ids:
                connection.execute("DELETE FROM topics WHERE id = %s", (ids["parent"],))
            for key in ("student", "admin"):
                if key in ids:
                    connection.execute("DELETE FROM users WHERE id = %s", (ids[key],))
