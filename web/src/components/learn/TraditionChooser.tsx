"use client";

import { SpandaMedallion } from "@/components/InkGlyph";
import type { PhilosophicalTradition } from "@/lib/learningPaths";
import { LEARNING_TRACKS, PHILOSOPHICAL_TRADITIONS } from "@/lib/learningPaths";
import type { ProgressMap } from "@/lib/learn/progress";
import { stepKey } from "@/lib/learn/progress";

type TraditionChooserProps = {
  progress: ProgressMap;
  hydrated: boolean;
  onSelectTradition: (traditionId: string) => void;
};

/**
 * Tradition chooser — "Duolingo for each philosophical language."
 * Each tradition card shows a sumi mark, title, invitation,
 * and progress stats.
 */
export function TraditionChooser({ progress, hydrated, onSelectTradition }: TraditionChooserProps) {
  return (
    <div className="section-stack">
      <header className="library-header">
        <div className="library-header__body">
          <p className="passage-reading__meta">Guided study</p>
          <h1 className="library-header__title">Choose Your Path</h1>
          <p className="library-header__lede">
            Each tradition is a philosophical language — vocabulary, metaphors, images, and ideas.
            Walk one gate to the next. Complete a path to see through that tradition's eyes.
          </p>
        </div>
      </header>

      <section className="mt-8 pb-16">
        <ul className="mx-auto grid max-w-4xl list-none gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {PHILOSOPHICAL_TRADITIONS.map((tradition) => {
            const { completed, total } = getTraditionProgress(tradition, progress);
            const pct = total > 0 ? Math.round((completed / total) * 100) : 0;
            const isDone = completed === total && total > 0;
            const isStarted = completed > 0;

            return (
              <li key={tradition.id}>
                <button
                  type="button"
                  onClick={() => onSelectTradition(tradition.id)}
                  className="group relative block h-full w-full text-left transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]"
                >
                  <article className="flex h-full flex-col gap-4 rounded-3xl border border-amber-200/15 bg-gradient-to-b from-[#0b0b14]/80 to-[#0b0b14]/60 p-6 backdrop-blur-sm transition-all duration-300 group-hover:border-amber-200/30 group-hover:shadow-[0_0_32px_rgba(240,201,121,0.12)]">
                    {/* Medallion */}
                    <div className="flex items-center justify-center">
                      <SpandaMedallion
                        glyph={tradition.glyph}
                        state={isDone ? "recognized" : isStarted ? "arising" : "unmanifest"}
                        size="lg"
                      />
                    </div>

                    {/* Title & Invitation */}
                    <div className="flex-1">
                      <h2 className="text-lg font-medium leading-snug text-stone-100 transition-colors duration-300 group-hover:text-amber-100">
                        {tradition.title}
                      </h2>
                      <p className="mt-2 text-sm leading-relaxed text-stone-400">{tradition.invitation}</p>
                    </div>

                    {/* Progress */}
                    {hydrated ? (
                      <div className="border-t border-amber-200/8 pt-3">
                        {isDone ? (
                          <div className="flex items-center gap-2">
                            <span className="rounded-full border border-emerald-300/35 bg-emerald-300/8 px-2.5 py-0.5 font-sans text-[9px] uppercase tracking-[0.14em] text-emerald-200">
                              Complete
                            </span>
                            <span className="font-sans text-xs text-stone-500">
                              {total} {total === 1 ? "gate" : "gates"}
                            </span>
                          </div>
                        ) : isStarted ? (
                          <div className="space-y-1.5">
                            <div className="flex items-center justify-between font-sans text-[10px] uppercase tracking-[0.16em] text-stone-500">
                              <span>Progress</span>
                              <span>
                                {completed}/{total}
                              </span>
                            </div>
                            <div className="h-1.5 overflow-hidden rounded-full bg-white/5">
                              <div
                                className="h-full bg-amber-200 transition-all duration-500"
                                style={{ width: `${pct}%` }}
                              />
                            </div>
                          </div>
                        ) : (
                          <div className="font-sans text-xs uppercase tracking-[0.16em] text-stone-500">
                            {total} {total === 1 ? "gate" : "gates"} · Start →
                          </div>
                        )}
                      </div>
                    ) : (
                      <div className="h-8 animate-pulse rounded border border-white/5 bg-white/5" />
                    )}
                  </article>
                </button>
              </li>
            );
          })}
        </ul>
      </section>
    </div>
  );
}

function getTraditionProgress(
  tradition: PhilosophicalTradition,
  progress: ProgressMap,
): { completed: number; total: number } {
  let completed = 0;
  let total = 0;

  for (const trackId of tradition.trackIds) {
    const track = LEARNING_TRACKS.find((t) => t.id === trackId);
    if (!track) continue;

    for (const step of track.steps) {
      total++;
      if (progress[stepKey(trackId, step.id)]) completed++;
    }
  }

  return { completed, total };
}
