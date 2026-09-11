from fastapi import APIRouter, Depends, HTTPException, status

from backend.auth.dependencies import get_current_user, get_database
from backend.database.connection import Database
from backend.users.models import UserRecord
from backend.users.repository import EmailAlreadyExistsError, UserRepository
from backend.users.schemas import (
    AccessibilityPreferences,
    UserProfileUpdate,
    UserResponse,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserResponse)
async def get_profile(
    current_user: UserRecord = Depends(get_current_user),
) -> UserRecord:
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_profile(
    payload: UserProfileUpdate,
    current_user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> UserRecord:
    try:
        updated = await UserRepository(database).update_profile(
            current_user.id, payload.name, payload.email
        )
    except EmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with that email already exists",
        ) from exc
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated


@router.get("/me/preferences", response_model=AccessibilityPreferences)
async def get_preferences(
    current_user: UserRecord = Depends(get_current_user),
) -> AccessibilityPreferences:
    return AccessibilityPreferences.model_validate(current_user, from_attributes=True)


@router.put("/me/preferences", response_model=AccessibilityPreferences)
async def update_preferences(
    payload: AccessibilityPreferences,
    current_user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> AccessibilityPreferences:
    updated = await UserRepository(database).update_preferences(
        current_user.id,
        payload.font_size,
        payload.readable_mode,
        payload.high_contrast,
        payload.dyslexia_mode,
    )
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return AccessibilityPreferences.model_validate(updated, from_attributes=True)
