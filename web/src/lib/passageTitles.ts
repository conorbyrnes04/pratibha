import type { VerseItem } from "@/lib/types";

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

/** Sort Patanjali units by pada.num when the list is a single YS collection view. */
export function sortPassagesForLibrary(items: VerseItem[]): VerseItem[] {
  if (items.length === 0 || !items.every(isPatanjaliYogaSutras)) return items;
  return [...items].sort((a, b) => passageSortKey(a) - passageSortKey(b));
}
