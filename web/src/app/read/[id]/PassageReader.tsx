'use client';

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import dynamic from "next/dynamic";
import { getVerse, getVerses, getRelatedVerses } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { collectionsMatch, displayCollectionName } from "@/lib/collectionLabels";
import { collectionArtPool, redbookSlug, redbookSrc } from "@/lib/collectionImages";
import {
  displayPassageLocation,
  displayPassageTitle,
  sortPassagesInText,
} from "@/lib/passageTitles";
import { LayerBlock } from "@/components/LayerBlock";
import { useT } from "@/components/LocaleProvider";
import { useLocalizedVerse, useLocalizedVerseCards } from "@/components/useLocalizedStudy";
import { ListenButton } from "@/components/ListenButton";
import { ReadingShell } from "@/components/ReadingShell";
import { InlineMarkdown } from "@/components/InlineMarkdown";
import { JournalPanel } from "@/components/JournalPanel";
import { StudentCommentary } from "@/components/StudentCommentary";
import { CircleReadings } from "@/components/CircleReadings";
import { QuietBoundary } from "@/components/SanghaBoundary";
import { CommentaryTeaser } from "@/components/CommentaryTeaser";
import { OriginalReliabilityBadge } from "@/components/OriginalReliabilityBadge";
import {
  getStudyLayers,
  getAppendixLayers,
  getAnchorChapter,
  getResonances,
  layerText,
  passagePreview,
  practiceText,
} from "@/lib/verseLayers";
import { firstSentence } from "@/lib/textPreview";
import { relatedPassages } from "@/lib/relatedPassages";
import { preferStudyUnits } from "@/lib/corpusFilters";
import { buildCitationIndex, resolveCitation, type CitationResolution } from "@/lib/citationResolver";
import { buttonVariants } from "@/components/ui/button";
import { KitLink } from "@/components/ui/kit-link";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
import {
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "@/components/ui/sheet";

const ShareComposer = dynamic(
  () => import("@/components/ShareComposer").then((m) => ({ default: m.ShareComposer })),
  { ssr: false },
);

function practiceFallback(item: VerseItem, t: (key: string) => string): string {
  if ((item.themes || []).includes("witness")) {
    return t("reader.practiceWitness");
  }
  if ((item.themes || []).includes("liberation")) {
    return t("reader.practiceLiberation");
  }
  return t("reader.practiceDefault");
}

export function PassageReader({ initialItem = null }: { initialItem?: VerseItem | null }) {
  const t = useT();
  const params = useParams<{ id: string }>();
  // Seed from the server-fetched passage so the initial (server) render already
  // contains the reading content for crawlers and social previews.
  const [item, setItem] = useState<VerseItem | null>(initialItem);
  const [allItems, setAllItems] = useState<VerseItem[]>([]);
  const [semanticRelated, setSemanticRelated] = useState<VerseItem[] | null>(null);
  const [showOriginal, setShowOriginal] = useState(true);
  const [folioDesignOpen, setFolioDesignOpen] = useState(false);
  const [loading, setLoading] = useState(!initialItem);
  const [backHref, setBackHref] = useState<string | null>(null);
  const id = decodeURIComponent(params.id || "");

  useEffect(() => {
    if (typeof window === "undefined") return;
    const b = new URLSearchParams(window.location.search).get("back");
    setBackHref(b && b.startsWith("/") ? b : null);
  }, []);

  useEffect(() => {
    // Don't flash a loading state when the server already provided this passage;
    // just refresh it in the background.
    if (!item || item._id !== id) setLoading(true);
    getVerse(id)
      .then((v) => setItem(v))
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);
  const study = useLocalizedVerse(item);
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

  useEffect(() => {
    setFolioDesignOpen(false);
  }, [id]);

  const themeRelated = useMemo(() => {
    if (!item) return [] as VerseItem[];
    return relatedPassages(item, allItems, 6);
  }, [allItems, item]);

  const related = semanticRelated && semanticRelated.length > 0 ? semanticRelated : themeRelated;
  const relatedMode = semanticRelated && semanticRelated.length > 0 ? "semantic" : "themes";
  const relatedStudy = useLocalizedVerseCards(related.slice(0, 5), 5);

  const siblings = useMemo(() => {
    if (!item?.collection) return [] as VerseItem[];
    const pool = preferStudyUnits(allItems).filter((v) => collectionsMatch(v.collection, item.collection));
    return sortPassagesInText(pool);
  }, [allItems, item]);

  const siblingIndex = item ? siblings.findIndex((v) => v._id === item._id) : -1;
  const prevPassage = siblingIndex > 0 ? siblings[siblingIndex - 1] : null;
  const nextPassage =
    siblingIndex >= 0 && siblingIndex < siblings.length - 1 ? siblings[siblingIndex + 1] : null;
  const neighborStudy = useLocalizedVerseCards(
    [prevPassage, nextPassage].filter((passage): passage is VerseItem => Boolean(passage)),
    2,
  );

  function passageHref(passageId: string): string {
    const base = `/read/${encodeURIComponent(passageId)}`;
    if (!backHref) return base;
    return `${base}?back=${encodeURIComponent(backHref)}`;
  }

  const resonances = useMemo(() => ((study || item) ? getResonances((study || item)!) : []), [item, study]);
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
    return <main className="page-shell page-shell--reading soft">{t("reader.openingManuscript")}</main>;
  }
  if (!item) {
    return (
      <main className="page-shell page-shell--reading">
        <section className="card p-8 text-center">
          <h1 className="text-2xl text-amber-100">{t("reader.notFound")}</h1>
          <p className="soft mx-auto mt-3 max-w-md leading-relaxed">{t("notFound.lede")}</p>
          <div className="mt-6 flex flex-wrap justify-center gap-3">
            <Link href="/read" className={buttonVariants()}>
              {t("notFound.library")}
            </Link>
            <Link href="/" className={buttonVariants({ variant: "secondary" })}>
              {t("common.home")}
            </Link>
          </div>
        </section>
      </main>
    );
  }

  const display = study || item;
  const layers = getStudyLayers(display);
  const appendixLayers = getAppendixLayers(display);
  const anchorChapter = getAnchorChapter(item);

  const originalLayer = layers.find((l) => l.kind === "original");
  const iastLayer = layers.find((l) => l.kind === "iast");
  const translationLayer = layers.find((l) => l.kind === "translation");
  const commentaryBody = layerText(display, "commentary");
  const keyTermsLayer = layers.find((l) => l.kind === "key_terms");
  const practice = practiceText(display) || practiceFallback(item, t);
  const hasSource = appendixLayers.length > 0 || Boolean(anchorChapter);
  const themes = item.themes || [];
  const themeLabels = display.themes || themes;
  const hasApparatus =
    Boolean(keyTermsLayer) || resonances.length > 0 || hasSource || themes.length > 0;

  const collectionHref = item.collection
    ? `/read?collection=${encodeURIComponent(item.collection)}`
    : "/read";

  const translationBody = (translationLayer?.body || passagePreview(display) || "").trim();
  const translationPreview = firstSentence(translationBody);
  const deck =
    translationPreview &&
    translationPreview.length > 12 &&
    translationPreview.length < 200 &&
    translationBody.length > translationPreview.length + 40
      ? translationPreview
      : null;

  const passageLocation = displayPassageLocation(item);

  return (
    <main className="page-shell page-shell--reading">
      <ReadingShell
        artSrcs={collectionArtPool(item.collection)}
        mandalaSrc={
          redbookSlug(item.collection) ? redbookSrc(redbookSlug(item.collection)!) : undefined
        }
      >
        <nav className="passage-reading__crumb" aria-label={t("reader.breadcrumb")}>
          <Link href="/read">{t("nav.library")}</Link>
          {item.collection ? (
            <>
              <span className="passage-reading__crumb-sep" aria-hidden>
                /
              </span>
              <Link href={collectionHref}>{displayCollectionName(item.collection)}</Link>
            </>
          ) : null}
          {backHref ? (
            <>
              <span className="passage-reading__crumb-sep" aria-hidden>
                ·
              </span>
              <Link href={backHref}>{t("nav.path")}</Link>
            </>
          ) : null}
        </nav>

        <header className="passage-reading__header">
          <p className="passage-reading__meta">
            {displayCollectionName(item.collection) || "Pratibha"}
            {passageLocation ? ` · ${passageLocation}` : ""}
            {siblings.length > 1 && siblingIndex >= 0
              ? ` · ${t("reader.ofCount", { n: siblingIndex + 1, total: siblings.length })}`
              : ""}
          </p>
          <h1 className="passage-reading__title">{displayPassageTitle(display)}</h1>
          {deck ? <p className="passage-reading__deck">{deck}</p> : null}
          <OriginalReliabilityBadge item={item} />
        </header>

        {originalLayer || iastLayer ? (
          <div className="passage-reading__toolbar">
            <button
              type="button"
              className="passage-reading__toggle"
              onClick={() => setShowOriginal((v) => !v)}
            >
              {showOriginal ? t("layers.hideOriginal") : t("layers.showOriginal")}
            </button>
            <ListenButton verseId={item._id} />
          </div>
        ) : (
          <ListenButton verseId={item._id} />
        )}

        {showOriginal && originalLayer ? (
          <LayerBlock layer={originalLayer} variant="plain" />
        ) : null}
        {showOriginal && iastLayer ? (
          <LayerBlock layer={iastLayer} variant="plain" />
        ) : null}

        {translationLayer ? (
          <LayerBlock layer={translationLayer} variant="plain" verseId={item._id} />
        ) : originalLayer ? null : (
          <section className="passage-layer passage-layer--translation">
            <h2 className="passage-layer__label">{t("layers.translation")}</h2>
            <p className="reading-prose mt-4">{passagePreview(display)}</p>
          </section>
        )}

        {commentaryBody ? <CommentaryTeaser body={commentaryBody} verseId={item._id} /> : null}

        {practice ? (
          <section className="passage-practice--plain">
            <ListenButton verseId={item._id} section="practice" variant="layer" />
            <h2 className="passage-layer__label">{t("layers.practice")}</h2>
            <p className="passage-practice__body">{practice}</p>
          </section>
        ) : null}

        <QuietBoundary>
          <CircleReadings verseId={item._id} />
        </QuietBoundary>
        <QuietBoundary>
          <StudentCommentary
            verseId={item._id}
            verseTitle={displayPassageTitle(display)}
            onKeepFolio={() => setFolioDesignOpen(true)}
          />
        </QuietBoundary>

        <footer className="passage-endmatter">
          <div className="passage-endmatter__tools">
            <KitLink
              href={`/chat?verse_id=${encodeURIComponent(item._id)}&mode=explain&back=${encodeURIComponent(`/read/${item._id}`)}`}
              size="sm"
            >
              {t("chat.askLabel")}
            </KitLink>
            <ShareComposer
              item={display}
              designOpen={folioDesignOpen}
              onDesignOpenChange={setFolioDesignOpen}
            />
            <Sheet>
              <SheetTrigger
                render={<button type="button" className={buttonVariants({ variant: "secondary", size: "sm" })} />}
              >
                {t("nav.journal")}
              </SheetTrigger>
              <SheetContent
                side="bottom"
                className="max-h-[85vh] border-t border-amber-200/15 bg-[#0b0b14] sm:max-w-none"
              >
                <SheetHeader>
                  <SheetTitle className="text-amber-100">{t("nav.journal")}</SheetTitle>
                  <SheetDescription className="soft">
                    {t("reader.journalLede", {
                      detail: item ? ` · ${displayPassageTitle(item)}` : "",
                    })}
                  </SheetDescription>
                </SheetHeader>
                <div className="overflow-y-auto px-4 pb-8">
                  <JournalPanel passage={item} bare />
                </div>
              </SheetContent>
            </Sheet>
          </div>

          {siblings.length > 1 ? (
            <nav className="passage-reading__nav" aria-label={t("reader.passagesInText")}>
              {prevPassage ? (
                <Link
                  href={passageHref(prevPassage._id)}
                  className={buttonVariants({ variant: "secondary", size: "sm" })}
                  aria-label={t("reader.previous", {
                    title: displayPassageTitle(
                      neighborStudy.find((passage) => passage._id === prevPassage._id) || prevPassage,
                    ),
                  })}
                >
                  ← {t("reader.previousShort")}
                </Link>
              ) : (
                <span className="soft px-1 text-sm">{t("reader.startOfText")}</span>
              )}
              <span className="soft tabular-nums text-sm">
                {t("reader.ofCount", {
                  n: siblingIndex >= 0 ? siblingIndex + 1 : "—",
                  total: siblings.length,
                })}
              </span>
              {nextPassage ? (
                <Link
                  href={passageHref(nextPassage._id)}
                  className={buttonVariants({ size: "sm" })}
                  aria-label={t("reader.next", {
                    title: displayPassageTitle(
                      neighborStudy.find((passage) => passage._id === nextPassage._id) || nextPassage,
                    ),
                  })}
                >
                  {t("reader.nextShort")} →
                </Link>
              ) : (
                <span className="soft px-1 text-sm">{t("reader.endOfText")}</span>
              )}
            </nav>
          ) : null}
        </footer>

        {hasApparatus ? (
          <div className="passage-apparatus">
            <Accordion>
              {keyTermsLayer ? (
                <AccordionItem value="terms">
                  <AccordionTrigger>
                    {t("layers.keyTerms")}
                    {(keyTermsLayer.items || []).length
                      ? ` · ${(keyTermsLayer.items || []).length}`
                      : ""}
                  </AccordionTrigger>
                  <AccordionContent>
                    <LayerBlock layer={keyTermsLayer} bare />
                  </AccordionContent>
                </AccordionItem>
              ) : null}
              {resonances.length > 0 ? (
                <AccordionItem value="resonances">
                  <AccordionTrigger>
                    {t("layers.resonances")} · {resonances.length}
                  </AccordionTrigger>
                  <AccordionContent>
                    <div className="space-y-4">
                      {resonances.map((r, idx) => {
                        const link = resonanceLinks[idx];
                        const href =
                          link?.kind === "passage"
                            ? `/read/${encodeURIComponent(link.passageId)}`
                            : link?.kind === "collection"
                              ? `/read?collection=${encodeURIComponent(link.collection)}`
                              : null;
                        return (
                          <article key={`${r.citation}-${idx}`}>
                            {href ? (
                              <Link
                                href={href}
                                className="group inline-flex items-center gap-1 text-sm text-amber-100 underline decoration-amber-200/30 underline-offset-2 transition hover:decoration-amber-200/70"
                              >
                                <InlineMarkdown>{r.citation}</InlineMarkdown>
                                <span aria-hidden className="text-[10px] text-amber-200/60">
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
                                <span className="font-semibold text-amber-100">{t("layers.divergence")}:</span>{" "}
                                <InlineMarkdown>{r.divergence}</InlineMarkdown>
                              </p>
                            ) : null}
                          </article>
                        );
                      })}
                    </div>
                  </AccordionContent>
                </AccordionItem>
              ) : null}
              {hasSource ? (
                <AccordionItem value="source">
                  <AccordionTrigger>{t("reader.publicDomainSource")}</AccordionTrigger>
                  <AccordionContent>
                    <div className="space-y-4">
                      {appendixLayers.map((layer, idx) => (
                        <LayerBlock key={`appendix-${layer.label}-${idx}`} layer={layer} bare />
                      ))}
                      {anchorChapter ? (
                        <div>
                          <h3 className="passage-layer__label">{t("layers.fullChapter")}</h3>
                          <LayerBlock
                            layer={{ kind: "appendix", label: t("layers.fullChapter"), body: anchorChapter }}
                            bare
                          />
                        </div>
                      ) : null}
                    </div>
                  </AccordionContent>
                </AccordionItem>
              ) : null}
              {themes.length > 0 ? (
                <AccordionItem value="themes">
                  <AccordionTrigger>
                    {t("reader.themes")} · {themes.length}
                  </AccordionTrigger>
                  <AccordionContent>
                    <ul className="passage-themes-inline">
                      {themes.map((theme, idx) => (
                        <li key={theme}>
                          <Link href={`/read?theme=${encodeURIComponent(theme)}`}>
                            {themeLabels[idx] || theme}
                          </Link>
                        </li>
                      ))}
                    </ul>
                  </AccordionContent>
                </AccordionItem>
              ) : null}
            </Accordion>
          </div>
        ) : null}

        {related.length > 0 ? (
          <aside className="passage-related">
            <h2 className="passage-layer__label">{t("reader.related")}</h2>
            <p className="soft mt-1 text-sm">
              {relatedMode === "semantic" ? t("reader.relatedSemantic") : t("reader.relatedThemes")}
            </p>
            <ul className="passage-related__list">
              {relatedStudy.map((r) => (
                <li key={r._id} className="passage-related__item">
                  <Link href={`/read/${encodeURIComponent(r._id)}`}>
                    <p className="passage-related__title">{displayPassageTitle(r)}</p>
                    <p className="passage-related__meta">
                      {displayCollectionName(r.collection)}
                      {displayPassageLocation(r) ? ` · ${displayPassageLocation(r)}` : ""}
                    </p>
                  </Link>
                </li>
              ))}
            </ul>
          </aside>
        ) : null}
      </ReadingShell>
    </main>
  );
}
