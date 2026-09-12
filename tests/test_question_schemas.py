import pytest
from pydantic import ValidationError

from backend.questions.schemas import QuestionWriteRequest


def test_mcq_requires_one_correct_option_and_contiguous_positions() -> None:
    with pytest.raises(ValidationError, match="exactly one correct option"):
        QuestionWriteRequest(
            topic_id=1,
            question_text="Choose one",
            question_type="MCQ",
            options=[
                {"option_text": "A", "is_correct": False, "position": 0},
                {"option_text": "B", "is_correct": False, "position": 1},
            ],
        )


def test_true_false_requires_the_two_canonical_options() -> None:
    question = QuestionWriteRequest(
        topic_id=1,
        question_text="The statement is true.",
        question_type="TRUE_FALSE",
        options=[
            {"option_text": "True", "is_correct": True, "position": 0},
            {"option_text": "False", "is_correct": False, "position": 1},
        ],
    )

    assert [option.option_text for option in question.options] == ["True", "False"]


def test_short_answer_requires_unique_answers_and_no_options() -> None:
    with pytest.raises(ValidationError, match="accepted answers must be unique"):
        QuestionWriteRequest(
            topic_id=1,
            question_text="Write the number.",
            question_type="SHORT_ANSWER",
            accepted_answers=["Three", " three "],
        )

    question = QuestionWriteRequest(
        topic_id=1,
        question_text="Write the number.",
        question_type="SHORT_ANSWER",
        accepted_answers=["3", "three"],
    )
    assert question.accepted_answers == ["3", "three"]
