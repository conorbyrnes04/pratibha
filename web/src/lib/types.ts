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
  layer_provenance?: string;
  items?: Array<KeyTerm | Resonance | Record<string, unknown>>;
};

export type VerseItem = {
  _id: string;
  collection?: string;
  section?: string;
  title?: string;
  sutra_id?: string;
  reference?: string;
  sequence?: number;
  work_id?: string;
  provenance?: {
    source_reference?: string;
    section?: string;
    collection?: string;
    original_id?: string;
  };
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
  anchor_chapter?: string;
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
  compareVerseIds?: string[];
  layerFocus?: PratibhaLayerKind;
  chatMode?: ChatMode;
};

export type JournalNoteKind = "reflection" | "chat_response";

export type SellReadyTier = "green" | "yellow" | "orange" | "red";

export type SourceAttribution = {
  id: string;
  collection: string;
  tradition: string;
  original_work: string;
  anchor_translation?: string | null;
  sanskrit_source?: string | null;
  editorial_note: string;
  conceived_by_conor?: boolean;
  coverage?: string | null;
  license: "public_domain" | "attributed_excerpt" | "mixed" | "original_editorial";
  license_label: string;
  sell_ready_tier: SellReadyTier;
  sell_ready_tier_label: string;
  pd_alternative?: string | null;
  status: "in_corpus" | "in_progress";
  passages_in_corpus: number;
  links?: Array<{ label: string; url: string | null }>;
};

export type SourcesPayload = {
  items: SourceAttribution[];
  summary: {
    collections_documented: number;
    collections_in_corpus: number;
    total_passages: number;
    sell_ready_tiers?: Partial<Record<SellReadyTier, number>>;
  };
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
  kind?: JournalNoteKind;
  question?: string;
  chatMode?: ChatMode;
  verseId?: string;
};
