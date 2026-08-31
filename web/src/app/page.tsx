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
import type { VerseItem } from "@/lib/types";

export default function Home() {
  const { configured, loading, user } = useAuth();
  const signedIn = !configured || Boolean(user);
  const { progress, hydrated } = useLearnProgress();
  const sit = useMemo(() => (hydrated ? currentTrailSit(progress) : null), [hydrated, progress]);
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
          <p className="passage-reading__meta">Today</p>
          <h1 className="passage-reading__title">Opening today&apos;s gate…</h1>
          <p className="passage-reading__deck">One step on the path. A passage. One practice.</p>
        </header>
      </main>
    );
  }

  return (
    <main className="page-shell page-shell--reading">
      <div className="section-stack">
        <header className="library-header">
          <div className="library-header__atmosphere" aria-hidden>
            <ArtBackdrop srcs={generatedArtPool("bg-hero")} variant="subtle" opacity={0.12} priority />
          </div>
          <div className="library-header__body">
            <p className="passage-reading__meta">Today</p>
            <h1 className="library-header__title">A walk through world wisdom</h1>
            <p className="library-header__lede">
              Pratibha is a guided path, not a pile of books. Each day opens one gate: a
              teaching, a canonical passage, and one practice. Finish the gate and the next
              step draws itself.
            </p>
          </div>
        </header>

        {sit ? (
          <>
            <TodayGate sit={sit} verse={verse} />
            {signedIn && verse ? (
              <SanghaBoundary>
                <CircleReadings verseId={verse._id} daily />
              </SanghaBoundary>
            ) : null}
          </>
        ) : (
          <div className="passage-reading__nav">
            <Link href="/learn?path=essential" className={buttonVariants()}>
              Open the path
            </Link>
          </div>
        )}

        {configured && !loading && !user ? (
          <p className="today-gate__signin">
            The path is open.{" "}
            <Link href="/login">Sign in</Link> to keep a journal and carry progress across devices.
          </p>
        ) : null}
      </div>
    </main>
  );
}
