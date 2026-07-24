'use client';

import { useEffect, useMemo, useState } from "react";
import { askChatStream, getCollections, getVerse, getVerses } from "@/lib/api";
import { useAuth } from "@/components/AuthProvider";
import { pushJournalNote } from "@/lib/journalCloud";
import { saveChatResponse } from "@/lib/journalStorage";
import type { ChatMode, PratibhaLayerKind, Source, VerseItem } from "@/lib/types";
import { FilterSelect } from "@/components/FilterSelect";
import { ComparePassageSelect } from "@/components/ComparePassageSelect";
import { buildCompareCollectionOptions, passagesInCollection } from "@/lib/corpusFilters";
import { COMPARE_PRESETS } from "@/lib/comparePresets";
import { displayCollectionName } from "@/lib/collectionLabels";
import { collectionArtPool, collectionImageSrc, generatedArtPool } from "@/lib/collectionImages";
import { ArtBackdrop, ArtChip } from "@/components/ArtImage";
import { Disclosure } from "@/components/ui/Disclosure";
import { displayPassageTitle } from "@/lib/passageTitles";
import { passagePreview, practiceText } from "@/lib/verseLayers";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type ChatMessage = { role: "user" | "assistant"; content: string };

function sourcePassageLabel(metadata?: Record<string, unknown>): string {
  if (!metadata) return "";
  const ref = String(metadata.reference || "").trim();
  const title = String(metadata.title || "").trim();
  if (ref && title) return `${ref} — ${title}`;
  if (title) return title;
  return "";
}

export default function ChatPage() {
  const { user } = useAuth();
  const [q, setQ] = useState("");
  const [useRag, setUseRag] = useState(true);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sources, setSources] = useState<Source[]>([]);
  const [busy, setBusy] = useState(false);
  const [compareMode, setCompareMode] = useState(false);
  const [collections, setCollections] = useState<string[]>([]);
  const [allPassages, setAllPassages] = useState<VerseItem[]>([]);
  const [compareA, setCompareA] = useState("");
  const [compareB, setCompareB] = useState("");
  const [compareVerseA, setCompareVerseA] = useState("");
  const [compareVerseB, setCompareVerseB] = useState("");
  const [compareWarning, setCompareWarning] = useState("");
  const [pinnedVerse, setPinnedVerse] = useState<VerseItem | null>(null);
  const [chatMode, setChatMode] = useState<ChatMode>("question");
  const [layerFocus, setLayerFocus] = useState<PratibhaLayerKind | "">("");
  const [savedReplies, setSavedReplies] = useState<Set<number>>(new Set());

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const fromUrl = params.get("q");
    if (fromUrl) setQ(fromUrl);

    const verseId = params.get("verse_id");
    const mode = params.get("mode") as ChatMode | null;
    if (mode && ["question", "explain", "compare", "practice"].includes(mode)) {
      setChatMode(mode);
      if (mode === "compare") setCompareMode(true);
      if (!fromUrl) {
        setQ(
          mode === "practice"
            ? "Give me one concrete practice from this passage."
            : mode === "compare"
              ? "Compare these two traditions on the question above."
              : "Guide me through this passage.",
        );
      }
    }

    const voiceA = params.get("voice_a");
    const voiceB = params.get("voice_b");
    if (voiceA) setCompareA(voiceA);
    if (voiceB) setCompareB(voiceB);
    if (params.get("compare") === "1") setCompareMode(true);

    const verseA = params.get("verse_a");
    const verseB = params.get("verse_b");
    if (verseA) setCompareVerseA(verseA);
    if (verseB) setCompareVerseB(verseB);

    if (verseId) {
      getVerse(verseId).then(setPinnedVerse).catch(() => setPinnedVerse(null));
    }
  }, []);

  useEffect(() => {
    getCollections().then((items) => {
      setCollections(items);
      setCompareA((prev) => prev || items[0] || "");
      setCompareB((prev) => prev || items[1] || items[0] || "");
    });
    getVerses("strong_draft").then(setAllPassages).catch(() => setAllPassages([]));
  }, []);

  useEffect(() => {
    setCompareVerseA((prev) => {
      if (!prev) return prev;
      return passagesInCollection(allPassages, compareA).some((item) => item._id === prev) ? prev : "";
    });
  }, [allPassages, compareA]);

  useEffect(() => {
    setCompareVerseB((prev) => {
      if (!prev) return prev;
      return passagesInCollection(allPassages, compareB).some((item) => item._id === prev) ? prev : "";
    });
  }, [allPassages, compareB]);

  const collectionOptions = useMemo(
    () => buildCompareCollectionOptions(collections, allPassages),
    [allPassages, collections],
  );

  const passagesA = useMemo(
    () => passagesInCollection(allPassages, compareA),
    [allPassages, compareA],
  );
  const passagesB = useMemo(
    () => passagesInCollection(allPassages, compareB),
    [allPassages, compareB],
  );

  const chatModeOptions = useMemo(
    () => [
      { value: "question", label: "Open question" },
      { value: "explain", label: "Explain" },
      { value: "practice", label: "Practice" },
      { value: "compare", label: "Compare" },
    ],
    [],
  );

  const layerOptions = useMemo(
    () => [
      { value: "", label: "All layers" },
      { value: "translation", label: "Translation" },
      { value: "commentary", label: "Commentary" },
      { value: "key_terms", label: "Key terms" },
      { value: "resonances", label: "Resonances" },
      { value: "practice", label: "Practice" },
    ],
    [],
  );

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

  function applyPreset(presetId: string) {
    const preset = COMPARE_PRESETS.find((item) => item.id === presetId);
    if (!preset) return;
    setCompareMode(true);
    setChatMode("compare");
    setCompareA(preset.voiceA);
    setCompareB(preset.voiceB);
    setCompareVerseA(preset.verseA || "");
    setCompareVerseB(preset.verseB || "");
    setQ(preset.prompt);
  }

  function saveReply(index: number, content: string) {
    const question =
      index > 0 && messages[index - 1]?.role === "user" ? messages[index - 1].content : "";
    const note = saveChatResponse({
      answer: content,
      question,
      verse: pinnedVerse,
      chatMode,
    });
    if (user) void pushJournalNote(note, user.id);
    setSavedReplies((prev) => new Set(prev).add(index));
  }

  async function ask() {
    if (!q.trim() || busy) return;
    const next: ChatMessage[] = [...messages, { role: "user", content: q.trim() }];
    // Add an empty assistant message we fill as tokens stream in.
    setMessages([...next, { role: "assistant", content: "" }]);
    const assistantIdx = next.length;
    setBusy(true);
    setQ("");
    setSources([]);
    setCompareWarning("");
    try {
      const selected = compareMode ? [compareA, compareB].filter(Boolean) : [];
      const compareVerseIds =
        compareMode && (compareVerseA || compareVerseB) ? [compareVerseA, compareVerseB] : undefined;
      const data = await askChatStream(
        next,
        useRag,
        compareMode,
        selected,
        { verseId: pinnedVerse?._id, compareVerseIds, layerFocus: layerFocus || undefined, chatMode },
        {
          onSources: (srcs, warning) => {
            setSources(srcs || []);
            setCompareWarning(warning || "");
          },
          onDelta: (full) => {
            setMessages((prev) => {
              const copy = [...prev];
              if (copy[assistantIdx]) copy[assistantIdx] = { role: "assistant", content: full };
              return copy;
            });
          },
        },
      );
      // Ensure final state matches (covers the no-delta error path).
      setMessages((prev) => {
        const copy = [...prev];
        copy[assistantIdx] = { role: "assistant", content: data.answer || "(no answer)" };
        return copy;
      });
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Unknown error";
      setMessages((prev) => {
        const copy = [...prev];
        copy[assistantIdx] = { role: "assistant", content: `I hit an error: ${msg}` };
        return copy;
      });
      setSources([]);
      setCompareWarning("");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="page-shell">
      <section className="manuscript-card relative overflow-hidden p-5 sm:p-6">
        <ArtBackdrop
          srcs={pinnedVerse ? collectionArtPool(pinnedVerse.collection) : generatedArtPool("heart-sutra")}
          variant="subtle"
          overlay="banner"
        />
        <div className="relative z-10">
          <p className="eyebrow">Dialogue with the corpus</p>
          <h1 className="mt-3 text-5xl font-semibold leading-none tracking-[-0.04em] text-stone-100 sm:text-6xl">Ask Pratibha</h1>
          <p className="soft mt-4 max-w-2xl text-xl leading-relaxed">Ask naturally. The companion answers with source-grounded explanation, cross-tradition context, and a practice you can actually try.</p>
        </div>
      </section>

      <div className="mt-8 grid gap-5 lg:grid-cols-[2fr_1fr]">
        <section className="manuscript-card p-5 sm:p-6">
          {pinnedVerse ? (
            <ArtChip
              src={collectionImageSrc(pinnedVerse.collection)}
              title={displayPassageTitle(pinnedVerse)}
              subtitle={`${displayCollectionName(pinnedVerse.collection)}${pinnedVerse.section ? ` • ${pinnedVerse.section}` : ""}`}
              className="mb-4"
            >
              <p className="soft mt-3 text-sm leading-relaxed">{passagePreview(pinnedVerse)}</p>
              {practiceText(pinnedVerse) ? (
                <p className="mt-3 text-sm leading-relaxed text-stone-200">
                  <span className="text-amber-100">Practice:</span> {practiceText(pinnedVerse)}
                </p>
              ) : null}
              <div className="mt-4 grid gap-3 sm:grid-cols-2">
                <FilterSelect
                  label="Study mode"
                  tone="gold"
                  value={chatMode}
                  onChange={(value) => {
                    const mode = value as ChatMode;
                    setChatMode(mode);
                    if (mode === "compare") setCompareMode(true);
                  }}
                  options={chatModeOptions}
                />
                <FilterSelect
                  label="Layer focus"
                  tone="lapis"
                  value={layerFocus}
                  onChange={(value) => setLayerFocus(value as PratibhaLayerKind | "")}
                  options={layerOptions}
                />
              </div>
            </ArtChip>
          ) : null}
          <div className="space-y-4">
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
                      {m.content ? (
                        <div className="chat-markdown reading-prose">
                          <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
                        </div>
                      ) : (
                        <p className="soft animate-pulse text-sm">Pratibha is thinking…</p>
                      )}
                      {m.content ? (
                        <button
                          type="button"
                          onClick={() => saveReply(idx, m.content)}
                          disabled={savedReplies.has(idx)}
                          className="btn-secondary mt-3 px-3 py-1 text-xs disabled:opacity-50"
                        >
                          {savedReplies.has(idx) ? "Saved to journal" : "Save to journal"}
                        </button>
                      ) : null}
                    </>
                  ) : (
                    <p>{m.content}</p>
                  )}
                </article>
              ))
            )}
          </div>

          <div className="mt-6">
            <p className="layer-heading mb-2">Try asking</p>
            <div className="flex flex-wrap gap-2">
              {suggestions.map((s) => (
                <button key={s} onClick={() => setQ(s)} className="btn-secondary px-3 py-1 text-xs">
                  {s}
                </button>
              ))}
            </div>
          </div>

          <div className="mt-4">
            <Disclosure
              summary="Retrieval & compare options"
              hint={`${useRag ? "Grounded" : "Freeform"}${compareMode ? " · Compare" : ""}`}
              defaultOpen={compareMode}
            >
              <label className="block font-sans text-sm soft">
                <input type="checkbox" checked={useRag} onChange={(e) => setUseRag(e.target.checked)} className="mr-2 accent-amber-300" />
                Use source-grounded retrieval (recommended)
              </label>
              <label className="mt-3 block font-sans text-sm soft">
                <input
                  type="checkbox"
                  checked={compareMode}
                  onChange={(e) => {
                    setCompareMode(e.target.checked);
                    if (e.target.checked) setChatMode("compare");
                  }}
                  className="mr-2 accent-amber-300"
                />
                Compare mode (debate/synthesis between two texts)
              </label>
              {compareMode && (
                <>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {COMPARE_PRESETS.map((preset) => (
                      <button
                        key={preset.id}
                        type="button"
                        onClick={() => applyPreset(preset.id)}
                        className="btn-secondary px-3 py-1 text-xs"
                      >
                        {preset.label}
                      </button>
                    ))}
                  </div>
                  <div className="mt-4 grid gap-3 lg:grid-cols-2">
                    <div className="space-y-3">
                      <FilterSelect
                        label="Voice A — text"
                        tone="gold"
                        value={compareA}
                        onChange={setCompareA}
                        options={collectionOptions.map((o) => ({ ...o, label: `A · ${o.label}` }))}
                      />
                      <ComparePassageSelect
                        label="Voice A — passage (optional)"
                        tone="gold"
                        collection={compareA}
                        passages={passagesA}
                        value={compareVerseA}
                        onChange={setCompareVerseA}
                      />
                    </div>
                    <div className="space-y-3">
                      <FilterSelect
                        label="Voice B — text"
                        tone="lapis"
                        value={compareB}
                        onChange={setCompareB}
                        options={collectionOptions.map((o) => ({ ...o, label: `B · ${o.label}` }))}
                      />
                      <ComparePassageSelect
                        label="Voice B — passage (optional)"
                        tone="lapis"
                        collection={compareB}
                        passages={passagesB}
                        value={compareVerseB}
                        onChange={setCompareVerseB}
                      />
                    </div>
                  </div>
                </>
              )}
            </Disclosure>
          </div>

          <textarea
            className="input-field mt-4 w-full rounded-2xl p-3"
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
              <p className="mt-2 text-sm text-amber-100">{displayPassageTitle(pinnedVerse)}</p>
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
                    {sourcePassageLabel(s.metadata) ? ` • ${sourcePassageLabel(s.metadata)}` : s.metadata?.title ? ` • ${String(s.metadata.title)}` : ""}
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
