'use client';

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { getVerse, getVerses } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { firstSentence, stripMarkdown } from "@/lib/textPreview";
import { displayCollectionName } from "@/lib/collectionLabels";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

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
  const [learningMode, setLearningMode] = useState(true);
  const [loading, setLoading] = useState(true);
  const id = decodeURIComponent(params.id || "");

  useEffect(() => {
    getVerse(id)
      .then((v) => setItem(v))
      .finally(() => setLoading(false));
  }, [id]);
  useEffect(() => {
    getVerses().then(setAllItems).catch(() => setAllItems([]));
  }, []);

  const related = useMemo(() => {
    if (!item) return [] as VerseItem[];
    const mineThemes = new Set(item.themes || []);
    const out = allItems.filter((v) => {
      if (v._id === item._id) return false;
      const sameCollection = (v.collection || "") === (item.collection || "");
      const overlap = (v.themes || []).some((t) => mineThemes.has(t));
      return sameCollection || overlap;
    });
    out.sort((a, b) => {
      const aSame = (a.collection || "") === (item.collection || "") ? 1 : 0;
      const bSame = (b.collection || "") === (item.collection || "") ? 1 : 0;
      return bSame - aSame;
    });
    return out.slice(0, 6);
  }, [allItems, item]);

  if (loading) {
    return <main className="mx-auto max-w-4xl px-4 py-8 soft">Loading passage...</main>;
  }
  if (!item) {
    return <main className="mx-auto max-w-4xl px-4 py-8 soft">Passage not found.</main>;
  }

  const prompt = encodeURIComponent(
    `Guide me through this passage from ${displayCollectionName(item.collection)} (${item.sutra_id || item._id}). First explain simply, then key themes, then one practice for today.`,
  );
  const norm = (s: string) => s.replace(/\s+/g, " ").trim().toLowerCase();
  const hasDistinctCommentary =
    Boolean(item.commentary?.trim()) &&
    norm(item.commentary || "") !== norm(item.translation || "");
  const used = new Set<string>();
  const coreIdea =
    pickDistinct(
      [
        ...sentenceCandidates(item.thesis),
        ...sentenceCandidates(item.translation),
        ...sentenceCandidates(item.commentary),
        ...sentenceCandidates(item.source_excerpt),
      ],
      used,
    ) || firstSentence(item.translation || item.commentary || item.source_excerpt || "");
  const plain =
    pickDistinct(
      [
        ...sentenceCandidates(item.source_excerpt),
        ...sentenceCandidates(item.commentary),
        ...sentenceCandidates(item.translation),
        ...sentenceCandidates(item.thesis),
      ],
      used,
    ) || "This passage asks for slower reading so the practical move is clear.";
  const practice = stripMarkdown((item.practice || item.abhyasa || "").trim() || practiceFallback(item));
  const reflection = reflectionPrompt(item);

  const nextStep = related[0] || null;

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <Link href="/read" className="soft text-sm hover:text-amber-100">
        ← Back to library
      </Link>
      <h1 className="mt-3 text-3xl text-amber-200">{item.title || item.sutra_id || item._id}</h1>
      <p className="soft mt-2">
        {displayCollectionName(item.collection)} {item.section ? `• ${item.section}` : ""}
      </p>
      <label className="mt-4 block text-sm soft">
        <input type="checkbox" className="mr-2" checked={learningMode} onChange={(e) => setLearningMode(e.target.checked)} />
        Learning mode
      </label>

      <div className="mt-6 grid gap-5 lg:grid-cols-[2fr_1fr]">
        <section>
          {learningMode ? (
            <section className="card mb-4 p-5">
              <h2 className="text-sm uppercase tracking-wider text-amber-100/90">Learning guide</h2>
              <div className="mt-3 space-y-3 text-sm">
                <p><span className="text-amber-100">Core idea:</span> {coreIdea}</p>
                <p><span className="text-amber-100">Why it matters:</span> {plain}</p>
                <p><span className="text-amber-100">Practice now:</span> {practice}</p>
                <p><span className="text-amber-100">Reflect:</span> {reflection}</p>
              </div>
            </section>
          ) : null}

          {item.sanskrit ? (
            <section className="card mt-6 p-5">
              <h2 className="text-sm uppercase tracking-wider text-amber-100/90">Devanagari</h2>
              <p className="mt-3 whitespace-pre-wrap text-2xl leading-relaxed">{item.sanskrit}</p>
            </section>
          ) : null}

          {item.transliteration ? (
            <section className="card mt-4 p-5">
              <h2 className="text-sm uppercase tracking-wider text-amber-100/90">IAST</h2>
              <p className="mt-3 whitespace-pre-wrap italic leading-relaxed">{item.transliteration}</p>
            </section>
          ) : null}

          {item.translation ? (
            <section className="card mt-6 p-5">
              <h2 className="text-sm uppercase tracking-wider text-amber-100/90">Root text</h2>
              <div className="chat-markdown mt-3 leading-relaxed">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{item.translation}</ReactMarkdown>
              </div>
            </section>
          ) : null}

          {hasDistinctCommentary ? (
            <section className="card mt-4 p-5">
              <h2 className="text-sm uppercase tracking-wider text-amber-100/90">Commentary</h2>
              <div className="chat-markdown mt-3 leading-relaxed">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>{item.commentary}</ReactMarkdown>
              </div>
            </section>
          ) : null}

          {item.appendixes && item.appendixes.length > 0 ? (
            <section className="card mt-4 p-5">
              <h2 className="text-sm uppercase tracking-wider text-amber-100/90">Appendix commentaries</h2>
              <div className="mt-3 space-y-4">
                {item.appendixes.map((a, idx) => (
                  <article key={`${a.commentator || "appendix"}-${idx}`} className="rounded-md border border-white/10 p-3">
                    <h3 className="text-amber-100">{a.commentator || "Commentary"}</h3>
                    <div className="chat-markdown soft mt-2 text-sm">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{a.text || ""}</ReactMarkdown>
                    </div>
                  </article>
                ))}
              </div>
            </section>
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
            <Link href={`/chat?q=${prompt}`} className="rounded-lg bg-amber-300 px-4 py-2 font-semibold text-slate-900">
              Guided Study
            </Link>
            <Link href="/random" className="rounded-lg border border-amber-200/30 px-4 py-2 text-amber-100">
              Explore another random passage
            </Link>
          </div>
        </section>

        <aside className="card h-fit p-4">
          <h2 className="text-lg text-amber-100">Related ideas</h2>
          <p className="soft mt-1 text-sm">Follow concept links across texts.</p>
          <div className="mt-3 space-y-3">
            {related.length === 0 ? (
              <p className="soft text-sm">No related passages yet.</p>
            ) : (
              related.map((r) => (
                <Link key={r._id} href={`/read/${encodeURIComponent(r._id)}`} className="block rounded-md border border-white/10 p-3 hover:border-amber-300/30">
                  <p className="text-sm text-amber-100">{r.title || r.sutra_id || r._id}</p>
                  <p className="soft mt-1 text-xs">
                    {displayCollectionName(r.collection)} {r.section ? `• ${r.section}` : ""}
                  </p>
                  <p className="soft mt-1 line-clamp-2 text-xs">{stripMarkdown(r.translation || r.commentary || "")}</p>
                </Link>
              ))
            )}
          </div>
          {nextStep ? (
            <div className="mt-4 rounded-md border border-amber-200/30 bg-amber-200/5 p-3">
              <p className="text-xs uppercase tracking-wide text-amber-100">Next natural step</p>
              <Link href={`/read/${encodeURIComponent(nextStep._id)}`} className="mt-1 block text-sm text-amber-100 hover:underline">
                {nextStep.title || nextStep.sutra_id || nextStep._id}
              </Link>
            </div>
          ) : null}
        </aside>
      </div>
    </main>
  );
}

