/** Curated Mythra Glyphnet symbols shipped under /public/glyphs. */

export const GLYPH_SLUGS = [
  "lotus",
  "eye",
  "gateway",
  "diamond",
  "key",
  "spiral",
  "infinity",
  "mandala",
  "labyrinth",
  "moon",
  "sun",
  "star",
  "fire",
  "water",
  "dragon",
  "serpent",
  "phoenix",
  "mirror",
  "chalice",
  "sage",
  "hermit",
  "mountain",
  "tree",
  "shiva",
  "vishnu",
  "ganesha",
  "athena",
  "flower",
  "yantra",
] as const;

export type GlyphSlug = (typeof GLYPH_SLUGS)[number];

export function glyphSrc(slug: GlyphSlug): string {
  return `/glyphs/${slug}.svg`;
}

function normalizeKey(name: string): string {
  return name.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();
}

/** Map a corpus text / tradition name to a glyph (or null to keep letter icons). */
const GLYPH_RULES: Array<{ pattern: RegExp; glyph: GlyphSlug }> = [
  { pattern: /tao|te.?ching|tao_te_ching|zhuang|chuang|lao.?tzu|chuang_tzu/i, glyph: "dragon" },
  { pattern: /bhagavad|gita/i, glyph: "vishnu" },
  { pattern: /epictetus/i, glyph: "sage" },
  { pattern: /phaedo|plato/i, glyph: "athena" },
  { pattern: /plotinus|ennead/i, glyph: "infinity" },
  { pattern: /milarepa|jetsun.?kahbum|tibet.?s.?great.?yogi/i, glyph: "mountain" },
  { pattern: /tilopa|maha.?mudra|ganges.?mahamudra/i, glyph: "diamond" },
  { pattern: /heart.?s[uū]tra|prajnaparamita|prajñāpāramitā/i, glyph: "lotus" },
  { pattern: /nagarjuna|madhyamaka|mulamadhyamakakarika|mmk/i, glyph: "diamond" },
  { pattern: /shantideva|śāntideva|bodhicary/i, glyph: "lotus" },
  { pattern: /chandogya|khandogya|khândogya/i, glyph: "sun" },
  { pattern: /upanishad|isavasya|svetasvatara|mandukya/i, glyph: "yantra" },
  { pattern: /vijnana|bhairava|shiva|siva|tantra|spanda|yogin[iī]|yogini_hrdaya|pratyabhij/i, glyph: "shiva" },
  { pattern: /heraclitus|fragment/i, glyph: "fire" },
  { pattern: /patanjali|patañjali|yoga.?s[uū]tras?|raja.?yoga/i, glyph: "spiral" },
  { pattern: /ibn|arabi|know yourself/i, glyph: "mirror" },
  { pattern: /confucius|analect/i, glyph: "tree" },
  { pattern: /marcus|meditation/i, glyph: "sage" },
  { pattern: /rumi|poet/i, glyph: "spiral" },
  { pattern: /dogen|dōgen|shobogenzo|shōbōgenzō/i, glyph: "moon" },
  { pattern: /eckhart|meister_eckhart|abegescheidenheit|abgeschiedenheit/i, glyph: "chalice" },
];

export function collectionGlyph(name?: string): GlyphSlug {
  const raw = (name || "").trim();
  if (!raw || raw.toLowerCase() === "all") return "lotus";
  const key = normalizeKey(raw);
  for (const rule of GLYPH_RULES) {
    if (rule.pattern.test(raw) || rule.pattern.test(key)) return rule.glyph;
  }
  return "diamond";
}

/** Home gateway / section ornaments. */
export const GATEWAY_GLYPHS = {
  archive: "gateway",
  dialogue: "eye",
  oracle: "star",
  curriculum: "labyrinth",
} as const satisfies Record<string, GlyphSlug>;
