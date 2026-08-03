import type { LearningStepSpec, LearningTrack } from "@/lib/learningPaths";
import { LEARNING_TRACKS, RECOMMENDED_SPINE } from "@/lib/learningPaths";

export const LEARN_STORAGE_KEY = "pratibha.learn.v1";
export const LEARN_EXPORT_VERSION = 2 as const;

/** Gate completion booleans (v1-compatible). */
export type ProgressMap = Record<string, boolean>;

/** ISO timestamps for when a gate was last marked complete. */
export type CompletedAtMap = Record<string, string>;

export type LearnProgressExport = {
  version: typeof LEARN_EXPORT_VERSION;
  exportedAt: string;
  progress: ProgressMap;
  completedAt: CompletedAtMap;
};

export type LearnProgressBundle = {
  progress: ProgressMap;
  completedAt: CompletedAtMap;
};

export type DailySitPick = {
  track: LearningTrack;
  step: LearningStepSpec;
  stepIndex: number;
  kind: "next" | "revisit";
  daysSince?: number;
};

export function stepKey(trackId: string, stepId: string): string {
  return `${trackId}:${stepId}`;
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
      // v1 bare boolean map
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

/** Simple spacing: revisit a completed gate after 2+ days (prefer oldest due). */
export function pickDailySit(
  progress: ProgressMap,
  completedAt: CompletedAtMap,
  preferredTrackId?: string,
): DailySitPick | null {
  const now = Date.now();
  const due: Array<DailySitPick & { daysSince: number }> = [];

  for (const track of LEARNING_TRACKS) {
    track.steps.forEach((step, stepIndex) => {
      const key = stepKey(track.id, step.id);
      if (!progress[key]) return;
      const at = completedAt[key];
      if (!at) return;
      const daysSince = daysBetween(at, now);
      if (daysSince >= 2) {
        due.push({ track, step, stepIndex, kind: "revisit", daysSince });
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
      return { track, step: track.steps[stepIndex], stepIndex, kind: "next" };
    }
  }

  // All complete — revisit the oldest completed gate if any.
  const completed: Array<DailySitPick & { daysSince: number }> = [];
  for (const track of LEARNING_TRACKS) {
    track.steps.forEach((step, stepIndex) => {
      const key = stepKey(track.id, step.id);
      if (!progress[key]) return;
      const at = completedAt[key];
      const daysSince = at ? daysBetween(at, now) : 999;
      completed.push({ track, step, stepIndex, kind: "revisit", daysSince });
    });
  }
  if (completed.length === 0) return null;
  completed.sort((a, b) => (b.daysSince ?? 0) - (a.daysSince ?? 0));
  return completed[0];
}
