'use client';

import Link from "next/link";
import { useT } from "@/components/LocaleProvider";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const t = useT();
  const message = error?.message || "Unknown error";
  const afterGoogle = /google|oauth|code|auth|sign in/i.test(message);

  return (
    <main className="mx-auto max-w-3xl px-4 py-12">
      <section className="card p-6">
        <h1 className="text-2xl text-amber-200">
          {afterGoogle ? t("error.googleAlmost") : t("error.somethingWrong")}
        </h1>
        <p className="soft mt-3">
          {afterGoogle ? t("error.googleAlmostLede") : t("error.somethingWrongLede")}
        </p>
        {process.env.NODE_ENV !== "production" ? (
          <p className="soft mt-2 text-xs">{message}</p>
        ) : null}
        <div className="mt-6 flex flex-wrap gap-3">
          <button onClick={reset} className="rounded-lg bg-amber-300 px-4 py-2 font-semibold text-slate-900">
            {t("common.tryAgain")}
          </button>
          <Link href="/" className="rounded-lg border border-amber-200/30 px-4 py-2 text-amber-100">
            {t("common.home")}
          </Link>
          <Link href="/login" className="rounded-lg border border-amber-200/30 px-4 py-2 text-amber-100">
            {t("auth.signIn")}
          </Link>
        </div>
      </section>
    </main>
  );
}
