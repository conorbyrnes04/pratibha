"use client";

import { InkGlyph } from "@/components/InkGlyph";
import { Button } from "@/components/ui/button";
import { threadDoneCount, threadKey, type ProgressMap } from "@/lib/learn/progress";
import { pathStepTitleForBead, type LearningThread } from "@/lib/learningThreads";
import { sumiGlyph } from "@/lib/sumiGlyphs";

type LearnThreadJourneyProps = {
  thread: LearningThread;
  progress: ProgressMap;
  onOpenBead: (threadId: string, beadId: string) => void;
  onBackHome: () => void;
};

export function LearnThreadJourney({
  thread,
  progress,
  onOpenBead,
  onBackHome,
}: LearnThreadJourneyProps) {
  const done = threadDoneCount(thread, progress);
  const total = thread.steps.length;

  return (
    <div className="section-stack">
      <header className="library-header">
        <div className="library-header__body">
          <button
            type="button"
            onClick={onBackHome}
            className="font-sans text-[10px] uppercase tracking-[0.16em] text-amber-200/55 hover:text-amber-100"
          >
            ← Themes
          </button>
          <p className="passage-reading__meta mt-4">Theme</p>
          <h1 className="library-header__title">{thread.title}</h1>
          <p className="library-header__lede">{thread.thesis}</p>
          <p className="mt-5 max-w-[var(--reading-measure)] leading-relaxed text-stone-300">{thread.arc}</p>
          <p className="mt-4 font-sans text-xs uppercase tracking-[0.16em] text-emerald-200/70">
            {done}/{total} beads sat
          </p>
        </div>
      </header>

      <ol className="mt-8 max-w-[var(--reading-measure)]">
        {thread.steps.map((bead, i) => {
          const sat = !!progress[threadKey(thread.id, bead.id)];
          const gateTitle = pathStepTitleForBead(bead);
          const prev = i > 0 ? thread.steps[i - 1] : null;
          return (
            <li key={bead.id} className="border-t border-[rgb(240_201_121_/_0.12)] py-6">
              <button type="button" onClick={() => onOpenBead(thread.id, bead.id)} className="w-full text-left">
                <div className="flex items-start gap-3">
                  <span
                    className={`mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
                      sat ? "bg-emerald-300/20" : "bg-amber-100/10"
                    }`}
                  >
                    <InkGlyph
                      glyph={bead.glyphSlug ?? sumiGlyph(bead.tradition)}
                      size="sm"
                      state={sat ? "recognized" : "arising"}
                    />
                  </span>
                  <div className="min-w-0">
                    <p className="font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/60">
                      Bead {i + 1}
                      {sat ? " · sat" : ""} · {bead.tradition}
                      {gateTitle ? ` · ${gateTitle}` : ""}
                    </p>
                    <p className="mt-2 text-base leading-relaxed text-stone-100">{bead.move}</p>
                    {prev ? (
                      <p className="soft mt-2 text-sm leading-relaxed">
                        After {prev.tradition}: {bead.homology}
                      </p>
                    ) : (
                      <p className="soft mt-2 text-sm leading-relaxed">{bead.homology}</p>
                    )}
                    <span className="mt-3 inline-block font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/50">
                      Sit this bead →
                    </span>
                  </div>
                </div>
              </button>
            </li>
          );
        })}
      </ol>

      <div className="mt-6 max-w-[var(--reading-measure)] border-t border-[rgb(240_201_121_/_0.12)] pt-5">
        <p className="passage-layer__label">Thread practice</p>
        <p className="mt-2 leading-relaxed text-stone-200">{thread.practice}</p>
        <Button type="button" variant="secondary" size="sm" className="mt-4" onClick={onBackHome}>
          Back to themes
        </Button>
      </div>
    </div>
  );
}
