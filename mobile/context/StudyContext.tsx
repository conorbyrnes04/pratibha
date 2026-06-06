import {
  LEARNING_TRACKS,
  RECOMMENDED_SPINE,
  type LearningTrack,
} from "@shared/learningPaths";
import type { VerseItem } from "@shared/types";
import * as Haptics from "expo-haptics";
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { getVerses, setApiBaseOverride } from "@/lib/api";
import {
  API_OVERRIDE_KEY,
  loadProgress,
  saveProgress,
  stepKey,
  type ProgressMap,
} from "@/lib/storage";
import AsyncStorage from "@react-native-async-storage/async-storage";

type StudyContextValue = {
  items: VerseItem[];
  progress: ProgressMap;
  hydrated: boolean;
  loading: boolean;
  error: string | null;
  trackById: Record<string, LearningTrack>;
  recommendedNextId: string;
  heroTrack: LearningTrack;
  heroNextStep: LearningTrack["steps"][number];
  heroNextIndex: number;
  startedTrackId: string | null;
  anyProgress: boolean;
  refreshCorpus: () => Promise<void>;
  toggleStep: (trackId: string, stepId: string) => Promise<void>;
  resetTrack: (trackId: string) => Promise<void>;
  trackDoneCount: (track: LearningTrack) => number;
};

const StudyContext = createContext<StudyContextValue | null>(null);

export function StudyProvider({ children }: { children: ReactNode }) {
  const [items, setItems] = useState<VerseItem[]>([]);
  const [progress, setProgress] = useState<ProgressMap>({});
  const [hydrated, setHydrated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const trackById = useMemo(() => {
    const m: Record<string, LearningTrack> = {};
    for (const t of LEARNING_TRACKS) m[t.id] = t;
    return m;
  }, []);

  const trackDoneCount = useCallback(
    (track: LearningTrack) => track.steps.filter((s) => progress[stepKey(track.id, s.id)]).length,
    [progress],
  );

  const anyProgress = useMemo(() => Object.values(progress).some(Boolean), [progress]);

  const recommendedNextId = useMemo(() => {
    for (const id of RECOMMENDED_SPINE) {
      const t = trackById[id];
      if (t && trackDoneCount(t) < t.steps.length) return id;
    }
    return RECOMMENDED_SPINE[RECOMMENDED_SPINE.length - 1];
  }, [progress, trackById, trackDoneCount]);

  const startedTrackId = useMemo(() => {
    for (const id of RECOMMENDED_SPINE) {
      const t = trackById[id];
      if (!t) continue;
      const d = trackDoneCount(t);
      if (d > 0 && d < t.steps.length) return id;
    }
    return null;
  }, [progress, trackById, trackDoneCount]);

  const heroTrack = trackById[startedTrackId || recommendedNextId] || LEARNING_TRACKS[0];
  const heroNextStep =
    heroTrack.steps.find((s) => !progress[stepKey(heroTrack.id, s.id)]) || heroTrack.steps[0];
  const heroNextIndex = Math.max(0, heroTrack.steps.findIndex((s) => s.id === heroNextStep.id));

  const refreshCorpus = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const verses = await getVerses("all");
      setItems(verses);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not reach the Pratibha API");
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    (async () => {
      const [p, api] = await Promise.all([loadProgress(), AsyncStorage.getItem(API_OVERRIDE_KEY)]);
      if (api) setApiBaseOverride(api);
      setProgress(p);
      setHydrated(true);
      await refreshCorpus();
    })();
  }, [refreshCorpus]);

  useEffect(() => {
    if (!hydrated) return;
    saveProgress(progress);
  }, [progress, hydrated]);

  const toggleStep = useCallback(async (trackId: string, stepId: string) => {
    await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    const key = stepKey(trackId, stepId);
    setProgress((p) => ({ ...p, [key]: !p[key] }));
  }, []);

  const resetTrack = useCallback(async (trackId: string) => {
    const track = trackById[trackId];
    setProgress((p) => {
      const next = { ...p };
      for (const s of track?.steps || []) delete next[stepKey(trackId, s.id)];
      return next;
    });
  }, [trackById]);

  const value: StudyContextValue = {
    items,
    progress,
    hydrated,
    loading,
    error,
    trackById,
    recommendedNextId,
    heroTrack,
    heroNextStep,
    heroNextIndex,
    startedTrackId,
    anyProgress,
    refreshCorpus,
    toggleStep,
    resetTrack,
    trackDoneCount,
  };

  return <StudyContext.Provider value={value}>{children}</StudyContext.Provider>;
}

export function useStudy() {
  const ctx = useContext(StudyContext);
  if (!ctx) throw new Error("useStudy must be used within StudyProvider");
  return ctx;
}
