"use client";

import { useEffect, useRef, useState } from "react";
import type { LearningTrack } from "@/lib/learningPaths";
import { useAuth } from "@/components/AuthProvider";
import { useSyncLearnProgress } from "@/lib/learnCloud";
import { recordPractice } from "@/lib/glyphUnlock";
import {
  clearTrackProgress,
  downloadLearnProgress,
  loadLearnProgressBundle,
  parseLearnProgressImport,
  type CompletedAtMap,
  type ProgressMap,
  saveLearnProgressBundle,
  stepKey,
} from "@/lib/learn/progress";

export function useLearnProgress() {
  const { user } = useAuth();
  const [progress, setProgress] = useState<ProgressMap>({});
  const [completedAt, setCompletedAt] = useState<CompletedAtMap>({});
  const [hydrated, setHydrated] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const syncTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const syncGen = useRef(0);
  const { sync } = useSyncLearnProgress();

  useEffect(() => {
    const bundle = loadLearnProgressBundle();
    setProgress(bundle.progress);
    setCompletedAt(bundle.completedAt);
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated || !user?.id) return;
    const gen = ++syncGen.current;
    void sync().then((result) => {
      if (gen !== syncGen.current) return;
      if (result.status === "synced" || result.status === "local") {
        setProgress(result.progress);
        setCompletedAt(result.completedAt);
      }
    });
  }, [hydrated, user?.id, sync]);

  useEffect(() => {
    if (!hydrated) return;
    saveLearnProgressBundle({ progress, completedAt });
    if (!user?.id) return;
    if (syncTimer.current) clearTimeout(syncTimer.current);
    syncTimer.current = setTimeout(() => {
      void sync();
    }, 800);
    return () => {
      if (syncTimer.current) clearTimeout(syncTimer.current);
    };
  }, [progress, completedAt, hydrated, user?.id, sync]);

  function flipKey(key: string) {
    const nextDone = !progress[key];
    if (nextDone) recordPractice(`learn:${key}`);
    setProgress((p) => {
      const nextProgress = { ...p, [key]: nextDone };
      setCompletedAt((c) => {
        const next = { ...c };
        if (nextDone) next[key] = new Date().toISOString();
        else delete next[key];
        saveLearnProgressBundle({ progress: nextProgress, completedAt: next });
        return next;
      });
      return nextProgress;
    });
  }

  function toggle(trackId: string, stepId: string) {
    flipKey(stepKey(trackId, stepId));
  }

  function resetTrack(trackId: string, track: LearningTrack | undefined) {
    setProgress((p) => {
      const bundle = clearTrackProgress(trackId, track, p, completedAt);
      setCompletedAt(bundle.completedAt);
      return bundle.progress;
    });
  }

  function exportProgress() {
    downloadLearnProgress(progress, completedAt);
  }

  function importProgressFromFile(file: File): Promise<void> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        try {
          const text = String(reader.result || "");
          const next = parseLearnProgressImport(text);
          setProgress(next.progress);
          setCompletedAt(next.completedAt);
          resolve();
        } catch (err) {
          reject(err instanceof Error ? err : new Error("Import failed"));
        }
      };
      reader.onerror = () => reject(new Error("Could not read file"));
      reader.readAsText(file);
    });
  }

  function openImportPicker() {
    fileInputRef.current?.click();
  }

  return {
    progress,
    completedAt,
    hydrated,
    toggle,
    resetTrack,
    setProgress,
    exportProgress,
    importProgressFromFile,
    openImportPicker,
    fileInputRef,
  };
}
