"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";

import { AdminGuard } from "@/components/admin/admin-guard";
import { AppShell } from "@/components/app-shell";
import { apiRequest } from "@/lib/api";
import type { Lesson, Topic } from "@/types/content";
import type { AdminStudent } from "@/types/progress";

export default function AdminDashboardPage() {
  const students = useQuery({ queryKey: ["admin-students"], queryFn: () => apiRequest<AdminStudent[]>("/admin/students") });
  const lessons = useQuery({ queryKey: ["lessons", "admin"], queryFn: () => apiRequest<Lesson[]>("/lessons") });
  const topics = useQuery({ queryKey: ["topics"], queryFn: () => apiRequest<Topic[]>("/topics") });
  return <AppShell><AdminGuard><header><p className="text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">Administration</p><h1 className="mt-2 text-3xl font-bold">Admin dashboard</h1><p className="mt-2 text-slate-600">Manage learning content and review student progress.</p></header><section className="mt-8 grid gap-4 sm:grid-cols-3">{[["Students", students.data?.length ?? "…"], ["Lessons", lessons.data?.length ?? "…"], ["Topics", topics.data?.length ?? "…"]].map(([label, value]) => <article key={label} className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><p className="text-sm text-slate-500">Total {label.toString().toLowerCase()}</p><p className="mt-2 text-3xl font-bold">{value}</p></article>)}</section><section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-xl font-bold">Quick actions</h2><div className="mt-5 flex flex-wrap gap-3"><Link href="/admin/lessons/new" className="rounded-lg bg-blue-700 px-5 py-3 font-semibold text-white hover:bg-blue-800">+ New lesson</Link><Link href="/admin/topics" className="rounded-lg border border-slate-300 px-5 py-3 font-semibold hover:bg-slate-50">+ Manage topics</Link><Link href="/admin/students" className="rounded-lg border border-slate-300 px-5 py-3 font-semibold hover:bg-slate-50">Review students</Link></div></section></AdminGuard></AppShell>;
}
