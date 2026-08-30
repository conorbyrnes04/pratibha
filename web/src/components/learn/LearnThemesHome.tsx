"use client";

import { DailySitCard } from "@/components/learn/DailySitCard";
import { ThreadsConstellation } from "@/components/learn/ThreadsConstellation";
import { buttonVariants } from "@/components/ui/button";
import {
  nextUnfinishedBead,
  recommendedNextThreadId,
  startedThreadId,
  threadDoneCount,
  type DailySitPick,
  type ProgressMap,
  type CompletedAtMap,
} from "@/lib/learn/progress";
import { findThread, LEARNING_THREADS } from "@/lib/learningThreads";

type LearnThemesHomeProps = {
  progress: ProgressMap;
  completedAt: CompletedAtMap;
  hydrated: boolean;
  dailySit: DailySitPick | null;
  onOpenBead: (threadId: string, beadId: string) => void;
  onOpenThread: (threadId: string) => void;
  onOpenLineage: () => void;
  onBeginSit: (sit: DailySitPick) => void;
};

export function LearnThemesHome({
  progress,
  completedAt,
  hydrated,
  dailySit,
  onOpenBead,
  onOpenThread,
  onOpenLineage,
  onBeginSit,
}: LearnThemesHomeProps) {
  const anyThemeProgress = LEARNING_THREADS.some((t) => threadDoneCount(t, progress) > 0);
  const continueId = startedThreadId(progress, completedAt) || recommendedNextThreadId(progress);
  const heroThread = findThread(continueId) || LEARNING_THREADS[0];
  const heroBead = heroThread ? nextUnfinishedBead(heroThread, progress) || heroThread.steps[0] : undefined;
  const heroLabel = startedThreadId(progress, completedAt)
    ? "Continue this theme"
    : anyThemeProgress
      ? "Recommended next"
      : "Start here";
  const heroDone = heroThread ? threadDoneCount(heroThread, progress) : 0;
  const heroIdx = heroThread && heroBead ? heroThread.steps.findIndex((s) => s.id === heroBead.id) : 0;

  return (
    <div className="section-stack">
      <header className="library-header">
        <div className="library-header__body">
          <p className="passage-reading__meta">Guided study</p>
          <h1 className="library-header__title">Paths</h1>
          <p className="library-header__lede">
            Follow a spiritual theme across traditions. Each bead is one move in a claim.
            A lineage path waits under a bead when a tradition wants a longer sitting.
          </p>
        </div>
      </header>

      {heroThread && heroBead ? (
        <section className="mt-6">
          <button
            type="button"
            onClick={() => onOpenBead(heroThread.id, heroBead.id)}
            className="learn-continue group w-full max-w-[var(--reading-measure)] text-left"
          >
            <p className="passage-reading__meta">{heroLabel}</p>
            <div className="mt-2 flex flex-wrap items-end justify-between gap-3">
              <div className="min-w-0">
                <h2 className="text-2xl font-medium leading-tight tracking-[-0.02em] text-[rgb(250_237_205)] sm:text-[1.65rem]">
                  {heroThread.title}
                </h2>
                <p className="soft mt-1.5 text-sm leading-relaxed">
                  {startedThreadId(progress, completedAt)
                    ? `Next · Bead ${heroIdx + 1}: ${heroBead.tradition}`
                    : heroThread.thesis}
                </p>
              </div>
              <span className={buttonVariants({ size: "sm" })}>
                {startedThreadId(progress, completedAt) ? "Continue →" : "Begin →"}
              </span>
            </div>
            <p className="soft mt-3 font-sans text-[10px] uppercase tracking-[0.14em] text-stone-500">
              {heroDone}/{heroThread.steps.length} beads sat
            </p>
          </button>

          {dailySit ? <DailySitCard sit={dailySit} onBegin={() => onBeginSit(dailySit)} /> : null}
        </section>
      ) : null}

      <ThreadsConstellation
        progress={progress}
        hydrated={hydrated}
        onOpenBead={onOpenBead}
        onOpenThread={onOpenThread}
      />

      <p className="mt-10 max-w-[var(--reading-measure)]">
        <button
          type="button"
          onClick={onOpenLineage}
          className="font-sans text-[11px] uppercase tracking-[0.16em] text-stone-500 transition hover:text-amber-200/70"
        >
          Walk a lineage instead →
        </button>
      </p>
    </div>
  );
}
