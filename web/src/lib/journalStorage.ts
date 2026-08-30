import type { ChatMode, JournalNote, VerseItem } from "@/lib/types";
import { displayPassageTitle } from "@/lib/passageTitles";

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

export function learnStepContextId(
  trackId: string,
  stepId: string,
  thread?: { threadId?: string | null; beadId?: string | null },
): string {
  const base = `learn:${trackId}:${stepId}`;
  if (thread?.threadId && thread?.beadId) {
    return `${base}:${thread.threadId}:${thread.beadId}`;
  }
  return base;
}

export function journalSourceHref(note: JournalNote): string | null {
  if (note.passageId.startsWith("learn:")) {
    const parts = note.passageId.split(":");
    const trackId = parts[1];
    const stepId = parts[2];
    const threadId = parts[3];
    const beadId = parts[4];
    if (!trackId || !stepId) return "/learn";
    const params = new URLSearchParams();
    if (threadId && beadId) {
      params.set("thread", threadId);
      params.set("bead", beadId);
    } else {
      params.set("track", trackId);
      params.set("step", stepId);
    }
    return `/learn?${params.toString()}`;
  }
  if (note.kind === "chat_response" || note.passageId.startsWith("chat:")) {
    const params = new URLSearchParams();
    if (note.verseId) params.set("verse_id", note.verseId);
    if (note.question) params.set("q", note.question);
    const qs = params.toString();
    return qs ? `/chat?${qs}` : "/chat";
  }
  return `/read/${encodeURIComponent(note.passageId)}`;
}

export function saveChatResponse(input: {
  answer: string;
  question: string;
  verse?: VerseItem | null;
  chatMode?: ChatMode;
}): JournalNote {
  const cleanAnswer = input.answer.trim();
  const cleanQuestion = input.question.trim();
  if (!cleanAnswer) {
    throw new Error("saveChatResponse requires a non-empty answer");
  }
  const shared = {
    body: cleanAnswer,
    prompt: cleanQuestion || "Ask Pratibha",
    kind: "chat_response" as const,
    question: cleanQuestion || undefined,
    chatMode: input.chatMode,
    tags: ["chat"],
  };
  if (input.verse) {
    return upsertJournalNote({
      ...shared,
      passage: input.verse,
      verseId: input.verse._id,
    });
  }
  return upsertJournalNote({
    ...shared,
    contextId: `chat:${Date.now()}`,
    contextTitle: "Ask Pratibha",
  });
}

export function upsertJournalNote(input: {
  existingId?: string;
  passage?: VerseItem;
  contextId?: string;
  contextTitle?: string;
  body: string;
  tags?: string[];
  prompt?: string;
  kind?: JournalNote["kind"];
  question?: string;
  chatMode?: ChatMode;
  verseId?: string;
}): JournalNote {
  const passageId = input.passage?._id || input.contextId;
  if (!passageId) {
    throw new Error("upsertJournalNote requires passage or contextId");
  }
  const passageTitle = input.passage ? displayPassageTitle(input.passage) : input.contextTitle || passageId;
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
    kind: input.kind || existing?.kind,
    question: input.question || existing?.question,
    chatMode: input.chatMode || existing?.chatMode,
    verseId: input.verseId || existing?.verseId,
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
