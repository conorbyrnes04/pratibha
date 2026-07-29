"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { getLexicon } from "@/lib/api";
import type { LexiconListItem } from "@/lib/lexiconTypes";
import {
  nativeScript,
  nativeScriptClass,
  romanization,
  traditionLabel,
} from "@/lib/lexiconDisplay";

function fold(s: string): string {
  return s
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase();
}

function matchesQuery(item: LexiconListItem, needle: string): boolean {
  if (!needle) return true;
  const hay = [
    item.id,
    item.short,
    ...(item.aliases || []),
    ...(item.traditions || []),
    ...Object.values(item.scripts || {}),
  ]
    .filter(Boolean)
    .map((x) => fold(String(x)))
    .join(" ");
  return hay.includes(needle);
}

export default function GlossaryPage() {
  const [items, setItems] = useState<LexiconListItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [q, setQ] = useState("");
  const [tradition, setTradition] = useState("all");

  useEffect(() => {
    let active = true;
    setLoading(true);
    setError("");
    getLexicon({ limit: 500 })
      .then((data) => {
        if (!active) return;
        setItems(data.items);
        if (data.items.length === 0) {
          setError("The lexicon is empty — lemmas may still be loading on the server.");
        }
      })
      .catch(() => {
        if (!active) return;
        setItems([]);
        setError("Could not reach the lexicon API. Is the Pratibha backend online?");
      })
      .finally(() => {
        if (active) setLoading(false);
      });
    return () => {
      active = false;
    };
  }, []);

  const traditions = useMemo(() => {
    const set = new Set<string>();
    for (const item of items) {
      for (const t of item.traditions || []) {
        if (t.trim()) set.add(t.trim());
      }
    }
    return [...set].sort((a, b) => a.localeCompare(b));
  }, [items]);

  const filtered = useMemo(() => {
    const needle = fold(q.trim());
    return items.filter((item) => {
      if (tradition !== "all" && !(item.traditions || []).includes(tradition)) return false;
      return matchesQuery(item, needle);
    });
  }, [items, q, tradition]);

  return (
    <main className="page-shell max-w-3xl">
      <header>
        <p className="eyebrow">Shared lexicon</p>
        <h1 className="mt-3 text-5xl font-semibold leading-none tracking-[-0.04em] text-stone-100 sm:text-6xl">
          Glossary
        </h1>
        <p className="soft mt-4 max-w-2xl text-xl leading-relaxed">
          Terms that do philosophical work across the manuscript — senses by tradition, not a flat dictionary.
        </p>
        <p className="mt-5">
          <Link href="/glossary/study" className="btn-secondary inline-flex px-5 py-2.5 text-sm">
            Study by language →
          </Link>
        </p>
      </header>

      <div className="mt-8 space-y-4">
        <label className="block">
          <span className="sr-only">Search glossary</span>
          <input
            value={q}
            onChange={(e) => setQ(e.target.value)}
            className="input-field w-full rounded-lg px-3 py-2.5"
            placeholder="Search lemmas, scripts, aliases…"
            autoComplete="off"
            spellCheck={false}
          />
        </label>

        {traditions.length > 0 ? (
          <div className="glossary-filters" role="group" aria-label="Filter by tradition">
            <button
              type="button"
              onClick={() => setTradition("all")}
              className={`glossary-filter ${tradition === "all" ? "glossary-filter--active" : ""}`}
            >
              All
            </button>
            {traditions.map((t) => (
              <button
                key={t}
                type="button"
                onClick={() => setTradition(t)}
                className={`glossary-filter ${tradition === t ? "glossary-filter--active" : ""}`}
              >
                {traditionLabel(t)}
              </button>
            ))}
          </div>
        ) : null}
      </div>

      <p className="soft mt-4 font-sans text-xs tracking-wide text-stone-500">
        {loading
          ? "Loading lexicon…"
          : error && items.length === 0
            ? null
            : `${filtered.length} ${filtered.length === 1 ? "lemma" : "lemmas"}`}
      </p>

      <div className="mt-6">
        {loading ? (
          <p className="soft text-lg">Opening the lexicon…</p>
        ) : error && items.length === 0 ? (
          <section className="py-10 text-center">
            <p className="text-2xl text-amber-100">Lexicon unavailable</p>
            <p className="soft mx-auto mt-3 max-w-md">{error}</p>
          </section>
        ) : filtered.length === 0 ? (
          <section className="py-10 text-center">
            <p className="text-2xl text-amber-100">No matching lemmas</p>
            <p className="soft mx-auto mt-3 max-w-md">
              Try another spelling, drop a diacritic, or clear the tradition filter.
            </p>
          </section>
        ) : (
          <ul className="glossary-list">
            {filtered.map((item) => {
              const native = nativeScript(item.scripts);
              const roman = romanization(item.scripts) || item.id;
              const short = item.short?.trim() || "";
              return (
                <li key={item.id}>
                  <Link href={`/glossary/${encodeURIComponent(item.id)}`} className="glossary-row">
                    <span className="glossary-row__head">
                      {native ? (
                        <span className={`glossary-row__native ${nativeScriptClass(item.scripts)}`}>
                          {native}
                        </span>
                      ) : null}
                      <span className="glossary-row__roman source-script source-script--latin">
                        {roman}
                      </span>
                    </span>
                    {short ? <span className="glossary-row__short soft">{short}</span> : null}
                    {(item.traditions || []).length > 0 ? (
                      <span className="glossary-row__meta">
                        {(item.traditions || []).map(traditionLabel).join(" · ")}
                      </span>
                    ) : null}
                  </Link>
                </li>
              );
            })}
          </ul>
        )}
      </div>
    </main>
  );
}
