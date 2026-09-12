from fastapi import APIRouter

from backend.lessons.admin_router import router as lessons_router
from backend.questions.admin_router import router as questions_router
from backend.topics.admin_router import router as topics_router

router = APIRouter(prefix="/admin")
router.include_router(lessons_router)
router.include_router(topics_router)
router.include_router(questions_router)
