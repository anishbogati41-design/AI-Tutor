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


def test_registration_session_profile_preferences_and_logout() -> None:
    email = f"phase2-{uuid.uuid4().hex}@example.test"
    user_id: int | None = None

    try:
        with TestClient(app) as client:
            preflight = client.options(
                "/auth/login",
                headers={
                    "Origin": "http://localhost:3000",
                    "Access-Control-Request-Method": "POST",
                },
            )
            assert preflight.status_code == 200
            assert preflight.headers["access-control-allow-origin"] == (
                "http://localhost:3000"
            )
            assert preflight.headers["access-control-allow-credentials"] == "true"

            registration = client.post(
                "/auth/register",
                json={
                    "name": "Phase Two Student",
                    "email": email,
                    "password": "secure-test-password",
                },
            )
            assert registration.status_code == 201
            user_id = registration.json()["id"]
            assert registration.json()["email"] == email
            assert "password" not in registration.text

            duplicate = client.post(
                "/auth/register",
                json={
                    "name": "Duplicate",
                    "email": email.upper(),
                    "password": "secure-test-password",
                },
            )
            assert duplicate.status_code == 409

            rejected_login = client.post(
                "/auth/login",
                json={"email": email, "password": "incorrect-password"},
            )
            assert rejected_login.status_code == 401

            login = client.post(
                "/auth/login",
                json={"email": email, "password": "secure-test-password"},
            )
            assert login.status_code == 200
            set_cookie = login.headers["set-cookie"]
            assert "adaptive_session=" in set_cookie
            assert "HttpOnly" in set_cookie
            assert "SameSite=strict" in set_cookie

            identity = client.get("/auth/me")
            assert identity.status_code == 200
            assert identity.json()["id"] == user_id

            profile = client.put(
                "/users/me",
                json={"name": "Updated Student", "email": email},
            )
            assert profile.status_code == 200
            assert profile.json()["name"] == "Updated Student"

            preferences = client.put(
                "/users/me/preferences",
                json={
                    "font_size": "large",
                    "readable_mode": True,
                    "high_contrast": True,
                    "dyslexia_mode": False,
                },
            )
            assert preferences.status_code == 200
            assert preferences.json() == {
                "font_size": "large",
                "readable_mode": True,
                "high_contrast": True,
                "dyslexia_mode": False,
            }

            logout = client.post("/auth/logout")
            assert logout.status_code == 204
            assert client.get("/auth/me").status_code == 401
    finally:
        if user_id is not None:
            with psycopg.connect(get_settings().database_url) as connection:
                connection.execute("DELETE FROM users WHERE id = %s", (user_id,))
