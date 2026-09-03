// Canonical display names for every collection — work title only.
// Author lives on the Library tome meta (libraryTomes.ts), not in the title.
// One consistent IAST-styled label per text so the UI never shows two spellings.

function norm(s: string): string {
  return s.trim().toLowerCase().replace(/\s+/g, " ");
}

const CANONICAL: Array<{ display: string; aliases: string[] }> = [
  { display: "Zhuangzi", aliases: ["the book of chuang tzu", "the_book_of_chuang_tzu", "chuang tzu", "chuang_tzu", "zhuangzi"] },
  { display: "Songs of Milarepa", aliases: ["milarepa songs", "milarepa_songs", "milarepa", "jetsun kahbum", "jetsün kahbum", "tibet's great yogi milarepa", "tibets great yogi milarepa", "milarepa — songs"] },
  { display: "Chāndogya Upaniṣad", aliases: ["chandogya upanishad", "chandogya_upanishad", "chāndogya upaniṣad", "chāndogya_upaniṣad", "khandogya upanishad", "khândogya-upanishad", "chandogya"] },
  { display: "Shōbōgenzō", aliases: ["dogen — shōbōgenzō", "dogen - shobogenzo", "dōgen — shōbōgenzō", "dogen_shobogenzo", "dōgen_shōbōgenzō", "shobogenzo", "shōbōgenzō", "dogen", "dōgen"] },
  { display: "Heart Sūtra", aliases: ["heart sutra", "heart sūtra", "heart_sutra", "prajnaparamitahrdaya", "prajñāpāramitāhṛdaya"] },
  { display: "Mūlamadhyamakakārikā", aliases: ["nagarjuna mulamadhyamakakarika", "nagarjuna_mulamadhyamakakarika", "nāgārjuna — mūlamadhyamakakārikā", "nāgārjuna mūlamadhyamakakārikā", "mulamadhyamakakarika", "mmk"] },
  { display: "Bodhicaryāvatāra", aliases: ["shantideva bodhicaryavatara", "shantideva_bodhicaryavatara", "śāntideva — bodhicaryāvatāra", "śāntideva bodhicaryāvatāra", "bodhicaryavatara", "bodhicaryāvatāra"] },
  { display: "Mahāmudrā Upadeśa", aliases: ["tilopa mahamudra", "tilopa_mahamudra", "tilopa — mahāmudrā upadeśa", "tilopa mahāmudrā upadeśa", "mahamudra upadesa", "ganges mahamudra"] },
  { display: "Aṣṭāvakra Gītā", aliases: ["astavakra gita", "astavakra_gita", "aṣṭāvakra gītā", "ashtavakra gita", "song of astavakra"] },
  { display: "Bhagavad Gītā", aliases: ["bhagavad gita", "bhagavad_gita", "bhagavad gītā", "gita"] },
  { display: "Enchiridion", aliases: ["epictetus works", "epictetus_works", "epictetus", "enchiridion", "epictetus — discourses & enchiridion"] },
  { display: "Fragments", aliases: ["heraclitus fragments", "heraclitus_fragments", "heraclitus", "fragments of heraclitus", "heraclitus — fragments"] },
  { display: "Īśāvāsya Upaniṣad", aliases: ["isavasya upanishad", "isavasya_upanishad", "īśāvāsya upaniṣad", "isha upanishad", "isa upanishad", "isavasya"] },
  { display: "Māṇḍūkya Upaniṣad & Kārikā", aliases: ["mandukya upanishad and gaudapada karika", "mandukya_upanishad_and_gaudapada_karika", "mandukya upanishad", "māṇḍūkya upaniṣad", "gaudapada karika", "mandukya", "māṇḍūkya upaniṣad & gauḍapāda's kārikā"] },
  { display: "Yoga Sūtras", aliases: ["patanjali yoga sutras", "patañjali yoga sūtras", "patañjali_yoga_sūtras", "patanjali_yoga_sutras", "yoga sutras", "yoga sūtras", "patanjali", "patañjali — yoga sūtras"] },
  { display: "Phaedo", aliases: ["phaedo (plato)", "phaedo plato", "phaedo_plato", "phaedo"] },
  { display: "Enneads", aliases: ["plotinus enneads", "plotinus_enneads", "plotinus", "enneads", "plotinus — enneads"] },
  { display: "Lallā Vākyāni", aliases: ["lalla vakyani", "lalla_vakyani", "lallā vākyāni", "lal ded", "lalla ded", "lala ded", "lalleshwari", "lalla yogiswari"] },
  { display: "Pratyabhijñāhṛdayam", aliases: ["pratyabhijnahrdayam", "pratyabhijñāhṛdayam", "pratyabhijna hrdayam", "heart of recognition"] },
  { display: "Meister Eckhart", aliases: ["meister eckhart", "meister_eckhart", "eckhart", "von abegescheidenheit", "abegescheidenheit", "abgeschiedenheit"] },
  { display: "Mathnawī", aliases: ["rumi mathnawi", "rumi_mathnawi", "rūmī — mathnawī-yi maʿnawī", "mathnawi", "mathnawī", "masnavi", "rumi", "rūmī"] },
  { display: "Śiva Sūtras", aliases: ["siva sutra", "siva_sutra", "śiva sūtra", "śiva_sūtra", "shiva sutra", "shiva_sutra", "śiva sūtra"] },
  { display: "Śvetāśvatara Upaniṣad", aliases: ["svetasvatara upanishad", "svetasvatara_upanishad", "śvetāśvatara upaniṣad", "svetasvatara"] },
  { display: "Tantrasāra", aliases: ["tantrasara", "tantrasāra", "tantrasara_sample", "abhinavagupta"] },
  { display: "Yoginīhṛdaya", aliases: ["yoginihrdaya", "yoginīhṛdaya", "yogini hrdaya", "yogini_hrdaya", "heart of the yogini"] },
  { display: "Tao Te Ching", aliases: ["tao te ching", "tao_te_ching", "dao de jing", "laozi", "lao tzu"] },
  { display: "Vijñāna Bhairava", aliases: ["vijnana bhairava", "vijnana_bhairava", "vijñāna bhairava", "vijñāna_bhairava", "vijnana bhairava yuktis", "vijnana_bhairava_yuktis", "vijnana bhairava tantra"] },
  { display: "Spandakārikā", aliases: ["yoga spandakarika", "yoga_spandakarika", "yoga spandakārikā", "spanda karika", "spandakarika"] },
  { display: "Know Yourself", aliases: ["know yourself (ibn arabi / balyani)", "know yourself an explanation of the oneness of being", "know_yourself_ibn_arabi_balyani", "know yourself ibn arabi balyani", "ibn arabi", "balyani", "know yourself (ibn ʿarabī / balyānī)"] },
  { display: "Conference of the Birds", aliases: ["conference of the birds", "conference_of_the_birds", "mantiq al tayr", "manṭiq al-ṭayr", "attar", "ʿaṭṭār"] },
  { display: "Kashf al-Maḥjūb", aliases: ["kashf al-mahjub", "kashf_al_mahjub", "kashf al-maḥjūb", "hujwiri", "hujwīrī", "unveiling of the veiled"] },
  { display: "Dhammapada", aliases: ["dhammapada", "dhammapāda", "the dhammapada"] },
  { display: "Kaṭha Upaniṣad", aliases: ["katha upanishad", "katha_upanishad", "kaṭha upaniṣad", "katha"] },
  { display: "Bṛhadāraṇyaka Upaniṣad", aliases: ["brihadaranyaka upanishad", "brihadaranyaka_upanishad", "bṛhadāraṇyaka upaniṣad", "brihad"] },
  { display: "Muṇḍaka Upaniṣad", aliases: ["mundaka upanishad", "mundaka_upanishad", "muṇḍaka upaniṣad", "mundaka"] },
  { display: "Meditations", aliases: ["marcus aurelius meditations", "marcus_aurelius_meditations", "marcus aurelius", "meditations"] },
  { display: "Parmenides", aliases: ["parmenides fragments", "parmenides_fragments", "parmenides"] },
  { display: "The Cloud of Unknowing", aliases: ["the cloud of unknowing", "the_cloud_of_unknowing", "cloud of unknowing"] },
  { display: "Analects", aliases: ["confucius — analects", "confucius analects", "confucius_analects", "analects", "lunyu"] },
  { display: "Zhōngyōng", aliases: ["zhongyong", "doctrine of the mean", "the doctrine of the mean"] },
  { display: "Mystical Theology", aliases: ["pseudo dionysius", "pseudo_dionysius", "dionysius", "mystical theology", "the divine names"] },
  { display: "The Soul of the Indian", aliases: ["the soul of the indian", "eastman_soul_of_the_indian", "soul of the indian"] },
  { display: "Old Indian Legends", aliases: ["old indian legends", "zitkala_sa_old_indian_legends", "zitkala-sa"] },
  { display: "Serer Cosaan", aliases: ["senegalese animism", "senegalese_animism", "serer cosaan", "serer"] },
  { display: "Pulaar Tradition", aliases: ["pulaar tradition", "pulaar_tradition", "fulbe", "fulɓe"] },
  { display: "Pulaar Texts", aliases: ["pulaar texts (gaden)", "pulaar_texts", "pulaar texts", "gaden", "le poular"] },
  { display: "Futa Jalon Fulde", aliases: ["futa jalon fulde (reichardt)", "futa_jalon_fulde", "futa jalon", "fuuta jaloo", "reichardt"] },
  { display: "Os Africanos no Brasil", aliases: ["os africanos no brasil", "os_africanos_no_brasil", "os africanos", "nina rodrigues africanos"] },
  { display: "O Animismo Fetichista", aliases: ["o animismo fetichista", "animismo_fetichista", "animisme fétichiste"] },
  { display: "Myths of Ìfẹ̀", aliases: ["myths of ìfẹ̀", "myths of ife", "myths_of_ife", "wyndham", "myths of ífè"] },
  { display: "Yoruba Proverbs (Òwe)", aliases: ["yoruba proverbs (òwe)", "yoruba_proverbs", "yoruba proverbs"] },
  { display: "The Yoruba Faith", aliases: ["the yoruba faith (samuel johnson)", "johnson_yoruba_religion", "the yoruba faith"] },
  { display: "Psalms", aliases: ["psalms (tehillim)", "psalms_tehillim", "tehillim", "psalms", "psalter"] },
  { display: "Ecclesiastes", aliases: ["ecclesiastes (qoheleth)", "ecclesiastes_qoheleth", "qoheleth", "ecclesiastes"] },
  { display: "Gospel of Mary", aliases: ["gospel of mary", "gospel_of_mary", "gospel of mary magdalene"] },
  { display: "Logia of Jesus", aliases: ["logia of jesus", "new_testament_logia", "new testament logia", "mystical logia of jesus"] },
  { display: "Gospel of Thomas", aliases: ["gospel of thomas", "gospel_of_thomas"] },
  { display: "Diamond Sūtra", aliases: ["vajracchedikā prajñāpāramitā", "vajracchedika_diamond_sutra", "vajracchedika prajnaparamita", "diamond sutra", "diamond sūtra"] },
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

/** Fold for equality: strip diacritics and non-alphanumerics. */
function foldKey(s: string): string {
  return s
    .normalize("NFD")
    .replace(/\p{M}/gu, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "");
}

/**
 * True when two collection labels refer to the same text.
 * Handles display vs corpus mismatches (e.g. Yoginīhṛdaya vs Yoginihrdaya).
 */
export function collectionsMatch(a?: string, b?: string): boolean {
  const left = (a || "").trim();
  const right = (b || "").trim();
  if (!left || !right) return false;
  if (left === right) return true;
  if (displayCollectionName(left) === displayCollectionName(right)) return true;
  return foldKey(left) === foldKey(right);
}
