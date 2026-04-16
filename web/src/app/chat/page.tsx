'use client';

import { useEffect, useMemo, useState } from "react";
import { askChat, getCollections } from "@/lib/api";
import type { Source } from "@/lib/types";
import { displayCollectionName } from "@/lib/collectionLabels";
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

  useEffect(() => {
    const fromUrl = new URLSearchParams(window.location.search).get("q");
    if (fromUrl) setQ(fromUrl);
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

  async function ask() {
    if (!q.trim() || busy) return;
    const next: ChatMessage[] = [...messages, { role: "user", content: q.trim() }];
    setMessages(next);
    setBusy(true);
    setQ("");
    try {
      const selected = compareMode ? [compareA, compareB].filter(Boolean) : [];
      const data = await askChat(next, useRag, compareMode, selected);
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
    <main className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="text-3xl text-amber-200">Study Chat</h1>
      <p className="soft mt-2">Ask naturally. You will get simple explanation, key insight, and one concrete practice.</p>

      <div className="mt-6 grid gap-4 lg:grid-cols-[2fr_1fr]">
        <section className="card p-4">
          <div className="space-y-3">
            {messages.length === 0 ? (
              <div className="soft rounded-md border border-white/10 p-4">
                Start with a prompt below, or ask your own question about any chapter.
              </div>
            ) : (
              messages.map((m, idx) => (
                <article
                  key={`${m.role}-${idx}`}
                  className={`rounded-md border p-4 whitespace-pre-wrap ${
                    m.role === "user" ? "border-amber-200/30 bg-amber-100/5" : "border-white/10 bg-slate-950/40"
                  }`}
                >
                  <p className="mb-2 text-xs uppercase tracking-wide soft">{m.role === "user" ? "You" : "Pratibha"}</p>
                  {m.role === "assistant" ? (
                    <div className="chat-markdown">
                      <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
                    </div>
                  ) : (
                    <p>{m.content}</p>
                  )}
                </article>
              ))
            )}
          </div>

          <div className="mt-4 flex flex-wrap gap-2">
            {suggestions.map((s) => (
              <button key={s} onClick={() => setQ(s)} className="rounded-full border border-amber-200/25 px-3 py-1 text-xs text-amber-100">
                {s}
              </button>
            ))}
          </div>

          <label className="mt-4 block text-sm soft">
            <input type="checkbox" checked={useRag} onChange={(e) => setUseRag(e.target.checked)} className="mr-2" />
            Use source-grounded retrieval (recommended)
          </label>
          <label className="mt-2 block text-sm soft">
            <input type="checkbox" checked={compareMode} onChange={(e) => setCompareMode(e.target.checked)} className="mr-2" />
            Compare mode (debate/synthesis between two texts)
          </label>
          {compareMode && (
            <div className="mt-2 grid gap-2 sm:grid-cols-2">
              <select
                value={compareA}
                onChange={(e) => setCompareA(e.target.value)}
                className="rounded-md border border-white/15 bg-slate-950/70 p-2 text-sm"
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
                className="rounded-md border border-white/15 bg-slate-950/70 p-2 text-sm"
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
            className="mt-3 w-full rounded-lg border border-white/15 bg-slate-950/70 p-3"
            rows={4}
            value={q}
            onChange={(e) => setQ(e.target.value)}
            placeholder="Ask about this chapter, ask for practice guidance, or compare two traditions..."
          />
          <div className="mt-3">
            <button
              onClick={ask}
              disabled={busy}
              className="rounded-lg bg-amber-300 px-5 py-2 font-semibold text-slate-900 disabled:opacity-50"
            >
              {busy ? "Thinking..." : "Ask"}
            </button>
          </div>
        </section>

        <aside className="card p-4">
          <h2 className="text-lg text-amber-100">Sources</h2>
          <p className="soft mt-1 text-sm">When RAG is enabled, supporting passages appear here.</p>
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
                <article key={`source-${s.rank}`} className="rounded-md border border-white/10 bg-slate-950/40 p-3">
                  <p className="text-xs soft">
                    #{s.rank} {typeof s.score === "number" ? `• score ${s.score.toFixed(3)}` : ""}
                  </p>
                  {(() => {
                    const side = (s.metadata?.compare_side as string | undefined) || "";
                    return side ? (
                    <p className="mt-1 text-[11px] uppercase tracking-wide text-amber-200">
                      Voice {side}
                    </p>
                    ) : null;
                  })()}
                  <p className="mt-1 text-xs soft">
                    {displayCollectionName(String((s.metadata?.collection as string) || ""))}
                    {s.metadata?.title ? ` • ${String(s.metadata.title)}` : ""}
                    {s.metadata?.section ? ` • ${String(s.metadata.section)}` : ""}
                  </p>
                  {Array.isArray(s.metadata?.themes) && (s.metadata?.themes as unknown[]).length > 0 ? (
                    <p className="mt-2 text-[11px] soft">
                      Themes: {(s.metadata?.themes as unknown[]).slice(0, 3).map((t) => String(t)).join(", ")}
                    </p>
                  ) : null}
                  <p className="mt-2 line-clamp-6 text-sm whitespace-pre-wrap">{s.text || ""}</p>
                </article>
              ))
            )}
          </div>
        </aside>
      </div>
    </main>
  );
}