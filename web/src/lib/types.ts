export type Appendix = {
  commentator?: string;
  text?: string;
};

// Graded maturity ladder (seed < draft < rich < polished). The old labels are
// retained as accepted values for back-compat with cached data and API params.
export type EditorialMaturity =
  | "seed"
  | "draft"
  | "rich"
  | "polished"
  // deprecated aliases, still accepted on input
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
  lemma_id?: string;
  sense_id?: string;
};

export type Resonance = {
  citation: string;
  resonance: string;
  divergence?: string;
  /** Corpus unit id when the cited passage exists in Pratibha (exact deep-link). */
  passage_id?: string;
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
    original_reliability?: string;
    verification?: string;
    english_source?: string;
    original_source?: string;
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
  /** English layers that already have archived ElevenLabs speech. */
  listen_sections?: Array<"translation" | "commentary" | "practice">;
};

export type Source = {
  rank: number;
  score?: number;
  text?: string;
  metadata?: Record<string, unknown>;
};

export type ChatMode = "question" | "explain" | "compare" | "practice";

export type ChatDepth = "simple" | "deep";

export type ChatOptions = {
  verseId?: string;
  compareVerseIds?: string[];
  layerFocus?: PratibhaLayerKind;
  chatMode?: ChatMode;
  /** Optional override; when omitted, backend maps question→simple and deep modes→deep. */
  depth?: ChatDepth;
  /** Bearer token so daily cap can key by user id when signed in. */
  accessToken?: string | null;
};

export type JournalNoteKind = "reflection" | "chat_response";

export type ProvenanceTier = "pd_render" | "pd_adapted" | "original";

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
  license: "public_domain" | "original_editorial";
  license_label: string;
  provenance_tier: ProvenanceTier;
  provenance_tier_label: string;
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
    provenance_tiers?: Partial<Record<ProvenanceTier, number>>;
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
