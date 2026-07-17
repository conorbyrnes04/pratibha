import type { ChatOptions, EditorialMaturity, Source, SourcesPayload, VerseItem } from "@/lib/types";

// Set NEXT_PUBLIC_API_BASE to the deployed backend URL (baked in at build time).
// The localhost fallback only applies in development so a misconfigured
// production build fails loudly (relative URLs) instead of silently calling
// a machine-local API that does not exist.
export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ||
  (process.env.NODE_ENV === "production" ? "" : "http://127.0.0.1:8000");

function withMaturity(path: string, minMaturity?: EditorialMaturity | "all"): string {
  if (!minMaturity || minMaturity === "all") return `${API_BASE}${path}`;
  const sep = path.includes("?") ? "&" : "?";
  return `${API_BASE}${path}${sep}min_maturity=${encodeURIComponent(minMaturity)}`;
}

export async function getVerses(minMaturity?: EditorialMaturity | "all"): Promise<VerseItem[]> {
  const res = await fetch(withMaturity("/verses", minMaturity), { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to load verses (${res.status})`);
  const data = await res.json();
  return Array.isArray(data?.items) ? (data.items as VerseItem[]) : [];
}

export async function getVerse(id: string): Promise<VerseItem | null> {
  const res = await fetch(`${API_BASE}/verse/${encodeURIComponent(id)}`, { cache: "no-store" });
  if (!res.ok) return null;
  return (await res.json()) as VerseItem;
}

export async function getDaily(minMaturity: EditorialMaturity | "all" = "strong_draft"): Promise<VerseItem | null> {
  const res = await fetch(withMaturity("/daily", minMaturity), { cache: "no-store" });
  if (!res.ok) return null;
  const data = (await res.json()) as VerseItem;
  return data && data._id ? data : null;
}

export async function getRandom(collection?: string, minMaturity: EditorialMaturity | "all" = "strong_draft"): Promise<VerseItem | null> {
  const path = collection ? `/random?collection=${encodeURIComponent(collection)}` : "/random";
  const url = withMaturity(path, minMaturity);
  const res = await fetch(url, { cache: "no-store" });
  if (!res.ok) return null;
  const data = (await res.json()) as VerseItem;
  return data && data._id ? data : null;
}

export async function getCollections(): Promise<string[]> {
  const res = await fetch(`${API_BASE}/collections`, { cache: "no-store" });
  if (!res.ok) return [];
  const data = await res.json();
  return Array.isArray(data?.items) ? data.items.map((x: unknown) => String(x)) : [];
}

export async function getSources(): Promise<SourcesPayload | null> {
  const res = await fetch(`${API_BASE}/sources`, { cache: "no-store" });
  if (!res.ok) return null;
  return (await res.json()) as SourcesPayload;
}

export async function askChat(
  messages: Array<{ role: "user" | "assistant"; content: string }>,
  useRag: boolean,
  compareMode = false,
  compareCollections: string[] = [],
  options: ChatOptions = {},
) {
  const res = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      messages,
      use_rag: useRag,
      compare_mode: compareMode,
      compare_collections: compareCollections,
      compare_verse_ids: options.compareVerseIds || [],
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
    compareWarning: String(data?.compare_warning || ""),
  };
}

export type ChatStreamHandlers = {
  onSources?: (sources: Source[], compareWarning: string) => void;
  onDelta?: (fullText: string, chunk: string) => void;
};

/**
 * Streaming chat over Server-Sent Events. Resolves with the final answer once
 * the stream completes; calls handlers incrementally as tokens arrive.
 */
export async function askChatStream(
  messages: Array<{ role: "user" | "assistant"; content: string }>,
  useRag: boolean,
  compareMode = false,
  compareCollections: string[] = [],
  options: ChatOptions = {},
  handlers: ChatStreamHandlers = {},
): Promise<{ answer: string; sources: Source[]; compareWarning: string }> {
  const res = await fetch(`${API_BASE}/chat.stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      messages,
      use_rag: useRag,
      compare_mode: compareMode,
      compare_collections: compareCollections,
      compare_verse_ids: options.compareVerseIds || [],
      verse_id: options.verseId,
      layer_focus: options.layerFocus,
      chat_mode: options.chatMode,
    }),
  });
  if (!res.ok || !res.body) throw new Error(`Chat failed (${res.status})`);

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  let answer = "";
  let sources: Source[] = [];
  let compareWarning = "";
  let errorMessage = "";

  // Parse SSE frames separated by a blank line.
  const handleEvent = (raw: string) => {
    const line = raw.split("\n").find((l) => l.startsWith("data:"));
    if (!line) return;
    let evt: { type?: string; text?: string; sources?: Source[]; compare_warning?: string; message?: string };
    try {
      evt = JSON.parse(line.slice(5).trim());
    } catch {
      return;
    }
    if (evt.type === "sources") {
      sources = Array.isArray(evt.sources) ? evt.sources : [];
      compareWarning = String(evt.compare_warning || "");
      handlers.onSources?.(sources, compareWarning);
    } else if (evt.type === "delta" && evt.text) {
      answer += evt.text;
      handlers.onDelta?.(answer, evt.text);
    } else if (evt.type === "error") {
      errorMessage = String(evt.message || "Chat failed");
    }
  };

  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });
    let idx;
    while ((idx = buffer.indexOf("\n\n")) !== -1) {
      const frame = buffer.slice(0, idx);
      buffer = buffer.slice(idx + 2);
      handleEvent(frame);
    }
  }
  if (buffer.trim()) handleEvent(buffer);

  if (!answer && errorMessage) {
    answer = errorMessage;
    handlers.onDelta?.(answer, answer);
  }
  return { answer, sources, compareWarning };
}
