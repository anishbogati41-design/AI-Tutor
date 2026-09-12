"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { AppShell } from "@/components/app-shell";
import { ApiError, apiRequest } from "@/lib/api";
import type { StudyPlan, StudyPlanItem } from "@/types/study-plan";

function formatDate(value: string): string {
  return new Intl.DateTimeFormat(undefined, {
    weekday: "long",
    month: "long",
    day: "numeric",
  }).format(new Date(`${value}T00:00:00`));
}

function isToday(value: string): boolean {
  const today = new Date();
  const localDate = [
    today.getFullYear(),
    String(today.getMonth() + 1).padStart(2, "0"),
    String(today.getDate()).padStart(2, "0"),
  ].join("-");
  return value === localDate;
}

function groupByDate(items: StudyPlanItem[]): Array<[string, StudyPlanItem[]]> {
  const groups = new Map<string, StudyPlanItem[]>();
  for (const item of items) {
    groups.set(item.scheduled_date, [
      ...(groups.get(item.scheduled_date) ?? []),
      item,
    ]);
  }
  return [...groups.entries()];
}

export default function StudyPlanPage() {
  const queryClient = useQueryClient();
  const [confirming, setConfirming] = useState(false);
  const [notice, setNotice] = useState("");
  const plan = useQuery({
    queryKey: ["study-plan"],
    queryFn: () => apiRequest<StudyPlan | null>("/study-plan"),
  });
  const refresh = useMutation({
    mutationFn: () =>
      apiRequest<StudyPlan>("/study-plan/refresh", { method: "POST" }),
    onSuccess: (newPlan) => {
      queryClient.setQueryData(["study-plan"], newPlan);
      queryClient.invalidateQueries({ queryKey: ["progress"] });
      setConfirming(false);
      setNotice("Your study plan has been refreshed.");
    },
  });

  const groups = groupByDate(plan.data?.items ?? []);
  const error = plan.error ?? refresh.error;

  return (
    <AppShell>
      <header className="flex flex-col gap-5 sm:flex-row sm:items-start sm:justify-between">
        <div>
          <p className="text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">
            Your learning
          </p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight">Study Plan</h1>
          <p className="mt-2 text-slate-600">
            Your personalized study plan based on your current progress.
          </p>
        </div>
        <button
          type="button"
          onClick={() => {
            setNotice("");
            refresh.reset();
            setConfirming(true);
          }}
          disabled={refresh.isPending}
          className="inline-flex min-h-11 items-center justify-center rounded-lg bg-blue-700 px-5 py-2 font-semibold text-white hover:bg-blue-800 disabled:cursor-wait disabled:opacity-60"
        >
          {refresh.isPending ? "Refreshing…" : "↻ Refresh"}
        </button>
      </header>

      {notice && (
        <p role="status" className="mt-6 rounded-xl bg-emerald-50 p-4 text-emerald-800">
          {notice}
        </p>
      )}
      {error && (
        <p role="alert" className="mt-6 rounded-xl bg-red-50 p-4 text-red-800">
          {error instanceof ApiError ? error.message : "Unable to load the study plan"}
        </p>
      )}

      <div className="relative mt-8 min-h-48">
        {refresh.isPending && (
          <div className="absolute inset-0 z-10 flex items-start justify-center rounded-2xl bg-white/80 pt-16" aria-live="polite">
            <p className="rounded-xl border border-slate-200 bg-white px-5 py-4 font-semibold text-blue-800 shadow-sm">
              ↻ Generating your new study plan…
            </p>
          </div>
        )}
        {plan.isPending && <p className="text-slate-600">Loading your study plan…</p>}
        {!plan.isPending && !plan.error && groups.length === 0 && (
          <section className="rounded-2xl border border-dashed border-slate-300 bg-white p-10 text-center">
            <h2 className="text-xl font-bold">No study plan yet</h2>
            <p className="mt-2 text-slate-600">
              Refresh to generate a plan from your published lessons and learning progress.
            </p>
          </section>
        )}
        <div className="space-y-6">
          {groups.map(([scheduledDate, items]) => (
            <section key={scheduledDate} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <div className="flex items-center justify-between gap-4 border-b border-slate-100 pb-4">
                <h2 className="text-lg font-bold">📅 {formatDate(scheduledDate)}</h2>
                {isToday(scheduledDate) && (
                  <span className="rounded-full bg-blue-50 px-3 py-1 text-xs font-bold uppercase tracking-wide text-blue-800">
                    Today
                  </span>
                )}
              </div>
              <div className="mt-5 space-y-4">
                {items.map((item) => (
                  <article key={item.id} className="rounded-xl border border-slate-200 p-5 transition hover:shadow-md">
                    <div className="flex items-start gap-3">
                      <span aria-hidden="true" className="mt-1 text-blue-600">●</span>
                      <div>
                        <h3 className="font-bold text-slate-950">{item.title}</h3>
                        <p className="mt-1 text-sm leading-6 text-slate-600">{item.description}</p>
                        {item.completed && (
                          <p className="mt-2 text-sm font-semibold text-emerald-700">Completed</p>
                        )}
                      </div>
                    </div>
                  </article>
                ))}
              </div>
            </section>
          ))}
        </div>
      </div>

      {confirming && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4" role="presentation">
          <section role="dialog" aria-modal="true" aria-labelledby="refresh-plan-title" className="w-full max-w-md rounded-2xl bg-white p-6 shadow-2xl">
            <h2 id="refresh-plan-title" className="text-xl font-bold">Refresh study plan?</h2>
            <p className="mt-3 text-slate-600">
              Generate a new study plan? Your current plan will be replaced.
            </p>
            <div className="mt-6 flex justify-end gap-3">
              <button type="button" onClick={() => setConfirming(false)} className="min-h-11 rounded-lg border border-slate-300 px-4 font-semibold text-slate-700 hover:bg-slate-50">
                Cancel
              </button>
              <button type="button" onClick={() => { setConfirming(false); refresh.mutate(); }} className="min-h-11 rounded-lg bg-blue-700 px-4 font-semibold text-white hover:bg-blue-800">
                Refresh Plan
              </button>
            </div>
          </section>
        </div>
      )}
    </AppShell>
  );
}
