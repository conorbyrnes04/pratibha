import type { PratibhaLayer, PratibhaLayerKind, Resonance, VerseItem } from "@/lib/types";
import { firstSentence, stripMarkdown } from "@/lib/textPreview";
import { humanizeTtcRefs, isTaoTeChing } from "@/lib/ttcRefs";
import { passageUsesIast } from "@/lib/sanskritScript";

const ORDER: PratibhaLayerKind[] = [
  "original",
  "iast",
  "translation",
  "commentary",
  "key_terms",
  "resonances",
  "practice",
  "appendix",
];

function clean(value?: string): string {
  return (value || "").trim();
}

const IAST_PLACEHOLDER_MARKERS = [
  "source-language basis",
  "no sanskrit",
  "not in corpus",
  "chinese text",
  "chinese source",
  "chinese source text tradition",
  "greek original",
  "greek text",
  "greek original not in corpus",
  "the enchiridion is a greek",
  "not applicable",
  "pending dedicated sanskrit",
  "n/a, as the key",
];

function hasRealTransliteration(body?: string): boolean {
  const value = clean(body);
  if (!value) return false;
  if (/^\*\([^)]+\)\*\.?$/.test(value)) return false;
  if (value.startsWith("*Source-language basis:*")) return false;
  const lowered = value.toLowerCase();
  return !IAST_PLACEHOLDER_MARKERS.some((marker) => lowered.includes(marker));
}

function maybeHumanize(item: VerseItem, text?: string): string {
  const value = clean(text);
  return isTaoTeChing(item) ? humanizeTtcRefs(value) : value;
}

function normalizeLayer(layer: PratibhaLayer, item?: VerseItem): PratibhaLayer | null {
  let body = clean(layer.body);
  if (item && isTaoTeChing(item)) {
    body = humanizeTtcRefs(body);
  }
  const items = Array.isArray(layer.items)
    ? layer.items.map((entry) => {
        if (!(item && isTaoTeChing(item)) || !entry || typeof entry !== "object") {
          return entry;
        }
        // Humanize any TTC refs present on key-term / resonance fields without
        // assuming which shape the entry is.
        const rec = entry as Record<string, unknown>;
        const humanizeField = (key: string) => {
          const value = rec[key];
          return typeof value === "string" ? humanizeTtcRefs(value) : value;
        };
        return {
          ...rec,
          term: humanizeField("term"),
          definition: humanizeField("definition"),
          citation: humanizeField("citation"),
          resonance: humanizeField("resonance"),
          divergence: humanizeField("divergence"),
        };
      })
    : [];
  const layerWithBody = { ...layer, body, ...(items.length ? { items } : {}) };
  if (layerWithBody.kind === "iast") {
    if (item && !passageUsesIast(item)) return null;
    if (!hasRealTransliteration(body) && items.length === 0) return null;
    return { ...layerWithBody, label: "IAST" };
  }
  if (layerWithBody.kind === "original") {
    if (!body && items.length === 0) return null;
    // Never show a "*Source-language basis: …*" placeholder as the Original.
    const hasScript = /[ऀ-ॿༀ-࿿Ͱ-Ͽἀ-῿֐-׿؀-ۿⲀ-⳿぀-ヿ一-鿿]/.test(body);
    if (!hasScript && !hasRealTransliteration(body) && items.length === 0) return null;
    return { ...layerWithBody, label: "Original" };
  }
  return layerWithBody;
}

function finalizeLayers(layers: PratibhaLayer[], item?: VerseItem): PratibhaLayer[] {
  return layers.map((layer) => normalizeLayer(layer, item)).filter(Boolean) as PratibhaLayer[];
}

function layer(kind: PratibhaLayerKind, label: string, body?: string, item?: VerseItem): PratibhaLayer | null {
  const value = clean(body);
  if (kind === "iast") {
    if (item && !passageUsesIast(item)) return null;
    if (!hasRealTransliteration(value)) return null;
  }
  return value ? { kind, label, body: value } : null;
}

export function getVerseLayers(item: VerseItem): PratibhaLayer[] {
  if (Array.isArray(item.pratibha_layers) && item.pratibha_layers.length > 0) {
    return finalizeLayers([...item.pratibha_layers].sort((a, b) => ORDER.indexOf(a.kind) - ORDER.indexOf(b.kind)), item);
  }

  const layers: Array<PratibhaLayer | null> = [
    layer("original", "Original", item.sanskrit),
    layer("iast", "IAST", item.transliteration, item),
    layer("translation", "Pratibha Translation", item.translation),
    layer("commentary", "Pratibha Commentary", item.commentary),
    layer("practice", "Practice (Abhyasa)", item.practice || item.abhyasa),
  ];
  for (let idx = 0; idx < (item.appendixes || []).length; idx += 1) {
    const appendix = (item.appendixes || [])[idx];
    layers.push(layer("appendix", appendix.commentator || `Appendix ${idx + 1}`, appendix.text));
  }
  return finalizeLayers(layers.filter(Boolean) as PratibhaLayer[], item);
}

/** Layers for default study view — excludes PD source appendices and full chapters. */
export function getStudyLayers(item: VerseItem): PratibhaLayer[] {
  return getVerseLayers(item).filter((layer) => layer.kind !== "appendix");
}

export function getAppendixLayers(item: VerseItem): PratibhaLayer[] {
  return getVerseLayers(item).filter((layer) => layer.kind === "appendix");
}

export function getAnchorChapter(item: VerseItem): string {
  return clean((item as VerseItem & { anchor_chapter?: string }).anchor_chapter);
}

export function getLayer(item: VerseItem, kind: PratibhaLayerKind): PratibhaLayer | undefined {
  return getVerseLayers(item).find((entry) => entry.kind === kind);
}

export function layerText(item: VerseItem, kind: PratibhaLayerKind): string {
  return maybeHumanize(item, getLayer(item, kind)?.body);
}

/** Hand-authored cross-tradition resonances (the truest "related ideas"). */
export function getResonances(item: VerseItem): Resonance[] {
  const resonanceLayer = getVerseLayers(item).find((entry) => entry.kind === "resonances");
  const items = Array.isArray(resonanceLayer?.items) ? resonanceLayer!.items : [];
  return items.filter(
    (entry): entry is Resonance =>
      Boolean(entry && typeof entry === "object" && "citation" in entry && "resonance" in entry),
  );
}

export function passagePreview(item: VerseItem): string {
  return stripMarkdown(firstSentence(layerText(item, "translation") || layerText(item, "commentary") || item.source_excerpt || ""));
}

export function practiceText(item: VerseItem): string {
  return stripMarkdown(layerText(item, "practice") || item.practice || item.abhyasa || "");
}

export function maturityLabel(value?: string): string {
  switch (value) {
    case "polished":
      return "Polished";
    case "rich":
      return "Rich";
    case "draft":
      return "Draft";
    case "seed":
      return "Seed";
    // Back-compat: older stored/label values still map cleanly.
    case "publishable":
      return "Polished";
    case "strong_draft":
      return "Draft";
    case "needs_rewrite":
      return "Draft";
    case "structural_draft":
      return "Seed";
    default:
      return "Seed";
  }
}
