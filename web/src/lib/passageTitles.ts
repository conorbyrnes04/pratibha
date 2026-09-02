import type { VerseItem } from "./types";
import { isTaoTeChing } from "./ttcRefs";

type VerseWithRef = VerseItem & {
  reference?: string;
  sequence?: number;
  provenance?: { source_reference?: string; section?: string };
};

const PATANJALI_MARKERS = ["patanjali", "patañjali", "yoga_sūtras", "yoga_sutras"];

/** Schema / unit-type tokens that must never appear as reader-facing location labels. */
const UNIT_TYPE_SECTIONS = new Set([
  "chapter_section",
  "teaching_passage",
  "sutra",
  "verse",
  "chapter_summary",
  "chapter",
]);

export function isPatanjaliYogaSutras(item: VerseWithRef): boolean {
  const blob = [item.collection, item._id, item.work_id].filter(Boolean).join(" ").toLowerCase();
  if (!PATANJALI_MARKERS.some((marker) => blob.includes(marker))) return false;
  return blob.includes("yoga") || blob.includes("sutra") || blob.includes("sūtra");
}

export function patanjaliSutraRef(item: VerseWithRef): string | null {
  const ref = (item.reference || "").trim();
  if (/^\d+\.\d+$/.test(ref)) return ref;

  const sourceRef = item.provenance?.source_reference || "";
  const fromSource = sourceRef.match(/Yoga S[uū]tras\s+(\d+)\.(\d+)/i);
  if (fromSource) return `${Number(fromSource[1])}.${Number(fromSource[2])}`;

  const sid = item.sutra_id || "";
  const fromSutraId = sid.match(/^YS_(\d+)_(\d+)/i);
  if (fromSutraId) return `${Number(fromSutraId[1])}.${Number(fromSutraId[2])}`;

  const fromId = (item._id || "").match(/ys_(\d+)_(\d+)/i);
  if (fromId) return `${Number(fromId[1])}.${Number(fromId[2])}`;

  return null;
}

function sectionToken(section?: string): string {
  return (section || "").trim().toLowerCase().replace(/\s+/g, "_");
}

function isUnitTypeSection(section?: string): boolean {
  return UNIT_TYPE_SECTIONS.has(sectionToken(section));
}

/** Prefer numbered citation from ids like TTC_MD_069, BG_01_02_04, ASG_11_5. */
function locationFromSutraId(item: VerseWithRef): string | null {
  const sid = (item.sutra_id || item._id || "").trim();
  if (!sid) return null;

  const ttc = sid.match(/^TTC(?:_MD)?_(\d+)$/i);
  if (ttc) return `Chapter ${Number(ttc[1])}`;

  const bg = sid.match(/^BG_(\d+)_(\d+)(?:_(\d+))?$/i);
  if (bg) {
    const ch = Number(bg[1]);
    const a = Number(bg[2]);
    const b = bg[3] ? Number(bg[3]) : null;
    return b != null ? `${ch}.${a}–${b}` : `${ch}.${a}`;
  }

  const asg = sid.match(/^ASG_(\d+)_(\d+)$/i);
  if (asg) return `Verse ${Number(asg[1])}.${Number(asg[2])}`;

  const ys = sid.match(/^YS_(\d+)_(\d+)/i);
  if (ys) return `${Number(ys[1])}.${Number(ys[2])}`;

  const an = sid.match(/^AN_(\d+)_(\d+)$/i);
  if (an) return `${Number(an[1])}.${Number(an[2])}`;

  const cloud = sid.match(/^CLOUD_(\d+)$/i);
  if (cloud) return null; // prefer explicit "Ch. N" from section when present

  return null;
}

function humanizeSection(section?: string): string | null {
  const raw = (section || "").trim();
  if (!raw || isUnitTypeSection(raw)) return null;

  const chapterNum = raw.match(/^chapter[_\s-]*0*(\d+)$/i);
  if (chapterNum) return `Chapter ${Number(chapterNum[1])}`;

  // Already reader-facing ("Analects 1.1", "Ch. 3", "1.4.2 (Madhu)")
  return raw.replace(/_/g, " ");
}

/**
 * Clear verse/chapter label for a passage — never a schema token like `chapter_section`.
 * Examples: "Chapter 69", "1.2", "Verse 11.5", "Analects 1.1".
 */
export function displayPassageLocation(item: VerseItem): string {
  const v = item as VerseWithRef;

  const reference = (v.reference || "").trim();
  if (reference && !isUnitTypeSection(reference)) return reference;

  // Prefer an already reader-facing section ("Analects 1.1", "Ch. 3", "1.4.2").
  const fromSection = humanizeSection(v.section) || humanizeSection(v.provenance?.section);
  if (fromSection && !/^chapter\s+\d+$/i.test(fromSection)) {
    // Keep fascicle/verse labels; bare "Chapter N" from chapter_01 yields to finer id below.
    if (!/^chapter_\d+$/i.test(sectionToken(v.section))) return fromSection;
  }

  if (isPatanjaliYogaSutras(v)) {
    const ref = patanjaliSutraRef(v);
    if (ref) return ref;
  }

  const fromId = locationFromSutraId(v);
  if (fromId) return fromId;

  if (fromSection) return fromSection;

  // Last resort: title that is itself a verse label ("Verse 11.5")
  const title = (v.title || "").trim();
  if (/^(verse|sūtra|sutra|chapter|ch\.?)\s/i.test(title)) return title;

  return "";
}

/** "Tao Te Ching · Chapter 69" — collection plus the verse/chapter label. */
export function displayPassageSourceLine(item: VerseItem): string {
  const collection = (item.collection || "").trim();
  const location = displayPassageLocation(item);
  if (collection && location) return `${collection} · ${location}`;
  return collection || location || "";
}

/**
 * Detects a "title" that is really a truncated first sentence (bulk-imported
 * texts whose titles were never authored — e.g. "Taking the posture of
 * Padmâ-âsana and carrying the…"). Those read poorly in lists and the Oracle.
 */
function looksLikeProseTitle(title: string): boolean {
  if (/(…|\.\.\.)$/.test(title)) return true;
  // Long, sentence-shaped, and not a reference label ("ŚS 3.79", "Verse 11.5").
  const words = title.split(/\s+/);
  if (words.length >= 8 && !/^\s*(verse|sūtra|sutra|chapter|ch\.?)\b/i.test(title)) return true;
  return false;
}

export function displayPassageTitle(item: VerseItem): string {
  const title = (item.title || "").trim();
  const ref = isPatanjaliYogaSutras(item) ? patanjaliSutraRef(item) : null;
  if (ref) return title ? `${ref} — ${title}` : ref;
  // When the title is an unauthored prose fragment, prefer a real location ref.
  if (title && looksLikeProseTitle(title)) {
    const location = displayPassageLocation(item);
    if (location) return location;
  }
  return title || item.sutra_id || item._id || "";
}

export function passageSortKey(item: VerseWithRef): number {
  if (typeof item.sequence === "number" && item.sequence > 0) return item.sequence;
  const ref = patanjaliSutraRef(item);
  if (!ref) return Number.MAX_SAFE_INTEGER;
  const [pada, num] = ref.split(".").map(Number);
  if (!pada || !num) return Number.MAX_SAFE_INTEGER;
  return pada * 100 + num;
}

function naturalParts(s: string): Array<string | number> {
  return s
    .toLowerCase()
    .split(/(\d+)/)
    .filter(Boolean)
    .map((p) => (/^\d+$/.test(p) ? Number(p) : p));
}

function compareNatural(a: string, b: string): number {
  const ap = naturalParts(a);
  const bp = naturalParts(b);
  const n = Math.max(ap.length, bp.length);
  for (let i = 0; i < n; i++) {
    const x = ap[i];
    const y = bp[i];
    if (x === undefined) return -1;
    if (y === undefined) return 1;
    if (typeof x === "number" && typeof y === "number") {
      if (x !== y) return x - y;
      continue;
    }
    const c = String(x).localeCompare(String(y));
    if (c) return c;
  }
  return 0;
}

/** Reading order within one text: sequence → sutra/id natural order → title. */
export function sortPassagesInText(items: VerseItem[]): VerseItem[] {
  if (items.length <= 1) return items;
  const allPatanjali = items.every(isPatanjaliYogaSutras);
  return [...items].sort((a, b) => {
    const seqA = typeof a.sequence === "number" && a.sequence > 0 ? a.sequence : null;
    const seqB = typeof b.sequence === "number" && b.sequence > 0 ? b.sequence : null;
    if (seqA != null && seqB != null && seqA !== seqB) return seqA - seqB;
    if (seqA != null && seqB == null) return -1;
    if (seqB != null && seqA == null) return 1;

    if (allPatanjali) {
      const ka = passageSortKey(a);
      const kb = passageSortKey(b);
      if (ka !== kb) return ka - kb;
    }

    const idA = a.sutra_id || a._id || "";
    const idB = b.sutra_id || b._id || "";
    const byId = compareNatural(idA, idB);
    if (byId) return byId;
    return displayPassageTitle(a).localeCompare(displayPassageTitle(b));
  });
}

/** Sort passages for library/list views (same reading order as in-text navigation). */
export function sortPassagesForLibrary(items: VerseItem[]): VerseItem[] {
  return sortPassagesInText(items);
}
