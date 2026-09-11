import Constants from "expo-constants";
import type { ChatOptions, EditorialMaturity, Source, VerseItem } from "@shared/types";

let runtimeApiBase: string | null = null;

export function isLocalhostApiBase(url: string): boolean {
  try {
    const host = new URL(url).hostname;
    return host === "127.0.0.1" || host === "localhost";
  } catch {
    return false;
  }
}

export function setApiBaseOverride(url: string | null): void {
  if (!__DEV__) return;
  runtimeApiBase = url?.replace(/\/$/, "") || null;
}

export const PRODUCTION_API_BASE = "https://pratibha-1.onrender.com";

export function getApiBase(): string {
  if (runtimeApiBase) return runtimeApiBase;
  const extra = Constants.expoConfig?.extra as { apiBase?: string } | undefined;
  return extra?.apiBase || process.env.EXPO_PUBLIC_API_BASE || PRODUCTION_API_BASE;
}

function withMaturity(path: string, minMaturity?: EditorialMaturity | "all"): string {
  const base = getApiBase();
  if (!minMaturity || minMaturity === "all") return `${base}${path}`;
  const sep = path.includes("?") ? "&" : "?";
  return `${base}${path}${sep}min_maturity=${encodeURIComponent(minMaturity)}`;
}

/** fetch with an abort timeout so a stalled/cold backend never hangs forever. */
async function fetchWithTimeout(url: string, ms: number, init?: RequestInit): Promise<Response> {
  const ctrl = new AbortController();
  const id = setTimeout(() => ctrl.abort(), ms);
  try {
    return await fetch(url, { ...init, signal: ctrl.signal });
  } finally {
    clearTimeout(id);
  }
}

export async function getVerses(minMaturity?: EditorialMaturity | "all"): Promise<VerseItem[]> {
  const url = withMaturity("/verses", minMaturity);
  // Render's free tier sleeps when idle; the first hit can take ~60s to wake.
  // Two attempts with a generous timeout: the first nudges it awake, the second
  // lands on a warm instance — instead of a timeout-less fetch hanging forever.
  let lastErr: unknown = null;
  for (let attempt = 0; attempt < 2; attempt += 1) {
    try {
      const res = await fetchWithTimeout(url, 75000);
      if (!res.ok) throw new Error(`Failed to load verses (${res.status})`);
      const data = await res.json();
      return Array.isArray(data?.items) ? (data.items as VerseItem[]) : [];
    } catch (e) {
      lastErr = e;
    }
  }
  throw lastErr instanceof Error ? lastErr : new Error("Could not load verses");
}

export async function getVerse(id: string): Promise<VerseItem | null> {
  const res = await fetch(`${getApiBase()}/verse/${encodeURIComponent(id)}`);
  if (!res.ok) return null;
  return (await res.json()) as VerseItem;
}

export async function getDaily(minMaturity: EditorialMaturity | "all" = "publishable"): Promise<VerseItem | null> {
  const res = await fetch(withMaturity("/daily", minMaturity));
  if (!res.ok) return null;
  const data = (await res.json()) as VerseItem;
  return data?._id ? data : null;
}

export type HealthStatus = {
  ok: boolean;
  status?: number;
  verseCount?: number;
  error?: string;
};

export async function pingHealth(): Promise<HealthStatus> {
  try {
    const res = await fetch(`${getApiBase()}/health`);
    if (!res.ok) {
      return { ok: false, status: res.status, error: `HTTP ${res.status}` };
    }
    const data = (await res.json()) as { items?: number; ok?: boolean };
    return {
      ok: true,
      status: res.status,
      verseCount: typeof data?.items === "number" ? data.items : undefined,
    };
  } catch (e) {
    return { ok: false, error: e instanceof Error ? e.message : "Connection failed" };
  }
}

export async function askChat(
  messages: Array<{ role: "user" | "assistant"; content: string }>,
  useRag: boolean,
  options: ChatOptions = {},
) {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (options.accessToken) headers.Authorization = `Bearer ${options.accessToken}`;
  const res = await fetch(`${getApiBase()}/chat`, {
    method: "POST",
    headers,
    body: JSON.stringify({
      messages,
      use_rag: useRag,
      compare_mode: false,
      verse_id: options.verseId,
      layer_focus: options.layerFocus,
      chat_mode: options.chatMode,
    }),
  });
  if (!res.ok) throw new Error(`Chat failed (${res.status})`);
  const data = await res.json();
  return {
    answer: String(data?.answer || ""),
    sources: (Array.isArray(data?.sources) ? data.sources : []) as Source[],
  };
}
