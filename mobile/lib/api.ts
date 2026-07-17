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
  runtimeApiBase = url?.replace(/\/$/, "") || null;
}

export function getApiBase(): string {
  if (runtimeApiBase) return runtimeApiBase;
  const extra = Constants.expoConfig?.extra as { apiBase?: string } | undefined;
  return extra?.apiBase || process.env.EXPO_PUBLIC_API_BASE || "http://127.0.0.1:8000";
}

function withMaturity(path: string, minMaturity?: EditorialMaturity | "all"): string {
  const base = getApiBase();
  if (!minMaturity || minMaturity === "all") return `${base}${path}`;
  const sep = path.includes("?") ? "&" : "?";
  return `${base}${path}${sep}min_maturity=${encodeURIComponent(minMaturity)}`;
}

export async function getVerses(minMaturity?: EditorialMaturity | "all"): Promise<VerseItem[]> {
  const res = await fetch(withMaturity("/verses", minMaturity));
  if (!res.ok) throw new Error(`Failed to load verses (${res.status})`);
  const data = await res.json();
  return Array.isArray(data?.items) ? (data.items as VerseItem[]) : [];
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
  const res = await fetch(`${getApiBase()}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
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
