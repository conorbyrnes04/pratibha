import type { EditorialMaturity, VerseItem } from "@/lib/types";

/** Bump when the cached shape changes so old localStorage entries are ignored.
 * v2: Patañjali regrouped from 195 single sūtras into 43 thematic clusters —
 * old cached catalogs still list the retired per-verse units, so invalidate.
 * v3: large corpus expansion (1499→2160) — Kaṭha/Śvetāśvatara/Dhammapada/
 * Epictetus completed, Marcus Books 2–12, MMK, and a new Diamond Sūtra tome —
 * so old cached catalogs miss whole collections and units.
 * v4: two new collections filling the Abrahamic gap — Ecclesiastes (Qoheleth,
 * Hebrew) and the Gospel of Thomas (Coptic).
 * v5: corpus-wide QA — 33 duplicate units removed, ~430 translations repaired via
 * independent strong-reviewer cross-check, placeholder originals suppressed.
 * v7: Yoruba + Dakota living-tradition tomes on the default Library shelf.
 * v8: two new collections — A Course in Miracles (Original Edition) and Kabbalah
 * (Sefer Yetzirah & the Zohar), each enriched with a Red Book hero mandala.
 * v9: Yoga shelf grows — Haṭha Yoga Pradīpikā (Pañcham Sinh) and Śiva Saṃhitā
 * (Vasu), each with a hero mandala; A Course in Miracles expanded (33→57).
 * v10: Lal Ded (Lallā Vākyāni) — 32 vakhs, ten hero verses, Red Book mandala.
 * v12: Gospel of Mary (BG 8502) + Logia of Jesus (Nestle 1904) — living sayings family.
 * v13: Gospel of Mary expanded 12→26 argument-arc units (still no invented lacunae).
 * v14: Sufi wave — Attar Conference of the Birds, Hujwīrī Kashf al-Maḥjūb,
 * and enriched Know Yourself (Balyānī).
 * v15: /verses is preview-only (no pratibha_layers) — drop fat v14 snapshots.
 * v16: Senegalese living speech — Serer cosaan, Fulɓe pastoral remnant, Gaden 1913 Pulaar. */
const CACHE_VERSION = 16;
const TTL_MS = 24 * 60 * 60 * 1000;

export type CatalogMaturityKey = "strong_draft" | "all";

type CacheEnvelope<T> = {
  v: number;
  savedAt: number;
  items: T[];
};

export type CatalogCacheHit<T> = {
  savedAt: number;
  items: T[];
  /** True when older than TTL — still safe to render while revalidating. */
  stale: boolean;
};

function versesStorageKey(maturity: CatalogMaturityKey): string {
  return `pratibha.catalog.verses.v${CACHE_VERSION}.${maturity}`;
}

function collectionsStorageKey(): string {
  return `pratibha.catalog.collections.v${CACHE_VERSION}`;
}

/** Map API maturity filter onto the two cache buckets the Library uses. */
export function catalogMaturityKey(minMaturity?: EditorialMaturity | "all"): CatalogMaturityKey {
  return minMaturity === "all" ? "all" : "strong_draft";
}

function readEnvelope<T>(key: string): CatalogCacheHit<T> | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(key);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as CacheEnvelope<T>;
    if (!parsed || parsed.v !== CACHE_VERSION || !Array.isArray(parsed.items)) return null;
    if (typeof parsed.savedAt !== "number") return null;
    return {
      savedAt: parsed.savedAt,
      items: parsed.items,
      stale: Date.now() - parsed.savedAt > TTL_MS,
    };
  } catch {
    return null;
  }
}

function catalogKeys(): string[] {
  if (typeof window === "undefined") return [];
  const keys: string[] = [];
  for (let i = 0; i < localStorage.length; i += 1) {
    const key = localStorage.key(i);
    if (key?.startsWith("pratibha.catalog.")) keys.push(key);
  }
  return keys;
}

function isCurrentCatalogKey(key: string): boolean {
  return (
    key === collectionsStorageKey() ||
    key === versesStorageKey("strong_draft") ||
    key === versesStorageKey("all")
  );
}

/** Drop superseded catalog snapshots (v1–v13, …) that still occupy the origin quota. */
export function evictStaleCatalogCaches(): number {
  let removed = 0;
  for (const key of catalogKeys()) {
    if (isCurrentCatalogKey(key)) continue;
    localStorage.removeItem(key);
    removed += 1;
  }
  return removed;
}

/** Drop every catalog cache, including the current version — Library will refetch. */
export function dropCatalogCaches(): number {
  let removed = 0;
  for (const key of catalogKeys()) {
    localStorage.removeItem(key);
    removed += 1;
  }
  return removed;
}

function writeEnvelope<T>(key: string, items: T[]): void {
  if (typeof window === "undefined") return;
  const envelope: CacheEnvelope<T> = {
    v: CACHE_VERSION,
    savedAt: Date.now(),
    items,
  };
  const raw = JSON.stringify(envelope);
  try {
    evictStaleCatalogCaches();
    localStorage.setItem(key, raw);
  } catch {
    dropCatalogCaches();
    try {
      localStorage.setItem(key, raw);
    } catch {
      // Quota / private mode — catalog still works without persistence.
    }
  }
}

export function readCatalogCache(maturity: CatalogMaturityKey): CatalogCacheHit<VerseItem> | null {
  return readEnvelope<VerseItem>(versesStorageKey(maturity));
}

export function writeCatalogCache(maturity: CatalogMaturityKey, items: VerseItem[]): void {
  writeEnvelope(versesStorageKey(maturity), items);
}

export function readCollectionsCache(): CatalogCacheHit<string> | null {
  return readEnvelope<string>(collectionsStorageKey());
}

export function writeCollectionsCache(items: string[]): void {
  writeEnvelope(collectionsStorageKey(), items);
}
