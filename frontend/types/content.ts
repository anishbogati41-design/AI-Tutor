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
