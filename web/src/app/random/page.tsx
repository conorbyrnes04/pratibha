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
import { ReadingShell } from "@/components/ReadingShell";
import { getVerseLayers } from "@/lib/verseLayers";
import { Button, buttonVariants } from "@/components/ui/button";

export default function RandomPage() {
  const [item, setItem] = useState<VerseItem | null>(null);
  const [collection, setCollection] = useState("all");
  const [collections, setCollections] = useState<string[]>(["all"]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [allItems, setAllItems] = useState<VerseItem[]>([]);

  useEffect(() => {
    getCollections()
      .then((names) => {
        if (names.length > 0) {
          setCollections(["all", ...names.slice().sort((a, b) => a.localeCompare(b))]);
        }
      })
      .catch(() => {});
    // Load the library only for the local fallback pool; collection list comes
    // from the dedicated endpoint above.
    getVerses("strong_draft")
      .then(setAllItems)
      .catch(() => {});
  }, []);

  async function nextOne(selected: string) {
    setLoading(true);
    setError("");
    try {
      const c = selected === "all" ? undefined : selected;
      const v = await getRandom(c, "strong_draft");
      if (v) {
        setItem(v);
        return;
      }
      // Fallback: pick locally from the already loaded library if /random returns empty.
      const pool = allItems.filter(
        (x) =>
          isReaderFacingUnit(x) &&
          (selected === "all" || (x.collection || "Unknown").trim() === selected),
      );
      if (pool.length > 0) {
        setItem(pool[Math.floor(Math.random() * pool.length)]);
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
    void nextOne("all");
    // Pick the first passage exactly once on mount.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const artSrcs = item ? collectionArtPool(item.collection) : generatedArtPool("default");

  return (
    <main className="page-shell page-shell--reading">
      <ReadingShell artSrcs={artSrcs}>
        <nav className="passage-reading__crumb" aria-label="Breadcrumb">
          <Link href="/">Today</Link>
          <span className="passage-reading__crumb-sep" aria-hidden>
            /
          </span>
          <span>Oracle</span>
        </nav>

        <header className="passage-reading__header">
          <p className="passage-reading__meta">Oracle</p>
          <h1 className="passage-reading__title">Random Discovery</h1>
          <p className="passage-reading__deck">Let the text choose you, then dive deeper.</p>
        </header>

        <div className="mt-2 flex max-w-[var(--reading-measure)] flex-wrap items-end gap-3">
          <div className="min-w-[min(100%,16rem)] flex-1">
            <FilterSelect
              label="Text"
              tone="gold"
              value={collection}
              onChange={(value) => {
                setCollection(value);
                void nextOne(value);
              }}
              options={buildCollectionOptions(allItems, collections)}
            />
          </div>
          <Button type="button" onClick={() => nextOne(collection)}>
            Another one
          </Button>
        </div>

        {loading ? (
          <p className="soft mt-8 max-w-[var(--reading-measure)]">Finding a passage…</p>
        ) : error ? (
          <section className="mt-8 max-w-[var(--reading-measure)]">
            <p className="text-amber-100">{error}</p>
            <div className="mt-4">
              <Button type="button" onClick={() => nextOne(collection)}>
                Retry
              </Button>
            </div>
          </section>
        ) : item ? (
          <article className="mt-10">
            <header className="passage-reading__header" style={{ paddingBottom: "1.25rem" }}>
              <p className="passage-reading__meta">
                {displayCollectionName(item.collection)}
                {displayPassageLocation(item) ? ` · ${displayPassageLocation(item)}` : ""}
              </p>
              <h2 className="passage-reading__title">{displayPassageTitle(item)}</h2>
            </header>

            {getVerseLayers(item)
              .filter((layer) => ["original", "iast", "translation", "practice"].includes(layer.kind))
              .map((layer, idx) => (
                <LayerBlock
                  key={`${layer.kind}-${idx}`}
                  layer={layer}
                  variant="plain"
                  compact={layer.kind !== "translation" && layer.kind !== "practice"}
                />
              ))}

            {item.themes && item.themes.length > 0 ? (
              <p className="library-passage__themes mt-4 max-w-[var(--reading-measure)]">
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
          <p className="soft mt-8 max-w-[var(--reading-measure)]">
            No random passage available yet. Try Library to pick one directly.
          </p>
        )}
      </ReadingShell>
    </main>
  );
}
