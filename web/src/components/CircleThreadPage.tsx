"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import type { Id } from "../../convex/_generated/dataModel";
import { CircleThread } from "@/components/CircleThread";
import { CircleSitButton } from "@/components/CircleMarks";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { formatCircleTime } from "@/lib/circleVerses";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useLocale, useT } from "@/components/LocaleProvider";

function looksLikeCommentaryId(id: string | undefined): boolean {
  return Boolean(id && /^[a-z0-9]{16,}$/i.test(id));
}

export function CircleThreadPage() {
  const t = useT();
  const { bcp47 } = useLocale();
  const params = useParams<{ id: string }>();
  const rawId = params.id;
  const valid = looksLikeCommentaryId(rawId);
  const id = (valid ? rawId : undefined) as Id<"student_commentaries"> | undefined;
  const reading = useQuery(
    api.studentCommentaries.getOffered,
    CONVEX_ENABLED && id ? { id } : "skip",
  );

  if (!CONVEX_ENABLED) {
    return (
      <main className="page-shell page-shell--reading">
        <p className="soft">{t("circle.unavailable")}</p>
      </main>
    );
  }

  if (!valid || reading === null) {
    return (
      <main className="page-shell page-shell--reading">
        <p className="passage-reading__meta">{t("circle.meta")}</p>
        <h1 className="library-header__title">{t("circle.notFound")}</h1>
        <Link href="/circle" className={cn(buttonVariants({ variant: "secondary" }), "mt-6")}>
          {t("circle.backToCircle")}
        </Link>
      </main>
    );
  }

  if (reading === undefined) {
    return (
      <main className="page-shell page-shell--reading">
        <p className="soft">{t("circle.opening")}</p>
      </main>
    );
  }

  return (
    <main className="page-shell page-shell--reading">
      <nav className="passage-reading__crumb" aria-label={t("reader.breadcrumb")}>
        <Link href="/circle">{t("circle.title")}</Link>
        <span aria-hidden="true"> · </span>
        <Link href={`/read/${encodeURIComponent(reading.verseId)}`}>{reading.verseTitle}</Link>
      </nav>
      <header className="mt-6">
        <p className="passage-reading__meta">{t("circle.thread")}</p>
        <h1 className="library-header__title">{reading.verseTitle}</h1>
        <p className="mt-3 font-sans text-xs uppercase tracking-[0.16em] text-amber-100/80">
          {reading.mine ? t("circle.yours") : reading.displayName}
          <span className="ms-2 font-normal normal-case tracking-normal text-stone-500">
            {formatCircleTime(reading.createdAt, bcp47)}
          </span>
        </p>
      </header>
      <p className="reading-prose mt-8 whitespace-pre-wrap text-[1.05rem] leading-relaxed">{reading.body}</p>
      <div className="mt-6 flex flex-wrap items-center gap-2">
        {!reading.mine ? <CircleSitButton commentaryId={reading._id} /> : null}
        <Link href={`/read/${encodeURIComponent(reading.verseId)}#circle`} className={cn(buttonVariants({ variant: "secondary", size: "sm" }))}>
          {t("circle.readVerse")}
        </Link>
        <Link href={`/read/${encodeURIComponent(reading.verseId)}#commentary`} className={cn(buttonVariants({ variant: "ghost", size: "sm" }))}>
          {t("circle.offerOnVerse")}
        </Link>
      </div>
      <section className="mt-10 border-t border-amber-200/15 pt-8">
        <h2 className="passage-layer__label">
          {reading.replyCount === 1
            ? t("circle.replyOne")
            : reading.replyCount > 0
              ? t("circle.replies", { count: reading.replyCount })
              : t("circle.noReplies")}
        </h2>
        <CircleThread commentaryId={reading._id} verseId={reading.verseId} loginNext={`/circle/${reading._id}`} />
      </section>
    </main>
  );
}
