"use client";

import { useParams } from "next/navigation";

import { QuestionManager } from "@/components/admin/question-manager";

export default function LessonQuestionManagerPage() {
  const parameters = useParams<{ id: string }>();
  return <QuestionManager fixedLessonId={parameters.id} />;
}
