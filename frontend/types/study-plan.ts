export type StudyPlanItem = {
  id: number;
  study_plan_id: number;
  title: string;
  description: string;
  scheduled_date: string;
  position: number;
  completed: boolean;
};

export type StudyPlan = {
  id: number;
  user_id: number;
  items: StudyPlanItem[];
};
