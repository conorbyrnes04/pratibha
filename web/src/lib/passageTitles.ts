import type { VerseItem } from "./types";

type VerseWithRef = VerseItem & {
  reference?: string;
  sequence?: number;
  provenance?: { source_reference?: string; section?: string };
};

const PATANJALI_MARKERS = ["patanjali", "patañjali", "yoga_sūtras", "yoga_sutras"];

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

export function displayPassageTitle(item: VerseItem): string {
  const title = (item.title || "").trim();
  const ref = isPatanjaliYogaSutras(item) ? patanjaliSutraRef(item) : null;
  if (ref) return title ? `${ref} — ${title}` : ref;
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
