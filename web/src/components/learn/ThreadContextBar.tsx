"use client";

import {
  beadIndex,
  findBead,
  findThread,
  type LearningThread,
  type ThreadStepRef,
} from "@/lib/learningThreads";
import { threadDoneCount } from "@/lib/learn/progress";
import { Button } from "@/components/ui/button";

type ThreadContextBarProps = {
  threadId: string;
  beadId: string;
  progress: Record<string, boolean>;
  onOpenBead: (threadId: string, beadId: string) => void;
  onLeaveThread: () => void;
  onBackToThread: () => void;
};

function litCount(thread: LearningThread, progress: Record<string, boolean>): number {
  return threadDoneCount(thread, progress);
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
      className="thread-context-bar sticky top-16 z-30 mb-5 border-b border-[rgb(240_201_121_/_0.18)] bg-[rgb(11_11_20_/_0.92)] py-3 backdrop-blur-md"
      style={{ ["--thread-hue" as string]: hue }}
      role="region"
      aria-label={`Tracing theme: ${thread.title}`}
    >
      <div className="relative flex flex-col gap-3">
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-x-2 gap-y-1">
            <span className="text-sm text-amber-100/80" aria-hidden>
              {thread.glyph}
            </span>
            <p className="passage-reading__meta !mb-0">
              Tracing · bead {idx + 1} of {total}
            </p>
            <span className="font-sans text-[10px] uppercase tracking-[0.14em] text-stone-500">
              {lit}/{total} sat
            </span>
          </div>
          <h3 className="mt-1 text-lg font-medium leading-tight text-[rgb(250_237_205)]">
            {thread.title}
          </h3>
          <p className="soft mt-1 text-sm leading-relaxed">{bead.move}</p>
          <p className="mt-1 font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/45">
            {bead.tradition}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <Button type="button" variant="secondary" size="sm" onClick={onBackToThread}>
            Theme
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
            Leave theme
          </Button>
        </div>
      </div>
    </div>
  );
}
