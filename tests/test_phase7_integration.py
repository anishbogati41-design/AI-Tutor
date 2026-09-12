import os
import uuid
from collections.abc import AsyncIterator

import psycopg
import pytest
from fastapi.testclient import TestClient

from backend.ai_teacher.router import get_ai_provider
from backend.ai_teacher.provider import AIProviderError
from backend.config import get_settings
from backend.main import app


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="set RUN_INTEGRATION_TESTS=1 with PostgreSQL and Redis available",
)


class FakeAIProvider:
    def __init__(self) -> None:
        self.inputs: list[str] = []

    async def stream(
        self, *, instructions: str, input_text: str
    ) -> AsyncIterator[str]:
        self.inputs.append(input_text)
        yield "A clear "
        yield "educational answer."

    async def complete(self, *, instructions: str, input_text: str) -> str:
        self.inputs.append(input_text)
        return "Start with the key idea, then work through each step."


class FailingAIProvider(FakeAIProvider):
    async def stream(
        self, *, instructions: str, input_text: str
    ) -> AsyncIterator[str]:
        raise AIProviderError("simulated failure")
        yield ""


def test_owned_conversations_streaming_chat_and_practice_help() -> None:
    settings = get_settings()
    suffix = uuid.uuid4().hex
    email = f"phase7-{suffix}@example.test"
    second_email = f"phase7-other-{suffix}@example.test"
    ids: dict[str, int] = {}
    provider = FakeAIProvider()

    try:
        with psycopg.connect(settings.database_url) as connection:
            topic = connection.execute(
                "INSERT INTO topics (name) VALUES (%s) RETURNING id",
                (f"Phase 7 topic {suffix}",),
            ).fetchone()
            ids["topic"] = topic[0]
            subtopic = connection.execute(
                "INSERT INTO topics (name, parent_topic_id) VALUES (%s, %s) RETURNING id",
                (f"Phase 7 subtopic {suffix}", ids["topic"]),
            ).fetchone()
            ids["subtopic"] = subtopic[0]
            lesson = connection.execute(
                """
                INSERT INTO lessons (
                    title, description, subtopic_id, estimated_minutes, is_published
                ) VALUES (%s, %s, %s, 10, TRUE) RETURNING id
                """,
                ("Fractions", "Learn equivalent fractions.", ids["subtopic"]),
            ).fetchone()
            ids["lesson"] = lesson[0]
            connection.execute(
                """
                INSERT INTO lesson_sections (
                    lesson_id, section_type, title, content, position
                ) VALUES (%s, 'EXPLANATION', 'Equivalent fractions', %s, 0)
                """,
                (ids["lesson"], "Multiply numerator and denominator equally."),
            )
            question = connection.execute(
                """
                INSERT INTO questions (
                    lesson_id, topic_id, question_text, question_type,
                    difficulty_score, explanation
                ) VALUES (%s, %s, %s, 'SHORT_ANSWER', 30, %s) RETURNING id
                """,
                (
                    ids["lesson"],
                    ids["subtopic"],
                    "Give a fraction equivalent to one half.",
                    "Two fourths is equivalent to one half.",
                ),
            ).fetchone()
            ids["question"] = question[0]

        app.dependency_overrides[get_ai_provider] = lambda: provider
        with TestClient(app) as client:
            registration = client.post(
                "/auth/register",
                json={"name": "Phase Seven Student", "email": email, "password": "student-password"},
            )
            assert registration.status_code == 201
            ids["student"] = registration.json()["id"]
            assert client.post(
                "/auth/login", json={"email": email, "password": "student-password"}
            ).status_code == 200

            created = client.post("/conversations", json={"title": "Fractions help"})
            assert created.status_code == 201
            ids["conversation"] = created.json()["id"]
            unrelated = client.post("/conversations", json={"title": "Separate chat"})
            assert unrelated.status_code == 201
            ids["unrelated_conversation"] = unrelated.json()["id"]
            assert client.post(
                f"/conversations/{ids['unrelated_conversation']}/messages",
                json={"content": "This text must stay in its own conversation."},
            ).status_code == 201
            message = client.post(
                f"/conversations/{ids['conversation']}/messages",
                json={"content": "Why is two fourths equal to one half?"},
            )
            assert message.status_code == 201
            streamed = client.post(
                "/ai/chat",
                json={
                    "conversation_id": ids["conversation"],
                    "message": "Why is two fourths equal to one half?",
                    "explanation_style": "SIMPLE",
                },
            )
            assert streamed.status_code == 200
            assert streamed.headers["content-type"].startswith("text/event-stream")
            assert 'data: {"text": "A clear "}' in streamed.text
            assert "event: done" in streamed.text
            assert streamed.text.index("event: delta") < streamed.text.index("event: done")

            detail = client.get(f"/conversations/{ids['conversation']}")
            assert detail.status_code == 200
            assert [item["role"] for item in detail.json()["messages"]] == [
                "USER", "ASSISTANT"
            ]
            assert detail.json()["messages"][-1]["content"] == (
                "A clear educational answer."
            )
            assert len(client.get("/conversations").json()) == 2
            assert provider.inputs[0] == (
                "User: Why is two fourths equal to one half?"
            )
            assert "must stay" not in provider.inputs[0]

            assert client.post(
                f"/conversations/{ids['conversation']}/messages",
                json={"content": "Explain that another way."},
            ).status_code == 201
            app.dependency_overrides[get_ai_provider] = lambda: FailingAIProvider()
            failed_stream = client.post(
                "/ai/chat",
                json={
                    "conversation_id": ids["conversation"],
                    "message": "Explain that another way.",
                },
            )
            assert "event: error" in failed_stream.text
            assert len(client.get(f"/conversations/{ids['conversation']}").json()["messages"]) == 3
            app.dependency_overrides[get_ai_provider] = lambda: provider

            with psycopg.connect(settings.database_url) as connection:
                before = connection.execute(
                    "SELECT COUNT(*) FROM questions WHERE lesson_id = %s",
                    (ids["lesson"],),
                ).fetchone()[0]
            help_response = client.post(
                f"/lessons/{ids['lesson']}/ai-practice",
                json={
                    "question_id": ids["question"],
                    "prompt": "Give me a hint.",
                    "explanation_style": "STEP_BY_STEP",
                },
            )
            assert help_response.status_code == 200
            assert "key idea" in help_response.json()["response"]
            with psycopg.connect(settings.database_url) as connection:
                after = connection.execute(
                    "SELECT COUNT(*) FROM questions WHERE lesson_id = %s",
                    (ids["lesson"],),
                ).fetchone()[0]
            assert after == before

            client.cookies.clear()
            registration = client.post(
                "/auth/register",
                json={"name": "Other Student", "email": second_email, "password": "student-password"},
            )
            assert registration.status_code == 201
            ids["other_student"] = registration.json()["id"]
            assert client.post(
                "/auth/login",
                json={"email": second_email, "password": "student-password"},
            ).status_code == 200
            assert client.get(f"/conversations/{ids['conversation']}").status_code == 404
            assert client.delete(f"/conversations/{ids['conversation']}").status_code == 404

            client.cookies.clear()
            assert client.post(
                "/auth/login", json={"email": email, "password": "student-password"}
            ).status_code == 200
            assert client.delete(f"/conversations/{ids['conversation']}").status_code == 204
            assert client.get(f"/conversations/{ids['conversation']}").status_code == 404
    finally:
        app.dependency_overrides.pop(get_ai_provider, None)
        with psycopg.connect(settings.database_url) as connection:
            if "lesson" in ids:
                connection.execute("DELETE FROM lessons WHERE id = %s", (ids["lesson"],))
            if "subtopic" in ids:
                connection.execute("DELETE FROM topics WHERE id = %s", (ids["subtopic"],))
            if "topic" in ids:
                connection.execute("DELETE FROM topics WHERE id = %s", (ids["topic"],))
            for key in ("student", "other_student"):
                if key in ids:
                    connection.execute("DELETE FROM users WHERE id = %s", (ids[key],))
