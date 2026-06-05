import type { LearningTrack } from "@/lib/learningPaths";

export const LEARN_STORAGE_KEY = "pratibha.learn.v1";

export type ProgressMap = Record<string, boolean>;

export function stepKey(trackId: string, stepId: string): string {
  return `${trackId}:${stepId}`;
}

export function loadLearnProgress(): ProgressMap {
  if (typeof window === "undefined") return {};
  try {
    const raw = localStorage.getItem(LEARN_STORAGE_KEY);
    if (!raw) return {};
    const parsed = JSON.parse(raw) as ProgressMap;
    return parsed && typeof parsed === "object" ? parsed : {};
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
