'use client';

import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import type { JournalNote } from "@/lib/types";
import { useAuth } from "@/components/AuthProvider";
import { useLocale, useT } from "@/components/LocaleProvider";
import { Button, buttonVariants } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import { useSyncJournal, useDeleteJournalNote } from "@/lib/journalCloud";
import { deleteJournalNote, journalSourceHref, loadJournalNotes, saveJournalNotes } from "@/lib/journalStorage";

export default function JournalPage() {
  const t = useT();
  const { bcp47 } = useLocale();
  const { user, loading: authLoading } = useAuth();
  const [notes, setNotes] = useState<JournalNote[]>([]);
  const [q, setQ] = useState("");
  const [expanded, setExpanded] = useState<Set<string>>(new Set());
  const [syncState, setSyncState] = useState<"idle" | "syncing" | "synced" | "local" | "error">("idle");
  const [syncError, setSyncError] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);
  const { sync, ready } = useSyncJournal();
  const deleteRemote = useDeleteJournalNote();

  // The sync closure changes identity when the remote query updates; keep the
  // latest in a ref so the driver effect below doesn't need it as a dependency
  // (which would otherwise re-fire the sync on every render).
  const syncRef = useRef(sync);
  useEffect(() => {
    syncRef.current = sync;
  }, [sync]);

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
      setSyncError(null);
      return;
    }
    // Wait for the remote note list to load before attempting to reconcile.
    if (!ready) {
      setSyncState("syncing");
      setSyncError(null);
      return;
    }

    const MAX_ATTEMPTS = 5;
    let cancelled = false;
    let attempts = 0;
    let timer: ReturnType<typeof setTimeout> | null = null;

    setSyncState("syncing");
    setSyncError(null);

    // Single in-flight sync at a time; on failure retry with exponential
    // backoff + jitter, capped at MAX_ATTEMPTS, then surface one error banner.
    const run = async () => {
      if (cancelled) return;
      const result = await syncRef.current();
      if (cancelled) return;
      setNotes(result.notes.sort((a, b) => b.updatedAt.localeCompare(a.updatedAt)));

      if (result.status === "error") {
        attempts += 1;
        if (attempts >= MAX_ATTEMPTS) {
          setSyncState("error");
          setSyncError(result.error ?? null);
          return;
        }
        const backoff = Math.min(30000, 500 * 2 ** attempts) + Math.random() * 500;
        setSyncState("syncing");
        timer = setTimeout(run, backoff);
        return;
      }

      setSyncState(result.status);
      setSyncError(null);
    };

    void run();

    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    };
  }, [user, authLoading, ready]);

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
      alert(t("journal.importFailed"));
    }
  }

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase();
    if (!needle) return notes;
    return notes.filter((note) => [note.passageTitle, note.body, note.prompt, note.tags.join(" ")].join(" ").toLowerCase().includes(needle));
  }, [notes, q]);

  function remove(id: string) {
    deleteJournalNote(id);
    if (user) void deleteRemote(id);
    refresh();
  }

  function sourceLabel(note: JournalNote): string {
    if (note.kind === "chat_response") return t("journal.reopenChat");
    if (note.passageId.startsWith("learn:")) return t("journal.reopenStep");
    return t("journal.reopenPassage");
  }

  return (
    <main className="page-shell page-shell--reading">
      <header className="library-header">
        <div className="library-header__body">
          <p className="passage-reading__meta">{t("journal.meta")}</p>
          <h1 className="library-header__title">{t("journal.title")}</h1>
          <p className="library-header__lede">
            {user ? t("journal.ledeSignedIn") : t("journal.ledeSignedOut")}
          </p>
          {!user && !authLoading ? (
            <Link
              href="/login?next=/journal"
              className={cn(buttonVariants({ variant: "secondary" }), "mt-4")}
            >
              {t("common.signInToSync")}
            </Link>
          ) : null}
        </div>
      </header>

      <div className="mt-8 flex flex-wrap items-center gap-3">
        <Input
          value={q}
          onChange={(event) => setQ(event.target.value)}
          className="min-w-0 flex-1"
          placeholder={t("journal.searchPlaceholder")}
        />
        <div className="flex shrink-0 items-center gap-2">
          <Button variant="secondary" size="sm" onClick={exportNotes} disabled={notes.length === 0}>
            {t("common.export")}
          </Button>
          <Button variant="secondary" size="sm" onClick={() => fileRef.current?.click()}>
            {t("common.import")}
          </Button>
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
          ? t("journal.syncing")
          : syncState === "synced"
            ? t("journal.synced")
            : syncState === "error"
              ? t("journal.syncError", { detail: syncError ? ` (${syncError})` : "" })
              : t("journal.localOnly")}
      </p>

      <div className="mt-8 space-y-4">
        {filtered.length === 0 ? (
          <section className="card flex flex-col items-center gap-3 p-10 text-center">
            <p className="text-2xl text-amber-100">
              {notes.length === 0 ? t("journal.empty") : t("journal.noMatch")}
            </p>
            <p className="soft max-w-md">
              {notes.length === 0 ? t("journal.emptyLede") : t("journal.noMatchLede")}
            </p>
            {notes.length === 0 ? (
              <Link href="/read" className={cn(buttonVariants(), "mt-2")}>
                {t("journal.browseLibrary")}
              </Link>
            ) : null}
          </section>
        ) : (
          filtered.map((note) => (
            <article key={note.id} className="card p-5 sm:p-6">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div className="min-w-0">
                  <p className="layer-heading">{new Date(note.updatedAt).toLocaleString(bcp47)}</p>
                  <h2 className="mt-2 text-2xl text-amber-100">{note.passageTitle}</h2>
                  {note.kind === "chat_response" && note.question ? (
                    <p className="soft mt-2 text-sm">{t("journal.youAsked", { question: note.question })}</p>
                  ) : null}
                </div>
                <div className="flex shrink-0 gap-2">
                  {journalSourceHref(note) ? (
                    <Link
                      href={journalSourceHref(note)!}
                      className={cn(buttonVariants({ variant: "secondary", size: "sm" }))}
                    >
                      {sourceLabel(note)}
                    </Link>
                  ) : null}
                  <Button variant="secondary" size="sm" onClick={() => remove(note.id)}>
                    {t("common.delete")}
                  </Button>
                </div>
              </div>
              {note.prompt ? <p className="soft mt-4 text-sm">{note.prompt}</p> : null}
              {(() => {
                const isLong = note.body.length > 360;
                const open = expanded.has(note.id) || !isLong;
                return (
                  <>
                    <p
                      className={cn(
                        "mt-4 whitespace-pre-wrap leading-relaxed text-stone-200",
                        !open && "line-clamp-6",
                      )}
                    >
                      {note.body}
                    </p>
                    {isLong ? (
                      <button
                        type="button"
                        onClick={() =>
                          setExpanded((prev) => {
                            const next = new Set(prev);
                            if (next.has(note.id)) next.delete(note.id);
                            else next.add(note.id);
                            return next;
                          })
                        }
                        className="mt-2 font-sans text-xs text-amber-100 hover:underline"
                      >
                        {open ? t("common.showLess") : t("common.showMore")}
                      </button>
                    ) : null}
                  </>
                );
              })()}
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
