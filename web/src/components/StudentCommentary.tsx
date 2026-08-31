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

export function StudentCommentary({
  verseId,
  verseTitle,
}: {
  verseId: string;
  verseTitle: string;
}) {
  if (!CONVEX_ENABLED) return null;
  return <StudentCommentaryInner verseId={verseId} verseTitle={verseTitle} />;
}

function StudentCommentaryInner({
  verseId,
  verseTitle,
}: {
  verseId: string;
  verseTitle: string;
}) {
  const { user } = useAuth();
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

  if (!user) {
    return (
      <section className="passage-commentary">
        <h2 className="passage-layer__label">Your commentary</h2>
        <p className="soft mt-3 text-sm leading-relaxed">
          Sign in to write your own reading of this verse — private first, then offer it
          to the circle if it has sat with you.
        </p>
        <Link href={`/login?next=/read/${encodeURIComponent(verseId)}`} className={`${buttonVariants({ size: "sm" })} mt-4`}>
          Sign in
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
      setError(err instanceof Error ? err.message : "Could not save.");
    } finally {
      setBusy(null);
    }
  }

  async function toggleManuscript() {
    setBusy("ms");
    setError("");
    try {
      if (inManuscript) await removeVerse({ verseId });
      else {
        await addVerse({ verseId, verseTitle });
        recordPractice(`manuscript:${verseId}`);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not update the manuscript.");
    } finally {
      setBusy(null);
    }
  }

  const offered = mine?.status === "offered";

  return (
    <section className="passage-commentary">
      <h2 className="passage-layer__label">Your commentary</h2>
      <p className="soft mt-2 text-sm leading-relaxed">
        Say what the line does. This stays private until you offer it.
        {offered ? " Offered to the circle." : mine ? " Saved privately." : ""}
      </p>
      <Textarea
        className="mt-4"
        value={body}
        onChange={(e) => setBody(e.target.value)}
        placeholder="What does this verse ask of you?"
        rows={6}
      />
      {!profile?.displayName || offered ? (
        <div className="mt-3">
          <label className="soft mb-1 block font-sans text-xs uppercase tracking-[0.16em]">
            Name on offered readings
          </label>
          <Input
            value={displayName}
            onChange={(e) => setDisplayName(e.target.value)}
            placeholder="How you are known in the circle"
            maxLength={40}
          />
        </div>
      ) : null}
      {error ? <p className="mt-3 text-sm text-red-300">{error}</p> : null}
      <div className="passage-endmatter__actions mt-4">
        <Button type="button" size="sm" disabled={!body.trim() || busy !== null} onClick={() => void save("private")}>
          {busy === "save" ? "Saving…" : "Save privately"}
        </Button>
        <Button
          type="button"
          size="sm"
          variant="secondary"
          disabled={!body.trim() || busy !== null}
          onClick={() => void save("offered")}
        >
          {busy === "offer" ? "Offering…" : offered ? "Update offered reading" : "Offer to this verse"}
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
                .catch((err) => setError(err instanceof Error ? err.message : "Could not withdraw."))
                .finally(() => setBusy(null));
            }}
          >
            Withdraw
          </Button>
        ) : null}
        <Button type="button" size="sm" variant="ghost" disabled={busy !== null} onClick={() => void toggleManuscript()}>
          {busy === "ms"
            ? "…"
            : inManuscript
              ? "Remove from manuscript"
              : "Add to manuscript"}
        </Button>
      </div>
    </section>
  );
}
