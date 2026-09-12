export type TopicAccuracy = {
  topic_id: number;
  topic_name: string;
  accuracy: number;
  correct_count: number;
  attempt_count: number;
};

export type Mastery = {
  topic_id: number;
  topic_name: string;
  mastery_percentage: number;
  mastery_label: string;
};

export type WeakTopic = {
  topic_id: number;
  topic_name: string;
  accuracy: number;
  attempt_count: number;
  average_difficulty: number;
};

export type Progress = {
  overall_score: number;
  topic_accuracy: TopicAccuracy[];
  mastery: Mastery[];
  weak_topics: WeakTopic[];
  recent_improvement: number;
  study_plan_preview: Array<{ id: number; title: string; scheduled_date: string; completed: boolean }>;
  course_progress: Array<{
    lesson_id: number;
    lesson_title: string;
    topic_name: string;
    correct_count: number;
    attempt_count: number;
    accuracy: number;
    progress_percentage: number;
    status: "NOT_STARTED" | "IN_PROGRESS" | "COMPLETED";
  }>;
};

export type AdminStudent = { id: number; name: string; email: string };

export type AdminStudentProgress = {
  student: AdminStudent;
  progress: Progress;
};
