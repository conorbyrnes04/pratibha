import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/convexApi";
import { isLocalOnlyId, setCloudBridge } from "@/lib/cloudBridge";
import { loadJournalNotes, saveJournalNotes } from "@/lib/storage";
import type { JournalNote } from "@shared/types";
import { useMutation, useQuery } from "convex/react";
import { useEffect, useLayoutEffect, useRef, type ReactNode } from "react";

function convexToNote(row: {
  _id: string;
  passageId: string;
  passageTitle?: string;
  body?: string;
  tags?: string[];
  prompt?: string;
  kind?: string;
  question?: string;
  chatMode?: string;
  verseId?: string;
  createdAt: string;
  updatedAt: string;
}): JournalNote {
  return {
    id: row._id,
    passageId: row.passageId,
    passageTitle: row.passageTitle || row.passageId,
    body: row.body || "",
    tags: Array.isArray(row.tags) ? row.tags : [],
    prompt: row.prompt,
    kind: row.kind as JournalNote["kind"],
    question: row.question,
    chatMode: row.chatMode as JournalNote["chatMode"],
    verseId: row.verseId,
    createdAt: row.createdAt,
    updatedAt: row.updatedAt,
  };
}

function notePayload(note: JournalNote, id?: string) {
  return {
    ...(id ? { id: id as never } : {}),
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

function mergeNotes(local: JournalNote[], remote: JournalNote[]): JournalNote[] {
  const byId = new Map<string, JournalNote>();
  for (const n of [...remote, ...local]) {
    const prev = byId.get(n.id);
    if (!prev || n.updatedAt > prev.updatedAt) byId.set(n.id, n);
  }
  return [...byId.values()].sort((a, b) => b.updatedAt.localeCompare(a.updatedAt));
}

export function CloudSync({ children }: { children: ReactNode }) {
  const { user, loading } = useAuth();
  const signedIn = Boolean(user);
  const remoteNotes = useQuery(api.journalNotes.list, signedIn ? {} : "skip");
  const upsertNote = useMutation(api.journalNotes.upsert);
  const removeNote = useMutation(api.journalNotes.remove);
  const upsertProgress = useMutation(api.learnProgress.upsert);

  useLayoutEffect(() => {
    if (!signedIn) {
      setCloudBridge(null);
      return;
    }
    setCloudBridge({
      signedIn: true,
      pushNote: async (note) => {
        const local = isLocalOnlyId(note.id);
        const newId = await upsertNote(notePayload(note, local ? undefined : note.id));
        return local && newId != null ? String(newId) : undefined;
      },
      deleteNote: async (id) => {
        if (!isLocalOnlyId(id)) await removeNote({ id: id as never });
      },
      pushProgress: async (progress, completedAt) => {
        await upsertProgress({ progress, completedAt });
      },
    });
    return () => setCloudBridge(null);
  }, [signedIn, upsertNote, removeNote, upsertProgress]);

  const pushingIds = useRef(new Set<string>());

  useEffect(() => {
    if (!signedIn || loading || remoteNotes === undefined) return;
    let cancelled = false;
    (async () => {
      const local = await loadJournalNotes();
      const rows = Array.isArray(remoteNotes) ? remoteNotes : [];
      const remote = rows.map((row) => convexToNote(row as Parameters<typeof convexToNote>[0]));
      const remoteById = new Map(remote.map((n) => [n.id, n]));
      const merged = mergeNotes(local, remote);
      const reconciled: JournalNote[] = [];
      for (const note of merged) {
        if (cancelled) return;
        const match = remoteById.get(note.id);
        if (match) {
          if (note.updatedAt > match.updatedAt) {
            await upsertNote(notePayload(note, note.id));
          }
          reconciled.push(note);
        } else if (isLocalOnlyId(note.id)) {
          if (pushingIds.current.has(note.id)) {
            reconciled.push(note);
            continue;
          }
          pushingIds.current.add(note.id);
          try {
            const newId = await upsertNote(notePayload(note));
            reconciled.push({ ...note, id: String(newId) });
          } finally {
            pushingIds.current.delete(note.id);
          }
        } else {
          reconciled.push(note);
        }
      }
      if (!cancelled) await saveJournalNotes(reconciled);
    })().catch(() => undefined);
    return () => {
      cancelled = true;
    };
  }, [signedIn, loading, remoteNotes, upsertNote]);

  return <>{children}</>;
}
