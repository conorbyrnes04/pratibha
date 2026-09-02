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

const CIRCLE_SET = new Set<string>(CIRCLE_VERSE_IDS);

export function isCircleVerse(verseId: string): boolean {
  return CIRCLE_SET.has(verseId);
}

export function showCircle(_verseId?: string, _offeredCount?: number, _daily = false): boolean {
  return true;
}
