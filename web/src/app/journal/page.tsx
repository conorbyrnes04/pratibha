'use client';

import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import type { JournalNote } from "@/lib/types";
import { useAuth } from "@/components/AuthProvider";
import { deleteJournalNoteRemote, syncJournalWithCloud } from "@/lib/journalCloud";
import { deleteJournalNote, journalSourceHref, loadJournalNotes, saveJournalNotes } from "@/lib/journalStorage";

export default function JournalPage() {
  const { user, loading: authLoading } = useAuth();
  const [notes, setNotes] = useState<JournalNote[]>([]);
  const [q, setQ] = useState("");
  const [syncState, setSyncState] = useState<"idle" | "syncing" | "synced" | "local">("idle");
  const fileRef = useRef<HTMLInputElement>(null);

  function refresh() {
    setNotes(loadJournalNotes().sort((a, b) => b.updatedAt.localeCompare(a.updatedAt)));
  }

  useEffect(() => {
    refresh();
  }, []);

  useEffect(() => {
    if (authLoading) return;
    if (!user) {
      setSyncState("local");
      return;
    }
    let active = true;
    setSyncState("syncing");
    void syncJournalWithCloud(user.id).then((merged) => {
      if (!active) return;
      setNotes(merged.sort((a, b) => b.updatedAt.localeCompare(a.updatedAt)));
      setSyncState("synced");
    });
    return () => {
      active = false;
    };
  }, [user, authLoading]);

  function exportNotes() {
    const blob = new Blob([JSON.stringify(loadJournalNotes(), null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `pratibha-journal-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  }

  async function importNotes(file: File) {
    try {
      const incoming = JSON.parse(await file.text());
      if (!Array.isArray(incoming)) throw new Error("not an array");
      // Merge by id; imported notes win on conflict.
      const byId = new Map<string, JournalNote>();
      for (const n of loadJournalNotes()) byId.set(n.id, n);
      for (const n of incoming as JournalNote[]) if (n && n.id) byId.set(n.id, n);
      saveJournalNotes([...byId.values()]);
      refresh();
    } catch {
      alert("Could not import: the file is not a valid Pratibha journal export.");
    }
  }

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase();
    if (!needle) return notes;
    return notes.filter((note) => [note.passageTitle, note.body, note.prompt, note.tags.join(" ")].join(" ").toLowerCase().includes(needle));
  }, [notes, q]);

  function remove(id: string) {
    deleteJournalNote(id);
    if (user) void deleteJournalNoteRemote(id);
    refresh();
  }

  function sourceLabel(note: JournalNote): string {
    if (note.kind === "chat_response") return "Reopen chat";
    if (note.passageId.startsWith("learn:")) return "Reopen step";
    return "Reopen passage";
  }

  return (
    <main className="page-shell">
      <header>
        <p className="eyebrow">Personal study memory</p>
        <h1 className="mt-3 text-5xl font-semibold leading-none tracking-[-0.04em] text-stone-100 sm:text-6xl">Journal</h1>
        <p className="soft mt-4 max-w-2xl text-xl leading-relaxed">
          {user
            ? "Signed in — notes sync to your account and stay cached in this browser."
            : "Saved reflections stay in this browser. Sign in to sync them across devices."}
        </p>
        {!user && !authLoading ? (
          <Link href="/login?next=/journal" className="btn-secondary mt-4 inline-flex px-4 py-2 text-sm">
            Sign in to sync
          </Link>
        ) : null}
      </header>

      <div className="mt-8 flex flex-wrap items-center gap-3">
        <input
          value={q}
          onChange={(event) => setQ(event.target.value)}
          className="input-field min-w-0 flex-1 rounded-lg px-3 py-2"
          placeholder="Search notes, passages, prompts..."
        />
        <div className="flex shrink-0 items-center gap-2">
          <button onClick={exportNotes} disabled={notes.length === 0} className="btn-secondary px-4 py-2 text-sm disabled:opacity-50">
            Export
          </button>
          <button onClick={() => fileRef.current?.click()} className="btn-secondary px-4 py-2 text-sm">
            Import
          </button>
          <input
            ref={fileRef}
            type="file"
            accept="application/json,.json"
            className="hidden"
            onChange={(e) => {
              const f = e.target.files?.[0];
              if (f) importNotes(f);
              e.target.value = "";
            }}
          />
        </div>
      </div>
      <p className="soft mt-2 font-sans text-xs leading-relaxed text-stone-500">
        {syncState === "syncing"
          ? "Syncing journal with your account…"
          : syncState === "synced"
            ? "Synced with your account. Export still makes a handy local backup."
            : "On this device only until you sign in. Export a backup if you clear the browser."}
      </p>

      <div className="mt-8 space-y-4">
        {filtered.length === 0 ? (
          <section className="card flex flex-col items-center gap-3 p-10 text-center">
            <p className="text-2xl text-amber-100">
              {notes.length === 0 ? "Your journal is empty" : "No matching notes"}
            </p>
            <p className="soft max-w-md">
              {notes.length === 0
                ? "Save a reflection from a passage, a learning step, or an Ask Pratibha response, and it will appear here."
                : "Try a different search term to find your saved reflections."}
            </p>
            {notes.length === 0 ? (
              <Link href="/read" className="btn-primary mt-2 px-5 py-2.5 text-sm">
                Browse the library
              </Link>
            ) : null}
          </section>
        ) : (
          filtered.map((note) => (
            <article key={note.id} className="card p-5 sm:p-6">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="layer-heading">{new Date(note.updatedAt).toLocaleString()}</p>
                  <h2 className="mt-2 text-2xl text-amber-100">{note.passageTitle}</h2>
                  {note.kind === "chat_response" && note.question ? (
                    <p className="soft mt-2 text-sm">You asked: {note.question}</p>
                  ) : null}
                </div>
                <div className="flex shrink-0 gap-2">
                  {journalSourceHref(note) ? (
                    <Link href={journalSourceHref(note)!} className="btn-secondary px-4 py-2 text-sm">
                      {sourceLabel(note)}
                    </Link>
                  ) : null}
                  <button onClick={() => remove(note.id)} className="btn-secondary px-4 py-2 text-sm">
                    Delete
                  </button>
                </div>
              </div>
              {note.prompt ? <p className="soft mt-4 text-sm">{note.prompt}</p> : null}
              <p className="mt-4 whitespace-pre-wrap leading-relaxed text-stone-200">{note.body}</p>
              {note.tags.length > 0 ? (
                <div className="mt-4 flex flex-wrap gap-2">
                  {note.tags.map((tag) => (
                    <span
                      key={tag}
                      className="rounded-full border border-amber-200/20 px-3 py-1 font-sans text-xs text-stone-400"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              ) : null}
            </article>
          ))
        )}
      </div>
    </main>
  );
}
