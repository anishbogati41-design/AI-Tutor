"use client";

import { useQuery } from "@tanstack/react-query";

import { apiRequest } from "@/lib/api";
import type { User } from "@/types/user";

export function AdminGuard({ children }: { children: React.ReactNode }) {
  const user = useQuery({ queryKey: ["current-user"], queryFn: () => apiRequest<User>("/auth/me") });
  if (user.isPending) return <p className="text-slate-600">Checking administrator access…</p>;
  if (!user.data?.is_admin) return <section className="rounded-2xl border border-red-200 bg-red-50 p-8"><h1 className="text-2xl font-bold text-red-900">Administrator access required</h1><p className="mt-2 text-red-800">Sign in through the administrator login to manage content.</p></section>;
  return children;
}
