"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useDeferredValue, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { Input } from "@/components/ui/input";
import { ApiError, apiRequest } from "@/lib/api";
import type { Lesson, Topic } from "@/types/content";

export default function LessonsPage() {
  const [search, setSearch] = useState("");
  const [topicId, setTopicId] = useState("");
  const deferredSearch = useDeferredValue(search.trim());
  const topics = useQuery({
    queryKey: ["topics"],
    queryFn: () => apiRequest<Topic[]>("/topics"),
  });
  const lessons = useQuery({
    queryKey: ["lessons", deferredSearch, topicId],
    queryFn: () => {
      const parameters = new URLSearchParams();
      if (deferredSearch) parameters.set("search", deferredSearch);
      if (topicId) parameters.set("topic_id", topicId);
      const query = parameters.toString();
      return apiRequest<Lesson[]>(`/lessons${query ? `?${query}` : ""}`);
    },
  });
  const topicById = new Map(topics.data?.map((topic) => [topic.id, topic.name]));
  const subtopics = topics.data?.filter((topic) => topic.parent_topic_id !== null) ?? [];

  return (
    <AppShell>
      <header>
        <p className="text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">
          Learn
        </p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight">Lessons</h1>
        <p className="mt-2 text-slate-600">
          Choose a topic and continue with a structured lesson.
        </p>
      </header>

      <section className="mt-8 grid gap-4 rounded-2xl border border-slate-200 bg-white p-5 shadow-sm md:grid-cols-[1fr_240px]">
        <div>
          <label htmlFor="lesson-search" className="mb-2 block text-sm font-semibold">
            Search lessons
          </label>
          <Input
            id="lesson-search"
            type="search"
            placeholder="Search by title or description"
            value={search}
            onChange={(event) => setSearch(event.target.value)}
          />
        </div>
        <div>
          <label htmlFor="topic-filter" className="mb-2 block text-sm font-semibold">
            Topic
          </label>
          <select
            id="topic-filter"
            value={topicId}
            onChange={(event) => setTopicId(event.target.value)}
            className="min-h-11 w-full rounded-lg border border-slate-300 bg-white px-3"
          >
            <option value="">All topics</option>
            {subtopics.map((topic) => (
              <option key={topic.id} value={topic.id}>
                {topic.name}
              </option>
            ))}
          </select>
        </div>
      </section>

      {lessons.isPending && <p className="mt-8 text-slate-600">Loading lessons…</p>}
      {lessons.error && (
        <p role="alert" className="mt-8 rounded-xl bg-red-50 p-4 text-red-800">
          {lessons.error instanceof ApiError
            ? lessons.error.message
            : "Unable to load lessons"}
        </p>
      )}
      {lessons.data?.length === 0 && (
        <section className="mt-8 rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
          <h2 className="text-xl font-bold">No lessons found</h2>
          <p className="mt-2 text-slate-600">
            Try another search or topic. Published lessons will appear here.
          </p>
        </section>
      )}
      {lessons.data && lessons.data.length > 0 && (
        <section className="mt-8 grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
          {lessons.data.map((lesson) => (
            <article
              key={lesson.id}
              className="flex flex-col rounded-2xl border border-slate-200 bg-white p-6 shadow-sm transition hover:-translate-y-0.5 hover:shadow-md"
            >
              <p className="text-sm font-semibold text-blue-700">
                {topicById.get(lesson.subtopic_id) ?? "Lesson"}
              </p>
              <h2 className="mt-2 text-xl font-bold">{lesson.title}</h2>
              <p className="mt-3 flex-1 leading-7 text-slate-600">
                {lesson.description || "Open this lesson to begin learning."}
              </p>
              <p className="mt-5 text-sm text-slate-500">
                {lesson.estimated_minutes} minutes
              </p>
              <Link
                href={`/lessons/${lesson.id}`}
                className="mt-5 inline-flex min-h-11 items-center justify-center rounded-lg bg-blue-700 px-4 py-2 font-semibold text-white hover:bg-blue-800"
              >
                View lesson →
              </Link>
            </article>
          ))}
        </section>
      )}
    </AppShell>
  );
}
