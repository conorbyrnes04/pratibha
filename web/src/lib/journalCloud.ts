import type { JournalNote } from "@/lib/types";
import { useCallback } from "react";
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

export type JournalSync = {
  /** True once the remote note list has loaded (or Convex is disabled). */
  ready: boolean;
  sync: () => Promise<JournalSyncResult>;
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

// `id` is the server-side row id when patching an existing note, or undefined
// when inserting. It must never be a locally-minted id (crypto UUID / "note_…")
// because the mutation validates it as a Convex `Id<"journal_notes">`.
function noteToConvex(note: JournalNote, id: Id<"journal_notes"> | undefined) {
  return {
    id,
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

function useSyncJournalLocal(): JournalSync {
  const sync = useCallback(
    async (): Promise<JournalSyncResult> => ({
      notes: loadJournalNotes(),
      status: "local",
    }),
    [],
  );
  return { ready: true, sync };
}

function useSyncJournalConvex(): JournalSync {
  const remoteNotes = useQuery(api.journalNotes.list);
  const upsert = useMutation(api.journalNotes.upsert);

  const sync = useCallback(async (): Promise<JournalSyncResult> => {
    const local = loadJournalNotes();

    if (remoteNotes === undefined) {
      return { notes: local, status: "local" };
    }

    try {
      const remote = remoteNotes.map(convexToNote);
      const remoteById = new Map(remote.map((n) => [n.id, n]));
      const merged = mergeByUpdated(local, remote);

      // Only write to Convex what actually changed, and reconcile the ids of
      // notes created on this device so they are not re-inserted every pass.
      let mutated = false;
      const reconciled: JournalNote[] = [];
      for (const note of merged) {
        const match = remoteById.get(note.id);
        if (match) {
          // Already on the server — patch only when the local copy is newer.
          if (note.updatedAt > match.updatedAt) {
            await upsert(noteToConvex(note, note.id as Id<"journal_notes">));
          }
          reconciled.push(note);
        } else {
          // Local-only note — insert once and adopt the server-assigned id.
          const newId = await upsert(noteToConvex(note, undefined));
          reconciled.push({ ...note, id: newId as unknown as string });
          mutated = true;
        }
      }

      const next = mutated ? reconciled : merged;
      saveJournalNotes(next);
      return { notes: next, status: "synced" };
    } catch (error) {
      console.warn("journal sync failed:", error);
      return {
        notes: local,
        status: "error",
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }, [remoteNotes, upsert]);

  return { ready: remoteNotes !== undefined, sync };
}

// A note id that was minted on this device (crypto UUID, "note_…", or legacy
// "jn_…") has no counterpart on the server yet, so it must be inserted rather
// than patched — and never passed to a `v.id()` argument.
function isLocalOnlyId(id: string): boolean {
  return id.startsWith("jn_") || id.startsWith("note_") || id.includes("-");
}

function usePushJournalNoteLocal() {
  return async (_note: JournalNote): Promise<void> => undefined;
}

function usePushJournalNoteConvex() {
  const upsert = useMutation(api.journalNotes.upsert);

  return async (note: JournalNote): Promise<void> => {
    try {
      const local = isLocalOnlyId(note.id);
      const newId = await upsert(
        noteToConvex(note, local ? undefined : (note.id as Id<"journal_notes">)),
      );
      // Adopt the server id locally so a later full sync patches instead of
      // inserting a duplicate.
      if (local) {
        const notes = loadJournalNotes().map((n) =>
          n.id === note.id ? { ...n, id: newId as unknown as string } : n,
        );
        saveJournalNotes(notes);
      }
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
    // Local-only notes never reached the server, so there is nothing to delete
    // (and their id would fail the `v.id()` validator).
    if (!isLocalOnlyId(id)) {
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
