"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import { useAuth } from "@/components/AuthProvider";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { recordPractice } from "@/lib/glyphUnlock";
import { buttonVariants } from "@/components/ui/button";
import { useT } from "@/components/LocaleProvider";

export function StudentCommentary({
  verseId,
  verseTitle,
  onKeepFolio,
}: {
  verseId: string;
  verseTitle: string;
  onKeepFolio?: () => void;
}) {
  if (!CONVEX_ENABLED) return null;
  return <StudentCommentaryInner verseId={verseId} verseTitle={verseTitle} onKeepFolio={onKeepFolio} />;
}

function StudentCommentaryInner({
  verseId,
  verseTitle,
  onKeepFolio,
}: {
  verseId: string;
  verseTitle: string;
  onKeepFolio?: () => void;
}) {
  const t = useT();
  const { user, loading } = useAuth();
  const mine = useQuery(api.studentCommentaries.getMine, user ? { verseId } : "skip");
  const profile = useQuery(api.profiles.getMine, user ? {} : "skip");
  const inManuscript = useQuery(api.manuscripts.hasVerse, user ? { verseId } : "skip");
  const upsert = useMutation(api.studentCommentaries.upsert);
  const withdraw = useMutation(api.studentCommentaries.withdraw);
  const addVerse = useMutation(api.manuscripts.addVerse);
  const removeVerse = useMutation(api.manuscripts.removeVerse);

  const [body, setBody] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState<"save" | "offer" | "ms" | null>(null);

  useEffect(() => {
    setBody(mine?.body ?? "");
    setError("");
  }, [verseId, mine?.body]);

  useEffect(() => {
    if (profile?.displayName) setDisplayName(profile.displayName);
  }, [profile?.displayName]);

  if (loading) return null;

  if (!user) {
    return (
      <section id="commentary" className="passage-commentary">
        <h2 className="passage-layer__label">{t("commentary.title")}</h2>
        <p className="soft mt-3 text-sm leading-relaxed">{t("commentary.signInLede")}</p>
        <Link href={`/login?next=/read/${encodeURIComponent(verseId)}`} className={`${buttonVariants({ size: "sm" })} mt-4`}>
          {t("auth.signIn")}
        </Link>
      </section>
    );
  }

  async function save(status: "private" | "offered") {
    setBusy(status === "offered" ? "offer" : "save");
    setError("");
    try {
      await upsert({
        verseId,
        verseTitle,
        body,
        status,
        displayName: displayName.trim() || undefined,
      });
      recordPractice(`commentary:${verseId}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("commentary.saveFailed"));
    } finally {
      setBusy(null);
    }
  }

  async function removeFromManuscript() {
    setBusy("ms");
    setError("");
    try {
      await removeVerse({ verseId });
    } catch (err) {
      setError(err instanceof Error ? err.message : t("commentary.msFailed"));
    } finally {
      setBusy(null);
    }
  }

  function saveToManuscript() {
    if (onKeepFolio) {
      onKeepFolio();
      return;
    }
    setBusy("ms");
    setError("");
    void addVerse({ verseId, verseTitle })
      .then(() => recordPractice(`manuscript:${verseId}`))
      .catch((err) => setError(err instanceof Error ? err.message : t("commentary.msFailed")))
      .finally(() => setBusy(null));
  }

  const offered = mine?.status === "offered";

  return (
    <section id="commentary" className="passage-commentary">
      <h2 className="passage-layer__label">{t("commentary.title")}</h2>
      <p className="soft mt-2 text-sm leading-relaxed">
        {t("commentary.lede")}
        {offered ? ` ${t("commentary.offered")}` : mine ? ` ${t("commentary.savedPrivate")}` : ""}
      </p>
      <Textarea
        className="mt-4"
        value={body}
        onChange={(e) => setBody(e.target.value)}
        placeholder={t("commentary.placeholder")}
        rows={6}
      />
      {!profile?.displayName || offered ? (
        <div className="mt-3">
          <label className="soft mb-1 block font-sans text-xs uppercase tracking-[0.16em]">
            {t("commentary.nameLabel")}
          </label>
          <Input
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            placeholder={t("commentary.namePlaceholder")}
            maxLength={40}
          />
        </div>
      ) : null}
      {error ? <p className="mt-3 text-sm text-red-300">{error}</p> : null}
      <div className="passage-endmatter__actions mt-4">
        <Button type="button" size="sm" disabled={!body.trim() || busy !== null} onClick={() => void save("private")}>
          {busy === "save" ? t("common.saving") : t("commentary.savePrivate")}
        </Button>
        <Button
          type="button"
          size="sm"
          variant="secondary"
          disabled={!body.trim() || busy !== null}
          onClick={() => void save("offered")}
        >
          {busy === "offer" ? t("commentary.offering") : offered ? t("commentary.updateOffered") : t("commentary.offer")}
        </Button>
        {offered ? (
          <Button
            type="button"
            size="sm"
            variant="ghost"
            disabled={busy !== null}
            onClick={() => {
              setBusy("save");
              void withdraw({ verseId })
                .catch((err) => setError(err instanceof Error ? err.message : t("commentary.withdrawFailed")))
                .finally(() => setBusy(null));
            }}
          >
            {t("commentary.withdraw")}
          </Button>
        ) : null}
        {inManuscript ? (
          <>
            <Button type="button" size="sm" variant="secondary" disabled={busy !== null} onClick={saveToManuscript}>
              {t("commentary.editCard")}
            </Button>
            <Button type="button" size="sm" variant="ghost" disabled={busy !== null} onClick={() => void removeFromManuscript()}>
              {busy === "ms" ? "…" : t("commentary.removeMs")}
            </Button>
          </>
        ) : (
          <Button type="button" size="sm" variant="secondary" disabled={busy !== null} onClick={saveToManuscript}>
            {busy === "ms" ? "…" : t("commentary.saveMs")}
          </Button>
        )}
      </div>
    </section>
  );
}
