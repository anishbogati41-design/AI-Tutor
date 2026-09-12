"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { useState } from "react";

import { AdminGuard } from "@/components/admin/admin-guard";
import { AppShell } from "@/components/app-shell";
import { Input } from "@/components/ui/input";
import { ApiError, apiRequest } from "@/lib/api";
import type { Lesson, Topic } from "@/types/content";

export default function AdminLessonsPage() {
  const queryClient = useQueryClient(); const [search, setSearch] = useState(""); const [topicId, setTopicId] = useState("");
  const lessons = useQuery({ queryKey: ["lessons", "admin"], queryFn: () => apiRequest<Lesson[]>("/lessons") });
  const topics = useQuery({ queryKey: ["topics"], queryFn: () => apiRequest<Topic[]>("/topics") });
  const remove = useMutation({ mutationFn: (id: number) => apiRequest<void>(`/admin/lessons/${id}`, { method: "DELETE" }), onSuccess: () => queryClient.invalidateQueries({ queryKey: ["lessons"] }) });
  const visible = lessons.data?.filter((lesson) => lesson.title.toLowerCase().includes(search.toLowerCase()) && (!topicId || lesson.subtopic_id === Number(topicId))) ?? [];
  const topicName = (id: number) => topics.data?.find((topic) => topic.id === id)?.name ?? "Unknown";
  return <AppShell><AdminGuard><header className="flex flex-wrap items-end justify-between gap-4"><div><p className="text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">Administration</p><h1 className="mt-2 text-3xl font-bold">Lessons</h1></div><Link href="/admin/lessons/new" className="rounded-lg bg-blue-700 px-5 py-3 font-semibold text-white">+ New lesson</Link></header><div className="mt-7 grid gap-4 sm:grid-cols-[1fr_240px]"><Input aria-label="Search lessons" placeholder="Search lessons" value={search} onChange={(event) => setSearch(event.target.value)} /><select aria-label="Filter by topic" value={topicId} onChange={(event) => setTopicId(event.target.value)} className="min-h-11 rounded-lg border border-slate-300 bg-white px-3"><option value="">All topics</option>{topics.data?.map((topic) => <option key={topic.id} value={topic.id}>{topic.name}</option>)}</select></div>{lessons.isPending && <p className="mt-8 text-slate-600">Loading lessons…</p>}<section className="mt-6 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">{visible.length === 0 && lessons.data && <p className="p-6 text-slate-600">No matching lessons.</p>}{visible.map((lesson) => <article key={lesson.id} className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 p-5 last:border-0"><div><div className="flex items-center gap-3"><h2 className="font-bold">{lesson.title}</h2><span className={`rounded-full px-2 py-1 text-xs font-bold ${lesson.is_published ? "bg-green-100 text-green-800" : "bg-slate-100 text-slate-700"}`}>{lesson.is_published ? "Published" : "Draft"}</span></div><p className="mt-1 text-sm text-slate-600">{topicName(lesson.subtopic_id)} · {lesson.estimated_minutes} minutes</p></div><div className="flex flex-wrap gap-4"><Link href={`/admin/lessons/${lesson.id}`} className="text-sm font-semibold text-blue-700">Edit</Link><Link href={`/admin/lessons/${lesson.id}/questions`} className="text-sm font-semibold text-blue-700">Questions</Link><button type="button" onClick={() => window.confirm(`Delete ${lesson.title}?`) && remove.mutate(lesson.id)} className="text-sm font-semibold text-red-700">Delete</button></div></article>)}</section>{remove.error && <p role="alert" className="mt-4 text-sm text-red-700">{remove.error instanceof ApiError ? remove.error.message : "Unable to delete lesson"}</p>}</AdminGuard></AppShell>;
}
