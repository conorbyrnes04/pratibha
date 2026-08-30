"use client";

import {
  LEARNING_THREADS,
  findThread,
  type LearningThread,
} from "@/lib/learningThreads";
import { threadDoneCount, threadKey } from "@/lib/learn/progress";
import { Button } from "@/components/ui/button";

type ThreadCompleteCardProps = {
  threadId: string;
  progress: Record<string, boolean>;
  onBackToMap: () => void;
  onTraceAnother: (threadId: string) => void;
  onDescendPath: () => void;
  onLeaveThread: () => void;
};

function litCount(thread: LearningThread, progress: Record<string, boolean>): number {
  return threadDoneCount(thread, progress);
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
      className="thread-complete max-w-[var(--reading-measure)] border-t border-[rgb(240_201_121_/_0.2)] pt-6"
      style={{ ["--thread-hue" as string]: thread.hue }}
      role="status"
      aria-live="polite"
    >
      <p className="passage-reading__meta">Theme complete</p>
      <div className="mt-2 flex items-start gap-3">
        <span className="text-2xl text-amber-100/80" aria-hidden>
          {thread.glyph}
        </span>
        <div>
          <h3 className="library-header__title !text-[clamp(1.6rem,3.5vw,2.1rem)]">{thread.title}</h3>
          <p className="library-header__lede !mt-2">{thread.thesis}</p>
        </div>
      </div>

      <div className="passage-practice--plain mt-5">
        <p className="passage-layer__label">Thread practice</p>
        <p className="passage-practice__body">{thread.practice}</p>
      </div>
      <p className="mt-4 text-sm leading-relaxed text-stone-300">{thread.integration}</p>

      <p className="mt-5 font-sans text-xs uppercase tracking-[0.16em] text-emerald-200/80">
        {lit}/{total} beads sat as the theme
      </p>

      <ol className="mt-3">
        {thread.steps.map((bead, i) => {
          const done = !!progress[threadKey(thread.id, bead.id)];
          return (
            <li
              key={bead.id}
              className="border-b border-[rgb(240_201_121_/_0.1)] py-3 last:border-b-0"
            >
              <p className="font-sans text-[10px] uppercase tracking-[0.14em] text-amber-200/55">
                {done ? "✓" : i + 1} · {bead.tradition}
              </p>
              <p className="mt-1 text-sm leading-relaxed text-stone-200">{bead.move}</p>
            </li>
          );
        })}
      </ol>

      <div className="mt-6 flex flex-wrap gap-2">
        <Button type="button" onClick={onDescendPath} size="sm">
          Sit the full gate on this path →
        </Button>
        <Button type="button" onClick={onBackToMap} variant="secondary" size="sm">
          Themes
        </Button>
        <Button type="button" onClick={onLeaveThread} variant="secondary" size="sm">
          Leave theme
        </Button>
      </div>

      {others.length > 0 ? (
        <div className="mt-8 border-t border-[rgb(240_201_121_/_0.12)] pt-5">
          <p className="passage-reading__meta">Trace another theme</p>
          <div className="mt-3 flex flex-wrap gap-2">
            {others.map((t) => (
              <Button
                key={t.id}
                type="button"
                variant="ghost"
                size="sm"
                onClick={() => onTraceAnother(t.id)}
                className="border border-white/12 px-3 font-sans text-[10px] uppercase tracking-[0.12em] text-amber-200/75 hover:border-amber-200/35 hover:bg-amber-200/5 hover:text-amber-100"
              >
                {t.glyph} {t.title}
              </Button>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  );
}
