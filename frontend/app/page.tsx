import Link from "next/link";

import { ButtonLink } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="mx-auto flex min-h-screen max-w-5xl items-center px-6 py-16">
      <section className="max-w-2xl">
        <p className="mb-4 text-sm font-semibold uppercase tracking-[0.2em] text-blue-700">
          Adaptive Education
        </p>
        <h1 className="text-5xl font-bold leading-tight tracking-tight text-slate-950">
          Learn at the pace that fits you.
        </h1>
        <p className="mt-6 max-w-xl text-lg leading-8 text-slate-600">
          Build understanding through structured lessons, adaptive practice,
          progress insights, and focused support.
        </p>
        <div className="mt-9 flex flex-wrap gap-3">
          <ButtonLink href="/register">Create account</ButtonLink>
          <Link
            href="/login"
            className="rounded-lg border border-slate-300 bg-white px-5 py-3 font-semibold text-slate-800 shadow-sm hover:bg-slate-50"
          >
            Sign in
          </Link>
        </div>
      </section>
    </main>
  );
}
