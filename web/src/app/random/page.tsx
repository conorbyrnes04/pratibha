'use client';

import Link from "next/link";
import { useEffect, useState } from "react";
import { getRandom, getVerses } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { displayCollectionName } from "@/lib/collectionLabels";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function RandomPage() {
  const [item, setItem] = useState<VerseItem | null>(null);
  const [collection, setCollection] = useState("all");
  const [collections, setCollections] = useState<string[]>(["all"]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [allItems, setAllItems] = useState<VerseItem[]>([]);

  useEffect(() => {
    getVerses()
      .then((items) => {
        setAllItems(items);
        const set = new Set(items.map((x) => (x.collection || "Unknown").trim()));
        setCollections(["all", ...Array.from(set).sort((a, b) => a.localeCompare(b))]);
      })
      .catch(() => {
        setError("Could not load the text library from the API.");
      });
  }, []);

  async function nextOne(selected: string) {
    setLoading(true);
    setError("");
    try {
      const c = selected === "all" ? undefined : selected;
      const v = await getRandom(c);
      if (v) {
        setItem(v);
        return;
      }
      // Fallback: pick locally from the already loaded library if /random returns empty.
      const pool =
        selected === "all"
          ? allItems
          : allItems.filter((x) => (x.collection || "Unknown").trim() === selected);
      if (pool.length > 0) {
        setItem(pool[Math.floor(Math.random() * pool.length)]);
        return;
      }
      setItem(null);
      setError("No passages are available for this selection yet.");
    } catch {
      setItem(null);
      setError("Random discovery is temporarily unavailable. Please retry.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void nextOne("all");
    // Trigger initial load once.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [allItems.length]);

  return (
    <main className="mx-auto max-w-4xl px-4 py-8">
      <h1 className="text-3xl text-amber-200">Random Discovery</h1>
      <p className="soft mt-2">Let the text choose you, then dive deeper.</p>

      <div className="mt-5 flex flex-wrap items-center gap-3">
        <select
          value={collection}
          onChange={(e) => {
            const value = e.target.value;
            setCollection(value);
            void nextOne(value);
          }}
          className="rounded-lg border border-white/15 bg-slate-950/70 px-3 py-2"
        >
          {collections.map((c) => (
            <option key={c} value={c}>
              {c === "all" ? "All collections" : displayCollectionName(c)}
            </option>
          ))}
        </select>
        <button onClick={() => nextOne(collection)} className="rounded-lg bg-amber-300 px-4 py-2 font-semibold text-slate-900">
          Another one
        </button>
        <Link href="/" className="rounded-lg border border-amber-200/30 px-4 py-2 text-amber-100">
          Home
        </Link>
        <Link href="/read" className="rounded-lg border border-amber-200/30 px-4 py-2 text-amber-100">
          Library
        </Link>
      </div>

      {loading ? (
        <p className="soft mt-6">Finding a passage...</p>
      ) : error ? (
        <section className="card mt-6 p-5">
          <p className="text-amber-100">{error}</p>
          <div className="mt-4">
            <button onClick={() => nextOne(collection)} className="rounded-lg bg-amber-300 px-4 py-2 font-semibold text-slate-900">
              Retry
            </button>
          </div>
        </section>
      ) : item ? (
        <section className="card mt-6 p-5">
          <h2 className="text-xl text-amber-100">{item.title || item.sutra_id || item._id}</h2>
          <p className="soft mt-1 text-sm">
            {displayCollectionName(item.collection)} {item.section ? `• ${item.section}` : ""}
          </p>
          {item.sanskrit ? <p className="mt-3 whitespace-pre-wrap text-xl leading-relaxed">{item.sanskrit}</p> : null}
          {item.transliteration ? <p className="soft mt-2 whitespace-pre-wrap italic">{item.transliteration}</p> : null}
          <div className="chat-markdown mt-4 leading-relaxed">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{item.translation || item.commentary || ""}</ReactMarkdown>
          </div>
          {item.themes && item.themes.length > 0 ? (
            <div className="mt-4 flex flex-wrap gap-2">
              {item.themes.slice(0, 6).map((t) => (
                <span key={t} className="rounded-full border border-amber-200/30 px-3 py-1 text-xs text-amber-100">
                  {t}
                </span>
              ))}
            </div>
          ) : null}
          <div className="mt-5 flex flex-wrap gap-3">
            <Link href={`/read/${encodeURIComponent(item._id)}`} className="rounded-lg bg-amber-300 px-4 py-2 font-semibold text-slate-900">
              Open full page
            </Link>
            <Link
              href={`/chat?q=${encodeURIComponent(
                `Study this passage from ${displayCollectionName(item.collection)}: ${item.title || item.sutra_id || item._id}. Explain simply, key insights, and one practice.`,
              )}`}
              className="rounded-lg border border-amber-200/30 px-4 py-2 text-amber-100"
            >
              Study this passage
            </Link>
          </div>
        </section>
      ) : (
        <p className="soft mt-6">No random passage available yet. Try Library to pick one directly.</p>
      )}
    </main>
  );
}

