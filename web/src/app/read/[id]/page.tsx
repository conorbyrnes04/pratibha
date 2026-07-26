'use client';

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { getVerse, getVerses, getRelatedVerses } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { collectionsMatch, displayCollectionName } from "@/lib/collectionLabels";
import { collectionArtPool } from "@/lib/collectionImages";
import { unitGlyph } from "@/lib/glyphs";
import { ArtBackdrop } from "@/components/ArtImage";
import { Glyph } from "@/components/Glyph";
import { displayPassageTitle, sortPassagesInText } from "@/lib/passageTitles";
import { LayerBlock } from "@/components/LayerBlock";
import { CommentaryTeaser } from "@/components/CommentaryTeaser";
import { InlineMarkdown } from "@/components/InlineMarkdown";
import { JournalPanel } from "@/components/JournalPanel";
import { Disclosure } from "@/components/ui/Disclosure";
import {
  getStudyLayers,
  getAppendixLayers,
  getAnchorChapter,
  getResonances,
  layerText,
  passagePreview,
  practiceText,
} from "@/lib/verseLayers";
import { relatedPassages } from "@/lib/relatedPassages";
import { preferStudyUnits } from "@/lib/corpusFilters";
import { buildCitationIndex, resolveCitation, type CitationResolution } from "@/lib/citationResolver";

function practiceFallback(item: VerseItem): string {
  if ((item.themes || []).includes("witness")) {
    return "For 2 minutes, notice thoughts and sensations as objects appearing in awareness.";
  }
  if ((item.themes || []).includes("liberation")) {
    return "Ask once: what am I taking myself to be in this moment?";
  }
  return "Read once slowly, then pause for one minute before your next action.";
}

export default function VerseDetailPage() {
  const params = useParams<{ id: string }>();
  const [item, setItem] = useState<VerseItem | null>(null);
  const [allItems, setAllItems] = useState<VerseItem[]>([]);
  const [semanticRelated, setSemanticRelated] = useState<VerseItem[] | null>(null);
  const [showOriginal, setShowOriginal] = useState(true);
  const [loading, setLoading] = useState(true);
  const [backHref, setBackHref] = useState<string | null>(null);
  const id = decodeURIComponent(params.id || "");

  useEffect(() => {
    if (typeof window === "undefined") return;
    const b = new URLSearchParams(window.location.search).get("back");
    setBackHref(b && b.startsWith("/") ? b : null);
  }, []);

  useEffect(() => {
    getVerse(id)
      .then((v) => setItem(v))
      .finally(() => setLoading(false));
  }, [id]);
  useEffect(() => {
    getVerses("strong_draft").then(setAllItems).catch(() => setAllItems([]));
  }, []);
  useEffect(() => {
    let cancelled = false;
    setSemanticRelated(null);
    getRelatedVerses(id, 6)
      .then((items) => {
        if (!cancelled) setSemanticRelated(items);
      })
      .catch(() => {
        if (!cancelled) setSemanticRelated([]);
      });
    return () => {
      cancelled = true;
    };
  }, [id]);

  const themeRelated = useMemo(() => {
    if (!item) return [] as VerseItem[];
    return relatedPassages(item, allItems, 6);
  }, [allItems, item]);

  const related = semanticRelated && semanticRelated.length > 0 ? semanticRelated : themeRelated;
  const relatedMode = semanticRelated && semanticRelated.length > 0 ? "semantic" : "themes";

  const siblings = useMemo(() => {
    if (!item?.collection) return [] as VerseItem[];
    const pool = preferStudyUnits(allItems).filter((v) => collectionsMatch(v.collection, item.collection));
    return sortPassagesInText(pool);
  }, [allItems, item]);

  const siblingIndex = item ? siblings.findIndex((v) => v._id === item._id) : -1;
  const prevPassage = siblingIndex > 0 ? siblings[siblingIndex - 1] : null;
  const nextPassage =
    siblingIndex >= 0 && siblingIndex < siblings.length - 1 ? siblings[siblingIndex + 1] : null;

  function passageHref(passageId: string): string {
    const base = `/read/${encodeURIComponent(passageId)}`;
    if (!backHref) return base;
    return `${base}?back=${encodeURIComponent(backHref)}`;
  }

  const resonances = useMemo(() => (item ? getResonances(item) : []), [item]);
  const citationIndex = useMemo(() => buildCitationIndex(allItems), [allItems]);
  const knownIds = useMemo(() => new Set(allItems.map((v) => v._id)), [allItems]);
  const resonanceLinks = useMemo<CitationResolution[]>(
    () =>
      resonances.map((r) => {
        if (r.passage_id && knownIds.has(r.passage_id)) {
          return { kind: "passage", passageId: r.passage_id, collection: "" };
        }
        return resolveCitation(r.citation, citationIndex);
      }),
    [resonances, citationIndex, knownIds],
  );

  if (loading) {
    return <main className="page-shell soft">Opening the manuscript...</main>;
  }
  if (!item) {
    return <main className="page-shell soft">Passage not found.</main>;
  }

  const layers = getStudyLayers(item);
  const appendixLayers = getAppendixLayers(item);
  const anchorChapter = getAnchorChapter(item);

  const originalLayer = layers.find((l) => l.kind === "original");
  const iastLayer = layers.find((l) => l.kind === "iast");
  const translationLayer = layers.find((l) => l.kind === "translation");
  const commentaryBody = layerText(item, "commentary");
  const keyTermsLayer = layers.find((l) => l.kind === "key_terms");
  const practice = practiceText(item) || practiceFallback(item);
  const hasSource = appendixLayers.length > 0 || Boolean(anchorChapter);
  const hasDeeper =
    Boolean(keyTermsLayer) || resonances.length > 0 || hasSource;

  const textNav =
    siblings.length > 1 ? (
      <nav className="passage-reading__nav" aria-label="Passages in this text">
        {prevPassage ? (
          <Link
            href={passageHref(prevPassage._id)}
            className="btn-secondary px-4 py-2"
            aria-label={`Previous: ${displayPassageTitle(prevPassage)}`}
          >
            ← Previous
          </Link>
        ) : (
          <span className="soft px-1">Start of text</span>
        )}
        <span className="soft tabular-nums">
          {siblingIndex >= 0 ? siblingIndex + 1 : "—"} of {siblings.length}
        </span>
        {nextPassage ? (
          <Link
            href={passageHref(nextPassage._id)}
            className="btn-primary px-4 py-2"
            aria-label={`Next: ${displayPassageTitle(nextPassage)}`}
          >
            Next →
          </Link>
        ) : (
          <span className="soft px-1">End of text</span>
        )}
      </nav>
    ) : null;

  const collectionHref = item.collection
    ? `/read?collection=${encodeURIComponent(item.collection)}`
    : "/read";

  return (
    <main className="page-shell">
      <div className="flex flex-wrap items-center gap-4">
        {backHref ? (
          <Link href={backHref} className="font-sans text-sm text-amber-200 hover:text-amber-100">
            ← Back to path
          </Link>
        ) : null}
        <Link href={collectionHref} className="soft font-sans text-sm hover:text-amber-100">
          ← Back to text
        </Link>
        <Link href="/read" className="soft font-sans text-sm hover:text-amber-100">
          Library
        </Link>
      </div>

      <div className="passage-reading mt-4">
        <header className="passage-reading__hero relative overflow-hidden rounded-[1.5rem]">
          <ArtBackdrop srcs={collectionArtPool(item.collection)} variant="banner" priority />
          <div className="relative z-10 px-4 py-8 sm:px-8">
            <div className="mx-auto flex max-w-xl flex-col items-center gap-3">
              <span className="passage-hero__glyph inline-flex" aria-hidden>
                <Glyph name={unitGlyph(item._id)} size="md" zoom />
              </span>
              <p className="eyebrow">
                {displayCollectionName(item.collection) || "Pratibha"}
                {item.section ? ` · ${item.section}` : ""}
                {siblings.length > 1 && siblingIndex >= 0
                  ? ` · ${siblingIndex + 1} of ${siblings.length}`
                  : ""}
              </p>
              <h1 className="text-3xl font-semibold leading-[1.1] tracking-[-0.03em] text-stone-100 sm:text-4xl">
                {displayPassageTitle(item)}
              </h1>
            </div>
          </div>
        </header>

        {originalLayer || iastLayer ? (
          <div className="mt-2 text-center">
            <button
              type="button"
              className="soft font-sans text-xs tracking-wide hover:text-amber-100"
              onClick={() => setShowOriginal((v) => !v)}
            >
              {showOriginal ? "Hide original" : "Show original"}
            </button>
          </div>
        ) : null}

        {showOriginal && originalLayer ? (
          <LayerBlock layer={originalLayer} variant="plain" />
        ) : null}
        {showOriginal && iastLayer ? (
          <LayerBlock layer={iastLayer} variant="plain" />
        ) : null}

        {translationLayer ? (
          <LayerBlock layer={translationLayer} variant="plain" />
        ) : (
          <section className="passage-layer passage-layer--translation">
            <h2 className="layer-heading">Translation</h2>
            <p className="reading-prose mt-4">{passagePreview(item)}</p>
          </section>
        )}

        {practice ? (
          <section className="passage-practice">
            <h2 className="layer-heading">Practice</h2>
            <p className="mt-3 text-[1.05rem] leading-relaxed text-stone-200">{practice}</p>
          </section>
        ) : null}

        {commentaryBody ? <CommentaryTeaser body={commentaryBody} /> : null}

        {textNav}

        {hasDeeper ? (
          <div className="passage-reading__secondary">
            <p className="eyebrow mb-3 text-amber-200/70">Go deeper</p>
            <div className="disclosure-stack">
              {keyTermsLayer ? (
                <Disclosure summary="Key terms" hint={`${(keyTermsLayer.items || []).length || ""}`}>
                  <LayerBlock layer={keyTermsLayer} bare />
                </Disclosure>
              ) : null}
              {resonances.length > 0 ? (
                <Disclosure summary="Cross-tradition resonances" hint={`${resonances.length}`}>
                  <div className="space-y-3">
                    {resonances.map((r, idx) => {
                      const link = resonanceLinks[idx];
                      const href =
                        link?.kind === "passage"
                          ? `/read/${encodeURIComponent(link.passageId)}`
                          : link?.kind === "collection"
                            ? `/read?collection=${encodeURIComponent(link.collection)}`
                            : null;
                      return (
                        <article key={`${r.citation}-${idx}`} className="citation-card p-3">
                          {href ? (
                            <Link
                              href={href}
                              className="group inline-flex items-center gap-1 text-sm text-amber-100 underline decoration-amber-200/30 underline-offset-2 transition hover:decoration-amber-200/70"
                            >
                              <InlineMarkdown>{r.citation}</InlineMarkdown>
                              <span aria-hidden className="text-[10px] text-amber-200/60 transition group-hover:translate-x-0.5">
                                {link?.kind === "passage" ? "↗" : "→"}
                              </span>
                            </Link>
                          ) : (
                            <span className="text-sm text-amber-100">
                              <InlineMarkdown>{r.citation}</InlineMarkdown>
                            </span>
                          )}
                          <p className="soft mt-1 text-sm leading-relaxed">
                            <InlineMarkdown>{r.resonance}</InlineMarkdown>
                          </p>
                          {r.divergence ? (
                            <p className="mt-2 text-sm leading-relaxed text-stone-300">
                              <span className="font-semibold text-amber-100">Divergence:</span>{" "}
                              <InlineMarkdown>{r.divergence}</InlineMarkdown>
                            </p>
                          ) : null}
                        </article>
                      );
                    })}
                  </div>
                </Disclosure>
              ) : null}
              {hasSource ? (
                <Disclosure summary="Public-domain source">
                  <div className="space-y-4">
                    {appendixLayers.map((layer, idx) => (
                      <LayerBlock key={`appendix-${layer.label}-${idx}`} layer={layer} bare />
                    ))}
                    {anchorChapter ? (
                      <div>
                        <h3 className="layer-heading mb-2">Full chapter — public-domain translation</h3>
                        <LayerBlock layer={{ kind: "appendix", label: "Full chapter", body: anchorChapter }} bare />
                      </div>
                    ) : null}
                  </div>
                </Disclosure>
              ) : null}
            </div>
          </div>
        ) : null}

        <div className="passage-reading__secondary">
          <div className="flex flex-wrap gap-3">
            <Link
              href={`/chat?verse_id=${encodeURIComponent(item._id)}&mode=explain`}
              className="btn-primary px-5 py-2.5"
            >
              Guided Study
            </Link>
            <Link
              href={`/chat?verse_id=${encodeURIComponent(item._id)}&mode=practice`}
              className="btn-secondary px-5 py-2.5"
            >
              Practice chat
            </Link>
          </div>

          {item.themes && item.themes.length > 0 ? (
            <div className="mt-6 flex flex-wrap gap-2">
              {item.themes.map((t) => (
                <Link
                  key={t}
                  href={`/read?theme=${encodeURIComponent(t)}`}
                  className="rounded-full border border-amber-200/30 px-3 py-1 text-xs text-amber-100 hover:border-amber-200/60"
                >
                  {t}
                </Link>
              ))}
            </div>
          ) : null}

          <div className="mt-8">
            <JournalPanel passage={item} />
          </div>

          {related.length > 0 ? (
            <div className="mt-10">
              <h2 className="layer-heading text-amber-100">Related passages</h2>
              <p className="soft mt-1 text-sm">
                {relatedMode === "semantic"
                  ? "Nearest in meaning across the corpus."
                  : "Shared themes across traditions."}
              </p>
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                {related.slice(0, 4).map((r) => (
                  <Link
                    key={r._id}
                    href={`/read/${encodeURIComponent(r._id)}`}
                    className="citation-card block p-3 hover:border-amber-300/30"
                  >
                    <p className="text-sm text-amber-100">{displayPassageTitle(r)}</p>
                    <p className="soft mt-1 text-xs">
                      {displayCollectionName(r.collection)}
                      {r.section ? ` · ${r.section}` : ""}
                    </p>
                  </Link>
                ))}
              </div>
            </div>
          ) : null}
        </div>
      </div>
    </main>
  );
}
