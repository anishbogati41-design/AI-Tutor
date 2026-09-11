import Link from "next/link";

export function AuthCard({
  title,
  description,
  alternateHref,
  alternateLabel,
  children,
}: {
  title: string;
  description: string;
  alternateHref: string;
  alternateLabel: string;
  children: React.ReactNode;
}) {
  return (
    <main className="flex min-h-screen items-center justify-center px-5 py-12">
      <section className="w-full max-w-md rounded-2xl border border-slate-200 bg-white p-7 shadow-xl shadow-slate-200/50">
        <Link href="/" className="text-sm font-semibold text-blue-700">
          Adaptive Education
        </Link>
        <h1 className="mt-5 text-3xl font-bold tracking-tight">{title}</h1>
        <p className="mt-2 text-slate-600">{description}</p>
        <div className="mt-7">{children}</div>
        <Link
          href={alternateHref}
          className="mt-6 block text-center text-sm font-semibold text-blue-700 hover:text-blue-900"
        >
          {alternateLabel}
        </Link>
      </section>
    </main>
  );
}
