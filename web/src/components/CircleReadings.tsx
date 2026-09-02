"use client";

import Link from "next/link";
import { useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import type { Id } from "../../convex/_generated/dataModel";
import { useAuth } from "@/components/AuthProvider";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { formatCircleTime } from "@/lib/circleVerses";
import { circleOpeningFor } from "@/lib/circleOpenings";
import { CircleThread } from "@/components/CircleThread";
import { CircleSitButton, CircleWatchButton } from "@/components/CircleMarks";
import { buttonVariants } from "@/components/ui/button";
import { useLocale, useT } from "@/components/LocaleProvider";

export function CircleReadings({
  verseId,
  daily = false,
  embedded = false,
}: {
  verseId: string;
  daily?: boolean;
  embedded?: boolean;
}) {
  if (!CONVEX_ENABLED) return null;
  return <CircleReadingsInner verseId={verseId} daily={daily} embedded={embedded} />;
}

function CircleReadingsInner({
  verseId,
  daily,
  embedded,
}: {
  verseId: string;
  daily: boolean;
  embedded: boolean;
}) {
  const t = useT();
  const { bcp47 } = useLocale();
  const { user, loading } = useAuth();
  const meta = useQuery(api.studentCommentaries.circleMeta, { verseId });
  const offered = useQuery(api.studentCommentaries.listOffered, { verseId });
  if (meta === undefined) return null;

  const count = meta.offeredCount;
  const next = daily ? "/" : `/read/${encodeURIComponent(verseId)}`;

  return (
    <section id={embedded ? undefined : "circle"} className={embedded ? "mt-4" : "passage-commentary scroll-mt-28"}>
      {embedded ? null : (
        <>
          <div className="flex flex-wrap items-baseline justify-between gap-3">
            <h2 className="passage-layer__label">{t("circle.title")}</h2>
            <span className="inline-flex flex-wrap items-center gap-x-4 gap-y-1">
              <CircleWatchButton verseId={verseId} />
              <Link href="/circle" className="font-sans text-xs uppercase tracking-[0.16em] text-amber-200/70 hover:text-amber-100">
                {t("circle.backToCircle")}
              </Link>
            </span>
          </div>
          <p className="soft mt-2 text-sm leading-relaxed">
            {t("circle.ledeVerse")}
            {count ? ` · ${count === 1 ? t("circle.offeredOne") : t("circle.offeredCount", { count })}` : ""}
          </p>
        </>
      )}
      {offered === undefined ? (
        <p className="soft mt-4 text-sm">{t("circle.opening")}</p>
      ) : offered.length === 0 ? (
        <EmptyVerseCircle verseId={verseId} loading={loading} user={Boolean(user)} next={next} embedded={embedded} />
      ) : (
        <ul className="mt-6 space-y-8">
          {offered.map((reading) => (
            <li key={reading._id} className="circle-reading">
              <p className="font-sans text-xs uppercase tracking-[0.16em] text-amber-100/80">
                {reading.mine ? t("circle.yours") : reading.displayName}
                <span className="ms-2 font-normal normal-case tracking-normal text-stone-500">
                  {formatCircleTime(reading.lastActivityAt, bcp47)}
                </span>
              </p>
              <p className="reading-prose mt-2 whitespace-pre-wrap text-[0.95rem] leading-relaxed">{reading.body}</p>
              <div className="mt-2 flex flex-wrap items-center gap-x-4 gap-y-1">
                <p className="font-sans text-[11px] uppercase tracking-[0.14em] text-stone-500">
                  {reading.replyCount === 1
                    ? t("circle.replyOne")
                    : reading.replyCount > 1
                      ? t("circle.replies", { count: reading.replyCount })
                      : t("circle.noReplies")}
                </p>
                {!reading.mine ? (
                  <CircleSitButton commentaryId={reading._id as Id<"student_commentaries">} />
                ) : null}
                <Link
                  href={`/circle/${reading._id}`}
                  className="font-sans text-[11px] uppercase tracking-[0.14em] text-amber-200/70 hover:text-amber-100"
                >
                  {t("circle.openThread")}
                </Link>
              </div>
              <CircleThread
                commentaryId={reading._id as Id<"student_commentaries">}
                verseId={verseId}
                compact
                showGuestPrompt={false}
              />
            </li>
          ))}
        </ul>
      )}
      {!loading && !user && offered && offered.length > 0 ? (
        <p className="soft mt-6 text-sm">
          <Link href={`/login?next=${encodeURIComponent(next)}`} className={buttonVariants({ size: "sm" })}>
            {t("circle.signInToReply")}
          </Link>
        </p>
      ) : null}
    </section>
  );
}

function EmptyVerseCircle({
  verseId,
  loading,
  user,
  next,
  embedded = false,
}: {
  verseId: string;
  loading: boolean;
  user: boolean;
  next: string;
  embedded?: boolean;
}) {
  const t = useT();
  const opening = circleOpeningFor(verseId);
  const cta = embedded ? null : loading || user ? (
    <Link href="#commentary" className="text-amber-100 underline-offset-2 hover:underline">
      {t("circle.writeYours")}
    </Link>
  ) : (
    <Link href={`/login?next=${encodeURIComponent(next)}`} className={buttonVariants({ size: "sm" })}>
      {t("circle.signInToJoin")}
    </Link>
  );

  if (opening) {
    return (
      <article className="card mt-4 p-5 sm:p-6">
        <p className="layer-heading">{t("circle.houseOpening")}</p>
        <p className="mt-3 leading-relaxed text-stone-200">{opening.body}</p>
        <p className="soft mt-4 text-sm">{cta}</p>
      </article>
    );
  }

  return (
    <p className="soft mt-4 text-sm leading-relaxed">
      {t("circle.emptyVerse")} {cta}
    </p>
  );
}
