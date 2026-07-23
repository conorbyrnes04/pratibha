/**
 * Maps a collection / tradition / realm name to pre-generated artwork.
 *
 * Images live in web/public/generated/<slug>.jpg (see scripts/generate_fal_images.py).
 * Each tradition has a primary thangka asset plus nature photo variants
 * (`{slug}-n01.jpg` …) that the UI rotates through for banners and thumbs.
 *
 * When a tradition has no dedicated asset, we map it to a thematically adjacent
 * existing slug rather than inventing new fal generations.
 */

function normalizeKey(name: string): string {
  return name.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();
}

const IMAGE_RULES: Array<{ pattern: RegExp; slug: string }> = [
  // Dedicated assets (order matters — more specific rules first)
  { pattern: /astavakra|ashtavakra|aṣṭāvakra/i, slug: "astavakra" },
  { pattern: /tao|te.?ching|tao_te_ching|zhuang|chuang|lao.?tzu|confucius|analect|zhongyong/i, slug: "daoism" },
  { pattern: /milarepa|jetsun|tibet.?s.?great.?yogi|rumi|mathnawi/i, slug: "milarepa" },
  { pattern: /tilopa|maha.?mudra|ganges.?mahamudra/i, slug: "tilopa" },
  { pattern: /heart.?s[uū]tra|prajnaparamita|prajñāpāramitā/i, slug: "heart-sutra" },
  { pattern: /nagarjuna|madhyamaka|mulamadhyamakakarika|mmk|dogen|dōgen|shobogenzo|shōbōgenzō/i, slug: "nagarjuna" },
  { pattern: /shantideva|śāntideva|bodhicary/i, slug: "shantideva" },
  {
    pattern: /chandogya|khandogya|khândogya|upanishad|upaniṣad|isavasya|svetasvatara|mandukya|bhagavad.?gita/i,
    slug: "upanishads",
  },
  { pattern: /vijnana|bhairava|shiva|siva|tantra|spanda|yogin[iī]|pratyabhij|utpala|somananda/i, slug: "kashmir-saiva" },
  { pattern: /heraclitus|fragment|epictetus|marcus.?aurelius|meditations\b/i, slug: "heraclitus" },
  { pattern: /patanjali|patañjali|yoga.?s[uū]tras?|raja.?yoga/i, slug: "patanjali" },
  { pattern: /plotinus|ennead|phaedo|plato|eckhart|ibn.?arabi|know.?yourself|oneness.?of.?being/i, slug: "plotinus" },
];

/** Learning-realm → artwork (Paths page / DailySit). */
const REALM_SLUGS: Record<string, string> = {
  foundations: "patanjali",
  trika: "kashmir-saiva",
  vedanta: "upanishads",
  bridges: "plotinus",
};

/** How many nature photo variants exist per base slug (`-n01` …). */
export const NATURE_VARIANT_COUNT = 3;

/** Shared overlay recipes — keep pages from inventing one-off scrims. */
export const ART_OVERLAY = {
  hero: "art-overlay art-overlay--hero",
  card: "art-overlay art-overlay--card",
  banner: "art-overlay art-overlay--banner",
  chip: "art-overlay art-overlay--chip",
} as const;

export type ArtOverlayKind = keyof typeof ART_OVERLAY;

/** Resolve a collection name to its artwork slug (always returns a valid slug). */
export function collectionImageSlug(name?: string): string {
  const raw = (name || "").trim();
  if (!raw || raw.toLowerCase() === "all") return "default";
  const key = normalizeKey(raw);
  for (const rule of IMAGE_RULES) {
    if (rule.pattern.test(raw) || rule.pattern.test(key)) return rule.slug;
  }
  return "default";
}

/** Public URL for a named page background or collection slug (e.g. "bg-hero"). */
export function generatedSrc(slug: string): string {
  return `/generated/${slug}.jpg`;
}

/** Nature photo variants for a base artwork slug (excludes the thangka primary). */
export function natureVariantSrcs(baseSlug: string): string[] {
  return Array.from({ length: NATURE_VARIANT_COUNT }, (_, i) =>
    generatedSrc(`${baseSlug}-n${String(i + 1).padStart(2, "0")}`),
  );
}

/**
 * Rotating pool for banners / thumbs: nature variants first, then the primary
 * thangka asset as a final fallback so missing nature files still render.
 */
export function collectionArtPool(name?: string): string[] {
  const slug = collectionImageSlug(name);
  return [...natureVariantSrcs(slug), generatedSrc(slug)];
}

/** Rotating pool for a named page background slug (e.g. "bg-library"). */
export function generatedArtPool(slug: string): string[] {
  return [...natureVariantSrcs(slug), generatedSrc(slug)];
}

function hashSeed(seed: string): number {
  let h = 2166136261;
  for (let i = 0; i < seed.length; i += 1) {
    h ^= seed.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return h >>> 0;
}

/** Stable pick from a pool (same seed → same image across renders). */
export function pickArtSrc(pool: string[], seed?: string): string {
  if (pool.length === 0) return generatedSrc("default");
  if (pool.length === 1) return pool[0];
  if (seed == null || seed === "") {
    return pool[Math.floor(Math.random() * pool.length)] ?? pool[0];
  }
  return pool[hashSeed(seed) % pool.length] ?? pool[0];
}

/** Public URL for a collection's artwork (optionally seeded for stable randomness). */
export function collectionImageSrc(name?: string, seed?: string): string {
  return pickArtSrc(collectionArtPool(name), seed);
}

/** Artwork for a Paths learning realm. */
export function realmImageSrc(realmId?: string, seed?: string): string {
  const slug = (realmId && REALM_SLUGS[realmId]) || "bg-paths";
  return pickArtSrc(generatedArtPool(slug), seed);
}

/** True when the collection has a dedicated (non-default) asset. */
export function hasDedicatedArt(name?: string): boolean {
  return collectionImageSlug(name) !== "default";
}
