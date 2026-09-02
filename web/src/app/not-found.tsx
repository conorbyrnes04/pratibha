'use client';

import Link from "next/link";
import { useT } from "@/components/LocaleProvider";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function NotFound() {
  const t = useT();
  return (
    <main className="mx-auto max-w-3xl px-4 py-16">
      <section className="card p-8 text-center">
        <p className="passage-reading__meta">{t("notFound.meta")}</p>
        <h1 className="mt-2 text-3xl text-amber-100">{t("notFound.title")}</h1>
        <p className="soft mx-auto mt-3 max-w-md leading-relaxed">{t("notFound.lede")}</p>
        <div className="mt-6 flex flex-wrap justify-center gap-3">
          <Link href="/read" className={cn(buttonVariants())}>
            {t("notFound.library")}
          </Link>
          <Link href="/" className={cn(buttonVariants({ variant: "secondary" }))}>
            {t("common.home")}
          </Link>
        </div>
      </section>
    </main>
  );
}
