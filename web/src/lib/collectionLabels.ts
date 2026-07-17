// Canonical display names for every collection, keyed by many raw/aliased
// forms. One consistent IAST-styled label per tradition so the UI never shows
// two spellings of the same text (e.g. "Chandogya" vs "Chāndogya"). Add new
// aliases here as collections are ingested.

function norm(s: string): string {
  return s.trim().toLowerCase().replace(/\s+/g, " ");
}

// Map of normalized alias -> canonical display name.
const CANONICAL: Array<{ display: string; aliases: string[] }> = [
  { display: "Zhuangzi", aliases: ["the book of chuang tzu", "the_book_of_chuang_tzu", "chuang tzu", "chuang_tzu", "zhuangzi"] },
  { display: "Milarepa — Songs", aliases: ["milarepa songs", "milarepa_songs", "milarepa", "jetsun kahbum", "jetsün kahbum", "tibet's great yogi milarepa", "tibets great yogi milarepa"] },
  { display: "Chāndogya Upaniṣad", aliases: ["chandogya upanishad", "chandogya_upanishad", "chāndogya upaniṣad", "chāndogya_upaniṣad", "khandogya upanishad", "khândogya-upanishad", "chandogya"] },
  { display: "Dōgen — Shōbōgenzō", aliases: ["dogen — shōbōgenzō", "dogen - shobogenzo", "dōgen — shōbōgenzō", "dogen_shobogenzo", "dōgen_shōbōgenzō", "shobogenzo", "shōbōgenzō", "dogen", "dōgen"] },
  { display: "Heart Sūtra", aliases: ["heart sutra", "heart sūtra", "heart_sutra", "prajnaparamitahrdaya", "prajñāpāramitāhṛdaya"] },
  { display: "Nāgārjuna — Mūlamadhyamakakārikā", aliases: ["nagarjuna mulamadhyamakakarika", "nagarjuna_mulamadhyamakakarika", "nāgārjuna — mūlamadhyamakakārikā", "nāgārjuna mūlamadhyamakakārikā", "mulamadhyamakakarika", "mmk"] },
  { display: "Śāntideva — Bodhicaryāvatāra", aliases: ["shantideva bodhicaryavatara", "shantideva_bodhicaryavatara", "śāntideva — bodhicaryāvatāra", "śāntideva bodhicaryāvatāra", "bodhicaryavatara", "bodhicaryāvatāra"] },
  { display: "Tilopa — Mahāmudrā Upadeśa", aliases: ["tilopa mahamudra", "tilopa_mahamudra", "tilopa — mahāmudrā upadeśa", "tilopa mahāmudrā upadeśa", "mahamudra upadesa", "ganges mahamudra"] },
  { display: "Aṣṭāvakra Gītā", aliases: ["astavakra gita", "astavakra_gita", "aṣṭāvakra gītā", "ashtavakra gita", "song of astavakra"] },
  { display: "Bhagavad Gītā", aliases: ["bhagavad gita", "bhagavad_gita", "bhagavad gītā", "gita"] },
  { display: "Epictetus — Discourses & Enchiridion", aliases: ["epictetus works", "epictetus_works", "epictetus", "enchiridion"] },
  { display: "Heraclitus — Fragments", aliases: ["heraclitus fragments", "heraclitus_fragments", "heraclitus", "fragments of heraclitus"] },
  { display: "Īśāvāsya Upaniṣad", aliases: ["isavasya upanishad", "isavasya_upanishad", "īśāvāsya upaniṣad", "isha upanishad", "isa upanishad", "isavasya"] },
  { display: "Māṇḍūkya Upaniṣad & Gauḍapāda's Kārikā", aliases: ["mandukya upanishad and gaudapada karika", "mandukya_upanishad_and_gaudapada_karika", "mandukya upanishad", "māṇḍūkya upaniṣad", "gaudapada karika", "mandukya"] },
  { display: "Patañjali — Yoga Sūtras", aliases: ["patanjali yoga sutras", "patañjali yoga sūtras", "patañjali_yoga_sūtras", "patanjali_yoga_sutras", "yoga sutras", "yoga sūtras", "patanjali"] },
  { display: "Phaedo (Plato)", aliases: ["phaedo (plato)", "phaedo plato", "phaedo_plato", "phaedo"] },
  { display: "Plotinus — Enneads", aliases: ["plotinus enneads", "plotinus_enneads", "plotinus", "enneads"] },
  { display: "Pratyabhijñāhṛdayam", aliases: ["pratyabhijnahrdayam", "pratyabhijñāhṛdayam", "pratyabhijna hrdayam", "heart of recognition"] },
  { display: "Śiva Sūtra", aliases: ["siva sutra", "siva_sutra", "śiva sūtra", "śiva_sūtra", "shiva sutra", "shiva_sutra"] },
  { display: "Śvetāśvatara Upaniṣad", aliases: ["svetasvatara upanishad", "svetasvatara_upanishad", "śvetāśvatara upaniṣad", "svetasvatara"] },
  { display: "Tantrasāra", aliases: ["tantrasara", "tantrasāra", "tantrasara_sample", "abhinavagupta"] },
  { display: "Tao Te Ching", aliases: ["tao te ching", "tao_te_ching", "dao de jing", "laozi", "lao tzu"] },
  { display: "Vijñāna Bhairava", aliases: ["vijnana bhairava", "vijnana_bhairava", "vijñāna bhairava", "vijñāna_bhairava", "vijnana bhairava yuktis", "vijnana_bhairava_yuktis", "vijnana bhairava tantra"] },
  { display: "Yoga Spandakārikā", aliases: ["yoga spandakarika", "yoga_spandakarika", "yoga spandakārikā", "spanda karika", "spandakarika"] },
  { display: "Know Yourself (Ibn ʿArabī / Balyānī)", aliases: ["know yourself (ibn arabi / balyani)", "know yourself an explanation of the oneness of being", "know_yourself_ibn_arabi_balyani", "know yourself ibn arabi balyani", "ibn arabi", "balyani"] },
];

const LOOKUP = new Map<string, string>();
for (const { display, aliases } of CANONICAL) {
  LOOKUP.set(norm(display), display);
  for (const a of aliases) LOOKUP.set(norm(a), display);
}

export function displayCollectionName(name?: string): string {
  const raw = (name || "").trim();
  if (!raw) return "";
  return LOOKUP.get(norm(raw)) ?? raw;
}
