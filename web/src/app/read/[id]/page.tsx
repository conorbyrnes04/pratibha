'use client';

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { getVerse, getVerses, getRelatedVerses } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { stripMarkdown } from "@/lib/textPreview";
import { displayCollectionName } from "@/lib/collectionLabels";
import { collectionArtPool } from "@/lib/collectionImages";
import { unitGlyph } from "@/lib/glyphs";
import { ArtBackdrop } from "@/components/ArtImage";
import { Glyph } from "@/components/Glyph";
import { displayPassageTitle } from "@/lib/passageTitles";
import { LayerBlock } from "@/components/LayerBlock";
import { JournalPanel } from "@/components/JournalPanel";
import { getStudyLayers, getAppendixLayers, getAnchorChapter, getResonances, layerText, passagePreview, practiceText } from "@/lib/verseLayers";
import { relatedPassages } from "@/lib/relatedPassages";

function practiceFallback(item: VerseItem): string {
  if ((item.themes || []).includes("witness")) {
    return "For 2 minutes, notice thoughts and sensations as objects appearing in awareness.";
  }
  if ((item.themes || []).includes("liberation")) {
    return "Ask once: what am I taking myself to be in this moment?";
  }
  return "Read once slowly, then pause for one minute before your next action.";
}

function reflectionPrompt(item: VerseItem): string {
  const t = (item.themes || [])[0];
  if (t) return `How does "${t}" show up in your life today?`;
  return "What changes if this passage is treated as instruction, not just information?";
}

function sentenceCandidates(input?: string): string[] {
  const clean = stripMarkdown(input || "");
  if (!clean) return [];
  return clean
    .split(/(?<=[.!?])\s+/)
    .map((s) => s.trim())
    .filter((s) => s.length > 0);
}

function normalizeSentence(s: string): string {
  return s.replace(/\s+/g, " ").trim().toLowerCase();
}

function pickDistinct(candidates: string[], used: Set<string>): string {
  for (const s of candidates) {
    const n = normalizeSentence(s);
    if (!n || used.has(n)) continue;
    used.add(n);
    return s;
  }
  return "";
}

export default function VerseDetailPage() {
  const params = useParams<{ id: string }>();
  const [item, setItem] = useState<VerseItem | null>(null);
  const [allItems, setAllItems] = useState<VerseItem[]>([]);
  const [semanticRelated, setSemanticRelated] = useState<VerseItem[] | null>(null);
  const [learningMode, setLearningMode] = useState(true);
  const [showOriginal, setShowOriginal] = useState(true);
  const [compact, setCompact] = useState(false);
  const [showSource, setShowSource] = useState(false);
  const [loading, setLoading] = useState(true);
  const [backHref, setBackHref] = useState<string | null>(null);
  const id = decodeURIComponent(params.id || "");

  // If we arrived from a guided path (/read/<id>?back=/learn?...), offer a link
  // straight back to that exact step. Only honor internal paths.
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

  // Prefer semantic neighbours from pgvector; fall back to theme overlap when
  // RAG is offline or the unit isn't indexed yet.
  const related = semanticRelated && semanticRelated.length > 0 ? semanticRelated : themeRelated;
  const relatedMode = semanticRelated && semanticRelated.length > 0 ? "semantic" : "themes";

  const resonances = useMemo(() => (item ? getResonances(item) : []), [item]);

  if (loading) {
    return <main className="page-shell soft">Opening the manuscript...</main>;
  }
  if (!item) {
    return <main className="page-shell soft">Passage not found.</main>;
  }

  const layers = getStudyLayers(item);
  const appendixLayers = getAppendixLayers(item);
  const anchorChapter = getAnchorChapter(item);
  const visibleLayers = layers.filter((layer) => showOriginal || (layer.kind !== "original" && layer.kind !== "iast"));
  const translation = layerText(item, "translation");
  const commentary = layerText(item, "commentary");
  const used = new Set<string>();
  const coreIdea =
    pickDistinct(
      [
        ...sentenceCandidates(item.thesis),
        ...sentenceCandidates(translation),
        ...sentenceCandidates(commentary),
        ...sentenceCandidates(item.source_excerpt),
      ],
      used,
    ) || passagePreview(item);
  const plain =
    pickDistinct(
      [
        ...sentenceCandidates(item.source_excerpt),
        ...sentenceCandidates(commentary),
        ...sentenceCandidates(translation),
        ...sentenceCandidates(item.thesis),
      ],
      used,
    ) || "This passage asks for slower reading so the practical move is clear.";
  const practice = practiceText(item) || practiceFallback(item);
  const reflection = reflectionPrompt(item);

  const nextStep = related[0] || null;

  return (
    <main className="page-shell">
      {backHref ? (
        <div className="flex flex-wrap items-center gap-4">
          <Link href={backHref} className="font-sans text-sm text-amber-200 hover:text-amber-100">
            ← Back to path
          </Link>
          <Link href="/read" className="soft font-sans text-sm hover:text-amber-100">
            Back to library
          </Link>
        </div>
      ) : (
        <Link href="/read" className="soft font-sans text-sm hover:text-amber-100">
          ← Back to library
        </Link>
      )}
      <section className="passage-hero manuscript-card mt-4 p-6 sm:p-8">
        <ArtBackdrop srcs={collectionArtPool(item.collection)} variant="hero" priority />
        <div className="relative z-10 grid gap-6 lg:grid-cols-[1fr_15rem] lg:items-end">
          <div className="flex items-start gap-4">
            <span className="passage-hero__glyph mt-1 hidden sm:inline-flex" aria-hidden>
              <Glyph name={unitGlyph(item._id)} size="lg" zoom />
            </span>
            <div>
              <p className="eyebrow">{displayCollectionName(item.collection) || "Pratibha"} {item.section ? ` / ${item.section}` : ""}</p>
              <h1 className="mt-3 max-w-4xl text-5xl font-semibold leading-[0.92] tracking-[-0.04em] text-stone-100 sm:text-6xl">
                {displayPassageTitle(item)}
              </h1>
            </div>
          </div>
          <div className="citation-card grid gap-2 border-amber-200/20 bg-[#0b0b14]/75 p-3 font-sans text-sm text-stone-300 backdrop-blur-sm">
            <label className="flex items-center gap-3">
              <input type="checkbox" className="accent-amber-300" checked={learningMode} onChange={(e) => setLearningMode(e.target.checked)} />
              Learning guide
            </label>
            <label className="flex items-center gap-3">
              <input type="checkbox" className="accent-amber-300" checked={showOriginal} onChange={(e) => setShowOriginal(e.target.checked)} />
              Original language
            </label>
            <label className="flex items-center gap-3">
              <input type="checkbox" className="accent-amber-300" checked={compact} onChange={(e) => setCompact(e.target.checked)} />
              Compact commentary
            </label>
            {(appendixLayers.length > 0 || anchorChapter) ? (
              <label className="flex items-center gap-3">
                <input type="checkbox" className="accent-amber-300" checked={showSource} onChange={(e) => setShowSource(e.target.checked)} />
                Public-domain source (Giles / Patrick)
              </label>
            ) : null}
          </div>
        </div>
      </section>

      <div className="mt-6 grid gap-5 lg:grid-cols-[2fr_1fr]">
        <section>
          {learningMode ? (
            <section className="practice-card mb-4 p-5">
              <h2 className="layer-heading">Learning guide</h2>
              <div className="mt-3 space-y-3 text-sm">
                <p><span className="text-amber-100">Core idea:</span> {coreIdea}</p>
                <p><span className="text-amber-100">Why it matters:</span> {plain}</p>
                <p><span className="text-amber-100">Practice now:</span> {practice}</p>
                <p><span className="text-amber-100">Reflect:</span> {reflection}</p>
              </div>
            </section>
          ) : null}

          {visibleLayers.map((layer, idx) => (
            <LayerBlock key={`${layer.kind}-${layer.label}-${idx}`} layer={layer} compact={compact && layer.kind === "commentary"} />
          ))}

          {showSource ? (
            <>
              {appendixLayers.map((layer, idx) => (
                <LayerBlock key={`appendix-${layer.label}-${idx}`} layer={layer} defaultCollapsed={Boolean(layer.body && layer.body.length > 1200)} />
              ))}
              {anchorChapter ? (
                <LayerBlock
                  layer={{ kind: "appendix", label: "Full chapter — public-domain translation", body: anchorChapter }}
                  defaultCollapsed
                />
              ) : null}
            </>
          ) : (appendixLayers.length > 0 || anchorChapter) ? (
            <button
              type="button"
              onClick={() => setShowSource(true)}
              className="mt-4 w-full rounded-2xl border border-dashed border-amber-200/25 px-4 py-3 text-left font-sans text-sm text-amber-100/90 hover:border-amber-200/45"
            >
              Compare with public-domain translation (Giles 1889) — hidden by default so study stays focused.
            </button>
          ) : null}

          {item.themes && item.themes.length > 0 ? (
            <section className="mt-4 flex flex-wrap gap-2">
              {item.themes.map((t) => (
                <Link
                  key={t}
                  href={`/read?theme=${encodeURIComponent(t)}`}
                  className="rounded-full border border-amber-200/30 px-3 py-1 text-xs text-amber-100 hover:border-amber-200/60"
                >
                  {t}
                </Link>
              ))}
            </section>
          ) : null}

          <div className="mt-6 flex flex-wrap gap-3">
            <Link href={`/chat?verse_id=${encodeURIComponent(item._id)}&mode=explain`} className="btn-primary px-5 py-2.5">
              Guided Study
            </Link>
            <Link href={`/chat?verse_id=${encodeURIComponent(item._id)}&mode=practice`} className="btn-secondary px-5 py-2.5">
              Practice chat
            </Link>
            <Link href="/random" className="btn-secondary px-5 py-2.5">
              Explore another random passage
            </Link>
          </div>

          <div className="mt-6">
            <JournalPanel passage={item} />
          </div>
        </section>

        <aside className="card h-fit p-4">
          <h2 className="text-2xl text-amber-100">Related ideas</h2>
          <p className="soft mt-1 text-sm">
            {relatedMode === "semantic"
              ? "Nearest teachings in meaning — across the corpus."
              : "The same insight echoing across traditions."}
          </p>

          {resonances.length > 0 ? (
            <div className="mt-4">
              <p className="layer-heading">Cross-tradition resonances</p>
              <div className="mt-2 space-y-3">
                {resonances.map((r, idx) => (
                  <article key={`${r.citation}-${idx}`} className="citation-card p-3">
                    <p className="text-sm text-amber-100">{r.citation}</p>
                    <p className="soft mt-1 text-xs leading-relaxed">{r.resonance}</p>
                    {r.divergence ? (
                      <p className="mt-2 text-xs leading-relaxed text-stone-300">
                        <span className="text-amber-100">Divergence:</span> {r.divergence}
                      </p>
                    ) : null}
                  </article>
                ))}
              </div>
            </div>
          ) : null}

          <div className="mt-4">
            <p className="layer-heading">Passages to explore</p>
            <div className="mt-2 space-y-3">
              {related.length === 0 ? (
                <p className="soft text-sm">No related passages yet.</p>
              ) : (
                related.map((r) => {
                  const crossTradition = (r.collection || "") !== (item.collection || "");
                  return (
                    <Link key={r._id} href={`/read/${encodeURIComponent(r._id)}`} className="citation-card block p-3 hover:border-amber-300/30">
                      <div className="flex items-start justify-between gap-2">
                        <p className="text-sm text-amber-100">{displayPassageTitle(r)}</p>
                        {crossTradition ? (
                          <span className="shrink-0 rounded-full border border-amber-200/25 px-2 py-0.5 font-sans text-[10px] uppercase tracking-wide text-amber-200/80">
                            Cross-tradition
                          </span>
                        ) : null}
                      </div>
                      <p className="soft mt-1 text-xs">
                        {displayCollectionName(r.collection)} {r.section ? `• ${r.section}` : ""}
                      </p>
                      <p className="soft mt-1 line-clamp-2 text-xs">{passagePreview(r)}</p>
                    </Link>
                  );
                })
              )}
            </div>
          </div>

          {nextStep ? (
            <div className="practice-card mt-4 p-3">
              <p className="layer-heading">Next natural step</p>
              <Link href={`/read/${encodeURIComponent(nextStep._id)}`} className="mt-1 block text-sm text-amber-100 hover:underline">
                {displayPassageTitle(nextStep)}
              </Link>
            </div>
          ) : null}
        </aside>
      </div>
    </main>
  );
}

