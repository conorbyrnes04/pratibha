'use client';

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { askChatStream, ChatApiError, getCollections, getDaily, getVerse, getVerses } from "@/lib/api";
import { useAuth } from "@/components/AuthProvider";
import { useAuthToken } from "@convex-dev/auth/react";
import { usePushJournalNote } from "@/lib/journalCloud";
import { recordPractice } from "@/lib/glyphUnlock";
import { saveChatResponse } from "@/lib/journalStorage";
import type { ChatMode, PratibhaLayerKind, Source, VerseItem } from "@/lib/types";
import { FilterSelect } from "@/components/FilterSelect";
import { ComparePassageSelect } from "@/components/ComparePassageSelect";
import { buildCompareCollectionOptions, passagesInCollection } from "@/lib/corpusFilters";
import { COMPARE_PRESETS } from "@/lib/comparePresets";
import { displayCollectionName } from "@/lib/collectionLabels";
import { collectionArtPool, generatedArtPool } from "@/lib/collectionImages";
import { ArtBackdrop } from "@/components/ArtImage";
import { useT } from "@/components/LocaleProvider";
import { Disclosure } from "@/components/ui/Disclosure";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import {
  displayPassageLocation,
  displayPassageSourceLine,
  displayPassageTitle,
} from "@/lib/passageTitles";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type ChatMessage = { role: "user" | "assistant"; content: string };

type ChatSuggestion = {
  id: string;
  label: string;
  /** Pin today's live daily verse before filling the prompt. */
  pinDaily?: boolean;
  mode?: ChatMode;
  prompt: string;
};

function sourcePassageLabel(metadata?: Record<string, unknown>): string {
  if (!metadata) return "";
  const ref = String(metadata.reference || "").trim();
  const title = String(metadata.title || "").trim();
  if (ref && title) return `${ref} — ${title}`;
  if (title) return title;
  return "";
}

/** Passage id from RAG chunk metadata → `/read/[id]`. */
function sourcePassageHref(metadata?: Record<string, unknown>): string | null {
  if (!metadata) return null;
  for (const key of ["_id", "unit_id", "verse_id"] as const) {
    const value = String(metadata[key] || "").trim();
    if (value) return `/read/${encodeURIComponent(value)}`;
  }
  return null;
}

export default function ChatPage() {
  const t = useT();
  const { user } = useAuth();
  const accessToken = useAuthToken();
  const pushNote = usePushJournalNote();
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
  const [chatRemaining, setChatRemaining] = useState<number | null>(null);
  const [dailyCapHit, setDailyCapHit] = useState(false);
  const [backHref, setBackHref] = useState<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const fromUrl = params.get("q");
    if (fromUrl) setQ(fromUrl);

    const back = params.get("back");
    if (back && back.startsWith("/")) setBackHref(back);

    const verseId = params.get("verse_id");
    const mode = params.get("mode") as ChatMode | null;
    if (mode && ["question", "explain", "compare", "practice"].includes(mode)) {
      setChatMode(mode);
      if (mode === "compare") setCompareMode(true);
      // Leave the box empty when a passage is pinned so grayed suggestions can show.
      // Only prefill when the URL explicitly carries `q=…`.
      if (!fromUrl && !verseId && mode === "compare") {
        setQ("Compare these two traditions on the question above.");
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
      { value: "question", label: t("chat.modeQuestion") },
      { value: "explain", label: t("chat.modeExplain") },
      { value: "practice", label: t("chat.modePractice") },
      { value: "compare", label: t("chat.modeCompare") },
    ],
    [t],
  );

  const layerOptions = useMemo(
    () => [
      { value: "", label: t("layers.allLayers") },
      { value: "translation", label: t("layers.translation") },
      { value: "commentary", label: t("layers.commentary") },
      { value: "key_terms", label: t("layers.keyTerms") },
      { value: "resonances", label: t("layers.resonances") },
      { value: "practice", label: t("layers.practice") },
    ],
    [t],
  );

  const pinnedSourceLine = pinnedVerse
    ? displayPassageSourceLine({
        ...pinnedVerse,
        collection: displayCollectionName(pinnedVerse.collection) || pinnedVerse.collection,
      })
    : "";
  const pinnedTitle = pinnedVerse ? displayPassageTitle(pinnedVerse) : "";
  const pinnedLocation = pinnedVerse ? displayPassageLocation(pinnedVerse) : "";
  const pinnedRef = pinnedLocation || pinnedTitle;

  const suggestions = useMemo<ChatSuggestion[]>(() => {
    if (pinnedVerse) {
      const ref = pinnedRef || t("chat.thisPassage");
      return [
        {
          id: "explain",
          label: t("chat.suggestExplain", { ref }),
          mode: "explain",
          prompt: `Explain this passage (${pinnedTitle}${pinnedSourceLine ? ` · ${pinnedSourceLine}` : ""}) in plain language.`,
        },
        {
          id: "practice-here",
          label: t("chat.suggestPractice", { ref }),
          mode: "practice",
          prompt: `What is the practical instruction in this passage (${pinnedTitle}${pinnedSourceLine ? ` · ${pinnedSourceLine}` : ""})?`,
        },
        {
          id: "resonances",
          label: t("chat.suggestResonate", { ref }),
          mode: "compare",
          prompt: `Where does this passage (${pinnedTitle}${pinnedSourceLine ? ` · ${pinnedSourceLine}` : ""}) resonate across traditions — and where does it diverge?`,
        },
        {
          id: "reflect",
          label: t("chat.suggestReflectVerse"),
          mode: "practice",
          prompt: `Give me one reflection question and one short practice from this passage (${pinnedTitle}${pinnedSourceLine ? ` · ${pinnedSourceLine}` : ""}).`,
        },
      ];
    }
    return [
      {
        id: "today-practice",
        label: t("chat.suggestToday"),
        pinDaily: true,
        mode: "practice",
        prompt: "What is the practical instruction in today's passage?",
      },
      {
        id: "compare",
        label: t("chat.suggestCompare"),
        mode: "compare",
        prompt: "Compare two traditions on desire, discipline, and freedom.",
      },
      {
        id: "reflect",
        label: t("chat.suggestReflect"),
        mode: "practice",
        prompt: "Give me one reflection question and one short practice.",
      },
    ];
  }, [pinnedVerse, pinnedRef, pinnedTitle, pinnedSourceLine, t]);

  async function applySuggestion(suggestion: ChatSuggestion) {
    if (busy || dailyCapHit) return;

    if (suggestion.pinDaily) {
      const daily = await getDaily("rich");
      if (!daily) {
        setQ(suggestion.prompt);
        return;
      }
      setPinnedVerse(daily);
      setCompareMode(false);
      setChatMode(suggestion.mode || "practice");
      const title = displayPassageTitle(daily);
      const source = displayPassageSourceLine({
        ...daily,
        collection: displayCollectionName(daily.collection) || daily.collection,
      });
      setQ(`What is the practical instruction in today's passage (${title}${source ? ` · ${source}` : ""})?`);
      const url = new URL(window.location.href);
      url.searchParams.set("verse_id", daily._id);
      url.searchParams.set("mode", suggestion.mode || "practice");
      window.history.replaceState({}, "", url.toString());
      return;
    }

    if (suggestion.mode) {
      setChatMode(suggestion.mode);
      if (suggestion.mode === "compare") setCompareMode(true);
    }

    setQ(suggestion.prompt);
  }

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
    if (user) void pushNote(note);
    setSavedReplies((prev) => new Set(prev).add(index));
  }

  async function ask() {
    if (!q.trim() || busy || dailyCapHit || !accessToken) return;
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
        {
          verseId: pinnedVerse?._id,
          compareVerseIds,
          layerFocus: layerFocus || undefined,
          chatMode,
          accessToken,
        },
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
      recordPractice(pinnedVerse?._id ? `chat:${pinnedVerse._id}` : "chat:ask");
      if (compareMode) recordPractice("chat:compare");
      if (typeof data.remaining === "number") setChatRemaining(data.remaining);
      // Ensure final state matches (covers the no-delta error path).
      setMessages((prev) => {
        const copy = [...prev];
        copy[assistantIdx] = { role: "assistant", content: data.answer || "(no answer)" };
        return copy;
      });
    } catch (err) {
      const isDailyCap = err instanceof ChatApiError && err.code === "daily_cap";
      if (isDailyCap) {
        setDailyCapHit(true);
        setChatRemaining(0);
      }
      const msg = isDailyCap
        ? t("chat.dailyCap")
        : err instanceof Error
          ? err.message
          : "Unknown error";
      setMessages((prev) => {
        const copy = [...prev];
        copy[assistantIdx] = {
          role: "assistant",
          content: isDailyCap ? msg : `I hit an error: ${msg}`,
        };
        return copy;
      });
      setSources([]);
      setCompareWarning("");
    } finally {
      setBusy(false);
    }
  }

  const showComposerSuggestions = !q.trim() && !dailyCapHit && !busy;
  const showSourceShelf = sources.length > 0 || Boolean(compareWarning);
  const fromGate = Boolean(backHref && (backHref === "/" || backHref.startsWith("/learn")));
  const backLabel = backHref === "/" ? "← Today" : "← Back to path";

  return (
    <main className="page-shell page-shell--reading">
      <header className="library-header">
        <div className="library-header__atmosphere" aria-hidden>
          <ArtBackdrop
            srcs={pinnedVerse ? collectionArtPool(pinnedVerse.collection) : generatedArtPool("heart-sutra")}
            variant="subtle"
            opacity={0.11}
          />
        </div>
        <div className="library-header__body">
          {backHref ? (
            <Link href={backHref} className="passage-reading__toggle">
              {backLabel}
            </Link>
          ) : null}
          <p className="passage-reading__meta">
            {fromGate ? t("chat.thisGate") : t("chat.meta")}
          </p>
          <h1 className="library-header__title">{t("chat.title")}</h1>
          <p className="library-header__lede">
            {fromGate && pinnedVerse
              ? t("chat.ledeGate")
              : pinnedVerse
                ? t("chat.ledePinned")
                : t("chat.lede")}
          </p>
        </div>
      </header>

      <div className="mt-6 max-w-[var(--reading-measure)]">
        {pinnedVerse ? (
          <div className="chat-study-pin mb-5">
            <Link
              href={`/read/${encodeURIComponent(pinnedVerse._id)}`}
              className="chat-study-pin__link"
            >
              <p className="passage-reading__meta !mb-0">{fromGate ? t("chat.thisGate") : t("chat.studying")}</p>
              <p className="chat-study-pin__title">{pinnedTitle}</p>
              {pinnedSourceLine ? (
                <p className="chat-study-pin__meta">{pinnedSourceLine}</p>
              ) : null}
            </Link>
          </div>
        ) : null}

        {messages.length > 0 ? (
          <div className="mb-6 space-y-4">
            {messages.map((m, idx) => (
              <article
                key={`${m.role}-${idx}`}
                className="whitespace-pre-wrap border-t border-[rgb(240_201_121_/_0.12)] py-4"
              >
                <p className="passage-layer__label mb-2">{m.role === "user" ? t("chat.you") : t("brand.name")}</p>
                {m.role === "assistant" ? (
                  <>
                    {m.content ? (
                      <div className="chat-markdown reading-prose">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
                      </div>
                    ) : (
                      <p className="soft animate-pulse text-sm">{t("chat.thinking")}</p>
                    )}
                    {m.content ? (
                      <Button
                        type="button"
                        variant="secondary"
                        size="sm"
                        className="mt-3 text-xs"
                        onClick={() => saveReply(idx, m.content)}
                        disabled={savedReplies.has(idx)}
                      >
                        {savedReplies.has(idx) ? t("chat.savedJournal") : t("chat.saveJournal")}
                      </Button>
                    ) : null}
                  </>
                ) : (
                  <p className="reading-prose">{m.content}</p>
                )}
              </article>
            ))}
          </div>
        ) : null}

        {dailyCapHit ? (
          <p className="mb-4 border-t border-[rgb(240_201_121_/_0.14)] pt-4 text-sm leading-relaxed text-stone-200">
            {t("chat.dailyCap")}{" "}
            <Link href="/read" className="text-amber-100 underline-offset-2 hover:underline">
              {t("chat.continueReading")}
            </Link>
          </p>
        ) : null}

        <div className={`chat-composer ${showComposerSuggestions ? "chat-composer--suggest" : ""}`}>
          <Textarea
            className="chat-composer__field"
            rows={4}
            value={q}
            onChange={(e) => setQ(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
                e.preventDefault();
                void ask();
              }
            }}
            placeholder={
              pinnedVerse
                ? t("chat.askPinned", { ref: pinnedRef || t("chat.thisPassage") })
                : t("chat.askOpen")
            }
            disabled={dailyCapHit}
            aria-label={t("chat.askLabel")}
          />
          {showComposerSuggestions ? (
            <ul className="chat-composer__suggestions" aria-label={t("chat.suggestions")}>
              {suggestions.map((s) => (
                <li key={s.id}>
                  <button
                    type="button"
                    className="chat-composer__suggestion"
                    onClick={() => void applySuggestion(s)}
                  >
                    {s.label}
                  </button>
                </li>
              ))}
            </ul>
          ) : null}
        </div>

        <div className="mt-3 flex flex-wrap items-center gap-3">
          <Button onClick={ask} disabled={busy || dailyCapHit || !q.trim()}>
            {busy ? t("chat.thinkingShort") : t("chat.ask")}
          </Button>
          {chatRemaining != null && chatRemaining >= 0 && !dailyCapHit ? (
            <p className="soft font-sans text-xs">
              {chatRemaining === 1
                ? t("chat.chatsLeftOne", { n: chatRemaining })
                : t("chat.chatsLeftMany", { n: chatRemaining })}
            </p>
          ) : null}
        </div>

        <div className="mt-6">
          <Disclosure
            summary={pinnedVerse ? t("chat.studyOptions") : t("chat.retrievalCompare")}
            hint={`${chatMode}${pinnedVerse && layerFocus ? ` · ${layerFocus}` : ""}${useRag ? ` · ${t("chat.grounded")}` : ` · ${t("chat.freeform")}`}${compareMode ? ` · ${t("chat.modeCompare")}` : ""}`}
            defaultOpen={compareMode}
          >
            {pinnedVerse ? (
              <div className="mb-4 grid gap-3 sm:grid-cols-2">
                <FilterSelect
                  label={t("chat.studyMode")}
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
                  label={t("chat.layerFocus")}
                  tone="lapis"
                  value={layerFocus}
                  onChange={(value) => setLayerFocus(value as PratibhaLayerKind | "")}
                  options={layerOptions}
                />
              </div>
            ) : null}
            <label className="block font-sans text-sm soft">
              <input type="checkbox" checked={useRag} onChange={(e) => setUseRag(e.target.checked)} className="mr-2 accent-amber-300" />
              {t("chat.useRag")}
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
              {t("chat.compareToggle")}
            </label>
            {compareMode ? (
              <>
                <div className="mt-4 flex flex-wrap gap-2">
                  {COMPARE_PRESETS.map((preset) => (
                    <Button
                      key={preset.id}
                      type="button"
                      variant="secondary"
                      size="sm"
                      className="text-xs"
                      onClick={() => applyPreset(preset.id)}
                    >
                      {preset.label}
                    </Button>
                  ))}
                </div>
                <div className="mt-4 grid gap-3 sm:grid-cols-2">
                  <div className="space-y-3">
                    <FilterSelect
                      label={t("chat.voiceAText")}
                      tone="gold"
                      value={compareA}
                      onChange={setCompareA}
                      options={collectionOptions.map((o) => ({ ...o, label: `A · ${o.label}` }))}
                    />
                    <ComparePassageSelect
                      label={t("chat.voiceAPassage")}
                      tone="gold"
                      collection={compareA}
                      passages={passagesA}
                      value={compareVerseA}
                      onChange={setCompareVerseA}
                    />
                  </div>
                  <div className="space-y-3">
                    <FilterSelect
                      label={t("chat.voiceBText")}
                      tone="lapis"
                      value={compareB}
                      onChange={setCompareB}
                      options={collectionOptions.map((o) => ({ ...o, label: `B · ${o.label}` }))}
                    />
                    <ComparePassageSelect
                      label={t("chat.voiceBPassage")}
                      tone="lapis"
                      collection={compareB}
                      passages={passagesB}
                      value={compareVerseB}
                      onChange={setCompareVerseB}
                    />
                  </div>
                </div>
              </>
            ) : null}
          </Disclosure>
        </div>

        {showSourceShelf ? (
          <aside className="mt-8 border-t border-[rgb(240_201_121_/_0.14)] pt-5">
            <h2 className="passage-reading__meta">{t("chat.sourceShelf")}</h2>
            {compareMode && compareWarning ? (
              <p className="mt-2 text-xs text-amber-100/90">{compareWarning}</p>
            ) : null}
            <div className="mt-2">
              {sources.map((s) => {
                const href = sourcePassageHref(s.metadata);
                const side = (s.metadata?.compare_side as string | undefined) || "";
                const meta = (
                  <p className="library-passage__meta">
                    {t("chat.sourceRank", { rank: s.rank })}
                    {side ? ` · ${t("chat.voice", { side })}` : ""}
                    {displayCollectionName(String((s.metadata?.collection as string) || ""))
                      ? ` · ${displayCollectionName(String((s.metadata?.collection as string) || ""))}`
                      : ""}
                    {sourcePassageLabel(s.metadata) ? ` · ${sourcePassageLabel(s.metadata)}` : ""}
                  </p>
                );
                const body = (
                  <p className="library-passage__preview line-clamp-5">{s.text || ""}</p>
                );
                if (href) {
                  return (
                    <Link key={`source-${s.rank}`} href={href} className="library-passage block">
                      {meta}
                      {body}
                    </Link>
                  );
                }
                return (
                  <article key={`source-${s.rank}`} className="library-passage">
                    {meta}
                    {body}
                  </article>
                );
              })}
            </div>
          </aside>
        ) : null}
      </div>
    </main>
  );
}
