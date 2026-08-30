'use client';

import Link from "next/link";
import { useEffect, useState } from "react";
import { getDaily } from "@/lib/api";
import type { VerseItem } from "@/lib/types";
import { generatedArtPool } from "@/lib/collectionImages";
import { ArtBackdrop } from "@/components/ArtImage";
import { VerseOfTheDay } from "@/components/VerseOfTheDay";
import { InkGlyph } from "@/components/InkGlyph";
import { Section } from "@/components/ui/Section";
import { Disclosure } from "@/components/ui/Disclosure";
import { useAuth } from "@/components/AuthProvider";
import { buttonVariants } from "@/components/ui/button";
import { CircleReadings } from "@/components/CircleReadings";
import { SanghaBoundary } from "@/components/SanghaBoundary";

const ALSO_IN_MANUSCRIPT = [
  { href: "/read", label: "Library", hint: "Browse the full corpus", glyph: "oak" as const },
  { href: "/chat", label: "Chat", hint: "Ask the texts anything", glyph: "eye" as const },
  { href: "/learn", label: "Paths", hint: "Guided gate-by-gate study", glyph: "labyrinth" as const },
  { href: "/learn#threads", label: "Themes", hint: "One claim, many traditions", glyph: "infinity" as const },
  { href: "/random", label: "Oracle", hint: "Draw an unexpected verse", glyph: "star" as const },
  { href: "/journal", label: "Journal", hint: "Keep your own notes", glyph: "lotus" as const },
  { href: "/manuscript", label: "Manuscript", hint: "A small book of verses you keep", glyph: "circle" as const },
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
      <main className="page-shell page-shell--reading">
        <div className="section-stack">
          <header className="library-header">
            <div className="library-header__atmosphere" aria-hidden>
              <ArtBackdrop srcs={generatedArtPool("bg-hero")} variant="subtle" opacity={0.12} priority />
            </div>
            <div className="library-header__body">
              <p className="passage-reading__meta">Pratibha</p>
              <h1 className="library-header__title">Living Manuscript of World Wisdom</h1>
              <p className="library-header__lede">
                Layered canonical texts — original, translation, commentary, and practice —
                across traditions. Here is today&apos;s passage; the rest opens when you sign in.
              </p>
            </div>
          </header>

          {daily ? (
            <VerseOfTheDay item={daily} preview />
          ) : (
            <div className="passage-reading__nav">
              <Link href="/login" className={buttonVariants()}>
                Sign in to enter
              </Link>
              <Link href="/login?mode=signup" className={buttonVariants({ variant: "secondary" })}>
                Create an account
              </Link>
            </div>
          )}
        </div>
      </main>
    );
  }

  if (loading || (signedIn && dailyLoading)) {
    return (
      <main className="page-shell page-shell--reading">
        <header className="passage-reading__header">
          <p className="passage-reading__meta">Today</p>
          <h1 className="passage-reading__title">Opening today&apos;s page…</h1>
          <p className="passage-reading__deck">One passage. Its layers. One practice line.</p>
        </header>
      </main>
    );
  }

  const readHref = daily ? `/read/${encodeURIComponent(daily._id)}` : "/read";

  return (
    <main className="page-shell page-shell--reading">
      <div className="section-stack">
        {daily ? (
          <>
            <VerseOfTheDay item={daily} />
            {signedIn ? (
              <SanghaBoundary>
                <CircleReadings verseId={daily._id} daily />
              </SanghaBoundary>
            ) : null}
          </>
        ) : (
          <section id="daily" className="scroll-mt-24">
            <header className="passage-reading__header">
              <p className="passage-reading__meta">Today&apos;s passage</p>
              <h1 className="passage-reading__title">A passage is waiting</h1>
              <p className="passage-reading__deck">
                Open a passage, let it read you back, then practice one concrete shift.
              </p>
            </header>
            <div className="passage-reading__nav">
              <Link href={readHref} className={buttonVariants()}>
                Open the Library
              </Link>
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
          <p className="soft max-w-[var(--reading-measure)] text-base leading-relaxed">
            Move from source to translation, from commentary to practice, and from one
            tradition into another without flattening their differences.
          </p>
          <div className="mt-6 grid gap-6">
            {(
              [
                { label: "Source-grounded", copy: "Original passages stay visible so interpretation never floats free." },
                { label: "Cross-tradition", copy: "Resonances name both shared structure and real divergence." },
                { label: "Practice-ready", copy: "Every study path returns to one embodied instruction." },
              ] as const
            ).map((item, idx) => (
              <div key={item.label} className="border-t border-[rgb(240_201_121_/_0.12)] pt-4">
                <p className="passage-reading__meta">0{idx + 1} · {item.label}</p>
                <p className="soft mt-2 max-w-[var(--reading-measure)] leading-relaxed">{item.copy}</p>
              </div>
            ))}
          </div>
        </Disclosure>
      </div>
    </main>
  );
}
