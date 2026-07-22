'use client';

import Link from "next/link";
import { useEffect, useState } from "react";
import { getDaily } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { displayCollectionName } from "@/lib/collectionLabels";
import { displayPassageTitle } from "@/lib/passageTitles";
import { passagePreview, practiceText } from "@/lib/verseLayers";
import { collectionArtPool, generatedArtPool } from "@/lib/collectionImages";
import type { GlyphSlug } from "@/lib/glyphs";
import { ArtBackdrop } from "@/components/ArtImage";
import { GlyphOrnament } from "@/components/Glyph";
import { Section } from "@/components/ui/Section";
import { OverviewCard } from "@/components/ui/OverviewCard";
import { ProductSnapshot, type ProductChip } from "@/components/ui/ProductSnapshot";
import { Disclosure } from "@/components/ui/Disclosure";

const PRODUCTS: ProductChip[] = [
  { href: "/read", label: "Library", hint: "Browse the full corpus", glyph: "gateway" },
  { href: "/chat", label: "Study Chat", hint: "Ask the texts anything", glyph: "eye" },
  { href: "/learn", label: "Paths", hint: "Guided gate-by-gate study", glyph: "labyrinth" },
  { href: "/learn#threads", label: "Threads", hint: "One theme, many traditions", glyph: "infinity" },
  { href: "/random", label: "Oracle", hint: "Draw an unexpected verse", glyph: "star" },
  { href: "/journal", label: "Journal", hint: "Keep your own notes", glyph: "leaves" },
];

const EXPLORE: Array<{ href: string; title: string; body: string; glyph: GlyphSlug }> = [
  { href: "/read", title: "Library", body: "The corpus by tradition, passage, and theme.", glyph: "gateway" },
  { href: "/chat", title: "Study Chat", body: "Question the texts and compare traditions.", glyph: "eye" },
  { href: "/learn", title: "Paths & Threads", body: "Descend gate by gate, or trace one theme.", glyph: "labyrinth" },
  { href: "/random", title: "Oracle", body: "Let an unexpected verse interrupt you.", glyph: "star" },
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

  const dailyArtPool = daily?.collection ? collectionArtPool(daily.collection) : generatedArtPool("bg-hero");
  const readHref = daily ? `/read/${encodeURIComponent(daily._id)}` : "/read";
  const askHref = daily ? `/chat?verse_id=${encodeURIComponent(daily._id)}&mode=explain` : "/chat";

  return (
    <main className="page-shell">
      <div className="section-stack">
        {/* Daily hero */}
        <section id="daily" className="manuscript-card scroll-mt-24 overflow-hidden p-6 sm:p-8">
          <ArtBackdrop srcs={dailyArtPool} variant="hero" priority />
          <div className="relative z-10">
            <p className="eyebrow">Today&apos;s passage</p>
            <h1 className="mt-4 text-3xl font-semibold leading-none text-amber-100 sm:text-4xl">{dailyTitle}</h1>
            <p className="soft mt-2 font-sans text-sm">{dailyCollection || "Pratibha corpus"}</p>
            <GlyphOrnament name="lotus" className="my-6 max-w-md" />
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
          </div>
        </section>

        {/* Product snapshot — glanceable map of every surface */}
        <ProductSnapshot items={PRODUCTS} activeHref="/" />

        {/* First-run journey */}
        <Section
          eyebrow="Start here"
          title="Three moves to begin"
          lead="New to Pratibha? Follow this path once and the rest opens up."
        >
          <div className="grid gap-4 sm:grid-cols-3">
            <OverviewCard
              eyebrow="Step 1"
              title="Read today's passage"
              body="Sit with one source and its practice."
              glyph="lotus"
              href={readHref}
            />
            <OverviewCard
              eyebrow="Step 2"
              title="Follow a Path"
              body="Descend a tradition gate by gate."
              glyph="labyrinth"
              href="/learn"
            />
            <OverviewCard
              eyebrow="Step 3"
              title="Ask Pratibha"
              body="Question the texts in your own words."
              glyph="eye"
              href="/chat"
            />
          </div>
        </Section>

        {/* Explore all surfaces */}
        <Section
          eyebrow="Explore"
          title="Ways in"
          action={
            <Link href="/read" className="btn-secondary px-4 py-2 text-sm">
              Open the library
            </Link>
          }
        >
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {EXPLORE.map((item) => (
              <OverviewCard
                key={item.href}
                title={item.title}
                body={item.body}
                glyph={item.glyph}
                href={item.href}
                stat="Continue"
              />
            ))}
          </div>
        </Section>

        {/* Secondary prose, tucked behind progressive disclosure */}
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
