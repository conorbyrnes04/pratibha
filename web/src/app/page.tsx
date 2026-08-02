'use client';

import Link from "next/link";
import { useEffect, useState } from "react";
import { getDaily } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { displayPassageTitle } from "@/lib/passageTitles";
import { collectionArtPool, generatedArtPool } from "@/lib/collectionImages";
import { ArtBackdrop } from "@/components/ArtImage";
import { BrandMark } from "@/components/BrandMark";
import { VerseOfTheDay } from "@/components/VerseOfTheDay";
import { InkGlyph } from "@/components/InkGlyph";
import { Section } from "@/components/ui/Section";
import { Disclosure } from "@/components/ui/Disclosure";
import { useAuth } from "@/components/AuthProvider";

const ALSO_IN_MANUSCRIPT = [
  { href: "/read", label: "Library", hint: "Browse the full corpus", glyph: "oak" as const },
  { href: "/chat", label: "Chat", hint: "Ask the texts anything", glyph: "eye" as const },
  { href: "/learn", label: "Paths", hint: "Guided gate-by-gate study", glyph: "labyrinth" as const },
  { href: "/learn#threads", label: "Threads", hint: "One theme, many traditions", glyph: "infinity" as const },
  { href: "/random", label: "Oracle", hint: "Draw an unexpected verse", glyph: "star" as const },
  { href: "/journal", label: "Journal", hint: "Keep your own notes", glyph: "lotus" as const },
];

export default function Home() {
  const { configured, loading, user } = useAuth();
  const signedIn = !configured || Boolean(user);
  const [daily, setDaily] = useState<VerseItem | null>(null);
  const [dailyLoading, setDailyLoading] = useState(true);

  useEffect(() => {
    // The /daily endpoint is public, so fetch the taste passage for everyone —
    // logged-out visitors see it as a preview, signed-in members as their day.
    let cancelled = false;
    setDailyLoading(true);
    getDaily("rich")
      .then((verse) => {
        if (!cancelled) setDaily(verse);
      })
      .catch(() => {
        if (!cancelled) setDaily(null);
      })
      .finally(() => {
        if (!cancelled) setDailyLoading(false);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (configured && !loading && !user) {
    return (
      <main className="page-shell">
        <div className="section-stack">
          <section className="manuscript-card overflow-hidden p-6 sm:p-10">
            <ArtBackdrop srcs={generatedArtPool("bg-hero")} variant="hero" priority />
            <div className="relative z-10 max-w-2xl">
              <p className="eyebrow">Pratibha</p>
              <h1 className="mt-4 text-4xl font-semibold leading-none text-amber-100 sm:text-5xl">
                Living Manuscript of World Wisdom
              </h1>
              <p className="soft mt-5 max-w-xl font-sans text-base leading-relaxed sm:text-lg">
                Layered canonical texts — original, translation, commentary, and practice —
                across traditions, with a source-grounded study companion.
              </p>
              <p className="soft mt-6 font-sans text-sm">
                Here is today&apos;s passage, in its own hand. The rest of the manuscript —
                Library, Paths, Study Chat, and Journal — opens when you sign in.
              </p>
            </div>
          </section>

          {daily ? (
            <VerseOfTheDay item={daily} preview />
          ) : (
            <section className="manuscript-card overflow-hidden p-6 sm:p-10">
              <div className="relative z-10 flex flex-wrap gap-3">
                <Link href="/login" className="btn-primary px-5 py-2.5">
                  Sign in to enter
                </Link>
                <Link href="/login?mode=signup" className="btn-secondary px-5 py-2.5">
                  Create an account
                </Link>
              </div>
            </section>
          )}
        </div>
      </main>
    );
  }

  if (loading || (signedIn && dailyLoading)) {
    return (
      <main className="page-shell">
        <section id="daily" className="manuscript-card scroll-mt-24 overflow-hidden p-6 sm:p-10">
          <ArtBackdrop srcs={generatedArtPool("bg-hero")} variant="hero" priority />
          <div className="relative z-10 flex min-h-[52vh] flex-col items-start justify-center">
            <BrandMark size="lg" className="opacity-90" />
            <p className="eyebrow mt-6">Pratibha · Today</p>
            <h1 className="mt-4 text-3xl font-semibold leading-none text-amber-100 sm:text-4xl">
              Opening today&apos;s page…
            </h1>
            <p className="soft mt-4 max-w-md font-sans text-base leading-relaxed">
              One passage. Its layers. One practice line.
            </p>
          </div>
        </section>
      </main>
    );
  }

  // Only the null-daily fallback card needs these; the populated card renders
  // through <VerseOfTheDay>, which derives its own title/art/links.
  const dailyTitle = daily ? displayPassageTitle(daily) : "A passage is waiting";
  const dailyArtPool = daily?.collection ? collectionArtPool(daily.collection) : generatedArtPool("bg-hero");
  const readHref = daily ? `/read/${encodeURIComponent(daily._id)}` : "/read";

  return (
    <main className="page-shell">
      <div className="section-stack">
        {daily ? (
          <VerseOfTheDay item={daily} />
        ) : (
          <section id="daily" className="manuscript-card scroll-mt-24 overflow-hidden p-6 sm:p-8">
            <ArtBackdrop srcs={dailyArtPool} variant="hero" priority />
            <div className="relative z-10">
              <p className="eyebrow">Pratibha · Today&apos;s passage</p>
              <h1 className="mt-4 text-3xl font-semibold leading-none text-amber-100 sm:text-4xl">{dailyTitle}</h1>
              <blockquote className="mt-6 max-w-3xl text-2xl leading-snug text-stone-100">
                Open a passage, let it read you back, then practice one concrete shift.
              </blockquote>
              <div className="mt-6 flex flex-wrap gap-3">
                <Link href={readHref} className="btn-primary px-5 py-2.5">
                  Open the Library
                </Link>
              </div>
            </div>
          </section>
        )}

        <Section
          eyebrow="Explore"
          title="Also in the manuscript"
          lead="When you are ready — library, paths, and the rest of the house."
        >
          <nav aria-label="Also in the manuscript" className="also-manuscript">
            {ALSO_IN_MANUSCRIPT.map((item) => (
              <Link key={item.href} href={item.href} title={item.hint} className="also-manuscript__link">
                <InkGlyph glyph={item.glyph} state="arising" size="sm" />
                <span>{item.label}</span>
              </Link>
            ))}
          </nav>
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
