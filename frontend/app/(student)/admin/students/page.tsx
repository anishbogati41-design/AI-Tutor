"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useState } from "react";

import { AppShell } from "@/components/app-shell";
import { Input } from "@/components/ui/input";
import { ApiError, apiRequest } from "@/lib/api";
import type { AdminStudent } from "@/types/progress";

export default function AdminStudentsPage() {
  const [search, setSearch] = useState("");
  const students = useQuery({ queryKey: ["admin-students"], queryFn: () => apiRequest<AdminStudent[]>("/admin/students") });
  const filtered = students.data?.filter((student) => `${student.name} ${student.email}`.toLowerCase().includes(search.toLowerCase())) ?? [];
  return <AppShell><header><p className="text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">Administration</p><h1 className="mt-2 text-3xl font-bold">Students</h1></header><div className="mt-6 max-w-md"><Input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search by name or email" aria-label="Search students" /></div>{students.isPending && <p className="mt-8">Loading students…</p>}{students.error && <p role="alert" className="mt-8 rounded-xl bg-red-50 p-4 text-red-800">{students.error instanceof ApiError ? students.error.message : "Unable to load students"}</p>}<section className="mt-6 overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">{filtered.length === 0 && students.data ? <p className="p-6 text-slate-600">No matching students.</p> : filtered.map((student) => <article key={student.id} className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 p-5 last:border-0"><div><h2 className="font-bold">{student.name}</h2><p className="text-sm text-slate-600">{student.email}</p></div><Link href={`/admin/students/${student.id}`} className="font-semibold text-blue-700">View progress →</Link></article>)}</section></AppShell>;
}
