"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";

import { AppShell } from "@/components/app-shell";
import { ApiError, apiRequest } from "@/lib/api";
import type { Lesson, Topic } from "@/types/content";

export default function PracticeLibraryPage() {
  const lessons = useQuery({
    queryKey: ["lessons", "practice-library"],
    queryFn: () => apiRequest<Lesson[]>("/lessons"),
  });
  const topics = useQuery({
    queryKey: ["topics"],
    queryFn: () => apiRequest<Topic[]>("/topics"),
  });
  const topicById = new Map(topics.data?.map((topic) => [topic.id, topic.name]));

  return (
    <AppShell>
      <header>
        <p className="text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">
          Practice
        </p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight">Choose a lesson</h1>
        <p className="mt-2 text-slate-600">
          Work through official practice questions and build your lesson record.
        </p>
      </header>
      {lessons.isPending && <p className="mt-8 text-slate-600">Loading lessons…</p>}
      {lessons.error && (
        <p role="alert" className="mt-8 rounded-xl bg-red-50 p-4 text-red-800">
          {lessons.error instanceof ApiError ? lessons.error.message : "Unable to load lessons"}
        </p>
      )}
      {lessons.data?.length === 0 && (
        <section className="mt-8 rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
          <h2 className="text-xl font-bold">No practice lessons yet</h2>
          <p className="mt-2 text-slate-600">Published lessons will appear here.</p>
        </section>
      )}
      <section className="mt-8 grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
        {lessons.data?.map((lesson) => (
          <article key={lesson.id} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
            <p className="text-sm font-semibold text-blue-700">
              {topicById.get(lesson.subtopic_id) ?? "Lesson"}
            </p>
            <h2 className="mt-2 text-xl font-bold">{lesson.title}</h2>
            <p className="mt-3 min-h-14 text-slate-600">
              {lesson.description || "Review what you learned through practice."}
            </p>
            <Link
              href={`/lessons/${lesson.id}/practice`}
              className="mt-5 inline-flex min-h-11 w-full items-center justify-center rounded-lg bg-blue-700 px-4 py-2 font-semibold text-white hover:bg-blue-800"
            >
              Start practice →
            </Link>
          </article>
        ))}
      </section>
    </AppShell>
  );
}
