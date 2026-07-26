/** Types for Pratibha lexicon lemmas (`data/lexicon/lemmas/*.yml`). */

export type LemmaMaturity =
  | "structural_draft"
  | "strong_draft"
  | "canonical";

export type LemmaScriptKey =
  | "iast"
  | "devanagari"
  | "greek"
  | "chinese"
  | "pinyin"
  | "arabic"
  | "latin";

export type LemmaScripts = Partial<Record<LemmaScriptKey, string>>;

export type RelatedRelation =
  | "related_as"
  | "diverges_from"
  | "rough_analogue";

export type RelatedLemma = {
  lemma_id: string;
  relation: RelatedRelation;
  note?: string;
};

export type Sense = {
  id: string;
  label: string;
  short: string;
  etymology?: string;
  traps?: string[];
  traditions?: string[];
  exemplars?: string[];
  body?: string;
};

export type Lemma = {
  id: string;
  maturity: LemmaMaturity;
  scripts?: LemmaScripts;
  aliases?: string[];
  traditions: string[];
  related?: RelatedLemma[];
  senses: Sense[];
};

/** Fast-list row from `data/lexicon/index.yml` (regenerable). */
export type LexiconIndexItem = {
  id: string;
  short: string;
  traditions: string[];
};

export type LexiconIndex = {
  lemmas: LexiconIndexItem[];
};

export type LexiconPayload = {
  index: LexiconIndexItem[];
  lemmas: Record<string, Lemma>;
};

/** List row from `GET /lexicon`. */
export type LexiconListItem = {
  id: string;
  short: string;
  traditions: string[];
  scripts?: LemmaScripts;
  maturity?: LemmaMaturity;
  aliases?: string[];
};

export type LexiconListResponse = {
  items: LexiconListItem[];
  total: number;
};

/** Slim occurrence from `GET /lexicon/{id}/passages`. */
export type LemmaPassageRef = {
  id: string;
  title?: string;
  collection?: string;
  term?: string;
  definition?: string;
};
