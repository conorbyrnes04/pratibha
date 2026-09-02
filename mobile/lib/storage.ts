import AsyncStorage from "@react-native-async-storage/async-storage";
import type { ChatMode, JournalNote, VerseItem } from "@shared/types";

export const LEARN_KEY = "pratibha.learn.v1";
export const JOURNAL_KEY = "pratibha.journal.v1";
export const API_OVERRIDE_KEY = "pratibha.apiBase";
export const APP_ICON_KEY = "pratibha.appIcon.v1";

export type ProgressMap = Record<string, boolean>;

export function stepKey(trackId: string, stepId: string): string {
  return `${trackId}:${stepId}`;
}

export async function loadProgress(): Promise<ProgressMap> {
  try {
    const raw = await AsyncStorage.getItem(LEARN_KEY);
    if (!raw) return {};
    const parsed = JSON.parse(raw) as ProgressMap;
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

export async function saveProgress(progress: ProgressMap): Promise<void> {
  await AsyncStorage.setItem(LEARN_KEY, JSON.stringify(progress));
}

export async function loadJournalNotes(): Promise<JournalNote[]> {
  try {
    const raw = await AsyncStorage.getItem(JOURNAL_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? (parsed as JournalNote[]) : [];
  } catch {
    return [];
  }
}

export async function saveJournalNotes(notes: JournalNote[]): Promise<void> {
  await AsyncStorage.setItem(JOURNAL_KEY, JSON.stringify(notes));
}

export function learnStepContextId(trackId: string, stepId: string): string {
  return `learn:${trackId}:${stepId}`;
}

function makeId(): string {
  return `note_${Date.now()}_${Math.random().toString(36).slice(2)}`;
}

export async function upsertJournalNote(input: {
  contextId?: string;
  contextTitle?: string;
  passage?: VerseItem;
  body: string;
  prompt?: string;
  tags?: string[];
  kind?: JournalNote["kind"];
  question?: string;
  chatMode?: ChatMode;
  verseId?: string;
}): Promise<JournalNote> {
  const notes = await loadJournalNotes();
  const passageId = input.passage?._id || input.contextId;
  if (!passageId) throw new Error("passage or contextId required");
  const timestamp = new Date().toISOString();
  const note: JournalNote = {
    id: makeId(),
    passageId,
    passageTitle:
      input.passage?.title || input.passage?.sutra_id || input.contextTitle || passageId,
    body: input.body,
    tags: input.tags || [],
    prompt: input.prompt,
    kind: input.kind,
    question: input.question,
    chatMode: input.chatMode,
    verseId: input.verseId,
    createdAt: timestamp,
    updatedAt: timestamp,
  };
  await saveJournalNotes([note, ...notes]);
  return note;
}

export async function saveChatResponse(input: {
  answer: string;
  question: string;
  verse?: VerseItem | null;
  chatMode?: ChatMode;
}): Promise<JournalNote> {
  const cleanAnswer = input.answer.trim();
  const cleanQuestion = input.question.trim();
  if (!cleanAnswer) throw new Error("saveChatResponse requires a non-empty answer");
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

export async function deleteJournalNote(id: string): Promise<void> {
  const notes = await loadJournalNotes();
  await saveJournalNotes(notes.filter((n) => n.id !== id));
}

export async function notesForContext(contextId: string): Promise<JournalNote[]> {
  return (await loadJournalNotes())
    .filter((n) => n.passageId === contextId)
    .sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}
