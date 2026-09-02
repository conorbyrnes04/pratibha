"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { getVerse } from "@/lib/api";
import { generatedArtPool } from "@/lib/collectionImages";
import { ArtBackdrop } from "@/components/ArtImage";
import { TodayGate } from "@/components/TodayGate";
import { useAuth } from "@/components/AuthProvider";
import { useLearnProgress } from "@/hooks/useLearnProgress";
import { currentTrailSit } from "@/lib/learn/trail";
import { buttonVariants } from "@/components/ui/button";
import { CircleReadings } from "@/components/CircleReadings";
import { SanghaBoundary } from "@/components/SanghaBoundary";
import { useT } from "@/components/LocaleProvider";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import type { VerseItem } from "@/lib/types";

export default function HomePageClient() {
  const t = useT();
  const { configured, loading, user } = useAuth();
  const { progress, completedAt, hydrated } = useLearnProgress();
  const sit = useMemo(
    () => (hydrated ? currentTrailSit(progress, undefined, completedAt) : null),
    [hydrated, progress, completedAt],
  );
  const [verse, setVerse] = useState<VerseItem | null>(null);

  useEffect(() => {
    const passageId = sit?.step.passageId;
    if (!passageId) {
      setVerse(null);
      return;
    }
    let cancelled = false;
    getVerse(passageId)
      .then((item) => {
        if (!cancelled) setVerse(item);
      })
      .catch(() => {
        if (!cancelled) setVerse(null);
      });
    return () => {
      cancelled = true;
    };
  }, [sit?.step.passageId]);

  if (!hydrated) {
    return (
      <main className="page-shell page-shell--reading">
        <header className="passage-reading__header">
          <p className="passage-reading__meta">{t("today.meta")}</p>
          <h1 className="passage-reading__title">{t("today.opening")}</h1>
          <p className="passage-reading__deck">{t("today.openingLede")}</p>
        </header>
      </main>
    );
  }

  return (
    <main className="page-shell page-shell--reading">
      <div className="section-stack section-stack--measure">
        <header className="library-header">
          <div className="library-header__atmosphere" aria-hidden>
            <ArtBackdrop srcs={generatedArtPool("bg-hero")} variant="subtle" opacity={0.12} priority />
          </div>
          <div className="library-header__body">
            <p className="passage-reading__meta">{t("today.meta")}</p>
            <h1 className="library-header__title">{t("today.title")}</h1>
            <p className="library-header__lede">{t("today.lede")}</p>
          </div>
        </header>

        <SanghaBoundary>
          <CirclePulse />
        </SanghaBoundary>

        {sit ? (
          <>
            <TodayGate sit={sit} verse={verse} />
            {verse ? (
              <SanghaBoundary>
                <CircleReadings verseId={verse._id} daily />
              </SanghaBoundary>
            ) : null}
          </>
        ) : (
          <div className="passage-reading__nav">
            <Link href="/learn?path=essential" className={buttonVariants()}>
              {t("today.openPath")}
            </Link>
          </div>
        )}

        {configured && !loading && !user ? (
          <p className="today-gate__signin">
            {t("today.signInHint").split("{link}").map((part, index, parts) =>
              index < parts.length - 1 ? (
                <span key={index}>
                  {part}
                  <Link href="/login">{t("today.signInLink")}</Link>
                </span>
              ) : (
                <span key={index}>{part}</span>
              ),
            )}
          </p>
        ) : null}
      </div>
    </main>
  );
}

function CirclePulse() {
  const t = useT();
  const { user } = useAuth();
  const mine = useQuery(
    api.studentCommentaries.listMineOffered,
    CONVEX_ENABLED && user ? {} : "skip",
  );
  const first = mine?.[0];
  if (!first) return null;
  const line =
    first.replyCount === 1
      ? t("circle.pulseReplyOne", { title: first.verseTitle })
      : t("circle.pulseReplies", { count: first.replyCount, title: first.verseTitle });
  return (
    <p className="soft mt-2 text-sm leading-relaxed">
      {line}{" "}
      <Link href={`/circle/${first._id}`} className="text-amber-100 underline-offset-2 hover:underline">
        {t("circle.pulseOpen")}
      </Link>
    </p>
  );
}
