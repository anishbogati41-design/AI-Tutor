"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";

import { apiRequest, ApiError } from "@/lib/api";
import type { AccessibilityPreferences, User } from "@/types/user";

const navigation = [
  { href: "/dashboard", label: "Dashboard", icon: "▦" },
  { href: "/lessons", label: "Lessons", icon: "▤" },
  { href: "/practice", label: "Practice", icon: "✎" },
  { href: "/chat", label: "AI Tutor", icon: "◇" },
  { href: "/study-plan", label: "Study Plan", icon: "▣" },
  { href: "/profile", label: "Profile", icon: "○" },
];

const adminNavigation = [
  { href: "/admin/dashboard", label: "Dashboard", icon: "▦" },
  { href: "/admin/lessons", label: "Lessons", icon: "▤" },
  { href: "/admin/topics", label: "Topics", icon: "◫" },
  { href: "/admin/questions", label: "Questions", icon: "◇" },
  { href: "/admin/students", label: "Students", icon: "◎" },
  { href: "/dashboard", label: "Student view", icon: "←" },
  { href: "/profile", label: "Profile", icon: "○" },
];

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const router = useRouter();
  const queryClient = useQueryClient();
  const currentUser = useQuery({
    queryKey: ["current-user"],
    queryFn: () => apiRequest<User>("/auth/me"),
  });
  const logout = useMutation({
    mutationFn: () => apiRequest<void>("/auth/logout", { method: "POST" }),
    onSuccess: () => {
      queryClient.clear();
      router.replace("/login");
      router.refresh();
    },
  });
  const preferences = useMutation({
    mutationFn: (payload: AccessibilityPreferences) =>
      apiRequest<AccessibilityPreferences>("/users/me/preferences", {
        method: "PUT",
        body: JSON.stringify(payload),
      }),
    onSuccess: (saved) => {
      queryClient.setQueryData<User>(["current-user"], (user) =>
        user ? { ...user, ...saved } : user,
      );
    },
  });

  useEffect(() => {
    if (currentUser.error instanceof ApiError && currentUser.error.status === 401) {
      router.replace("/login");
    }
  }, [currentUser.error, router]);

  useEffect(() => {
    const root = document.documentElement;
    const user = currentUser.data;
    root.classList.toggle("font-large", user?.font_size === "large");
    root.classList.toggle("font-extra-large", user?.font_size === "extra-large");
    root.classList.toggle("readable-mode", Boolean(user?.readable_mode));
    root.classList.toggle("high-contrast", Boolean(user?.high_contrast));
    root.classList.toggle("dyslexia-mode", Boolean(user?.dyslexia_mode));
  }, [currentUser.data]);

  if (currentUser.isPending) {
    return <main className="p-8 text-slate-600">Loading your learning space…</main>;
  }
  if (currentUser.error instanceof ApiError && currentUser.error.status === 401) {
    return <main className="p-8 text-slate-600">Your session has ended. Redirecting to sign in…</main>;
  }
  if (!currentUser.data) {
    return <main className="p-8 text-red-700">Unable to load your account.</main>;
  }
  const user = currentUser.data;
  const items = user.is_admin ? adminNavigation : navigation;
  const updatePreferences = (changes: Partial<AccessibilityPreferences>) =>
    preferences.mutate({
      font_size: user.font_size,
      readable_mode: user.readable_mode,
      high_contrast: user.high_contrast,
      dyslexia_mode: user.dyslexia_mode,
      ...changes,
    });

  return (
    <div className="min-h-screen md:grid md:grid-cols-[240px_1fr]">
      <aside className="border-b border-slate-200 bg-white px-4 py-4 md:min-h-screen md:border-b-0 md:border-r md:px-5 md:py-7">
        <div className="flex items-center justify-between md:block">
          <Link href={user.is_admin ? "/admin/dashboard" : "/dashboard"} className="text-lg font-extrabold text-blue-800">
            ◆ {user.is_admin ? "Admin panel" : "EduAdapt"}
          </Link>
          <p className="text-sm text-slate-500 md:mt-2">
            {user.name}
          </p>
        </div>
        <nav className="mt-4 flex gap-2 overflow-x-auto pb-2 md:mt-8 md:block md:space-y-2 md:overflow-visible md:pb-0" aria-label="Main navigation">
          {items.map((item) => {
            const active =
              pathname === item.href ||
              (item.href.startsWith("/admin/") && pathname.startsWith(`${item.href}/`)) ||
              (item.href === "/lessons" &&
                pathname.startsWith("/lessons/") &&
                !pathname.endsWith("/practice")) ||
              (item.href === "/chat" && pathname.startsWith("/chat/"));

            return (
              <Link
                key={item.href}
                href={item.href}
                className={`flex items-center gap-3 rounded-lg px-4 py-3 text-sm font-semibold transition ${
                  active
                    ? "bg-blue-50 text-blue-800"
                    : "text-slate-600 hover:bg-slate-100 hover:text-slate-950"
                }`}
              >
                <span aria-hidden="true">{item.icon}</span>
                {item.label}
              </Link>
            );
          })}
        </nav>
        <button
          type="button"
          onClick={() => logout.mutate()}
          disabled={logout.isPending}
          className="mt-4 rounded-lg px-4 py-3 text-sm font-semibold text-red-700 hover:bg-red-50 disabled:opacity-60 md:mt-10 md:w-full md:text-left"
        >
          {logout.isPending ? "Signing out…" : "Sign out"}
        </button>
      </aside>
      <main className="min-w-0 px-5 py-8 md:px-10 md:py-10">{children}</main>
      <details className="fixed bottom-5 right-5 z-40 w-72 rounded-xl border border-slate-300 bg-white shadow-xl">
        <summary className="cursor-pointer list-none rounded-xl px-4 py-3 font-semibold text-blue-800">Accessibility</summary>
        <div className="space-y-3 border-t border-slate-200 p-4 text-sm">
          <button type="button" className="w-full rounded-lg border border-slate-300 px-3 py-2 text-left font-semibold" onClick={() => updatePreferences({ font_size: user.font_size === "default" ? "large" : user.font_size === "large" ? "extra-large" : "default" })}>Font size: {user.font_size.replace("-", " ")}</button>
          {[["Readable spacing", "readable_mode"], ["High contrast", "high_contrast"], ["Dyslexia-friendly font", "dyslexia_mode"]] .map(([label, key]) => <button key={key} type="button" className="flex w-full justify-between rounded-lg border border-slate-300 px-3 py-2 font-semibold" onClick={() => updatePreferences({ [key]: !user[key as keyof User] })}><span>{label}</span><span>{user[key as keyof User] ? "On" : "Off"}</span></button>)}
          {preferences.error && <p className="text-red-700">Unable to save preferences.</p>}
        </div>
      </details>
    </div>
  );
}
