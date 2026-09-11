import {
  LEARNING_TRACKS,
  RECOMMENDED_SPINE,
  type LearningTrack,
} from "@shared/learningPaths";
import type { VerseItem } from "@shared/types";
import * as Haptics from "expo-haptics";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/convexApi";
import { getCloudBridge } from "@/lib/cloudBridge";
import { useQuery } from "convex/react";
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import Constants from "expo-constants";
import { getVerses, isLocalhostApiBase, setApiBaseOverride } from "@/lib/api";
import {
  API_OVERRIDE_KEY,
  CORPUS_CACHE_KEY,
  asCompletedAt,
  asProgress,
  loadLearnBundle,
  mergeCompletedAt,
  mergeProgress,
  saveLearnBundle,
  stepKey,
  type CompletedAtMap,
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
  const { user } = useAuth();
  const remoteProgress = useQuery(api.learnProgress.get, user ? {} : "skip");
  const mergedForUser = useRef<string | null>(null);
  const [items, setItems] = useState<VerseItem[]>([]);
  const [progress, setProgress] = useState<ProgressMap>({});
  const [completedAt, setCompletedAt] = useState<CompletedAtMap>({});
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
      // Cache so the Library opens instantly next launch and survives a
      // cold/flaky backend (Render free tier sleeps when idle).
      if (verses.length > 0) {
        AsyncStorage.setItem(CORPUS_CACHE_KEY, JSON.stringify(verses)).catch(() => undefined);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Could not reach the Pratibha API");
      // Keep any cached corpus already on screen rather than blanking it.
      setItems((prev) => prev);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    (async () => {
      const [bundle, apiOverride, cachedCorpus] = await Promise.all([
        loadLearnBundle(),
        __DEV__ ? AsyncStorage.getItem(API_OVERRIDE_KEY) : Promise.resolve(null),
        AsyncStorage.getItem(CORPUS_CACHE_KEY),
      ]);
      if (apiOverride && !(Constants.isDevice && isLocalhostApiBase(apiOverride))) {
        setApiBaseOverride(apiOverride);
      }
      setProgress(bundle.progress);
      setCompletedAt(bundle.completedAt);
      setHydrated(true);
      // Show the cached corpus immediately (no spinner) while we refresh in the
      // background; the very first install has no cache and waits for the fetch.
      if (cachedCorpus) {
        try {
          const parsed = JSON.parse(cachedCorpus) as VerseItem[];
          if (Array.isArray(parsed) && parsed.length > 0) {
            setItems(parsed);
            setLoading(false);
          }
        } catch {
          // ignore a corrupt cache
        }
      }
      await refreshCorpus();
    })();
  }, [refreshCorpus]);

  useEffect(() => {
    if (!user) {
      mergedForUser.current = null;
      return;
    }
    if (!hydrated || remoteProgress === undefined) return;
    if (mergedForUser.current === user.id) return;
    mergedForUser.current = user.id;
    const remoteP = asProgress(remoteProgress?.progress);
    const remoteC = asCompletedAt(remoteProgress?.completedAt);
    setProgress((local) => mergeProgress(local, remoteP));
    setCompletedAt((local) => mergeCompletedAt(local, remoteC));
  }, [user, hydrated, remoteProgress]);

  useEffect(() => {
    if (!hydrated) return;
    void saveLearnBundle({ progress, completedAt });
    if (user && mergedForUser.current === user.id) {
      void getCloudBridge()?.pushProgress(progress, completedAt);
    }
  }, [progress, completedAt, hydrated, user]);

  const toggleStep = useCallback(async (trackId: string, stepId: string) => {
    await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
    const key = stepKey(trackId, stepId);
    setProgress((p) => {
      const nextDone = !p[key];
      setCompletedAt((c) => {
        if (nextDone) return { ...c, [key]: c[key] || new Date().toISOString() };
        const next = { ...c };
        delete next[key];
        return next;
      });
      return { ...p, [key]: nextDone };
    });
  }, []);

  const resetTrack = useCallback(async (trackId: string) => {
    const track = trackById[trackId];
    const keys = (track?.steps || []).map((s) => stepKey(trackId, s.id));
    setProgress((p) => {
      const next = { ...p };
      for (const k of keys) delete next[k];
      return next;
    });
    setCompletedAt((c) => {
      const next = { ...c };
      for (const k of keys) delete next[k];
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
