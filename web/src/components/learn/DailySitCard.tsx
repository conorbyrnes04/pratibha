"use client";

import type { LearningStepSpec, LearningTrack } from "@/lib/learningPaths";
import { Button } from "@/components/ui/button";

type DailySitCardProps = {
  track: LearningTrack;
  step: LearningStepSpec;
  stepIndex: number;
  onBegin: () => void;
  /** Optional realm id for themed artwork. */
  realmId?: string;
};

export function DailySitCard({ track, step, stepIndex, onBegin }: DailySitCardProps) {
  return (
    <section className="daily-sit mt-6 max-w-[var(--reading-measure)] border-t border-[rgb(240_201_121_/_0.14)] pt-5">
      <p className="passage-reading__meta">Today&apos;s sit</p>
      <p className="soft mt-2 text-sm leading-relaxed">
        From your current path · Step {stepIndex + 1}: {step.title}
      </p>
      <p className="mt-3 max-w-[var(--reading-measure)] leading-relaxed text-stone-200">{step.practice}</p>
      <Button type="button" onClick={onBegin} className="mt-4">
        Begin practice →
      </Button>
      <p className="soft mt-3 font-sans text-[10px] uppercase tracking-[0.14em] text-stone-500">
        {track.title}
      </p>
    </section>
  );
}
