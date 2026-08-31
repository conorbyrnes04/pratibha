import type { LearningTrack } from "@/lib/learningPaths";

export const LEARN_STORAGE_KEY = "pratibha.learn.v1";
export const LEARN_EXPORT_VERSION = 3 as const;

/** Gate completion booleans. Path keys: trackId:stepId. Legacy theme keys: thread:threadId:beadId. */
export type ProgressMap = Record<string, boolean>;

/** ISO timestamps for when a gate was last marked complete. */
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

/** Accepts v2 (path-only) and v3 (path + legacy theme) exports, plus bare v1 maps. */
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
