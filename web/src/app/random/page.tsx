'use client';

import Link from "next/link";
import { useEffect, useState } from "react";
import { getCollections, getRandom, getVerses } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { FilterSelect } from "@/components/FilterSelect";
import { buildCollectionOptions, isReaderFacingUnit } from "@/lib/corpusFilters";
import { displayCollectionName } from "@/lib/collectionLabels";
import { collectionArtPool, collectionImageSrc, generatedArtPool } from "@/lib/collectionImages";
import { ArtBackdrop } from "@/components/ArtImage";
import { displayPassageTitle } from "@/lib/passageTitles";
import { LayerBlock } from "@/components/LayerBlock";
import { getVerseLayers } from "@/lib/verseLayers";

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

  return (
    <main className="page-shell max-w-4xl">
      <section className="manuscript-card relative overflow-hidden p-5 sm:p-6">
        <ArtBackdrop
          srcs={item ? collectionArtPool(item.collection) : generatedArtPool("default")}
          variant="banner"
        />
        <div className="relative z-10">
          <p className="eyebrow">Oracle</p>
          <h1 className="mt-3 text-5xl font-semibold leading-none tracking-[-0.04em] text-stone-100 sm:text-6xl">Random Discovery</h1>
          <p className="soft mt-4 text-xl">Let the text choose you, then dive deeper.</p>
        </div>
      </section>

      <div className="mt-6 flex flex-wrap items-end gap-3">
        <div className="min-w-[min(100%,18rem)] flex-1">
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
        <button onClick={() => nextOne(collection)} className="btn-primary px-5 py-2.5">
          Another one
        </button>
        <Link href="/" className="btn-secondary px-5 py-2.5">
          Home
        </Link>
        <Link href="/read" className="btn-secondary px-5 py-2.5">
          Library
        </Link>
      </div>

      {loading ? (
        <p className="soft mt-6">Finding a passage...</p>
      ) : error ? (
        <section className="card mt-6 p-5">
          <p className="text-amber-100">{error}</p>
          <div className="mt-4">
            <button onClick={() => nextOne(collection)} className="btn-primary px-5 py-2.5">
              Retry
            </button>
          </div>
        </section>
      ) : item ? (
        <section className="manuscript-card relative mt-8 overflow-hidden p-6 sm:p-8">
          <ArtBackdrop srcs={collectionArtPool(item.collection)} variant="hero" />
          <div className="relative z-10">
            <h2 className="text-3xl leading-none text-amber-100">{displayPassageTitle(item)}</h2>
            <p className="soft mt-1 text-sm">
              {displayCollectionName(item.collection)} {item.section ? `• ${item.section}` : ""}
            </p>
            {getVerseLayers(item)
              .filter((layer) => ["original", "iast", "translation", "practice"].includes(layer.kind))
              .map((layer, idx) => (
                <LayerBlock key={`${layer.kind}-${idx}`} layer={layer} compact />
              ))}
            {item.themes && item.themes.length > 0 ? (
              <div className="mt-4 flex flex-wrap gap-2">
                {item.themes.slice(0, 6).map((t) => (
                  <span key={t} className="rounded-full border border-amber-200/30 px-3 py-1 font-sans text-xs text-amber-100">
                    {t}
                  </span>
                ))}
              </div>
            ) : null}
            <div className="mt-5 flex flex-wrap gap-3">
              <Link href={`/read/${encodeURIComponent(item._id)}`} className="btn-primary px-5 py-2.5">
                Open full page
              </Link>
              <Link
                href={`/chat?verse_id=${encodeURIComponent(item._id)}&mode=explain`}
                className="btn-secondary px-5 py-2.5"
              >
                Study this passage
              </Link>
            </div>
          </div>
        </section>
      ) : (
        <p className="soft mt-6">No random passage available yet. Try Library to pick one directly.</p>
      )}
    </main>
  );
}

