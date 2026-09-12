export type Topic = {
  id: number;
  name: string;
  parent_topic_id: number | null;
  description: string;
};

export type Lesson = {
  id: number;
  title: string;
  description: string;
  subtopic_id: number;
  estimated_minutes: number;
  is_published: boolean;
};

export type LessonSection = {
  id: number;
  lesson_id: number;
  section_type: "INTRODUCTION" | "EXPLANATION" | "EXAMPLE" | "SUMMARY";
  title: string;
  content: string;
  position: number;
};

export type LessonDetail = Lesson & {
  sections: LessonSection[];
};

export type QuestionType = "MCQ" | "TRUE_FALSE" | "SHORT_ANSWER";

export type QuestionOption = {
  id: number;
  question_id: number;
  option_text: string;
  position: number;
  is_correct?: boolean;
};

export type PracticeQuestion = {
  id: number;
  lesson_id: number;
  topic_id: number;
  question_text: string;
  question_type: QuestionType;
  difficulty_score: number;
  explanation?: string;
  accepted_answers?: string[];
  options: QuestionOption[];
};

export type PracticeSummary = {
  lesson_id: number;
  correct_count: number;
  total_count: number;
  accuracy: number;
};

export type PracticeSession = {
  lesson_id: number;
  lesson_title: string;
  summary: PracticeSummary;
  questions: PracticeQuestion[];
};

export type AnswerResult = {
  is_correct: boolean;
  correct_answer: string;
  explanation: string;
};

export type AdaptiveQuestion = {
  mastery_percentage: number;
  mastery_label: string;
  target_difficulty: number;
  question: PracticeQuestion;
};
