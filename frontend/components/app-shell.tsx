"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect } from "react";

import { apiRequest, ApiError } from "@/lib/api";
import type { User } from "@/types/user";

const navigation = [
  { href: "/lessons", label: "Lessons", icon: "▤" },
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
  if (!currentUser.data) {
    return <main className="p-8 text-red-700">Unable to load your account.</main>;
  }

  return (
    <div className="min-h-screen md:grid md:grid-cols-[240px_1fr]">
      <aside className="border-b border-slate-200 bg-white px-4 py-4 md:min-h-screen md:border-b-0 md:border-r md:px-5 md:py-7">
        <div className="flex items-center justify-between md:block">
          <Link href="/lessons" className="text-lg font-extrabold text-blue-800">
            ◆ EduAdapt
          </Link>
          <p className="text-sm text-slate-500 md:mt-2">
            {currentUser.data.name}
          </p>
        </div>
        <nav className="mt-4 flex gap-2 md:mt-8 md:block md:space-y-2" aria-label="Main navigation">
          {navigation.map((item) => {
            const active =
              pathname === item.href ||
              (item.href === "/lessons" && pathname.startsWith("/lessons/"));
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
    </div>
  );
}
