import { sumiGlyph, verseSumiGlyph, type SumiSlug } from "@/lib/sumiGlyphs";
import type { KeyTerm, VerseItem } from "@/lib/types";

export const SHARE_MARK_GROUPS = [
  {
    id: "animals",
    label: "Animals",
    marks: [
      "bear",
      "bee",
      "butterfly",
      "crane",
      "crow",
      "deer",
      "dolphin",
      "dragon",
      "eagle",
      "elephant",
      "fish",
      "fox",
      "hawk",
      "horse",
      "lion",
      "owl",
      "ox",
      "raven",
      "serpent",
      "spider",
      "stag",
      "swan",
      "tiger",
      "turtle",
      "whale",
      "wolf",
    ],
  },
  {
    id: "plants",
    label: "Plants",
    marks: ["lotus", "mushroom", "oak", "rose", "tree", "vine"],
  },
  {
    id: "objects",
    label: "Objects",
    marks: ["celtic_key", "celtic_star", "chalice", "cross", "eye", "heart", "labyrinth", "mandala", "mirror", "triangle", "yantra"],
  },
  {
    id: "elements",
    label: "Elements",
    marks: ["air", "desert", "earth", "fire", "lightning", "mountain", "ocean", "rainbow", "storm", "tides", "volcano", "water"],
  },
  {
    id: "cosmos",
    label: "Cosmos",
    marks: ["circle", "comet", "constellation", "infinity", "moon", "spiral", "star", "sun", "void", "yin_yang"],
  },
  {
    id: "figures",
    label: "Figures",
    marks: ["fool", "hermit", "king", "maiden", "mother", "sage", "shaman", "warrior"],
  },
  {
    id: "deities",
    label: "Deities",
    marks: [
      "anubis",
      "apollo",
      "artemis",
      "athena",
      "brahma",
      "dionysus",
      "durga",
      "eros",
      "freyja",
      "ganesha",
      "hades",
      "hera",
      "horus",
      "isis",
      "kali",
      "lakshmi",
      "loki",
      "nuwa",
      "odin",
      "oshun",
      "osiris",
      "persephone",
      "quetzalcoatl",
      "saraswati",
      "shango",
      "shiva",
      "tezcatlipoca",
      "thanatos",
      "thor",
      "thoth",
      "thunderbird",
      "vishnu",
      "yemaya",
      "zeus",
    ],
  },
] as const;

export const SHARE_FORCE_MARKS = SHARE_MARK_GROUPS.flatMap((group) => group.marks);

export type ShareForceMark = (typeof SHARE_FORCE_MARKS)[number];

export const SHARE_INKS = {
  ash: { label: "Ash", hex: "#8a8680" },
  bone: { label: "Bone", hex: "#e8e4dc" },
  gold: { label: "Gold", hex: "#f0c979" },
  copper: { label: "Copper", hex: "#c47a3a" },
  moonlight: { label: "Moonlight", hex: "#c5d4e0" },
} as const;

export type ShareInk = keyof typeof SHARE_INKS;
export type ShareTextMode = "original" | "translation" | "both";

export const SHARE_TEXT_MODES: { id: ShareTextMode; label: string }[] = [
  { id: "translation", label: "Translation" },
  { id: "original", label: "Original" },
  { id: "both", label: "Both" },
];

export type ShareAspectRatio = "post" | "story";

export const SHARE_ASPECT_RATIOS = {
  post: { width: 1080, height: 1350, ratio: "1080 / 1350" },
  story: { width: 1080, height: 1920, ratio: "1080 / 1920" },
} as const;

export type ShareCardOptions = {
  verseId: string;
  mark: ShareForceMark;
  ink: ShareInk;
  textMode: ShareTextMode;
  /** 1-based index into folioCandidates; omitted means the full passage. */
  line?: number;
};

export type FolioLine = {
  source: "original" | "iast" | "translation";
  text: string;
};

export function isShareForceMark(value: string): value is ShareForceMark {
  return (SHARE_FORCE_MARKS as readonly string[]).includes(value);
}

export function isShareInk(value: string): value is ShareInk {
  return Object.prototype.hasOwnProperty.call(SHARE_INKS, value);
}

export function isShareTextMode(value: string): value is ShareTextMode {
  return value === "original" || value === "translation" || value === "both";
}

export function defaultShareMark(collection?: string): ShareForceMark {
  const mapped = sumiGlyph(collection);
  if (isShareForceMark(mapped)) return mapped;
  const fallback: Record<string, ShareForceMark> = {
    hermit: "mountain",
    cross: "chalice",
    owl: "owl",
  };
  return fallback[mapped] || "lotus";
}

function layerBody(item: VerseItem, kind: string): string {
  const layer = item.pratibha_layers?.find((entry) => entry.kind === kind);
  return (layer?.body || "").trim();
}

function verseKeyTerms(item: VerseItem): string[] {
  const layer = item.pratibha_layers?.find((entry) => entry.kind === "key_terms");
  const terms: string[] = [];
  for (const entry of layer?.items || []) {
    if (entry && typeof entry === "object" && "term" in entry) {
      const term = (entry as KeyTerm).term;
      if (term) terms.push(term);
    }
  }
  return terms;
}

function asShareMark(slug: string, collection?: string): ShareForceMark {
  if (isShareForceMark(slug)) return slug;
  return defaultShareMark(collection);
}

/** Opening folio mark: verse image first, tradition if nothing resonates. */
export function verseShareMark(item: Pick<VerseItem, "collection" | "title" | "thesis" | "translation" | "themes" | "pratibha_layers">): ShareForceMark {
  return asShareMark(
    verseSumiGlyph({
      collection: item.collection,
      title: item.title,
      thesis: item.thesis,
      translation: layerBody(item as VerseItem, "translation") || item.translation,
      themes: item.themes,
      keyTerms: verseKeyTerms(item as VerseItem),
    }),
    item.collection,
  );
}

export function parseShareOptions(
  verseId: string,
  query: { g?: string; ink?: string; t?: string; l?: string },
  source?: string | Pick<VerseItem, "collection" | "title" | "thesis" | "translation" | "themes" | "pratibha_layers">,
): ShareCardOptions {
  const line = Number.parseInt(query.l || "", 10);
  const mark =
    query.g && isShareForceMark(query.g)
      ? query.g
      : typeof source === "object" && source
        ? verseShareMark(source)
        : defaultShareMark(typeof source === "string" ? source : undefined);
  return {
    verseId,
    mark,
    ink: query.ink && isShareInk(query.ink) ? query.ink : "gold",
    textMode: query.t && isShareTextMode(query.t) ? query.t : "translation",
    line: Number.isFinite(line) && line > 0 ? line : undefined,
  };
}

export function shareQuery(options: Pick<ShareCardOptions, "mark" | "ink" | "textMode" | "line">): string {
  const params = new URLSearchParams({
    g: options.mark,
    ink: options.ink,
    t: options.textMode,
  });
  if (options.line) params.set("l", String(options.line));
  return params.toString();
}

export function shareOgPath(options: ShareCardOptions): string {
  return `/api/og/verse?id=${encodeURIComponent(options.verseId)}&${shareQuery(options)}`;
}

export function sharePagePath(options: ShareCardOptions): string {
  return `/s/${encodeURIComponent(options.verseId)}?${shareQuery(options)}`;
}

export function clipShareText(text: string, max: number): string {
  const clean = text.replace(/\s+/g, " ").trim();
  if (clean.length <= max) return clean;
  const slice = clean.slice(0, max);
  const end = Math.max(
    slice.lastIndexOf("。"),
    slice.lastIndexOf("；"),
    slice.lastIndexOf(". "),
    slice.lastIndexOf("? "),
    slice.lastIndexOf(" "),
  );
  return `${(end > 16 ? slice.slice(0, end) : slice).trim()}…`;
}

export function shareCaption(input: {
  title: string;
  translation: string;
  readUrl: string;
}): string {
  const line = clipShareText(input.translation.replace(/^["“]|["”]$/g, ""), 180);
  const quoted = line ? `“${line}”\n\n` : "";
  return `${input.title}\n\n${quoted}${input.readUrl}`;
}

export const SHARE_SOCIAL = [
  { id: "instagram_story", label: "IG Story" },
  { id: "instagram_post", label: "IG Post" },
  { id: "tiktok", label: "TikTok" },
  { id: "x", label: "X" },
  { id: "whatsapp", label: "WhatsApp" },
  { id: "signal", label: "Signal" },
] as const;

export type ShareSocialId = (typeof SHARE_SOCIAL)[number]["id"];

export function tweetIntentUrl(caption: string, url: string): string {
  const text = clipShareText(caption.replace(url, "").trim(), 220);
  return `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`;
}

export function whatsappIntentUrl(caption: string): string {
  return `https://wa.me/?text=${encodeURIComponent(caption)}`;
}

export function instagramHomeUrl(): string {
  return "https://www.instagram.com/";
}

export function tiktokUploadUrl(): string {
  return "https://www.tiktok.com/upload";
}

export function markSrc(mark: SumiSlug | string): string {
  return `/sumi/${mark}.svg`;
}

function isDenseScript(text: string): boolean {
  return /[\u0900-\u097F\u0F00-\u0FFF\u4E00-\u9FFF]/.test(text);
}

function looksIast(text: string): boolean {
  if (isDenseScript(text)) return false;
  const words = text.split(/\s+/).filter(Boolean);
  if (words.length < 2) return false;
  const english = words.filter((word) =>
    /^(the|and|of|to|in|is|that|this|a|an|for|with|not|by|from|as|or|be|it|on)$/i.test(word),
  );
  return english.length / words.length < 0.28;
}

function tidyUnit(text: string): string {
  return text
    .replace(/\s*(?:\|\||॥)\s*\d+\s*(?:\|\||॥)\s*/g, " ")
    .replace(/^[“"']+|[”"']+$/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function splitUnits(text: string): string[] {
  return text
    .split(/\r\n|\n|।|॥|\||。|；/)
    .map(tidyUnit)
    .filter((unit) => unit.length > 1 && !/^\d+$/.test(unit));
}

function sweetSpot(text: string): { lo: number; hi: number; peak: number } {
  if (/[\u4E00-\u9FFF]/.test(text)) return { lo: 5, hi: 22, peak: 10 };
  if (isDenseScript(text)) return { lo: 8, hi: 36, peak: 18 };
  return { lo: 14, hi: 48, peak: 26 };
}

function scoreFolioLine(text: string): number {
  const { lo, hi, peak } = sweetSpot(text);
  if (text.length < lo || text.length > hi) return 0;
  let score = 1 - Math.abs(text.length - peak) / peak;
  const words = text.split(/\s+/).filter(Boolean);
  if ((looksIast(text) || /[\u0900-\u097F]/.test(text)) && words.length === 3) score += 0.22;
  if (/(?:^|\s)(ma|na|ca|hi|yat|मा|न|च|हि|यत्)$/i.test(text)) score -= 0.22;
  if (text.includes("''")) score -= 0.25;
  return score;
}

function prefixes(unit: string): string[] {
  const out: string[] = [];
  if (isDenseScript(unit) && /[\u4E00-\u9FFF]/.test(unit) && unit.includes("，") && unit.length > 16) {
    for (const part of unit.split("，")) {
      const clean = tidyUnit(part);
      if (clean) out.push(clean);
    }
    return out;
  }
  if (looksIast(unit) || /[\u0900-\u097F]/.test(unit)) {
    const words = unit.split(/\s+/).filter(Boolean);
    for (const n of [2, 3, 4]) {
      if (words.length >= n) out.push(words.slice(0, n).join(" "));
    }
  }
  if (/[;:—–]/.test(unit)) {
    const head = tidyUnit(unit.split(/[;:—–]/)[0] || "");
    if (head && head !== unit) out.push(head);
  }
  return out;
}

function collectFrom(source: FolioLine["source"], text: string): FolioLine[] {
  const seen = new Set<string>();
  const lines: FolioLine[] = [];
  const add = (raw: string) => {
    const value = tidyUnit(raw);
    const key = value.toLowerCase();
    if (!value || seen.has(key) || scoreFolioLine(value) <= 0) return;
    seen.add(key);
    lines.push({ source, text: value });
  };
  for (const unit of splitUnits(text)) {
    add(unit);
    for (const part of prefixes(unit)) add(part);
  }
  return lines;
}

export function folioCandidates(input: {
  original?: string;
  iast?: string;
  translation?: string;
  mode: ShareTextMode;
}): FolioLine[] {
  const lines: FolioLine[] = [];
  if (input.mode === "translation") {
    lines.push(...collectFrom("translation", input.translation || ""));
  } else {
    lines.push(...collectFrom("original", input.original || ""));
    lines.push(...collectFrom("iast", input.iast || ""));
  }
  return lines.sort((a, b) => scoreFolioLine(b.text) - scoreFolioLine(a.text) || a.text.localeCompare(b.text));
}

export function nextFolioLine(count: number, current?: number): number | undefined {
  if (count < 1) return undefined;
  if (!current) return 1;
  return current >= count ? undefined : current + 1;
}

export function pickFolioLine(lines: FolioLine[], line?: number): FolioLine | undefined {
  if (!line) return undefined;
  return lines[line - 1];
}
