import {
  catalogMaturityKey,
  readCatalogCache,
  readCollectionsCache,
  writeCatalogCache,
  writeCollectionsCache,
} from "@/lib/catalogCache";
import type { ChatOptions, EditorialMaturity, Source, SourcesPayload, VerseItem } from "@/lib/types";
import type { Lemma, LemmaPassageRef, LexiconListItem, LexiconListResponse } from "@/lib/lexiconTypes";
import type { LexiconStudyPayload } from "@/lib/lexiconStudyTypes";

// Set NEXT_PUBLIC_API_BASE to the deployed backend URL (baked in at build time).
// The localhost fallback only applies in development so a misconfigured
// production build fails loudly (relative URLs) instead of silently calling
// a machine-local API that does not exist.
export const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE ||
  (process.env.NODE_ENV === "production" ? "" : "http://127.0.0.1:8000");

/** Catalog fetch progress for Library UX (cold starts feel slow). */
export type CatalogFetchStatus = "loading" | "waking";

export type CatalogFetchMeta = {
  fromCache: boolean;
  stale?: boolean;
};

export type CatalogFetchOptions = {
  onStatus?: (status: CatalogFetchStatus) => void;
  onMeta?: (meta: CatalogFetchMeta) => void;
  signal?: AbortSignal;
};

const CATALOG_TIMEOUT_MS = 12_000;
/** After this, Library may show "Waking the library…" when there is no cache. */
const WAKING_HINT_MS = 2_000;
const CATALOG_BACKOFF_MS = [400, 1_200, 2_800] as const;

function withMaturity(path: string, minMaturity?: EditorialMaturity | "all"): string {
  if (!minMaturity || minMaturity === "all") return `${API_BASE}${path}`;
  const sep = path.includes("?") ? "&" : "?";
  return `${API_BASE}${path}${sep}min_maturity=${encodeURIComponent(minMaturity)}`;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function fetchWithTimeout(
  url: string,
  timeoutMs: number,
  signal?: AbortSignal,
): Promise<Response> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  const onAbort = () => controller.abort();
  signal?.addEventListener("abort", onAbort);
  try {
    return await fetch(url, { cache: "no-store", signal: controller.signal });
  } finally {
    clearTimeout(timer);
    signal?.removeEventListener("abort", onAbort);
  }
}

function isRetryableCatalogError(err: unknown, status?: number, signal?: AbortSignal): boolean {
  if (signal?.aborted) return false;
  if (status != null && status >= 500) return true;
  if (err instanceof DOMException && err.name === "AbortError") return true; // per-attempt timeout
  if (err instanceof TypeError) return true; // network failure
  return false;
}

/** Cheap liveness ping — useful before the first heavy `/verses` on a cold Render box. */
export async function pingHealth(signal?: AbortSignal): Promise<{ ok: boolean; ready?: boolean }> {
  try {
    const res = await fetchWithTimeout(`${API_BASE}/health`, 8_000, signal);
    if (!res.ok) return { ok: false };
    const data = (await res.json()) as { ok?: boolean; ready?: boolean };
    return { ok: Boolean(data?.ok), ready: data?.ready };
  } catch {
    return { ok: false };
  }
}

/**
 * Library catalog. Writes localStorage on success; on network/5xx failure returns
 * a non-empty cache when available instead of throwing an empty shelf.
 */
export async function getVerses(
  minMaturity?: EditorialMaturity | "all",
  options: CatalogFetchOptions = {},
): Promise<VerseItem[]> {
  const cacheKey = catalogMaturityKey(minMaturity);
  const url = withMaturity("/verses", minMaturity);
  options.onStatus?.("loading");

  let wakeNotified = false;
  const wakeTimer = setTimeout(() => {
    wakeNotified = true;
    options.onStatus?.("waking");
  }, WAKING_HINT_MS);

  let lastError: Error | null = null;
  try {
    for (let attempt = 0; attempt < CATALOG_BACKOFF_MS.length; attempt++) {
      if (options.signal?.aborted) {
        lastError = new Error("Catalog fetch aborted");
        break;
      }
      try {
        const res = await fetchWithTimeout(url, CATALOG_TIMEOUT_MS, options.signal);
        if (!res.ok) {
          const err = new Error(`Failed to load verses (${res.status})`);
          lastError = err;
          if (
            isRetryableCatalogError(err, res.status, options.signal) &&
            attempt < CATALOG_BACKOFF_MS.length - 1
          ) {
            if (!wakeNotified) {
              wakeNotified = true;
              options.onStatus?.("waking");
            }
            await sleep(CATALOG_BACKOFF_MS[attempt]);
            continue;
          }
          break;
        }
        const data = await res.json();
        const items = Array.isArray(data?.items) ? (data.items as VerseItem[]) : [];
        writeCatalogCache(cacheKey, items);
        options.onMeta?.({ fromCache: false });
        return items;
      } catch (err) {
        lastError = err instanceof Error ? err : new Error(String(err));
        if (
          isRetryableCatalogError(err, undefined, options.signal) &&
          attempt < CATALOG_BACKOFF_MS.length - 1
        ) {
          if (!wakeNotified) {
            wakeNotified = true;
            options.onStatus?.("waking");
          }
          await sleep(CATALOG_BACKOFF_MS[attempt]);
          continue;
        }
        break;
      }
    }
  } finally {
    clearTimeout(wakeTimer);
  }

  if (options.signal?.aborted) {
    throw lastError || new Error("Catalog fetch aborted");
  }

  const cached = readCatalogCache(cacheKey);
  if (cached) {
    options.onMeta?.({ fromCache: true, stale: true });
    return cached.items;
  }
  throw lastError || new Error("Failed to load verses");
}

export async function getVerse(id: string, locale?: string): Promise<VerseItem | null> {
  const suffix = locale && locale !== "en" ? `?locale=${encodeURIComponent(locale)}` : "";
  const res = await fetch(`${API_BASE}/verse/${encodeURIComponent(id)}${suffix}`, { cache: "no-store" });
  if (!res.ok) return null;
  return (await res.json()) as VerseItem;
}

export async function translateStudyFields(
  locale: string,
  fields: Record<string, string>,
): Promise<Record<string, string>> {
  const clean = Object.fromEntries(
    Object.entries(fields).filter(([, value]) => Boolean(value && value.trim())),
  );
  if (!locale || locale === "en" || Object.keys(clean).length === 0) return clean;
  const res = await fetch(`${API_BASE}/study/translate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    cache: "no-store",
    body: JSON.stringify({ locale, fields: clean }),
  });
  if (!res.ok) return clean;
  const data = (await res.json()) as { fields?: Record<string, string> };
  return { ...clean, ...(data.fields || {}) };
}

/** Semantic neighbours from pgvector; empty array when RAG is off / unavailable. */
export async function getRelatedVerses(id: string, limit = 6): Promise<VerseItem[]> {
  const res = await fetch(
    `${API_BASE}/verse/${encodeURIComponent(id)}/related?limit=${limit}`,
    { cache: "no-store" },
  );
  if (!res.ok) return [];
  const data = await res.json();
  return Array.isArray(data?.items) ? (data.items as VerseItem[]) : [];
}

export type ListenSection = "translation" | "commentary" | "practice" | "all";

export type ListenPlan = {
  room: string;
  sections: Array<Exclude<ListenSection, "all">>;
};

export async function listenConfigured(): Promise<boolean> {
  try {
    const res = await fetch(`${API_BASE}/listen/status`, { cache: "no-store" });
    if (!res.ok) return false;
    const data = (await res.json()) as { configured?: boolean };
    return Boolean(data?.configured);
  } catch {
    return false;
  }
}

export async function listenPlan(verseId: string): Promise<ListenPlan | null> {
  try {
    const res = await fetch(
      `${API_BASE}/listen/plan?verse_id=${encodeURIComponent(verseId)}`,
      { cache: "no-store" },
    );
    if (!res.ok) return null;
    const data = (await res.json()) as { room?: string; sections?: string[] };
    const sections = (data.sections || []).filter(
      (s): s is Exclude<ListenSection, "all"> =>
        s === "translation" || s === "commentary" || s === "practice",
    );
    return { room: data.room || "unmarked", sections };
  } catch {
    return null;
  }
}

export class ListenApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ListenApiError";
    this.status = status;
  }
}

function listenHeaders(accessToken?: string | null): Record<string, string> {
  const headers: Record<string, string> = {};
  if (accessToken) headers.Authorization = `Bearer ${accessToken}`;
  return headers;
}

export async function listenCue(
  room: string,
  edge: "open" | "close",
  accessToken?: string | null,
): Promise<Blob> {
  const res = await fetch(
    `${API_BASE}/listen/cue/${encodeURIComponent(room)}/${edge}`,
    { cache: "no-store", headers: listenHeaders(accessToken) },
  );
  if (!res.ok) {
    throw new ListenApiError("Could not load this cue.", res.status);
  }
  return res.blob();
}

export async function listenPassage(
  verseId: string,
  accessToken?: string | null,
  section: ListenSection = "all",
): Promise<{ blob: Blob; room: string }> {
  const headers: Record<string, string> = {
    ...listenHeaders(accessToken),
    "Content-Type": "application/json",
  };
  const res = await fetch(`${API_BASE}/listen`, {
    method: "POST",
    cache: "no-store",
    headers,
    body: JSON.stringify({ verse_id: verseId, section }),
  });
  if (!res.ok) {
    let detail = "Could not speak this passage.";
    try {
      const data = (await res.json()) as { detail?: string };
      if (typeof data?.detail === "string" && data.detail.trim()) detail = data.detail;
    } catch {
      /* ignore */
    }
    throw new ListenApiError(detail, res.status);
  }
  const blob = await res.blob();
  return { blob, room: res.headers.get("X-Listen-Room") || "" };
}

export async function getDaily(minMaturity: EditorialMaturity | "all" = "rich"): Promise<VerseItem | null> {
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

/**
 * Collection names for filters / chat. Same retry + localStorage fallback pattern
 * as getVerses so a cold API never looks like an empty corpus.
 */
export async function getCollections(options: CatalogFetchOptions = {}): Promise<string[]> {
  const url = `${API_BASE}/collections`;
  options.onStatus?.("loading");

  let wakeNotified = false;
  const wakeTimer = setTimeout(() => {
    wakeNotified = true;
    options.onStatus?.("waking");
  }, WAKING_HINT_MS);

  let lastError: Error | null = null;
  try {
    for (let attempt = 0; attempt < CATALOG_BACKOFF_MS.length; attempt++) {
      if (options.signal?.aborted) {
        lastError = new Error("Collections fetch aborted");
        break;
      }
      try {
        const res = await fetchWithTimeout(url, CATALOG_TIMEOUT_MS, options.signal);
        if (!res.ok) {
          const err = new Error(`Failed to load collections (${res.status})`);
          lastError = err;
          if (
            isRetryableCatalogError(err, res.status, options.signal) &&
            attempt < CATALOG_BACKOFF_MS.length - 1
          ) {
            if (!wakeNotified) {
              wakeNotified = true;
              options.onStatus?.("waking");
            }
            await sleep(CATALOG_BACKOFF_MS[attempt]);
            continue;
          }
          break;
        }
        const data = await res.json();
        const items = Array.isArray(data?.items) ? data.items.map((x: unknown) => String(x)) : [];
        writeCollectionsCache(items);
        options.onMeta?.({ fromCache: false });
        return items;
      } catch (err) {
        lastError = err instanceof Error ? err : new Error(String(err));
        if (
          isRetryableCatalogError(err, undefined, options.signal) &&
          attempt < CATALOG_BACKOFF_MS.length - 1
        ) {
          if (!wakeNotified) {
            wakeNotified = true;
            options.onStatus?.("waking");
          }
          await sleep(CATALOG_BACKOFF_MS[attempt]);
          continue;
        }
        break;
      }
    }
  } finally {
    clearTimeout(wakeTimer);
  }

  if (options.signal?.aborted) return [];

  const cached = readCollectionsCache();
  if (cached) {
    options.onMeta?.({ fromCache: true, stale: true });
    return cached.items;
  }
  // Preserve prior soft-fail for callers that only need a dropdown: empty list
  // when there is truly nothing cached (chat/random still degrade gracefully).
  if (lastError) {
    options.onMeta?.({ fromCache: false });
  }
  return [];
}

export async function getSources(): Promise<SourcesPayload | null> {
  const res = await fetch(`${API_BASE}/sources`, { cache: "no-store" });
  if (!res.ok) return null;
  return (await res.json()) as SourcesPayload;
}

/** Browse lexicon lemmas. Backend: `GET /lexicon?q=&tradition=&limit=`. */
export async function getLexicon(opts: {
  q?: string;
  tradition?: string;
  limit?: number;
} = {}): Promise<LexiconListResponse> {
  const params = new URLSearchParams();
  if (opts.q?.trim()) params.set("q", opts.q.trim());
  if (opts.tradition?.trim() && opts.tradition !== "all") params.set("tradition", opts.tradition.trim());
  if (opts.limit != null) params.set("limit", String(opts.limit));
  const qs = params.toString();
  const res = await fetch(`${API_BASE}/lexicon${qs ? `?${qs}` : ""}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to load lexicon (${res.status})`);
  const data = await res.json();
  const items = Array.isArray(data?.items) ? (data.items as LexiconListItem[]) : [];
  const total = typeof data?.total === "number" ? data.total : items.length;
  return { items, total };
}

/** Language decks + sense cards. Backend: `GET /lexicon/study`. */
export async function getLexiconStudy(
  minimumMaturity: "structural_draft" | "strong_draft" | "canonical" = "strong_draft",
): Promise<LexiconStudyPayload> {
  const params = new URLSearchParams({ minimum_maturity: minimumMaturity });
  const res = await fetch(`${API_BASE}/lexicon/study?${params}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`Failed to load lexicon study (${res.status})`);
  return (await res.json()) as LexiconStudyPayload;
}

/** Full lemma document. Backend: `GET /lexicon/{id}`. */
export async function getLemma(id: string): Promise<Lemma | null> {
  const res = await fetch(`${API_BASE}/lexicon/${encodeURIComponent(id)}`, { cache: "no-store" });
  if (!res.ok) return null;
  return (await res.json()) as Lemma;
}

/** Passages that use this lemma. Backend: `GET /lexicon/{id}/passages`. */
export async function getLemmaPassages(id: string): Promise<LemmaPassageRef[]> {
  const res = await fetch(`${API_BASE}/lexicon/${encodeURIComponent(id)}/passages`, {
    cache: "no-store",
  });
  if (!res.ok) return [];
  const data = await res.json();
  if (Array.isArray(data)) return data as LemmaPassageRef[];
  if (Array.isArray(data?.items)) return data.items as LemmaPassageRef[];
  return [];
}

export class ChatApiError extends Error {
  status: number;
  code?: string;
  limit?: number;
  remaining?: number;

  constructor(
    message: string,
    opts: { status: number; code?: string; limit?: number; remaining?: number },
  ) {
    super(message);
    this.name = "ChatApiError";
    this.status = opts.status;
    this.code = opts.code;
    this.limit = opts.limit;
    this.remaining = opts.remaining;
  }
}

const DAILY_CAP_MESSAGE =
  "You've reached today's study chat limit. Return tomorrow — or continue reading the manuscript.";

function chatHeaders(options: ChatOptions): HeadersInit {
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (options.accessToken) headers.Authorization = `Bearer ${options.accessToken}`;
  return headers;
}

function chatBody(
  messages: Array<{ role: "user" | "assistant"; content: string }>,
  useRag: boolean,
  compareMode: boolean,
  compareCollections: string[],
  options: ChatOptions,
) {
  return {
    messages,
    use_rag: useRag,
    compare_mode: compareMode,
    compare_collections: compareCollections,
    compare_verse_ids: options.compareVerseIds || [],
    verse_id: options.verseId,
    layer_focus: options.layerFocus,
    chat_mode: options.chatMode,
    depth: options.depth,
  };
}

async function throwChatHttpError(res: Response): Promise<never> {
  let code: string | undefined;
  let detail = "";
  let limit: number | undefined;
  let remaining: number | undefined;
  try {
    const data = await res.json();
    code = typeof data?.code === "string" ? data.code : undefined;
    detail = typeof data?.detail === "string" ? data.detail : "";
    if (typeof data?.limit === "number") limit = data.limit;
    if (typeof data?.remaining === "number") remaining = data.remaining;
  } catch {
    /* ignore non-JSON */
  }
  const headerRemaining = res.headers.get("X-Chat-Daily-Remaining");
  if (remaining === undefined && headerRemaining != null) {
    const n = Number(headerRemaining);
    if (!Number.isNaN(n)) remaining = n;
  }
  if (res.status === 429 && code === "daily_cap") {
    throw new ChatApiError(detail || DAILY_CAP_MESSAGE, {
      status: 429,
      code: "daily_cap",
      limit,
      remaining: remaining ?? 0,
    });
  }
  throw new ChatApiError(detail || `Chat failed (${res.status})`, {
    status: res.status,
    code,
    limit,
    remaining,
  });
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
    headers: chatHeaders(options),
    body: JSON.stringify(chatBody(messages, useRag, compareMode, compareCollections, options)),
  });
  if (!res.ok) await throwChatHttpError(res);
  const data = await res.json();
  const headerRemaining = res.headers.get("X-Chat-Daily-Remaining");
  const remainingFromHeader =
    headerRemaining != null && !Number.isNaN(Number(headerRemaining))
      ? Number(headerRemaining)
      : undefined;
  return {
    answer: String(data?.answer || ""),
    sources: (Array.isArray(data?.sources) ? data.sources : []) as Source[],
    compareWarning: String(data?.compare_warning || ""),
    remaining:
      typeof data?.remaining === "number"
        ? data.remaining
        : remainingFromHeader,
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
): Promise<{ answer: string; sources: Source[]; compareWarning: string; remaining?: number }> {
  const res = await fetch(`${API_BASE}/chat.stream`, {
    method: "POST",
    headers: chatHeaders(options),
    body: JSON.stringify(chatBody(messages, useRag, compareMode, compareCollections, options)),
  });
  if (!res.ok || !res.body) await throwChatHttpError(res);
  // throwChatHttpError is Promise<never>, but TS does not narrow res.body across the await.
  const stream = res.body as ReadableStream<Uint8Array>;

  const headerRemaining = res.headers.get("X-Chat-Daily-Remaining");
  let remaining: number | undefined =
    headerRemaining != null && !Number.isNaN(Number(headerRemaining))
      ? Number(headerRemaining)
      : undefined;

  const reader = stream.getReader();
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
    let evt: {
      type?: string;
      text?: string;
      sources?: Source[];
      compare_warning?: string;
      message?: string;
      remaining?: number;
      limit?: number;
    };
    try {
      evt = JSON.parse(line.slice(5).trim());
    } catch {
      return;
    }
    if (evt.type === "sources") {
      sources = Array.isArray(evt.sources) ? evt.sources : [];
      compareWarning = String(evt.compare_warning || "");
      handlers.onSources?.(sources, compareWarning);
    } else if (evt.type === "quota" && typeof evt.remaining === "number") {
      remaining = evt.remaining;
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
  return { answer, sources, compareWarning, remaining };
}
