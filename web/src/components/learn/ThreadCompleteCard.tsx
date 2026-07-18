"use client";

import {
  LEARNING_THREADS,
  findThread,
  type LearningThread,
} from "@/lib/learningThreads";

type ThreadCompleteCardProps = {
  threadId: string;
  progress: Record<string, boolean>;
  onBackToMap: () => void;
  onTraceAnother: (threadId: string) => void;
  onDescendPath: () => void;
  onLeaveThread: () => void;
};

function stepKey(trackId: string, stepId: string): string {
  return `${trackId}:${stepId}`;
}

function litCount(thread: LearningThread, progress: Record<string, boolean>): number {
  return thread.steps.filter((s) => progress[stepKey(s.trackId, s.stepId)]).length;
}

export function ThreadCompleteCard({
  threadId,
  progress,
  onBackToMap,
  onTraceAnother,
  onDescendPath,
  onLeaveThread,
}: ThreadCompleteCardProps) {
  const thread = findThread(threadId);
  if (!thread) return null;

  const lit = litCount(thread, progress);
  const total = thread.steps.length;
  const others = LEARNING_THREADS.filter((t) => t.id !== threadId).slice(0, 3);

  return (
    <div
      className="thread-complete relative overflow-hidden rounded-3xl border border-amber-200/35 bg-amber-100/[0.06] p-6 sm:p-8"
      style={{ ["--thread-hue" as string]: thread.hue }}
      role="status"
      aria-live="polite"
    >
      <div
        className="pointer-events-none absolute inset-0 opacity-50"
        style={{
          background: `radial-gradient(ellipse at 20% 0%, hsl(${thread.hue} 55% 45% / 0.2), transparent 55%)`,
        }}
        aria-hidden
      />
      <div className="relative">
        <p className="font-sans text-[10px] uppercase tracking-[0.2em] text-amber-200/70">Thread complete</p>
        <div className="mt-3 flex items-center gap-3">
          <span className="flex h-12 w-12 items-center justify-center rounded-full border border-amber-200/35 bg-amber-100/10 text-2xl text-amber-100">
            {thread.glyph}
          </span>
          <div>
            <h3 className="text-3xl leading-none text-amber-100">{thread.title}</h3>
            <p className="soft mt-2 text-sm leading-relaxed">{thread.subtitle}</p>
          </div>
        </div>

        <p className="mt-5 font-sans text-xs uppercase tracking-[0.16em] text-emerald-200/80">
          {lit}/{total} beads lit via path gates
        </p>

        <ol className="mt-4 space-y-2">
          {thread.steps.map((bead, i) => {
            const done = !!progress[stepKey(bead.trackId, bead.stepId)];
            return (
              <li
                key={bead.id}
                className={`rounded-2xl border px-4 py-3 ${
                  done ? "border-emerald-300/20 bg-emerald-300/5" : "border-white/8 bg-black/20"
                }`}
              >
                <p className="font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/55">
                  {done ? "✓" : i + 1} · {bead.tradition}
                </p>
                <p className="mt-1 text-sm leading-relaxed text-stone-200">{bead.insight}</p>
              </li>
            );
          })}
        </ol>

        <div className="mt-6 flex flex-wrap gap-2">
          <button type="button" onClick={onDescendPath} className="btn-primary px-4 py-2 text-sm">
            Stay on this path →
          </button>
          <button type="button" onClick={onBackToMap} className="btn-secondary px-4 py-2 text-sm">
            Thread map
          </button>
          <button type="button" onClick={onLeaveThread} className="btn-secondary px-4 py-2 text-sm">
            Leave thread
          </button>
        </div>

        {others.length > 0 ? (
          <div className="mt-8 border-t border-amber-200/10 pt-5">
            <p className="font-sans text-[10px] uppercase tracking-[0.16em] text-stone-500">Trace another</p>
            <div className="mt-3 flex flex-wrap gap-2">
              {others.map((t) => (
                <button
                  key={t.id}
                  type="button"
                  onClick={() => onTraceAnother(t.id)}
                  className="rounded-full border border-white/12 px-3 py-1.5 font-sans text-[10px] uppercase tracking-[0.12em] text-amber-200/75 transition hover:border-amber-200/35 hover:text-amber-100"
                >
                  {t.glyph} {t.title}
                </button>
              ))}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}
