from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class QuestionOptionRecord:
    id: int
    question_id: int
    option_text: str
    is_correct: bool
    position: int


@dataclass(frozen=True, slots=True)
class QuestionRecord:
    id: int
    lesson_id: int
    topic_id: int
    question_text: str
    question_type: str
    difficulty_score: float
    explanation: str
    accepted_answers: tuple[str, ...]
    options: tuple[QuestionOptionRecord, ...]


@dataclass(frozen=True, slots=True)
class PracticeSummaryRecord:
    lesson_id: int
    correct_count: int
    total_count: int

    @property
    def accuracy(self) -> float:
        if self.total_count == 0:
            return 0.0
        return round(self.correct_count / self.total_count * 100, 2)


@dataclass(frozen=True, slots=True)
class PracticeSessionRecord:
    lesson_id: int
    lesson_title: str
    summary: PracticeSummaryRecord
    questions: tuple[QuestionRecord, ...]
