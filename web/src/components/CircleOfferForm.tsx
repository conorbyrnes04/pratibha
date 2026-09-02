"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import { useAuth } from "@/components/AuthProvider";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { buttonVariants } from "@/components/ui/button";
import { recordPractice } from "@/lib/glyphUnlock";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { useT } from "@/components/LocaleProvider";

export function CircleOfferForm({
  verseId,
  verseTitle,
  compact = false,
  onOffered,
  loginNext,
}: {
  verseId: string;
  verseTitle: string;
  compact?: boolean;
  onOffered?: () => void;
  loginNext?: string;
}) {
  if (!CONVEX_ENABLED) return null;
  return (
    <CircleOfferFormInner
      verseId={verseId}
      verseTitle={verseTitle}
      compact={compact}
      onOffered={onOffered}
      loginNext={loginNext}
    />
  );
}

function CircleOfferFormInner({
  verseId,
  verseTitle,
  compact = false,
  onOffered,
  loginNext,
}: {
  verseId: string;
  verseTitle: string;
  compact?: boolean;
  onOffered?: () => void;
  loginNext?: string;
}) {
  const t = useT();
  const { user, loading } = useAuth();
  const mine = useQuery(api.studentCommentaries.getMine, user ? { verseId } : "skip");
  const profile = useQuery(api.profiles.getMine, user ? {} : "skip");
  const upsert = useMutation(api.studentCommentaries.upsert);
  const [body, setBody] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState<"save" | "offer" | null>(null);
  const next = loginNext ?? `/read/${encodeURIComponent(verseId)}#commentary`;

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
      <p className="soft mt-3 text-sm">
        <Link href={`/login?next=${encodeURIComponent(next)}`} className={buttonVariants({ size: "sm" })}>
          {t("circle.signInToJoin")}
        </Link>
      </p>
    );
  }

  const offered = mine?.status === "offered";
  const needsName = !profile?.displayName || offered;

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
      if (status === "offered") onOffered?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : t("commentary.saveFailed"));
    } finally {
      setBusy(null);
    }
  }

  return (
    <div>
      {offered ? <p className="soft mb-2 text-sm">{t("commentary.offered")}</p> : null}
      <Textarea
        className={compact ? "mt-2" : "mt-3"}
        value={body}
        onChange={(e) => setBody(e.target.value)}
        placeholder={t("circle.composePlaceholder")}
        rows={compact ? 4 : 6}
      />
      {needsName ? (
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
        <Button
          type="button"
          size="sm"
          disabled={!body.trim() || busy !== null}
          onClick={() => void save("offered")}
        >
          {busy === "offer" ? t("commentary.offering") : offered ? t("commentary.updateOffered") : t("commentary.offer")}
        </Button>
        <Button
          type="button"
          size="sm"
          variant="ghost"
          disabled={!body.trim() || busy !== null}
          onClick={() => void save("private")}
        >
          {busy === "save" ? t("common.saving") : t("commentary.savePrivate")}
        </Button>
      </div>
    </div>
  );
}
