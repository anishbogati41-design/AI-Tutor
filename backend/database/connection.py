from __future__ import annotations

import logging

from psycopg_pool import AsyncConnectionPool

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, database_url: str) -> None:
        self._pool = AsyncConnectionPool(
            conninfo=database_url,
            min_size=1,
            max_size=5,
            open=False,
        )

    async def open(self) -> None:
        await self._pool.open()
        await self._pool.wait()
        logger.info("PostgreSQL connection pool is ready")

    async def close(self) -> None:
        await self._pool.close()

    async def is_healthy(self) -> bool:
        try:
            async with self._pool.connection() as connection:
                await connection.execute("SELECT 1")
            return True
        except Exception:
            logger.exception("PostgreSQL health check failed")
            return False
