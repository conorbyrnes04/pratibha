'use client';

import { useEffect, useState } from "react";
import type { JournalNote, VerseItem } from "@/lib/types";
import { deleteJournalNote, notesForPassage, upsertJournalNote } from "@/lib/journalStorage";
import { practiceText } from "@/lib/verseLayers";

type JournalPanelProps =
  | {
      passage: VerseItem;
      prompt?: string;
    }
  | {
      contextId: string;
      contextTitle: string;
      prompt: string;
    };

function storageKey(props: JournalPanelProps): string {
  return "passage" in props ? props.passage._id : props.contextId;
}

function defaultPrompt(props: JournalPanelProps): string {
  if ("prompt" in props && props.prompt) return props.prompt;
  if ("passage" in props) {
    return practiceText(props.passage) || "What changes if this passage becomes an instruction for today?";
  }
  return props.prompt;
}

export function JournalPanel(props: JournalPanelProps) {
  const key = storageKey(props);
  const prompt = defaultPrompt(props);
  const [notes, setNotes] = useState<JournalNote[]>([]);
  const [body, setBody] = useState("");

  function refresh() {
    setNotes(notesForPassage(key));
  }

  useEffect(() => {
    refresh();
    setBody("");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [key]);

  function save() {
    const clean = body.trim();
    if (!clean) return;
    if ("passage" in props) {
      upsertJournalNote({ passage: props.passage, body: clean, prompt });
    } else {
      upsertJournalNote({
        contextId: props.contextId,
        contextTitle: props.contextTitle,
        body: clean,
        prompt,
      });
    }
    setBody("");
    refresh();
  }

  function remove(id: string) {
    deleteJournalNote(id);
    refresh();
  }

  return (
    <section className="card p-4">
      <p className="layer-heading">Journal</p>
      <p className="soft mt-2 text-sm leading-relaxed">{prompt}</p>
      <textarea
        value={body}
        onChange={(event) => setBody(event.target.value)}
        rows={4}
        className="input-field mt-3 w-full rounded-2xl p-3 text-sm"
        placeholder="Write a note, question, or practice observation..."
      />
      <button onClick={save} disabled={!body.trim()} className="btn-primary mt-3 px-4 py-2 text-sm disabled:opacity-50">
        Save note
      </button>
      <div className="mt-4 space-y-3">
        {notes.length === 0 ? (
          <p className="soft text-sm">No notes for this step yet.</p>
        ) : (
          notes.slice(0, 3).map((note) => (
            <article key={note.id} className="citation-card p-3">
              <p className="soft text-xs">{new Date(note.updatedAt).toLocaleString()}</p>
              <p className="mt-2 whitespace-pre-wrap text-sm leading-relaxed text-stone-200">{note.body}</p>
              <button onClick={() => remove(note.id)} className="mt-2 font-sans text-xs text-amber-100 hover:underline">
                Delete
              </button>
            </article>
          ))
        )}
      </div>
    </section>
  );
}
