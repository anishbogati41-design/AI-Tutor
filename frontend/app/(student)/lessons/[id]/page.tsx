"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { ApiError, apiRequest } from "@/lib/api";
import type { LessonDetail, Topic } from "@/types/content";

const sectionLabels = {
  INTRODUCTION: "Introduction",
  EXPLANATION: "Explanation",
  EXAMPLE: "Example",
  SUMMARY: "Summary",
};

export default function LessonPage() {
  const parameters = useParams<{ id: string }>();
  const [sectionIndex, setSectionIndex] = useState(0);
  const [viewed, setViewed] = useState(() => new Set([0]));
  const lesson = useQuery({
    queryKey: ["lesson", parameters.id],
    queryFn: () => apiRequest<LessonDetail>(`/lessons/${parameters.id}`),
  });
  const topic = useQuery({
    queryKey: ["topic", lesson.data?.subtopic_id],
    queryFn: () => apiRequest<Topic>(`/topics/${lesson.data?.subtopic_id}`),
    enabled: Boolean(lesson.data),
  });

  useEffect(() => {
    setSectionIndex(0);
    setViewed(new Set([0]));
  }, [parameters.id]);

  const selectSection = (index: number) => {
    setSectionIndex(index);
    setViewed((previous) => new Set(previous).add(index));
  };
  const sections = lesson.data?.sections ?? [];
  const currentSection = sections[sectionIndex];

  return (
    <AppShell>
      <Link href="/lessons" className="text-sm font-semibold text-blue-700 hover:text-blue-900">
        ← Back to lessons
      </Link>

      {lesson.isPending && <p className="mt-8 text-slate-600">Loading lesson…</p>}
      {lesson.error && (
        <p role="alert" className="mt-8 rounded-xl bg-red-50 p-4 text-red-800">
          {lesson.error instanceof ApiError ? lesson.error.message : "Unable to load lesson"}
        </p>
      )}
      {lesson.data && (
        <>
          <header className="mt-6">
            <p className="text-sm font-semibold text-blue-700">
              {topic.data?.name ?? "Lesson"}
            </p>
            <h1 className="mt-2 text-3xl font-bold tracking-tight">{lesson.data.title}</h1>
            <p className="mt-3 text-slate-600">
              {lesson.data.estimated_minutes} minutes
              {lesson.data.description ? ` · ${lesson.data.description}` : ""}
            </p>
            <Link
              href={`/lessons/${lesson.data.id}/practice`}
              className="mt-5 inline-flex min-h-11 items-center rounded-lg bg-blue-700 px-5 py-2.5 font-semibold text-white hover:bg-blue-800"
            >
              Practice this lesson →
            </Link>
          </header>

          {sections.length === 0 ? (
            <section className="mt-8 rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
              <h2 className="text-xl font-bold">Content is being prepared</h2>
              <p className="mt-2 text-slate-600">This lesson has no sections yet.</p>
            </section>
          ) : (
            <div className="mt-8 grid gap-6 lg:grid-cols-[240px_1fr]">
              <aside className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
                <h2 className="px-2 text-sm font-bold uppercase tracking-wide text-slate-500">
                  Sections
                </h2>
                <ol className="mt-3 space-y-2">
                  {sections.map((section, index) => (
                    <li key={section.id}>
                      <button
                        type="button"
                        onClick={() => selectSection(index)}
                        className={`w-full rounded-lg px-3 py-3 text-left text-sm transition ${
                          index === sectionIndex
                            ? "bg-blue-50 font-semibold text-blue-800"
                            : "text-slate-600 hover:bg-slate-50"
                        }`}
                      >
                        <span aria-hidden="true" className="mr-2">
                          {viewed.has(index) ? "●" : "○"}
                        </span>
                        {index + 1}. {sectionLabels[section.section_type]}
                      </button>
                    </li>
                  ))}
                </ol>
              </aside>

              {currentSection && (
                <article className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm md:p-9">
                  <p className="text-sm font-semibold uppercase tracking-wide text-blue-700">
                    {sectionLabels[currentSection.section_type]}
                  </p>
                  <h2 className="mt-2 text-2xl font-bold">{currentSection.title}</h2>
                  <div className="mt-6 whitespace-pre-wrap text-base leading-8 text-slate-700">
                    {currentSection.content}
                  </div>
                  <div className="mt-10 flex flex-wrap justify-between gap-3 border-t border-slate-200 pt-6">
                    <Button
                      type="button"
                      className="bg-slate-700 hover:bg-slate-900"
                      disabled={sectionIndex === 0}
                      onClick={() => selectSection(sectionIndex - 1)}
                    >
                      ← Previous
                    </Button>
                    {sectionIndex < sections.length - 1 ? (
                      <Button type="button" onClick={() => selectSection(sectionIndex + 1)}>
                        Next →
                      </Button>
                    ) : (
                      <Link
                        href="/lessons"
                        className="inline-flex min-h-11 items-center rounded-lg bg-green-700 px-5 py-2.5 font-semibold text-white hover:bg-green-800"
                      >
                        Finish lesson
                      </Link>
                    )}
                  </div>
                </article>
              )}
            </div>
          )}
        </>
      )}
    </AppShell>
  );
}
