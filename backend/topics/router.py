from fastapi import APIRouter, Depends, HTTPException, status

from backend.auth.dependencies import get_current_user, get_database
from backend.database.connection import Database
from backend.topics.models import TopicRecord
from backend.topics.repository import TopicRepository
from backend.topics.schemas import TopicResponse
from backend.users.models import UserRecord

router = APIRouter(prefix="/topics", tags=["topics"])


@router.get("", response_model=list[TopicResponse])
async def list_topics(
    current_user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> list[TopicRecord]:
    del current_user
    return await TopicRepository(database).list_all()


@router.get("/{topic_id}", response_model=TopicResponse)
async def get_topic(
    topic_id: int,
    current_user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> TopicRecord:
    del current_user
    topic = await TopicRepository(database).get_by_id(topic_id)
    if topic is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return topic


@router.get("/{topic_id}/subtopics", response_model=list[TopicResponse])
async def list_subtopics(
    topic_id: int,
    current_user: UserRecord = Depends(get_current_user),
    database: Database = Depends(get_database),
) -> list[TopicRecord]:
    del current_user
    repository = TopicRepository(database)
    if await repository.get_by_id(topic_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Topic not found")
    return await repository.list_children(topic_id)
