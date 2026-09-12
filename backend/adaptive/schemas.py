from pydantic import BaseModel

from backend.questions.schemas import QuestionResponse


class AdaptiveQuestionResponse(BaseModel):
    mastery_percentage: float
    mastery_label: str
    target_difficulty: float
    question: QuestionResponse
