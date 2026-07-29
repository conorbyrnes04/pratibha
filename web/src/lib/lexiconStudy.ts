import type { SrsEntry, SrsGrade, StudyCard, StudyDeckId } from "@/lib/lexiconStudyTypes";

const STORAGE_KEY = "pratibha.lexicon.srs.v1";
const DAY_MS = 24 * 60 * 60 * 1000;

export function scriptClassName(scriptClass?: string): string {
  switch (scriptClass) {
    case "devanagari":
      return "source-script";
    case "chinese":
      return "source-script source-script--latin lex-study-script--cjk";
    case "greek":
      return "source-script source-script--latin";
    case "arabic":
      return "source-script source-script--latin lex-study-script--arabic";
    default:
      return "source-script source-script--latin";
  }
}

export function modeLabel(mode: StudyCard["mode"]): string {
  switch (mode) {
    case "recognition":
      return "Recognize";
    case "trap":
      return "Trap";
    case "production":
      return "Produce";
    default:
      return mode;
  }
}

export function loadSrsMap(): Record<string, SrsEntry> {
  if (typeof window === "undefined") return {};
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) return {};
    const parsed = JSON.parse(raw) as Record<string, SrsEntry>;
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

export function saveSrsMap(map: Record<string, SrsEntry>): void {
  if (typeof window === "undefined") return;
  window.localStorage.setItem(STORAGE_KEY, JSON.stringify(map));
}

function ensureEntry(map: Record<string, SrsEntry>, cardId: string): SrsEntry {
  const existing = map[cardId];
  if (existing) return existing;
  return {
    cardId,
    ease: 2.5,
    intervalDays: 0,
    due: 0,
    reps: 0,
    lapses: 0,
  };
}

/** SM-2–ish scheduling tuned for short sacred-term sessions. */
export function gradeCard(
  map: Record<string, SrsEntry>,
  cardId: string,
  grade: SrsGrade,
  now = Date.now(),
): Record<string, SrsEntry> {
  const entry = { ...ensureEntry(map, cardId) };
  let ease = entry.ease;
  let interval = entry.intervalDays;
  let reps = entry.reps;
  let lapses = entry.lapses;

  if (grade === "again") {
    reps = 0;
    lapses += 1;
    interval = 0;
    ease = Math.max(1.3, ease - 0.2);
  } else if (grade === "hard") {
    reps += 1;
    interval = interval <= 0 ? 0.5 : Math.max(1, interval * 1.2);
    ease = Math.max(1.3, ease - 0.15);
  } else if (grade === "good") {
    reps += 1;
    interval = interval <= 0 ? 1 : interval * ease;
    ease = ease + 0.0;
  } else {
    reps += 1;
    interval = interval <= 0 ? 3 : interval * ease * 1.3;
    ease = ease + 0.15;
  }

  const next: SrsEntry = {
    cardId,
    ease: Math.round(ease * 100) / 100,
    intervalDays: Math.round(interval * 100) / 100,
    due: now + Math.max(0, interval) * DAY_MS,
    reps,
    lapses,
  };

  return { ...map, [cardId]: next };
}

function shuffle<T>(items: T[]): T[] {
  const out = [...items];
  for (let i = out.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

export type DeckStats = {
  due: number;
  new: number;
  learning: number;
  total: number;
};

export function deckStats(
  cards: StudyCard[],
  deckId: StudyDeckId,
  srs: Record<string, SrsEntry>,
  now = Date.now(),
): DeckStats {
  const pool = cards.filter((c) => c.deck_id === deckId);
  let due = 0;
  let neu = 0;
  let learning = 0;
  for (const card of pool) {
    const entry = srs[card.id];
    if (!entry || entry.reps === 0) {
      neu += 1;
    } else if (entry.due <= now) {
      due += 1;
    } else {
      learning += 1;
    }
  }
  return { due, new: neu, learning, total: pool.length };
}

/**
 * Build a session queue: due cards first, then unseen, capped.
 * If the deck is caught up, pull a light ahead-review so small decks stay usable.
 */
export function buildSessionQueue(
  cards: StudyCard[],
  deckId: StudyDeckId,
  srs: Record<string, SrsEntry>,
  limit = 18,
  now = Date.now(),
): StudyCard[] {
  const pool = cards.filter((c) => c.deck_id === deckId);
  const due: StudyCard[] = [];
  const neu: StudyCard[] = [];
  const ahead: StudyCard[] = [];

  for (const card of pool) {
    const entry = srs[card.id];
    if (!entry || entry.reps === 0) {
      neu.push(card);
    } else if (entry.due <= now) {
      due.push(card);
    } else {
      ahead.push(card);
    }
  }

  const modeRank = (m: StudyCard["mode"]) =>
    m === "recognition" ? 0 : m === "trap" ? 1 : 2;

  const sortBucket = (bucket: StudyCard[]) =>
    shuffle(bucket).sort((a, b) => modeRank(a.mode) - modeRank(b.mode));

  let queue = [...sortBucket(due), ...sortBucket(neu)];
  if (queue.length === 0) {
    queue = sortBucket(ahead).slice(0, Math.min(limit, 8));
  }
  return queue.slice(0, limit);
}
