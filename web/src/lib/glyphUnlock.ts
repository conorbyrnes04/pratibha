import { dropCatalogCaches, evictStaleCatalogCaches } from "@/lib/catalogCache";
import { loadJournalNotes } from "@/lib/journalStorage";
import { SHARE_FORCE_MARKS, type ShareForceMark } from "@/lib/shareCard";
import { evictStudyI18nCache } from "@/lib/studyI18n";

const STORAGE_KEY = "pratibha.study.v1";
export const GLYPH_UNLOCK_EVENT = "pratibha:glyph-unlock";

/** Always available so a first folio still has a small palette. */
export const STARTER_MARKS: ShareForceMark[] = [
  "lotus",
  "circle",
  "moon",
  "fire",
  "tree",
  "heart",
  "water",
  "mountain",
];

type StudyEntry = { at: number; mark?: ShareForceMark };
type PracticeEntry = { at: number };
type StudyLedger = {
  verses: Record<string, StudyEntry>;
  practices?: Record<string, PracticeEntry>;
};

function emptyLedger(): StudyLedger {
  return { verses: {}, practices: {} };
}

export function loadStudyLedger(): StudyLedger {
  if (typeof window === "undefined") return emptyLedger();
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return emptyLedger();
    const parsed = JSON.parse(raw) as StudyLedger;
    if (!parsed || typeof parsed !== "object" || !parsed.verses) return emptyLedger();
    return {
      verses: parsed.verses,
      practices: parsed.practices && typeof parsed.practices === "object" ? parsed.practices : {},
    };
  } catch {
    return emptyLedger();
  }
}

function compactLedger(ledger: StudyLedger): StudyLedger {
  const verses = Object.entries(ledger.verses)
    .sort((a, b) => (b[1].at || 0) - (a[1].at || 0))
    .slice(0, 400);
  const practices = Object.entries(ledger.practices || {})
    .sort((a, b) => (b[1].at || 0) - (a[1].at || 0))
    .slice(0, 400);
  return {
    verses: Object.fromEntries(verses),
    practices: Object.fromEntries(practices),
  };
}

function writeLedger(ledger: StudyLedger): boolean {
  const raw = JSON.stringify(ledger);
  try {
    localStorage.setItem(STORAGE_KEY, raw);
    return true;
  } catch {
    evictStaleCatalogCaches();
    try {
      localStorage.setItem(STORAGE_KEY, raw);
      return true;
    } catch {
      dropCatalogCaches();
      evictStudyI18nCache();
      try {
        localStorage.setItem(STORAGE_KEY, raw);
        return true;
      } catch {
        try {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(compactLedger(ledger)));
          return true;
        } catch {
          return false;
        }
      }
    }
  }
}

function saveStudyLedger(ledger: StudyLedger): void {
  if (typeof window === "undefined") return;
  writeLedger(ledger);
}

function isCorpusVerseId(id: string): boolean {
  return Boolean(id) && !id.startsWith("learn:") && !id.startsWith("chat:");
}

function practiceIds(ledger = loadStudyLedger()): string[] {
  return Object.keys(ledger.practices || {});
}

/** Distinct passages already sat with — ledger, journal, and optional manuscript. */
export function studiedVerseIds(extraVerseIds: string[] = []): string[] {
  const ids = new Set<string>();
  for (const id of Object.keys(loadStudyLedger().verses)) {
    if (isCorpusVerseId(id)) ids.add(id);
  }
  for (const note of loadJournalNotes()) {
    if (isCorpusVerseId(note.passageId)) ids.add(note.passageId);
    if (note.verseId && isCorpusVerseId(note.verseId)) ids.add(note.verseId);
  }
  for (const id of extraVerseIds) {
    if (isCorpusVerseId(id)) ids.add(id);
  }
  return [...ids];
}

/**
 * Same sequence for every student: common marks first, Śiva last.
 * A verse may use its own mark on that folio, but it does not skip this line.
 */
export const UNLOCK_ORDER: ShareForceMark[] = [
  "vine",
  "oak",
  "rose",
  "mushroom",
  "earth",
  "air",
  "ocean",
  "storm",
  "desert",
  "lightning",
  "rainbow",
  "tides",
  "volcano",
  "star",
  "sun",
  "spiral",
  "comet",
  "eye",
  "triangle",
  "cross",
  "mirror",
  "chalice",
  "fish",
  "bee",
  "deer",
  "fox",
  "owl",
  "crow",
  "horse",
  "ox",
  "turtle",
  "wolf",
  "spider",
  "crane",
  "swan",
  "hawk",
  "eagle",
  "dolphin",
  "butterfly",
  "lion",
  "tiger",
  "bear",
  "elephant",
  "whale",
  "mandala",
  "labyrinth",
  "yantra",
  "celtic_key",
  "celtic_star",
  "constellation",
  "infinity",
  "void",
  "yin_yang",
  "stag",
  "raven",
  "serpent",
  "dragon",
  "fool",
  "maiden",
  "mother",
  "warrior",
  "hermit",
  "king",
  "sage",
  "shaman",
  "ganesha",
  "vishnu",
  "lakshmi",
  "saraswati",
  "durga",
  "kali",
  "brahma",
  "zeus",
  "apollo",
  "artemis",
  "athena",
  "hera",
  "hades",
  "persephone",
  "dionysus",
  "eros",
  "odin",
  "thor",
  "freyja",
  "loki",
  "isis",
  "osiris",
  "horus",
  "anubis",
  "thoth",
  "oshun",
  "yemaya",
  "shango",
  "nuwa",
  "quetzalcoatl",
  "tezcatlipoca",
  "thunderbird",
  "thanatos",
  "shiva",
];

function dripQueue(): ShareForceMark[] {
  const starters = new Set<string>(STARTER_MARKS);
  const listed = new Set<string>(UNLOCK_ORDER);
  const extra = SHARE_FORCE_MARKS.filter((mark) => !starters.has(mark) && !listed.has(mark));
  return [...UNLOCK_ORDER.filter((mark) => !starters.has(mark)), ...extra];
}

function studyCredits(extraVerseIds: string[] = []): number {
  return studiedVerseIds(extraVerseIds).length + practiceIds().length;
}

export function unlockedMarks(input: {
  verseMark?: ShareForceMark;
  extraVerseIds?: string[];
} = {}): Set<ShareForceMark> {
  const unlocked = new Set<ShareForceMark>(STARTER_MARKS);
  if (input.verseMark) unlocked.add(input.verseMark);
  let granted = 0;
  const credits = studyCredits(input.extraVerseIds);
  for (const mark of dripQueue()) {
    if (unlocked.has(mark)) continue;
    if (granted >= credits) break;
    unlocked.add(mark);
    granted += 1;
  }
  return unlocked;
}

export function unlockProgress(unlocked: Set<ShareForceMark>): {
  remaining: number;
  nextUnlockIn: number;
} {
  const remaining = SHARE_FORCE_MARKS.length - unlocked.size;
  if (remaining <= 0) return { remaining: 0, nextUnlockIn: 0 };
  return { remaining, nextUnlockIn: 1 };
}

export function glyphMalaStats(unlocked: Set<ShareForceMark>): {
  opened: number;
  total: number;
  remaining: number;
  complete: boolean;
} {
  const total = SHARE_FORCE_MARKS.length;
  const opened = Math.min(unlocked.size, total);
  return { opened, total, remaining: total - opened, complete: opened >= total };
}

export const UNLOCK_HINT =
  "Sit with a passage, or use manuscript, glossary, lexicon, chat, journal, or a path.";

let pendingUnlocks: ShareForceMark[] = [];
let unlockListeners = 0;

export function takePendingUnlocks(): ShareForceMark[] {
  const next = pendingUnlocks;
  pendingUnlocks = [];
  return next;
}

export function retainUnlockListener(): ShareForceMark[] {
  unlockListeners += 1;
  return takePendingUnlocks();
}

export function releaseUnlockListener(): void {
  unlockListeners = Math.max(0, unlockListeners - 1);
}

export function emitGlyphUnlocks(marks: ShareForceMark[]): void {
  if (marks.length === 0) return;
  const shown = marks.slice(0, 2);
  if (typeof window === "undefined" || unlockListeners === 0) {
    pendingUnlocks = [...pendingUnlocks, ...shown];
    return;
  }
  window.dispatchEvent(new CustomEvent(GLYPH_UNLOCK_EVENT, { detail: { marks: shown } }));
}

function freshMarks(before: Set<ShareForceMark>, after: Set<ShareForceMark>): ShareForceMark[] {
  return [...after].filter((slug) => !before.has(slug));
}

export function recordStudy(verseId: string, mark: ShareForceMark): {
  firstTime: boolean;
  freshMarks: ShareForceMark[];
} {
  const before = unlockedMarks({ verseMark: mark });
  const ledger = loadStudyLedger();
  const firstTime = !ledger.verses[verseId];
  if (!ledger.verses[verseId]) {
    ledger.verses[verseId] = { at: Date.now(), mark };
  } else if (!ledger.verses[verseId]!.mark) {
    ledger.verses[verseId] = { ...ledger.verses[verseId]!, mark };
  }
  saveStudyLedger(ledger);
  const unlocked = freshMarks(before, unlockedMarks({ verseMark: mark }));
  emitGlyphUnlocks(unlocked);
  return { firstTime, freshMarks: unlocked };
}

/** First use of a distinct practice (lemma, chat verse, learn step, …) stays unlocked. */
export function recordPractice(practiceId: string): ShareForceMark[] {
  if (typeof window === "undefined" || !practiceId) return [];
  const before = unlockedMarks({});
  const ledger = loadStudyLedger();
  const practices = { ...(ledger.practices || {}) };
  if (practices[practiceId]) return [];
  practices[practiceId] = { at: Date.now() };
  ledger.practices = practices;
  saveStudyLedger(ledger);
  const unlocked = freshMarks(before, unlockedMarks({}));
  emitGlyphUnlocks(unlocked);
  return unlocked;
}
