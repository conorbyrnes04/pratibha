"use client";

import { useEffect, useMemo, useState, type ReactNode } from "react";
import Link from "next/link";
import { getVerse } from "@/lib/api";
import { ShareCard } from "@/components/ShareCard";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageTitle } from "@/lib/passageTitles";
import { stripMarkdown } from "@/lib/textPreview";
import { layerText } from "@/lib/verseLayers";
import {
  clipShareText,
  folioCandidates,
  isShareForceMark,
  isShareInk,
  isShareTextMode,
  pickFolioLine,
  verseShareMark,
  type ShareAspectRatio,
  type ShareForceMark,
  type ShareInk,
  type ShareTextMode,
} from "@/lib/shareCard";
import type { VerseItem } from "@/lib/types";

export type FolioCardOptions = {
  mark?: string;
  ink?: string;
  textMode?: string;
  line?: number;
  aspectRatio?: string;
  holographic?: boolean;
  reading?: string;
};

export function ManuscriptFolio({
  verseId,
  verseTitle,
  note,
  card,
  actions,
  variant = "card",
  page,
  pages,
}: {
  verseId: string;
  verseTitle: string;
  note?: string;
  card?: FolioCardOptions;
  actions?: ReactNode;
  variant?: "card" | "leaf";
  page?: number;
  pages?: number;
}) {
  const [item, setItem] = useState<VerseItem | null | undefined>(undefined);

  useEffect(() => {
    let cancelled = false;
    void getVerse(verseId).then((verse) => {
      if (!cancelled) setItem(verse);
    });
    return () => {
      cancelled = true;
    };
  }, [verseId]);

  const mark: ShareForceMark =
    card?.mark && isShareForceMark(card.mark)
      ? card.mark
      : item
        ? verseShareMark(item)
        : "lotus";
  const ink: ShareInk = card?.ink && isShareInk(card.ink) ? card.ink : "gold";
  const storedMode: ShareTextMode | undefined =
    card?.textMode && isShareTextMode(card.textMode) ? card.textMode : undefined;
  const aspectRatio: ShareAspectRatio =
    card?.aspectRatio === "story" ? "story" : "post";
  const holographic = Boolean(card?.holographic);
  const storedReading = card?.reading?.trim() || "";
  const title = item ? displayPassageTitle(item) : verseTitle;
  const collection = item
    ? displayCollectionName(item.collection) || item.collection
    : "Pratibha";
  const original = item ? stripMarkdown(layerText(item, "original")) : "";
  const iast = item ? stripMarkdown(layerText(item, "iast")) : "";
  const translation = item
    ? stripMarkdown(layerText(item, "translation") || item.translation || "")
    : "";
  const mode: ShareTextMode = storedMode || (original ? "both" : "translation");

  const cardCopy = useMemo(() => {
    const lines = folioCandidates({
      original,
      iast,
      translation,
      mode,
    });
    const picked = pickFolioLine(lines, card?.line) || (!card?.line ? lines[0] : undefined);
    if (picked) {
      return {
        title,
        collection,
        original: picked.source === "translation" ? undefined : picked.text,
        translation: picked.source === "translation" ? picked.text : undefined,
        reading: storedReading || undefined,
      };
    }
    return {
      title,
      collection,
      original: original ? clipShareText(original, 72) : undefined,
      translation: translation ? clipShareText(translation, 110) : undefined,
      reading: storedReading || undefined,
    };
  }, [card?.line, collection, iast, mode, original, storedReading, title, translation]);

  const textMode: ShareTextMode = cardCopy.original && !cardCopy.translation
    ? "original"
    : cardCopy.translation && !cardCopy.original
      ? "translation"
      : cardCopy.original
        ? "both"
        : "translation";

  if (variant === "leaf") {
    const body = cardCopy.translation || cardCopy.original || translation || "";
    return (
      <article className="manuscript-leaf">
        <p className="manuscript-leaf__meta">
          {collection}
          {page && pages ? ` · ${page} of ${pages}` : ""}
        </p>
        <h2 className="manuscript-leaf__title">
          <Link href={`/read/${encodeURIComponent(verseId)}`}>{title}</Link>
        </h2>
        {body ? <p className="manuscript-leaf__verse">{body}</p> : null}
        {storedReading ? <p className="manuscript-leaf__note">{storedReading}</p> : null}
        {note ? <p className="manuscript-leaf__note">{note}</p> : null}
        {actions ? <div className="manuscript-folio__actions">{actions}</div> : null}
      </article>
    );
  }

  return (
    <article className="manuscript-folio">
      <Link href={`/read/${encodeURIComponent(verseId)}`} className="manuscript-folio__card">
        <ShareCard
          mark={mark}
          ink={ink}
          textMode={textMode}
          copy={cardCopy}
          fillWindow={Boolean(cardCopy.original || cardCopy.translation)}
          aspectRatio={aspectRatio}
          holographic={holographic}
        />
      </Link>
      {note ? <p className="manuscript-folio__note">{note}</p> : null}
      {actions ? <div className="manuscript-folio__actions">{actions}</div> : null}
    </article>
  );
}
