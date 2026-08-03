"use client";

import { useEffect, useRef, useState } from "react";
import type { LearningTrack } from "@/lib/learningPaths";
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
  const [progress, setProgress] = useState<ProgressMap>({});
  const [completedAt, setCompletedAt] = useState<CompletedAtMap>({});
  const [hydrated, setHydrated] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    const bundle = loadLearnProgressBundle();
    setProgress(bundle.progress);
    setCompletedAt(bundle.completedAt);
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (!hydrated) return;
    saveLearnProgressBundle({ progress, completedAt });
  }, [progress, completedAt, hydrated]);

  function toggle(trackId: string, stepId: string) {
    const key = stepKey(trackId, stepId);
    setProgress((p) => {
      const nextDone = !p[key];
      setCompletedAt((c) => {
        const next = { ...c };
        if (nextDone) next[key] = new Date().toISOString();
        else delete next[key];
        return next;
      });
      return { ...p, [key]: nextDone };
    });
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
