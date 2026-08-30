import type { JournalNote } from "@/lib/types";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { loadJournalNotes, saveJournalNotes } from "@/lib/journalStorage";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import { Id } from "../../convex/_generated/dataModel";

export type JournalSyncResult = {
  notes: JournalNote[];
  status: "synced" | "local" | "error";
  error?: string;
};

function convexToNote(row: any): JournalNote {
  return {
    id: row._id,
    passageId: row.passageId,
    passageTitle: row.passageTitle || row.passageId,
    body: row.body || "",
    tags: Array.isArray(row.tags) ? row.tags : [],
    prompt: row.prompt || undefined,
    kind: row.kind || undefined,
    question: row.question || undefined,
    chatMode: row.chatMode || undefined,
    verseId: row.verseId || undefined,
    createdAt: row.createdAt,
    updatedAt: row.updatedAt,
  };
}

function noteToConvex(note: JournalNote) {
  return {
    id: note.id.startsWith("jn_") ? undefined : (note.id as Id<"journal_notes">),
    passageId: note.passageId,
    passageTitle: note.passageTitle,
    body: note.body,
    tags: note.tags || [],
    prompt: note.prompt,
    kind: note.kind,
    question: note.question,
    chatMode: note.chatMode,
    verseId: note.verseId,
    createdAt: note.createdAt,
    updatedAt: note.updatedAt,
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

function useSyncJournalLocal() {
  return {
    sync: async (): Promise<JournalSyncResult> => ({
      notes: loadJournalNotes(),
      status: "local",
    }),
  };
}

function useSyncJournalConvex() {
  const remoteNotes = useQuery(api.journalNotes.list);
  const upsert = useMutation(api.journalNotes.upsert);

  const sync = async (): Promise<JournalSyncResult> => {
    const local = loadJournalNotes();

    if (remoteNotes === undefined) {
      return { notes: local, status: "local" };
    }

    try {
      const remote = remoteNotes.map(convexToNote);
      const merged = mergeByUpdated(local, remote);
      saveJournalNotes(merged);

      if (merged.length) {
        for (const note of merged) {
          await upsert(noteToConvex(note));
        }
      }

      return { notes: merged, status: "synced" };
    } catch (error) {
      console.warn("journal sync failed:", error);
      return {
        notes: local,
        status: "error",
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  };

  return { sync };
}

function usePushJournalNoteLocal() {
  return async (_note: JournalNote): Promise<void> => undefined;
}

function usePushJournalNoteConvex() {
  const upsert = useMutation(api.journalNotes.upsert);

  return async (note: JournalNote): Promise<void> => {
    try {
      await upsert(noteToConvex(note));
    } catch (error) {
      console.warn("journal push failed:", error);
    }
  };
}

function useDeleteJournalNoteLocal() {
  return async (_id: string): Promise<void> => undefined;
}

function useDeleteJournalNoteConvex() {
  const remove = useMutation(api.journalNotes.remove);

  return async (id: string): Promise<void> => {
    if (!id.startsWith("jn_")) {
      try {
        await remove({ id: id as Id<"journal_notes"> });
      } catch (error) {
        console.warn("journal remote delete failed:", error);
      }
    }
  };
}

export const useSyncJournal = CONVEX_ENABLED ? useSyncJournalConvex : useSyncJournalLocal;
export const usePushJournalNote = CONVEX_ENABLED ? usePushJournalNoteConvex : usePushJournalNoteLocal;
export const useDeleteJournalNote = CONVEX_ENABLED
  ? useDeleteJournalNoteConvex
  : useDeleteJournalNoteLocal;
