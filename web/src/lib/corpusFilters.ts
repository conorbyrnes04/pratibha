import type { VerseItem } from "./types";
import { collectionIcon } from "./collectionIcons";
import { collectionsMatch, displayCollectionName } from "./collectionLabels";
import { displayPassageTitle, isPatanjaliYogaSutras, passageSortKey, sortPassagesForLibrary } from "./passageTitles";
export type ThemeCount = { theme: string; count: number };

const SUMMARY_SOURCE_RE = /^(?:ASG|PHR)_SUM_/i;
const SUMMARY_UNIT_RE = /(?:^|\.)(?:asg_sum|phr_sum)(?:_|\.|$)/i;

/** Chapter-range overview meta-units (e.g. ASG_SUM_*) — not reader-facing verses. */
export function isChapterSummaryMetaUnit(item: VerseItem): boolean {
  const section = (item.section || "").trim().toLowerCase().replace(/\s+/g, "_");
  if (section === "chapter_summary") return true;
  const provSection = (item.provenance?.section || "").trim().toLowerCase().replace(/\s+/g, "_");
  if (provSection === "chapter_summary") return true;
  for (const key of ["sutra_id", "_id"] as const) {
    const val = (item[key] || "").trim();
    if (!val) continue;
    if (SUMMARY_SOURCE_RE.test(val) || SUMMARY_UNIT_RE.test(val)) return true;
  }
  return false;
}

export function isReaderFacingUnit(item: VerseItem): boolean {
  return !isChapterSummaryMetaUnit(item);
}

export type CollectionFilterOption = {
  value: string;
  label: string;
  hint?: string;
  icon?: string;
};

export function uniqueCollections(items: VerseItem[]): string[] {
  const set = new Set(items.map((x) => (x.collection || "Unknown").trim()));
  return ["all", ...Array.from(set).sort((a, b) => a.localeCompare(b))];
}

export function topThemes(items: VerseItem[], limit = 16): ThemeCount[] {
  const counts = new Map<string, number>();
  for (const item of items) {
    for (const theme of item.themes || []) {
      const clean = theme?.trim();
      if (!clean) continue;
      counts.set(clean, (counts.get(clean) || 0) + 1);
    }
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .slice(0, limit)
    .map(([theme, count]) => ({ theme, count }));
}

export function countForCollection(items: VerseItem[], collection: string): number {
  const pool = preferStudyUnits(items);
  if (collection === "all") return pool.length;
  return pool.filter((x) => collectionsMatch(x.collection, collection)).length;
}

export function buildCollectionOptions(items: VerseItem[], collections: string[]): CollectionFilterOption[] {
  return collections.map((c) => ({
    value: c,
    icon: collectionIcon(c),
    label: c === "all" ? "All texts" : displayCollectionName(c),
    hint: `${countForCollection(items, c)} passages`,
  }));
}

export function buildNamedCollectionOptions(collections: string[]): CollectionFilterOption[] {
  return collections.map((c) => ({
    value: c,
    icon: collectionIcon(c),
    label: displayCollectionName(c),
  }));
}

export function buildCompareCollectionOptions(
  collections: string[],
  items: VerseItem[],
): CollectionFilterOption[] {
  return collections.map((c) => ({
    value: c,
    icon: collectionIcon(c),
    label: displayCollectionName(c),
    hint: `${countForCollection(items, c)} passages`,
  }));
}

export function passagesInCollection(items: VerseItem[], collection: string): VerseItem[] {
  const target = (collection || "").trim();
  if (!target) return [];
  return preferStudyUnits(items).filter((item) => collectionsMatch(item.collection, target));
}

export function sortComparePassages(items: VerseItem[], collection: string): VerseItem[] {
  const pool = passagesInCollection(items, collection);
  if (pool.length === 0) return pool;
  if (pool.every(isPatanjaliYogaSutras)) return sortPassagesForLibrary(pool);
  return [...pool].sort((a, b) => {
    const seqA = typeof a.sequence === "number" ? a.sequence : passageSortKey(a);
    const seqB = typeof b.sequence === "number" ? b.sequence : passageSortKey(b);
    if (seqA !== seqB) return seqA - seqB;
    return displayPassageTitle(a).localeCompare(displayPassageTitle(b));
  });
}

export function filterPassages(
  items: VerseItem[],
  opts: { q?: string; collection?: string; theme?: string; blob?: (item: VerseItem) => string },
): VerseItem[] {
  const needle = (opts.q || "").trim().toLowerCase();
  const collection = opts.collection || "all";
  const theme = opts.theme || "all";
  return preferStudyUnits(items).filter((x) => {
    if (collection !== "all" && !collectionsMatch(x.collection, collection)) return false;
    if (theme !== "all" && !(x.themes || []).includes(theme)) return false;
    if (!needle) return true;
    const blob = opts.blob ? opts.blob(x) : [x.title, x.sutra_id, x.collection].join(" ");
    return blob.toLowerCase().includes(needle);
  });
}

/** Prefer curated Zhuangzi MD units over raw chapter dumps when both exist. */
export function preferStudyUnits(items: VerseItem[]): VerseItem[] {
  const readerFacing = items.filter(isReaderFacingUnit);
  const mdChapters = new Set<number>();
  for (const item of readerFacing) {
    const m = (item._id || "").match(/zhuangzi_md_(\d+)/i);
    if (m) mdChapters.add(Number(m[1]));
  }
  if (mdChapters.size === 0) return readerFacing;
  return readerFacing.filter((item) => {
    const m = (item._id || "").match(/\.ctz_(\d+)/i);
    if (!m) return true;
    return !mdChapters.has(Number(m[1]));
  });
}
