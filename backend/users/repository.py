from __future__ import annotations

from typing import Any

from psycopg.errors import UniqueViolation
from backend.database.connection import Database
from backend.users.models import UserRecord


class EmailAlreadyExistsError(Exception):
    pass


class UserRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    async def create(self, name: str, email: str, password_hash: str) -> UserRecord:
        try:
            async with self._database.connection() as connection:
                cursor = await connection.execute(
                    """
                    INSERT INTO users (name, email, password_hash)
                    VALUES (%s, %s, %s)
                    RETURNING id, name, email, password_hash, is_admin,
                              font_size, readable_mode, high_contrast, dyslexia_mode
                    """,
                    (name, email, password_hash),
                )
                row = await cursor.fetchone()
        except UniqueViolation as exc:
            raise EmailAlreadyExistsError from exc

        if row is None:
            raise RuntimeError("user insert did not return a row")
        return self._record(row)

    async def get_by_id(self, user_id: int) -> UserRecord | None:
        return await self._fetch_one("WHERE id = %s", (user_id,))

    async def get_by_email(self, email: str) -> UserRecord | None:
        return await self._fetch_one("WHERE email = %s", (email,))

    async def update_profile(
        self, user_id: int, name: str, email: str
    ) -> UserRecord | None:
        try:
            async with self._database.connection() as connection:
                cursor = await connection.execute(
                    """
                    UPDATE users
                    SET name = %s, email = %s
                    WHERE id = %s
                    RETURNING id, name, email, password_hash, is_admin,
                              font_size, readable_mode, high_contrast, dyslexia_mode
                    """,
                    (name, email, user_id),
                )
                row = await cursor.fetchone()
        except UniqueViolation as exc:
            raise EmailAlreadyExistsError from exc

        return self._record(row) if row is not None else None

    async def update_preferences(
        self,
        user_id: int,
        font_size: str,
        readable_mode: bool,
        high_contrast: bool,
        dyslexia_mode: bool,
    ) -> UserRecord | None:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                UPDATE users
                SET font_size = %s,
                    readable_mode = %s,
                    high_contrast = %s,
                    dyslexia_mode = %s
                WHERE id = %s
                RETURNING id, name, email, password_hash, is_admin,
                          font_size, readable_mode, high_contrast, dyslexia_mode
                """,
                (
                    font_size,
                    readable_mode,
                    high_contrast,
                    dyslexia_mode,
                    user_id,
                ),
            )
            row = await cursor.fetchone()
        return self._record(row) if row is not None else None

    async def _fetch_one(
        self, where_clause: str, parameters: tuple[object, ...]
    ) -> UserRecord | None:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                f"""
                SELECT id, name, email, password_hash, is_admin,
                       font_size, readable_mode, high_contrast, dyslexia_mode
                FROM users
                {where_clause}
                """,
                parameters,
            )
            row = await cursor.fetchone()
        return self._record(row) if row is not None else None

    @staticmethod
    def _record(row: tuple[Any, ...]) -> UserRecord:
        return UserRecord(
            id=row[0],
            name=row[1],
            email=row[2],
            password_hash=row[3],
            is_admin=row[4],
            font_size=row[5],
            readable_mode=row[6],
            high_contrast=row[7],
            dyslexia_mode=row[8],
        )
