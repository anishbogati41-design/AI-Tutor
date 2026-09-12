"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";

import { AppShell } from "@/components/app-shell";
import { Button } from "@/components/ui/button";
import { ApiError, apiRequest, streamSse } from "@/lib/api";
import type {
  Conversation,
  ConversationDetail,
  ExplanationStyle,
} from "@/types/conversation";

export function ChatWorkspace({ conversationId }: { conversationId?: number }) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [message, setMessage] = useState("");
  const [style, setStyle] = useState<ExplanationStyle>("SIMPLE");
  const [streamedText, setStreamedText] = useState("");
  const [streamError, setStreamError] = useState("");
  const conversations = useQuery({
    queryKey: ["conversations"],
    queryFn: () => apiRequest<Conversation[]>("/conversations"),
  });
  const detail = useQuery({
    queryKey: ["conversation", conversationId],
    queryFn: () => apiRequest<ConversationDetail>(`/conversations/${conversationId}`),
    enabled: Boolean(conversationId),
  });
  const remove = useMutation({
    mutationFn: (id: number) =>
      apiRequest<void>(`/conversations/${id}`, { method: "DELETE" }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["conversations"] });
      router.replace("/chat");
    },
  });
  const send = useMutation({
    mutationFn: async (content: string) => {
      let activeId = conversationId;
      if (!activeId) {
        const created = await apiRequest<Conversation>("/conversations", {
          method: "POST",
          body: JSON.stringify({ title: content.slice(0, 80) }),
        });
        activeId = created.id;
        router.replace(`/chat/${activeId}`);
      }
      await apiRequest(`/conversations/${activeId}/messages`, {
        method: "POST",
        body: JSON.stringify({ content }),
      });
      await queryClient.invalidateQueries({ queryKey: ["conversation", activeId] });
      setStreamedText("");
      await streamSse(
        "/ai/chat",
        { conversation_id: activeId, message: content, explanation_style: style },
        (event, data) => {
          if (event === "delta") {
            const parsed = JSON.parse(data) as { text: string };
            setStreamedText((current) => current + parsed.text);
          } else if (event === "error") {
            const parsed = JSON.parse(data) as { detail: string };
            throw new Error(parsed.detail);
          }
        },
      );
      return activeId;
    },
    onSuccess: async (activeId) => {
      setMessage("");
      setStreamedText("");
      await queryClient.invalidateQueries({ queryKey: ["conversation", activeId] });
      await queryClient.invalidateQueries({ queryKey: ["conversations"] });
    },
    onError: (error) => {
      setStreamError(error instanceof Error ? error.message : "Unable to contact the AI tutor");
    },
  });

  const submit = (event: FormEvent) => {
    event.preventDefault();
    const content = message.trim();
    if (!content || send.isPending) return;
    setStreamError("");
    send.mutate(content);
  };

  return (
    <AppShell>
      <header>
        <p className="text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">AI Tutor</p>
        <h1 className="mt-2 text-3xl font-bold">Educational chat</h1>
        <p className="mt-2 text-slate-600">Ask about a lesson, concept, or study problem.</p>
      </header>
      <div className="mt-7 grid gap-6 lg:grid-cols-[250px_1fr]">
        <aside className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
          <Link href="/chat" className="flex min-h-11 items-center justify-center rounded-lg bg-blue-700 px-4 font-semibold text-white hover:bg-blue-800">+ New conversation</Link>
          <h2 className="mt-6 text-sm font-bold uppercase tracking-wide text-slate-500">Conversations</h2>
          {conversations.isPending && <p className="mt-3 text-sm text-slate-500">Loading…</p>}
          <div className="mt-3 space-y-2">
            {conversations.data?.map((conversation) => (
              <Link key={conversation.id} href={`/chat/${conversation.id}`} className={`block rounded-lg px-3 py-3 text-sm font-semibold ${conversation.id === conversationId ? "bg-blue-50 text-blue-800" : "hover:bg-slate-100"}`}>
                {conversation.title}
              </Link>
            ))}
          </div>
        </aside>
        <section className="flex min-h-[560px] flex-col rounded-2xl border border-slate-200 bg-white p-5 shadow-sm md:p-7">
          {detail.isPending && conversationId && <p className="text-slate-500">Loading conversation…</p>}
          {detail.error && <p role="alert" className="rounded-xl bg-red-50 p-4 text-red-800">{detail.error instanceof ApiError ? detail.error.message : "Unable to load conversation"}</p>}
          <div className="flex-1 space-y-4" aria-live="polite">
            {!conversationId && !send.isPending && <div className="rounded-xl bg-blue-50 p-5"><h2 className="font-bold text-blue-950">Start a conversation</h2><p className="mt-2 text-blue-900">Your messages are saved in this conversation. Other conversations are not used as memory.</p></div>}
            {detail.data?.messages.map((item) => (
              <article key={item.id} className={`max-w-3xl rounded-2xl p-4 leading-7 ${item.role === "USER" ? "ml-auto bg-blue-700 text-white" : "bg-slate-100 text-slate-900"}`}>
                <p className="mb-1 text-xs font-bold uppercase opacity-70">{item.role === "USER" ? "You" : "AI tutor"}</p>
                <p className="whitespace-pre-wrap">{item.content}</p>
              </article>
            ))}
            {send.isPending && streamedText && <article className="max-w-3xl rounded-2xl bg-slate-100 p-4 leading-7"><p className="mb-1 text-xs font-bold uppercase text-slate-500">AI tutor</p><p className="whitespace-pre-wrap">{streamedText}</p></article>}
            {send.isPending && !streamedText && <p className="text-sm text-slate-500">The tutor is thinking…</p>}
          </div>
          {(streamError || send.error) && <p role="alert" className="mt-4 rounded-xl bg-red-50 p-3 text-sm text-red-800">{streamError || (send.error instanceof ApiError ? send.error.message : "Unable to contact the AI tutor")}</p>}
          <form onSubmit={submit} className="mt-6 border-t border-slate-200 pt-5">
            <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
              <label htmlFor="explanation-style" className="text-sm font-semibold">Explanation style</label>
              <select id="explanation-style" value={style} onChange={(event) => setStyle(event.target.value as ExplanationStyle)} className="rounded-lg border border-slate-300 bg-white px-3 py-2 text-sm">
                <option value="SIMPLE">Simple</option><option value="DETAILED">Detailed</option><option value="STEP_BY_STEP">Step by step</option>
              </select>
            </div>
            <textarea value={message} onChange={(event) => setMessage(event.target.value)} maxLength={10000} rows={3} placeholder="Ask an educational question…" className="w-full rounded-xl border border-slate-300 p-3 outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100" />
            <div className="mt-3 flex items-center justify-between gap-3">
              {conversationId ? <button type="button" onClick={() => window.confirm("Delete this conversation?") && remove.mutate(conversationId)} className="text-sm font-semibold text-red-700">Delete conversation</button> : <span />}
              <Button type="submit" disabled={!message.trim() || send.isPending}>{send.isPending ? "Responding…" : "Send"}</Button>
            </div>
          </form>
        </section>
      </div>
    </AppShell>
  );
}
