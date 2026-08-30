'use client';

import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { Suspense, useEffect, useMemo, useState } from "react";
import { getVerses } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { firstSentence, stripMarkdown } from "@/lib/textPreview";
import { displayCollectionName } from "@/lib/collectionLabels";

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
  const [collection, setCollection] = useState("all");
  const [theme, setTheme] = useState(searchParams.get("theme") || "all");
  const [learningMode, setLearningMode] = useState(true);

  useEffect(() => {
    getVerses().then(setItems).catch(() => setItems([]));
  }, []);

  useEffect(() => {
    const fromUrl = searchParams.get("theme") || "all";
    setTheme(fromUrl);
  }, [searchParams]);

  const collections = useMemo(() => {
    const set = new Set(items.map((x) => (x.collection || "Unknown").trim()));
    return ["all", ...Array.from(set).sort((a, b) => a.localeCompare(b))];
  }, [items]);

  const themes = useMemo(() => {
    const set = new Set<string>();
    for (const x of items) {
      for (const t of x.themes || []) {
        if (t && t.trim()) set.add(t.trim());
      }
    }
    return ["all", ...Array.from(set).sort((a, b) => a.localeCompare(b))];
  }, [items]);

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase();
    return items.filter((x) => {
      const matchCollection = collection === "all" || (x.collection || "").trim() === collection;
      if (!matchCollection) return false;
      const matchTheme = theme === "all" || (x.themes || []).includes(theme);
      if (!matchTheme) return false;
      if (!needle) return true;
      const blob = [x.title, x.sutra_id, x.translation, x.commentary, x.collection].join(" ").toLowerCase();
      return blob.includes(needle);
    });
  }, [items, q, collection, theme]);

  function applyTheme(next: string) {
    const params = new URLSearchParams(searchParams.toString());
    if (next === "all") params.delete("theme");
    else params.set("theme", next);
    router.replace(`/read${params.toString() ? `?${params.toString()}` : ""}`);
  }

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="text-3xl text-amber-200">Library</h1>
      <p className="soft mt-2">Move idea-to-idea: filter by themes, open a passage, then follow related concepts.</p>

      <div className="mt-6 grid gap-3 sm:grid-cols-[2fr_1fr_1fr]">
        <input
          value={q}
          onChange={(e) => setQ(e.target.value)}
          className="rounded-lg border border-white/15 bg-slate-950/70 px-3 py-2"
          placeholder="Search passages, titles, themes..."
        />
        <select
          value={collection}
          onChange={(e) => setCollection(e.target.value)}
          className="rounded-lg border border-white/15 bg-slate-950/70 px-3 py-2"
        >
          {collections.map((c) => (
            <option key={c} value={c}>
              {c === "all" ? "All collections" : displayCollectionName(c)}
            </option>
          ))}
        </select>
        <select
          value={theme}
          onChange={(e) => {
            setTheme(e.target.value);
            applyTheme(e.target.value);
          }}
          className="rounded-lg border border-white/15 bg-slate-950/70 px-3 py-2"
        >
          {themes.map((t) => (
            <option key={t} value={t}>
              {t === "all" ? "All themes" : `Theme: ${t}`}
            </option>
          ))}
        </select>
      </div>

      <label className="mt-4 block text-sm soft">
        <input type="checkbox" className="mr-2" checked={learningMode} onChange={(e) => setLearningMode(e.target.checked)} />
        Learning mode previews
      </label>

      <div className="mt-3 flex flex-wrap gap-2">
        {themes.slice(1, 10).map((t) => (
          <button
            key={t}
            onClick={() => {
              setTheme(t);
              applyTheme(t);
            }}
            className={`rounded-full border px-3 py-1 text-xs ${
              theme === t ? "border-amber-200/60 text-amber-100" : "border-white/20 text-slate-200"
            }`}
          >
            {t}
          </button>
        ))}
      </div>

      <div className="mt-6 space-y-3">
        {filtered.slice(0, 300).map((x) => (
          <Link key={x._id} href={`/read/${encodeURIComponent(x._id)}`} className="card block p-4 hover:border-amber-300/30">
            <div className="flex items-start justify-between gap-4">
              <div>
                <h2 className="text-lg text-amber-100">{x.title || x.sutra_id || x._id}</h2>
                <p className="soft text-sm">{displayCollectionName(x.collection)} {x.section ? `• ${x.section}` : ""}</p>
              </div>
              {x.themes && x.themes.length > 0 ? (
                <span className="rounded-full border border-amber-200/30 px-2 py-1 text-xs text-amber-100">
                  {x.themes.slice(0, 2).join(" · ")}
                </span>
              ) : null}
            </div>
            {!learningMode ? (
              <p className="soft mt-3 line-clamp-2 text-sm">{stripMarkdown(x.translation || x.commentary || "Open to view passage.")}</p>
            ) : (
              <div className="soft mt-3 space-y-2 text-sm">
                <p className="line-clamp-2">
                  <span className="text-amber-100">Core idea:</span> {stripMarkdown(x.translation || "Open to view passage.")}
                </p>
                <p className="line-clamp-2">
                  <span className="text-amber-100">Why it matters:</span> {firstSentence(x.commentary || x.translation || "")}
                </p>
                <p className="line-clamp-2">
                  <span className="text-amber-100">Reflect:</span> {reflectionPrompt(x)}
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
    <Suspense fallback={
      <main className="mx-auto max-w-6xl px-4 py-8">
        <h1 className="text-3xl text-amber-200">Library</h1>
        <p className="soft mt-2">Loading passages...</p>
      </main>
    }>
      <ReadPageContent />
    </Suspense>
  );
}

