'use client';

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import type { JournalNote } from "@/lib/types";
import { deleteJournalNote, loadJournalNotes } from "@/lib/journalStorage";

export default function JournalPage() {
  const [notes, setNotes] = useState<JournalNote[]>([]);
  const [q, setQ] = useState("");

  function refresh() {
    setNotes(loadJournalNotes().sort((a, b) => b.updatedAt.localeCompare(a.updatedAt)));
  }

  useEffect(() => {
    refresh();
  }, []);

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase();
    if (!needle) return notes;
    return notes.filter((note) => [note.passageTitle, note.body, note.prompt, note.tags.join(" ")].join(" ").toLowerCase().includes(needle));
  }, [notes, q]);

  function remove(id: string) {
    deleteJournalNote(id);
    refresh();
  }

  function sourceHref(note: JournalNote): string | null {
    if (note.passageId.startsWith("learn:")) {
      const [, trackId, stepId] = note.passageId.split(":");
      if (!trackId || !stepId) return "/learn";
      return `/learn?track=${encodeURIComponent(trackId)}&step=${encodeURIComponent(stepId)}`;
    }
    return `/read/${encodeURIComponent(note.passageId)}`;
  }

  return (
    <main className="page-shell">
      <p className="eyebrow">Personal study memory</p>
      <h1 className="mt-3 text-5xl font-semibold leading-none tracking-[-0.04em] text-stone-100 sm:text-6xl">Journal</h1>
      <p className="soft mt-4 max-w-2xl text-xl leading-relaxed">Saved reflections stay local in this browser and remain linked to their source passages.</p>

      <input
        value={q}
        onChange={(event) => setQ(event.target.value)}
        className="input-field mt-6 w-full max-w-xl rounded-lg px-3 py-2"
        placeholder="Search notes, passages, prompts..."
      />

      <div className="mt-6 space-y-4">
        {filtered.length === 0 ? (
          <section className="card p-5">
            <p className="soft">No notes yet. Save a reflection from a learning path step or passage reader.</p>
          </section>
        ) : (
          filtered.map((note) => (
            <article key={note.id} className="card p-5">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <p className="layer-heading">{new Date(note.updatedAt).toLocaleString()}</p>
                  <h2 className="mt-2 text-2xl text-amber-100">{note.passageTitle}</h2>
                </div>
                <div className="flex gap-2">
                  {sourceHref(note) ? (
                    <Link href={sourceHref(note)!} className="btn-secondary px-4 py-2 text-sm">
                      {note.passageId.startsWith("learn:") ? "Reopen step" : "Reopen passage"}
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
