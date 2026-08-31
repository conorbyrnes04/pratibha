"use client";

import { InkGlyph } from "@/components/InkGlyph";
import { useHoloTilt } from "@/lib/useHoloTilt";
import { BrandMark } from "@/components/BrandMark";
import {
  SHARE_INKS,
  type ShareInk,
  type ShareForceMark,
  type ShareTextMode,
  type ShareAspectRatio,
} from "@/lib/shareCard";

export type ShareCardCopy = {
  title: string;
  collection?: string;
  original?: string;
  translation?: string;
};

export function ShareCard({
  mark,
  ink,
  textMode,
  copy,
  fillWindow = false,
  aspectRatio = "post",
  holographic = false,
}: {
  mark: ShareForceMark;
  ink: ShareInk;
  textMode: ShareTextMode;
  copy: ShareCardCopy;
  fillWindow?: boolean;
  aspectRatio?: ShareAspectRatio;
  holographic?: boolean;
}) {
  const hex = SHARE_INKS[ink].hex;
  const tilt = useHoloTilt(holographic);
  const showOriginal = (textMode === "original" || textMode === "both") && Boolean(copy.original);
  const showTranslation =
    (textMode === "translation" || textMode === "both" || !showOriginal) && Boolean(copy.translation);
  const modeClass = fillWindow ? "share-card--line" : `share-card--${textMode}`;

  return (
    <article
      className={`share-card ${modeClass} share-card--${aspectRatio}${holographic ? " share-card--holo" : ""}`}
      style={{
        ["--share-ink" as string]: hex,
        ["--holo-x" as string]: String(tilt.x),
        ["--holo-y" as string]: String(tilt.y),
      }}
    >
      <div className="share-card__mark" aria-hidden>
        <InkGlyph glyph={mark} ink={hex} className="share-card__glyph" stroke strokeKey={`${mark}-${ink}`} />
      </div>
      <p className="share-card__meta">{copy.collection || "Pratibha"}</p>
      <h2 className="share-card__title">{copy.title}</h2>
      <div className="share-card__copy">
        {showOriginal ? (
          <p className="share-card__original">{copy.original}</p>
        ) : null}
        {showTranslation ? (
          <p className="share-card__translation">{copy.translation}</p>
        ) : null}
      </div>
      {holographic ? <span className="share-card__foil" aria-hidden /> : null}
      <footer className="share-card__foot">
        <BrandMark size="sm" />
        <span>pratibha</span>
        {holographic ? <span className="share-card__fav">favorite</span> : null}
      </footer>
    </article>
  );
}
