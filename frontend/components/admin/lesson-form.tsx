"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { ApiError, apiRequest } from "@/lib/api";
import type { LessonDetail, LessonSection, Topic } from "@/types/content";

type DraftSection = Pick<LessonSection, "section_type" | "title" | "content">;
const blankSection = (): DraftSection => ({ section_type: "INTRODUCTION", title: "", content: "" });

export function LessonForm({ lessonId }: { lessonId?: string }) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [subtopicId, setSubtopicId] = useState("");
  const [minutes, setMinutes] = useState("20");
  const [published, setPublished] = useState(false);
  const [sections, setSections] = useState<DraftSection[]>([blankSection()]);
  const topics = useQuery({ queryKey: ["topics"], queryFn: () => apiRequest<Topic[]>("/topics") });
  const lesson = useQuery({ queryKey: ["lesson", lessonId, "admin"], queryFn: () => apiRequest<LessonDetail>(`/lessons/${lessonId}`), enabled: Boolean(lessonId) });

  useEffect(() => {
    if (!lesson.data) return;
    setTitle(lesson.data.title); setDescription(lesson.data.description); setSubtopicId(String(lesson.data.subtopic_id)); setMinutes(String(lesson.data.estimated_minutes)); setPublished(lesson.data.is_published);
    setSections(lesson.data.sections.map(({ section_type, title: sectionTitle, content }) => ({ section_type, title: sectionTitle, content })));
  }, [lesson.data]);

  const save = useMutation({
    mutationFn: () => apiRequest<LessonDetail>(lessonId ? `/admin/lessons/${lessonId}` : "/admin/lessons", {
      method: lessonId ? "PUT" : "POST",
      body: JSON.stringify({ title, description, subtopic_id: Number(subtopicId), estimated_minutes: Number(minutes), is_published: published, sections: sections.map((section, position) => ({ ...section, position })) }),
    }),
    onSuccess: async (saved) => { await queryClient.invalidateQueries({ queryKey: ["lessons"] }); router.push(`/admin/lessons/${saved.id}`); },
  });
  const updateSection = (index: number, changes: Partial<DraftSection>) => setSections((items) => items.map((item, itemIndex) => itemIndex === index ? { ...item, ...changes } : item));
  const moveSection = (index: number, direction: -1 | 1) => setSections((items) => { const target = index + direction; if (target < 0 || target >= items.length) return items; const copy = [...items]; [copy[index], copy[target]] = [copy[target], copy[index]]; return copy; });

  if (lessonId && lesson.isPending) return <p className="text-slate-600">Loading lesson editor…</p>;
  if (lesson.error) return <p role="alert" className="rounded-xl bg-red-50 p-4 text-red-800">{lesson.error instanceof ApiError ? lesson.error.message : "Unable to load lesson"}</p>;
  return <form className="space-y-6" onSubmit={(event) => { event.preventDefault(); save.mutate(); }}><section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h2 className="text-xl font-bold">Lesson details</h2><div className="mt-5 grid gap-5 sm:grid-cols-2"><div><label htmlFor="lesson-title" className="mb-2 block text-sm font-semibold">Title</label><Input id="lesson-title" required value={title} onChange={(event) => setTitle(event.target.value)} /></div><div><label htmlFor="lesson-subtopic" className="mb-2 block text-sm font-semibold">Subtopic</label><select id="lesson-subtopic" required value={subtopicId} onChange={(event) => setSubtopicId(event.target.value)} className="min-h-11 w-full rounded-lg border border-slate-300 bg-white px-3"><option value="">Select a subtopic</option>{topics.data?.filter((topic) => topic.parent_topic_id !== null).map((topic) => <option key={topic.id} value={topic.id}>{topic.name}</option>)}</select></div><div className="sm:col-span-2"><label htmlFor="lesson-description" className="mb-2 block text-sm font-semibold">Description</label><textarea id="lesson-description" value={description} onChange={(event) => setDescription(event.target.value)} className="min-h-24 w-full rounded-lg border border-slate-300 p-3" /></div><div><label htmlFor="lesson-minutes" className="mb-2 block text-sm font-semibold">Estimated minutes</label><Input id="lesson-minutes" required type="number" min="1" max="1440" value={minutes} onChange={(event) => setMinutes(event.target.value)} /></div><label className="flex items-center gap-3 self-end pb-3 font-semibold"><input type="checkbox" checked={published} onChange={(event) => setPublished(event.target.checked)} className="size-5 accent-blue-700" /> Published</label></div></section><section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><div className="flex items-center justify-between gap-4"><h2 className="text-xl font-bold">Ordered sections</h2><button type="button" onClick={() => setSections((items) => [...items, blankSection()])} className="font-semibold text-blue-700">+ Add section</button></div><div className="mt-5 space-y-5">{sections.map((section, index) => <article key={index} className="rounded-xl border border-slate-200 p-5"><div className="flex flex-wrap items-center justify-between gap-3"><h3 className="font-bold">Section {index + 1}</h3><div className="flex gap-3"><button type="button" disabled={index === 0} onClick={() => moveSection(index, -1)} className="text-sm font-semibold text-blue-700 disabled:text-slate-300">Move up</button><button type="button" disabled={index === sections.length - 1} onClick={() => moveSection(index, 1)} className="text-sm font-semibold text-blue-700 disabled:text-slate-300">Move down</button><button type="button" onClick={() => setSections((items) => items.filter((_, itemIndex) => itemIndex !== index))} className="text-sm font-semibold text-red-700">Remove</button></div></div><div className="mt-4 grid gap-4 sm:grid-cols-2"><div><label className="mb-2 block text-sm font-semibold">Type</label><select value={section.section_type} onChange={(event) => updateSection(index, { section_type: event.target.value as DraftSection["section_type"] })} className="min-h-11 w-full rounded-lg border border-slate-300 bg-white px-3"><option value="INTRODUCTION">Introduction</option><option value="EXPLANATION">Explanation</option><option value="EXAMPLE">Example</option><option value="SUMMARY">Summary</option></select></div><div><label className="mb-2 block text-sm font-semibold">Title</label><Input required value={section.title} onChange={(event) => updateSection(index, { title: event.target.value })} /></div><div className="sm:col-span-2"><label className="mb-2 block text-sm font-semibold">Content</label><textarea required value={section.content} onChange={(event) => updateSection(index, { content: event.target.value })} className="min-h-32 w-full rounded-lg border border-slate-300 p-3" /></div></div></article>)}</div></section>{save.error && <p role="alert" className="rounded-xl bg-red-50 p-4 text-red-800">{save.error instanceof ApiError ? save.error.message : "Unable to save lesson"}</p>}<div className="flex gap-3"><Button type="submit" disabled={save.isPending || sections.length === 0}>{save.isPending ? "Saving…" : "Save lesson"}</Button><Button type="button" className="bg-slate-700 hover:bg-slate-900" onClick={() => router.push("/admin/lessons")}>Cancel</Button></div></form>;
}
