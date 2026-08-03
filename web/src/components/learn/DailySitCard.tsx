"use client";

import type { DailySitPick } from "@/lib/learn/progress";
import { Button } from "@/components/ui/button";

type DailySitCardProps = {
  sit: DailySitPick;
  onBegin: () => void;
  /** Optional realm id for themed artwork. */
  realmId?: string;
};

export function DailySitCard({ sit, onBegin }: DailySitCardProps) {
  const { track, step, stepIndex, kind, daysSince } = sit;
  const isRevisit = kind === "revisit";

  return (
    <section className="daily-sit mt-6 max-w-[var(--reading-measure)] border-t border-[rgb(240_201_121_/_0.14)] pt-5">
      <p className="passage-reading__meta">{isRevisit ? "Today's revisit" : "Today's sit"}</p>
      <p className="soft mt-2 text-sm leading-relaxed">
        {isRevisit
          ? `Return to a gate you marked ${daysSince != null ? `${daysSince} day${daysSince === 1 ? "" : "s"} ago` : "earlier"} · ${step.title}`
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
