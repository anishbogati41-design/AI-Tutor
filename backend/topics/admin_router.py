from fastapi import APIRouter, Depends, HTTPException, Response, status

from backend.auth.dependencies import get_database, require_admin
from backend.database.connection import Database
from backend.topics.models import TopicRecord
from backend.topics.repository import TopicInUseError, TopicRepository
from backend.topics.schemas import TopicResponse, TopicWriteRequest
from backend.topics.service import (
    InvalidTopicParentError,
    TopicNotFoundError,
    TopicService,
)
from backend.users.models import UserRecord

router = APIRouter(prefix="/topics", tags=["administrator content"])


@router.post("", response_model=TopicResponse, status_code=status.HTTP_201_CREATED)
async def create_topic(
    payload: TopicWriteRequest,
    admin: UserRecord = Depends(require_admin),
    database: Database = Depends(get_database),
) -> TopicRecord:
    del admin
    try:
        return await TopicService(TopicRepository(database)).create(payload)
    except InvalidTopicParentError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Parent topic does not exist",
        ) from exc


@router.put("/{topic_id}", response_model=TopicResponse)
async def update_topic(
    topic_id: int,
    payload: TopicWriteRequest,
    admin: UserRecord = Depends(require_admin),
    database: Database = Depends(get_database),
) -> TopicRecord:
    del admin
    try:
        return await TopicService(TopicRepository(database)).update(topic_id, payload)
    except TopicNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found") from exc
    except InvalidTopicParentError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Parent topic is invalid or would create a cycle",
        ) from exc


@router.delete(
    "/{topic_id}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response
)
async def delete_topic(
    topic_id: int,
    admin: UserRecord = Depends(require_admin),
    database: Database = Depends(get_database),
) -> Response:
    del admin
    try:
        deleted = await TopicRepository(database).delete(topic_id)
    except TopicInUseError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Topic is still referenced by a subtopic, lesson, or learning record",
        ) from exc
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
