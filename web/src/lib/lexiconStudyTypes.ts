/** Types for `GET /lexicon/study` flashcard decks. */

export type StudyDeckId = "sanskrit" | "greek" | "chinese" | "arabic" | "german";

export type StudyCardMode = "recognition" | "trap" | "production";

export type StudyDeck = {
  id: StudyDeckId;
  label: string;
  native_label: string;
  blurb: string;
  script_hint: string;
  lemma_count: number;
  card_count: number;
  sample: string;
};

export type StudyCardFront = {
  native?: string;
  roman?: string;
  script_class?: string;
  prompt?: string;
  trap?: string;
  cue?: string;
  sense_label?: string;
};

export type StudyCardBack = {
  label: string;
  short: string;
  etymology?: string;
  traps?: string[];
  exemplars?: string[];
  correction?: string;
  native?: string;
  roman?: string;
  script_class?: string;
};

export type StudyCard = {
  id: string;
  sense_id: string;
  lemma_id: string;
  deck_id: StudyDeckId;
  mode: StudyCardMode;
  maturity: string;
  traditions: string[];
  front: StudyCardFront;
  back: StudyCardBack;
};

export type LexiconStudyPayload = {
  minimum_maturity: string;
  decks: StudyDeck[];
  cards: StudyCard[];
  totals: {
    decks: number;
    cards: number;
    lemmas: number;
  };
};

export type SrsGrade = "again" | "hard" | "good" | "easy";

export type SrsEntry = {
  cardId: string;
  ease: number;
  intervalDays: number;
  due: number;
  reps: number;
  lapses: number;
};
