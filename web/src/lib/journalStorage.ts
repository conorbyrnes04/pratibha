import type { JournalNote, VerseItem } from "@/lib/types";

const STORAGE_KEY = "pratibha.journal.v1";

function now(): string {
  return new Date().toISOString();
}

function makeId(): string {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) return crypto.randomUUID();
  return `note_${Date.now()}_${Math.random().toString(36).slice(2)}`;
}

export function loadJournalNotes(): JournalNote[] {
  if (typeof window === "undefined") return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? (parsed as JournalNote[]) : [];
  } catch {
    return [];
  }
}

export function saveJournalNotes(notes: JournalNote[]): void {
  if (typeof window === "undefined") return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(notes));
}

export function notesForPassage(passageId: string): JournalNote[] {
  return loadJournalNotes()
    .filter((note) => note.passageId === passageId)
    .sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}

export function learnStepContextId(trackId: string, stepId: string): string {
  return `learn:${trackId}:${stepId}`;
}

export function upsertJournalNote(input: {
  existingId?: string;
  passage?: VerseItem;
  contextId?: string;
  contextTitle?: string;
  body: string;
  tags?: string[];
  prompt?: string;
}): JournalNote {
  const passageId = input.passage?._id || input.contextId;
  if (!passageId) {
    throw new Error("upsertJournalNote requires passage or contextId");
  }
  const passageTitle =
    input.passage?.title ||
    input.passage?.sutra_id ||
    input.contextTitle ||
    passageId;
  const notes = loadJournalNotes();
  const timestamp = now();
  const existing = input.existingId ? notes.find((note) => note.id === input.existingId) : undefined;
  const note: JournalNote = {
    id: existing?.id || makeId(),
    passageId,
    passageTitle,
    body: input.body,
    tags: input.tags || existing?.tags || [],
    prompt: input.prompt || existing?.prompt,
    createdAt: existing?.createdAt || timestamp,
    updatedAt: timestamp,
  };
  const next = existing ? notes.map((entry) => (entry.id === note.id ? note : entry)) : [note, ...notes];
  saveJournalNotes(next);
  return note;
}

export function deleteJournalNote(id: string): void {
  saveJournalNotes(loadJournalNotes().filter((note) => note.id !== id));
}
