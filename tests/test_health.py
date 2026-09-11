from fastapi.testclient import TestClient

from backend.main import app


class HealthyDependency:
    async def is_healthy(self) -> bool:
        return True


class UnhealthyDependency:
    async def is_healthy(self) -> bool:
        return False


def test_liveness_does_not_require_dependencies() -> None:
    client = TestClient(app)
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readiness_reports_dependency_failure() -> None:
    app.state.database = HealthyDependency()
    app.state.redis_store = UnhealthyDependency()

    client = TestClient(app)
    response = client.get("/health/ready")

    assert response.status_code == 503
    assert response.json() == {
        "status": "unavailable",
        "checks": {"postgres": True, "redis": False},
    }
