"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { getSources } from "@/lib/api";
import { collectionIcon } from "@/lib/collectionIcons";
import { displayCollectionName } from "@/lib/collectionLabels";
import type { SourceAttribution } from "@/lib/types";

const LICENSE_TONE: Record<string, string> = {
  public_domain: "text-emerald-300/90",
  attributed_excerpt: "text-amber-200/90",
  mixed: "text-sky-200/80",
  original_editorial: "text-stone-300",
};

const SELL_READY_TONE: Record<string, string> = {
  green: "text-emerald-300/90",
  yellow: "text-amber-200/90",
  orange: "text-orange-200/85",
  red: "text-red-300/85",
};

function SourceCard({ item }: { item: SourceAttribution }) {
  const inCorpus = item.passages_in_corpus > 0;
  const licenseClass = LICENSE_TONE[item.license] || "text-stone-300";
  const tierClass = SELL_READY_TONE[item.sell_ready_tier] || "text-stone-300";

  return (
    <article className={`manuscript-card rounded-[22px] p-5 sm:p-6 ${!inCorpus ? "opacity-75" : ""}`}>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <div className="flex items-start gap-3">
          <span className="mt-0.5 font-sans text-2xl text-amber-200/80" aria-hidden>
            {collectionIcon(item.collection)}
          </span>
          <div>
            <h2 className="text-2xl font-semibold tracking-[-0.03em] text-stone-100">
              {displayCollectionName(item.collection)}
            </h2>
            <p className="soft mt-1 font-sans text-sm">{item.tradition}</p>
          </div>
        </div>
        <div className="flex flex-wrap gap-2 font-sans text-xs uppercase tracking-[0.14em]">
          <span className={`rounded-full border border-amber-200/15 px-2.5 py-1 ${tierClass}`}>
            {item.sell_ready_tier_label}
          </span>
          <span className={`rounded-full border border-amber-200/15 px-2.5 py-1 ${licenseClass}`}>
            {item.license_label}
          </span>
          {item.status === "in_progress" ? (
            <span className="rounded-full border border-amber-200/15 px-2.5 py-1 text-stone-400">In progress</span>
          ) : item.coverage ? (
            <span className="rounded-full border border-amber-200/15 px-2.5 py-1 text-stone-300">{item.coverage}</span>
          ) : (
            <span className="rounded-full border border-amber-200/15 px-2.5 py-1 text-stone-300">
              {item.passages_in_corpus} passages
            </span>
          )}
        </div>
      </div>

      <dl className="mt-5 space-y-3 font-sans text-sm leading-relaxed text-stone-300">
        <div>
          <dt className="layer-heading mb-1">Original work</dt>
          <dd>{item.original_work}</dd>
        </div>
        {item.anchor_translation ? (
          <div>
            <dt className="layer-heading mb-1">Anchor translation / English basis</dt>
            <dd>{item.anchor_translation}</dd>
          </div>
        ) : null}
        {item.pd_alternative ? (
          <div>
            <dt className="layer-heading mb-1">Public-domain alternative</dt>
            <dd className="text-stone-400">{item.pd_alternative}</dd>
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

      {item.links?.length ? (
        <div className="mt-4 flex flex-wrap gap-3 font-sans text-sm">
          {item.links.map((link) =>
            link.url ? (
              <a
                key={link.label}
                href={link.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-amber-200/90 underline decoration-amber-200/30 underline-offset-4 hover:text-amber-100"
              >
                {link.label}
              </a>
            ) : (
              <span key={link.label} className="text-stone-500">
                {link.label}
              </span>
            ),
          )}
        </div>
      ) : null}

      {inCorpus ? (
        <Link
          href={`/read?collection=${encodeURIComponent(item.collection)}`}
          className="mt-5 inline-block font-sans text-sm text-amber-200/90 hover:text-amber-100"
        >
          Browse {displayCollectionName(item.collection)} in Library →
        </Link>
      ) : null}
    </article>
  );
}

export default function SourcesPage() {
  const [items, setItems] = useState<SourceAttribution[]>([]);
  const [summary, setSummary] = useState({
    collections_documented: 0,
    collections_in_corpus: 0,
    total_passages: 0,
    sell_ready_tiers: {} as Partial<Record<SourceAttribution["sell_ready_tier"], number>>,
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
        setSummary(data.summary);
      })
      .catch(() => setError("Could not load sources."));
  }, []);

  const inCorpus = useMemo(() => items.filter((i) => i.passages_in_corpus > 0), [items]);
  const inProgress = useMemo(
    () => items.filter((i) => i.status === "in_progress" || i.passages_in_corpus === 0),
    [items],
  );

  return (
    <main className="page-shell max-w-4xl">
      <p className="eyebrow">Attribution</p>
      <h1 className="mt-3 text-5xl font-semibold leading-none tracking-[-0.04em] text-stone-100 sm:text-6xl">Sources</h1>
      <p className="soft mt-4 max-w-2xl text-xl leading-relaxed">
        Translations, editions, and editorial layers used in Pratibha — so credit is clear and the study companion stays on
        solid ground.
      </p>

      <section className="manuscript-card mt-8 rounded-[22px] p-5 sm:p-6">
        <h2 className="text-2xl font-semibold text-stone-100">How Pratibha uses texts</h2>
        <div className="soft mt-4 space-y-3 font-sans text-sm leading-relaxed">
          <p>
            <strong className="font-medium text-stone-200">Anchor passages</strong> reproduce or closely follow named
            translations or public-domain editions where indicated. We do not claim copyright over those English renderings.
          </p>
          <p>
            <strong className="font-medium text-stone-200">Pratibha layers</strong> — commentary, key terms, cross-tradition
            resonances, and practice — are original editorial work unless a unit explicitly cites a traditional commentator.
          </p>
          <p>
            <strong className="font-medium text-stone-200">Sanskrit and source scripts</strong> follow received or scholarly
            editions noted per collection. Devanagari marked as editorial reconstruction is not manuscript-verified.
          </p>
          <p>
            <strong className="font-medium text-stone-200">Sell-ready tier</strong> — green collections use public-domain
            anchors or original Pratibha work; yellow means a PD alternative is listed; orange and red need Pratibha
            English or a license before commercial use.
          </p>
          <p className="text-stone-400">
            Pratibha is a study companion, not a substitute for primary editions. For citation, scholarship, or publication,
            consult the listed translators and publishers directly.
          </p>
        </div>
        {summary.total_passages > 0 ? (
          <p className="mt-5 font-sans text-xs uppercase tracking-[0.18em] text-stone-500">
            {summary.collections_in_corpus} collections live · {summary.total_passages} passages indexed
            {summary.sell_ready_tiers?.green ? ` · ${summary.sell_ready_tiers.green} sell-ready` : ""}
            {summary.sell_ready_tiers?.yellow ? ` · ${summary.sell_ready_tiers.yellow} PD swap pending` : ""}
          </p>
        ) : null}
      </section>

      {error ? <p className="mt-6 font-sans text-sm text-red-300/90">{error}</p> : null}

      <section className="mt-10">
        <h2 className="layer-heading mb-4">In the corpus</h2>
        <div className="space-y-5">
          {inCorpus.map((item) => (
            <SourceCard key={item.id} item={item} />
          ))}
        </div>
      </section>

      {inProgress.length > 0 ? (
        <section className="mt-12">
          <h2 className="layer-heading mb-4">In progress or not yet ingested</h2>
          <div className="space-y-5">
            {inProgress.map((item) => (
              <SourceCard key={item.id} item={item} />
            ))}
          </div>
        </section>
      ) : null}

      <p className="soft mt-12 font-sans text-sm leading-relaxed">
        See a missing or incorrect credit?{" "}
        <Link href="/read" className="text-amber-200/90 underline decoration-amber-200/30 underline-offset-4">
          Note it when saving a passage to your journal
        </Link>
        .
      </p>
    </main>
  );
}
