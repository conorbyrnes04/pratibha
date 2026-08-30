import { storage } from "./storage";
import { isConvexConfigured } from "../convex/httpClient";
import catalog from "./learnCatalog.json";

export type LearnStep = {
  id: string;
  title?: string;
  tradition?: string;
  insight?: string;
  passageId: string;
  keyIdea?: string;
  practice?: string;
};

export type LearnTrack = {
  id: string;
  title: string;
  level: string;
  focus: string;
  outcome: string;
  description: string;
  estimatedSessions: string;
  steps: LearnStep[];
};

export type LearnThread = {
  id: string;
  title: string;
  subtitle: string;
  thesis: string;
  practice: string;
  integration: string;
  steps: LearnStep[];
};

export type LearnRealm = {
  id: string;
  title: string;
  blurb: string;
  trackIds: string[];
};

type Catalog = {
  realms: LearnRealm[];
  recommendedSpine: string[];
  recommendedThreads: string[];
  tracks: LearnTrack[];
  threads: LearnThread[];
};

const data = catalog as Catalog;

export const LEARN_REALMS = data.realms;
export const LEARN_TRACKS = data.tracks;
export const LEARN_THREADS = data.threads;
export const RECOMMENDED_SPINE = data.recommendedSpine;
export const RECOMMENDED_THREADS = data.recommendedThreads;

const LOCAL_KEY = "pratibha.learn.v1";

export type ProgressMap = Record<string, boolean>;
export type CompletedAtMap = Record<string, string>;

export function stepKey(trackId: string, stepId: string): string {
  return `${trackId}:${stepId}`;
}

export function threadKey(threadId: string, beadId: string): string {
  return `thread:${threadId}:${beadId}`;
}

export function loadProgress(): { progress: ProgressMap; completedAt: CompletedAtMap } {
  try {
    const raw = storage.get(LOCAL_KEY);
    const parsed = raw ? JSON.parse(raw) : {};
    return {
      progress: parsed.progress && typeof parsed.progress === "object" ? parsed.progress : {},
      completedAt: parsed.completedAt && typeof parsed.completedAt === "object" ? parsed.completedAt : {},
    };
  } catch {
    return { progress: {}, completedAt: {} };
  }
}

export function saveProgress(progress: ProgressMap, completedAt: CompletedAtMap) {
  storage.set(
    LOCAL_KEY,
    JSON.stringify({ version: 3, exportedAt: new Date().toISOString(), progress, completedAt }),
  );
}

export function markComplete(progress: ProgressMap, completedAt: CompletedAtMap, key: string) {
  const next = { ...progress, [key]: true };
  const times = { ...completedAt, [key]: completedAt[key] || new Date().toISOString() };
  saveProgress(next, times);
  return { progress: next, completedAt: times };
}

export async function syncLearnProgress(
  httpClient: { query: Function; mutation: Function } | null,
  user: unknown,
): Promise<{ progress: ProgressMap; completedAt: CompletedAtMap }> {
  const local = loadProgress();
  if (!httpClient || !user || !isConvexConfigured()) return local;
  try {
    const remote = (await httpClient.query("learnProgress:get", {})) as {
      progress?: ProgressMap;
      completedAt?: CompletedAtMap;
    } | null;
    const progress = { ...(remote?.progress || {}), ...local.progress };
    const completedAt = { ...(remote?.completedAt || {}), ...local.completedAt };
    for (const key of Object.keys(local.progress)) {
      if (local.progress[key] || remote?.progress?.[key]) progress[key] = true;
    }
    saveProgress(progress, completedAt);
    await httpClient.mutation("learnProgress:upsert", { progress, completedAt });
    return { progress, completedAt };
  } catch {
    return local;
  }
}

export function trackById(id: string): LearnTrack | undefined {
  return LEARN_TRACKS.find((t) => t.id === id);
}

export function threadById(id: string): LearnThread | undefined {
  return LEARN_THREADS.find((t) => t.id === id);
}
