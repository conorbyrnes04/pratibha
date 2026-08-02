"use client";

import { useEffect, useMemo, useState, type CSSProperties } from "react";
import {
  LEARNING_THREADS,
  pathStepTitleForBead,
  type LearningThread,
  type ThreadStepRef,
} from "@/lib/learningThreads";
import { InkGlyph, SpandaMedallion } from "@/components/InkGlyph";
import { sumiGlyph } from "@/lib/sumiGlyphs";

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
  /** Currently traced thread (from URL / context bar). */
  activeThreadId?: string | null;
  activeBeadId?: string | null;
  onOpenBead: (threadId: string, beadId: string) => void;
};

function ThreadBead({
  step,
  index,
  done,
  active,
  hue,
  onOpen,
}: {
  step: ThreadStepRef;
  index: number;
  done: boolean;
  active: boolean;
  hue: number;
  onOpen: () => void;
}) {
  const gateTitle = pathStepTitleForBead(step);
  const beadState = done ? "recognized" : active ? "arising" : "unmanifest";
  return (
    <button
      type="button"
      onClick={onOpen}
      className={`thread-bead group flex shrink-0 flex-col items-center gap-2 text-center ${active ? "thread-bead--active" : ""}`}
      style={{ animationDelay: `${index * 0.08}s` }}
      aria-current={active ? "step" : undefined}
    >
      <span
        className={`thread-bead__orb relative flex h-12 w-12 items-center justify-center rounded-full border-2 transition duration-300 ${
          done
            ? "border-emerald-300/70 bg-emerald-300/15 text-emerald-200"
            : active
              ? "border-amber-200/80 bg-amber-200/15 text-amber-50 shadow-[0_0_0_6px_rgb(240_201_121_/_0.12)]"
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
        <InkGlyph
          glyph={step.glyphSlug ?? sumiGlyph(step.tradition)}
          state={beadState}
          size="sm"
        />
      </span>
      <span className="max-w-[6.5rem] font-sans text-[9px] uppercase tracking-[0.12em] text-amber-200/55">
        {step.tradition}
      </span>
      {gateTitle ? (
        <span className="max-w-[6.5rem] line-clamp-2 font-sans text-[9px] leading-snug text-stone-400/90">
          {gateTitle}
        </span>
      ) : null}
    </button>
  );
}

/** A short tapered ink ribbon linking two beads — a single ensō-style brush
 *  stroke, thin at both ends and fullest in the middle. Lit (bone) once the
 *  bead to its left is done; ash otherwise. */
function ThreadConnector({ lit }: { lit: boolean }) {
  return (
    <svg
      className="mt-6 hidden w-8 shrink-0 sm:block"
      width="32"
      height="10"
      viewBox="0 0 32 10"
      aria-hidden
      focusable="false"
    >
      <path
        d="M0,5 Q16,1 32,5 Q16,9 0,5 Z"
        fill={lit ? "var(--ink-light)" : "var(--ink-ghost)"}
        opacity={lit ? 0.85 : 0.6}
      />
    </svg>
  );
}

function ThreadCard({
  thread,
  progress,
  expanded,
  activeBeadId,
  onToggle,
  onOpenBead,
}: {
  thread: LearningThread;
  progress: ProgressMap;
  expanded: boolean;
  activeBeadId?: string | null;
  onToggle: () => void;
  onOpenBead: (threadId: string, beadId: string) => void;
}) {
  const { done, total } = threadProgress(thread, progress);
  const pct = Math.round((done / Math.max(1, total)) * 100);
  const complete = done === total;

  return (
    <article
      id={`thread-${thread.id}`}
      className={`thread-card scroll-mt-28 border-t border-[rgb(240_201_121_/_0.14)] py-5 transition duration-300 ${
        expanded ? "border-amber-200/30" : ""
      }`}
      style={{ ["--thread-hue" as string]: thread.hue }}
    >
      <div>
        <button type="button" onClick={onToggle} className="w-full text-left">
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-start gap-3">
              <SpandaMedallion
                glyph={thread.glyphSlug ?? sumiGlyph(thread.title)}
                state={complete ? "recognized" : "arising"}
                size="md"
                hue={thread.hue}
              />
              <div>
                <h3 className="text-xl font-medium leading-tight tracking-[-0.02em] text-[rgb(250_237_205)] sm:text-2xl">
                  {thread.title}
                </h3>
                <p className="soft mt-2 max-w-[var(--reading-measure)] text-sm leading-relaxed">
                  {thread.subtitle}
                </p>
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
          {thread.steps.map((step, i) => {
            const beadDone = !!progress[stepKey(step.trackId, step.stepId)];
            return (
              <div key={step.id} className="flex shrink-0 items-start gap-2">
                <ThreadBead
                  step={step}
                  index={i}
                  done={beadDone}
                  active={activeBeadId === step.id}
                  hue={thread.hue}
                  onOpen={() => onOpenBead(thread.id, step.id)}
                />
                {i < thread.steps.length - 1 ? <ThreadConnector lit={beadDone} /> : null}
              </div>
            );
          })}
        </div>

        <div className="mt-4 h-1 rounded-full bg-white/8">
          <div
            className="h-1 rounded-full bg-gradient-to-r from-amber-400/80 to-amber-200/60 transition-all duration-700"
            style={{ width: `${pct}%` }}
          />
        </div>
        <p className="mt-2 font-sans text-[9px] uppercase tracking-[0.14em] text-stone-500">
          Beads light when you complete their path gates
        </p>
      </div>

      {expanded ? (
        <div className="mt-4 border-t border-[rgb(240_201_121_/_0.1)] pt-4">
          <p className="passage-layer__label">Along the thread</p>
          <ol className="mt-3 space-y-2">
            {thread.steps.map((step) => {
              const beadDone = !!progress[stepKey(step.trackId, step.stepId)];
              const gateTitle = pathStepTitleForBead(step);
              const isActive = activeBeadId === step.id;
              return (
                <li key={step.id}>
                  <button
                    type="button"
                    onClick={() => onOpenBead(thread.id, step.id)}
                    className={`thread-step-row w-full border-b border-[rgb(240_201_121_/_0.1)] py-3.5 text-left transition last:border-b-0 ${
                      isActive
                        ? "bg-amber-200/[0.04]"
                        : beadDone
                          ? "opacity-90"
                          : "hover:bg-white/[0.015]"
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <span
                        className={`mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-full ${
                          beadDone ? "bg-emerald-300/20" : "bg-amber-100/10"
                        }`}
                      >
                        <InkGlyph
                          glyph={step.glyphSlug ?? sumiGlyph(step.tradition)}
                          size="sm"
                          state={beadDone ? "recognized" : isActive ? "arising" : "unmanifest"}
                        />
                      </span>
                      <div>
                        <p className="font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/60">
                          {step.tradition}
                          {gateTitle ? ` · ${gateTitle}` : ""}
                        </p>
                        <p className="mt-1 leading-relaxed text-stone-200">{step.insight}</p>
                        <span className="mt-2 inline-block font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/45">
                          {isActive ? "Current bead" : "Open on thread →"}
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

export function ThreadsConstellation({
  progress,
  hydrated,
  activeThreadId = null,
  activeBeadId = null,
  onOpenBead,
}: ThreadsConstellationProps) {
  const [expandedId, setExpandedId] = useState<string | null>(activeThreadId || LEARNING_THREADS[0]?.id || null);
  const safeProgress = hydrated ? progress : {};

  useEffect(() => {
    if (activeThreadId) setExpandedId(activeThreadId);
  }, [activeThreadId]);

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
    <section id="threads" className="threads-field relative scroll-mt-24">
      <header className="library-header">
        <div className="library-header__body">
          <div className="flex flex-wrap items-end justify-between gap-3">
            <div>
              <p className="passage-reading__meta">Threads</p>
              <h2 className="library-header__title">One theme, many traditions</h2>
              <p className="library-header__lede">
                A thread is a horizontal cut across paths — one insight followed tradition by tradition.
                Each bead opens that gate while keeping you on the thread.
              </p>
            </div>
            <p className="font-sans text-xs uppercase tracking-[0.18em] text-amber-200/50">
              {litBeads}/{totalBeads} beads lit
            </p>
          </div>
        </div>
      </header>

      <div className="mt-2">
        {LEARNING_THREADS.map((thread) => (
          <ThreadCard
            key={thread.id}
            thread={thread}
            progress={safeProgress}
            expanded={expandedId === thread.id}
            activeBeadId={activeThreadId === thread.id ? activeBeadId : null}
            onToggle={() => setExpandedId((id) => (id === thread.id ? null : thread.id))}
            onOpenBead={onOpenBead}
          />
        ))}
      </div>
    </section>
  );
}
