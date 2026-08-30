import { InkGlyph } from "@/components/InkGlyph";
import { BrandMark } from "@/components/BrandMark";
import {
  SHARE_INKS,
  SHARE_ASPECT_RATIOS,
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
}: {
  mark: ShareForceMark;
  ink: ShareInk;
  textMode: ShareTextMode;
  copy: ShareCardCopy;
  fillWindow?: boolean;
  aspectRatio?: ShareAspectRatio;
}) {
  const hex = SHARE_INKS[ink].hex;
  const showOriginal = (textMode === "original" || textMode === "both") && Boolean(copy.original);
  const showTranslation =
    (textMode === "translation" || textMode === "both" || !showOriginal) && Boolean(copy.translation);
  const modeClass = fillWindow ? "share-card--line" : `share-card--${textMode}`;
  const aspectClass = `share-card--${aspectRatio}`;

  return (
    <article className={`share-card ${modeClass} ${aspectClass}`} style={{ ["--share-ink" as string]: hex }}>
      <div className="share-card__mark" aria-hidden>
        <InkGlyph glyph={mark} ink={hex} className="share-card__glyph" />
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
      <footer className="share-card__foot">
        <BrandMark size="sm" />
        <span>pratibha</span>
      </footer>
    </article>
  );
}
