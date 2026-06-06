'use client';

import { useEffect, useMemo, useState } from "react";
import { askChat, getCollections, getVerse } from "@/lib/api";
import { saveChatResponse } from "@/lib/journalStorage";
import type { ChatMode, PratibhaLayerKind, Source, VerseItem } from "@/lib/types";
import { displayCollectionName } from "@/lib/collectionLabels";
import { maturityLabel, passagePreview, practiceText } from "@/lib/verseLayers";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type ChatMessage = { role: "user" | "assistant"; content: string };

export default function ChatPage() {
  const [q, setQ] = useState("");
  const [useRag, setUseRag] = useState(true);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [busy, setBusy] = useState(false);
  const [compareMode, setCompareMode] = useState(false);
  const [collections, setCollections] = useState<string[]>([]);
  const [compareA, setCompareA] = useState("");
  const [compareB, setCompareB] = useState("");
  const [compareWarning, setCompareWarning] = useState("");
  const [pinnedVerse, setPinnedVerse] = useState<VerseItem | null>(null);
  const [chatMode, setChatMode] = useState<ChatMode>("question");
  const [layerFocus, setLayerFocus] = useState<PratibhaLayerKind | "">("");
  const [savedReplies, setSavedReplies] = useState<Set<number>>(new Set());

  useEffect(() => {
    const fromUrl = new URLSearchParams(window.location.search).get("q");
    if (fromUrl) setQ(fromUrl);
    const params = new URLSearchParams(window.location.search);
    const verseId = params.get("verse_id");
    const mode = params.get("mode") as ChatMode | null;
    if (mode && ["question", "explain", "compare", "practice"].includes(mode)) {
      setChatMode(mode);
      if (!fromUrl) {
        setQ(mode === "practice" ? "Give me one concrete practice from this passage." : "Guide me through this passage.");
      }
    }
    if (verseId) {
      getVerse(verseId).then(setPinnedVerse).catch(() => setPinnedVerse(null));
    }
  }, []);

  useEffect(() => {
    getCollections().then((items) => {
      setCollections(items);
      if (items.length > 0) setCompareA((prev) => prev || items[0]);
      if (items.length > 1) setCompareB((prev) => prev || items[1]);
    });
  }, []);

  const suggestions = useMemo(
    () => [
      "Explain this passage in plain language.",
      "What is the practical instruction for today?",
      "How do the appendixes/commentators differ?",
      "Give me one reflection question and one short practice.",
      "Compare two traditions on desire, discipline, and freedom.",
      "Debate Phaedo (Plato) and Epictetus on preparing for death.",
    ],
    [],
  );

  function saveReply(index: number, content: string) {
    const question =
      index > 0 && messages[index - 1]?.role === "user" ? messages[index - 1].content : "";
    saveChatResponse({
      answer: content,
      question,
      verse: pinnedVerse,
      chatMode,
    });
    setSavedReplies((prev) => new Set(prev).add(index));
  }

  async function ask() {
    if (!q.trim() || busy) return;
    const next: ChatMessage[] = [...messages, { role: "user", content: q.trim() }];
    setMessages(next);
    setBusy(true);
    setQ("");
    try {
      const selected = compareMode ? [compareA, compareB].filter(Boolean) : [];
      const data = await askChat(next, useRag, compareMode, selected, {
        verseId: pinnedVerse?._id,
        layerFocus: layerFocus || undefined,
        chatMode,
      });
      setMessages([...next, { role: "assistant", content: data.answer || "(no answer)" }]);
      setSources(data.sources || []);
      setCompareWarning(data.compareWarning || "");
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Unknown error";
      setMessages([...next, { role: "assistant", content: `I hit an error: ${msg}` }]);
      setSources([]);
      setCompareWarning("");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="page-shell">
      <p className="eyebrow">Dialogue with the corpus</p>
      <h1 className="mt-3 text-5xl font-semibold leading-none tracking-[-0.04em] text-stone-100 sm:text-6xl">Ask Pratibha</h1>
      <p className="soft mt-4 max-w-2xl text-xl leading-relaxed">Ask naturally. The companion answers with source-grounded explanation, cross-tradition context, and a practice you can actually try.</p>

      <div className="mt-6 grid gap-4 lg:grid-cols-[2fr_1fr]">
        <section className="manuscript-card p-4 sm:p-5">
          {pinnedVerse ? (
            <div className="practice-card mb-4 p-4">
              <p className="layer-heading">Pinned passage</p>
              <h2 className="mt-2 text-2xl leading-none text-amber-100">
                {pinnedVerse.title || pinnedVerse.sutra_id || pinnedVerse._id}
              </h2>
              <p className="soft mt-1 font-sans text-sm">
                {displayCollectionName(pinnedVerse.collection)} {pinnedVerse.section ? `• ${pinnedVerse.section}` : ""} • {maturityLabel(pinnedVerse.editorial_maturity)}
              </p>
              <p className="soft mt-3 text-sm leading-relaxed">{passagePreview(pinnedVerse)}</p>
              {practiceText(pinnedVerse) ? (
                <p className="mt-3 text-sm leading-relaxed text-stone-200">
                  <span className="text-amber-100">Practice:</span> {practiceText(pinnedVerse)}
                </p>
              ) : null}
              <div className="mt-4 grid gap-2 sm:grid-cols-2">
                <select value={chatMode} onChange={(e) => setChatMode(e.target.value as ChatMode)} className="input-field rounded-md p-2 text-sm">
                  <option value="question">Open question</option>
                  <option value="explain">Explain</option>
                  <option value="practice">Practice</option>
                  <option value="compare">Compare</option>
                </select>
                <select value={layerFocus} onChange={(e) => setLayerFocus(e.target.value as PratibhaLayerKind | "")} className="input-field rounded-md p-2 text-sm">
                  <option value="">All layers</option>
                  <option value="translation">Translation</option>
                  <option value="commentary">Commentary</option>
                  <option value="key_terms">Key terms</option>
                  <option value="resonances">Resonances</option>
                  <option value="practice">Practice</option>
                </select>
              </div>
            </div>
          ) : null}
          <div className="space-y-3">
            {messages.length === 0 ? (
              <div className="citation-card p-5">
                <p className="layer-heading">Begin</p>
                <p className="soft mt-3 text-lg">Start with a prompt below, or ask your own question about any chapter.</p>
              </div>
            ) : (
              messages.map((m, idx) => (
                <article
                  key={`${m.role}-${idx}`}
                  className={`whitespace-pre-wrap rounded-2xl border p-4 ${
                    m.role === "user" ? "border-amber-200/30 bg-amber-100/10" : "citation-card"
                  }`}
                >
                  <p className="layer-heading mb-2">{m.role === "user" ? "You" : "Pratibha"}</p>
                  {m.role === "assistant" ? (
                    <>
                      <div className="chat-markdown reading-prose">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
                      </div>
                      <button
                        type="button"
                        onClick={() => saveReply(idx, m.content)}
                        disabled={savedReplies.has(idx)}
                        className="btn-secondary mt-3 px-3 py-1 text-xs disabled:opacity-50"
                      >
                        {savedReplies.has(idx) ? "Saved to journal" : "Save to journal"}
                      </button>
                    </>
                  ) : (
                    <p>{m.content}</p>
                  )}
                </article>
              ))
            )}
          </div>

          <div className="mt-4 flex flex-wrap gap-2">
            {suggestions.map((s) => (
              <button key={s} onClick={() => setQ(s)} className="btn-secondary px-3 py-1 text-xs">
                {s}
              </button>
            ))}
          </div>

          <label className="mt-4 block font-sans text-sm soft">
            <input type="checkbox" checked={useRag} onChange={(e) => setUseRag(e.target.checked)} className="mr-2 accent-amber-300" />
            Use source-grounded retrieval (recommended)
          </label>
          <label className="mt-2 block font-sans text-sm soft">
            <input type="checkbox" checked={compareMode} onChange={(e) => setCompareMode(e.target.checked)} className="mr-2 accent-amber-300" />
            Compare mode (debate/synthesis between two texts)
          </label>
          {compareMode && (
            <div className="mt-2 grid gap-2 sm:grid-cols-2">
              <select
                value={compareA}
                onChange={(e) => setCompareA(e.target.value)}
                className="input-field rounded-md p-2 text-sm"
              >
                {collections.map((c) => (
                  <option key={`a-${c}`} value={c}>
                    A: {displayCollectionName(c)}
                  </option>
                ))}
              </select>
              <select
                value={compareB}
                onChange={(e) => setCompareB(e.target.value)}
                className="input-field rounded-md p-2 text-sm"
              >
                {collections.map((c) => (
                  <option key={`b-${c}`} value={c}>
                    B: {displayCollectionName(c)}
                  </option>
                ))}
              </select>
            </div>
          )}
          <textarea
            className="input-field mt-3 w-full rounded-2xl p-3"
            rows={4}
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Ask about this chapter, ask for practice guidance, or compare two traditions..."
          />
          <div className="mt-3">
            <button
              onClick={ask}
              disabled={busy}
              className="btn-primary px-6 py-2.5 disabled:opacity-50"
            >
              {busy ? "Thinking..." : "Ask"}
            </button>
          </div>
        </section>

        <aside className="card p-4">
          <h2 className="text-2xl text-amber-100">Source shelf</h2>
          <p className="soft mt-1 text-sm">Supporting passages appear here when retrieval is enabled.</p>
          {pinnedVerse ? (
            <article className="practice-card mt-3 p-3">
              <p className="layer-heading">Primary source</p>
              <p className="mt-2 text-sm text-amber-100">{pinnedVerse.title || pinnedVerse.sutra_id || pinnedVerse._id}</p>
              <p className="soft mt-1 line-clamp-4 text-sm">{passagePreview(pinnedVerse)}</p>
            </article>
          ) : null}
          {compareMode && compareWarning ? (
            <p className="mt-2 rounded-md border border-amber-300/40 bg-amber-300/10 p-2 text-xs text-amber-100">
              {compareWarning}
            </p>
          ) : null}
          <div className="mt-3 space-y-3">
            {sources.length === 0 ? (
              <p className="soft text-sm">No sources shown yet.</p>
            ) : (
              sources.map((s) => (
                <article key={`source-${s.rank}`} className="citation-card p-3">
                  <p className="layer-heading">
                    Source {s.rank}
                  </p>
                  {(() => {
                    const side = (s.metadata?.compare_side as string | undefined) || "";
                    return side ? (
                    <p className="mt-1 font-sans text-[11px] uppercase tracking-wide text-amber-200">
                      Voice {side}
                    </p>
                    ) : null;
                  })()}
                  <p className="mt-2 text-sm text-amber-100">
                    {displayCollectionName(String((s.metadata?.collection as string) || ""))}
                    {s.metadata?.title ? ` • ${String(s.metadata.title)}` : ""}
                    {s.metadata?.section ? ` • ${String(s.metadata.section)}` : ""}
                  </p>
                  {Array.isArray(s.metadata?.themes) && (s.metadata?.themes as unknown[]).length > 0 ? (
                    <p className="mt-2 text-[11px] soft">
                      Themes: {(s.metadata?.themes as unknown[]).slice(0, 3).map((t) => String(t)).join(", ")}
                    </p>
                  ) : null}
                  <p className="soft mt-2 line-clamp-6 whitespace-pre-wrap text-sm leading-relaxed">{s.text || ""}</p>
                </article>
              ))
            )}
          </div>
        </aside>
      </div>
    </main>
  );
}