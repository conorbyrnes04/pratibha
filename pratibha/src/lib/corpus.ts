const API_BASE = (process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000").replace(/\/$/, "");

export type Layer = { kind?: string; label?: string; body?: string };

export type Passage = {
  _id: string;
  title?: string;
  collection?: string;
  section?: string;
  translation?: string;
  translation_literal?: string;
  translation_note?: string;
  translation_confidence?: string;
  commentary?: string;
  practice?: string;
  abhyasa?: string;
  themes?: string[];
  pratibha_layers?: Layer[] | Record<string, string>;
  // Top-level source-script fields exist but are unreliable for non-Sanskrit
  // collections; prefer the `original`/`iast` pratibha_layers instead.
  sanskrit_devanagari?: string;
  sanskrit_iast?: string;
};

// The reading "layers" we render, in manuscript order. `original` is the
// source-language text (Devanagari / Chinese / Greek / …); `iast` is its
// romanization when present.
export type LayerKind =
  | "original"
  | "iast"
  | "translation"
  | "literal"
  | "commentary"
  | "key_terms"
  | "resonances"
  | "practice";

function layersToMap(passage: Passage): Record<string, string> {
  const layers = passage.pratibha_layers;
  const map: Record<string, string> = {};
  if (Array.isArray(layers)) {
    for (const layer of layers) {
      const kind = (layer.kind || "").trim();
      const body = (layer.body || "").trim();
      if (kind && body) map[kind] = body;
    }
  } else if (layers && typeof layers === "object") {
    for (const [kind, body] of Object.entries(layers)) {
      if (typeof body === "string" && body.trim()) map[kind] = body.trim();
    }
  }
  return map;
}

// Resolve a single reading layer, preferring the structured `pratibha_layers`
// (correct across all collections) and falling back to the flat fields.
export function getLayer(passage: Passage | null | undefined, kind: LayerKind): string {
  if (!passage) return "";
  const m = layersToMap(passage);
  switch (kind) {
    case "original":
      return m.original || "";
    case "iast":
      return m.iast || "";
    case "translation":
      return (passage.translation || m.translation || "").trim();
    case "literal":
      return (passage.translation_literal || "").trim();
    case "commentary":
      // Prefer the layer's clean prose; the flat `commentary` field appends the
      // Key Terms / Resonances sections we render as their own layers.
      return (m.commentary || passage.commentary || "").trim();
    case "key_terms":
      return m.key_terms || "";
    case "resonances":
      return m.resonances || "";
    case "practice":
      return (passage.practice || passage.abhyasa || m.practice || "").trim();
    default:
      return "";
  }
}

// Back-compat helper used by earlier callers (Home/Read list previews).
export function layerText(passage: Passage | null | undefined, kind: string): string {
  if (kind === "translation" || kind === "original" || kind === "commentary" || kind === "practice") {
    return getLayer(passage, kind as LayerKind);
  }
  if (!passage) return "";
  const direct = (passage as Record<string, unknown>)[kind];
  return typeof direct === "string" ? direct.trim() : "";
}

export async function fetchDaily(): Promise<Passage | null> {
  const response = await fetch(`${API_BASE}/daily`);
  if (!response.ok) throw new Error(`Daily failed: ${response.status}`);
  const data = await response.json();
  return data && data._id ? data : null;
}

export async function fetchPassages(limit = 40): Promise<Passage[]> {
  const response = await fetch(`${API_BASE}/verses`);
  if (!response.ok) throw new Error(`Verses failed: ${response.status}`);
  const data = await response.json();
  const items: Passage[] = data.items || data.verses || [];
  return items.slice(0, limit);
}

// Full passage with every layer — the list endpoint returns slim payloads, so
// the reader fetches the complete unit on open.
export async function fetchVerse(id: string): Promise<Passage> {
  const response = await fetch(`${API_BASE}/verse/${encodeURIComponent(id)}`);
  if (!response.ok) throw new Error(`Verse failed: ${response.status}`);
  return response.json();
}
