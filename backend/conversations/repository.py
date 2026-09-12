from __future__ import annotations

from typing import Any

from backend.conversations.models import ConversationRecord, MessageRecord
from backend.database.connection import Database


class ConversationRepository:
    def __init__(self, database: Database) -> None:
        self._database = database

    async def create(self, user_id: int, title: str) -> ConversationRecord:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                INSERT INTO conversations (user_id, title)
                VALUES (%s, %s)
                RETURNING id, user_id, title, created_at, updated_at
                """,
                (user_id, title),
            )
            row = await cursor.fetchone()
        if row is None:
            raise RuntimeError("conversation insert did not return a row")
        return self._conversation(row)

    async def list_owned(self, user_id: int) -> list[ConversationRecord]:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                SELECT id, user_id, title, created_at, updated_at
                FROM conversations WHERE user_id = %s
                ORDER BY updated_at DESC, id DESC
                """,
                (user_id,),
            )
            rows = await cursor.fetchall()
        return [self._conversation(row) for row in rows]

    async def get_owned(
        self, conversation_id: int, user_id: int
    ) -> ConversationRecord | None:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                """
                SELECT id, user_id, title, created_at, updated_at
                FROM conversations WHERE id = %s AND user_id = %s
                """,
                (conversation_id, user_id),
            )
            row = await cursor.fetchone()
            if row is None:
                return None
            message_cursor = await connection.execute(
                """
                SELECT id, conversation_id, role, content, created_at
                FROM messages WHERE conversation_id = %s
                ORDER BY created_at, id
                """,
                (conversation_id,),
            )
            messages = tuple(
                self._message(message) for message in await message_cursor.fetchall()
            )
        return ConversationRecord(*row, messages=messages)

    async def add_message(
        self, conversation_id: int, user_id: int, role: str, content: str
    ) -> MessageRecord | None:
        async with self._database.connection() as connection:
            owner_cursor = await connection.execute(
                "SELECT 1 FROM conversations WHERE id = %s AND user_id = %s",
                (conversation_id, user_id),
            )
            if await owner_cursor.fetchone() is None:
                return None
            cursor = await connection.execute(
                """
                INSERT INTO messages (conversation_id, role, content)
                VALUES (%s, %s, %s)
                RETURNING id, conversation_id, role, content, created_at
                """,
                (conversation_id, role, content),
            )
            row = await cursor.fetchone()
            await connection.execute(
                "UPDATE conversations SET updated_at = CURRENT_TIMESTAMP WHERE id = %s",
                (conversation_id,),
            )
        if row is None:
            raise RuntimeError("message insert did not return a row")
        return self._message(row)

    async def delete_owned(self, conversation_id: int, user_id: int) -> bool:
        async with self._database.connection() as connection:
            cursor = await connection.execute(
                "DELETE FROM conversations WHERE id = %s AND user_id = %s",
                (conversation_id, user_id),
            )
            return cursor.rowcount > 0

    @staticmethod
    def _conversation(row: tuple[Any, ...]) -> ConversationRecord:
        return ConversationRecord(
            id=row[0], user_id=row[1], title=row[2],
            created_at=row[3], updated_at=row[4],
        )

    @staticmethod
    def _message(row: tuple[Any, ...]) -> MessageRecord:
        return MessageRecord(
            id=row[0], conversation_id=row[1], role=row[2],
            content=row[3], created_at=row[4],
        )
