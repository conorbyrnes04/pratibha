"use client";

import { findBead, findThread } from "@/lib/learningThreads";
import type { DailySitPick } from "@/lib/learn/progress";
import { Button } from "@/components/ui/button";

type DailySitCardProps = {
  sit: DailySitPick;
  onBegin: () => void;
  /** Optional realm id for themed artwork. */
  realmId?: string;
};

export function DailySitCard({ sit, onBegin }: DailySitCardProps) {
  const isRevisit = sit.kind === "revisit";

  if (sit.mode === "thread") {
    const thread = findThread(sit.threadId);
    const bead = thread ? findBead(thread, sit.beadId) : undefined;
    if (!thread || !bead) return null;
    return (
      <section className="daily-sit mt-6 max-w-[var(--reading-measure)] border-t border-[rgb(240_201_121_/_0.14)] pt-5">
        <p className="passage-reading__meta">{isRevisit ? "Today's revisit" : "Today's sit"}</p>
        <p className="soft mt-2 text-sm leading-relaxed">
          {isRevisit
            ? `Return to a bead you sat ${sit.daysSince != null ? `${sit.daysSince} day${sit.daysSince === 1 ? "" : "s"} ago` : "earlier"} · ${bead.tradition}`
            : `Next move on ${thread.title} · ${bead.tradition}`}
        </p>
        <p className="mt-3 max-w-[var(--reading-measure)] leading-relaxed text-stone-200">{bead.move}</p>
        <Button type="button" onClick={onBegin} className="mt-4">
          {isRevisit ? "Revisit bead →" : "Sit this bead →"}
        </Button>
        <p className="soft mt-3 font-sans text-[10px] uppercase tracking-[0.14em] text-stone-500">
          {thread.title}
          {isRevisit ? " · spaced return" : " · theme"}
        </p>
      </section>
    );
  }

  const { track, step, stepIndex } = sit;
  return (
    <section className="daily-sit mt-6 max-w-[var(--reading-measure)] border-t border-[rgb(240_201_121_/_0.14)] pt-5">
      <p className="passage-reading__meta">{isRevisit ? "Today's revisit" : "Today's sit"}</p>
      <p className="soft mt-2 text-sm leading-relaxed">
        {isRevisit
          ? `Return to a gate you marked ${sit.daysSince != null ? `${sit.daysSince} day${sit.daysSince === 1 ? "" : "s"} ago` : "earlier"} · ${step.title}`
          : `From your current path · Step ${stepIndex + 1}: ${step.title}`}
      </p>
      <p className="mt-3 max-w-[var(--reading-measure)] leading-relaxed text-stone-200">{step.practice}</p>
      <Button type="button" onClick={onBegin} className="mt-4">
        {isRevisit ? "Revisit practice →" : "Begin practice →"}
      </Button>
      <p className="soft mt-3 font-sans text-[10px] uppercase tracking-[0.14em] text-stone-500">
        {track.title}
        {isRevisit ? " · spaced return" : ""}
      </p>
    </section>
  );
}
