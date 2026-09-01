"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../../convex/_generated/api";
import { useAuth } from "@/components/AuthProvider";
import { useT } from "@/components/LocaleProvider";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { recordPractice } from "@/lib/glyphUnlock";
import { ManuscriptFolio } from "@/components/ManuscriptFolio";

export default function ManuscriptPage() {
  const t = useT();
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
        <p className="passage-reading__meta">{t("manuscript.meta")}</p>
        <h1 className="passage-reading__title">{t("manuscript.title")}</h1>
        <p className="soft mt-4">{t("manuscript.signInLede")}</p>
        <Link href="/login?next=/manuscript" className="mt-6 inline-block text-amber-100 underline">
          {t("auth.signIn")}
        </Link>
      </main>
    );
  }

  return <ManuscriptEditor />;
}

function ManuscriptEditor() {
  const t = useT();
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
      recordPractice("manuscript:save");
      if (visibility === "public") {
        recordPractice("manuscript:share");
        setShareHint(t("manuscript.sharePublic"));
      }
      if (visibility === "private") setShareHint(t("manuscript.sharePrivate"));
    } catch (err) {
      setError(err instanceof Error ? err.message : t("manuscript.updateFailed"));
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
        <p className="passage-reading__meta">{t("manuscript.title")}</p>
        <h1 className="passage-reading__title">{title || t("manuscript.defaultTitle")}</h1>
        <p className="passage-reading__deck">{t("manuscript.deck")}</p>
      </header>

      <section className="space-y-4">
        <div>
          <label className="soft mb-1 block font-sans text-xs uppercase tracking-[0.16em]">{t("common.title")}</label>
          <Input value={title} onChange={(e) => setTitle(e.target.value)} placeholder={t("manuscript.titlePlaceholder")} />
        </div>
        <div>
          <label className="soft mb-1 block font-sans text-xs uppercase tracking-[0.16em]">{t("manuscript.yourName")}</label>
          <Input
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            placeholder={t("manuscript.namePlaceholder")}
            maxLength={40}
          />
        </div>
        <div className="passage-endmatter__actions">
          <Button type="button" size="sm" onClick={() => void saveSettings()}>
            {t("common.save")}
          </Button>
          <Button
            type="button"
            size="sm"
            variant="secondary"
            onClick={() => void saveSettings(manuscript?.visibility === "public" ? "private" : "public")}
          >
            {manuscript?.visibility === "public" ? t("manuscript.makePrivate") : t("manuscript.makePublic")}
          </Button>
        </div>
        {shareHint ? <p className="soft text-sm">{shareHint}</p> : null}
        {error ? <p className="text-sm text-red-300">{error}</p> : null}
        {manuscript?.visibility === "public" && shareUrl ? (
          <p className="soft text-sm">
            {t("manuscript.share")}:{" "}
            <Link href={`/m/${manuscript.slug}`} className="text-amber-100 underline decoration-amber-200/30">
              {shareUrl}
            </Link>
          </p>
        ) : null}
      </section>

      <section className="mt-12">
        <h2 className="passage-layer__label">
          {t("manuscript.verses")}
          {manuscript?.entries.length ? ` · ${manuscript.entries.length}` : ""}
        </h2>
        {!manuscript || manuscript.entries.length === 0 ? (
          <p className="soft mt-4 text-sm leading-relaxed">
            {t("manuscript.empty")}
          </p>
        ) : (
          <div className="manuscript-grid">
            {manuscript.entries.map((entry, index) => (
              <ManuscriptFolio
                key={entry.verseId}
                verseId={entry.verseId}
                verseTitle={entry.verseTitle}
                card={{
                  mark: entry.mark,
                  ink: entry.ink,
                  textMode: entry.textMode,
                  line: entry.line,
                  aspectRatio: entry.aspectRatio,
                  holographic: entry.holographic,
                  reading: entry.reading,
                }}
                actions={
                  <>
                    <Textarea
                      value={notes[entry.verseId] ?? ""}
                      onChange={(e) =>
                        setNotes((prev) => ({ ...prev, [entry.verseId]: e.target.value }))
                      }
                      onBlur={() => {
                        const next = notes[entry.verseId] ?? "";
                        if (next !== (entry.note || "")) {
                          void setEntryNote({ verseId: entry.verseId, note: next })
                            .then(() => recordPractice(`manuscript:note:${entry.verseId}`))
                            .catch((err) =>
                              setError(err instanceof Error ? err.message : t("manuscript.noteFailed")),
                            );
                        }
                      }}
                      placeholder={t("manuscript.notePlaceholder")}
                      rows={2}
                    />
                    <div className="flex flex-wrap gap-2">
                      <Button
                        type="button"
                        size="sm"
                        variant="ghost"
                        disabled={index === 0}
                        onClick={() => void moveVerse({ verseId: entry.verseId, direction: "up" })}
                      >
                        {t("common.up")}
                      </Button>
                      <Button
                        type="button"
                        size="sm"
                        variant="ghost"
                        disabled={index === manuscript.entries.length - 1}
                        onClick={() => void moveVerse({ verseId: entry.verseId, direction: "down" })}
                      >
                        {t("common.down")}
                      </Button>
                      <Button
                        type="button"
                        size="sm"
                        variant="ghost"
                        onClick={() => void removeVerse({ verseId: entry.verseId })}
                      >
                        {t("common.remove")}
                      </Button>
                    </div>
                  </>
                }
              />
            ))}
          </div>
        )}
      </section>
    </main>
  );
}
