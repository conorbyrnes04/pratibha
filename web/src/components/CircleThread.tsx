"use client";

import { useMemo, useState } from "react";
import Link from "next/link";
import { useMutation, useQuery } from "convex/react";
import { api } from "../../convex/_generated/api";
import type { Id } from "../../convex/_generated/dataModel";
import { useAuth } from "@/components/AuthProvider";
import { useLocale, useT } from "@/components/LocaleProvider";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { buttonVariants } from "@/components/ui/button";
import { formatCircleTime } from "@/lib/circleVerses";

export type CircleReplyRow = {
  _id: Id<"circle_replies">;
  displayName: string;
  body: string;
  createdAt: number;
  parentReplyId: Id<"circle_replies"> | null;
  mine: boolean;
};

type NestedReply = CircleReplyRow & { children: NestedReply[] };

function nestReplies(rows: CircleReplyRow[]): NestedReply[] {
  const byId = new Map<string, NestedReply>();
  for (const row of rows) {
    byId.set(row._id, { ...row, children: [] });
  }
  const roots: NestedReply[] = [];
  for (const row of byId.values()) {
    const parent = row.parentReplyId ? byId.get(row.parentReplyId) : undefined;
    if (parent) parent.children.push(row);
    else roots.push(row);
  }
  return roots;
}

export function CircleThread({
  commentaryId,
  verseId,
  compact = false,
  showGuestPrompt = true,
  loginNext,
}: {
  commentaryId: Id<"student_commentaries">;
  verseId: string;
  compact?: boolean;
  showGuestPrompt?: boolean;
  loginNext?: string;
}) {
  const { user, loading } = useAuth();
  const replies = useQuery(api.circleReplies.list, { commentaryId });
  const nested = useMemo(() => nestReplies(replies ?? []), [replies]);
  const canWrite = Boolean(user);

  return (
    <div className={compact ? "mt-3" : "mt-6"}>
      {replies === undefined ? null : nested.length > 0 ? (
        <ul className="space-y-4">
          {nested.map((reply) => (
            <ReplyItem
              key={reply._id}
              reply={reply}
              commentaryId={commentaryId}
              depth={0}
              canWrite={canWrite}
            />
          ))}
        </ul>
      ) : null}
      {loading ? null : canWrite ? (
        <ReplyComposer commentaryId={commentaryId} compact={compact} />
      ) : showGuestPrompt ? (
        <GuestReplyPrompt verseId={verseId} loginNext={loginNext} />
      ) : null}
    </div>
  );
}

function GuestReplyPrompt({ verseId, loginNext }: { verseId: string; loginNext?: string }) {
  const t = useT();
  const next = loginNext ?? `/read/${encodeURIComponent(verseId)}#circle`;
  return (
    <p className="soft mt-3 text-sm">
      <Link href={`/login?next=${encodeURIComponent(next)}`} className={buttonVariants({ size: "sm" })}>
        {t("circle.signInToReply")}
      </Link>
    </p>
  );
}

function ReplyItem({
  reply,
  commentaryId,
  depth,
  canWrite,
}: {
  reply: NestedReply;
  commentaryId: Id<"student_commentaries">;
  depth: number;
  canWrite: boolean;
}) {
  const t = useT();
  const { bcp47 } = useLocale();
  const [open, setOpen] = useState(false);

  return (
    <li className={depth > 0 ? "circle-reply circle-reply--nested" : "circle-reply"}>
      <p className="font-sans text-[11px] uppercase tracking-[0.14em] text-stone-400">
        {reply.mine ? t("common.you") : reply.displayName}
        <span className="ms-2 font-normal normal-case tracking-normal text-stone-500">
          {formatCircleTime(reply.createdAt, bcp47)}
        </span>
      </p>
      <p className="soft mt-1 whitespace-pre-wrap text-sm leading-relaxed">{reply.body}</p>
      {depth === 0 && canWrite ? (
        open ? (
          <ReplyComposer
            commentaryId={commentaryId}
            parentReplyId={reply._id}
            onDone={() => setOpen(false)}
            compact
            autoFocus
          />
        ) : (
          <button
            type="button"
            className="mt-2 font-sans text-xs uppercase tracking-[0.16em] text-amber-200/70 hover:text-amber-100"
            onClick={() => setOpen(true)}
          >
            {t("circle.replyTo", { name: reply.displayName })}
          </button>
        )
      ) : null}
      {reply.children.length > 0 ? (
        <ul className="mt-3 space-y-3">
          {reply.children.map((child) => (
            <ReplyItem
              key={child._id}
              reply={child}
              commentaryId={commentaryId}
              depth={depth + 1}
              canWrite={canWrite}
            />
          ))}
        </ul>
      ) : null}
    </li>
  );
}

function ReplyComposer({
  commentaryId,
  parentReplyId,
  onDone,
  compact = false,
  autoFocus = false,
}: {
  commentaryId: Id<"student_commentaries">;
  parentReplyId?: Id<"circle_replies">;
  onDone?: () => void;
  compact?: boolean;
  autoFocus?: boolean;
}) {
  const t = useT();
  const { user } = useAuth();
  const profile = useQuery(api.profiles.getMine, user ? {} : "skip");
  const post = useMutation(api.circleReplies.post);
  const [open, setOpen] = useState(Boolean(parentReplyId) || autoFocus);
  const [body, setBody] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const needsName = Boolean(user) && profile !== undefined && !profile?.displayName;

  async function submit() {
    setBusy(true);
    setError("");
    try {
      await post({
        commentaryId,
        body,
        parentReplyId,
        displayName: displayName.trim() || undefined,
      });
      setBody("");
      setOpen(false);
      onDone?.();
    } catch (err) {
      setError(err instanceof Error ? err.message : t("circle.replyFailed"));
    } finally {
      setBusy(false);
    }
  }

  if (!user) return null;

  if (!open && !parentReplyId) {
    return (
      <button
        type="button"
        className={`${compact ? "mt-2" : "mt-4"} font-sans text-xs uppercase tracking-[0.16em] text-amber-200/70 hover:text-amber-100`}
        onClick={() => setOpen(true)}
      >
        {t("circle.reply")}
      </button>
    );
  }

  return (
    <div className={`${compact ? "mt-3" : "mt-4"} space-y-2`}>
      {needsName ? (
        <Input
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          placeholder={t("commentary.namePlaceholder")}
          maxLength={40}
        />
      ) : null}
      <Textarea
        value={body}
        onChange={(e) => setBody(e.target.value)}
        placeholder={t("circle.replyPlaceholder")}
        rows={compact ? 3 : 4}
        autoFocus={autoFocus}
      />
      {error ? <p className="text-sm text-red-300">{error}</p> : null}
      <div className="flex gap-2">
        <Button
          type="button"
          size="sm"
          disabled={!body.trim() || busy || (needsName && !displayName.trim())}
          onClick={() => void submit()}
        >
          {busy ? t("common.sending") : t("circle.postReply")}
        </Button>
        <Button
          type="button"
          size="sm"
          variant="ghost"
          onClick={() => {
            setOpen(false);
            setError("");
            onDone?.();
          }}
        >
          {t("common.cancel")}
        </Button>
      </div>
    </div>
  );
}
