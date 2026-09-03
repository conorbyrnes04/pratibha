'use client';

import Link from "next/link";
import { useEffect, useState } from "react";
import { getCollections, getRandom, getVerses } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { FilterSelect } from "@/components/FilterSelect";
import { buildCollectionOptions, isReaderFacingUnit } from "@/lib/corpusFilters";
import { displayCollectionName } from "@/lib/collectionLabels";
import { collectionArtPool, generatedArtPool } from "@/lib/collectionImages";
import { displayPassageLocation, displayPassageTitle } from "@/lib/passageTitles";
import { LayerBlock } from "@/components/LayerBlock";
import { ArtBackdrop } from "@/components/ArtImage";
import { getVerseLayers } from "@/lib/verseLayers";
import { recordPractice } from "@/lib/glyphUnlock";
import { Button, buttonVariants } from "@/components/ui/button";
import { useT } from "@/components/LocaleProvider";
import { useLocalizedVerse } from "@/components/useLocalizedStudy";

export default function RandomPage() {
  const t = useT();
  const [item, setItem] = useState<VerseItem | null>(null);
  const [collection, setCollection] = useState("all");
  const [collections, setCollections] = useState<string[]>(["all"]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [allItems, setAllItems] = useState<VerseItem[]>([]);
  const study = useLocalizedVerse(item);

  useEffect(() => {
    getCollections()
      .then((names) => {
        if (names.length > 0) {
          setCollections(["all", ...names.slice().sort((a, b) => a.localeCompare(b))]);
        }
      })
      .catch(() => {});
  }, []);

  async function nextOne(selected: string, pool: VerseItem[] = allItems) {
    setLoading(true);
    setError("");
    try {
      const c = selected === "all" ? undefined : selected;
      const v = await getRandom(c, "strong_draft");
      if (v) {
        setItem(v);
        recordPractice("oracle:draw");
        return;
      }
      const local = pool.filter(
        (x) =>
          isReaderFacingUnit(x) &&
          (selected === "all" || (x.collection || "Unknown").trim() === selected),
      );
      if (local.length > 0) {
        setItem(local[Math.floor(Math.random() * local.length)]);
        recordPractice("oracle:draw");
        return;
      }
      if (pool.length === 0) {
        // Local catalog still loading — keep the spinner; the allItems effect retries.
        setItem(null);
        return;
      }
      setItem(null);
      setError("No passages are available for this selection yet.");
    } catch {
      setItem(null);
      setError("Random discovery is temporarily unavailable. Please retry.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    let cancelled = false;
    async function firstDraw() {
      setLoading(true);
      const [v, verses] = await Promise.all([
        getRandom(undefined, "strong_draft"),
        getVerses("strong_draft").catch(() => [] as VerseItem[]),
      ]);
      if (cancelled) return;
      setAllItems(verses);
      if (v) {
        setItem(v);
        recordPractice("oracle:draw");
        setLoading(false);
        return;
      }
      const pool = verses.filter(isReaderFacingUnit);
      if (pool.length > 0) {
        setItem(pool[Math.floor(Math.random() * pool.length)]);
        recordPractice("oracle:draw");
        setLoading(false);
        return;
      }
      setItem(null);
      setError("Random discovery is temporarily unavailable. Please retry.");
      setLoading(false);
    }
    void firstDraw();
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    // If the first draw raced ahead of the local library and fell through to an
    // empty pool, retry once the library finishes loading.
    if (allItems.length > 0 && !item && !loading && !error) {
      void nextOne(collection, allItems);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [allItems]);

  const artSrcs = item ? collectionArtPool(item.collection) : generatedArtPool("default");

  return (
    <main className="page-shell page-shell--library">
      <div className="section-stack">
        <header className="library-header">
          <div className="library-header__atmosphere" aria-hidden>
            <ArtBackdrop srcs={artSrcs} variant="subtle" opacity={0.12} priority />
          </div>
          <div className="library-header__body">
            <p className="passage-reading__meta">{t("oracle.meta")}</p>
            <h1 className="library-header__title">{t("oracle.title")}</h1>
            <p className="library-header__lede">{t("oracle.deck")}</p>
          </div>
        </header>

        <div className="library-toolbar">
          <FilterSelect
            label={t("oracle.text")}
            tone="gold"
            value={collection}
            onChange={(value) => {
              setCollection(value);
              void nextOne(value);
            }}
            options={buildCollectionOptions(allItems, collections)}
          />
          <div className="flex items-end">
            <Button type="button" className="w-full sm:w-auto" onClick={() => nextOne(collection)}>
              Another one
            </Button>
          </div>
        </div>

        {loading ? (
          <p className="soft">Finding a passage…</p>
        ) : error ? (
          <section>
            <p className="text-amber-100">{error}</p>
            <div className="mt-4">
              <Button type="button" onClick={() => nextOne(collection)}>
                Retry
              </Button>
            </div>
          </section>
        ) : item ? (
          <article className="oracle-folio">
            <header className="passage-reading__header" style={{ paddingBottom: "1.25rem" }}>
              <p className="passage-reading__meta">
                {displayCollectionName(item.collection)}
                {displayPassageLocation(item) ? ` · ${displayPassageLocation(item)}` : ""}
              </p>
              <h2 className="passage-reading__title">{displayPassageTitle(study || item)}</h2>
            </header>

            {getVerseLayers(study || item)
              .filter((layer) => ["original", "iast", "translation", "commentary", "practice"].includes(layer.kind))
              .map((layer, idx) => (
                <LayerBlock
                  key={`${layer.kind}-${idx}`}
                  layer={layer}
                  variant="plain"
                  compact={layer.kind !== "translation" && layer.kind !== "practice"}
                />
              ))}

            {item.themes && item.themes.length > 0 ? (
              <p className="library-passage__themes mt-4">
                {item.themes.slice(0, 6).join(" · ")}
              </p>
            ) : null}

            <div className="passage-reading__nav">
              <Link
                href={`/read/${encodeURIComponent(item._id)}`}
                className={buttonVariants()}
              >
                Open full page
              </Link>
              <Link
                href={`/chat?verse_id=${encodeURIComponent(item._id)}&mode=explain`}
                className={buttonVariants({ variant: "secondary" })}
              >
                Study this passage
              </Link>
              <Link href="/read" className={buttonVariants({ variant: "ghost" })}>
                Library
              </Link>
            </div>
          </article>
        ) : (
          <p className="soft">
            No random passage available yet. Try Library to pick one directly.
          </p>
        )}
      </div>
    </main>
  );
}
