'use client';

import { useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { stripMarkdown } from "@/lib/textPreview";
import { ListenButton } from "@/components/ListenButton";

type CommentaryTeaserProps = {
  body: string;
  label?: string;
  verseId?: string;
};

function teaserExcerpt(body: string, maxWords = 120): string {
  const clean = stripMarkdown(body).replace(/\s+/g, " ").trim();
  if (!clean) return "";
  const sentences = clean.split(/(?<=[.!?])\s+/).filter(Boolean);
  let out = "";
  for (const sentence of sentences.slice(0, 3)) {
    const next = out ? `${out} ${sentence}` : sentence;
    if (next.split(/\s+/).length > maxWords && out) break;
    out = next;
    if (out.split(/\s+/).length >= 90) break;
  }
  if (!out) {
    const words = clean.split(/\s+/).slice(0, maxWords);
    out = words.join(" ");
  }
  const fullWords = clean.split(/\s+/).length;
  const teaserWords = out.split(/\s+/).length;
  if (teaserWords < fullWords && !/[.!?…]$/.test(out)) out = `${out}…`;
  return out;
}

export function CommentaryTeaser({ body, label = "Commentary", verseId }: CommentaryTeaserProps) {
  const [open, setOpen] = useState(false);
  const teaser = useMemo(() => teaserExcerpt(body), [body]);
  const needsExpand = stripMarkdown(body).trim().length > teaser.replace(/…$/, "").length + 8;

  useEffect(() => {
    setOpen(false);
  }, [body]);

  if (!body.trim()) return null;

  const listen = verseId ? (
    <ListenButton verseId={verseId} section="commentary" variant="layer" />
  ) : null;

  if (!needsExpand) {
    return (
      <section className="commentary-holo commentary-holo--open" aria-label={label}>
        <div className="passage-layer__head">
          <p className="commentary-holo__label">{label}</p>
          {listen}
        </div>
        <div className="commentary-holo__body chat-markdown reading-prose">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{body}</ReactMarkdown>
        </div>
      </section>
    );
  }

  return (
    <section
      className={`commentary-holo${open ? " commentary-holo--open" : ""}`}
      aria-label={label}
    >
      <button
        type="button"
        className="commentary-holo__hit"
        aria-expanded={open}
        onClick={() => setOpen((v) => !v)}
      >
        <span className="commentary-holo__main">
          <span className="passage-layer__head">
            <span className="commentary-holo__label">{label}</span>
            {listen}
          </span>
          {!open ? (
            <span className="commentary-holo__teaser chat-markdown">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{teaser}</ReactMarkdown>
            </span>
          ) : null}
        </span>
        <span className="commentary-holo__affordance">{open ? "Collapse" : "Continue"}</span>
      </button>
      {open ? (
        <div className="commentary-holo__body chat-markdown reading-prose">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{body}</ReactMarkdown>
        </div>
      ) : null}
    </section>
  );
}
