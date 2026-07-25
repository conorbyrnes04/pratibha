import type { JournalNote } from "@/lib/types";
import { loadJournalNotes, saveJournalNotes } from "@/lib/journalStorage";
import { getSupabase } from "@/lib/supabaseClient";

type Row = {
  id: string;
  user_id: string;
  passage_id: string;
  passage_title: string;
  body: string;
  tags: string[] | null;
  prompt: string | null;
  kind: string | null;
  question: string | null;
  chat_mode: string | null;
  verse_id: string | null;
  created_at: string;
  updated_at: string;
};

export type JournalSyncResult = {
  notes: JournalNote[];
  status: "synced" | "local" | "error";
  error?: string;
};

function rowToNote(row: Row): JournalNote {
  return {
    id: row.id,
    passageId: row.passage_id,
    passageTitle: row.passage_title || row.passage_id,
    body: row.body || "",
    tags: Array.isArray(row.tags) ? row.tags : [],
    prompt: row.prompt || undefined,
    kind: (row.kind as JournalNote["kind"]) || undefined,
    question: row.question || undefined,
    chatMode: (row.chat_mode as JournalNote["chatMode"]) || undefined,
    verseId: row.verse_id || undefined,
    createdAt: row.created_at,
    updatedAt: row.updated_at,
  };
}

function noteToRow(note: JournalNote, userId: string): Row {
  return {
    id: note.id,
    user_id: userId,
    passage_id: note.passageId,
    passage_title: note.passageTitle,
    body: note.body,
    tags: note.tags || [],
    prompt: note.prompt ?? null,
    kind: note.kind ?? null,
    question: note.question ?? null,
    chat_mode: note.chatMode ?? null,
    verse_id: note.verseId ?? null,
    created_at: note.createdAt,
    updated_at: note.updatedAt,
  };
}

function mergeByUpdated(local: JournalNote[], remote: JournalNote[]): JournalNote[] {
  const byId = new Map<string, JournalNote>();
  for (const n of [...remote, ...local]) {
    const prev = byId.get(n.id);
    if (!prev || n.updatedAt > prev.updatedAt) byId.set(n.id, n);
  }
  return [...byId.values()].sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}

/**
 * Pull remote notes, merge with local (newest updatedAt wins), push the union,
 * and persist locally.
 */
export async function syncJournalWithCloud(userId: string): Promise<JournalSyncResult> {
  const supabase = getSupabase();
  const local = loadJournalNotes();
  if (!supabase) return { notes: local, status: "local" };

  const { data, error } = await supabase.from("journal_notes").select("*").eq("user_id", userId);
  if (error) {
    console.warn("journal sync pull failed:", error.message);
    return { notes: local, status: "error", error: error.message };
  }

  const remote = (data as Row[]).map(rowToNote);
  const merged = mergeByUpdated(local, remote);
  saveJournalNotes(merged);

  if (merged.length) {
    const payload = merged.map((n) => noteToRow(n, userId));
    const { error: upsertError } = await supabase.from("journal_notes").upsert(payload, { onConflict: "id" });
    if (upsertError) {
      console.warn("journal sync push failed:", upsertError.message);
      return { notes: merged, status: "error", error: upsertError.message };
    }
  }

  return { notes: merged, status: "synced" };
}

export async function pushJournalNote(note: JournalNote, userId: string): Promise<void> {
  const supabase = getSupabase();
  if (!supabase) return;
  const { error } = await supabase.from("journal_notes").upsert(noteToRow(note, userId), { onConflict: "id" });
  if (error) console.warn("journal push failed:", error.message);
}

export async function deleteJournalNoteRemote(id: string): Promise<void> {
  const supabase = getSupabase();
  if (!supabase) return;
  const { error } = await supabase.from("journal_notes").delete().eq("id", id);
  if (error) console.warn("journal remote delete failed:", error.message);
}
