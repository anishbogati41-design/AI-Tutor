from __future__ import annotations

from fastapi import Depends, HTTPException, Request, status

from backend.config import Settings, get_settings
from backend.database.connection import Database
from backend.redis_store.client import RedisStore
from backend.users.models import UserRecord
from backend.users.repository import UserRepository


def get_database(request: Request) -> Database:
    return request.app.state.database


def get_redis_store(request: Request) -> RedisStore:
    return request.app.state.redis_store


async def get_current_user(
    request: Request,
    settings: Settings = Depends(get_settings),
    database: Database = Depends(get_database),
    redis_store: RedisStore = Depends(get_redis_store),
) -> UserRecord:
    session_id = request.cookies.get(settings.session_cookie_name)
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    session = await redis_store.get_session(session_id)
    if session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session is invalid or expired",
        )

    user = await UserRepository(database).get_by_id(int(session["user_id"]))
    if user is None:
        await redis_store.delete_session(session_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session user no longer exists",
        )
    return user


async def require_admin(
    current_user: UserRecord = Depends(get_current_user),
) -> UserRecord:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator access required",
        )
    return current_user
