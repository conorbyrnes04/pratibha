import type { LearningStepSpec, LearningTrack } from "@/lib/learningPaths";
import { LEARNING_TRACKS, RECOMMENDED_SPINE } from "@/lib/learningPaths";
import {
  LEARNING_THREADS,
  RECOMMENDED_THREADS,
  type LearningThread,
  type ThreadStepRef,
} from "@/lib/learningThreads";

export const LEARN_STORAGE_KEY = "pratibha.learn.v1";
export const LEARN_EXPORT_VERSION = 3 as const;

/** Gate / bead completion booleans (v1-compatible). Path keys: trackId:stepId. Thread keys: thread:threadId:beadId. */
export type ProgressMap = Record<string, boolean>;

/** ISO timestamps for when a gate or bead was last marked complete. */
export type CompletedAtMap = Record<string, string>;

export type LearnProgressExport = {
  version: 2 | 3;
  exportedAt: string;
  progress: ProgressMap;
  completedAt: CompletedAtMap;
};

export type LearnProgressBundle = {
  progress: ProgressMap;
  completedAt: CompletedAtMap;
};

export type DailySitPick =
  | {
      mode: "thread";
      kind: "next" | "revisit";
      daysSince?: number;
      threadId: string;
      beadId: string;
    }
  | {
      mode: "path";
      kind: "next" | "revisit";
      daysSince?: number;
      track: LearningTrack;
      step: LearningStepSpec;
      stepIndex: number;
    };

export function stepKey(trackId: string, stepId: string): string {
  return `${trackId}:${stepId}`;
}

export function threadKey(threadId: string, beadId: string): string {
  return `thread:${threadId}:${beadId}`;
}

export function isThreadKey(key: string): boolean {
  return key.startsWith("thread:");
}

export function parseThreadKey(key: string): { threadId: string; beadId: string } | null {
  if (!key.startsWith("thread:")) return null;
  const rest = key.slice("thread:".length);
  const sep = rest.indexOf(":");
  if (sep <= 0 || sep === rest.length - 1) return null;
  return { threadId: rest.slice(0, sep), beadId: rest.slice(sep + 1) };
}

function asProgressMap(value: unknown): ProgressMap | null {
  if (!value || typeof value !== "object" || Array.isArray(value)) return null;
  const out: ProgressMap = {};
  for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
    if (typeof k === "string" && typeof v === "boolean") out[k] = v;
  }
  return out;
}

function asCompletedAtMap(value: unknown): CompletedAtMap {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  const out: CompletedAtMap = {};
  for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
    if (typeof k === "string" && typeof v === "string" && v) out[k] = v;
  }
  return out;
}

export function loadLearnProgressBundle(): LearnProgressBundle {
  if (typeof window === "undefined") return { progress: {}, completedAt: {} };
  try {
    const raw = localStorage.getItem(LEARN_STORAGE_KEY);
    if (!raw) return { progress: {}, completedAt: {} };
    const parsed = JSON.parse(raw) as unknown;
    if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
      const obj = parsed as Record<string, unknown>;
      if ("progress" in obj) {
        return {
          progress: asProgressMap(obj.progress) ?? {},
          completedAt: asCompletedAtMap(obj.completedAt),
        };
      }
      const bare = asProgressMap(parsed);
      if (bare) return { progress: bare, completedAt: {} };
    }
    return { progress: {}, completedAt: {} };
  } catch {
    return { progress: {}, completedAt: {} };
  }
}

export function loadLearnProgress(): ProgressMap {
  return loadLearnProgressBundle().progress;
}

export function saveLearnProgressBundle(bundle: LearnProgressBundle): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(
    LEARN_STORAGE_KEY,
    JSON.stringify({
      version: LEARN_EXPORT_VERSION,
      progress: bundle.progress,
      completedAt: bundle.completedAt,
    }),
  );
}

export function saveLearnProgress(progress: ProgressMap): void {
  const { completedAt } = loadLearnProgressBundle();
  saveLearnProgressBundle({ progress, completedAt });
}

export function trackDoneCount(track: LearningTrack, progress: ProgressMap): number {
  return track.steps.filter((s) => progress[stepKey(track.id, s.id)]).length;
}

export function threadDoneCount(thread: LearningThread, progress: ProgressMap): number {
  return thread.steps.filter((s) => progress[threadKey(thread.id, s.id)]).length;
}

export function nextUnfinishedBead(
  thread: LearningThread,
  progress: ProgressMap,
): ThreadStepRef | undefined {
  return thread.steps.find((s) => !progress[threadKey(thread.id, s.id)]);
}

export function lastTouchedThreadId(completedAt: CompletedAtMap): string | null {
  let best: { id: string; t: number } | null = null;
  for (const [key, iso] of Object.entries(completedAt)) {
    const parsed = parseThreadKey(key);
    if (!parsed) continue;
    const t = Date.parse(iso);
    if (!Number.isFinite(t)) continue;
    if (!best || t > best.t) best = { id: parsed.threadId, t };
  }
  return best?.id ?? null;
}

export function recommendedNextThreadId(progress: ProgressMap): string {
  for (const id of RECOMMENDED_THREADS) {
    const t = LEARNING_THREADS.find((x) => x.id === id);
    if (t && threadDoneCount(t, progress) < t.steps.length) return id;
  }
  return RECOMMENDED_THREADS[RECOMMENDED_THREADS.length - 1] ?? LEARNING_THREADS[0]?.id ?? "";
}

export function startedThreadId(progress: ProgressMap, completedAt: CompletedAtMap): string | null {
  const last = lastTouchedThreadId(completedAt);
  if (last) {
    const t = LEARNING_THREADS.find((x) => x.id === last);
    if (t && threadDoneCount(t, progress) < t.steps.length) return last;
  }
  for (const id of RECOMMENDED_THREADS) {
    const t = LEARNING_THREADS.find((x) => x.id === id);
    if (!t) continue;
    const d = threadDoneCount(t, progress);
    if (d > 0 && d < t.steps.length) return id;
  }
  return null;
}

export function clearTrackProgress(
  trackId: string,
  track: LearningTrack | undefined,
  progress: ProgressMap,
  completedAt: CompletedAtMap = {},
): LearnProgressBundle {
  const nextProgress = { ...progress };
  const nextCompletedAt = { ...completedAt };
  for (const s of track?.steps || []) {
    const key = stepKey(trackId, s.id);
    delete nextProgress[key];
    delete nextCompletedAt[key];
  }
  return { progress: nextProgress, completedAt: nextCompletedAt };
}

export function clearThreadProgress(
  threadId: string,
  thread: LearningThread | undefined,
  progress: ProgressMap,
  completedAt: CompletedAtMap = {},
): LearnProgressBundle {
  const nextProgress = { ...progress };
  const nextCompletedAt = { ...completedAt };
  for (const bead of thread?.steps || []) {
    const key = threadKey(threadId, bead.id);
    delete nextProgress[key];
    delete nextCompletedAt[key];
  }
  return { progress: nextProgress, completedAt: nextCompletedAt };
}

export function buildLearnProgressExport(
  progress: ProgressMap,
  completedAt: CompletedAtMap = {},
): LearnProgressExport {
  return {
    version: LEARN_EXPORT_VERSION,
    exportedAt: new Date().toISOString(),
    progress: { ...progress },
    completedAt: { ...completedAt },
  };
}

/** Accepts v2 (path-only) and v3 (path + thread) exports, plus bare v1 maps. */
export function parseLearnProgressImport(raw: string): LearnProgressBundle {
  const data = JSON.parse(raw) as unknown;
  if (data && typeof data === "object" && !Array.isArray(data)) {
    const obj = data as Record<string, unknown>;
    if ("progress" in obj) {
      const mapped = asProgressMap(obj.progress);
      if (mapped) {
        return { progress: mapped, completedAt: asCompletedAtMap(obj.completedAt) };
      }
    }
    const bare = asProgressMap(data);
    if (bare) return { progress: bare, completedAt: {} };
  }
  throw new Error("Unrecognized progress file");
}

export function downloadLearnProgress(progress: ProgressMap, completedAt: CompletedAtMap = {}): void {
  if (typeof window === "undefined") return;
  const payload = buildLearnProgressExport(progress, completedAt);
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  const day = payload.exportedAt.slice(0, 10);
  a.href = url;
  a.download = `pratibha-learn-progress-${day}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function daysBetween(iso: string, now = Date.now()): number {
  const then = Date.parse(iso);
  if (!Number.isFinite(then)) return 0;
  return Math.floor((now - then) / (1000 * 60 * 60 * 24));
}

function pickLineageSit(
  progress: ProgressMap,
  completedAt: CompletedAtMap,
  preferredTrackId?: string,
  now = Date.now(),
): Extract<DailySitPick, { mode: "path" }> | null {
  const due: Array<Extract<DailySitPick, { mode: "path" }> & { daysSince: number }> = [];

  for (const track of LEARNING_TRACKS) {
    track.steps.forEach((step, stepIndex) => {
      const key = stepKey(track.id, step.id);
      if (!progress[key]) return;
      const at = completedAt[key];
      if (!at) return;
      const daysSince = daysBetween(at, now);
      if (daysSince >= 2) {
        due.push({ mode: "path", track, step, stepIndex, kind: "revisit", daysSince });
      }
    });
  }

  if (due.length > 0) {
    due.sort((a, b) => (b.daysSince ?? 0) - (a.daysSince ?? 0));
    return due[0];
  }

  const trackOrder = [
    ...(preferredTrackId ? [preferredTrackId] : []),
    ...RECOMMENDED_SPINE,
    ...LEARNING_TRACKS.map((t) => t.id),
  ];
  const seen = new Set<string>();
  for (const id of trackOrder) {
    if (seen.has(id)) continue;
    seen.add(id);
    const track = LEARNING_TRACKS.find((t) => t.id === id);
    if (!track) continue;
    const stepIndex = track.steps.findIndex((s) => !progress[stepKey(track.id, s.id)]);
    if (stepIndex >= 0) {
      return { mode: "path", track, step: track.steps[stepIndex], stepIndex, kind: "next" };
    }
  }

  const completed: Array<Extract<DailySitPick, { mode: "path" }> & { daysSince: number }> = [];
  for (const track of LEARNING_TRACKS) {
    track.steps.forEach((step, stepIndex) => {
      const key = stepKey(track.id, step.id);
      if (!progress[key]) return;
      const at = completedAt[key];
      const daysSince = at ? daysBetween(at, now) : 999;
      completed.push({ mode: "path", track, step, stepIndex, kind: "revisit", daysSince });
    });
  }
  if (completed.length === 0) return null;
  completed.sort((a, b) => (b.daysSince ?? 0) - (a.daysSince ?? 0));
  return completed[0];
}

/**
 * Theme-first daily sit:
 * 1. Due thread bead (completed ≥2 days ago)
 * 2. Next unfinished bead on the most recently touched thread
 * 3. First bead of an unstarted thread (foundations-adjacent first)
 * 4. Only then a lineage next-gate
 */
export function pickDailySit(
  progress: ProgressMap,
  completedAt: CompletedAtMap,
  preferredTrackId?: string,
): DailySitPick | null {
  const now = Date.now();

  const dueThread: Array<{ threadId: string; beadId: string; daysSince: number }> = [];
  for (const thread of LEARNING_THREADS) {
    for (const bead of thread.steps) {
      const key = threadKey(thread.id, bead.id);
      if (!progress[key]) continue;
      const at = completedAt[key];
      if (!at) continue;
      const daysSince = daysBetween(at, now);
      if (daysSince >= 2) {
        dueThread.push({ threadId: thread.id, beadId: bead.id, daysSince });
      }
    }
  }
  if (dueThread.length > 0) {
    dueThread.sort((a, b) => b.daysSince - a.daysSince);
    const top = dueThread[0];
    return {
      mode: "thread",
      kind: "revisit",
      daysSince: top.daysSince,
      threadId: top.threadId,
      beadId: top.beadId,
    };
  }

  const last = lastTouchedThreadId(completedAt);
  if (last) {
    const thread = LEARNING_THREADS.find((t) => t.id === last);
    const next = thread && nextUnfinishedBead(thread, progress);
    if (thread && next) {
      return { mode: "thread", kind: "next", threadId: thread.id, beadId: next.id };
    }
  }

  for (const id of RECOMMENDED_THREADS) {
    const thread = LEARNING_THREADS.find((t) => t.id === id);
    if (!thread) continue;
    if (threadDoneCount(thread, progress) === 0 && thread.steps[0]) {
      return { mode: "thread", kind: "next", threadId: thread.id, beadId: thread.steps[0].id };
    }
  }

  for (const id of RECOMMENDED_THREADS) {
    const thread = LEARNING_THREADS.find((t) => t.id === id);
    const next = thread && nextUnfinishedBead(thread, progress);
    if (thread && next) {
      return { mode: "thread", kind: "next", threadId: thread.id, beadId: next.id };
    }
  }

  return pickLineageSit(progress, completedAt, preferredTrackId, now);
}
