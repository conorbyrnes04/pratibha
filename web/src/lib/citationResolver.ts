import type { VerseItem } from "@/lib/types";

/**
 * Resolve a cross-tradition resonance citation (free text like
 * "Bhagavad Gītā 2.47" or "Śiva Sūtra I.1") to a corpus passage.
 *
 * Two-tier: an exact passage match when the reference numbers line up, else a
 * collection-level match so the reader can still jump to the tradition. Texts
 * that aren't in the corpus (Marcus Aurelius, Gospel of Thomas, …) resolve to
 * null and stay plain text — we never fabricate a link.
 */

export type CitationResolution =
  | { kind: "passage"; passageId: string; collection: string }
  | { kind: "collection"; collection: string }
  | null;

export type CitationIndex = {
  /** folded alias -> canonical collection value (as stored on verses) */
  aliasToCollection: Map<string, string>;
  /** canonical collection value -> passages with their normalized ref keys */
  entries: Map<string, Array<{ id: string; refKeys: Set<string> }>>;
  /** sorted folded aliases (longest first) for greedy matching */
  aliasOrder: string[];
};

/** Strip diacritics and lowercase for robust matching. */
function fold(input: string | undefined | null): string {
  if (!input) return "";
  return input
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

const ROMAN: Record<string, number> = {
  i: 1, ii: 2, iii: 3, iv: 4, v: 5, vi: 6, vii: 7, viii: 8, ix: 9, x: 10,
  xi: 11, xii: 12, xiii: 13, xiv: 14, xv: 15, xvi: 16, xvii: 17, xviii: 18,
};

function romanToArabic(token: string): string {
  return ROMAN[token] !== undefined ? String(ROMAN[token]) : token;
}

function stripLeadingZero(part: string): string {
  return /^\d+$/.test(part) ? String(parseInt(part, 10)) : part;
}

/**
 * Extract normalized numeric reference keys from a string.
 * "PHR_012" -> {"12"}, "Ennead I.6.1" -> {"1.6.1"}, "2.2.13" -> {"2.2.13"}.
 */
function normRefKeys(input: string | undefined | null): Set<string> {
  const keys = new Set<string>();
  if (!input) return keys;
  const folded = fold(input).replace(/[–—]/g, "-");
  const re = /\b([ivxlc]+|\d+)([.\-_ ]([ivxlc]+|\d+)){0,3}/g;
  let match: RegExpExecArray | null;
  while ((match = re.exec(folded)) !== null) {
    const parts = match[0]
      .split(/[.\-_ ]+/)
      .filter(Boolean)
      .map((p) => stripLeadingZero(romanToArabic(p)));
    if (parts.length && parts.every((p) => /^\d+$/.test(p))) {
      keys.add(parts.join("."));
    }
  }
  return keys;
}

/**
 * Curated citation aliases -> the collection value as it appears on verses.
 * Values must match `VerseItem.collection` produced by the API loader.
 */
const CITATION_ALIASES: Record<string, string> = {
  "bhagavad gita": "Bhagavad Gita",
  gita: "Bhagavad Gita",
  "yoga sutra": "Patañjali Yoga Sūtras",
  "yoga sutras": "Patañjali Yoga Sūtras",
  patanjali: "Patañjali Yoga Sūtras",
  yogasutra: "Patañjali Yoga Sūtras",
  "siva sutra": "Siva Sutra",
  "shiva sutra": "Siva Sutra",
  ennead: "Plotinus Enneads",
  plotinus: "Plotinus Enneads",
  chandogya: "Chāndogya Upaniṣad",
  mandukya: "Mandukya Upanishad and Gaudapada Karika",
  gaudapada: "Mandukya Upanishad and Gaudapada Karika",
  isavasya: "Isavasya Upanishad",
  "isha upanishad": "Isavasya Upanishad",
  "isa upanishad": "Isavasya Upanishad",
  svetasvatara: "Svetasvatara Upanishad",
  "tao te ching": "Tao Te Ching",
  "dao de jing": "Tao Te Ching",
  daodejing: "Tao Te Ching",
  "daode jing": "Tao Te Ching",
  laozi: "Tao Te Ching",
  "lao tzu": "Tao Te Ching",
  zhuangzi: "The Book of Chuang Tzu",
  "chuang tzu": "The Book of Chuang Tzu",
  "zhuang zhou": "The Book of Chuang Tzu",
  heraclitus: "Heraclitus Fragments",
  phaedo: "Phaedo (Plato)",
  enchiridion: "Epictetus Works",
  epictetus: "Epictetus Works",
  "vijnana bhairava": "Vijnana Bhairava",
  vbt: "Vijnana Bhairava",
  "bhairava tantra": "Vijnana Bhairava",
  pratyabhijnahrdayam: "Pratyabhijnahrdayam",
  pratyabhijna: "Pratyabhijnahrdayam",
  spandakarika: "Yoga Spandakarika",
  "spanda karika": "Yoga Spandakarika",
  mulamadhyamakakarika: "Nagarjuna Mulamadhyamakakarika",
  mmk: "Nagarjuna Mulamadhyamakakarika",
  astavakra: "Astavakra Gita",
  ashtavakra: "Astavakra Gita",
  "heart sutra": "Heart Sutra",
  prajnaparamitahrdaya: "Heart Sutra",
  shantideva: "Shantideva Bodhicaryavatara",
  bodhicaryavatara: "Shantideva Bodhicaryavatara",
  milarepa: "Milarepa Songs",
  tilopa: "Tilopa Mahamudra",
  mahamudra: "Tilopa Mahamudra",
  "ibn arabi": "Know Yourself (Ibn Arabi / Balyani)",
  balyani: "Know Yourself (Ibn Arabi / Balyani)",
  tantrasara: "Tantrasara",
  abhinavagupta: "Tantrasara",
};

/**
 * Texts we know are NOT in the corpus. Matching one suppresses a false
 * collection link (so the citation stays honest plain text).
 */
const EXTERNAL_MARKERS = [
  "katha upanishad", "kena upanishad", "mundaka", "brihadaranyaka",
  "taittiriya", "aitareya", "aristotle", "kant", "heidegger", "husserl",
  "wittgenstein", "spinoza", "descartes", "hegel", "nietzsche", "sartre",
  "merleau", "whitehead", "rumi", "eckhart", "augustine", "aquinas",
  "dogen", "hakuin", "marcus aurelius", "meditations", "dhammapada",
  "gospel", "course in miracles", "william james", "book of job",
  "narada", "samkhya", "republic", "abhidharma", "pseudo-dionysius",
  "mathnawi", "koan", "kensho", " zen", "upanisad 1", // generic fallbacks
].map(fold);

export function buildCitationIndex(verses: VerseItem[]): CitationIndex {
  const aliasToCollection = new Map<string, string>();
  const entries = new Map<string, Array<{ id: string; refKeys: Set<string> }>>();

  for (const [alias, collection] of Object.entries(CITATION_ALIASES)) {
    aliasToCollection.set(fold(alias), collection);
  }

  for (const v of verses) {
    const collection = (v.collection || "").trim();
    if (!collection) continue;
    // The collection's own name is an alias for itself.
    aliasToCollection.set(fold(collection), collection);

    const refKeys = new Set<string>();
    for (const key of normRefKeys(v.sutra_id)) refKeys.add(key);
    for (const key of normRefKeys(v.reference)) refKeys.add(key);
    for (const key of normRefKeys(v.section)) refKeys.add(key);
    for (const key of normRefKeys(v.provenance?.source_reference)) refKeys.add(key);

    const list = entries.get(collection) || [];
    list.push({ id: v._id, refKeys });
    entries.set(collection, list);
  }

  const aliasOrder = Array.from(aliasToCollection.keys()).sort((a, b) => b.length - a.length);
  return { aliasToCollection, entries, aliasOrder };
}

function findCollection(citation: string, index: CitationIndex): { collection: string; at: number } | null {
  const folded = fold(citation);
  for (const alias of index.aliasOrder) {
    const at = alias ? folded.indexOf(alias) : -1;
    if (at >= 0) {
      const collection = index.aliasToCollection.get(alias);
      if (collection) return { collection, at };
    }
  }
  return null;
}

export function resolveCitation(citation: string, index: CitationIndex): CitationResolution {
  if (!citation) return null;
  const folded = fold(citation);

  const found = findCollection(citation, index);
  if (!found) {
    return null;
  }
  const { collection, at } = found;

  // If an external (not-in-corpus) text is named *before* our collection alias,
  // the citation is really about that external text — keep it plain, don't link.
  for (const marker of EXTERNAL_MARKERS) {
    if (!marker || fold(collection).includes(marker)) continue;
    const mAt = folded.indexOf(marker);
    if (mAt >= 0 && mAt < at) return null;
  }

  const refs = normRefKeys(citation);
  const list = index.entries.get(collection) || [];

  if (refs.size > 0) {
    for (const entry of list) {
      for (const key of entry.refKeys) {
        if (refs.has(key)) return { kind: "passage", passageId: entry.id, collection };
      }
    }
    // Prefix match: citation "2.2.13" vs unit key "2.2", or vice versa.
    for (const entry of list) {
      for (const r of refs) {
        for (const k of entry.refKeys) {
          if (r.startsWith(`${k}.`) || k.startsWith(`${r}.`)) {
            return { kind: "passage", passageId: entry.id, collection };
          }
        }
      }
    }
  }

  return { kind: "collection", collection };
}
