import { sumiGlyph, type SumiSlug } from "./sumiGlyphs";
import { displayCollectionName } from "./collectionLabels";
import { countForCollection, preferStudyUnits } from "./corpusFilters";
import type { VerseItem } from "./types";

export type LibrarySort = "title" | "author" | "tradition";

export type LibraryTome = {
  collection: string;
  /** Work title only (no author prefix). */
  displayName: string;
  /** Tradition family — shown in the card footer. */
  tradition: string;
  /** Standardized author attribution — shown under the title. */
  author: string;
  /** Estimated authorship date — shown in the card footer. */
  authored: string;
  /** Approximate midpoint year (negative = BCE). */
  eraYear: number;
  count: number;
  glyph: SumiSlug;
  themes: string[];
};

const TRADITION_ORDER = [
  "Vedānta",
  "Yoga",
  "Kashmir Śaiva",
  "Buddhist",
  "Daoist",
  "Confucian",
  "Greek",
  "Christian",
  "Sufi",
  "Other",
] as const;

export type TraditionShelf = {
  tradition: string;
  tomes: LibraryTome[];
};

type TomeMeta = {
  pattern: RegExp;
  tradition: string;
  /** Person or school name only — no dates here. */
  author: string;
  authored: string;
  eraYear: number;
};

/**
 * Author format: bare name, or "Name (trad.)" / "Name (attrib.)" when needed.
 * Dates live only in `authored`. Titles live only in displayCollectionName.
 */
const TOME_META: TomeMeta[] = [
  { pattern: /astavakra|ashtavakra|a[sṣ][tṭ][aā]vakra/i, tradition: "Vedānta", author: "Aṣṭāvakra (attrib.)", authored: "c. early CE (uncertain)", eraYear: 200 },
  { pattern: /bhagavad/i, tradition: "Vedānta", author: "Vyāsa (trad.)", authored: "c. 2nd c. BCE – 2nd c. CE", eraYear: -50 },
  { pattern: /chandogya|chāndogya|khandogya/i, tradition: "Vedānta", author: "Upaniṣadic", authored: "c. 8th–6th c. BCE", eraYear: -700 },
  { pattern: /isavasya|īśāvāsya|isha.?upani|isa.?upani/i, tradition: "Vedānta", author: "Upaniṣadic", authored: "c. 5th–3rd c. BCE", eraYear: -400 },
  { pattern: /svetasvatara|śvetāśvatara/i, tradition: "Vedānta", author: "Upaniṣadic", authored: "c. 5th–3rd c. BCE", eraYear: -350 },
  { pattern: /mandukya|māṇḍūkya|gaudapada|gauḍapāda/i, tradition: "Vedānta", author: "Gauḍapāda", authored: "c. 5th–6th c. CE", eraYear: 500 },
  { pattern: /katha|kaṭha/i, tradition: "Vedānta", author: "Upaniṣadic", authored: "c. 5th–3rd c. BCE", eraYear: -400 },
  { pattern: /brihad|bṛhadāraṇyaka|brihadaranyaka/i, tradition: "Vedānta", author: "Upaniṣadic", authored: "c. 7th–5th c. BCE", eraYear: -600 },
  { pattern: /mundaka|muṇḍaka/i, tradition: "Vedānta", author: "Upaniṣadic", authored: "c. 5th–3rd c. BCE", eraYear: -400 },
  { pattern: /dhammapada|dhammapāda/i, tradition: "Buddhist", author: "Anonymous (Tipiṭaka)", authored: "c. 3rd c. BCE", eraYear: -250 },
  { pattern: /marcus|meditations/i, tradition: "Greek", author: "Marcus Aurelius", authored: "c. 170–180 CE", eraYear: 175 },
  { pattern: /cloud.?of.?unknowing/i, tradition: "Christian", author: "Anonymous (English mystic)", authored: "c. 14th c. CE", eraYear: 1375 },
  { pattern: /parmenides/i, tradition: "Greek", author: "Parmenides", authored: "c. 5th c. BCE", eraYear: -475 },
  { pattern: /patanjali|patañjali|yoga.?s[uū]tra/i, tradition: "Yoga", author: "Patañjali", authored: "c. 2nd–4th c. CE", eraYear: 300 },
  { pattern: /vijnana.?bhairava|vijñāna.?bhairava/i, tradition: "Kashmir Śaiva", author: "Anonymous", authored: "c. 8th–9th c. CE", eraYear: 850 },
  { pattern: /spanda/i, tradition: "Kashmir Śaiva", author: "Vasugupta / Kallaṭa", authored: "c. 9th c. CE", eraYear: 875 },
  { pattern: /siva.?s[uū]tra|śiva.?s[uū]tra|shiva.?sutra/i, tradition: "Kashmir Śaiva", author: "Vasugupta", authored: "c. 9th c. CE", eraYear: 850 },
  { pattern: /pratyabhij/i, tradition: "Kashmir Śaiva", author: "Kṣemarāja", authored: "c. 11th c. CE", eraYear: 1020 },
  { pattern: /tantras[aā]ra|abhinavagupta/i, tradition: "Kashmir Śaiva", author: "Abhinavagupta", authored: "c. 1000 CE", eraYear: 1000 },
  { pattern: /yogin[iī]h[rṛ]daya|yogini.?hrdaya|heart of the yogini/i, tradition: "Kashmir Śaiva", author: "Anonymous (Śrīvidyā)", authored: "c. 11th–13th c. CE", eraYear: 1150 },
  { pattern: /heart.?s[uū]tra|prajnaparamita|prajñāpāramitā/i, tradition: "Buddhist", author: "Anonymous (attrib.)", authored: "c. 1st–7th c. CE", eraYear: 350 },
  { pattern: /nagarjuna|madhyamaka|mulamadhyamakakarika|mmk/i, tradition: "Buddhist", author: "Nāgārjuna", authored: "c. 2nd–3rd c. CE", eraYear: 200 },
  { pattern: /shantideva|śāntideva|bodhicary/i, tradition: "Buddhist", author: "Śāntideva", authored: "c. 8th c. CE", eraYear: 750 },
  { pattern: /milarepa|jetsun/i, tradition: "Buddhist", author: "Milarepa", authored: "c. 11th–12th c. CE", eraYear: 1100 },
  { pattern: /tilopa|maha.?mudra/i, tradition: "Buddhist", author: "Tilopa", authored: "c. 10th–11th c. CE", eraYear: 1000 },
  { pattern: /dogen|dōgen|shobogenzo|shōbōgenzō/i, tradition: "Buddhist", author: "Dōgen", authored: "c. 13th c. CE", eraYear: 1240 },
  { pattern: /rumi|rūmī|mathnaw|masnavi/i, tradition: "Sufi", author: "Jalāl al-Dīn Rūmī", authored: "c. 1258–1273 CE", eraYear: 1265 },
  { pattern: /tao.?te.?ching|dao.?de.?jing|laozi|lao.?tzu/i, tradition: "Daoist", author: "Laozi (trad.)", authored: "c. 4th–3rd c. BCE", eraYear: -350 },
  { pattern: /zhuang|chuang/i, tradition: "Daoist", author: "Zhuangzi", authored: "c. 4th–3rd c. BCE", eraYear: -320 },
  { pattern: /analect|confucius|lunyu/i, tradition: "Confucian", author: "Confucius (trad.)", authored: "c. 5th–3rd c. BCE", eraYear: -450 },
  { pattern: /zhongyong|doctrine of the mean/i, tradition: "Confucian", author: "Zisi (trad.)", authored: "c. 5th–3rd c. BCE", eraYear: -400 },
  { pattern: /heraclitus/i, tradition: "Greek", author: "Heraclitus", authored: "c. 500 BCE", eraYear: -500 },
  { pattern: /epictetus|enchiridion/i, tradition: "Greek", author: "Epictetus", authored: "c. 50–135 CE", eraYear: 100 },
  { pattern: /phaedo|plato/i, tradition: "Greek", author: "Plato", authored: "c. 360 BCE", eraYear: -360 },
  { pattern: /plotinus|ennead/i, tradition: "Greek", author: "Plotinus", authored: "c. 270 CE", eraYear: 270 },
  { pattern: /eckhart|abegescheidenheit|abgeschiedenheit/i, tradition: "Christian", author: "Meister Eckhart", authored: "c. 1300 CE", eraYear: 1300 },
  { pattern: /dionysius|areopagite|mystical.?theology|divine.?names/i, tradition: "Christian", author: "Pseudo-Dionysius", authored: "c. 5th–6th c. CE", eraYear: 500 },
  { pattern: /ibn|arabi|balyani|know yourself/i, tradition: "Sufi", author: "Balyānī", authored: "c. 13th–14th c. CE", eraYear: 1300 },
];

function metaFor(collection: string): Omit<TomeMeta, "pattern"> {
  for (const row of TOME_META) {
    if (row.pattern.test(collection)) {
      return {
        tradition: row.tradition,
        author: row.author,
        authored: row.authored,
        eraYear: row.eraYear,
      };
    }
  }
  return {
    tradition: "Other",
    author: "Unknown",
    authored: "date uncertain",
    eraYear: 0,
  };
}

/** Fold for title sort: strip diacritics, ignore leading "the ". */
function titleSortKey(title: string): string {
  return title
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/^the\s+/, "")
    .trim();
}

function authorSortKey(author: string): string {
  return author
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/\s*\((trad\.|attrib\.)\)\s*/g, "")
    .trim();
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

    const meta = metaFor(collection);
    tomes.push({
      collection,
      displayName: displayCollectionName(collection),
      tradition: meta.tradition,
      author: meta.author,
      authored: meta.authored,
      eraYear: meta.eraYear,
      count: countForCollection(items, collection),
      glyph: sumiGlyph(collection, meta.tradition),
      themes,
    });
  }

  return sortTomes(tomes, "title");
}

export function sortTomes(tomes: LibraryTome[], sort: LibrarySort): LibraryTome[] {
  const copy = [...tomes];
  if (sort === "author") {
    return copy.sort(
      (a, b) =>
        authorSortKey(a.author).localeCompare(authorSortKey(b.author)) ||
        titleSortKey(a.displayName).localeCompare(titleSortKey(b.displayName)),
    );
  }
  if (sort === "tradition") {
    const rank = (t: string) => {
      const i = (TRADITION_ORDER as readonly string[]).indexOf(t);
      return i === -1 ? 99 : i;
    };
    return copy.sort(
      (a, b) =>
        rank(a.tradition) - rank(b.tradition) ||
        titleSortKey(a.displayName).localeCompare(titleSortKey(b.displayName)),
    );
  }
  return copy.sort((a, b) => titleSortKey(a.displayName).localeCompare(titleSortKey(b.displayName)));
}

export function groupTomesByTradition(tomes: LibraryTome[]): TraditionShelf[] {
  const buckets = new Map<string, LibraryTome[]>();
  for (const tome of tomes) {
    const list = buckets.get(tome.tradition) || [];
    list.push(tome);
    buckets.set(tome.tradition, list);
  }
  return TRADITION_ORDER.filter((t) => buckets.has(t)).map((tradition) => ({
    tradition,
    tomes: (buckets.get(tradition) || []).sort((a, b) =>
      titleSortKey(a.displayName).localeCompare(titleSortKey(b.displayName)),
    ),
  }));
}

export const LIBRARY_SORT_OPTIONS: Array<{ value: LibrarySort; label: string; hint: string }> = [
  { value: "title", label: "Title", hint: "A–Z by work title" },
  { value: "author", label: "Author", hint: "A–Z by author" },
  { value: "tradition", label: "Tradition", hint: "Grouped by lineage" },
];
