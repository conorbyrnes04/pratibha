import type { Locale } from "@/i18n";
import { translateStudyFields } from "@/lib/api";
import { firstSentence } from "@/lib/textPreview";
import type { KeyTerm, PratibhaLayerKind, Resonance, VerseItem } from "@/lib/types";
import { layerText, passagePreview, practiceText } from "@/lib/verseLayers";

const SOURCE_KINDS = new Set<PratibhaLayerKind>(["original", "iast"]);
const BODY_KINDS = new Set<PratibhaLayerKind>(["translation", "commentary", "practice"]);

const inflight = new Map<string, Promise<Record<string, string>>>();

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
  let appI = 0;
  for (const layer of item.pratibha_layers || []) {
    if (SOURCE_KINDS.has(layer.kind)) continue;
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
    } else if (layer.kind === "appendix") {
      const body = (layer.body || "").trim();
      if (body) {
        fields[`appendix:${appI}`] = body;
        appI += 1;
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
      if (BODY_KINDS.has(layer.kind) && fields[layer.kind]) {
        return { ...layer, body: fields[layer.kind] };
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

export async function localizeStudyFields(
  locale: Locale,
  fields: Record<string, string>,
): Promise<Record<string, string>> {
  const clean = Object.fromEntries(
    Object.entries(fields).filter(([, value]) => Boolean(value && value.trim())),
  );
  if (locale === "en" || Object.keys(clean).length === 0) return clean;
  const key = `${locale}:${fieldKey(clean)}`;
  const pending = inflight.get(key);
  if (pending) return pending;
  const request = translateStudyFields(locale, clean).finally(() => inflight.delete(key));
  inflight.set(key, request);
  return request;
}
