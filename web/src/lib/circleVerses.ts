export const CIRCLE_VERSE_IDS = [
  "siva_sutra.ss_i_1",
  "siva_sutra.ss_i_2",
  "siva_sutra.ss_i_5",
  "pratyabhijnahrdayam.phr_001",
  "pratyabhijnahrdayam.phr_013",
  "pratyabhijnahrdayam.phr_020",
  "vijnana_bhairava.yukti_001",
  "vijnana_bhairava.yukti_002",
  "bhagavad_gita.bg_02_47",
  "bhagavad_gita.bg_06_35",
  "epictetus_works.epi_enc_001",
  "tao_te_ching.ttc_md_002",
] as const;

/** Verses that always hold a seat on the Circle hub — any verse can. */
export const FEATURED_CIRCLE_DOORS: { id: string; label: string }[] = [
  { id: "siva_sutra.ss_i_1", label: "Consciousness is the Self" },
  { id: "siva_sutra.ss_i_2", label: "Knowledge is bondage" },
  { id: "siva_sutra.ss_i_5", label: "The surge of awareness is Bhairava" },
  { id: "pratyabhijnahrdayam.phr_001", label: "Consciousness, autonomous" },
  { id: "pratyabhijnahrdayam.phr_013", label: "Pratyabhijñāhṛdayam 13" },
  { id: "pratyabhijnahrdayam.phr_020", label: "Pratyabhijñāhṛdayam 20" },
  { id: "vijnana_bhairava.yukti_001", label: "Vijñāna Bhairava 1" },
  { id: "vijnana_bhairava.yukti_002", label: "Vijñāna Bhairava 2" },
  { id: "bhagavad_gita.bg_02_47", label: "Your claim is to action alone" },
  { id: "bhagavad_gita.bg_06_35", label: "Practice and dispassion" },
  { id: "epictetus_works.epi_enc_001", label: "The division that liberates" },
  { id: "tao_te_ching.ttc_md_002", label: "The use of absence" },
];

const CIRCLE_SET = new Set<string>(CIRCLE_VERSE_IDS);

export function isCircleVerse(verseId: string): boolean {
  return CIRCLE_SET.has(verseId);
}

/** Every verse holds a circle. Daily and featured doors are only editorial emphasis. */
export function showCircle(_verseId?: string, _offeredCount?: number, _daily = false): boolean {
  return true;
}

export function excerptReading(body: string, max = 280): string {
  const trimmed = body.trim();
  if (trimmed.length <= max) return trimmed;
  const sliced = trimmed.slice(0, max).replace(/\s+\S*$/, "");
  return `${sliced || trimmed.slice(0, max)}…`;
}

export function formatCircleTime(ts: number, locale: string): string {
  const deltaSec = Math.round((ts - Date.now()) / 1000);
  const abs = Math.abs(deltaSec);
  const rtf = new Intl.RelativeTimeFormat(locale, { numeric: "auto" });
  if (abs < 60) return rtf.format(deltaSec, "second");
  if (abs < 3600) return rtf.format(Math.round(deltaSec / 60), "minute");
  if (abs < 86400) return rtf.format(Math.round(deltaSec / 3600), "hour");
  if (abs < 86400 * 14) return rtf.format(Math.round(deltaSec / 86400), "day");
  return new Date(ts).toLocaleDateString(locale, { month: "short", day: "numeric", year: "numeric" });
}
