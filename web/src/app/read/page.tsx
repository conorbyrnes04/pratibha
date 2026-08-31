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
import { catalogQuoteCandidates } from "@/lib/heroQuotes";

/** Library catalog lifecycle — never treat cold/fail as a true empty shelf. */
type LibraryStatus = "loading" | "waking" | "ready" | "error";

function reflectionPrompt(item: VerseItem): string {
  const t = (item.themes || [])[0];
  if (t) return `Where do you notice "${t}" in direct experience today?`;
  return "What one shift in seeing does this passage invite right now?";
}

// Shared-element flight timing — the tome's Red Book mandala morphs from the
// shelf emblem into the reading header backdrop and back.
const TOME_FLIGHT = { type: "spring", stiffness: 260, damping: 32, mass: 0.9 } as const;

function TomeCard({ tome, onOpen }: { tome: LibraryTome; onOpen: () => void }) {
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
          {tome.count} {tome.count === 1 ? "passage" : "passages"} · {tome.authored}
        </span>
      </span>
    </button>
  );
}

function LibraryPageContent() {
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
          setLoadError(
            "Couldn’t refresh the library — showing a saved catalog. Retry when the API is awake.",
          );
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
          setLoadError(
            "Couldn’t refresh the library — showing a saved catalog. Retry when the API is awake.",
          );
        } else {
          setItems([]);
          setShowingStale(false);
          setStatus("error");
          setLoadError(
            "The library API is waking up or unreachable. This is not an empty corpus — wait a moment and try again.",
          );
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

  // Shelf of tomes when browsing the whole library; passage list once a text is open or search is active.
  const showShelf = collection === "all" && !q.trim();
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
  const fallbackQuotes = useMemo(() => {
    if (collection === "all") return [];
    return catalogQuoteCandidates(
      filtered.map((x) => firstSentence(layerText(x, "translation") || layerText(x, "original") || "")),
    );
  }, [collection, filtered]);

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
              ← All texts
            </button>
          ) : (
            <p className="passage-reading__meta">Archive</p>
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
                {collection !== "all" ? displayCollectionName(collection) : "Library"}
              </h1>
              <p className="library-header__lede">
                {collection !== "all"
                  ? `${openTomeMeta?.count ?? filtered.length} passages · open a page, then follow related ideas across traditions.`
                  : "Texts grouped by tradition. Open a tome, then follow resonances across the shelf."}
              </p>
            </div>
          </div>
        </div>
      </header>

      <div className="section-stack section-stack--tight mt-6">
        <div>
          <div className="library-toolbar">
            <label className="block min-w-0">
              <p className="layer-heading mb-2">Search</p>
              <Input
                value={q}
                onChange={(e) => setQ(e.target.value)}
                className="w-full"
                placeholder={showShelf ? "Search across all texts..." : "Search passages in this text..."}
              />
            </label>
            {!showShelf ? (
              <FilterSelect
                label="Text"
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
                label="Sort"
                tone="gold"
                value={librarySort}
                onChange={(next) => setLibrarySort(next as LibrarySort)}
                options={LIBRARY_SORT_OPTIONS}
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
            <Disclosure summary="Display options" hint={includeDrafts ? "drafts on" : undefined}>
              {!showShelf ? (
                <label className="flex items-center gap-2 font-sans text-sm soft">
                  <input type="checkbox" className="accent-amber-300" checked={learningMode} onChange={(e) => setLearningMode(e.target.checked)} />
                  Learning mode previews (core idea · why it matters · practice)
                </label>
              ) : null}
              <label className={`flex items-center gap-2 font-sans text-sm soft${!showShelf ? " mt-3" : ""}`}>
                <input type="checkbox" className="accent-amber-300" checked={includeDrafts} onChange={(e) => setIncludeDrafts(e.target.checked)} />
                Include rewrite and structural drafts
              </label>
            </Disclosure>
          </div>

          {isBooting ? (
            <div className="mt-4 rounded-2xl border border-amber-300/30 bg-amber-300/10 p-4 font-sans text-sm text-amber-100">
              <p className="font-medium">
                {status === "waking" ? "Waking the library…" : "Opening the library…"}
              </p>
              <p className="mt-2 soft text-amber-100/80">
                The API may be cold-starting. This is not an empty shelf — passages will appear when the catalog is ready.
              </p>
            </div>
          ) : null}

          {isHardError ? (
            <div className="mt-4 rounded-2xl border border-amber-300/30 bg-amber-300/10 p-4 font-sans text-sm text-amber-100">
              <p>{loadError}</p>
              <button
                type="button"
                onClick={retryCatalog}
                className="mt-3 rounded-full border border-amber-200/40 px-4 py-2 font-sans text-xs tracking-wide text-amber-50 transition hover:border-amber-100/70 hover:bg-amber-300/10"
              >
                Retry
              </button>
            </div>
          ) : null}

          {showingStale && hasItems && loadError ? (
            <div className="mt-4 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-amber-300/20 bg-amber-300/5 p-4 font-sans text-sm text-amber-100/90">
              <p>{loadError}</p>
              <button
                type="button"
                onClick={retryCatalog}
                className="shrink-0 rounded-full border border-amber-200/40 px-4 py-2 font-sans text-xs tracking-wide text-amber-50 transition hover:border-amber-100/70 hover:bg-amber-300/10"
              >
                Retry
              </button>
            </div>
          ) : null}
        </div>

      {isBooting || isHardError ? null : showShelf ? (
        <div className="space-y-10">
          {isTrueEmpty ? (
            <p className="soft mt-2">
              The catalog loaded successfully but has no passages yet. If you expected texts here, check that the
              backend corpus finished loading.
            </p>
          ) : (
            <>
              <p className="soft font-sans text-sm">
                {tomes.length} texts · {items.length} passages
                {showingStale && loadError ? " · saved catalog" : ""}
                {librarySort === "author"
                  ? " · sorted by author"
                  : librarySort === "tradition"
                    ? " · grouped by tradition"
                    : " · sorted by title"}
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
          {filtered.slice(0, 300).map((x) => (
            <Link
              key={x._id}
              href={`/read/${encodeURIComponent(x._id)}`}
              className="library-passage group"
            >
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
                  {passagePreview(x) || "Open to view passage."}
                </p>
              ) : (
                <div className="library-passage__learning">
                  <p className="line-clamp-2">
                    <span>Core idea</span> {passagePreview(x) || "Open to view passage."}
                  </p>
                  <p className="line-clamp-2">
                    <span>Why it matters</span>{" "}
                    {firstSentence(layerText(x, "commentary") || layerText(x, "translation") || "")}
                  </p>
                  <p className="line-clamp-2">
                    <span>Practice</span> {practiceText(x) || reflectionPrompt(x)}
                  </p>
                </div>
              )}
            </Link>
          ))}
          {filtered.length === 0 ? (
            <p className="soft mt-6">No passages match. Try another search, or return to the shelf.</p>
          ) : null}
        </div>
      )}
      </div>
    </main>
    </LayoutGroup>
  );
}

export default function ReadPage() {
  return (
    <Suspense fallback={<main className="page-shell page-shell--library soft">Opening the library...</main>}>
      <LibraryPageContent />
    </Suspense>
  );
}
