from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from redis.asyncio import Redis

logger = logging.getLogger(__name__)


class RedisStore:
    def __init__(self, redis_url: str) -> None:
        self._client = Redis.from_url(redis_url, decode_responses=True)

    async def open(self) -> None:
        await self._client.ping()
        logger.info("Redis connection is ready")

    async def close(self) -> None:
        await self._client.aclose()

    async def is_healthy(self) -> bool:
        try:
            return bool(await self._client.ping())
        except Exception:
            logger.exception("Redis health check failed")
            return False

    async def set_session(
        self, session_id: str, user_id: int, is_admin: bool, ttl_seconds: int
    ) -> None:
        key = f"session:{session_id}"
        async with self._client.pipeline(transaction=True) as pipeline:
            pipeline.hset(
                key,
                mapping={"user_id": str(user_id), "is_admin": "1" if is_admin else "0"},
            )
            pipeline.expire(key, ttl_seconds)
            await pipeline.execute()

    async def get_session(self, session_id: str) -> dict[str, object] | None:
        value = await self._client.hgetall(f"session:{session_id}")
        if not value:
            return None
        return {
            "user_id": int(value["user_id"]),
            "is_admin": value["is_admin"] == "1",
        }

    async def delete_session(self, session_id: str) -> None:
        await self._client.delete(f"session:{session_id}")

    async def increment_ai_rate(self, user_id: int, window_seconds: int) -> int:
        return await self._increment_with_expiry(
            f"ai_rate:{user_id}", window_seconds
        )

    async def increment_ai_daily(self, user_id: int) -> int:
        now = datetime.now(timezone.utc)
        tomorrow = (now + timedelta(days=1)).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        ttl_seconds = max(1, int((tomorrow - now).total_seconds()))
        return await self._increment_with_expiry(f"ai_daily:{user_id}", ttl_seconds)

    async def _increment_with_expiry(self, key: str, ttl_seconds: int) -> int:
        count = int(await self._client.incr(key))
        if count == 1:
            await self._client.expire(key, ttl_seconds)
        return count
