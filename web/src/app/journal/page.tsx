'use client';

import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import type { JournalNote } from "@/lib/types";
import { deleteJournalNote, journalSourceHref, loadJournalNotes, saveJournalNotes } from "@/lib/journalStorage";

export default function JournalPage() {
  const [notes, setNotes] = useState<JournalNote[]>([]);
  const [q, setQ] = useState("");
  const fileRef = useRef<HTMLInputElement>(null);

  function refresh() {
    setNotes(loadJournalNotes().sort((a, b) => b.updatedAt.localeCompare(a.updatedAt)));
  }

  useEffect(() => {
    refresh();
  }, []);

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
    refresh();
  }

  function sourceLabel(note: JournalNote): string {
    if (note.kind === "chat_response") return "Reopen chat";
    if (note.passageId.startsWith("learn:")) return "Reopen step";
    return "Reopen passage";
  }

  return (
    <main className="page-shell">
      <p className="eyebrow">Personal study memory</p>
      <h1 className="mt-3 text-5xl font-semibold leading-none tracking-[-0.04em] text-stone-100 sm:text-6xl">Journal</h1>
      <p className="soft mt-4 max-w-2xl text-xl leading-relaxed">Saved reflections stay local in this browser and remain linked to their source passages. They are not synced — export a backup so you don&apos;t lose them if you clear your browser or switch devices.</p>

      <div className="mt-6 flex flex-wrap items-center gap-3">
        <input
          value={q}
          onChange={(event) => setQ(event.target.value)}
          className="input-field w-full max-w-xl rounded-lg px-3 py-2"
          placeholder="Search notes, passages, prompts..."
        />
        <button onClick={exportNotes} disabled={notes.length === 0} className="btn-secondary px-4 py-2 text-sm disabled:opacity-50">
          Export backup
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

      <div className="mt-6 space-y-4">
        {filtered.length === 0 ? (
          <section className="card p-5">
            <p className="soft">No notes yet. Save a reflection from a passage, learning step, or an Ask Pratibha response.</p>
          </section>
        ) : (
          filtered.map((note) => (
            <article key={note.id} className="card p-5">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="layer-heading">{new Date(note.updatedAt).toLocaleString()}</p>
                  <h2 className="mt-2 text-2xl text-amber-100">{note.passageTitle}</h2>
                  {note.kind === "chat_response" && note.question ? (
                    <p className="soft mt-2 text-sm">You asked: {note.question}</p>
                  ) : null}
                </div>
                <div className="flex gap-2">
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
              {note.prompt ? <p className="soft mt-3 text-sm">{note.prompt}</p> : null}
              <p className="mt-4 whitespace-pre-wrap leading-relaxed text-stone-200">{note.body}</p>
            </article>
          ))
        )}
      </div>
    </main>
  );
}
