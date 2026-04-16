'use client';

import Link from "next/link";
import { useEffect, useState } from "react";
import { getDaily } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { firstSentence, stripMarkdown } from "@/lib/textPreview";
import { displayCollectionName } from "@/lib/collectionLabels";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function DailyPage() {
  const [item, setItem] = useState<VerseItem | null>(null);

  useEffect(() => {
    getDaily().then(setItem).catch(() => setItem(null));
  }, []);

  if (!item) {
    return <main className="mx-auto max-w-4xl px-4 py-8 soft">No daily passage available yet.</main>;
  }

  return (
    <main className="mx-auto max-w-4xl px-4 py-8">
      <h1 className="text-3xl text-amber-200">Daily Passage</h1>
      <p className="soft mt-2">
        {displayCollectionName(item.collection)} {item.section ? `• ${item.section}` : ""}
      </p>
      <section className="card mt-6 p-5">
        <h2 className="text-xl text-amber-100">{item.title || item.sutra_id || item._id}</h2>
        <div className="soft mt-3 space-y-2 rounded-md border border-white/10 bg-slate-950/30 p-3 text-sm">
          <p><span className="text-amber-100">Core idea:</span> {firstSentence(item.translation || item.commentary || "")}</p>
          <p><span className="text-amber-100">Why it matters:</span> {firstSentence(item.commentary || item.translation || "")}</p>
          <p><span className="text-amber-100">Practice:</span> {stripMarkdown(item.abhyasa || "Read once slowly, then carry one line into your next conversation.")}</p>
        </div>
        <div className="chat-markdown mt-3 leading-relaxed">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{item.translation || item.commentary || ""}</ReactMarkdown>
        </div>
      </section>
      {item.themes && item.themes.length > 0 ? (
        <div className="mt-4 flex flex-wrap gap-2">
          {item.themes.map((t) => (
            <Link key={t} href={`/read?theme=${encodeURIComponent(t)}`} className="rounded-full border border-amber-200/30 px-3 py-1 text-xs text-amber-100">
              {t}
            </Link>
          ))}
        </div>
      ) : null}
      <div className="mt-6">
        <Link href={`/read/${encodeURIComponent(item._id)}`} className="rounded-lg bg-amber-300 px-4 py-2 font-semibold text-slate-900">
          Open full study page
        </Link>
      </div>
    </main>
  );
}

