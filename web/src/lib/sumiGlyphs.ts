/**
 * Sumi-e ink marks shipped under /public/sumi.
 *
 * These are flat black potrace fills — designed to be recolored via CSS
 * mask (see components/InkGlyph.tsx), never rendered as raw black-on-white
 * <img> like the Mythra Glyphnet set in lib/glyphs.ts. In the Sumi/Spanda
 * system the dark UI is the void (anuttara); the ink glyph is ābhāsa, the
 * "shining forth," so it is always painted in a state color — ash, bone, or
 * gold — never left as source-black.
 */

export const SUMI_SLUGS = [
  "air",
  "anubis",
  "apollo",
  "artemis",
  "athena",
  "bear",
  "bee",
  "brahma",
  "butterfly",
  "celtic_key",
  "celtic_star",
  "chalice",
  "circle",
  "comet",
  "constellation",
  "crane",
  "cross",
  "crow",
  "deer",
  "desert",
  "dionysus",
  "dolphin",
  "dragon",
  "durga",
  "eagle",
  "earth",
  "elephant",
  "eros",
  "eye",
  "fire",
  "fish",
  "fool",
  "fox",
  "freyja",
  "ganesha",
  "hades",
  "hawk",
  "heart",
  "hera",
  "hermit",
  "horse",
  "horus",
  "infinity",
  "isis",
  "kali",
  "king",
  "labyrinth",
  "lakshmi",
  "lightning",
  "lion",
  "loki",
  "lotus",
  "maiden",
  "mandala",
  "mirror",
  "moon",
  "mother",
  "mountain",
  "mushroom",
  "nuwa",
  "oak",
  "ocean",
  "odin",
  "oshun",
  "osiris",
  "owl",
  "ox",
  "persephone",
  "play",
  "quetzalcoatl",
  "rainbow",
  "raven",
  "rose",
  "sage",
  "saraswati",
  "serpent",
  "shaman",
  "shango",
  "shiva",
  "spider",
  "spiral",
  "stag",
  "star",
  "storm",
  "sun",
  "swan",
  "tezcatlipoca",
  "thanatos",
  "thor",
  "thoth",
  "thunderbird",
  "tides",
  "tiger",
  "tree",
  "triangle",
  "turtle",
  "vine",
  "vishnu",
  "void",
  "volcano",
  "warrior",
  "water",
  "whale",
  "wolf",
  "yantra",
  "yemaya",
  "yin_yang",
  "zeus",
] as const;

export type SumiSlug = (typeof SUMI_SLUGS)[number];

export function sumiSrc(slug: SumiSlug | string): string {
  return `/sumi/${slug}.svg`;
}

function normalizeKey(name: string): string {
  return name.normalize("NFD").replace(/\p{M}/gu, "").toLowerCase();
}

/**
 * Map a corpus text / tradition name to a sumi mark. Mirrors the shape of
 * GLYPH_RULES in lib/glyphs.ts, but every target is constrained to a slug
 * that actually exists in SUMI_SLUGS (the sumi set is much smaller than the
 * Glyphnet set, so several picks stand in for an unavailable "ideal" glyph —
 * each of those is called out with a comment).
 */
const SUMI_RULES: Array<{ pattern: RegExp; glyph: SumiSlug }> = [
  { pattern: /tao|te.?ching|tao_te_ching|zhuang|chuang|lao.?tzu|chuang_tzu/i, glyph: "dragon" },
  { pattern: /astavakra|ashtavakra|a[sṣ][tṭ][aā]vakra/i, glyph: "hermit" },
  { pattern: /bhagavad/i, glyph: "vishnu" },
  { pattern: /epictetus/i, glyph: "sage" },
  { pattern: /phaedo|plato/i, glyph: "athena" },
  { pattern: /plotinus|ennead/i, glyph: "infinity" },
  { pattern: /milarepa|jetsun.?kahbum|tibet.?s.?great.?yogi/i, glyph: "mountain" },
  { pattern: /tilopa|maha.?mudra|ganges.?mahamudra/i, glyph: "water" },
  { pattern: /heart.?s[uū]tra|prajnaparamita|prajñāpāramitā/i, glyph: "lotus" },
  { pattern: /nagarjuna|madhyamaka|mulamadhyamakakarika|mmk/i, glyph: "void" },
  { pattern: /shantideva|śāntideva|bodhicary/i, glyph: "heart" },
  { pattern: /chandogya|khandogya|khândogya/i, glyph: "sun" },
  { pattern: /isavasya|īśāvāsya|isha.?upani/i, glyph: "circle" },
  { pattern: /svetasvatara|śvetāśvatara/i, glyph: "fire" },
  { pattern: /mandukya|māṇḍūkya|gaudapada|gauḍapāda/i, glyph: "moon" },
  { pattern: /katha|ka[tṭ]ha/i, glyph: "thanatos" },
  { pattern: /brihad|b[rṛ]had[aā]ra[nṇ]yaka/i, glyph: "sun" },
  { pattern: /mundaka|mu[nṇ][dḍ]aka/i, glyph: "yantra" },
  { pattern: /upanishad|upaniṣad/i, glyph: "yantra" },
  { pattern: /vijnana|bhairava|vijñāna.?bhairava/i, glyph: "eye" },
  { pattern: /lalla|lal.?ded|lalleshwari|vakyani|vākyāni/i, glyph: "fire" },
  { pattern: /pratyabhij/i, glyph: "mirror" },
  { pattern: /spanda/i, glyph: "tides" },
  { pattern: /tantras[aā]ra|abhinavagupta/i, glyph: "yantra" },
  { pattern: /yogin[iī]h[rṛ]daya|yogini.?hrdaya|heart of the yogini/i, glyph: "yantra" },
  { pattern: /siva.?s[uū]tra|śiva.?s[uū]tra|shiva.?sutra/i, glyph: "shiva" },
  { pattern: /vijnana|bhairava|shiva|siva|tantra|spanda|yogin[iī]|yogini_hrdaya|pratyabhij/i, glyph: "shiva" },
  { pattern: /heraclitus|fragment/i, glyph: "fire" },
  { pattern: /patanjali|patañjali|yoga.?s[uū]tras?|raja.?yoga/i, glyph: "spiral" },
  { pattern: /ibn|arabi|know yourself/i, glyph: "mirror" },
  { pattern: /attar|mantiq|conference.?of.?the.?birds/i, glyph: "crane" },
  { pattern: /hujwir|kashf.?al.?ma[hḥ]jub/i, glyph: "eye" },
  { pattern: /confucius|analect|zhongyong/i, glyph: "tree" },
  { pattern: /marcus|meditation/i, glyph: "sage" },
  { pattern: /rumi|poet/i, glyph: "spiral" },
  { pattern: /dogen|dōgen|shobogenzo|shōbōgenzō/i, glyph: "moon" },
  { pattern: /eckhart|meister_eckhart|abegescheidenheit|abgeschiedenheit/i, glyph: "chalice" },
  { pattern: /dhammapada|dhammapāda/i, glyph: "tree" },
  { pattern: /cloud.?of.?unknowing/i, glyph: "void" },
  { pattern: /parmenides/i, glyph: "circle" },
  { pattern: /dionysius|areopagite|mystical.?theology|divine.?names/i, glyph: "chalice" },
  { pattern: /gospel.?of.?mary/i, glyph: "chalice" },
  { pattern: /logia of jesus|new.?testament.?logia/i, glyph: "cross" },
  { pattern: /gospel.?of.?thomas/i, glyph: "cross" },
  { pattern: /psalm|tehillim|psalter/i, glyph: "sun" },
  { pattern: /ecclesiastes|qoheleth/i, glyph: "sage" },
  { pattern: /pulaar.?texts|gaden|le.?poular/i, glyph: "horse" },
  { pattern: /pulaar.?tradition|ful[bɓ]e|peul/i, glyph: "ox" },
  { pattern: /senegalese.?animism|serer|pangool|roog/i, glyph: "oak" },
  { pattern: /yoruba|orisha|[oò]r[iì][sṣ][aà]/i, glyph: "oshun" },
];

/** Tradition family marks when a text has no more specific resonance. */
export const TRADITION_SUMI: Record<string, SumiSlug> = {
  "Vedānta": "swan",
  "Yoga": "spiral",
  "Kashmir Śaiva": "shiva",
  "Buddhist": "lotus",
  "Daoist": "yin_yang",
  "Confucian": "oak",
  "Yoruba": "oshun",
  "Serer": "oak",
  "Pulaar": "ox",
  "Dakota": "thunderbird",
  "Hebrew": "sage",
  "Greek": "athena",
  "Christian": "chalice",
  "Sufi": "rose",
};

export function traditionSumiGlyph(tradition?: string): SumiSlug {
  const raw = (tradition || "").trim();
  if (!raw) return "circle";
  const exact = TRADITION_SUMI[raw];
  if (exact) return exact;
  const key = normalizeKey(raw);
  for (const [label, glyph] of Object.entries(TRADITION_SUMI)) {
    if (normalizeKey(label) === key) return glyph;
  }
  return "circle";
}

function asSumiGlyph(slug: string): SumiSlug {
  return (SUMI_SLUGS as readonly string[]).includes(slug) ? (slug as SumiSlug) : "circle";
}

/**
 * Verse-level images. Specific names outrank common words. Title / themes /
 * key terms count triple; the translation is a weaker signal. Commentary is
 * ignored so a long gloss cannot steal the mark.
 */
const SEMANTIC_RULES: Array<{ pattern: RegExp; glyph: SumiSlug; weight: number }> = [
  { pattern: /\bbutterfly|蝴蝶|hu.?tie/i, glyph: "butterfly", weight: 3 },
  { pattern: /\bdolphin/i, glyph: "dolphin", weight: 3 },
  { pattern: /\bdragon|long mai|naga raja|nāgarāja/i, glyph: "dragon", weight: 3 },
  { pattern: /\beagle|garuda|garu[dḍ]a/i, glyph: "eagle", weight: 3 },
  { pattern: /\belephant|gaja|airavata/i, glyph: "elephant", weight: 3 },
  { pattern: /\bfox\b|kitsune/i, glyph: "fox", weight: 3 },
  { pattern: /\bhorse|a[sś]va|steed|chariot.?horse/i, glyph: "horse", weight: 3 },
  { pattern: /\blion|si[mṃ]ha|narasimha/i, glyph: "lion", weight: 3 },
  { pattern: /\bowl\b/i, glyph: "owl", weight: 3 },
  { pattern: /\braven/i, glyph: "raven", weight: 3 },
  { pattern: /\bcrow\b/i, glyph: "crow", weight: 3 },
  { pattern: /\bserpent|n[aā]ga|kundalin[iī]|snake/i, glyph: "serpent", weight: 3 },
  { pattern: /\bspider/i, glyph: "spider", weight: 3 },
  { pattern: /\bstag\b|antler/i, glyph: "stag", weight: 3 },
  { pattern: /\bdeer\b|doe\b|m[rṛ]ga/i, glyph: "deer", weight: 3 },
  { pattern: /\bturtle|tortoise|k[uū]rma/i, glyph: "turtle", weight: 3 },
  { pattern: /\bwhale/i, glyph: "whale", weight: 3 },
  { pattern: /\bwolf|wolves/i, glyph: "wolf", weight: 3 },
  { pattern: /\bbear\b/i, glyph: "bear", weight: 3 },
  { pattern: /\bbee\b|honeybee|madhu/i, glyph: "bee", weight: 3 },
  { pattern: /\bcrane\b/i, glyph: "crane", weight: 3 },
  { pattern: /\bfish\b|matsya|carp|koi\b/i, glyph: "fish", weight: 3 },
  { pattern: /\bhawk\b|falcon/i, glyph: "hawk", weight: 3 },
  { pattern: /\box\b|buffalo|nandi|v[rṛ][sṣ]a/i, glyph: "ox", weight: 3 },
  { pattern: /\bswan\b|ha[mṃ]sa/i, glyph: "swan", weight: 3 },
  { pattern: /\btiger\b|vy[aā]ghra/i, glyph: "tiger", weight: 3 },
  { pattern: /ga[nṇ]e[sś][ah]|ganapati/i, glyph: "ganesha", weight: 3 },
  { pattern: /\bk[aā]l[iī]\b|mah[aā]k[aā]l[iī]/i, glyph: "kali", weight: 3 },
  { pattern: /\bdurg[aā]\b/i, glyph: "durga", weight: 3 },
  { pattern: /\blak[sṣ]m[iī]/i, glyph: "lakshmi", weight: 3 },
  { pattern: /sarasvat[iī]/i, glyph: "saraswati", weight: 3 },
  { pattern: /\bvi[sṣ][nṇ]u|k[rṛ][sṣ][nṇ]a|n[aā]r[aā]ya[nṇ]a/i, glyph: "vishnu", weight: 3 },
  { pattern: /\b[sś]iva\b|bhairava|rudra|trident|tri[sś][uū]la/i, glyph: "shiva", weight: 3 },
  { pattern: /\bbrahma\b/i, glyph: "brahma", weight: 3 },
  { pattern: /\bathena|pallas/i, glyph: "athena", weight: 3 },
  { pattern: /\bapollo|lyre\b/i, glyph: "apollo", weight: 3 },
  { pattern: /\bartemis/i, glyph: "artemis", weight: 3 },
  { pattern: /\bzeus\b/i, glyph: "zeus", weight: 3 },
  { pattern: /\bdionysus|bacchus|thyrsus/i, glyph: "dionysus", weight: 3 },
  { pattern: /\bhades\b/i, glyph: "hades", weight: 3 },
  { pattern: /\bpersephone|pomegranate/i, glyph: "persephone", weight: 3 },
  { pattern: /\beros\b|cupid/i, glyph: "eros", weight: 3 },
  { pattern: /\bodin\b/i, glyph: "odin", weight: 3 },
  { pattern: /\bthor\b|mjolnir/i, glyph: "thor", weight: 3 },
  { pattern: /\banubis/i, glyph: "anubis", weight: 3 },
  { pattern: /\bhorus|wedjat/i, glyph: "horus", weight: 3 },
  { pattern: /\bthoth\b/i, glyph: "thoth", weight: 3 },
  { pattern: /\bisis\b/i, glyph: "isis", weight: 3 },
  { pattern: /\bosiris/i, glyph: "osiris", weight: 3 },
  { pattern: /\b[sś][uū]nyat[aā]|emptiness|empty of|voidness|nothingness|\bvoid\b/i, glyph: "void", weight: 3 },
  { pattern: /\byin.?yang|tai.?ji/i, glyph: "yin_yang", weight: 3 },
  { pattern: /\bthunderbird/i, glyph: "thunderbird", weight: 3 },
  { pattern: /\bquetzalcoatl|feathered serpent/i, glyph: "quetzalcoatl", weight: 3 },
  { pattern: /\bagni\b|flame|blaze|conflagration|heraclitean fire/i, glyph: "fire", weight: 2 },
  { pattern: /\bthunderbolt|lightning|vajra|indra.?s bolt/i, glyph: "lightning", weight: 2 },
  { pattern: /\bocean|sea\b|samudra|tide/i, glyph: "ocean", weight: 2 },
  { pattern: /\bmountain|himalay|kail[aā]sa|sumeru|meru\b/i, glyph: "mountain", weight: 2 },
  { pattern: /\bmoon\b|candra|lunar|full.?moon/i, glyph: "moon", weight: 2 },
  { pattern: /\bsun\b|s[uū]rya|[aā]ditya|solar/i, glyph: "sun", weight: 2 },
  { pattern: /\blotus|padma|pu[nṇ][dḍ]ar[iī]ka/i, glyph: "lotus", weight: 2 },
  { pattern: /\bmirror|darpana|pratibimba/i, glyph: "mirror", weight: 2 },
  { pattern: /\byantra\b/i, glyph: "yantra", weight: 2 },
  { pattern: /\bmandala\b/i, glyph: "mandala", weight: 2 },
  { pattern: /\beye\b|netra|witness|dra[sṣ][tṭ][aā]|seer\b/i, glyph: "eye", weight: 2 },
  { pattern: /\bchalice|grail|wine.?cup/i, glyph: "chalice", weight: 2 },
  { pattern: /\bwarrior|arjuna|k[sṣ]atriya|battlefield|kuruk[sṣ]etra/i, glyph: "warrior", weight: 2 },
  { pattern: /\bhermit|solitude|cave.?dweller|retreat/i, glyph: "hermit", weight: 2 },
  { pattern: /\bsage\b|[rṛ][sṣ]i\b|teacher of/i, glyph: "sage", weight: 2 },
  { pattern: /\binfinit|ananta|apeiron/i, glyph: "infinity", weight: 2 },
  { pattern: /\bspiral|ku[nṇ][dḍ]alin[iī] coil/i, glyph: "spiral", weight: 2 },
  { pattern: /\bstorm\b|tempest/i, glyph: "storm", weight: 2 },
  { pattern: /\bwater|river|ga[nṅ]g[aā]|apas\b/i, glyph: "water", weight: 1 },
  { pattern: /\bheart\b|h[rṛ]daya/i, glyph: "heart", weight: 1 },
  { pattern: /\btree\b|bodhi tree|a[sś]vattha|world.?tree/i, glyph: "tree", weight: 1 },
  { pattern: /\bfire\b|burn(ing|s)?\b/i, glyph: "fire", weight: 1 },
];

export type VerseGlyphInput = {
  collection?: string;
  tradition?: string;
  title?: string;
  thesis?: string;
  translation?: string;
  themes?: string[];
  keyTerms?: string[];
};

function semanticHaystacks(input: VerseGlyphInput): { tight: string; body: string } {
  return {
    tight: [input.title, input.thesis, ...(input.themes || []), ...(input.keyTerms || [])]
      .filter(Boolean)
      .join(" \n "),
    body: (input.translation || "").slice(0, 800),
  };
}

/** Best verse-level mark, or undefined when nothing in the passage is specific enough. */
export function semanticSumiGlyph(input: VerseGlyphInput): SumiSlug | undefined {
  const { tight, body } = semanticHaystacks(input);
  if (!tight && !body) return undefined;
  let best: { glyph: SumiSlug; score: number } | undefined;
  for (const rule of SEMANTIC_RULES) {
    let score = 0;
    if (tight && rule.pattern.test(tight)) score += rule.weight * 3;
    else if (body && rule.pattern.test(body)) score += rule.weight;
    if (!score) continue;
    if (!best || score > best.score) best = { glyph: rule.glyph, score };
  }
  if (!best || best.score < 3) return undefined;
  return asSumiGlyph(best.glyph);
}

/** Verse image if one resonates; otherwise the collection, then the tradition. */
export function verseSumiGlyph(input: VerseGlyphInput): SumiSlug {
  return semanticSumiGlyph(input) || sumiGlyph(input.collection, input.tradition);
}

/** Map a corpus text / tradition name to a preferred sumi mark. */
export function sumiGlyph(name?: string, tradition?: string): SumiSlug {
  const raw = (name || "").trim();
  if (raw && raw.toLowerCase() !== "all") {
    const key = normalizeKey(raw);
    for (const rule of SUMI_RULES) {
      if (rule.pattern.test(raw) || rule.pattern.test(key)) return asSumiGlyph(rule.glyph);
    }
  }
  if (tradition) return traditionSumiGlyph(tradition);
  if (!raw || raw.toLowerCase() === "all") return "lotus";
  return "circle";
}

/** Landscape / strip plates that collapse in a circular trail well. */
const TRAIL_UNSUITABLE = new Set<SumiSlug>([
  "celtic_key",
  "desert",
  "eye",
  "fire",
  "infinity",
  "lightning",
  "mother",
  "mushroom",
  "owl",
  "rose",
  "stag",
  "vine",
]);

const TRAIL_SUMI_SLUGS = SUMI_SLUGS.filter((slug) => !TRAIL_UNSUITABLE.has(slug));

function hashToSlug(seed: string, slugs: readonly SumiSlug[]): SumiSlug {
  const key = seed.trim() || "pratibha";
  let h = 2166136261;
  for (let i = 0; i < key.length; i += 1) {
    h ^= key.charCodeAt(i);
    h = Math.imul(h, 16777619);
  }
  return slugs[Math.abs(h) % slugs.length]!;
}

/** Stable "random" sumi mark for a passage — same id always gets the same mark. */
export function unitSumiGlyph(seed?: string): SumiSlug {
  return hashToSlug(seed || "", SUMI_SLUGS);
}

/** Trail nodes sit in a circle — skip landscape plates that smear into a sliver. */
export function trailSumiGlyph(seed?: string): SumiSlug {
  return hashToSlug(seed || "", TRAIL_SUMI_SLUGS);
}
