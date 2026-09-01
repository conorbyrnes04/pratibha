"use client";

import { useState } from "react";
import Link from "next/link";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import type { Id } from "../../convex/_generated/dataModel";
import { useAuth } from "@/components/AuthProvider";
import { CONVEX_ENABLED } from "@/lib/convexConfigured";
import { showCircle } from "@/lib/circleVerses";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { buttonVariants } from "@/components/ui/button";
import { useT } from "@/components/LocaleProvider";

export function CircleReadings({
  verseId,
  daily = false,
}: {
  verseId: string;
  daily?: boolean;
}) {
  if (!CONVEX_ENABLED) return null;
  return <CircleReadingsInner verseId={verseId} daily={daily} />;
}

function CircleReadingsInner({ verseId, daily }: { verseId: string; daily: boolean }) {
  const t = useT();
  const { user, loading } = useAuth();
  const meta = useQuery(api.studentCommentaries.circleMeta, { verseId });
  const offered = useQuery(
    api.studentCommentaries.listOffered,
    user ? { verseId } : "skip",
  );
  const visible = showCircle(verseId, meta?.offeredCount ?? 0, daily);
  if (!visible || meta === undefined) return null;

  const open = Boolean(meta.open || daily);
  const count = meta.offeredCount;

  return (
    <section className="passage-commentary">
      <h2 className="passage-layer__label">{open ? t("circle.title") : t("circle.otherReadings")}</h2>
      <p className="soft mt-2 text-sm leading-relaxed">
        {open ? t("circle.ledeOpen") : t("circle.ledeClosed")}
        {count ? ` · ${count}` : ""}
      </p>
      {loading ? null : !user ? (
        <p className="soft mt-4 text-sm">
          <Link href={`/login?next=/read/${encodeURIComponent(verseId)}`} className={buttonVariants({ size: "sm" })}>
            {t("circle.signIn")}
          </Link>
        </p>
      ) : offered === undefined ? (
        <p className="soft mt-4 text-sm">{t("circle.opening")}</p>
      ) : offered.length === 0 ? (
        <p className="soft mt-4 text-sm leading-relaxed">
          {t("circle.openEmpty")}{" "}
          <Link href={`#commentary`} className="text-amber-100 underline-offset-2 hover:underline">
            {t("circle.writeYours")}
          </Link>
          .
        </p>
      ) : (
        <ul className="mt-6 space-y-6">
          {offered.map((reading) => (
            <li key={reading._id}>
              <p className="font-sans text-xs uppercase tracking-[0.16em] text-amber-100/80">
                {reading.displayName}
              </p>
              <p className="reading-prose mt-2 text-[0.95rem] leading-relaxed">{reading.body}</p>
              <ReplyThread commentaryId={reading._id} />
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

function ReplyThread({ commentaryId }: { commentaryId: Id<"student_commentaries"> }) {
  const t = useT();
  const replies = useQuery(api.circleReplies.list, { commentaryId });
  const post = useMutation(api.circleReplies.post);
  const [open, setOpen] = useState(false);
  const [body, setBody] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const already = replies?.some((r) => r.mine);

  async function submit() {
    setBusy(true);
    setError("");
    try {
      await post({ commentaryId, body });
      setBody("");
      setOpen(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : t("circle.replyFailed"));
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="mt-3">
      {replies && replies.length > 0 ? (
        <ul className="space-y-3 border-l border-amber-200/15 pl-4">
          {replies.map((reply) => (
            <li key={reply._id}>
              <p className="font-sans text-[11px] uppercase tracking-[0.14em] text-stone-400">
                {reply.displayName}
              </p>
              <p className="soft mt-1 text-sm leading-relaxed">{reply.body}</p>
            </li>
          ))}
        </ul>
      ) : null}
      {already ? (
        <p className="soft mt-2 text-xs">{t("circle.youReplied")}</p>
      ) : (
        <>
          {!open ? (
            <button
              type="button"
              className="mt-2 font-sans text-xs uppercase tracking-[0.16em] text-amber-200/70 hover:text-amber-100"
              onClick={() => setOpen(true)}
            >
              {t("circle.reply")}
            </button>
          ) : (
            <div className="mt-3 space-y-2">
              <Textarea
                value={body}
                onChange={(e) => setBody(e.target.value)}
                placeholder={t("circle.replyPlaceholder")}
                rows={3}
              />
              {error ? <p className="text-sm text-red-300">{error}</p> : null}
              <div className="flex gap-2">
                <Button type="button" size="sm" disabled={!body.trim() || busy} onClick={() => void submit()}>
                  {busy ? t("common.sending") : t("circle.postReply")}
                </Button>
                <Button type="button" size="sm" variant="ghost" onClick={() => setOpen(false)}>
                  {t("common.cancel")}
                </Button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
