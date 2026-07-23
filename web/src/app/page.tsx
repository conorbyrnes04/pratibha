'use client';

import Link from "next/link";
import { useEffect, useState } from "react";
import { getDaily } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageTitle } from "@/lib/passageTitles";
import { passagePreview, practiceText } from "@/lib/verseLayers";
import { collectionArtPool, generatedArtPool } from "@/lib/collectionImages";
import { ArtBackdrop } from "@/components/ArtImage";
import { InkGlyph } from "@/components/InkGlyph";
import { Section } from "@/components/ui/Section";
import { ProductSnapshot, type ProductChip } from "@/components/ui/ProductSnapshot";
import { Disclosure } from "@/components/ui/Disclosure";

const PRODUCTS: ProductChip[] = [
  { href: "/read", label: "Library", hint: "Browse the full corpus", glyph: "oak" },
  { href: "/chat", label: "Study Chat", hint: "Ask the texts anything", glyph: "eye" },
  { href: "/learn", label: "Paths", hint: "Guided gate-by-gate study", glyph: "labyrinth" },
  { href: "/learn#threads", label: "Threads", hint: "One theme, many traditions", glyph: "infinity" },
  { href: "/random", label: "Oracle", hint: "Draw an unexpected verse", glyph: "star" },
  { href: "/journal", label: "Journal", hint: "Keep your own notes", glyph: "lotus" },
];

export default function Home() {
  const [daily, setDaily] = useState<VerseItem | null>(null);

  useEffect(() => {
    getDaily("strong_draft").then(setDaily).catch(() => setDaily(null));
  }, []);

  const dailyTitle = daily ? displayPassageTitle(daily) : "A passage is waiting";
  const dailyCollection = displayCollectionName(daily?.collection);
  const dailyLine = daily ? passagePreview(daily) : "";
  const dailyPractice = daily
    ? practiceText(daily) || "Read slowly, then carry one line into the next action."
    : "Read slowly, then carry one line into the next action.";

  const dailyArtPool = daily?.collection ? collectionArtPool(daily.collection) : generatedArtPool("bg-hero");
  const readHref = daily ? `/read/${encodeURIComponent(daily._id)}` : "/read";
  const askHref = daily ? `/chat?verse_id=${encodeURIComponent(daily._id)}&mode=explain` : "/chat";

  return (
    <main className="page-shell">
      <div className="section-stack">
        {/* Daily hero — one composition: brand signal + passage + CTAs + quiet surface strip */}
        <section id="daily" className="manuscript-card scroll-mt-24 overflow-hidden p-6 sm:p-8">
          <ArtBackdrop srcs={dailyArtPool} variant="hero" priority />
          <div className="relative z-10">
            <p className="eyebrow">Pratibha · Today&apos;s passage</p>
            <h1 className="mt-4 text-3xl font-semibold leading-none text-amber-100 sm:text-4xl">{dailyTitle}</h1>
            <p className="soft mt-2 font-sans text-sm">{dailyCollection || "Pratibha corpus"}</p>
            <div className="my-6">
              <InkGlyph glyph="lotus" state="arising" size="lg" />
            </div>
            <blockquote className="max-w-3xl text-2xl leading-snug text-stone-100">
              {dailyLine || "Open a passage, let it read you back, then practice one concrete shift."}
            </blockquote>
            <div className="practice-card mt-6 max-w-3xl p-4">
              <p className="layer-heading">Practice</p>
              <p className="soft mt-2 text-base leading-relaxed">{dailyPractice}</p>
            </div>
            <div className="mt-6 flex flex-wrap gap-3">
              <Link href={readHref} className="btn-primary px-5 py-2.5">
                Read today&apos;s passage
              </Link>
              <Link href={askHref} className="btn-secondary px-5 py-2.5">
                Ask about it
              </Link>
            </div>
            <div className="mt-8 border-t border-white/10 pt-5">
              <ProductSnapshot items={PRODUCTS} />
            </div>
          </div>
        </section>

        {/* First-run journey — light steps, not cards */}
        <Section
          eyebrow="Start here"
          title="Three moves to begin"
          lead="New to Pratibha? Follow this path once and the rest opens up."
        >
          <div className="start-steps">
            <Link href={readHref} className="start-step">
              <div className="start-step__top">
                <InkGlyph glyph="lotus" state="arising" size="sm" />
                <span className="start-step__eyebrow">Step 1</span>
              </div>
              <h3 className="start-step__title">Read today&apos;s passage</h3>
              <p className="start-step__body mt-2">Sit with one source and its practice.</p>
            </Link>
            <Link href="/learn" className="start-step">
              <div className="start-step__top">
                <InkGlyph glyph="labyrinth" state="arising" size="sm" />
                <span className="start-step__eyebrow">Step 2</span>
              </div>
              <h3 className="start-step__title">Follow a Path</h3>
              <p className="start-step__body mt-2">Descend a tradition gate by gate.</p>
            </Link>
            <Link href="/chat" className="start-step">
              <div className="start-step__top">
                <InkGlyph glyph="eye" state="arising" size="sm" />
                <span className="start-step__eyebrow">Step 3</span>
              </div>
              <h3 className="start-step__title">Ask Pratibha</h3>
              <p className="start-step__body mt-2">Question the texts in your own words.</p>
            </Link>
          </div>
        </Section>

        <Disclosure summary="What makes Pratibha different" hint="How it works">
          <p className="soft max-w-2xl text-lg leading-relaxed">
            Move from source to translation, from commentary to practice, and from one
            tradition into another without flattening their differences.
          </p>
          <div className="mt-6 grid gap-4 lg:grid-cols-3">
            {(
              [
                { label: "Source-grounded", copy: "Original passages stay visible so interpretation never floats free." },
                { label: "Cross-tradition", copy: "Resonances name both shared structure and real divergence." },
                { label: "Practice-ready", copy: "Every study path returns to one embodied instruction." },
              ] as const
            ).map((item, idx) => (
              <div key={item.label} className="citation-card p-5">
                <p className="text-3xl text-amber-200/80">0{idx + 1}</p>
                <h3 className="mt-2 text-xl text-stone-100">{item.label}</h3>
                <p className="soft mt-2 leading-relaxed">{item.copy}</p>
              </div>
            ))}
          </div>
        </Disclosure>
      </div>
    </main>
  );
}
