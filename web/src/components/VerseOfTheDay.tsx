import Link from "next/link";
import type { VerseItem } from "@/lib/types";
import { getLayer, passagePreview, practiceText } from "@/lib/verseLayers";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageSourceLine, displayPassageTitle } from "@/lib/passageTitles";
import { collectionArtPool, generatedArtPool } from "@/lib/collectionImages";
import { LayerBlock } from "@/components/LayerBlock";
import { ReadingShell } from "@/components/ReadingShell";
import { buttonVariants } from "@/components/ui/button";

/**
 * The daily passage, formatted so the source **Original** (Devanagari, Tibetan
 * Uchen, Chinese, Greek…) and the **Translation** lead — the two layers that
 * give a first-time or logged-out visitor a real taste of the manuscript.
 *
 * preview mode (logged-out) swaps the study actions for a sign-in invitation
 * and keeps the deeper layers (commentary, resonances, practice) behind the gate.
 */
export function VerseOfTheDay({ item, preview = false }: { item: VerseItem; preview?: boolean }) {
  const original = getLayer(item, "original");
  const iast = getLayer(item, "iast");
  const translation = getLayer(item, "translation");
  const practice = preview ? "" : practiceText(item);

  const title = displayPassageTitle(item);
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
          <p className="passage-reading__meta">Today&apos;s passage</p>
          <h1 className="passage-reading__title">{title}</h1>
          <p className="passage-reading__deck">{sourceLine || "Pratibha corpus"}</p>
        </header>

        {original ? <LayerBlock layer={original} variant="plain" /> : null}
        {iast ? <LayerBlock layer={iast} variant="plain" /> : null}
        {translation ? (
          <LayerBlock layer={translation} variant="plain" />
        ) : (
          <section className="passage-layer passage-layer--translation">
            <h2 className="passage-layer__label">Translation</h2>
            <p className="reading-prose">{passagePreview(item)}</p>
          </section>
        )}

        {practice ? (
          <section className="passage-practice--plain">
            <h2 className="passage-layer__label">Practice</h2>
            <p className="passage-practice__body">{practice}</p>
          </section>
        ) : null}

        {preview ? (
          <div className="passage-reading__nav">
            <p className="soft mb-1 w-full font-sans text-sm leading-relaxed">
              Sign in to open commentary, resonances, practice, and the rest of the manuscript.
            </p>
            <Link href="/login" className={buttonVariants()}>
              Sign in to enter
            </Link>
            <Link href="/login?mode=signup" className={buttonVariants({ variant: "secondary" })}>
              Create an account
            </Link>
          </div>
        ) : (
          <div className="passage-reading__nav">
            <Link href={readHref} className={buttonVariants()}>
              Read today&apos;s passage
            </Link>
            <Link href={askHref} className={buttonVariants({ variant: "secondary" })}>
              Ask about this
            </Link>
          </div>
        )}
      </ReadingShell>
    </section>
  );
}
