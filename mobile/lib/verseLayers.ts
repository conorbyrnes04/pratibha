import type { PratibhaLayer, PratibhaLayerKind, VerseItem } from "@shared/types";
import { firstSentence, stripMarkdown } from "@/lib/textPreview";

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

function hasRealTransliteration(body?: string): boolean {
  const value = clean(body);
  if (!value) return false;
  return !/source-language basis/i.test(value);
}

function normalizeLayer(layer: PratibhaLayer): PratibhaLayer | null {
  const body = clean(layer.body);
  const items = Array.isArray(layer.items) ? layer.items : [];
  if (layer.kind === "iast") {
    if (!hasRealTransliteration(body) && items.length === 0) return null;
    return { ...layer, label: "IAST" };
  }
  if (layer.kind === "original") {
    if (!body && items.length === 0) return null;
    return { ...layer, label: "Original" };
  }
  return layer;
}

function finalizeLayers(layers: PratibhaLayer[]): PratibhaLayer[] {
  return layers.map(normalizeLayer).filter(Boolean) as PratibhaLayer[];
}

function layer(kind: PratibhaLayerKind, label: string, body?: string): PratibhaLayer | null {
  const value = clean(body);
  if (kind === "iast" && !hasRealTransliteration(value)) return null;
  return value ? { kind, label, body: value } : null;
}

export function getVerseLayers(item: VerseItem): PratibhaLayer[] {
  if (Array.isArray(item.pratibha_layers) && item.pratibha_layers.length > 0) {
    return finalizeLayers([...item.pratibha_layers].sort((a, b) => ORDER.indexOf(a.kind) - ORDER.indexOf(b.kind)));
  }

  const layers: Array<PratibhaLayer | null> = [
    layer("original", "Original", item.sanskrit),
    layer("iast", "IAST", item.transliteration),
    layer("translation", "Pratibha Translation", item.translation),
    layer("commentary", "Pratibha Commentary", item.commentary),
    layer("practice", "Practice (Abhyasa)", item.practice || item.abhyasa),
  ];
  for (let idx = 0; idx < (item.appendixes || []).length; idx += 1) {
    const appendix = (item.appendixes || [])[idx];
    layers.push(layer("appendix", appendix.commentator || `Appendix ${idx + 1}`, appendix.text));
  }
  return finalizeLayers(layers.filter(Boolean) as PratibhaLayer[]);
}

export function getLayer(item: VerseItem, kind: PratibhaLayerKind): PratibhaLayer | undefined {
  return getVerseLayers(item).find((entry) => entry.kind === kind);
}

export function layerText(item: VerseItem, kind: PratibhaLayerKind): string {
  return clean(getLayer(item, kind)?.body);
}

export function passagePreview(item: VerseItem): string {
  return stripMarkdown(
    firstSentence(layerText(item, "translation") || layerText(item, "commentary") || item.source_excerpt || ""),
  );
}
