'use client';

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useMemo, useState } from "react";
import { getVerses } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { firstSentence } from "@/lib/textPreview";
import { FilterSelect } from "@/components/FilterSelect";
import { ThemeConstellation } from "@/components/ThemeConstellation";
import { buildCollectionOptions, filterPassages, topThemes, uniqueCollections } from "@/lib/corpusFilters";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageTitle, patanjaliSutraRef, sortPassagesForLibrary } from "@/lib/passageTitles";
import { layerText, maturityLabel, passagePreview, practiceText } from "@/lib/verseLayers";

function reflectionPrompt(item: VerseItem): string {
  const t = (item.themes || [])[0];
  if (t) return `Where do you notice "${t}" in direct experience today?`;
  return "What one shift in seeing does this passage invite right now?";
}

function ReadPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [items, setItems] = useState<VerseItem[]>([]);
  const [q, setQ] = useState("");
  const [collection, setCollection] = useState(searchParams.get("collection") || "all");
  const [theme, setTheme] = useState(searchParams.get("theme") || "all");
  const [learningMode, setLearningMode] = useState(true);
  const [includeDrafts, setIncludeDrafts] = useState(false);

  useEffect(() => {
    getVerses(includeDrafts ? "all" : "strong_draft").then(setItems).catch(() => setItems([]));
  }, [includeDrafts]);

  useEffect(() => {
    setCollection(searchParams.get("collection") || "all");
    setTheme(searchParams.get("theme") || "all");
  }, [searchParams]);

  const collections = useMemo(() => uniqueCollections(items), [items]);
  const collectionOptions = useMemo(() => buildCollectionOptions(items, collections), [collections, items]);
  const themeConstellation = useMemo(() => topThemes(items, 16), [items]);

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

  return (
    <main className="page-shell">
      <p className="eyebrow">Archive</p>
      <h1 className="mt-3 text-5xl font-semibold leading-none tracking-[-0.04em] text-stone-100 sm:text-6xl">Library</h1>
      <p className="soft mt-4 max-w-2xl text-xl leading-relaxed">Move idea-to-idea: choose a collection, follow a theme thread, open a passage, then trace related concepts.</p>

      <div className="mt-6 grid gap-4 lg:grid-cols-[2fr_1fr]">
        <label className="block">
          <p className="layer-heading mb-2">Search</p>
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            className="input-field w-full rounded-[18px] px-4 py-3"
            placeholder="Search passages, titles, themes..."
          />
        </label>
        <FilterSelect
          label="Collection"
          tone="gold"
          value={collection}
          onChange={(next) => {
            setCollection(next);
            syncReadUrl({ collection: next });
          }}
          options={collectionOptions}
        />
      </div>

      <div className="mt-5">
        <ThemeConstellation
          themes={themeConstellation}
          active={theme}
          onChange={(next) => {
            setTheme(next);
            syncReadUrl({ theme: next });
          }}
        />
      </div>

      <label className="mt-4 block font-sans text-sm soft">
        <input type="checkbox" className="mr-2 accent-amber-300" checked={learningMode} onChange={(e) => setLearningMode(e.target.checked)} />
        Learning mode previews
      </label>
      <label className="mt-2 block font-sans text-sm soft">
        <input type="checkbox" className="mr-2 accent-amber-300" checked={includeDrafts} onChange={(e) => setIncludeDrafts(e.target.checked)} />
        Include rewrite and structural drafts
      </label>

      <div className="mt-6 space-y-3">
        {filtered.slice(0, 300).map((x) => (
          <Link key={x._id} href={`/read/${encodeURIComponent(x._id)}`} className="card group block p-5 transition hover:-translate-y-0.5 hover:border-amber-300/30">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-2xl leading-none text-amber-100">{displayPassageTitle(x)}</h2>
                <p className="soft text-sm">{displayCollectionName(x.collection)} {x.section ? `• ${x.section}` : ""}</p>
              </div>
              {x.themes && x.themes.length > 0 ? (
                <div className="flex flex-wrap justify-end gap-2">
                  <span className="rounded-full border border-amber-200/30 px-2 py-1 font-sans text-xs text-amber-100">
                    {x.themes.slice(0, 2).join(" · ")}
                  </span>
                  <span className="rounded-full border border-white/15 px-2 py-1 font-sans text-xs text-stone-300">
                    {maturityLabel(x.editorial_maturity)}
                  </span>
                </div>
              ) : null}
            </div>
            {!learningMode ? (
              <p className="soft mt-3 line-clamp-2 text-sm">{passagePreview(x) || "Open to view passage."}</p>
            ) : (
              <div className="soft mt-4 space-y-2 text-sm">
                <p className="line-clamp-2">
                  <span className="text-amber-100">Core idea:</span> {passagePreview(x) || "Open to view passage."}
                </p>
                <p className="line-clamp-2">
                  <span className="text-amber-100">Why it matters:</span> {firstSentence(layerText(x, "commentary") || layerText(x, "translation") || "")}
                </p>
                <p className="line-clamp-2">
                  <span className="text-amber-100">Practice:</span> {practiceText(x) || reflectionPrompt(x)}
                </p>
              </div>
            )}
          </Link>
        ))}
      </div>
    </main>
  );
}

export default function ReadPage() {
  return (
    <Suspense fallback={<main className="page-shell soft">Opening the archive...</main>}>
      <ReadPageContent />
    </Suspense>
  );
}
