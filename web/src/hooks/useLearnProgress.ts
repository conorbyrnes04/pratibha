"use client";

import { useEffect, useState } from "react";
import type { LearningTrack } from "@/lib/learningPaths";
import {
  clearTrackProgress,
  loadLearnProgress,
  type ProgressMap,
  saveLearnProgress,
  stepKey,
} from "@/lib/learn/progress";

export function useLearnProgress() {
  const [progress, setProgress] = useState<ProgressMap>({});
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setProgress(loadLearnProgress());
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    saveLearnProgress(progress);
  }, [progress, hydrated]);

  function toggle(trackId: string, stepId: string) {
    const key = stepKey(trackId, stepId);
    setProgress((p) => ({ ...p, [key]: !p[key] }));
  }

  function resetTrack(trackId: string, track: LearningTrack | undefined) {
    setProgress((p) => clearTrackProgress(trackId, track, p));
  }

  return { progress, hydrated, toggle, resetTrack, setProgress };
}
