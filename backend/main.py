from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware

from backend.admin.router import router as admin_router
from backend.auth.router import router as auth_router
from backend.config import get_settings
from backend.database.connection import Database
from backend.logging.config import configure_logging
from backend.lessons.router import router as lessons_router
from backend.questions.router import router as questions_router
from backend.redis_store.client import RedisStore
from backend.topics.router import router as topics_router
from backend.users.router import router as users_router


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
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type"],
)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(topics_router)
app.include_router(lessons_router)
app.include_router(questions_router)
app.include_router(admin_router)


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
