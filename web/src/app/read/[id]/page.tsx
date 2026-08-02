'use client';

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { getVerse, getVerses, getRelatedVerses } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { collectionsMatch, displayCollectionName } from "@/lib/collectionLabels";
import { collectionArtPool } from "@/lib/collectionImages";
import { displayPassageTitle, sortPassagesInText } from "@/lib/passageTitles";
import { LayerBlock } from "@/components/LayerBlock";
import { ReadingShell } from "@/components/ReadingShell";
import { InlineMarkdown } from "@/components/InlineMarkdown";
import { JournalPanel } from "@/components/JournalPanel";
import {
  getStudyLayers,
  getAppendixLayers,
  getAnchorChapter,
  getResonances,
  layerText,
  passagePreview,
  practiceText,
} from "@/lib/verseLayers";
import { firstSentence, stripMarkdown } from "@/lib/textPreview";
import { relatedPassages } from "@/lib/relatedPassages";
import { preferStudyUnits } from "@/lib/corpusFilters";
import { buildCitationIndex, resolveCitation, type CitationResolution } from "@/lib/citationResolver";
import { Button, buttonVariants } from "@/components/ui/button";
import { KitLink } from "@/components/ui/kit-link";
import { Separator } from "@/components/ui/separator";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
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

function practiceFallback(item: VerseItem): string {
  if ((item.themes || []).includes("witness")) {
    return "For 2 minutes, notice thoughts and sensations as objects appearing in awareness.";
  }
  if ((item.themes || []).includes("liberation")) {
    return "Ask once: what am I taking myself to be in this moment?";
  }
  return "Read once slowly, then pause for one minute before your next action.";
}

function commentaryTeaser(body: string, maxWords = 55): string {
  const clean = stripMarkdown(body).replace(/\s+/g, " ").trim();
  if (!clean) return "";
  const words = clean.split(/\s+/);
  if (words.length <= maxWords) return clean;
  return `${words.slice(0, maxWords).join(" ")}…`;
}

export default function VerseDetailPage() {
  const params = useParams<{ id: string }>();
  const [item, setItem] = useState<VerseItem | null>(null);
  const [allItems, setAllItems] = useState<VerseItem[]>([]);
  const [semanticRelated, setSemanticRelated] = useState<VerseItem[] | null>(null);
  const [showOriginal, setShowOriginal] = useState(true);
  const [commentaryOpen, setCommentaryOpen] = useState(false);
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

  useEffect(() => {
    setCommentaryOpen(false);
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
    return <main className="page-shell page-shell--reading soft">Opening the manuscript...</main>;
  }
  if (!item) {
    return <main className="page-shell page-shell--reading soft">Passage not found.</main>;
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
  const themes = item.themes || [];
  const hasApparatus =
    Boolean(keyTermsLayer) || resonances.length > 0 || hasSource || themes.length > 0;

  const collectionHref = item.collection
    ? `/read?collection=${encodeURIComponent(item.collection)}`
    : "/read";

  const translationBody = (translationLayer?.body || passagePreview(item) || "").trim();
  const translationPreview = firstSentence(translationBody);
  const deck =
    translationPreview &&
    translationPreview.length > 12 &&
    translationPreview.length < 200 &&
    translationBody.length > translationPreview.length + 40
      ? translationPreview
      : null;

  const commentaryPreview = commentaryBody ? commentaryTeaser(commentaryBody) : "";
  const commentaryNeedsExpand =
    Boolean(commentaryBody) &&
    stripMarkdown(commentaryBody).trim().length > commentaryPreview.replace(/…$/, "").length + 8;

  return (
    <main className="page-shell page-shell--reading">
      <ReadingShell artSrcs={collectionArtPool(item.collection)}>
        <nav className="passage-reading__crumb" aria-label="Breadcrumb">
          <Link href="/read">Library</Link>
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
              <Link href={backHref}>Path</Link>
            </>
          ) : null}
        </nav>

        <header className="passage-reading__header">
          <p className="passage-reading__meta">
            {displayCollectionName(item.collection) || "Pratibha"}
            {item.section ? ` · ${item.section}` : ""}
            {siblings.length > 1 && siblingIndex >= 0
              ? ` · ${siblingIndex + 1} of ${siblings.length}`
              : ""}
          </p>
          <h1 className="passage-reading__title">{displayPassageTitle(item)}</h1>
          {deck ? <p className="passage-reading__deck">{deck}</p> : null}
        </header>

        {originalLayer || iastLayer ? (
          <button
            type="button"
            className="passage-reading__toggle"
            onClick={() => setShowOriginal((v) => !v)}
          >
            {showOriginal ? "Hide original" : "Show original"}
          </button>
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
            <h2 className="passage-layer__label">Translation</h2>
            <p className="reading-prose mt-4">{passagePreview(item)}</p>
          </section>
        )}

        {practice ? (
          <>
            <Separator className="mt-8 max-w-[var(--reading-measure)] bg-[rgb(240_201_121_/_0.16)]" />
            <section className="passage-practice--plain">
              <h2 className="passage-layer__label">Practice</h2>
              <p className="passage-practice__body">{practice}</p>
            </section>
          </>
        ) : null}

        {commentaryBody ? (
          <div className="passage-commentary">
            {commentaryNeedsExpand ? (
              <Collapsible open={commentaryOpen} onOpenChange={setCommentaryOpen}>
                <CollapsibleTrigger className="passage-commentary__trigger">
                  <span className="passage-layer__label mb-0">Commentary</span>
                  <span className="font-sans text-xs text-stone-500">
                    {commentaryOpen ? "Collapse" : "Continue"}
                  </span>
                </CollapsibleTrigger>
                {!commentaryOpen ? (
                  <p className="passage-commentary__teaser">{commentaryPreview}</p>
                ) : null}
                <CollapsibleContent>
                  <div className="passage-commentary__body chat-markdown reading-prose">
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{commentaryBody}</ReactMarkdown>
                  </div>
                </CollapsibleContent>
              </Collapsible>
            ) : (
              <>
                <h2 className="passage-layer__label">Commentary</h2>
                <div className="passage-commentary__body chat-markdown reading-prose">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>{commentaryBody}</ReactMarkdown>
                </div>
              </>
            )}
          </div>
        ) : null}

        <footer className="passage-endmatter">
          {siblings.length > 1 ? (
            <nav className="passage-reading__nav passage-reading__nav--flush" aria-label="Passages in this text">
              {prevPassage ? (
                <Link
                  href={passageHref(prevPassage._id)}
                  className={buttonVariants({ variant: "secondary", size: "sm" })}
                  aria-label={`Previous: ${displayPassageTitle(prevPassage)}`}
                >
                  ← Previous
                </Link>
              ) : (
                <span className="soft px-1 text-sm">Start of text</span>
              )}
              <span className="soft tabular-nums text-sm">
                {siblingIndex >= 0 ? siblingIndex + 1 : "—"} of {siblings.length}
              </span>
              {nextPassage ? (
                <Link
                  href={passageHref(nextPassage._id)}
                  className={buttonVariants({ size: "sm" })}
                  aria-label={`Next: ${displayPassageTitle(nextPassage)}`}
                >
                  Next →
                </Link>
              ) : (
                <span className="soft px-1 text-sm">End of text</span>
              )}
            </nav>
          ) : null}

          <div className="passage-endmatter__actions">
            <KitLink
              href={`/chat?verse_id=${encodeURIComponent(item._id)}&mode=explain`}
              size="sm"
            >
              Ask about this
            </KitLink>
            <KitLink
              href={`/chat?verse_id=${encodeURIComponent(item._id)}&mode=practice`}
              variant="secondary"
              size="sm"
            >
              Practice chat
            </KitLink>
            <Sheet>
              <SheetTrigger
                render={<Button type="button" variant="ghost" size="sm" className="border border-white/10" />}
              >
                Write a note
              </SheetTrigger>
              <SheetContent
                side="bottom"
                className="max-h-[85vh] border-t border-amber-200/15 bg-[#0b0b14] sm:max-w-none"
              >
                <SheetHeader>
                  <SheetTitle className="text-amber-100">Journal</SheetTitle>
                  <SheetDescription className="soft">
                    A private note on this passage — saved on this device
                    {item ? ` · ${displayPassageTitle(item)}` : ""}.
                  </SheetDescription>
                </SheetHeader>
                <div className="overflow-y-auto px-4 pb-8">
                  <JournalPanel passage={item} bare />
                </div>
              </SheetContent>
            </Sheet>
          </div>
        </footer>

        {hasApparatus ? (
          <div className="passage-apparatus">
            <Accordion>
              {keyTermsLayer ? (
                <AccordionItem value="terms">
                  <AccordionTrigger>
                    Key terms
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
                  <AccordionTrigger>Resonances · {resonances.length}</AccordionTrigger>
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
                                <span className="font-semibold text-amber-100">Divergence:</span>{" "}
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
                  <AccordionTrigger>Public-domain source</AccordionTrigger>
                  <AccordionContent>
                    <div className="space-y-4">
                      {appendixLayers.map((layer, idx) => (
                        <LayerBlock key={`appendix-${layer.label}-${idx}`} layer={layer} bare />
                      ))}
                      {anchorChapter ? (
                        <div>
                          <h3 className="passage-layer__label">Full chapter</h3>
                          <LayerBlock
                            layer={{ kind: "appendix", label: "Full chapter", body: anchorChapter }}
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
                  <AccordionTrigger>Themes · {themes.length}</AccordionTrigger>
                  <AccordionContent>
                    <ul className="passage-themes-inline">
                      {themes.map((t) => (
                        <li key={t}>
                          <Link href={`/read?theme=${encodeURIComponent(t)}`}>{t}</Link>
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
            <h2 className="passage-layer__label">Related</h2>
            <p className="soft mt-1 text-sm">
              {relatedMode === "semantic"
                ? "Nearest in meaning across the corpus."
                : "Shared themes across traditions."}
            </p>
            <ul className="passage-related__list">
              {related.slice(0, 5).map((r) => (
                <li key={r._id} className="passage-related__item">
                  <Link href={`/read/${encodeURIComponent(r._id)}`}>
                    <p className="passage-related__title">{displayPassageTitle(r)}</p>
                    <p className="passage-related__meta">
                      {displayCollectionName(r.collection)}
                      {r.section ? ` · ${r.section}` : ""}
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
