"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ApiError, apiRequest } from "@/lib/api";
import type {
  Lesson,
  PracticeQuestion,
  PracticeSession,
  QuestionType,
  Topic,
} from "@/types/content";
import type { User } from "@/types/user";

type DraftOption = { option_text: string; is_correct: boolean };

const defaultOptions: DraftOption[] = [
  { option_text: "", is_correct: true },
  { option_text: "", is_correct: false },
];

export default function QuestionManagerPage() {
  const queryClient = useQueryClient();
  const [lessonId, setLessonId] = useState("");
  const [editingId, setEditingId] = useState<number | null>(null);
  const [topicId, setTopicId] = useState("");
  const [questionText, setQuestionText] = useState("");
  const [questionType, setQuestionType] = useState<QuestionType>("MCQ");
  const [difficulty, setDifficulty] = useState("0");
  const [explanation, setExplanation] = useState("");
  const [options, setOptions] = useState<DraftOption[]>(defaultOptions);
  const [acceptedAnswers, setAcceptedAnswers] = useState("");

  const currentUser = useQuery({
    queryKey: ["current-user"],
    queryFn: () => apiRequest<User>("/auth/me"),
  });
  const lessons = useQuery({
    queryKey: ["lessons", "admin-question-manager"],
    queryFn: () => apiRequest<Lesson[]>("/lessons"),
    enabled: currentUser.data?.is_admin === true,
  });
  const topics = useQuery({
    queryKey: ["topics"],
    queryFn: () => apiRequest<Topic[]>("/topics"),
    enabled: currentUser.data?.is_admin === true,
  });
  const practice = useQuery({
    queryKey: ["practice", lessonId, "admin"],
    queryFn: () => apiRequest<PracticeSession>(`/lessons/${lessonId}/practice`),
    enabled: Boolean(lessonId) && currentUser.data?.is_admin === true,
  });

  useEffect(() => {
    if (!lessonId && lessons.data?.length) setLessonId(String(lessons.data[0].id));
  }, [lessonId, lessons.data]);

  useEffect(() => {
    if (!editingId) {
      const lesson = lessons.data?.find((item) => item.id === Number(lessonId));
      if (lesson) setTopicId(String(lesson.subtopic_id));
    }
  }, [editingId, lessonId, lessons.data]);

  const resetForm = () => {
    const lesson = lessons.data?.find((item) => item.id === Number(lessonId));
    setEditingId(null);
    setTopicId(lesson ? String(lesson.subtopic_id) : "");
    setQuestionText("");
    setQuestionType("MCQ");
    setDifficulty("0");
    setExplanation("");
    setOptions(defaultOptions.map((option) => ({ ...option })));
    setAcceptedAnswers("");
    save.reset();
  };

  const save = useMutation({
    mutationFn: () => {
      const payload = {
        topic_id: Number(topicId),
        question_text: questionText,
        question_type: questionType,
        difficulty_score: Number(difficulty),
        explanation,
        accepted_answers:
          questionType === "SHORT_ANSWER"
            ? acceptedAnswers.split(",").map((answer) => answer.trim()).filter(Boolean)
            : [],
        options:
          questionType === "SHORT_ANSWER"
            ? []
            : options.map((option, position) => ({ ...option, position })),
      };
      const path = editingId
        ? `/admin/lessons/${lessonId}/questions/${editingId}`
        : `/admin/lessons/${lessonId}/questions`;
      return apiRequest<PracticeQuestion>(path, {
        method: editingId ? "PUT" : "POST",
        body: JSON.stringify(payload),
      });
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["practice", lessonId, "admin"] });
      resetForm();
    },
  });
  const remove = useMutation({
    mutationFn: (questionId: number) =>
      apiRequest<void>(`/admin/lessons/${lessonId}/questions/${questionId}`, {
        method: "DELETE",
      }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["practice", lessonId, "admin"] });
      resetForm();
    },
  });

  const changeType = (type: QuestionType) => {
    setQuestionType(type);
    setAcceptedAnswers("");
    setOptions(
      type === "TRUE_FALSE"
        ? [
            { option_text: "True", is_correct: true },
            { option_text: "False", is_correct: false },
          ]
        : defaultOptions.map((option) => ({ ...option })),
    );
  };
  const editQuestion = (question: PracticeQuestion) => {
    setEditingId(question.id);
    setTopicId(String(question.topic_id));
    setQuestionText(question.question_text);
    setQuestionType(question.question_type);
    setDifficulty(String(question.difficulty_score));
    setExplanation(question.explanation ?? "");
    setAcceptedAnswers(question.accepted_answers?.join(", ") ?? "");
    setOptions(
      question.options.length
        ? question.options.map((option) => ({
            option_text: option.option_text,
            is_correct: Boolean(option.is_correct),
          }))
        : defaultOptions.map((option) => ({ ...option })),
    );
    save.reset();
  };
  const updateOption = (index: number, changes: Partial<DraftOption>) => {
    setOptions((current) =>
      current.map((option, optionIndex) =>
        optionIndex === index ? { ...option, ...changes } : option,
      ),
    );
  };
  const chooseCorrect = (index: number) => {
    setOptions((current) =>
      current.map((option, optionIndex) => ({
        ...option,
        is_correct: optionIndex === index,
      })),
    );
  };

  return (
    <AppShell>
      {!currentUser.isPending && !currentUser.data?.is_admin ? (
        <section className="rounded-2xl border border-red-200 bg-red-50 p-8">
          <h1 className="text-2xl font-bold text-red-900">Administrator access required</h1>
          <p className="mt-2 text-red-800">Your account cannot manage official questions.</p>
        </section>
      ) : (
        <>
          <header>
            <p className="text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">Administration</p>
            <h1 className="mt-2 text-3xl font-bold">Practice questions</h1>
            <p className="mt-2 text-slate-600">Create and maintain the official question bank for each lesson.</p>
          </header>

          <div className="mt-8">
            <label htmlFor="admin-lesson" className="mb-2 block text-sm font-semibold">Lesson</label>
            <select
              id="admin-lesson"
              value={lessonId}
              onChange={(event) => {
                setLessonId(event.target.value);
                setEditingId(null);
              }}
              className="min-h-11 w-full max-w-xl rounded-lg border border-slate-300 bg-white px-3"
            >
              {lessons.data?.length === 0 && <option value="">No lessons available</option>}
              {lessons.data?.map((lesson) => <option key={lesson.id} value={lesson.id}>{lesson.title}</option>)}
            </select>
          </div>

          {lessonId && (
            <div className="mt-8 grid gap-7 xl:grid-cols-[minmax(0,1fr)_minmax(360px,0.8fr)]">
              <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-xl font-bold">{editingId ? "Edit question" : "Add question"}</h2>
                <form className="mt-5 space-y-5" onSubmit={(event) => { event.preventDefault(); save.mutate(); }}>
                  <div>
                    <label htmlFor="question-text" className="mb-2 block text-sm font-semibold">Question text</label>
                    <textarea id="question-text" required value={questionText} onChange={(event) => setQuestionText(event.target.value)} className="min-h-28 w-full rounded-lg border border-slate-300 p-3" />
                  </div>
                  <div className="grid gap-4 sm:grid-cols-3">
                    <div>
                      <label htmlFor="question-type" className="mb-2 block text-sm font-semibold">Type</label>
                      <select id="question-type" value={questionType} onChange={(event) => changeType(event.target.value as QuestionType)} className="min-h-11 w-full rounded-lg border border-slate-300 bg-white px-3">
                        <option value="MCQ">Multiple choice</option>
                        <option value="TRUE_FALSE">True / False</option>
                        <option value="SHORT_ANSWER">Short answer</option>
                      </select>
                    </div>
                    <div>
                      <label htmlFor="question-topic" className="mb-2 block text-sm font-semibold">Topic</label>
                      <select id="question-topic" required value={topicId} onChange={(event) => setTopicId(event.target.value)} className="min-h-11 w-full rounded-lg border border-slate-300 bg-white px-3">
                        <option value="">Select topic</option>
                        {topics.data?.map((topic) => <option key={topic.id} value={topic.id}>{topic.name}</option>)}
                      </select>
                    </div>
                    <div>
                      <label htmlFor="question-difficulty" className="mb-2 block text-sm font-semibold">Difficulty (0–100)</label>
                      <Input id="question-difficulty" type="number" min="0" max="100" step="0.01" value={difficulty} onChange={(event) => setDifficulty(event.target.value)} />
                    </div>
                  </div>

                  {questionType !== "SHORT_ANSWER" && (
                    <fieldset className="space-y-3">
                      <legend className="text-sm font-semibold">Options and correct answer</legend>
                      {options.map((option, index) => (
                        <div key={index} className="flex items-center gap-3">
                          <input type="radio" name="correct-option" checked={option.is_correct} onChange={() => chooseCorrect(index)} className="size-5 accent-blue-700" aria-label={`Mark option ${index + 1} correct`} />
                          <Input
                            required
                            value={option.option_text}
                            disabled={questionType === "TRUE_FALSE"}
                            onChange={(event) => updateOption(index, { option_text: event.target.value })}
                            placeholder={`Option ${index + 1}`}
                          />
                          {questionType === "MCQ" && options.length > 2 && (
                            <button type="button" onClick={() => setOptions((current) => current.filter((_, itemIndex) => itemIndex !== index))} className="text-sm font-semibold text-red-700">Remove</button>
                          )}
                        </div>
                      ))}
                      {questionType === "MCQ" && (
                        <button type="button" onClick={() => setOptions((current) => [...current, { option_text: "", is_correct: false }])} className="text-sm font-semibold text-blue-700">+ Add option</button>
                      )}
                    </fieldset>
                  )}
                  {questionType === "SHORT_ANSWER" && (
                    <div>
                      <label htmlFor="accepted-answers" className="mb-2 block text-sm font-semibold">Accepted answers</label>
                      <Input id="accepted-answers" required value={acceptedAnswers} onChange={(event) => setAcceptedAnswers(event.target.value)} placeholder="Separate alternatives with commas" />
                    </div>
                  )}
                  <div>
                    <label htmlFor="question-explanation" className="mb-2 block text-sm font-semibold">Explanation</label>
                    <textarea id="question-explanation" value={explanation} onChange={(event) => setExplanation(event.target.value)} className="min-h-24 w-full rounded-lg border border-slate-300 p-3" />
                  </div>
                  {save.error && (
                    <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-800">
                      {save.error instanceof ApiError ? save.error.message : "Unable to save question"}
                    </p>
                  )}
                  {save.isSuccess && <p role="status" className="text-sm text-green-700">Question saved.</p>}
                  <div className="flex gap-3">
                    <Button type="submit" disabled={save.isPending}>{save.isPending ? "Saving…" : editingId ? "Update question" : "Add question"}</Button>
                    {editingId && <Button type="button" className="bg-slate-700 hover:bg-slate-900" onClick={resetForm}>Cancel</Button>}
                  </div>
                </form>
              </section>

              <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
                <h2 className="text-xl font-bold">Existing questions</h2>
                {practice.isPending && <p className="mt-4 text-slate-600">Loading questions…</p>}
                {practice.data?.questions.length === 0 && <p className="mt-4 text-slate-600">No questions have been added.</p>}
                <div className="mt-4 space-y-4">
                  {practice.data?.questions.map((question) => (
                    <article key={question.id} className="rounded-xl border border-slate-200 p-4">
                      <div className="flex justify-between gap-3">
                        <div>
                          <p className="text-xs font-bold uppercase tracking-wide text-blue-700">{question.question_type.replace("_", " ")}</p>
                          <h3 className="mt-2 font-semibold">{question.question_text}</h3>
                        </div>
                        <span className="text-sm text-slate-500">{question.difficulty_score}</span>
                      </div>
                      <div className="mt-4 flex gap-4">
                        <button type="button" onClick={() => editQuestion(question)} className="text-sm font-semibold text-blue-700">Edit</button>
                        <button
                          type="button"
                          onClick={() => {
                            if (window.confirm("Delete this practice question?")) remove.mutate(question.id);
                          }}
                          className="text-sm font-semibold text-red-700"
                        >
                          Delete
                        </button>
                      </div>
                    </article>
                  ))}
                </div>
              </section>
            </div>
          )}
        </>
      )}
    </AppShell>
  );
}
