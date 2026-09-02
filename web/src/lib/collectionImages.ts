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
  { pattern: /heart.?s[uū]tra|prajnaparamita|prajñāpāramitā|vajracchedika|vajracchedikā|diamond.?s[uū]tra/i, slug: "heart-sutra" },
  { pattern: /nagarjuna|madhyamaka|mulamadhyamakakarika|mmk|dogen|dōgen|shobogenzo|shōbōgenzō/i, slug: "nagarjuna" },
  { pattern: /shantideva|śāntideva|bodhicary/i, slug: "shantideva" },
  {
    pattern: /chandogya|khandogya|khândogya|upanishad|upaniṣad|isavasya|svetasvatara|mandukya|bhagavad.?gita/i,
    slug: "upanishads",
  },
  { pattern: /vijnana|bhairava|shiva|siva|tantra|spanda|yogin[iī]|pratyabhij|utpala|somananda/i, slug: "kashmir-saiva" },
  { pattern: /heraclitus|fragment|epictetus|marcus.?aurelius|meditations\b|stoic/i, slug: "heraclitus" },
  { pattern: /patanjali|patañjali|yoga.?s[uū]tras?|raja.?yoga/i, slug: "patanjali" },
  { pattern: /plotinus|ennead|phaedo|plato|eckhart|dionysius|areopagite|cloud.?of.?unknowing|christian.?mystic|ibn.?arabi|know.?yourself|oneness.?of.?being|ecclesiastes|qoheleth|gospel.?of.?thomas|gospel.?of.?mary|logia of jesus|new.?testament.?logia|kabbalah|zohar|yetzirah|eastman|soul of the indian|dakota/i, slug: "plotinus" },
  { pattern: /parmenides/i, slug: "heraclitus" },
];

/** Learning-realm → artwork (Paths page / DailySit). */
const REALM_SLUGS: Record<string, string> = {
  foundations: "patanjali",
  trika: "kashmir-saiva",
  vedanta: "upanishads",
  "letting-go": "plotinus",
  tao: "daoism",
  hellenic: "plotinus",
  stoic: "heraclitus",
  christian: "plotinus",
  bridges: "plotinus",
  "yoga-dharma": "patanjali",
  sufi: "milarepa",
  confucian: "daoism",
  kabbalah: "plotinus",
  qoheleth: "plotinus",
  presocratic: "heraclitus",
  dakota: "plotinus",
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
 * Red Book (Jungian / Liber Novus) collection art — one illuminated image per
 * collection, from scripts/generate_numinos_art.py → /generated/redbook/<slug>.jpg.
 * When a collection matches, its Red Book image IS the artwork (no nature-photo
 * rotation), re-skinning the library in the illuminated-manuscript style.
 * Order mirrors the generator manifest; more specific patterns first.
 */
const REDBOOK_RULES: Array<{ pattern: RegExp; slug: string }> = [
  { pattern: /gospel.?of.?mary/i, slug: "gospel_of_mary" },
  { pattern: /attar|mantiq|conference.?of.?the.?birds/i, slug: "conference_of_the_birds" },
  { pattern: /hujwir|kashf.?al.?ma[hḥ]jub/i, slug: "kashf_al_mahjub" },
  { pattern: /logia of jesus|new.?testament.?logia/i, slug: "new_testament_logia" },
  { pattern: /course in miracles|acim/i, slug: "a_course_in_miracles" },
  { pattern: /psalm|tehillim|psalter/i, slug: "psalms_tehillim" },
  { pattern: /lalla|lal.?ded|lalleshwari|vakyani|vākyāni/i, slug: "lalla_vakyani" },
  { pattern: /kabbalah|zohar|yetzirah|sephiroth|sefirot/i, slug: "kabbalah_zohar_yetzirah" },
  { pattern: /ha[tṭ]ha|pradipika|pradīpikā/i, slug: "hatha_yoga_pradipika" },
  { pattern: /[sś]iva.?sa[mṃ]hit[aā]|shiva.?samhita/i, slug: "siva_samhita" },
  { pattern: /a[sṣ]t[aā]vakra|ashtavakra/i, slug: "astavakra_gita" },
  { pattern: /bhagavad/i, slug: "bhagavad_gita" },
  { pattern: /brihadaranyaka|b[rṛ]had[aā]ra[nṇ]yaka/i, slug: "brihadaranyaka_upanishad" },
  { pattern: /ch[aā]ndogya|khandogya/i, slug: "chandogya_upanishad" },
  { pattern: /confucius|analect/i, slug: "confucius_analects" },
  { pattern: /dhammapada/i, slug: "dhammapada" },
  { pattern: /d[oō]gen|shobogenzo|sh[oō]b[oō]genz[oō]/i, slug: "dogen_shobogenzo" },
  { pattern: /soul of the indian|eastman|ohiyesa/i, slug: "eastman_soul_of_the_indian" },
  { pattern: /ecclesiastes|qoheleth/i, slug: "ecclesiastes_qoheleth" },
  { pattern: /epictetus/i, slug: "epictetus_works" },
  { pattern: /gospel of thomas|thomas/i, slug: "gospel_of_thomas" },
  { pattern: /heart.?s[uū]tra|vajracchedik|diamond.?s[uū]tra|prajn[aā]p[aā]ramit[aā]/i, slug: "heart_sutra" },
  { pattern: /heraclitus/i, slug: "heraclitus_fragments" },
  { pattern: /isavasya|[iī][sś][aā]v[aā]sya|isha.?upani/i, slug: "isavasya_upanishad" },
  { pattern: /katha|ka[tṭ]ha/i, slug: "katha_upanishad" },
  { pattern: /ibn|arabi|know yourself|balyani/i, slug: "ibn_arabi" },
  { pattern: /mandukya|m[aā][nṇ][dḍ][uū]kya|gaudapada|gau[dḍ]ap[aā]da/i, slug: "mandukya_upanishad" },
  { pattern: /marcus|meditations|aurelius/i, slug: "marcus_aurelius" },
  { pattern: /eckhart/i, slug: "meister_eckhart" },
  { pattern: /milarepa/i, slug: "milarepa_songs" },
  { pattern: /mundaka|mu[nṇ][dḍ]aka/i, slug: "mundaka_upanishad" },
  { pattern: /nagarjuna|n[aā]g[aā]rjuna|madhyamaka|mulamadhyamaka/i, slug: "nagarjuna" },
  { pattern: /parmenides/i, slug: "parmenides" },
  { pattern: /patanjali|pata[nñ]jali|yoga.?s[uū]tra/i, slug: "patanjali_yoga_sutras" },
  { pattern: /phaedo|plato/i, slug: "phaedo_plato" },
  { pattern: /plotinus|ennead/i, slug: "plotinus_enneads" },
  { pattern: /pratyabhij/i, slug: "pratyabhijnahrdayam" },
  { pattern: /dionysius|divine names/i, slug: "pseudo_dionysius" },
  { pattern: /rumi|r[uū]m[iī]|mathnawi|mathnaw[iī]/i, slug: "rumi_mathnawi" },
  { pattern: /shantideva|[sś][aā]ntideva|bodhicary/i, slug: "shantideva" },
  { pattern: /siva.?s[uū]tra|[sś]iva.?s[uū]tra|shiva.?sutra/i, slug: "siva_sutra" },
  { pattern: /svetasvatara|[sś]vet[aā][sś]vatara/i, slug: "svetasvatara_upanishad" },
  { pattern: /tantras[aā]ra|abhinavagupta/i, slug: "tantrasara" },
  { pattern: /tao|te.?ching|lao.?tzu/i, slug: "tao_te_ching" },
  { pattern: /chuang|zhuang/i, slug: "chuang_tzu" },
  { pattern: /cloud of unknowing/i, slug: "cloud_of_unknowing" },
  { pattern: /tilopa|maha.?mudra/i, slug: "tilopa_mahamudra" },
  { pattern: /vijnana|bhairava|vij[nñ][aā]na/i, slug: "vijnana_bhairava" },
  { pattern: /spanda/i, slug: "yoga_spandakarika" },
  { pattern: /yogin[iī]h[rṛ]daya|yogini.?hrdaya|heart of the yogini/i, slug: "yoginihrdaya" },
  { pattern: /samuel johnson|yoruba faith|johnson.?yoruba/i, slug: "johnson_yoruba_religion" },
  { pattern: /yoruba|[oò]we/i, slug: "yoruba_proverbs" },
  { pattern: /zhongyong/i, slug: "zhongyong" },
  { pattern: /old indian legends|zitkala/i, slug: "zitkala_sa_legends" },
];

/** Red Book image slug for a collection, or null if none matches. */
export function redbookSlug(name?: string): string | null {
  const raw = (name || "").trim();
  if (!raw) return null;
  const key = normalizeKey(raw);
  for (const rule of REDBOOK_RULES) {
    if (rule.pattern.test(raw) || rule.pattern.test(key)) return rule.slug;
  }
  return null;
}

export function redbookSrc(slug: string): string {
  return `/generated/redbook/${slug}.jpg`;
}

/**
 * Rotating pool for banners / thumbs. Prefers the collection's Red Book image
 * (single, no rotation); otherwise nature variants + the thangka primary.
 */
export function collectionArtPool(name?: string): string[] {
  const rb = redbookSlug(name);
  if (rb) return [redbookSrc(rb)];
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
