"use client";

import type { LearningStepSpec, LearningTrack } from "@/lib/learningPaths";

type DailySitCardProps = {
  track: LearningTrack;
  step: LearningStepSpec;
  stepIndex: number;
  onBegin: () => void;
};

export function DailySitCard({ track, step, stepIndex, onBegin }: DailySitCardProps) {
  return (
    <section className="daily-sit card mt-5 border-amber-200/25 p-5 sm:p-6">
      <p className="eyebrow">Today&apos;s sit</p>
      <p className="soft mt-2 text-sm leading-relaxed">
        From your current path · Step {stepIndex + 1}: {step.title}
      </p>
      <p className="mt-4 leading-relaxed text-stone-200">{step.practice}</p>
      <button type="button" onClick={onBegin} className="btn-primary mt-4 px-5 py-2 text-sm">
        Begin practice →
      </button>
      <p className="soft mt-3 font-sans text-[10px] uppercase tracking-[0.14em] text-stone-500">
        {track.title}
      </p>
    </section>
  );
}
