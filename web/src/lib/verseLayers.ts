import type { PratibhaLayer, PratibhaLayerKind, VerseItem } from "@/lib/types";
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

function layer(kind: PratibhaLayerKind, label: string, body?: string): PratibhaLayer | null {
  const value = clean(body);
  return value ? { kind, label, body: value } : null;
}

export function getVerseLayers(item: VerseItem): PratibhaLayer[] {
  if (Array.isArray(item.pratibha_layers) && item.pratibha_layers.length > 0) {
    return [...item.pratibha_layers].sort((a, b) => ORDER.indexOf(a.kind) - ORDER.indexOf(b.kind));
  }

  const layers: Array<PratibhaLayer | null> = [
    layer("original", "Devanagari / Original", item.sanskrit),
    layer("iast", "IAST / Transliteration", item.transliteration),
    layer("translation", "Pratibha Translation", item.translation),
    layer("commentary", "Pratibha Commentary", item.commentary),
    layer("practice", "Practice (Abhyasa)", item.practice || item.abhyasa),
  ];
  for (let idx = 0; idx < (item.appendixes || []).length; idx += 1) {
    const appendix = (item.appendixes || [])[idx];
    layers.push(layer("appendix", appendix.commentator || `Appendix ${idx + 1}`, appendix.text));
  }
  return layers.filter(Boolean) as PratibhaLayer[];
}

export function getLayer(item: VerseItem, kind: PratibhaLayerKind): PratibhaLayer | undefined {
  return getVerseLayers(item).find((entry) => entry.kind === kind);
}

export function layerText(item: VerseItem, kind: PratibhaLayerKind): string {
  return clean(getLayer(item, kind)?.body);
}

export function passagePreview(item: VerseItem): string {
  return stripMarkdown(firstSentence(layerText(item, "translation") || layerText(item, "commentary") || item.source_excerpt || ""));
}

export function practiceText(item: VerseItem): string {
  return stripMarkdown(layerText(item, "practice") || item.practice || item.abhyasa || "");
}

export function maturityLabel(value?: string): string {
  switch (value) {
    case "publishable":
      return "Publishable";
    case "strong_draft":
      return "Strong draft";
    case "needs_rewrite":
      return "Needs rewrite";
    case "structural_draft":
      return "Structural draft";
    default:
      return "Unreviewed";
  }
}
