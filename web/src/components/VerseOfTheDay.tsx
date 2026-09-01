"use client";

import Link from "next/link";
import type { VerseItem } from "@/lib/types";
import { getLayer, passagePreview, practiceText } from "@/lib/verseLayers";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageSourceLine, displayPassageTitle } from "@/lib/passageTitles";
import { collectionArtPool, generatedArtPool } from "@/lib/collectionImages";
import { LayerBlock } from "@/components/LayerBlock";
import { ListenButton } from "@/components/ListenButton";
import { ReadingShell } from "@/components/ReadingShell";
import { buttonVariants } from "@/components/ui/button";
import { ShareComposer } from "@/components/ShareComposer";
import { SanghaBoundary } from "@/components/SanghaBoundary";
import { useT } from "@/components/LocaleProvider";
import { useLocalizedVerse } from "@/components/useLocalizedStudy";

/**
 * The daily passage, formatted so the source **Original** (Devanagari, Tibetan
 * Uchen, Chinese, Greek…) and the **Translation** lead — the two layers that
 * give a first-time or logged-out visitor a real taste of the manuscript.
 *
 * preview mode (logged-out) swaps the study actions for a sign-in invitation
 * and keeps the deeper layers (commentary, resonances, practice) behind the gate.
 */
export function VerseOfTheDay({ item, preview = false }: { item: VerseItem; preview?: boolean }) {
  const t = useT();
  const study = useLocalizedVerse(item) || item;
  const original = getLayer(study, "original");
  const iast = getLayer(study, "iast");
  const translation = getLayer(study, "translation");
  const practice = preview ? "" : practiceText(study);

  const title = displayPassageTitle(study);
  const sourceLine = displayPassageSourceLine({
    ...item,
    collection: displayCollectionName(item.collection) || item.collection,
  });
  const artPool = item.collection ? collectionArtPool(item.collection) : generatedArtPool("bg-hero");
  const readHref = `/read/${encodeURIComponent(item._id)}`;
  const askHref = `/chat?verse_id=${encodeURIComponent(item._id)}&mode=explain`;

  return (
    <section id="daily" className="scroll-mt-24">
      <ReadingShell artSrcs={artPool}>
        <header className="passage-reading__header">
          <p className="passage-reading__meta">{t("today.passage")}</p>
          <h1 className="passage-reading__title">{title}</h1>
          <p className="passage-reading__deck">{sourceLine || t("today.corpus")}</p>
          <ListenButton verseId={item._id} />
        </header>

        {original ? <LayerBlock layer={original} variant="plain" /> : null}
        {iast ? <LayerBlock layer={iast} variant="plain" /> : null}
        {translation ? (
          <LayerBlock layer={translation} variant="plain" verseId={item._id} />
        ) : (
          <section className="passage-layer passage-layer--translation">
            <h2 className="passage-layer__label">{t("layers.translation")}</h2>
            <p className="reading-prose">{passagePreview(study)}</p>
          </section>
        )}

        {practice ? (
          <section className="passage-practice--plain">
            <ListenButton verseId={item._id} section="practice" variant="layer" />
            <h2 className="passage-layer__label">{t("layers.practice")}</h2>
            <p className="passage-practice__body">{practice}</p>
          </section>
        ) : null}

        {preview ? (
          <div className="passage-reading__nav">
            <p className="soft mb-1 w-full font-sans text-sm leading-relaxed">
              {t("today.previewLede")}
            </p>
            <Link href="/login" className={buttonVariants()}>
              {t("today.signInEnter")}
            </Link>
            <Link href="/login?mode=signup" className={buttonVariants({ variant: "secondary" })}>
              {t("auth.createAccount")}
            </Link>
          </div>
        ) : (
          <div className="passage-reading__nav">
            <Link href={readHref} className={buttonVariants()}>
              {t("today.readToday")}
            </Link>
            <Link href={askHref} className={buttonVariants({ variant: "secondary" })}>
              {t("today.askAbout")}
            </Link>
            <SanghaBoundary>
              <ShareComposer item={study} />
            </SanghaBoundary>
          </div>
        )}
      </ReadingShell>
    </section>
  );
}
