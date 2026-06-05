export type Appendix = {
  commentator?: string;
  text?: string;
};

export type EditorialMaturity =
  | "publishable"
  | "strong_draft"
  | "needs_rewrite"
  | "structural_draft";

export type PratibhaLayerKind =
  | "original"
  | "iast"
  | "translation"
  | "commentary"
  | "key_terms"
  | "resonances"
  | "practice"
  | "appendix";

export type KeyTerm = {
  term: string;
  definition: string;
};

export type Resonance = {
  citation: string;
  resonance: string;
  divergence?: string;
};

export type PratibhaLayer = {
  kind: PratibhaLayerKind;
  label: string;
  body?: string;
  items?: Array<KeyTerm | Resonance | Record<string, unknown>>;
};

export type VerseItem = {
  _id: string;
  collection?: string;
  section?: string;
  title?: string;
  sutra_id?: string;
  thesis?: string;
  source_excerpt?: string;
  translation?: string;
  commentary?: string;
  abhyasa?: string;
  practice?: string;
  sanskrit?: string;
  transliteration?: string;
  themes?: string[];
  appendixes?: Appendix[];
  editorial_maturity?: EditorialMaturity;
  editorial_score?: number;
  pratibha_layers?: PratibhaLayer[];
};

export type Source = {
  rank: number;
  score?: number;
  text?: string;
  metadata?: Record<string, unknown>;
};

export type ChatMode = "question" | "explain" | "compare" | "practice";

export type ChatOptions = {
  verseId?: string;
  layerFocus?: PratibhaLayerKind;
  chatMode?: ChatMode;
};

export type JournalNote = {
  id: string;
  passageId: string;
  passageTitle: string;
  body: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
  prompt?: string;
};
