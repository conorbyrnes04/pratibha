import Link from "next/link";
import type { VerseItem } from "@/lib/types";
import { getLayer, passagePreview, practiceText } from "@/lib/verseLayers";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageTitle } from "@/lib/passageTitles";
import { collectionArtPool, generatedArtPool } from "@/lib/collectionImages";
import { ArtBackdrop } from "@/components/ArtImage";
import { BrandMark } from "@/components/BrandMark";
import { LayerBlock } from "@/components/LayerBlock";

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
  const collection = displayCollectionName(item.collection);
  const artPool = item.collection ? collectionArtPool(item.collection) : generatedArtPool("bg-hero");
  const readHref = `/read/${encodeURIComponent(item._id)}`;
  const askHref = `/chat?verse_id=${encodeURIComponent(item._id)}&mode=explain`;

  return (
    <section id="daily" className="manuscript-card scroll-mt-24 overflow-hidden p-6 sm:p-8">
      <ArtBackdrop srcs={artPool} variant="hero" priority />
      <div className="relative z-10">
        <p className="eyebrow">Pratibha · Today&apos;s passage</p>
        <h1 className="mt-4 text-3xl font-semibold leading-none text-amber-100 sm:text-4xl">{title}</h1>
        <p className="soft mt-2 font-sans text-sm">{collection || "Pratibha corpus"}</p>

        <div className="my-6">
          <BrandMark size="lg" className="opacity-90" />
        </div>

        {/* Featured: source Original + Translation lead the card. */}
        {original ? (
          <LayerBlock layer={original} variant="plain" />
        ) : null}
        {iast ? <LayerBlock layer={iast} variant="plain" /> : null}
        {translation ? (
          <LayerBlock layer={translation} variant="plain" />
        ) : (
          <section className="passage-layer passage-layer--translation">
            <h2 className="layer-heading">Translation</h2>
            <p className="reading-prose mt-4">{passagePreview(item)}</p>
          </section>
        )}

        {practice ? (
          <div className="practice-card mt-6 max-w-3xl p-4">
            <p className="layer-heading">Practice</p>
            <p className="soft mt-2 text-base leading-relaxed">{practice}</p>
          </div>
        ) : null}

        {preview ? (
          <div className="mt-8 max-w-3xl">
            <p className="soft font-sans text-sm leading-relaxed">
              This is today&apos;s single passage. Sign in to read its commentary, cross-tradition
              resonances, and daily practice — and to open the full Library, Paths, Study Chat, and Journal.
            </p>
            <div className="mt-4 flex flex-wrap gap-3">
              <Link href="/login" className="btn-primary px-5 py-2.5">
                Sign in to enter
              </Link>
              <Link href="/login?mode=signup" className="btn-secondary px-5 py-2.5">
                Create an account
              </Link>
            </div>
          </div>
        ) : (
          <div className="mt-6 flex flex-wrap gap-3">
            <Link href={readHref} className="btn-primary px-5 py-2.5">
              Read today&apos;s passage
            </Link>
            <Link href={askHref} className="btn-secondary px-5 py-2.5">
              Ask about this
            </Link>
          </div>
        )}
      </div>
    </section>
  );
}
