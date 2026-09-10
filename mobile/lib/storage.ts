import { getCloudBridge } from "@/lib/cloudBridge";
import type { ChatMode, JournalNote, VerseItem } from "@shared/types";
import AsyncStorage from "@react-native-async-storage/async-storage";

export const LEARN_KEY = "pratibha.learn.v1";
export const JOURNAL_KEY = "pratibha.journal.v1";
export const API_OVERRIDE_KEY = "pratibha.apiBase";
export const APP_ICON_KEY = "pratibha.appIcon.v1";
export const THEME_KEY = "pratibha.theme.v1";

export type ProgressMap = Record<string, boolean>;
export type CompletedAtMap = Record<string, string>;
export type LearnBundle = { progress: ProgressMap; completedAt: CompletedAtMap };

export function stepKey(trackId: string, stepId: string): string {
  return `${trackId}:${stepId}`;
}

function asMap(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : {};
}

export function asProgress(value: unknown): ProgressMap {
  const out: ProgressMap = {};
  for (const [k, v] of Object.entries(asMap(value))) {
    if (typeof v === "boolean") out[k] = v;
  }
  return out;
}

export function asCompletedAt(value: unknown): CompletedAtMap {
  const out: CompletedAtMap = {};
  for (const [k, v] of Object.entries(asMap(value))) {
    if (typeof v === "string" && v) out[k] = v;
  }
  return out;
}

export function mergeProgress(local: ProgressMap, remote: ProgressMap): ProgressMap {
  const keys = new Set([...Object.keys(local), ...Object.keys(remote)]);
  const out: ProgressMap = {};
  for (const k of keys) out[k] = Boolean(local[k] || remote[k]);
  return out;
}

export function mergeCompletedAt(local: CompletedAtMap, remote: CompletedAtMap): CompletedAtMap {
  const keys = new Set([...Object.keys(local), ...Object.keys(remote)]);
  const out: CompletedAtMap = {};
  for (const k of keys) {
    const a = local[k];
    const b = remote[k];
    if (a && b) out[k] = a < b ? a : b;
    else out[k] = a || b || "";
    if (!out[k]) delete out[k];
  }
  return out;
}

export async function loadLearnBundle(): Promise<LearnBundle> {
  try {
    const raw = await AsyncStorage.getItem(LEARN_KEY);
    if (!raw) return { progress: {}, completedAt: {} };
    const parsed = JSON.parse(raw) as unknown;
    const obj = asMap(parsed);
    if (typeof obj.progress === "object" && obj.progress !== null && !Array.isArray(obj.progress)) {
      return {
        progress: asProgress(obj.progress),
        completedAt: asCompletedAt(obj.completedAt),
      };
    }
    return { progress: asProgress(parsed), completedAt: {} };
  } catch {
    return { progress: {}, completedAt: {} };
  }
}

export async function saveLearnBundle(bundle: LearnBundle): Promise<void> {
  await AsyncStorage.setItem(LEARN_KEY, JSON.stringify(bundle));
}

export async function loadProgress(): Promise<ProgressMap> {
  return (await loadLearnBundle()).progress;
}

export async function saveProgress(progress: ProgressMap): Promise<void> {
  const prev = await loadLearnBundle();
  await saveLearnBundle({ ...prev, progress });
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
  try {
    const cloudId = await getCloudBridge()?.pushNote(note);
    if (cloudId && cloudId !== note.id) {
      const latest = await loadJournalNotes();
      const next = latest.map((n) => (n.id === note.id ? { ...n, id: cloudId } : n));
      await saveJournalNotes(next);
      return { ...note, id: cloudId };
    }
  } catch {
    /* keep the local note; next sign-in sync retries */
  }
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
  try {
    await getCloudBridge()?.deleteNote(id);
  } catch {
    /* local delete still stands */
  }
}

export async function notesForContext(contextId: string): Promise<JournalNote[]> {
  return (await loadJournalNotes())
    .filter((n) => n.passageId === contextId)
    .sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}
