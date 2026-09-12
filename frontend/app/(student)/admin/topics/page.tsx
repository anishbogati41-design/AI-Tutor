"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { AdminGuard } from "@/components/admin/admin-guard";
import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ApiError, apiRequest } from "@/lib/api";
import type { Topic } from "@/types/content";

export default function AdminTopicsPage() {
  const queryClient = useQueryClient();
  const [editing, setEditing] = useState<Topic | null>(null);
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [parentId, setParentId] = useState("");
  const topics = useQuery({ queryKey: ["topics"], queryFn: () => apiRequest<Topic[]>("/topics") });
  const reset = () => { setEditing(null); setName(""); setDescription(""); setParentId(""); save.reset(); };
  const save = useMutation({ mutationFn: () => apiRequest<Topic>(editing ? `/admin/topics/${editing.id}` : "/admin/topics", { method: editing ? "PUT" : "POST", body: JSON.stringify({ name, description, parent_topic_id: parentId ? Number(parentId) : null }) }), onSuccess: async () => { await queryClient.invalidateQueries({ queryKey: ["topics"] }); reset(); } });
  const remove = useMutation({ mutationFn: (id: number) => apiRequest<void>(`/admin/topics/${id}`, { method: "DELETE" }), onSuccess: () => queryClient.invalidateQueries({ queryKey: ["topics"] }) });
  const edit = (topic: Topic) => { setEditing(topic); setName(topic.name); setDescription(topic.description); setParentId(topic.parent_topic_id ? String(topic.parent_topic_id) : ""); };
  return <AppShell><AdminGuard><header><p className="text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">Administration</p><h1 className="mt-2 text-3xl font-bold">Topics</h1><p className="mt-2 text-slate-600">Maintain the topic and subtopic hierarchy used by lessons.</p></header><div className="mt-8 grid gap-7 lg:grid-cols-[minmax(300px,0.8fr)_1fr]"><section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-xl font-bold">{editing ? "Edit topic" : "Add topic"}</h2><form className="mt-5 space-y-4" onSubmit={(event) => { event.preventDefault(); save.mutate(); }}><div><label htmlFor="topic-name" className="mb-2 block text-sm font-semibold">Name</label><Input id="topic-name" required value={name} onChange={(event) => setName(event.target.value)} /></div><div><label htmlFor="topic-parent" className="mb-2 block text-sm font-semibold">Parent topic</label><select id="topic-parent" value={parentId} onChange={(event) => setParentId(event.target.value)} className="min-h-11 w-full rounded-lg border border-slate-300 bg-white px-3"><option value="">Top-level topic</option>{topics.data?.filter((item) => item.id !== editing?.id).map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}</select></div><div><label htmlFor="topic-description" className="mb-2 block text-sm font-semibold">Description</label><textarea id="topic-description" value={description} onChange={(event) => setDescription(event.target.value)} className="min-h-24 w-full rounded-lg border border-slate-300 p-3" /></div>{save.error && <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-800">{save.error instanceof ApiError ? save.error.message : "Unable to save topic"}</p>}<div className="flex gap-3"><Button type="submit" disabled={save.isPending}>{save.isPending ? "Saving…" : "Save topic"}</Button>{editing && <Button type="button" className="bg-slate-700 hover:bg-slate-900" onClick={reset}>Cancel</Button>}</div></form></section><section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-xl font-bold">Topic hierarchy</h2>{topics.isPending && <p className="mt-4 text-slate-600">Loading topics…</p>}<div className="mt-4 space-y-3">{topics.data?.map((topic) => <article key={topic.id} className={`rounded-xl border border-slate-200 p-4 ${topic.parent_topic_id ? "ml-5" : ""}`}><div className="flex flex-wrap justify-between gap-4"><div><p className="text-xs font-bold uppercase tracking-wide text-blue-700">{topic.parent_topic_id ? "Subtopic" : "Topic"}</p><h3 className="mt-1 font-bold">{topic.name}</h3><p className="mt-1 text-sm text-slate-600">{topic.description || "No description"}</p></div><div className="flex gap-3"><button type="button" onClick={() => edit(topic)} className="text-sm font-semibold text-blue-700">Edit</button><button type="button" onClick={() => window.confirm(`Delete ${topic.name}?`) && remove.mutate(topic.id)} className="text-sm font-semibold text-red-700">Delete</button></div></div></article>)}</div>{remove.error && <p role="alert" className="mt-4 text-sm text-red-700">{remove.error instanceof ApiError ? remove.error.message : "Unable to delete topic"}</p>}</section></div></AdminGuard></AppShell>;
}
