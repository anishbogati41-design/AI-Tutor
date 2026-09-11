from fastapi import APIRouter

from backend.lessons.admin_router import router as lessons_router
from backend.topics.admin_router import router as topics_router

router = APIRouter(prefix="/admin")
router.include_router(lessons_router)
router.include_router(topics_router)
