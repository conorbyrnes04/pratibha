'use client';

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { getVerses } from "@/lib/api";
import { LEARNING_TRACKS } from "@/lib/learningPaths";
import type { VerseItem } from "@/lib/types";
import { displayCollectionName } from "@/lib/collectionLabels";

const STORAGE_KEY = "pratibha.learn.v1";

type ProgressMap = Record<string, boolean>;

function stepKey(trackId: string, stepId: string): string {
  return `${trackId}:${stepId}`;
}

function matchStepItem(step: { theme?: string; collection?: string }, items: VerseItem[]): VerseItem | null {
  const filtered = items.filter((v) => {
    const okCollection = !step.collection || (v.collection || "").trim() === step.collection;
    const okTheme = !step.theme || (v.themes || []).includes(step.theme);
    return okCollection && okTheme;
  });
  return filtered[0] || null;
}

export default function LearnPage() {
  const [items, setItems] = useState<VerseItem[]>([]);
  const [selectedTrackId, setSelectedTrackId] = useState(LEARNING_TRACKS[0].id);
  const [progress, setProgress] = useState<ProgressMap>({});

  useEffect(() => {
    getVerses().then(setItems).catch(() => setItems([]));
  }, []);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return;
      const parsed = JSON.parse(raw) as ProgressMap;
      setProgress(parsed || {});
    } catch {
      setProgress({});
    }
  }, []);

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
  }, [progress]);

  const track = useMemo(() => LEARNING_TRACKS.find((t) => t.id === selectedTrackId) || LEARNING_TRACKS[0], [selectedTrackId]);
  const completed = track.steps.filter((s) => progress[stepKey(track.id, s.id)]).length;
  const pct = Math.round((completed / Math.max(1, track.steps.length)) * 100);

  function toggle(trackId: string, stepId: string) {
    const key = stepKey(trackId, stepId);
    setProgress((p) => ({ ...p, [key]: !p[key] }));
  }

  function resetTrack(trackId: string) {
    setProgress((p) => {
      const next = { ...p };
      for (const s of LEARNING_TRACKS.find((t) => t.id === trackId)?.steps || []) {
        delete next[stepKey(trackId, s.id)];
      }
      return next;
    });
  }

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <h1 className="text-3xl text-amber-200">Learning Paths</h1>
      <p className="soft mt-2">Follow a guided sequence: understand, connect, practice, integrate.</p>

      <div className="mt-6 grid gap-5 lg:grid-cols-[1fr_2fr]">
        <aside className="card h-fit p-4">
          <h2 className="text-lg text-amber-100">Tracks</h2>
          <div className="mt-3 space-y-2">
            {LEARNING_TRACKS.map((t) => {
              const done = t.steps.filter((s) => progress[stepKey(t.id, s.id)]).length;
              return (
                <button
                  key={t.id}
                  onClick={() => setSelectedTrackId(t.id)}
                  className={`w-full rounded-md border p-3 text-left ${
                    selectedTrackId === t.id ? "border-amber-200/60 bg-amber-100/5" : "border-white/10"
                  }`}
                >
                  <p className="text-sm text-amber-100">{t.title}</p>
                  <p className="soft mt-1 text-xs">
                    {t.level} • {done}/{t.steps.length} complete
                  </p>
                </button>
              );
            })}
          </div>
        </aside>

        <section className="card p-5">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="text-2xl text-amber-100">{track.title}</h2>
              <p className="soft mt-1 text-sm">{track.description}</p>
            </div>
            <button onClick={() => resetTrack(track.id)} className="rounded-md border border-amber-200/30 px-3 py-2 text-xs text-amber-100">
              Reset progress
            </button>
          </div>

          <div className="mt-4">
            <div className="h-2 rounded-full bg-white/10">
              <div className="h-2 rounded-full bg-amber-300" style={{ width: `${pct}%` }} />
            </div>
            <p className="soft mt-2 text-xs">{completed}/{track.steps.length} complete • {pct}%</p>
          </div>

          <div className="mt-5 space-y-3">
            {track.steps.map((s, idx) => {
              const done = !!progress[stepKey(track.id, s.id)];
              const item = matchStepItem(s, items);
              const readHref = item ? `/read/${encodeURIComponent(item._id)}` : `/read${s.theme ? `?theme=${encodeURIComponent(s.theme)}` : ""}`;
              const chatHref = `/chat?q=${encodeURIComponent(s.chatPrompt + (item?.title ? ` Use: ${item.title}.` : ""))}`;
              return (
                <article key={s.id} className="rounded-md border border-white/10 p-4">
                  <div className="flex items-start justify-between gap-3">
                    <div>
                      <p className="text-xs uppercase tracking-wide text-amber-200/80">Step {idx + 1}</p>
                      <h3 className="mt-1 text-lg text-amber-100">{s.title}</h3>
                      <p className="soft mt-1 text-sm">{s.why}</p>
                      <p className="soft mt-2 text-xs">
                        {s.collection ? `${displayCollectionName(s.collection)} • ` : ""}
                        {s.theme ? `theme: ${s.theme}` : "open exploration"}
                      </p>
                    </div>
                    <button
                      onClick={() => toggle(track.id, s.id)}
                      className={`rounded-md border px-3 py-2 text-xs ${done ? "border-emerald-300/50 text-emerald-200" : "border-white/20 text-slate-200"}`}
                    >
                      {done ? "Completed" : "Mark complete"}
                    </button>
                  </div>
                  <div className="mt-3 flex flex-wrap gap-2">
                    <Link href={readHref} className="rounded-md bg-amber-300 px-3 py-2 text-xs font-semibold text-slate-900">
                      Open step
                    </Link>
                    <Link href={chatHref} className="rounded-md border border-amber-200/30 px-3 py-2 text-xs text-amber-100">
                      Guided chat
                    </Link>
                  </div>
                </article>
              );
            })}
          </div>
        </section>
      </div>
    </main>
  );
}
