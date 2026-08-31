'use client';

import Link from "next/link";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const message = error?.message || "Unknown error";
  const afterGoogle = /google|oauth|code|auth|sign in/i.test(message);

  return (
    <main className="mx-auto max-w-3xl px-4 py-12">
      <section className="card p-6">
        <h1 className="text-2xl text-amber-200">
          {afterGoogle ? "Google sign-in almost made it" : "Something went wrong"}
        </h1>
        <p className="soft mt-3">
          {afterGoogle
            ? "Your Google account connected. Reload home to open the session — if it is still blank, sign in again from /login."
            : "The page hit an unexpected issue. Your data is safe; this is usually a temporary loading problem."}
        </p>
        <p className="soft mt-2 text-xs">{message}</p>
        <div className="mt-6 flex flex-wrap gap-3">
          <button onClick={reset} className="rounded-lg bg-amber-300 px-4 py-2 font-semibold text-slate-900">
            Try again
          </button>
          <Link href="/" className="rounded-lg border border-amber-200/30 px-4 py-2 text-amber-100">
            Home
          </Link>
          <Link href="/login" className="rounded-lg border border-amber-200/30 px-4 py-2 text-amber-100">
            Sign in
          </Link>
        </div>
      </section>
    </main>
  );
}
