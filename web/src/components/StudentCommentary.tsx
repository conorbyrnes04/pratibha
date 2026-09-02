"use client";

import { useState } from "react";
import Link from "next/link";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import { useAuth } from "@/components/AuthProvider";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { Button } from "@/components/ui/button";
import { CircleOfferForm } from "@/components/CircleOfferForm";
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
  const inManuscript = useQuery(api.manuscripts.hasVerse, user ? { verseId } : "skip");
  const addVerse = useMutation(api.manuscripts.addVerse);
  const removeVerse = useMutation(api.manuscripts.removeVerse);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

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

  async function removeFromManuscript() {
    setBusy(true);
    setError("");
    try {
      await removeVerse({ verseId });
    } catch (err) {
      setError(err instanceof Error ? err.message : t("commentary.msFailed"));
    } finally {
      setBusy(false);
    }
  }

  function saveToManuscript() {
    if (onKeepFolio) {
      onKeepFolio();
      return;
    }
    setBusy(true);
    setError("");
    void addVerse({ verseId, verseTitle })
      .then(() => recordPractice(`manuscript:${verseId}`))
      .catch((err) => setError(err instanceof Error ? err.message : t("commentary.msFailed")))
      .finally(() => setBusy(false));
  }

  return (
    <section id="commentary" className="passage-commentary">
      <h2 className="passage-layer__label">{t("commentary.title")}</h2>
      <p className="soft mt-2 text-sm leading-relaxed">{t("commentary.lede")}</p>
      <CircleOfferForm verseId={verseId} verseTitle={verseTitle} />
      {error ? <p className="mt-3 text-sm text-red-300">{error}</p> : null}
      <div className="passage-endmatter__actions mt-3">
        {inManuscript ? (
          <>
            <Button type="button" size="sm" variant="secondary" disabled={busy} onClick={saveToManuscript}>
              {t("commentary.editCard")}
            </Button>
            <Button type="button" size="sm" variant="ghost" disabled={busy} onClick={() => void removeFromManuscript()}>
              {busy ? "…" : t("commentary.removeMs")}
            </Button>
          </>
        ) : (
          <Button type="button" size="sm" variant="secondary" disabled={busy} onClick={saveToManuscript}>
            {busy ? "…" : t("commentary.saveMs")}
          </Button>
        )}
      </div>
    </section>
  );
}
