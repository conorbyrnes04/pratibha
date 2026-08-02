"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { getSources } from "@/lib/api";
import { collectionGlyph } from "@/lib/glyphs";
import { collectionImageSrc, generatedArtPool } from "@/lib/collectionImages";
import { displayCollectionName } from "@/lib/collectionLabels";
import { ArtBackdrop, ArtThumb } from "@/components/ArtImage";
import { Glyph } from "@/components/Glyph";
import { Section } from "@/components/ui/Section";
import { Disclosure } from "@/components/ui/Disclosure";
import type { SourceAttribution } from "@/lib/types";

const LICENSE_TONE: Record<string, string> = {
  public_domain: "text-emerald-300/90",
  original_editorial: "text-amber-200/90",
};

const TIER_TONE: Record<string, string> = {
  pd_render: "text-emerald-300/80",
  pd_adapted: "text-sky-200/80",
  original: "text-amber-200/90",
};

function publicLinks(item: SourceAttribution) {
  return (item.links || []).filter((link) => Boolean(link.url && /^https?:\/\//i.test(link.url)));
}

function SourceCard({ item }: { item: SourceAttribution }) {
  const inCorpus = item.passages_in_corpus > 0;
  const licenseClass = LICENSE_TONE[item.license] || "text-stone-300";
  const links = publicLinks(item);
  const glyph = collectionGlyph(item.collection);

  return (
    <article className={`manuscript-card overflow-hidden rounded-[22px] ${!inCorpus ? "opacity-75" : ""}`}>
      <div className="relative h-24 w-full sm:h-28">
        <ArtThumb
          src={collectionImageSrc(item.collection)}
          className="absolute inset-0 h-full w-full"
          imgClassName="object-cover [object-position:center_28%]"
        />
        <div className="art-overlay art-overlay--banner absolute inset-0" />
      </div>
      <div className="relative -mt-8 p-5 pt-0 sm:p-6 sm:pt-0">
        <div className="flex flex-wrap items-start justify-between gap-3">
          <div className="flex items-start gap-3">
            <span
              className="mt-0.5 flex h-11 w-11 shrink-0 items-center justify-center rounded-full border border-amber-200/25 bg-[#0b0b14]/85 backdrop-blur-sm"
              aria-hidden
            >
              <Glyph name={glyph} size="sm" />
            </span>
            <div>
              <h2 className="text-2xl font-semibold tracking-[-0.03em] text-stone-100">
                {displayCollectionName(item.collection)}
              </h2>
              <p className="soft mt-1 font-sans text-sm">{item.tradition}</p>
            </div>
          </div>
          <div className="flex flex-wrap gap-2 font-sans text-xs uppercase tracking-[0.14em]">
            <span className={`rounded-full border border-amber-200/15 px-2.5 py-1 ${licenseClass}`}>
              {item.license_label}
            </span>
            {item.provenance_tier_label ? (
              <span
                className={`rounded-full border border-amber-200/15 px-2.5 py-1 ${TIER_TONE[item.provenance_tier] || "text-stone-300"}`}
              >
                {item.provenance_tier_label}
              </span>
            ) : null}
            {item.status === "in_progress" || !inCorpus ? (
              <span className="rounded-full border border-amber-200/15 px-2.5 py-1 text-stone-400">Coming soon</span>
            ) : item.coverage ? (
              <span className="rounded-full border border-amber-200/15 px-2.5 py-1 text-stone-300">{item.coverage}</span>
            ) : (
              <span className="rounded-full border border-amber-200/15 px-2.5 py-1 text-stone-300">
                {item.passages_in_corpus} passages
              </span>
            )}
          </div>
        </div>

        <p className="mt-4 font-sans text-sm leading-relaxed text-stone-300">{item.original_work}</p>

        <div className="mt-4">
          <Disclosure summary="Edition & editorial details" hint={item.license_label}>
            <dl className="space-y-3 font-sans text-sm leading-relaxed text-stone-300">
              {item.anchor_translation ? (
                <div>
                  <dt className="layer-heading mb-1">English basis</dt>
                  <dd>{item.anchor_translation}</dd>
                </div>
              ) : null}
              {item.sanskrit_source ? (
                <div>
                  <dt className="layer-heading mb-1">Source language</dt>
                  <dd>{item.sanskrit_source}</dd>
                </div>
              ) : null}
              <div>
                <dt className="layer-heading mb-1">Pratibha editorial</dt>
                <dd className="text-stone-400">
                  {item.editorial_note}
                  {item.conceived_by_conor ? (
                    <span className="mt-1 block text-amber-200/80">
                      Original Pratibha work conceived by Conor Byrnes.
                    </span>
                  ) : null}
                </dd>
              </div>
            </dl>
          </Disclosure>
        </div>

        {links.length || inCorpus ? (
          <div className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-2 font-sans text-sm">
            {links.map((link) => (
              <a
                key={link.label}
                href={link.url!}
                target="_blank"
                rel="noopener noreferrer"
                className="text-amber-200/90 underline decoration-amber-200/30 underline-offset-4 hover:text-amber-100"
              >
                {link.label}
              </a>
            ))}
            {inCorpus ? (
              <Link
                href={`/read?collection=${encodeURIComponent(item.collection)}`}
                className="text-amber-200/90 hover:text-amber-100"
              >
                Browse in Library →
              </Link>
            ) : null}
          </div>
        ) : null}
      </div>
    </article>
  );
}

export default function SourcesPage() {
  const [items, setItems] = useState<SourceAttribution[]>([]);
  const [summary, setSummary] = useState({
    collections_documented: 0,
    collections_in_corpus: 0,
    total_passages: 0,
  });
  const [error, setError] = useState("");

  useEffect(() => {
    getSources()
      .then((data) => {
        if (!data) {
          setError("Could not load sources. Is the API running?");
          return;
        }
        setItems(data.items);
        setSummary({
          collections_documented: data.summary.collections_documented,
          collections_in_corpus: data.summary.collections_in_corpus,
          total_passages: data.summary.total_passages,
        });
      })
      .catch(() => setError("Could not load sources."));
  }, []);

  const inCorpus = useMemo(() => items.filter((i) => i.passages_in_corpus > 0), [items]);
  const comingSoon = useMemo(
    () => items.filter((i) => i.status === "in_progress" || i.passages_in_corpus === 0),
    [items],
  );

  return (
    <main className="page-shell page-shell--reading">
      <div className="section-stack">
        <header className="library-header">
          <div className="library-header__atmosphere" aria-hidden>
            <ArtBackdrop srcs={generatedArtPool("bg-sources")} variant="subtle" opacity={0.11} />
          </div>
          <div className="library-header__body">
          <p className="passage-reading__meta">Attribution · Asteya</p>
          <h1 className="library-header__title">Sources</h1>
          <p className="library-header__lede">
            Pratibha is offered freely to students, so it must be built without stealing. Every English rendering here stands on
            a public-domain source or original authorship — and each text says exactly where it comes from.
          </p>

          <section className="mt-8 max-w-[var(--reading-measure)] border-t border-[rgb(240_201_121_/_0.14)] pt-5">
              <div className="flex flex-wrap items-baseline justify-between gap-3">
                <h2 className="text-xl font-medium text-[rgb(250_237_205)]">How this corpus was reconciled</h2>
                {summary.total_passages > 0 ? (
                  <p className="font-sans text-xs uppercase tracking-[0.18em] text-stone-500">
                    {summary.collections_in_corpus} texts · {summary.total_passages} passages
                  </p>
                ) : null}
              </div>
              <p className="soft mt-3 font-sans text-sm leading-relaxed">
                Earlier drafts of some texts leaned on copyrighted modern translations. Those were removed and re-grounded: the
                English is now rendered from public-domain source-language texts, or follows a public-domain translation by name.
                Nothing under copyright is reproduced.
              </p>
              <div className="mt-4">
                <Disclosure summary="How the renderings were made">
                  <div className="space-y-3 font-sans text-sm leading-relaxed">
                    <p>
                      <strong className="font-medium text-stone-200">Rendered from the source.</strong> For most texts the English
                      is generated afresh from a public-domain original — Sanskrit, Classical Chinese, Tibetan, Persian, Middle
                      High German, classical Japanese, or Greek — rather than copied from a modern translation.
                    </p>
                    <p>
                      <strong className="font-medium text-stone-200">Adapted from public-domain translations.</strong> Where a
                      text rests on an out-of-copyright English translation (Arnold, Carter, Jowett, MacKenna, Patrick, Weir,
                      Evans-Wentz), that translator is credited by name on the text.
                    </p>
                    <p>
                      <strong className="font-medium text-stone-200">Checked against copyrighted editions, never copied from
                      them.</strong> Renderings were compared to existing translations only to catch errors and echoed phrasing;
                      shared wording was rewritten so the English is genuinely independent.
                    </p>
                    <p>
                      <strong className="font-medium text-stone-200">Original work is marked as such.</strong> The Śiva Sūtra and
                      Tantrasāra are original translation and commentary. Across every text, Pratibha&apos;s commentary, key
                      terms, resonances, and practice are original editorial work.
                    </p>
                    <p className="text-stone-400">
                      Pratibha is a study companion offered as a gift, not a substitute for primary editions. For citation or
                      scholarship, consult the source texts and the named translators directly. See a credit that looks wrong?
                      Please flag it.
                    </p>
                  </div>
                </Disclosure>
              </div>
          </section>

          {error ? <p className="mt-6 font-sans text-sm text-red-300/90">{error}</p> : null}
          </div>
        </header>

        <Section title="In the library" as="h2">
          <div className="space-y-5">
            {inCorpus.map((item) => (
              <SourceCard key={item.id} item={item} />
            ))}
          </div>
        </Section>

        {comingSoon.length > 0 ? (
          <Section title="Coming into the library" as="h2">
            <div className="space-y-5">
              {comingSoon.map((item) => (
                <SourceCard key={item.id} item={item} />
              ))}
            </div>
          </Section>
        ) : null}

        <p className="soft font-sans text-sm leading-relaxed">
          See a missing or incorrect credit?{" "}
          <Link href="/read" className="text-amber-200/90 underline decoration-amber-200/30 underline-offset-4">
            Note it when saving a passage to your journal
          </Link>
          .
        </p>
      </div>
    </main>
  );
}
