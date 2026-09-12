"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";

import { AppShell } from "@/components/app-shell";
import { ApiError, apiRequest } from "@/lib/api";
import type { Progress } from "@/types/progress";

const masteryColor: Record<string, string> = {
  BEGINNER: "bg-red-500", DEVELOPING: "bg-orange-500", INTERMEDIATE: "bg-yellow-500",
  PROFICIENT: "bg-green-500", MASTERED: "bg-indigo-500",
};

export default function DashboardPage() {
  const progress = useQuery({ queryKey: ["progress"], queryFn: () => apiRequest<Progress>("/progress") });
  return (
    <AppShell>
      <header><p className="text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">Your learning</p><h1 className="mt-2 text-3xl font-bold">Dashboard</h1><p className="mt-2 text-slate-600">Your practice results shape the next question you receive.</p></header>
      {progress.isPending && <p className="mt-8 text-slate-600">Loading progress…</p>}
      {progress.error && <p role="alert" className="mt-8 rounded-xl bg-red-50 p-4 text-red-800">{progress.error instanceof ApiError ? progress.error.message : "Unable to load progress"}</p>}
      {progress.data && <>
        <section className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {[
            ["Overall score", `${progress.data.overall_score}%`],
            ["Topics tracked", progress.data.mastery.length],
            ["Weak topics", progress.data.weak_topics.length],
            ["Mastered topics", progress.data.mastery.filter((item) => item.mastery_label === "MASTERED").length],
          ].map(([label, value]) => <article key={label} className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm"><p className="text-sm text-slate-500">{label}</p><p className="mt-2 text-3xl font-bold">{value}</p></article>)}
        </section>
        <div className="mt-6 grid gap-6 lg:grid-cols-[2fr_1fr]">
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-xl font-bold">Topic mastery</h2>
            {progress.data.mastery.length === 0 ? <p className="mt-4 text-slate-600">Complete a practice question to begin tracking mastery.</p> : <div className="mt-5 space-y-5">{progress.data.mastery.map((item) => <div key={item.topic_id}><div className="flex justify-between gap-4"><span className="font-semibold">{item.topic_name}</span><span className="text-sm text-slate-600">{item.mastery_percentage}% · {item.mastery_label.toLowerCase()}</span></div><div className="mt-2 h-3 overflow-hidden rounded-full bg-slate-100"><div className={`h-full ${masteryColor[item.mastery_label] ?? "bg-blue-500"}`} style={{ width: `${item.mastery_percentage}%` }} /></div></div>)}</div>}
          </section>
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-xl font-bold">Weak topics</h2>{progress.data.weak_topics.length === 0 ? <p className="mt-4 text-slate-600">No weak topics recorded.</p> : <div className="mt-4 space-y-3">{progress.data.weak_topics.map((item) => <article key={item.topic_id} className="rounded-xl bg-amber-50 p-4"><h3 className="font-bold">{item.topic_name}</h3><p className="mt-1 text-sm text-slate-700">{item.accuracy}% accuracy across {item.attempt_count} attempts</p></article>)}</div>}<Link href="/practice" className="mt-5 inline-block font-semibold text-blue-700">Continue practice →</Link></section>
        </div>
        <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <div className="flex items-center justify-between gap-4">
            <h2 className="text-xl font-bold">Study plan preview</h2>
            <Link href="/study-plan" className="font-semibold text-blue-700">View plan →</Link>
          </div>
          {progress.data.study_plan_preview.length === 0 ? (
            <p className="mt-4 text-slate-600">Generate a study plan to see your next learning tasks.</p>
          ) : (
            <div className="mt-4 grid gap-3 md:grid-cols-3">
              {progress.data.study_plan_preview.map((item) => (
                <article key={item.id} className="rounded-xl bg-blue-50 p-4">
                  <p className="text-xs font-bold uppercase tracking-wide text-blue-700">{item.scheduled_date}</p>
                  <h3 className="mt-2 font-bold">{item.title}</h3>
                  {item.completed && <p className="mt-2 text-sm font-semibold text-emerald-700">Completed</p>}
                </article>
              ))}
            </div>
          )}
        </section>
      </>}
    </AppShell>
  );
}
