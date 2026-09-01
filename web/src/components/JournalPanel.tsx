'use client';

import { useEffect, useState } from "react";
import type { JournalNote, VerseItem } from "@/lib/types";
import { useAuth } from "@/components/AuthProvider";
import { usePushJournalNote, useDeleteJournalNote } from "@/lib/journalCloud";
import { recordPractice } from "@/lib/glyphUnlock";
import { deleteJournalNote, notesForPassage, upsertJournalNote } from "@/lib/journalStorage";
import { practiceText } from "@/lib/verseLayers";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { useLocale } from "@/components/LocaleProvider";

type JournalPanelProps =
  | {
      passage: VerseItem;
      prompt?: string;
      /** Omit card chrome (e.g. inside a Sheet). */
      bare?: boolean;
    }
  | {
      contextId: string;
      contextTitle: string;
      prompt: string;
      bare?: boolean;
    };

function storageKey(props: JournalPanelProps): string {
  return "passage" in props ? props.passage._id : props.contextId;
}

function defaultPrompt(props: JournalPanelProps, fallback: string): string {
  if ("prompt" in props && props.prompt) return props.prompt;
  if ("passage" in props) {
    return practiceText(props.passage) || fallback;
  }
  return props.prompt;
}

export function JournalPanel(props: JournalPanelProps) {
  const { t, bcp47 } = useLocale();
  const { user } = useAuth();
  const pushNote = usePushJournalNote();
  const deleteRemote = useDeleteJournalNote();
  const key = storageKey(props);
  const prompt = defaultPrompt(props, t("journal.defaultPrompt"));
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
    const note =
      "passage" in props
        ? upsertJournalNote({ passage: props.passage, body: clean, prompt })
        : upsertJournalNote({
            contextId: props.contextId,
            contextTitle: props.contextTitle,
            body: clean,
            prompt,
          });
    if (user) void pushNote(note);
    recordPractice(`journal:${key}`);
    setBody("");
    refresh();
  }

  function remove(id: string) {
    deleteJournalNote(id);
    if (user) void deleteRemote(id);
    refresh();
  }

  const bare = Boolean(props.bare);

  return (
    <section className={bare ? undefined : "card p-4"}>
      {bare ? null : <p className="layer-heading">{t("journal.panelTitle")}</p>}
      <p className={`soft text-sm leading-relaxed ${bare ? "" : "mt-2"}`}>{prompt}</p>
      <Textarea
        value={body}
        onChange={(event) => setBody(event.target.value)}
        rows={4}
        className="mt-3 w-full rounded-2xl text-sm"
        placeholder={t("journal.placeholder")}
      />
      <Button onClick={save} disabled={!body.trim()} size="sm" className="mt-3">
        {t("journal.saveNote")}
      </Button>
      <div className="mt-4 space-y-3">
        {notes.length === 0 ? (
          <p className="soft text-sm">{t("journal.emptyPassage")}</p>
        ) : (
          notes.slice(0, 3).map((note) => (
            <article key={note.id} className="citation-card p-3">
              <p className="soft text-xs">{new Date(note.updatedAt).toLocaleString(bcp47)}</p>
              <p className="mt-2 whitespace-pre-wrap text-sm leading-relaxed text-stone-200">{note.body}</p>
              <button onClick={() => remove(note.id)} className="mt-2 font-sans text-xs text-amber-100 hover:underline">
                {t("common.delete")}
              </button>
            </article>
          ))
        )}
      </div>
    </section>
  );
}
