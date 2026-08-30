"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../../convex/_generated/api";
import { useAuth } from "@/components/AuthProvider";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

export default function ManuscriptPage() {
  const { user, loading } = useAuth();

  if (!CONVEX_ENABLED) {
    return (
      <main className="page-shell page-shell--reading">
        <p className="soft">Manuscripts need Convex auth configured.</p>
      </main>
    );
  }

  if (loading) {
    return (
      <main className="page-shell page-shell--reading">
        <p className="soft">Opening your manuscript…</p>
      </main>
    );
  }

  if (!user) {
    return (
      <main className="page-shell page-shell--reading">
        <p className="passage-reading__meta">Manuscript</p>
        <h1 className="passage-reading__title">Your manuscript</h1>
        <p className="soft mt-4">Sign in to gather verses into a small book you can share.</p>
        <Link href="/login?next=/manuscript" className="mt-6 inline-block text-amber-100 underline">
          Sign in
        </Link>
      </main>
    );
  }

  return <ManuscriptEditor />;
}

function ManuscriptEditor() {
  const manuscript = useQuery(api.manuscripts.getMine);
  const profile = useQuery(api.profiles.getMine);
  const removeVerse = useMutation(api.manuscripts.removeVerse);
  const moveVerse = useMutation(api.manuscripts.moveVerse);
  const setEntryNote = useMutation(api.manuscripts.setEntryNote);
  const updateSettings = useMutation(api.manuscripts.updateSettings);

  const [title, setTitle] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [notes, setNotes] = useState<Record<string, string>>({});
  const [error, setError] = useState("");
  const [shareHint, setShareHint] = useState("");

  useEffect(() => {
    if (manuscript) {
      setTitle(manuscript.title);
      setDisplayName(manuscript.displayName === "Student" ? "" : manuscript.displayName);
    } else if (profile?.displayName) {
      setDisplayName(profile.displayName);
    }
  }, [manuscript, profile?.displayName]);

  useEffect(() => {
    if (!manuscript) return;
    const next: Record<string, string> = {};
    for (const entry of manuscript.entries) next[entry.verseId] = entry.note;
    setNotes(next);
  }, [manuscript]);

  async function saveSettings(visibility?: "private" | "public") {
    setError("");
    try {
      await updateSettings({
        title: title.trim() || undefined,
        displayName: displayName.trim() || undefined,
        visibility,
      });
      if (visibility === "public") setShareHint("Public. Anyone with the link can read it.");
      if (visibility === "private") setShareHint("Private again.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not update.");
    }
  }

  const shareUrl =
    manuscript && typeof window !== "undefined"
      ? `${window.location.origin}/m/${manuscript.slug}`
      : manuscript
        ? `/m/${manuscript.slug}`
        : "";

  return (
    <main className="page-shell page-shell--reading">
      <header className="passage-reading__header">
        <p className="passage-reading__meta">Your manuscript</p>
        <h1 className="passage-reading__title">{title || "A small book of verses"}</h1>
        <p className="passage-reading__deck">
          Twelve to forty passages you actually sit with. Private until you share the link.
        </p>
      </header>

      <section className="space-y-4">
        <div>
          <label className="soft mb-1 block font-sans text-xs uppercase tracking-[0.16em]">Title</label>
          <Input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="A name for this chapbook" />
        </div>
        <div>
          <label className="soft mb-1 block font-sans text-xs uppercase tracking-[0.16em]">Your name</label>
          <Input
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            placeholder="How you are known on a shared manuscript"
            maxLength={40}
          />
        </div>
        <div className="passage-endmatter__actions">
          <Button type="button" size="sm" onClick={() => void saveSettings()}>
            Save
          </Button>
          <Button
            type="button"
            size="sm"
            variant="secondary"
            onClick={() => void saveSettings(manuscript?.visibility === "public" ? "private" : "public")}
          >
            {manuscript?.visibility === "public" ? "Make private" : "Make public"}
          </Button>
        </div>
        {shareHint ? <p className="soft text-sm">{shareHint}</p> : null}
        {error ? <p className="text-sm text-red-300">{error}</p> : null}
        {manuscript?.visibility === "public" && shareUrl ? (
          <p className="soft text-sm">
            Share:{" "}
            <Link href={`/m/${manuscript.slug}`} className="text-amber-100 underline decoration-amber-200/30">
              {shareUrl}
            </Link>
          </p>
        ) : null}
      </section>

      <section className="mt-12">
        <h2 className="passage-layer__label">
          Verses
          {manuscript?.entries.length ? ` · ${manuscript.entries.length}` : ""}
        </h2>
        {!manuscript || manuscript.entries.length === 0 ? (
          <p className="soft mt-4 text-sm leading-relaxed">
            Nothing here yet. Open a passage and choose Add to manuscript.
          </p>
        ) : (
          <ol className="mt-6 space-y-8">
            {manuscript.entries.map((entry, index) => (
              <li key={entry.verseId}>
                <p className="font-sans text-xs uppercase tracking-[0.16em] text-stone-400">
                  {index + 1}
                </p>
                <Link
                  href={`/read/${encodeURIComponent(entry.verseId)}`}
                  className="mt-1 block text-lg text-amber-100"
                >
                  {entry.verseTitle}
                </Link>
                <Textarea
                  className="mt-3 min-h-16"
                  value={notes[entry.verseId] ?? ""}
                  onChange={(e) =>
                    setNotes((prev) => ({ ...prev, [entry.verseId]: e.target.value }))
                  }
                  onBlur={() => {
                    const next = notes[entry.verseId] ?? "";
                    if (next !== (entry.note || "")) {
                      void setEntryNote({ verseId: entry.verseId, note: next }).catch((err) =>
                        setError(err instanceof Error ? err.message : "Could not save the note."),
                      );
                    }
                  }}
                  placeholder="A one-line margin — optional"
                  rows={2}
                />
                <div className="mt-2 flex flex-wrap gap-2">
                  <Button
                    type="button"
                    size="sm"
                    variant="ghost"
                    disabled={index === 0}
                    onClick={() => void moveVerse({ verseId: entry.verseId, direction: "up" })}
                  >
                    Up
                  </Button>
                  <Button
                    type="button"
                    size="sm"
                    variant="ghost"
                    disabled={index === manuscript.entries.length - 1}
                    onClick={() => void moveVerse({ verseId: entry.verseId, direction: "down" })}
                  >
                    Down
                  </Button>
                  <Button
                    type="button"
                    size="sm"
                    variant="ghost"
                    onClick={() => void removeVerse({ verseId: entry.verseId })}
                  >
                    Remove
                  </Button>
                </div>
              </li>
            ))}
          </ol>
        )}
      </section>
    </main>
  );
}
