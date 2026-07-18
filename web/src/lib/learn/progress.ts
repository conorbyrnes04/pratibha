import type { LearningTrack } from "@/lib/learningPaths";

export const LEARN_STORAGE_KEY = "pratibha.learn.v1";
export const LEARN_EXPORT_VERSION = 1 as const;

export type ProgressMap = Record<string, boolean>;

export type LearnProgressExport = {
  version: typeof LEARN_EXPORT_VERSION;
  exportedAt: string;
  progress: ProgressMap;
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

export function loadLearnProgress(): ProgressMap {
  if (typeof window === "undefined") return {};
  try {
    const raw = localStorage.getItem(LEARN_STORAGE_KEY);
    if (!raw) return {};
    return asProgressMap(JSON.parse(raw)) ?? {};
  } catch {
    return {};
  }
}

export function saveLearnProgress(progress: ProgressMap): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(LEARN_STORAGE_KEY, JSON.stringify(progress));
}

export function trackDoneCount(track: LearningTrack, progress: ProgressMap): number {
  return track.steps.filter((s) => progress[stepKey(track.id, s.id)]).length;
}

export function clearTrackProgress(trackId: string, track: LearningTrack | undefined, progress: ProgressMap): ProgressMap {
  const next = { ...progress };
  for (const s of track?.steps || []) {
    delete next[stepKey(trackId, s.id)];
  }
  return next;
}

export function buildLearnProgressExport(progress: ProgressMap): LearnProgressExport {
  return {
    version: LEARN_EXPORT_VERSION,
    exportedAt: new Date().toISOString(),
    progress: { ...progress },
  };
}

export function parseLearnProgressImport(raw: string): ProgressMap {
  const data = JSON.parse(raw) as unknown;
  if (data && typeof data === "object" && !Array.isArray(data)) {
    const obj = data as Record<string, unknown>;
    if ("progress" in obj) {
      const mapped = asProgressMap(obj.progress);
      if (mapped) return mapped;
    }
    const bare = asProgressMap(data);
    if (bare) return bare;
  }
  throw new Error("Unrecognized progress file");
}

export function downloadLearnProgress(progress: ProgressMap): void {
  if (typeof window === "undefined") return;
  const payload = buildLearnProgressExport(progress);
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  const day = payload.exportedAt.slice(0, 10);
  a.href = url;
  a.download = `pratibha-learn-progress-${day}.json`;
  a.click();
  URL.revokeObjectURL(url);
}
