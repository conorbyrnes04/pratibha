"use client";

import {
  beadIndex,
  findBead,
  findThread,
  type LearningThread,
  type ThreadStepRef,
} from "@/lib/learningThreads";
import { Button } from "@/components/ui/button";

type ThreadContextBarProps = {
  threadId: string;
  beadId: string;
  progress: Record<string, boolean>;
  onOpenBead: (threadId: string, beadId: string) => void;
  onLeaveThread: () => void;
  onBackToThread: () => void;
};

function stepKey(trackId: string, stepId: string): string {
  return `${trackId}:${stepId}`;
}

function litCount(thread: LearningThread, progress: Record<string, boolean>): number {
  return thread.steps.filter((s) => progress[stepKey(s.trackId, s.stepId)]).length;
}

export function ThreadContextBar({
  threadId,
  beadId,
  progress,
  onOpenBead,
  onLeaveThread,
  onBackToThread,
}: ThreadContextBarProps) {
  const thread = findThread(threadId);
  if (!thread) return null;

  const idx = beadIndex(thread, beadId);
  const bead: ThreadStepRef | undefined = findBead(thread, beadId) ?? thread.steps[0];
  if (!bead || idx < 0) return null;

  const prev = idx > 0 ? thread.steps[idx - 1] : null;
  const next = idx < thread.steps.length - 1 ? thread.steps[idx + 1] : null;
  const lit = litCount(thread, progress);
  const total = thread.steps.length;
  const hue = thread.hue;

  return (
    <div
      className="thread-context-bar sticky top-16 z-30 mb-4 overflow-hidden rounded-2xl border border-amber-200/30 bg-[#0b0b14]/92 shadow-[0_12px_40px_rgb(0_0_0_/_0.45)] backdrop-blur-md"
      style={{ ["--thread-hue" as string]: hue }}
      role="region"
      aria-label={`Tracing thread: ${thread.title}`}
    >
      <div
        className="pointer-events-none absolute inset-0 opacity-40"
        style={{
          background: `linear-gradient(105deg, hsl(${hue} 55% 40% / 0.18), transparent 55%)`,
        }}
        aria-hidden
      />
      <div className="relative flex flex-col gap-3 p-4 sm:flex-row sm:items-center sm:justify-between sm:gap-4 sm:p-4">
        <div className="min-w-0 flex-1">
          <div className="flex flex-wrap items-center gap-2">
            <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full border border-amber-200/30 bg-amber-100/5 text-sm text-amber-100">
              {thread.glyph}
            </span>
            <p className="font-sans text-[10px] uppercase tracking-[0.18em] text-amber-200/70">
              Tracing thread · bead {idx + 1} of {total}
            </p>
            <span className="font-sans text-[10px] uppercase tracking-[0.14em] text-stone-500">
              {lit}/{total} lit via path gates
            </span>
          </div>
          <h3 className="mt-1 truncate text-xl leading-none text-amber-100">{thread.title}</h3>
          <p className="soft mt-1.5 line-clamp-2 text-sm leading-relaxed">{bead.insight}</p>
          <p className="mt-1 font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/45">
            {bead.tradition}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2 sm:shrink-0">
          <Button type="button" variant="secondary" size="sm" onClick={onBackToThread}>
            Thread map
          </Button>
          <Button
            type="button"
            variant="secondary"
            size="sm"
            disabled={!prev}
            onClick={() => prev && onOpenBead(threadId, prev.id)}
          >
            ← Prev
          </Button>
          <Button
            type="button"
            size="sm"
            disabled={!next}
            onClick={() => next && onOpenBead(threadId, next.id)}
          >
            {next ? "Next bead →" : "Last bead"}
          </Button>
          <Button type="button" variant="ghost" size="sm" onClick={onLeaveThread}>
            Leave thread
          </Button>
        </div>
      </div>
    </div>
  );
}
