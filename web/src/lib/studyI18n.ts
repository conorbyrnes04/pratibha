import type { Locale } from "@/i18n";
import { translateStudyFields } from "@/lib/api";
import { firstSentence } from "@/lib/textPreview";
import type { KeyTerm, PratibhaLayerKind, Resonance, VerseItem } from "@/lib/types";
import { layerText, passagePreview, practiceText } from "@/lib/verseLayers";

const SOURCE_KINDS = new Set<PratibhaLayerKind>(["original", "iast"]);
const BODY_KINDS = new Set<PratibhaLayerKind>(["translation", "commentary", "practice"]);
const SKIP_KINDS = new Set<PratibhaLayerKind>(["original", "iast", "appendix"]);
export const CORE_STUDY_KEYS = new Set(["title", "thesis", "translation", "commentary", "practice"]);
const LOCAL_CACHE_PREFIX = "pratibha.i18n.v1:";

const inflight = new Map<string, Promise<Record<string, string>>>();

function fieldKind(key: string): string {
  return key.includes(":") ? key.split(":", 1)[0] : key;
}

function djb2(text: string): string {
  let hash = 5381;
  for (let i = 0; i < text.length; i += 1) hash = ((hash << 5) + hash) ^ text.charCodeAt(i);
  return (hash >>> 0).toString(36);
}

function localCacheKey(locale: string, kind: string, text: string): string {
  return `${LOCAL_CACHE_PREFIX}${locale}:${kind}:${djb2(text)}`;
}

function readLocalTranslation(locale: string, kind: string, text: string): string | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = window.localStorage.getItem(localCacheKey(locale, kind, text));
    if (!raw) return null;
    const parsed = JSON.parse(raw) as { s?: string; t?: string };
    if (parsed.s !== text || !parsed.t?.trim()) return null;
    return parsed.t.trim();
  } catch {
    return null;
  }
}

export function evictStudyI18nCache(): number {
  if (typeof window === "undefined") return 0;
  const keys: string[] = [];
  for (let i = 0; i < window.localStorage.length; i += 1) {
    const key = window.localStorage.key(i);
    if (key?.startsWith(LOCAL_CACHE_PREFIX)) keys.push(key);
  }
  for (const key of keys) window.localStorage.removeItem(key);
  return keys.length;
}

function writeLocalTranslation(locale: string, kind: string, source: string, translated: string) {
  if (typeof window === "undefined" || !translated.trim()) return;
  try {
    window.localStorage.setItem(
      localCacheKey(locale, kind, source),
      JSON.stringify({ s: source, t: translated }),
    );
  } catch {
    evictStudyI18nCache();
    try {
      window.localStorage.setItem(
        localCacheKey(locale, kind, source),
        JSON.stringify({ s: source, t: translated }),
      );
    } catch {
      /* quota / private mode */
    }
  }
}

export function applyCachedStudyFields(
  locale: Locale,
  fields: Record<string, string>,
): Record<string, string> {
  if (locale === "en") return fields;
  const out: Record<string, string> = { ...fields };
  for (const [key, value] of Object.entries(fields)) {
    const cached = readLocalTranslation(locale, fieldKind(key), value);
    if (cached) out[key] = cached;
  }
  return out;
}

function fieldKey(fields: Record<string, string>): string {
  return JSON.stringify(
    Object.keys(fields)
      .sort()
      .reduce<Record<string, string>>((acc, key) => {
        const value = (fields[key] || "").trim();
        if (value) acc[key] = value;
        return acc;
      }, {}),
  );
}

function isKeyTerm(entry: unknown): entry is KeyTerm {
  return Boolean(entry && typeof entry === "object" && "term" in entry && "definition" in entry);
}

function isResonance(entry: unknown): entry is Resonance {
  return Boolean(entry && typeof entry === "object" && "citation" in entry && "resonance" in entry);
}

export function extractVerseStudyFields(item: VerseItem): Record<string, string> {
  const fields: Record<string, string> = {};
  if (item.title?.trim()) fields.title = item.title.trim();
  if (item.thesis?.trim()) fields.thesis = item.thesis.trim();
  let termI = 0;
  let resI = 0;
  for (const layer of item.pratibha_layers || []) {
    if (SKIP_KINDS.has(layer.kind) || SOURCE_KINDS.has(layer.kind)) continue;
    if (BODY_KINDS.has(layer.kind)) {
      const body = (layer.body || "").trim();
      if (body) fields[layer.kind] = body;
      continue;
    }
    if (layer.kind === "key_terms") {
      for (const entry of layer.items || []) {
        if (!isKeyTerm(entry)) continue;
        const definition = (entry.definition || "").trim();
        if (definition) {
          fields[`key_term:${termI}`] = definition;
          termI += 1;
        }
      }
    } else if (layer.kind === "resonances") {
      for (const entry of layer.items || []) {
        if (!isResonance(entry)) continue;
        const resonance = (entry.resonance || "").trim();
        const divergence = (entry.divergence || "").trim();
        if (resonance) fields[`resonance:${resI}`] = resonance;
        if (divergence) fields[`divergence:${resI}`] = divergence;
        resI += 1;
      }
    }
  }
  if (!fields.translation && item.translation?.trim()) fields.translation = item.translation.trim();
  if (!fields.commentary && item.commentary?.trim()) fields.commentary = item.commentary.trim();
  if (!fields.practice) {
    const practice = (item.practice || item.abhyasa || "").trim();
    if (practice) fields.practice = practice;
  }
  (item.themes || []).forEach((theme, idx) => {
    const text = (theme || "").trim();
    if (text) fields[`theme:${idx}`] = text;
  });
  return fields;
}

export function applyVerseStudyFields(item: VerseItem, fields: Record<string, string>): VerseItem {
  let termI = 0;
  let resI = 0;
  let appI = 0;
  return {
    ...item,
    title: fields.title || item.title,
    thesis: fields.thesis || item.thesis,
    translation: fields.translation || item.translation,
    commentary: fields.commentary || item.commentary,
    practice: fields.practice || item.practice,
    abhyasa: fields.practice || item.abhyasa,
    themes: item.themes?.map((theme, idx) => fields[`theme:${idx}`] || theme),
    pratibha_layers: item.pratibha_layers?.map((layer) => {
      if (SOURCE_KINDS.has(layer.kind)) return layer;
      if (BODY_KINDS.has(layer.kind)) {
        return {
          ...layer,
          body: fields[layer.kind] || layer.body,
        };
      }
      if (layer.kind === "key_terms" && layer.items) {
        return {
          ...layer,
          items: layer.items.map((entry) => {
            if (!isKeyTerm(entry) || !entry.definition?.trim()) return entry;
            const next = fields[`key_term:${termI}`];
            termI += 1;
            return next ? { ...entry, definition: next } : entry;
          }),
        };
      }
      if (layer.kind === "resonances" && layer.items) {
        return {
          ...layer,
          items: layer.items.map((entry) => {
            if (!isResonance(entry)) return entry;
            const resonance = fields[`resonance:${resI}`];
            const divergence = fields[`divergence:${resI}`];
            resI += 1;
            return {
              ...entry,
              resonance: resonance || entry.resonance,
              divergence: divergence || entry.divergence,
            };
          }),
        };
      }
      if (layer.kind === "appendix" && layer.body?.trim()) {
        const next = fields[`appendix:${appI}`];
        appI += 1;
        return next ? { ...layer, body: next } : layer;
      }
      return layer;
    }),
  };
}

export function extractVerseCardFields(items: VerseItem[], limit = 40): Record<string, string> {
  const fields: Record<string, string> = {};
  for (const item of items.slice(0, limit)) {
    const title = (item.title || "").trim();
    const preview = passagePreview(item);
    const commentary = firstSentence(layerText(item, "commentary") || "");
    const practice = firstSentence(practiceText(item) || "");
    if (title) fields[`title:${item._id}`] = title;
    if (preview) fields[`translation:${item._id}`] = preview;
    if (commentary) fields[`commentary:${item._id}`] = commentary;
    if (practice) fields[`practice:${item._id}`] = practice;
  }
  return fields;
}

export function applyVerseCardFields(item: VerseItem, fields: Record<string, string>): VerseItem {
  return applyVerseStudyFields(item, {
    title: fields[`title:${item._id}`] || item.title || "",
    translation: fields[`translation:${item._id}`] || item.translation || "",
    commentary: fields[`commentary:${item._id}`] || item.commentary || "",
    practice: fields[`practice:${item._id}`] || item.practice || "",
  });
}

export function splitCoreStudyFields(fields: Record<string, string>): {
  core: Record<string, string>;
  rest: Record<string, string>;
} {
  const core: Record<string, string> = {};
  const rest: Record<string, string> = {};
  for (const [key, value] of Object.entries(fields)) {
    const kind = fieldKind(key);
    if (CORE_STUDY_KEYS.has(kind)) core[key] = value;
    else rest[key] = value;
  }
  return { core, rest };
}

export async function localizeStudyFields(
  locale: Locale,
  fields: Record<string, string>,
): Promise<Record<string, string>> {
  const clean = Object.fromEntries(
    Object.entries(fields).filter(([, value]) => Boolean(value && value.trim())),
  );
  if (locale === "en" || Object.keys(clean).length === 0) return clean;
  const cached: Record<string, string> = {};
  const missing: Record<string, string> = {};
  for (const [key, value] of Object.entries(clean)) {
    const hit = readLocalTranslation(locale, fieldKind(key), value);
    if (hit) cached[key] = hit;
    else missing[key] = value;
  }
  if (Object.keys(missing).length === 0) return { ...clean, ...cached };
  const key = `${locale}:${fieldKey(missing)}`;
  const pending = inflight.get(key);
  const request =
    pending ||
    translateStudyFields(locale, missing).then((translated) => {
      for (const [field, source] of Object.entries(missing)) {
        const text = (translated[field] || "").trim();
        if (text && text !== source) writeLocalTranslation(locale, fieldKind(field), source, text);
      }
      return { ...clean, ...cached, ...translated };
    });
  if (!pending) inflight.set(key, request.finally(() => inflight.delete(key)));
  return request;
}
