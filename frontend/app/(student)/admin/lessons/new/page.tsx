import { AdminGuard } from "@/components/admin/admin-guard";
import { LessonForm } from "@/components/admin/lesson-form";
import { AppShell } from "@/components/app-shell";

export default function NewLessonPage() { return <AppShell><AdminGuard><header className="mb-8"><p className="text-sm font-semibold uppercase tracking-[0.16em] text-blue-700">Administration</p><h1 className="mt-2 text-3xl font-bold">New lesson</h1></header><LessonForm /></AdminGuard></AppShell>; }
