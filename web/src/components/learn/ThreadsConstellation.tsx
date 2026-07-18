"use client";

import { useEffect, useMemo, useState, type CSSProperties } from "react";
import { LEARNING_THREADS, type LearningThread, type ThreadStepRef } from "@/lib/learningThreads";

type ProgressMap = Record<string, boolean>;

function stepKey(trackId: string, stepId: string): string {
  return `${trackId}:${stepId}`;
}

function threadProgress(thread: LearningThread, progress: ProgressMap): { done: number; total: number } {
  const total = thread.steps.length;
  const done = thread.steps.filter((s) => progress[stepKey(s.trackId, s.stepId)]).length;
  return { done, total };
}

type ThreadsConstellationProps = {
  progress: ProgressMap;
  /** Wait until localStorage progress has loaded to avoid SSR/client mismatch. */
  hydrated: boolean;
  onOpenStep: (trackId: string, stepId: string) => void;
};

function ThreadBead({
  step,
  index,
  done,
  hue,
  onOpen,
}: {
  step: ThreadStepRef;
  index: number;
  done: boolean;
  hue: number;
  onOpen: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onOpen}
      className="thread-bead group flex shrink-0 flex-col items-center gap-2 text-center"
      style={{ animationDelay: `${index * 0.08}s` }}
    >
      <span
        className={`thread-bead__orb relative flex h-12 w-12 items-center justify-center rounded-full border-2 font-sans text-[10px] font-bold uppercase tracking-wider transition duration-300 ${
          done
            ? "border-emerald-300/70 bg-emerald-300/15 text-emerald-200"
            : "border-amber-200/35 bg-[#0b0b14]/60 text-amber-100/90 group-hover:border-amber-200/60"
        }`}
        style={
          done
            ? undefined
            : ({ ["--thread-hue" as string]: `${hue}` } as CSSProperties)
        }
      >
        <span
          className="thread-bead__pulse absolute inset-0 rounded-full"
          style={{ background: `radial-gradient(circle, hsl(${hue} 70% 55% / 0.28), transparent 70%)` }}
          aria-hidden
        />
        {index + 1}
      </span>
      <span className="max-w-[5.5rem] font-sans text-[9px] uppercase tracking-[0.12em] text-amber-200/55">{step.tradition}</span>
    </button>
  );
}

function ThreadCard({
  thread,
  progress,
  expanded,
  onToggle,
  onOpenStep,
}: {
  thread: LearningThread;
  progress: ProgressMap;
  expanded: boolean;
  onToggle: () => void;
  onOpenStep: (trackId: string, stepId: string) => void;
}) {
  const { done, total } = threadProgress(thread, progress);
  const pct = Math.round((done / Math.max(1, total)) * 100);
  const complete = done === total;

  return (
    <article
      className={`thread-card overflow-hidden rounded-3xl border transition duration-500 ${
        expanded ? "border-amber-200/40 bg-amber-100/[0.04]" : "border-white/10 bg-black/20"
      }`}
      style={{ ["--thread-hue" as string]: thread.hue }}
    >
      <div className="p-5 sm:p-6">
        <button type="button" onClick={onToggle} className="w-full text-left">
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-start gap-4">
              <span className="thread-card__glyph flex h-12 w-12 shrink-0 items-center justify-center rounded-full border border-amber-200/25 bg-amber-100/5 text-xl text-amber-200/90">
                {thread.glyph}
              </span>
              <div>
                <h3 className="text-2xl leading-none text-amber-100">{thread.title}</h3>
                <p className="soft mt-2 text-sm leading-relaxed">{thread.subtitle}</p>
              </div>
            </div>
            <span className="font-sans text-xs text-stone-400">
              {complete ? "✓" : `${done}/${total}`}
            </span>
          </div>
          <span className="mt-3 inline-block font-sans text-[10px] uppercase tracking-[0.16em] text-amber-200/50">
            {expanded ? "Close thread ↑" : "Unfold thread ↓"}
          </span>
        </button>

        {/* Beads sit outside the toggle button so hydration stays valid (no nested buttons).
            Fixed gaps (not justify-between) so 3-bead and 4-bead threads match. */}
        <div
          className="thread-constellation mt-5 flex items-start gap-2 overflow-x-auto pb-1"
          onClick={(e) => e.stopPropagation()}
        >
          {thread.steps.map((step, i) => (
            <div key={step.id} className="flex shrink-0 items-start gap-2">
              <ThreadBead
                step={step}
                index={i}
                done={!!progress[stepKey(step.trackId, step.stepId)]}
                hue={thread.hue}
                onOpen={() => onOpenStep(step.trackId, step.stepId)}
              />
              {i < thread.steps.length - 1 ? (
                <span
                  className="thread-connector mt-6 hidden h-px w-8 shrink-0 sm:block"
                  aria-hidden
                />
              ) : null}
            </div>
          ))}
        </div>

        <div className="mt-4 h-1 rounded-full bg-white/8">
          <div
            className="h-1 rounded-full bg-gradient-to-r from-amber-400/80 to-amber-200/60 transition-all duration-700"
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>

      {expanded ? (
        <div className="border-t border-amber-200/10 px-5 pb-5 sm:px-6 sm:pb-6">
          <p className="layer-heading mt-4">Along the thread</p>
          <ol className="mt-3 space-y-3">
            {thread.steps.map((step, i) => {
              const beadDone = !!progress[stepKey(step.trackId, step.stepId)];
              return (
                <li key={step.id}>
                  <button
                    type="button"
                    onClick={() => onOpenStep(step.trackId, step.stepId)}
                    className={`thread-step-row w-full rounded-2xl border p-4 text-left transition hover:border-amber-200/35 ${
                      beadDone ? "border-emerald-300/20 bg-emerald-300/5" : "border-white/8 bg-black/15"
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <span
                        className={`mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full font-sans text-xs font-bold ${
                          beadDone ? "bg-emerald-300/20 text-emerald-200" : "bg-amber-100/10 text-amber-200/80"
                        }`}
                      >
                        {beadDone ? "✓" : i + 1}
                      </span>
                      <div>
                        <p className="font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/60">{step.tradition}</p>
                        <p className="mt-1 leading-relaxed text-stone-200">{step.insight}</p>
                        <span className="mt-2 inline-block font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/45">
                          Enter gate →
                        </span>
                      </div>
                    </div>
                  </button>
                </li>
              );
            })}
          </ol>
        </div>
      ) : null}
    </article>
  );
}

export function ThreadsConstellation({ progress, hydrated, onOpenStep }: ThreadsConstellationProps) {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const safeProgress = hydrated ? progress : {};

  useEffect(() => {
    if (expandedId === null && LEARNING_THREADS[0]) {
      setExpandedId(LEARNING_THREADS[0].id);
    }
  }, [expandedId]);

  const totalBeads = useMemo(
    () => LEARNING_THREADS.reduce((n, t) => n + t.steps.length, 0),
    [],
  );
  const litBeads = useMemo(() => {
    let n = 0;
    for (const thread of LEARNING_THREADS) {
      for (const step of thread.steps) {
        if (safeProgress[stepKey(step.trackId, step.stepId)]) n++;
      }
    }
    return n;
  }, [safeProgress]);

  return (
    <section className="threads-field relative mt-12 overflow-hidden rounded-[2rem] border border-amber-200/12 p-5 sm:p-8">
      <div className="threads-field__glow pointer-events-none absolute inset-0" aria-hidden />
      <div className="relative">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="eyebrow">Threads</p>
            <h2 className="mt-2 text-3xl font-semibold leading-none text-amber-100 sm:text-4xl">One theme, many traditions</h2>
            <p className="soft mt-3 max-w-xl text-base leading-relaxed">
              A thread is a single insight traced across the corpus — like a golden sutra running through the diagram.
              Each bead opens the gate where that tradition speaks it.
            </p>
          </div>
          <p className="font-sans text-xs uppercase tracking-[0.18em] text-amber-200/50">
            {litBeads}/{totalBeads} beads lit
          </p>
        </div>

        <div className="mt-8 grid gap-4 lg:grid-cols-2">
          {LEARNING_THREADS.map((thread) => (
            <ThreadCard
              key={thread.id}
              thread={thread}
              progress={safeProgress}
              expanded={expandedId === thread.id}
              onToggle={() => setExpandedId((id) => (id === thread.id ? null : thread.id))}
              onOpenStep={onOpenStep}
            />
          ))}
        </div>
      </div>
    </section>
  );
}
