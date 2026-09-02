"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import { ArtBackdrop } from "@/components/ArtImage";
import { Glyph } from "@/components/Glyph";
import { CircleOfferForm } from "@/components/CircleOfferForm";
import { CircleSitButton, CircleWatchButton } from "@/components/CircleMarks";
import type { Id } from "../../convex/_generated/dataModel";
import { useAuth } from "@/components/AuthProvider";
import { useLearnProgress } from "@/hooks/useLearnProgress";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { generatedArtPool } from "@/lib/collectionImages";
import { getVerse } from "@/lib/api";
import {
  excerptReading,
  FEATURED_CIRCLE_DOORS,
  formatCircleTime,
} from "@/lib/circleVerses";
import { CIRCLE_OPENINGS, featuredDoorLabel } from "@/lib/circleOpenings";
import { currentTrailSit } from "@/lib/learn/trail";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useLocale, useT } from "@/components/LocaleProvider";
import type { VerseItem } from "@/lib/types";

export function CircleHub() {
  const t = useT();
  const { bcp47 } = useLocale();
  const { user, loading } = useAuth();
  const { progress, completedAt, hydrated } = useLearnProgress();
  const sit = useMemo(
    () => (hydrated ? currentTrailSit(progress, undefined, completedAt) : null),
    [hydrated, progress, completedAt],
  );
  const [todayVerse, setTodayVerse] = useState<VerseItem | null>(null);
  const recent = useQuery(api.studentCommentaries.listRecent, CONVEX_ENABLED ? {} : "skip");
  const watched = useQuery(api.circleWatches.mine, CONVEX_ENABLED && user ? {} : "skip");

  useEffect(() => {
    const passageId = sit?.step.passageId;
    if (!passageId) {
      setTodayVerse(null);
      return;
    }
    let cancelled = false;
    getVerse(passageId)
      .then((item) => {
        if (!cancelled) setTodayVerse(item);
      })
      .catch(() => {
        if (!cancelled) setTodayVerse(null);
      });
    return () => {
      cancelled = true;
    };
  }, [sit?.step.passageId]);

  const todayId = sit?.step.passageId;
  const todayTitle =
    todayVerse?.title ||
    (todayId ? featuredDoorLabel(todayId) : undefined) ||
    sit?.step.title ||
    "";

  const watchedDoors = (watched ?? [])
    .filter((id) => !FEATURED_CIRCLE_DOORS.some((door) => door.id === id))
    .slice(0, 8)
    .map((id) => ({ id, label: featuredDoorLabel(id) || id }));

  return (
    <main className="page-shell page-shell--reading">
      <header className="library-header">
        <div className="library-header__atmosphere" aria-hidden>
          <ArtBackdrop srcs={generatedArtPool("bg-hero")} variant="subtle" opacity={0.12} priority />
        </div>
        <div className="library-header__body">
          <p className="passage-reading__meta">{t("circle.meta")}</p>
          <h1 className="library-header__title">{t("circle.title")}</h1>
          <p className="library-header__lede">{t("circle.lede")}</p>
          {!user && !loading ? (
            <Link href="/login?next=/circle" className={cn(buttonVariants({ variant: "secondary" }), "mt-4")}>
              {t("circle.signInToJoin")}
            </Link>
          ) : null}
        </div>
      </header>

      {todayId ? (
        <section className="mt-10">
          <p className="passage-layer__label">{t("circle.todaySits")}</p>
          <div className="mt-2 flex flex-wrap items-baseline justify-between gap-3">
            <h2 className="text-2xl text-amber-100">
              <Link href={`/read/${encodeURIComponent(todayId)}#circle`} className="hover:underline">
                {todayTitle}
              </Link>
            </h2>
            {CONVEX_ENABLED ? <CircleWatchButton verseId={todayId} /> : null}
          </div>
          <p className="soft mt-2 max-w-xl text-sm leading-relaxed">{t("circle.todaySitsLede")}</p>
          {CONVEX_ENABLED ? (
            <div className="mt-4">
              <CircleOfferForm
                verseId={todayId}
                verseTitle={todayTitle}
                compact
                loginNext="/circle"
              />
            </div>
          ) : null}
        </section>
      ) : null}

      <section className="mt-12">
        <div className="flex items-center gap-3">
          <Glyph name="circle" size="sm" />
          <h2 className="passage-layer__label">{t("circle.doors")}</h2>
        </div>
        <p className="soft mt-2 max-w-xl text-sm leading-relaxed">{t("circle.doorsLede")}</p>
        <ul className="circle-doors mt-5">
          {FEATURED_CIRCLE_DOORS.map((door) => (
            <li key={door.id}>
              <Link
                href={`/read/${encodeURIComponent(door.id)}#circle`}
                className={`circle-door${door.id === todayId ? " circle-door--today" : ""}`}
              >
                {door.label}
              </Link>
            </li>
          ))}
        </ul>
        {watchedDoors.length > 0 ? (
          <>
            <p className="soft mt-6 font-sans text-xs uppercase tracking-[0.16em]">{t("circle.watched")}</p>
            <ul className="circle-doors mt-3">
              {watchedDoors.map((door) => (
                <li key={door.id}>
                  <Link href={`/read/${encodeURIComponent(door.id)}#circle`} className="circle-door circle-door--watching">
                    {door.label}
                  </Link>
                </li>
              ))}
            </ul>
          </>
        ) : null}
      </section>

      <section className="mt-12">
        <h2 className="passage-layer__label">{t("circle.recent")}</h2>
        {!CONVEX_ENABLED ? (
          <p className="soft mt-4 text-sm">{t("circle.unavailable")}</p>
        ) : recent === undefined ? (
          <p className="soft mt-4 text-sm">{t("circle.opening")}</p>
        ) : recent.length === 0 ? (
          <div className="mt-6">
            <p className="text-xl text-amber-100">{t("circle.houseOpenings")}</p>
            <p className="soft mt-2 max-w-xl text-sm leading-relaxed">{t("circle.houseOpeningsLede")}</p>
            <ul className="mt-6 space-y-4">
              {CIRCLE_OPENINGS.map((opening) => (
                <li key={opening.id}>
                  <article className="card p-5 sm:p-6">
                    <p className="layer-heading">{t("circle.houseOpening")}</p>
                    <h3 className="mt-2 text-2xl text-amber-100">
                      <Link href={`/read/${encodeURIComponent(opening.id)}#circle`} className="hover:underline">
                        {opening.label}
                      </Link>
                    </h3>
                    <p className="mt-3 leading-relaxed text-stone-200">{opening.body}</p>
                    <Link
                      href={`/read/${encodeURIComponent(opening.id)}#commentary`}
                      className={cn(buttonVariants({ size: "sm" }), "mt-4")}
                    >
                      {t("circle.writeYours")}
                    </Link>
                  </article>
                </li>
              ))}
            </ul>
          </div>
        ) : (
          <ul className="mt-6 space-y-4">
            {recent.map((reading) => (
              <li key={reading._id}>
                <article className="card p-5 sm:p-6">
                  <p className="layer-heading">
                    {reading.mine ? t("circle.yours") : reading.displayName}
                    <span className="ms-2 font-normal text-stone-500">
                      {formatCircleTime(reading.lastActivityAt, bcp47)}
                    </span>
                  </p>
                  <h3 className="mt-2 text-2xl text-amber-100">
                    <Link href={`/read/${encodeURIComponent(reading.verseId)}#circle`} className="hover:underline">
                      {reading.verseTitle}
                    </Link>
                  </h3>
                  <p className="mt-3 whitespace-pre-wrap leading-relaxed text-stone-200">
                    {excerptReading(reading.body)}
                  </p>
                  <div className="mt-4 flex flex-wrap items-center gap-2">
                    <Link href={`/circle/${reading._id}`} className={cn(buttonVariants({ size: "sm" }))}>
                      {t("circle.openThread")}
                    </Link>
                    <Link
                      href={`/read/${encodeURIComponent(reading.verseId)}#circle`}
                      className={cn(buttonVariants({ variant: "secondary", size: "sm" }))}
                    >
                      {t("circle.readVerse")}
                    </Link>
                    <span className="self-center font-sans text-[11px] uppercase tracking-[0.14em] text-stone-500">
                      {reading.replyCount === 1
                        ? t("circle.replyOne")
                        : reading.replyCount > 0
                          ? t("circle.replies", { count: reading.replyCount })
                          : t("circle.noReplies")}
                    </span>
                    {!reading.mine ? (
                      <CircleSitButton commentaryId={reading._id as Id<"student_commentaries">} />
                    ) : reading.sitCount > 0 ? (
                      <span className="self-center font-sans text-[11px] uppercase tracking-[0.14em] text-stone-500">
                        {reading.sitCount === 1
                          ? t("circle.satOne")
                          : t("circle.satCount", { count: reading.sitCount })}
                      </span>
                    ) : null}
                  </div>
                </article>
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}
