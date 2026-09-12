from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class QuestionType(StrEnum):
    MCQ = "MCQ"
    TRUE_FALSE = "TRUE_FALSE"
    SHORT_ANSWER = "SHORT_ANSWER"


class QuestionOptionWriteRequest(BaseModel):
    option_text: str
    is_correct: bool = False
    position: int = Field(ge=0)

    @field_validator("option_text")
    @classmethod
    def validate_option_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized or len(normalized) > 1000:
            raise ValueError("option_text must contain 1 to 1000 characters")
        return normalized


class QuestionWriteRequest(BaseModel):
    topic_id: int = Field(gt=0)
    question_text: str
    question_type: QuestionType
    difficulty_score: float = Field(default=0, ge=0, le=100)
    explanation: str = ""
    accepted_answers: list[str] = Field(default_factory=list)
    options: list[QuestionOptionWriteRequest] = Field(default_factory=list)

    @field_validator("question_text")
    @classmethod
    def validate_question_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized or len(normalized) > 10000:
            raise ValueError("question_text must contain 1 to 10000 characters")
        return normalized

    @field_validator("explanation")
    @classmethod
    def validate_explanation(cls, value: str) -> str:
        normalized = value.strip()
        if len(normalized) > 20000:
            raise ValueError("explanation must be at most 20000 characters")
        return normalized

    @field_validator("accepted_answers")
    @classmethod
    def normalize_answers(cls, values: list[str]) -> list[str]:
        normalized = [" ".join(value.split()) for value in values]
        if any(not value or len(value) > 1000 for value in normalized):
            raise ValueError("accepted answers must contain 1 to 1000 characters")
        return normalized

    @model_validator(mode="after")
    def validate_type_fields(self) -> "QuestionWriteRequest":
        positions = sorted(option.position for option in self.options)
        option_keys = [option.option_text.casefold() for option in self.options]
        correct_count = sum(option.is_correct for option in self.options)

        if positions != list(range(len(positions))):
            raise ValueError("option positions must be unique and contiguous from zero")
        if len(set(option_keys)) != len(option_keys):
            raise ValueError("option text must be unique")

        if self.question_type is QuestionType.MCQ:
            if len(self.options) < 2 or correct_count != 1 or self.accepted_answers:
                raise ValueError(
                    "MCQ requires at least two options, exactly one correct option, and no accepted_answers"
                )
        elif self.question_type is QuestionType.TRUE_FALSE:
            if (
                len(self.options) != 2
                or set(option_keys) != {"true", "false"}
                or correct_count != 1
                or self.accepted_answers
            ):
                raise ValueError(
                    "TRUE_FALSE requires True and False options, exactly one correct option, and no accepted_answers"
                )
        elif self.options or not self.accepted_answers:
            raise ValueError(
                "SHORT_ANSWER requires accepted_answers and does not accept options"
            )

        answer_keys = [answer.casefold() for answer in self.accepted_answers]
        if len(set(answer_keys)) != len(answer_keys):
            raise ValueError("accepted answers must be unique")
        return self


class QuestionOptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    option_text: str
    position: int
    is_correct: bool | None = None


class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    lesson_id: int
    topic_id: int
    question_text: str
    question_type: QuestionType
    difficulty_score: float
    explanation: str | None = None
    accepted_answers: tuple[str, ...] | None = None
    options: tuple[QuestionOptionResponse, ...]


class PracticeSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    lesson_id: int
    correct_count: int
    total_count: int
    accuracy: float


class PracticeSessionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    lesson_id: int
    lesson_title: str
    summary: PracticeSummaryResponse
    questions: tuple[QuestionResponse, ...]


class AnswerRequest(BaseModel):
    answer: str

    @field_validator("answer")
    @classmethod
    def validate_answer(cls, value: str) -> str:
        normalized = " ".join(value.split())
        if not normalized or len(normalized) > 5000:
            raise ValueError("answer must contain 1 to 5000 characters")
        return normalized


class AnswerResponse(BaseModel):
    is_correct: bool
    correct_answer: str
    explanation: str
