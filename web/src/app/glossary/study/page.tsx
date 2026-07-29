"use client";

import Link from "next/link";
import { useCallback, useEffect, useMemo, useState } from "react";
import { getLexiconStudy } from "@/lib/api";
import {
  buildSessionQueue,
  deckStats,
  gradeCard,
  loadSrsMap,
  modeLabel,
  saveSrsMap,
  scriptClassName,
} from "@/lib/lexiconStudy";
import type {
  LexiconStudyPayload,
  SrsEntry,
  SrsGrade,
  StudyCard,
  StudyDeck,
  StudyDeckId,
} from "@/lib/lexiconStudyTypes";
import { InlineMarkdown } from "@/components/InlineMarkdown";

type Phase = "pick" | "session" | "done";

const GRADE_KEYS: { grade: SrsGrade; label: string; hint: string; key: string }[] = [
  { grade: "again", label: "Again", hint: "missed", key: "1" },
  { grade: "hard", label: "Hard", hint: "struggled", key: "2" },
  { grade: "good", label: "Good", hint: "knew it", key: "3" },
  { grade: "easy", label: "Easy", hint: "instant", key: "4" },
];

function FlipCard({
  card,
  flipped,
  onFlip,
}: {
  card: StudyCard;
  flipped: boolean;
  onFlip: () => void;
}) {
  const frontNative = card.front.native;
  const frontRoman = card.front.roman;
  const backNative = card.back.native || frontNative;
  const backRoman = card.back.roman || frontRoman;
  const backScript = card.back.script_class || card.front.script_class;

  return (
    <button
      type="button"
      className={`lex-flip ${flipped ? "lex-flip--flipped" : ""}`}
      onClick={onFlip}
      aria-pressed={flipped}
      aria-label={flipped ? "Hide answer" : "Reveal answer"}
    >
      <div className="lex-flip__inner">
        <div className="lex-flip__face lex-flip__face--front">
          <p className="lex-flip__mode">{modeLabel(card.mode)}</p>
          {card.mode === "trap" ? (
            <>
              <p className="lex-flip__prompt">{card.front.prompt}</p>
              <blockquote className="lex-flip__trap">
                <InlineMarkdown>{card.front.trap || ""}</InlineMarkdown>
              </blockquote>
              {(frontNative || frontRoman) && (
                <p className="lex-flip__term-hint">
                  {frontNative ? (
                    <span className={scriptClassName(card.front.script_class)}>{frontNative}</span>
                  ) : null}
                  {frontNative && frontRoman ? <span className="lex-flip__dot">·</span> : null}
                  {frontRoman ? (
                    <span className="source-script source-script--latin">{frontRoman}</span>
                  ) : null}
                </p>
              )}
            </>
          ) : card.mode === "production" ? (
            <>
              <p className="lex-flip__prompt">{card.front.prompt}</p>
              {card.front.sense_label ? (
                <p className="lex-flip__sense-label">{card.front.sense_label}</p>
              ) : null}
              <p className="lex-flip__cue soft">
                <InlineMarkdown>{card.front.cue || ""}</InlineMarkdown>
              </p>
            </>
          ) : (
            <>
              <p className="lex-flip__prompt">{card.front.prompt}</p>
              {frontNative ? (
                <p
                  className={`lex-flip__native ${scriptClassName(card.front.script_class)}`}
                  dir={card.front.script_class === "arabic" ? "rtl" : undefined}
                >
                  {frontNative}
                </p>
              ) : null}
              {frontRoman ? (
                <p className="lex-flip__roman source-script source-script--latin">{frontRoman}</p>
              ) : null}
            </>
          )}
          <p className="lex-flip__hint">Tap or press Space to reveal</p>
        </div>

        <div className="lex-flip__face lex-flip__face--back" aria-hidden={!flipped}>
          <p className="lex-flip__mode">{modeLabel(card.mode)} · answer</p>
          {card.mode === "production" ? (
            <>
              {backNative ? (
                <p
                  className={`lex-flip__native ${scriptClassName(backScript)}`}
                  dir={backScript === "arabic" ? "rtl" : undefined}
                >
                  {backNative}
                </p>
              ) : null}
              {backRoman ? (
                <p className="lex-flip__roman source-script source-script--latin">{backRoman}</p>
              ) : null}
            </>
          ) : (
            <h2 className="lex-flip__label">{card.back.label}</h2>
          )}
          {card.mode === "trap" && card.back.correction ? (
            <p className="lex-flip__correction">{card.back.correction}</p>
          ) : null}
          <p className="lex-flip__short soft">
            <InlineMarkdown>{card.back.short}</InlineMarkdown>
          </p>
          {card.back.etymology ? (
            <p className="lex-flip__etym">
              <span>Etymology.</span> <InlineMarkdown>{card.back.etymology}</InlineMarkdown>
            </p>
          ) : null}
          {(card.back.traps || []).length > 0 && card.mode !== "trap" ? (
            <ul className="lex-flip__traps">
              {(card.back.traps || []).slice(0, 2).map((t) => (
                <li key={t}>
                  <InlineMarkdown>{t}</InlineMarkdown>
                </li>
              ))}
            </ul>
          ) : null}
        </div>
      </div>
    </button>
  );
}

function DeckTile({
  deck,
  stats,
  onSelect,
}: {
  deck: StudyDeck;
  stats: { due: number; new: number; total: number };
  onSelect: () => void;
}) {
  return (
    <button type="button" className="lex-deck" onClick={onSelect}>
      <span className="lex-deck__sample" aria-hidden="true">
        {deck.sample}
      </span>
      <span className="lex-deck__body">
        <span className="lex-deck__eyebrow">{deck.native_label}</span>
        <span className="lex-deck__title">{deck.label}</span>
        <span className="lex-deck__blurb">{deck.blurb}</span>
        <span className="lex-deck__meta">
          <span>
            {stats.due > 0 ? `${stats.due} due` : "Caught up"}
            {stats.new > 0 ? ` · ${Math.min(stats.new, 12)} new ready` : ""}
          </span>
          <span>
            {deck.lemma_count} lemmas · {deck.card_count} cards
          </span>
        </span>
      </span>
    </button>
  );
}

export default function GlossaryStudyPage() {
  const [payload, setPayload] = useState<LexiconStudyPayload | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [srs, setSrs] = useState<Record<string, SrsEntry>>({});
  const [phase, setPhase] = useState<Phase>("pick");
  const [activeDeck, setActiveDeck] = useState<StudyDeck | null>(null);
  const [queue, setQueue] = useState<StudyCard[]>([]);
  const [index, setIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [graded, setGraded] = useState(0);
  const [sessionAgain, setSessionAgain] = useState(0);

  useEffect(() => {
    setSrs(loadSrsMap());
    let active = true;
    setLoading(true);
    getLexiconStudy("strong_draft")
      .then((data) => {
        if (!active) return;
        setPayload(data);
      })
      .catch(() => {
        if (!active) return;
        setError("Could not load lexicon study decks. Is the Pratibha backend online?");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const cards = payload?.cards || [];

  const startDeck = useCallback(
    (deck: StudyDeck) => {
      const map = loadSrsMap();
      setSrs(map);
      const q = buildSessionQueue(cards, deck.id as StudyDeckId, map, 18);
      if (q.length === 0) return;
      setActiveDeck(deck);
      setQueue(q);
      setIndex(0);
      setFlipped(false);
      setGraded(0);
      setSessionAgain(0);
      setPhase("session");
    },
    [cards],
  );

  const current = queue[index] || null;
  const progress = queue.length ? ((index + (flipped ? 0.5 : 0)) / queue.length) * 100 : 0;

  const onGrade = useCallback(
    (grade: SrsGrade) => {
      if (!current || !flipped) return;
      const nextMap = gradeCard(srs, current.id, grade);
      setSrs(nextMap);
      saveSrsMap(nextMap);
      setGraded((n) => n + 1);
      if (grade === "again") setSessionAgain((n) => n + 1);

      if (index + 1 >= queue.length) {
        setPhase("done");
        return;
      }
      setIndex((i) => i + 1);
      setFlipped(false);
    },
    [current, flipped, index, queue.length, srs],
  );

  useEffect(() => {
    if (phase !== "session") return;
    function onKey(e: KeyboardEvent) {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;
      if (e.key === " " || e.key === "Enter") {
        e.preventDefault();
        if (!flipped) setFlipped(true);
        return;
      }
      if (!flipped) return;
      const hit = GRADE_KEYS.find((g) => g.key === e.key);
      if (hit) {
        e.preventDefault();
        onGrade(hit.grade);
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [phase, flipped, onGrade]);

  const deckTiles = useMemo(() => {
    if (!payload) return [];
    return payload.decks.map((deck) => ({
      deck,
      stats: deckStats(cards, deck.id as StudyDeckId, srs),
    }));
  }, [payload, cards, srs]);

  return (
    <main className="page-shell max-w-3xl">
      <p className="mb-6">
        <Link
          href="/glossary"
          className="font-sans text-sm text-amber-200/80 underline decoration-amber-200/25 underline-offset-4 transition hover:text-amber-100 hover:decoration-amber-200/60"
        >
          ← Glossary
        </Link>
      </p>

      {phase === "pick" ? (
        <>
          <header className="lex-study-hero">
            <p className="eyebrow">Sacred lexicon</p>
            <h1 className="lex-study-hero__title">Build the terms</h1>
            <p className="soft mt-4 max-w-2xl text-xl leading-relaxed">
              Decks by language. Cards by sense. Recognize the script, catch the trap, produce the form —
              then return to the passage that holds it.
            </p>
          </header>

          <div className="ornament my-8" />

          {loading ? (
            <p className="soft text-lg">Opening the decks…</p>
          ) : error ? (
            <section className="py-8 text-center">
              <p className="text-2xl text-amber-100">Study unavailable</p>
              <p className="soft mx-auto mt-3 max-w-md">{error}</p>
            </section>
          ) : (
            <div className="lex-deck-grid">
              {deckTiles.map(({ deck, stats }) => (
                <DeckTile key={deck.id} deck={deck} stats={stats} onSelect={() => startDeck(deck)} />
              ))}
            </div>
          )}

          {payload ? (
            <p className="soft mt-8 font-sans text-xs tracking-wide text-stone-500">
              {payload.totals.lemmas} lemmas · {payload.totals.cards} cards · progress saved on this
              device
            </p>
          ) : null}
        </>
      ) : null}

      {phase === "session" && current && activeDeck ? (
        <section className="lex-session">
          <header className="lex-session__bar">
            <button
              type="button"
              className="lex-session__back"
              onClick={() => setPhase("pick")}
            >
              ← {activeDeck.label}
            </button>
            <p className="lex-session__count">
              {index + 1} / {queue.length}
            </p>
          </header>
          <div className="lex-session__progress" aria-hidden="true">
            <span style={{ width: `${progress}%` }} />
          </div>

          <FlipCard card={current} flipped={flipped} onFlip={() => setFlipped((v) => !v)} />

          <div className="lex-session__footer">
            {flipped ? (
              <>
                <div className="lex-grades" role="group" aria-label="How well did you know this?">
                  {GRADE_KEYS.map((g) => (
                    <button
                      key={g.grade}
                      type="button"
                      className={`lex-grade lex-grade--${g.grade}`}
                      onClick={() => onGrade(g.grade)}
                    >
                      <span className="lex-grade__key">{g.key}</span>
                      <span className="lex-grade__label">{g.label}</span>
                      <span className="lex-grade__hint">{g.hint}</span>
                    </button>
                  ))}
                </div>
                <p className="lex-session__links">
                  <Link href={`/glossary/${encodeURIComponent(current.lemma_id)}`}>
                    Open lemma
                  </Link>
                  {(current.back.exemplars || [])[0] ? (
                    <>
                      <span aria-hidden="true">·</span>
                      <Link href={`/read/${encodeURIComponent(current.back.exemplars![0])}`}>
                        Exemplar passage
                      </Link>
                    </>
                  ) : null}
                </p>
              </>
            ) : (
              <button type="button" className="btn-primary px-6 py-2.5" onClick={() => setFlipped(true)}>
                Reveal
              </button>
            )}
          </div>
        </section>
      ) : null}

      {phase === "done" && activeDeck ? (
        <section className="lex-done">
          <p className="eyebrow">{activeDeck.label}</p>
          <h1 className="lex-study-hero__title">Session complete</h1>
          <p className="soft mt-4 text-xl leading-relaxed">
            {graded} card{graded === 1 ? "" : "s"} reviewed
            {sessionAgain > 0 ? ` · ${sessionAgain} marked again` : " · clean pass"}.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <button type="button" className="btn-primary px-6 py-2.5" onClick={() => startDeck(activeDeck)}>
              Study again
            </button>
            <button type="button" className="btn-secondary px-6 py-2.5" onClick={() => setPhase("pick")}>
              Choose another deck
            </button>
          </div>
          <p className="soft mt-8 font-sans text-sm">
            <Link
              href="/glossary"
              className="text-amber-200/80 underline decoration-amber-200/25 underline-offset-4 hover:text-amber-100"
            >
              Return to glossary
            </Link>
          </p>
        </section>
      ) : null}
    </main>
  );
}
