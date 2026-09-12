"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useParams } from "next/navigation";

import { AppShell } from "@/components/app-shell";
import { ApiError, apiRequest } from "@/lib/api";
import type { AdminStudentProgress } from "@/types/progress";

export default function AdminStudentProgressPage() {
  const parameters = useParams<{ id: string }>();
  const result = useQuery({
    queryKey: ["admin-student-progress", parameters.id],
    queryFn: () => apiRequest<AdminStudentProgress>(`/admin/students/${parameters.id}/progress`),
  });
  const progress = result.data?.progress;

  return (
    <AppShell>
      <Link href="/admin/students" className="text-sm font-semibold text-blue-700">← All students</Link>
      <h1 className="mt-5 text-3xl font-bold">{result.data?.student.name ?? "Student progress"}</h1>
      {result.data && <p className="mt-2 text-slate-600">{result.data.student.email}</p>}
      {result.isPending && <p className="mt-8">Loading progress…</p>}
      {result.error && <p role="alert" className="mt-8 rounded-xl bg-red-50 p-4 text-red-800">{result.error instanceof ApiError ? result.error.message : "Unable to load progress"}</p>}
      {progress && <>
        <section className="mt-7 grid gap-4 sm:grid-cols-2">
          <article className="rounded-2xl border border-slate-200 bg-white p-6"><p className="text-sm text-slate-500">Overall score</p><p className="mt-2 text-3xl font-bold">{progress.overall_score}%</p></article>
          <article className="rounded-2xl border border-slate-200 bg-white p-6"><p className="text-sm text-slate-500">Weak topics</p><p className="mt-2 text-3xl font-bold">{progress.weak_topics.length}</p></article>
        </section>
        <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6">
          <h2 className="text-xl font-bold">Course progress</h2>
          <div className="mt-5 space-y-5">{progress.course_progress.map((course) => (
            <article key={course.lesson_id} className="rounded-xl border border-slate-200 p-5">
              <div className="flex flex-wrap items-start justify-between gap-3"><div><h3 className="font-bold">{course.lesson_title}</h3><p className="mt-1 text-sm text-slate-600">{course.topic_name} · {course.attempt_count} attempts · {course.correct_count} correct · {course.accuracy}% accuracy</p></div><span className="rounded-full bg-slate-100 px-3 py-1 text-xs font-bold">{course.status.replaceAll("_", " ")}</span></div>
              <div className="mt-4 h-3 overflow-hidden rounded-full bg-slate-100"><div className="h-full bg-blue-600" style={{ width: `${course.progress_percentage}%` }} /></div>
              <p className="mt-2 text-right text-sm font-semibold">{course.progress_percentage}% practiced</p>
            </article>
          ))}</div>
        </section>
        <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6">
          <h2 className="text-xl font-bold">Topic mastery</h2>
          {progress.mastery.length === 0 ? <p className="mt-4 text-slate-600">No practice results yet.</p> : <div className="mt-5 space-y-4">{progress.mastery.map((item) => <div key={item.topic_id}><div className="flex justify-between"><span className="font-semibold">{item.topic_name}</span><span>{item.mastery_percentage}% · {item.mastery_label}</span></div><div className="mt-2 h-3 overflow-hidden rounded-full bg-slate-100"><div className="h-full bg-blue-600" style={{ width: `${item.mastery_percentage}%` }} /></div></div>)}</div>}
        </section>
      </>}
    </AppShell>
  );
}
