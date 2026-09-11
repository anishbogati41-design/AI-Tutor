from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request, Response, status

from backend.config import get_settings
from backend.database.connection import Database
from backend.logging.config import configure_logging
from backend.redis_store.client import RedisStore


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)

    database = Database(settings.database_url)
    redis_store = RedisStore(settings.redis_url)
    await database.open()
    await redis_store.open()
    app.state.database = database
    app.state.redis_store = redis_store

    try:
        yield
    finally:
        await redis_store.close()
        await database.close()


app = FastAPI(
    title="Adaptive Education API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health/live", tags=["health"])
async def liveness() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/ready", tags=["health"])
async def readiness(request: Request, response: Response) -> dict[str, object]:
    checks = {
        "postgres": await request.app.state.database.is_healthy(),
        "redis": await request.app.state.redis_store.is_healthy(),
    }
    ready = all(checks.values())
    if not ready:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return {"status": "ready" if ready else "unavailable", "checks": checks}
