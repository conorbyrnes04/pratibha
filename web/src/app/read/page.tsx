'use client';

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useMemo, useState } from "react";
import { getVerses, pingHealth } from "@/lib/api";
import { catalogMaturityKey, readCatalogCache } from "@/lib/catalogCache";
import type { VerseItem } from "@/lib/types";
import { firstSentence } from "@/lib/textPreview";
import { FilterSelect } from "@/components/FilterSelect";
import { ThemeConstellation } from "@/components/ThemeConstellation";
import { buildCollectionOptions, filterPassages, topThemes, uniqueCollections } from "@/lib/corpusFilters";
import { collectionsMatch, displayCollectionName } from "@/lib/collectionLabels";
import { collectionArtPool, generatedArtPool, redbookSlug, redbookSrc } from "@/lib/collectionImages";
import { LayoutGroup, motion } from "motion/react";
import { sumiGlyph, verseSumiGlyph } from "@/lib/sumiGlyphs";
import { buildLibraryTomes, groupTomesByTradition, sortTomes, LIBRARY_SORT_OPTIONS, type LibrarySort, type LibraryTome } from "@/lib/libraryTomes";
import { ArtBackdrop } from "@/components/ArtImage";
import { InkGlyph } from "@/components/InkGlyph";
import { Disclosure } from "@/components/ui/Disclosure";
import {
  displayPassageLocation,
  displayPassageTitle,
  patanjaliSutraRef,
  sortPassagesForLibrary,
} from "@/lib/passageTitles";
import { layerText, passagePreview, practiceText } from "@/lib/verseLayers";
import { Input } from "@/components/ui/input";
import { CollectionGate } from "@/components/CollectionGate";
import { ListenButton } from "@/components/ListenButton";
import { useT } from "@/components/LocaleProvider";
import { useLocalizedVerseCards } from "@/components/useLocalizedStudy";
import { catalogQuoteCandidates } from "@/lib/heroQuotes";

/** Library catalog lifecycle — never treat cold/fail as a true empty shelf. */
type LibraryStatus = "loading" | "waking" | "ready" | "error";

function reflectionPrompt(item: VerseItem, t: (key: string, vars?: Record<string, string | number>) => string): string {
  const theme = (item.themes || [])[0];
  if (theme) return t("library.noticeTheme", { theme });
  return t("library.shiftInvite");
}

// Shared-element flight timing — the tome's Red Book mandala morphs from the
// shelf emblem into the reading header backdrop and back.
const TOME_FLIGHT = { type: "spring", stiffness: 260, damping: 32, mass: 0.9 } as const;

function TomeCard({ tome, onOpen }: { tome: LibraryTome; onOpen: () => void }) {
  const t = useT();
  const rb = redbookSlug(tome.collection);
  return (
    <button type="button" onClick={onOpen} className="tome">
      <span className="tome__glyph" aria-hidden>
        {rb ? (
          <motion.span
            layoutId={`tome-${tome.collection}`}
            transition={TOME_FLIGHT}
            className="tome__mandala"
            style={{ backgroundImage: `url(${redbookSrc(rb)})` }}
          />
        ) : (
          <InkGlyph glyph={tome.glyph} state="arising" size="xl" mask />
        )}
      </span>
      <span className="tome__body">
        <span className="tome__title">{tome.displayName}</span>
        <span className="tome__author">{tome.author}</span>
      </span>
      <span className="tome__foot">
        <span className="tome__tradition">{tome.tradition}</span>
        <span className="tome__meta">
          {tome.count} {tome.count === 1 ? t("library.passageOne") : t("library.passageMany")} · {tome.authored}
        </span>
      </span>
    </button>
  );
}

function LibraryPageContent() {
  const t = useT();
  const router = useRouter();
  const searchParams = useSearchParams();
  const [items, setItems] = useState<VerseItem[]>([]);
  const [status, setStatus] = useState<LibraryStatus>("loading");
  const [loadError, setLoadError] = useState("");
  const [showingStale, setShowingStale] = useState(false);
  const [retryToken, setRetryToken] = useState(0);
  const [q, setQ] = useState("");
  const [collection, setCollection] = useState(searchParams.get("collection") || "all");
  const [theme, setTheme] = useState(searchParams.get("theme") || "all");
  const [learningMode, setLearningMode] = useState(true);
  const [includeDrafts, setIncludeDrafts] = useState(false);
  const [librarySort, setLibrarySort] = useState<LibrarySort>("tradition");

  useEffect(() => {
    const maturity = includeDrafts ? "all" : "strong_draft";
    const cacheKey = catalogMaturityKey(maturity);
    const cached = readCatalogCache(cacheKey);
    const hasCachedItems = Boolean(cached && cached.items.length > 0);

    if (hasCachedItems && cached) {
      setItems(cached.items);
      setShowingStale(true);
      setStatus("ready");
      setLoadError("");
    } else {
      setItems([]);
      setShowingStale(false);
      setStatus("loading");
      setLoadError("");
    }

    const ac = new AbortController();
    let servedFromCache = false;
    // Nudge Render awake before the heavier /verses payload.
    void pingHealth(ac.signal);

    getVerses(maturity, {
      signal: ac.signal,
      onStatus: (s) => {
        if (ac.signal.aborted) return;
        if (!hasCachedItems) setStatus(s);
      },
      onMeta: (meta) => {
        servedFromCache = Boolean(meta.fromCache);
      },
    })
      .then((rows) => {
        if (ac.signal.aborted) return;
        setItems(rows);
        setStatus("ready");
        if (servedFromCache) {
          setShowingStale(true);
          setLoadError("library.staleCatalog");
        } else {
          setShowingStale(false);
          setLoadError("");
        }
      })
      .catch(() => {
        if (ac.signal.aborted) return;
        if (hasCachedItems) {
          setStatus("ready");
          setShowingStale(true);
          setLoadError("library.staleCatalog");
        } else {
          setItems([]);
          setShowingStale(false);
          setStatus("error");
          setLoadError("library.unreachable");
        }
      });

    return () => ac.abort();
  }, [includeDrafts, retryToken]);

  useEffect(() => {
    setCollection(searchParams.get("collection") || "all");
    setTheme(searchParams.get("theme") || "all");
  }, [searchParams]);

  const collections = useMemo(() => uniqueCollections(items), [items]);
  const collectionOptions = useMemo(() => buildCollectionOptions(items, collections), [collections, items]);
  const themeConstellation = useMemo(() => topThemes(items, 16), [items]);

  const tomes = useMemo(() => {
    const all = buildLibraryTomes(items);
    const themed =
      theme === "all"
        ? all
        : all.filter((tome) =>
            items.some(
              (item) =>
                collectionsMatch(item.collection, tome.collection) && (item.themes || []).includes(theme),
            ),
          );
    return sortTomes(themed, librarySort);
  }, [items, theme, librarySort]);

  const shelves = useMemo(
    () => (librarySort === "tradition" ? groupTomesByTradition(tomes) : null),
    [tomes, librarySort],
  );

  const filtered = useMemo(
    () =>
      sortPassagesForLibrary(
        filterPassages(items, {
          q,
          collection,
          theme,
          blob: (x) =>
            [x.title, x.sutra_id, x.reference, patanjaliSutraRef(x), layerText(x, "translation"), layerText(x, "commentary"), x.collection].join(" "),
        }),
      ),
    [items, q, collection, theme],
  );
  const showShelf = collection === "all" && !q.trim();
  const studyList = useLocalizedVerseCards(showShelf ? [] : filtered, 40);
  const hasItems = items.length > 0;
  const isBooting = (status === "loading" || status === "waking") && !hasItems;
  const isHardError = status === "error" && !hasItems;
  const isTrueEmpty = status === "ready" && !hasItems && !loadError;

  function retryCatalog() {
    setRetryToken((n) => n + 1);
  }

  function syncReadUrl(next: { collection?: string; theme?: string }) {
    const params = new URLSearchParams(searchParams.toString());
    const coll = next.collection ?? collection;
    const th = next.theme ?? theme;
    if (coll === "all") params.delete("collection");
    else params.set("collection", coll);
    if (th === "all") params.delete("theme");
    else params.set("theme", th);
    router.replace(`/read${params.toString() ? `?${params.toString()}` : ""}`);
  }

  function openTome(value: string) {
    setCollection(value);
    setQ("");
    syncReadUrl({ collection: value });
    if (typeof window !== "undefined") window.scrollTo({ top: 0, behavior: "auto" });
  }

  const headerArtPool =
    collection !== "all" ? collectionArtPool(collection) : generatedArtPool("bg-library");
  const openTomeMeta =
    collection !== "all" ? tomes.find((t) => collectionsMatch(t.collection, collection)) : null;
  const openTomeRb = collection !== "all" ? redbookSlug(collection) : null;
  const fallbackQuoteKey = useMemo(() => {
    if (collection === "all") return "";
    return catalogQuoteCandidates(
      filtered.map((x) => firstSentence(layerText(x, "translation") || layerText(x, "original") || "")),
    ).join("\0");
  }, [collection, filtered]);
  const fallbackQuotes = useMemo(
    () => (fallbackQuoteKey ? fallbackQuoteKey.split("\0") : []),
    [fallbackQuoteKey],
  );

  return (
    <LayoutGroup>
    <main className="page-shell page-shell--library">
      <header className="library-header">
        <div className="library-header__atmosphere" aria-hidden>
          {collection !== "all" && openTomeRb ? (
            <div
              className="library-header__flown"
              style={{ backgroundImage: `url(${redbookSrc(openTomeRb)})` }}
            />
          ) : (
            <ArtBackdrop srcs={headerArtPool} variant="subtle" opacity={0.12} priority={collection !== "all"} />
          )}
        </div>
        <div className="library-header__body">
          {collection !== "all" ? (
            <button
              type="button"
              onClick={() => openTome("all")}
              className="passage-reading__toggle"
            >
              ← {t("library.allTexts")}
            </button>
          ) : (
            <p className="passage-reading__meta">{t("library.meta")}</p>
          )}
          {collection !== "all" ? (
            <CollectionGate
              collection={collection}
              title={displayCollectionName(collection)}
              mandalaSrc={openTomeRb ? redbookSrc(openTomeRb) : null}
              layoutId={openTomeRb ? `tome-${collection}` : undefined}
              fallbackQuotes={fallbackQuotes}
              glyph={
                <InkGlyph
                  glyph={openTomeMeta?.glyph || sumiGlyph(collection, openTomeMeta?.tradition)}
                  state="arising"
                  size="xl"
                  mask
                />
              }
            />
          ) : null}
          <div id="collection-text" className="mt-2 flex items-start gap-3">
            {collection !== "all" ? (
              <span className="library-row__glyph mt-1 hidden sm:inline-flex" aria-hidden>
                <InkGlyph
                  glyph={openTomeMeta?.glyph || sumiGlyph(collection, openTomeMeta?.tradition)}
                  state="arising"
                  size="md"
                  mask
                />
              </span>
            ) : null}
            <div className="min-w-0">
              <h1 className="library-header__title">
                {collection !== "all" ? displayCollectionName(collection) : t("library.title")}
              </h1>
              <p className="library-header__lede">
                {collection !== "all"
                  ? t("library.collectionLede", { count: openTomeMeta?.count ?? filtered.length })
                  : t("library.lede")}
              </p>
            </div>
          </div>
        </div>
      </header>

      <div className="section-stack section-stack--tight mt-6">
        <div>
          <div className="library-toolbar">
            <label className="block min-w-0">
              <p className="layer-heading mb-2">{t("library.search")}</p>
              <Input
                value={q}
                onChange={(e) => setQ(e.target.value)}
                className="w-full"
                placeholder={showShelf ? t("library.searchAll") : t("library.searchInText")}
              />
            </label>
            {!showShelf ? (
              <FilterSelect
                label={t("library.text")}
                tone="gold"
                value={collection}
                onChange={(next) => {
                  setCollection(next);
                  syncReadUrl({ collection: next });
                }}
                options={collectionOptions}
              />
            ) : (
              <FilterSelect
                label={t("library.sortLabel")}
                tone="gold"
                value={librarySort}
                onChange={(next) => setLibrarySort(next as LibrarySort)}
                options={LIBRARY_SORT_OPTIONS.map((option) => ({
                  ...option,
                  label: t(`library.sort.${option.value}`),
                  hint: t(`library.sortHint.${option.value}`),
                }))}
              />
            )}
          </div>

          <div className="mt-6">
            <ThemeConstellation
              themes={themeConstellation}
              active={theme}
              onChange={(next) => {
                setTheme(next);
                syncReadUrl({ theme: next });
              }}
            />
          </div>

          <div className="mt-3">
            <Disclosure summary={t("library.displayOptions")} hint={includeDrafts ? t("library.draftsOn") : undefined}>
              {!showShelf ? (
                <label className="flex items-center gap-2 font-sans text-sm soft">
                  <input type="checkbox" className="accent-amber-300" checked={learningMode} onChange={(e) => setLearningMode(e.target.checked)} />
                  {t("library.learningMode")}
                </label>
              ) : null}
              <label className={`flex items-center gap-2 font-sans text-sm soft${!showShelf ? " mt-3" : ""}`}>
                <input type="checkbox" className="accent-amber-300" checked={includeDrafts} onChange={(e) => setIncludeDrafts(e.target.checked)} />
                {t("library.includeDrafts")}
              </label>
            </Disclosure>
          </div>

          {isBooting ? (
            <div className="mt-4 rounded-2xl border border-amber-300/30 bg-amber-300/10 p-4 font-sans text-sm text-amber-100">
              <p className="font-medium">
                {status === "waking" ? t("library.waking") : t("library.opening")}
              </p>
              <p className="mt-2 soft text-amber-100/80">
                {t("library.wakingLede")}
              </p>
            </div>
          ) : null}

          {isHardError ? (
            <div className="mt-4 rounded-2xl border border-amber-300/30 bg-amber-300/10 p-4 font-sans text-sm text-amber-100">
              <p>{t(loadError)}</p>
              <button
                type="button"
                onClick={retryCatalog}
                className="mt-3 rounded-full border border-amber-200/40 px-4 py-2 font-sans text-xs tracking-wide text-amber-50 transition hover:border-amber-100/70 hover:bg-amber-300/10"
              >
                {t("common.retry")}
              </button>
            </div>
          ) : null}

          {showingStale && hasItems && loadError ? (
            <div className="mt-4 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-4 font-sans text-sm text-amber-100/90">
              <p>{t(loadError)}</p>
              <button
                type="button"
                onClick={retryCatalog}
                className="shrink-0 rounded-full border border-amber-200/40 px-4 py-2 font-sans text-xs tracking-wide text-amber-50 transition hover:border-amber-100/70 hover:bg-amber-300/10"
              >
                {t("common.retry")}
              </button>
            </div>
          ) : null}
        </div>

      {isBooting || isHardError ? null : showShelf ? (
        <div className="space-y-10">
          {isTrueEmpty ? (
            <p className="soft mt-2">
              {t("library.emptyCatalog")}
            </p>
          ) : (
            <>
              <p className="soft font-sans text-sm">
                {t("library.textsPassages", { texts: tomes.length, passages: items.length })}
                {showingStale && loadError ? ` · ${t("library.savedCatalog")}` : ""}
                {librarySort === "author"
                  ? ` · ${t("library.sortedByAuthor")}`
                  : librarySort === "tradition"
                    ? ` · ${t("library.groupedByTradition")}`
                    : ` · ${t("library.sortedByTitle")}`}
              </p>
              {shelves ? (
                shelves.map((shelf) => (
                  <section key={shelf.tradition}>
                    <div className="mb-4 flex items-baseline justify-between gap-3">
                      <h2 className="layer-heading text-amber-100/90">{shelf.tradition}</h2>
                      <p className="soft font-sans text-xs">
                        {shelf.tomes.length} {shelf.tomes.length === 1 ? "text" : "texts"}
                      </p>
                    </div>
                    <div className="tome-shelf">
                      {shelf.tomes.map((tome) => (
                        <TomeCard key={tome.collection} tome={tome} onOpen={() => openTome(tome.collection)} />
                      ))}
                    </div>
                  </section>
                ))
              ) : (
                <div className="tome-shelf">
                  {tomes.map((tome) => (
                    <TomeCard key={tome.collection} tome={tome} onOpen={() => openTome(tome.collection)} />
                  ))}
                </div>
              )}

              {tomes.length === 0 ? (
                <p className="soft mt-6">No texts match this theme yet. Clear the theme filter to see the full shelf.</p>
              ) : null}
            </>
          )}
        </div>
      ) : (
        <div className="library-list">
          {studyList.slice(0, 300).map((x) => (
            <div key={x._id} className="library-passage library-passage--listen group">
              <Link href={`/read/${encodeURIComponent(x._id)}`} className="library-passage__open">
                <div className="library-passage__top">
                  <span className="library-row__glyph hidden sm:inline-flex" aria-hidden>
                    <InkGlyph
                      glyph={verseSumiGlyph({
                        collection: x.collection,
                        tradition: tomes.find((t) => collectionsMatch(t.collection, x.collection || ""))?.tradition,
                        title: x.title,
                        thesis: x.thesis,
                        translation: x.translation,
                        themes: x.themes,
                      })}
                      state="arising"
                      size="sm"
                      mask
                    />
                  </span>
                  <div className="min-w-0 flex-1">
                    <h2 className="library-passage__title">{displayPassageTitle(x)}</h2>
                    <p className="library-passage__meta">
                      {displayCollectionName(x.collection)}
                      {displayPassageLocation(x) ? ` · ${displayPassageLocation(x)}` : ""}
                    </p>
                    {x.themes && x.themes.length > 0 ? (
                      <p className="library-passage__themes">{x.themes.slice(0, 2).join(" · ")}</p>
                    ) : null}
                  </div>
                </div>
                {!learningMode ? (
                  <p className="library-passage__preview line-clamp-2">
                    {passagePreview(x) || t("library.openPassage")}
                  </p>
                ) : (
                  <div className="library-passage__learning">
                    <p className="line-clamp-2">
                      <span>{t("library.coreIdea")}</span> {passagePreview(x) || t("library.openPassage")}
                    </p>
                    <p className="line-clamp-2">
                      <span>{t("library.whyItMatters")}</span>{" "}
                      {firstSentence(layerText(x, "commentary") || layerText(x, "translation") || "")}
                    </p>
                    <p className="line-clamp-2">
                      <span>{t("common.practice")}</span> {practiceText(x) || reflectionPrompt(x, t)}
                    </p>
                  </div>
                )}
              </Link>
              <ListenButton verseId={x._id} variant="header" />
            </div>
          ))}
          {filtered.length === 0 ? (
            <p className="soft mt-6">{t("library.noMatchTry")}</p>
          ) : null}
        </div>
      )}
      </div>
    </main>
    </LayoutGroup>
  );
}

export default function ReadPage() {
  const t = useT();
  return (
    <Suspense fallback={<main className="page-shell page-shell--library soft">{t("library.opening")}</main>}>
      <LibraryPageContent />
    </Suspense>
  );
}
