import { collectionGlyph, type GlyphSlug } from "./glyphs";
import { displayCollectionName } from "./collectionLabels";
import { countForCollection, preferStudyUnits } from "./corpusFilters";
import type { VerseItem } from "./types";

export type LibraryTome = {
  collection: string;
  displayName: string;
  tradition: string;
  count: number;
  glyph: GlyphSlug;
  themes: string[];
};

/** Shelf sections — order is intentional (East → West → bridges). */
const TRADITION_ORDER = [
  "Vedānta",
  "Yoga",
  "Kashmir Śaiva",
  "Buddhist",
  "Daoist",
  "Greek",
  "Sufi",
  "Other",
] as const;

export type TraditionShelf = {
  tradition: string;
  tomes: LibraryTome[];
};

function traditionOf(collection: string): string {
  const c = collection.toLowerCase();
  if (/astavakra|ashtavakra|bhagavad|upanishad|upaniṣad|chandogya|isavasya|svetasvatara|mandukya/.test(c)) {
    return "Vedānta";
  }
  if (/patanjali|patañjali|yoga.?s[uū]tra/.test(c)) return "Yoga";
  if (/vijnana|bhairava|siva|śiva|shiva|spanda|pratyabhij|tantras[aā]ra/.test(c)) return "Kashmir Śaiva";
  if (/nagarjuna|heart|shantideva|milarepa|tilopa|maha.?mudra|dogen/.test(c)) return "Buddhist";
  if (/tao|te.?ching|zhuang|chuang|lao/.test(c)) return "Daoist";
  if (/heraclitus|epictetus|plotinus|phaedo|plato|ennead/.test(c)) return "Greek";
  if (/ibn|arabi|balyani|know yourself/.test(c)) return "Sufi";
  return "Other";
}

/** Build clickable tomes from loaded verses, one per collection. */
export function buildLibraryTomes(items: VerseItem[]): LibraryTome[] {
  const pool = preferStudyUnits(items);
  const byColl = new Map<string, VerseItem[]>();
  for (const item of pool) {
    const key = (item.collection || "Unknown").trim();
    if (!key) continue;
    const list = byColl.get(key) || [];
    list.push(item);
    byColl.set(key, list);
  }

  const tomes: LibraryTome[] = [];
  for (const [collection, rows] of byColl) {
    const themeCounts = new Map<string, number>();
    for (const row of rows) {
      for (const theme of row.themes || []) {
        const t = theme.trim();
        if (!t) continue;
        themeCounts.set(t, (themeCounts.get(t) || 0) + 1);
      }
    }
    const themes = [...themeCounts.entries()]
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 3)
      .map(([t]) => t);

    tomes.push({
      collection,
      displayName: displayCollectionName(collection),
      tradition: traditionOf(collection),
      count: countForCollection(items, collection),
      glyph: collectionGlyph(collection),
      themes,
    });
  }

  return tomes.sort((a, b) => a.displayName.localeCompare(b.displayName));
}

/** Group tomes into tradition shelves for the Library landing. */
export function groupTomesByTradition(tomes: LibraryTome[]): TraditionShelf[] {
  const buckets = new Map<string, LibraryTome[]>();
  for (const tome of tomes) {
    const list = buckets.get(tome.tradition) || [];
    list.push(tome);
    buckets.set(tome.tradition, list);
  }
  return TRADITION_ORDER.filter((t) => buckets.has(t)).map((tradition) => ({
    tradition,
    tomes: (buckets.get(tradition) || []).sort((a, b) => a.displayName.localeCompare(b.displayName)),
  }));
}
