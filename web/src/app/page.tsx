'use client';

import Link from "next/link";
import { useEffect, useState } from "react";
import { getDaily } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageTitle } from "@/lib/passageTitles";
import { passagePreview, practiceText } from "@/lib/verseLayers";

const gateways = [
  {
    href: "/read",
    label: "Enter the Library",
    title: "Archive",
    copy: "Browse the corpus by tradition, passage, and theme.",
  },
  {
    href: "/chat",
    label: "Ask Pratibha",
    title: "Dialogue",
    copy: "Question the texts, compare traditions, and ask for practice.",
  },
  {
    href: "/random",
    label: "Draw a Passage",
    title: "Oracle",
    copy: "Let an unexpected verse interrupt your current frame.",
  },
  {
    href: "/learn",
    label: "Follow a Path",
    title: "Curriculum",
    copy: "Move through guided sequences from concept to embodiment.",
  },
];

export default function Home() {
  const [daily, setDaily] = useState<VerseItem | null>(null);

  useEffect(() => {
    getDaily("strong_draft").then(setDaily).catch(() => setDaily(null));
  }, []);

  const dailyTitle = daily ? displayPassageTitle(daily) : "A passage is waiting";
  const dailyCollection = displayCollectionName(daily?.collection);
  const dailyLine = daily ? passagePreview(daily) : "";
  const dailyPractice = daily ? practiceText(daily) || "Read slowly, then carry one line into the next action." : "Read slowly, then carry one line into the next action.";

  return (
    <main className="page-shell">
      <section id="daily" className="manuscript-card scroll-mt-24 p-6 sm:p-8">
        <p className="eyebrow">Today&apos;s passage</p>
        <h1 className="mt-4 text-3xl font-semibold leading-none text-amber-100 sm:text-4xl">{dailyTitle}</h1>
        <p className="soft mt-2 font-sans text-sm">{dailyCollection || "Pratibha corpus"}</p>
        <div className="ornament my-6" />
        <blockquote className="max-w-3xl text-2xl leading-snug text-stone-100">
          {dailyLine || "Open a passage, let it read you back, then practice one concrete shift."}
        </blockquote>
        <div className="practice-card mt-6 max-w-3xl p-4">
          <p className="layer-heading">Practice</p>
          <p className="soft mt-2 text-base leading-relaxed">{dailyPractice}</p>
        </div>
        <div className="mt-6 flex flex-wrap gap-3">
          {daily ? (
            <Link href={`/read/${encodeURIComponent(daily._id)}`} className="btn-primary px-5 py-2.5">
              Read passage
            </Link>
          ) : null}
          <Link href={daily ? `/chat?verse_id=${encodeURIComponent(daily._id)}&mode=explain` : "/chat"} className="btn-secondary px-5 py-2.5">
            Ask about it
          </Link>
        </div>
      </section>

      <section className="mt-14">
        <p className="eyebrow">A contemplative library that speaks back</p>
        <h2 className="display-title mt-5 text-balance text-stone-100">
          Study living wisdom, not just text.
        </h2>
        <p className="soft mt-6 max-w-2xl text-xl leading-relaxed">
          Move from source to translation, from commentary to practice, and from one tradition into another without flattening their differences.
        </p>
        <div className="mt-8 flex flex-wrap gap-3">
          <a href="#daily" className="btn-primary px-6 py-3">
            Begin with today
          </a>
          <Link href="/read" className="btn-secondary px-6 py-3">
            Open the library
          </Link>
        </div>
      </section>

      <section className="mt-14">
        <p className="eyebrow">Ways in</p>
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          {gateways.map((g) => (
            <Link key={g.href} href={g.href} className="card group block p-5 transition hover:-translate-y-0.5 hover:border-amber-200/40">
              <p className="layer-heading">{g.title}</p>
              <h2 className="mt-5 text-2xl font-semibold text-amber-100">{g.label}</h2>
              <p className="soft mt-3 text-base leading-relaxed">{g.copy}</p>
              <p className="mt-6 font-sans text-xs uppercase tracking-[0.2em] text-amber-200/70 group-hover:text-amber-100">
                Continue
              </p>
            </Link>
          ))}
        </div>
      </section>

      <section className="mt-12 grid gap-4 lg:grid-cols-3">
        {["Source-grounded", "Cross-tradition", "Practice-ready"].map((label, idx) => (
          <div key={label} className="citation-card p-5">
            <p className="text-4xl text-amber-200/80">0{idx + 1}</p>
            <h2 className="mt-3 text-2xl text-stone-100">{label}</h2>
            <p className="soft mt-2 leading-relaxed">
              {idx === 0
                ? "Original passages stay visible so interpretation never floats free."
                : idx === 1
                  ? "Resonances name both shared structure and real divergence."
                  : "Every study path returns to one embodied instruction."}
            </p>
          </div>
        ))}
      </section>
    </main>
  );
}
