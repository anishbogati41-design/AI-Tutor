from __future__ import annotations

import secrets

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from starlette.concurrency import run_in_threadpool

from backend.auth.dependencies import (
    get_current_user,
    get_database,
    get_redis_store,
)
from backend.auth.passwords import DUMMY_PASSWORD_HASH, hash_password, verify_password
from backend.auth.schemas import LoginRequest, RegisterRequest
from backend.config import Settings, get_settings
from backend.database.connection import Database
from backend.redis_store.client import RedisStore
from backend.users.models import UserRecord
from backend.users.repository import EmailAlreadyExistsError, UserRepository
from backend.users.schemas import UserResponse

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: RegisterRequest,
    database: Database = Depends(get_database),
) -> UserRecord:
    password_hash = await run_in_threadpool(hash_password, payload.password)
    try:
        return await UserRepository(database).create(
            payload.name, payload.email, password_hash
        )
    except EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with that email already exists",
        ) from exc


@router.post("/login", response_model=UserResponse)
async def login(
    payload: LoginRequest,
    response: Response,
    database: Database = Depends(get_database),
    redis_store: RedisStore = Depends(get_redis_store),
    settings: Settings = Depends(get_settings),
) -> UserRecord:
    user = await UserRepository(database).get_by_email(payload.email)
    password_valid = await run_in_threadpool(
        verify_password,
        payload.password,
        user.password_hash if user is not None else DUMMY_PASSWORD_HASH,
    )
    if user is None or not password_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    session_id = secrets.token_urlsafe(32)
    await redis_store.set_session(
        session_id,
        user.id,
        user.is_admin,
        settings.session_ttl_seconds,
    )
    response.set_cookie(
        key=settings.session_cookie_name,
        value=session_id,
        max_age=settings.session_ttl_seconds,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="strict",
        path="/",
    )
    return user


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def logout(
    request: Request,
    response: Response,
    current_user: UserRecord = Depends(get_current_user),
    redis_store: RedisStore = Depends(get_redis_store),
    settings: Settings = Depends(get_settings),
) -> Response:
    del current_user
    session_id = request.cookies[settings.session_cookie_name]
    await redis_store.delete_session(session_id)
    response.delete_cookie(
        key=settings.session_cookie_name,
        httponly=True,
        secure=settings.cookie_secure,
        samesite="strict",
        path="/",
    )
    response.status_code = status.HTTP_204_NO_CONTENT
    return response


@router.get("/me", response_model=UserResponse)
async def authenticated_user(
    current_user: UserRecord = Depends(get_current_user),
) -> UserRecord:
    return current_user
