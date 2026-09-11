import asyncio
import os

import pytest

from backend.config import get_settings
from backend.database.connection import Database
from backend.redis_store.client import RedisStore


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_INTEGRATION_TESTS") != "1",
    reason="set RUN_INTEGRATION_TESTS=1 with PostgreSQL and Redis available",
)


def test_postgres_and_approved_redis_operations() -> None:
    async def scenario() -> None:
        settings = get_settings()
        database = Database(settings.database_url)
        redis_store = RedisStore(settings.redis_url)

        await database.open()
        await redis_store.open()
        try:
            assert await database.is_healthy() is True

            await redis_store.set_session("phase1-check", 42, True, 30)
            assert await redis_store.get_session("phase1-check") == {
                "user_id": 42,
                "is_admin": True,
            }
            assert await redis_store.increment_ai_rate(42, 30) >= 1
            assert await redis_store.increment_ai_daily(42) >= 1
            await redis_store.delete_session("phase1-check")
            assert await redis_store.get_session("phase1-check") is None
        finally:
            await redis_store.close()
            await database.close()

    asyncio.run(scenario())
