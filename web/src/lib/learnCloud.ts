import {
  loadLearnProgressBundle,
  saveLearnProgressBundle,
  type CompletedAtMap,
  type ProgressMap,
} from "@/lib/learn/progress";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";

export type LearnProgressSyncResult = {
  progress: ProgressMap;
  completedAt: CompletedAtMap;
  status: "synced" | "local" | "error";
  error?: string;
};

function asMap(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};
}

function asProgress(value: unknown): ProgressMap {
  const out: ProgressMap = {};
  for (const [k, v] of Object.entries(asMap(value))) {
    if (typeof v === "boolean") out[k] = v;
  }
  return out;
}

function asCompletedAt(value: unknown): CompletedAtMap {
  const out: CompletedAtMap = {};
  for (const [k, v] of Object.entries(asMap(value))) {
    if (typeof v === "string" && v) out[k] = v;
  }
  return out;
}

function mergeProgress(local: ProgressMap, remote: ProgressMap): ProgressMap {
  const keys = new Set([...Object.keys(local), ...Object.keys(remote)]);
  const out: ProgressMap = {};
  for (const k of keys) {
    out[k] = Boolean(local[k] || remote[k]);
  }
  return out;
}

function mergeCompletedAt(local: CompletedAtMap, remote: CompletedAtMap): CompletedAtMap {
  const keys = new Set([...Object.keys(local), ...Object.keys(remote)]);
  const out: CompletedAtMap = {};
  for (const k of keys) {
    const a = local[k];
    const b = remote[k];
    if (a && b) out[k] = a < b ? a : b;
    else out[k] = a || b || "";
    if (!out[k]) delete out[k];
  }
  return out;
}

function useSyncLearnProgressLocal() {
  return {
    sync: async (): Promise<LearnProgressSyncResult> => {
      const local = loadLearnProgressBundle();
      return { progress: local.progress, completedAt: local.completedAt, status: "local" };
    },
  };
}

function useSyncLearnProgressConvex() {
  const remoteProgress = useQuery(api.learnProgress.get);
  const upsert = useMutation(api.learnProgress.upsert);

  const sync = async (): Promise<LearnProgressSyncResult> => {
    const local = loadLearnProgressBundle();

    if (remoteProgress === undefined) {
      return { progress: local.progress, completedAt: local.completedAt, status: "local" };
    }

    try {
      const remoteData = remoteProgress || { progress: {}, completedAt: {} };
      const progress = mergeProgress(local.progress, asProgress(remoteData.progress));
      const completedAt = mergeCompletedAt(local.completedAt, asCompletedAt(remoteData.completedAt));
      saveLearnProgressBundle({ progress, completedAt });

      await upsert({ progress, completedAt });

      return { progress, completedAt, status: "synced" };
    } catch (error) {
      console.warn("learn progress sync failed:", error);
      return {
        progress: local.progress,
        completedAt: local.completedAt,
        status: "error",
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  };

  return { sync };
}

export const useSyncLearnProgress = CONVEX_ENABLED
  ? useSyncLearnProgressConvex
  : useSyncLearnProgressLocal;
