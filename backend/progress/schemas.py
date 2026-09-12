from pydantic import BaseModel


class TopicAccuracyResponse(BaseModel):
    topic_id: int
    topic_name: str
    accuracy: float
    correct_count: int
    attempt_count: int


class MasteryResponse(BaseModel):
    topic_id: int
    topic_name: str
    mastery_percentage: float
    mastery_label: str


class WeakTopicResponse(BaseModel):
    topic_id: int
    topic_name: str
    accuracy: float
    attempt_count: int
    average_difficulty: float


class StudyPlanPreviewItem(BaseModel):
    id: int
    title: str
    scheduled_date: str
    completed: bool


class CourseProgressResponse(BaseModel):
    lesson_id: int
    lesson_title: str
    topic_name: str
    correct_count: int
    attempt_count: int
    accuracy: float
    progress_percentage: float
    status: str


class ProgressResponse(BaseModel):
    overall_score: float
    topic_accuracy: list[TopicAccuracyResponse]
    mastery: list[MasteryResponse]
    weak_topics: list[WeakTopicResponse]
    recent_improvement: float
    study_plan_preview: list[StudyPlanPreviewItem]
    course_progress: list[CourseProgressResponse]


class AdminStudentResponse(BaseModel):
    id: int
    name: str
    email: str


class AdminStudentProgressResponse(BaseModel):
    student: AdminStudentResponse
    progress: ProgressResponse
