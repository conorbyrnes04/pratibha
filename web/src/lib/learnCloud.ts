import {
  loadLearnProgressBundle,
  saveLearnProgressBundle,
  type CompletedAtMap,
  type ProgressMap,
} from "@/lib/learn/progress";
import { getSupabase } from "@/lib/supabaseClient";

type Row = {
  user_id: string;
  progress: ProgressMap;
  completed_at: CompletedAtMap;
  updated_at: string;
};

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

/** Merge maps: for progress, true wins; for completedAt, earliest completion wins. */
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

/**
 * Pull remote learn progress, merge with local, upsert, and persist locally.
 */
export async function syncLearnProgressWithCloud(userId: string): Promise<LearnProgressSyncResult> {
  const supabase = getSupabase();
  const local = loadLearnProgressBundle();
  if (!supabase) {
    return { progress: local.progress, completedAt: local.completedAt, status: "local" };
  }

  const { data, error } = await supabase
    .from("learn_progress")
    .select("*")
    .eq("user_id", userId)
    .maybeSingle();

  if (error) {
    console.warn("learn progress sync pull failed:", error.message);
    return {
      progress: local.progress,
      completedAt: local.completedAt,
      status: "error",
      error: error.message,
    };
  }

  const remoteProgress = asProgress(data?.progress);
  const remoteCompleted = asCompletedAt(data?.completed_at);
  const progress = mergeProgress(local.progress, remoteProgress);
  const completedAt = mergeCompletedAt(local.completedAt, remoteCompleted);
  saveLearnProgressBundle({ progress, completedAt });

  const { error: upsertError } = await supabase.from("learn_progress").upsert(
    {
      user_id: userId,
      progress,
      completed_at: completedAt,
      updated_at: new Date().toISOString(),
    },
    { onConflict: "user_id" },
  );

  if (upsertError) {
    console.warn("learn progress sync push failed:", upsertError.message);
    return { progress, completedAt, status: "error", error: upsertError.message };
  }

  return { progress, completedAt, status: "synced" };
}
