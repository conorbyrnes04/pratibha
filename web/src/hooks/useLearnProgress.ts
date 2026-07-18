"use client";

import { useEffect, useRef, useState } from "react";
import type { LearningTrack } from "@/lib/learningPaths";
import {
  clearTrackProgress,
  downloadLearnProgress,
  loadLearnProgress,
  parseLearnProgressImport,
  type ProgressMap,
  saveLearnProgress,
  stepKey,
} from "@/lib/learn/progress";

export function useLearnProgress() {
  const [progress, setProgress] = useState<ProgressMap>({});
  const [hydrated, setHydrated] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

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

  function exportProgress() {
    downloadLearnProgress(progress);
  }

  function importProgressFromFile(file: File): Promise<void> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => {
        try {
          const text = String(reader.result || "");
          const next = parseLearnProgressImport(text);
          setProgress(next);
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
