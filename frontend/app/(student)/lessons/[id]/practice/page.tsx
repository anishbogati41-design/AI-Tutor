"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ApiError, apiRequest } from "@/lib/api";
import type { AdaptiveQuestion, AnswerResult, PracticeSession } from "@/types/content";

function difficultyLabel(score: number) {
  if (score < 34) return "Foundational";
  if (score < 67) return "Intermediate";
  return "Advanced";
}

export default function PracticePage() {
  const parameters = useParams<{ id: string }>();
  const queryClient = useQueryClient();
  const [answer, setAnswer] = useState("");
  const [result, setResult] = useState<AnswerResult | null>(null);
  const [sessionCounts, setSessionCounts] = useState({ correct: 0, total: 0 });
  const practice = useQuery({
    queryKey: ["practice", parameters.id],
    queryFn: () => apiRequest<PracticeSession>(`/lessons/${parameters.id}/practice`),
  });
  const adaptive = useQuery({
    queryKey: ["next-practice-question", parameters.id],
    queryFn: () => apiRequest<AdaptiveQuestion>(`/lessons/${parameters.id}/practice/next`),
  });
  const question = adaptive.data?.question;
  const submit = useMutation({
    mutationFn: () =>
      apiRequest<AnswerResult>(`/practice/${question?.id}/answer`, {
        method: "POST",
        body: JSON.stringify({ answer }),
      }),
    onSuccess: (answerResult) => {
      setResult(answerResult);
      setSessionCounts((counts) => ({
        correct: counts.correct + Number(answerResult.is_correct),
        total: counts.total + 1,
      }));
      queryClient.invalidateQueries({ queryKey: ["practice", parameters.id] });
      queryClient.invalidateQueries({ queryKey: ["progress"] });
    },
  });

  useEffect(() => {
    setAnswer("");
    setResult(null);
    setSessionCounts({ correct: 0, total: 0 });
  }, [parameters.id]);

  const nextQuestion = () => {
    setAnswer("");
    setResult(null);
    submit.reset();
    queryClient.invalidateQueries({ queryKey: ["next-practice-question", parameters.id] });
  };

  return (
    <AppShell>
      <Link href="/practice" className="text-sm font-semibold text-blue-700 hover:text-blue-900">
        ← Choose another lesson
      </Link>
      {practice.isPending && <p className="mt-8 text-slate-600">Loading practice…</p>}
      {practice.error && (
        <p role="alert" className="mt-8 rounded-xl bg-red-50 p-4 text-red-800">
          {practice.error instanceof ApiError ? practice.error.message : "Unable to load practice"}
        </p>
      )}
      {adaptive.error && !practice.error && (
        <p role="alert" className="mt-8 rounded-xl bg-red-50 p-4 text-red-800">
          {adaptive.error instanceof ApiError ? adaptive.error.message : "Unable to load the next question"}
        </p>
      )}
      {practice.data && (
        <>
          <header className="mt-6 flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">Practice</p>
              <h1 className="mt-2 text-3xl font-bold">{practice.data.lesson_title}</h1>
            </div>
            <div className="rounded-xl bg-slate-100 px-4 py-3 text-sm text-slate-700">
              This session: {sessionCounts.correct}/{sessionCounts.total} correct · Overall: {practice.data.summary.accuracy}%
            </div>
          </header>

          {adaptive.isPending ? (
            <p className="mt-8 text-slate-600">Selecting your next question…</p>
          ) : !question ? (
            <section className="mt-8 rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
              <h2 className="text-xl font-bold">No practice questions yet</h2>
              <p className="mt-2 text-slate-600">Questions for this lesson are still being prepared.</p>
              <Link href={`/lessons/${parameters.id}`} className="mt-5 inline-block font-semibold text-blue-700">
                Return to the lesson
              </Link>
            </section>
          ) : (
            <section className="mt-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm md:p-9">
              <div className="flex flex-wrap justify-between gap-3 text-sm text-slate-500">
                <span>{adaptive.data?.mastery_label.toLowerCase()} mastery · {adaptive.data?.mastery_percentage}%</span>
                <span>{difficultyLabel(question.difficulty_score)} · target {adaptive.data?.target_difficulty}</span>
              </div>
              <h2 className="mt-6 text-2xl font-bold leading-9">{question.question_text}</h2>

              {!result && question.question_type !== "SHORT_ANSWER" && (
                <div className="mt-7 space-y-3">
                  {question.options.map((option) => (
                    <label
                      key={option.id}
                      className={`flex cursor-pointer items-center gap-3 rounded-xl border p-4 ${
                        answer === option.option_text
                          ? "border-blue-600 bg-blue-50"
                          : "border-slate-200 hover:bg-slate-50"
                      }`}
                    >
                      <input
                        type="radio"
                        name="practice-answer"
                        value={option.option_text}
                        checked={answer === option.option_text}
                        onChange={(event) => setAnswer(event.target.value)}
                        className="size-5 accent-blue-700"
                      />
                      <span>{option.option_text}</span>
                    </label>
                  ))}
                </div>
              )}
              {!result && question.question_type === "SHORT_ANSWER" && (
                <div className="mt-7">
                  <label htmlFor="short-answer" className="mb-2 block text-sm font-semibold">Your answer</label>
                  <Input
                    id="short-answer"
                    value={answer}
                    onChange={(event) => setAnswer(event.target.value)}
                    placeholder="Type your answer"
                    onKeyDown={(event) => {
                      if (event.key === "Enter" && answer.trim()) submit.mutate();
                    }}
                  />
                </div>
              )}
              {submit.error && (
                <p role="alert" className="mt-5 text-sm text-red-700">
                  {submit.error instanceof ApiError ? submit.error.message : "Unable to submit answer"}
                </p>
              )}
              {!result && (
                <Button
                  type="button"
                  className="mt-7"
                  disabled={!answer.trim() || submit.isPending}
                  onClick={() => submit.mutate()}
                >
                  {submit.isPending ? "Checking…" : "Submit answer"}
                </Button>
              )}
              {result && (
                <div className={`mt-7 rounded-xl border-l-4 p-5 ${result.is_correct ? "border-green-600 bg-green-50" : "border-red-600 bg-red-50"}`}>
                  <h3 className="text-xl font-bold">{result.is_correct ? "Correct!" : "Incorrect"}</h3>
                  {!result.is_correct && <p className="mt-2">Correct answer: <strong>{result.correct_answer}</strong></p>}
                  <p className="mt-3 leading-7">{result.explanation || "Review the lesson explanation and try another question."}</p>
                  <Button type="button" className="mt-5" onClick={nextQuestion}>Next question →</Button>
                </div>
              )}
            </section>
          )}
        </>
      )}
    </AppShell>
  );
}
