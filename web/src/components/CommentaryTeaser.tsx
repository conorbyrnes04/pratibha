'use client';

import { useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { stripMarkdown } from "@/lib/textPreview";
import { ListenButton } from "@/components/ListenButton";
import { useT } from "@/components/LocaleProvider";

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

export function CommentaryTeaser({ body, label, verseId }: CommentaryTeaserProps) {
  const t = useT();
  const heading = label || t("layers.commentary");
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
  const showBody = !needsExpand || open;

  return (
    <section
      className={`commentary-holo${showBody ? " commentary-holo--open" : ""}`}
      aria-label={heading}
    >
      {listen}
      <div className="commentary-holo__header">
        <h2 className="commentary-holo__label">{heading}</h2>
      </div>
      {needsExpand && !open ? (
        <button
          type="button"
          className="commentary-holo__hit"
          aria-expanded={false}
          onClick={() => setOpen(true)}
        >
          <span className="commentary-holo__teaser chat-markdown">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{teaser}</ReactMarkdown>
          </span>
          <span className="commentary-holo__affordance">{t("common.showMore")}</span>
        </button>
      ) : (
        <div className="commentary-holo__body chat-markdown reading-prose">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{body}</ReactMarkdown>
        </div>
      )}
      {needsExpand && open ? (
        <button
          type="button"
          className="commentary-holo__collapse"
          aria-expanded
          onClick={() => setOpen(false)}
        >
          {t("common.showLess")}
        </button>
      ) : null}
    </section>
  );
}
