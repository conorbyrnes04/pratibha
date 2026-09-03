"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { getSources } from "@/lib/api";
import { collectionGlyph } from "@/lib/glyphs";
import { collectionImageSrc, generatedArtPool } from "@/lib/collectionImages";
import { displayCollectionName } from "@/lib/collectionLabels";
import { TRADITION_ORDER } from "@/lib/libraryTomes";
import { ArtBackdrop, ArtThumb } from "@/components/ArtImage";
import { FilterSelect } from "@/components/FilterSelect";
import { Glyph } from "@/components/Glyph";
import { Disclosure } from "@/components/ui/Disclosure";
import type { SourceAttribution } from "@/lib/types";
import { useT } from "@/components/LocaleProvider";

type SourceDensity = "open" | "columns" | "tight";
const DENSITY_KEY = "pratibha.sources.density";

function readDensity(): SourceDensity {
  if (typeof window === "undefined") return "columns";
  const raw = window.localStorage.getItem(DENSITY_KEY);
  return raw === "open" || raw === "tight" || raw === "columns" ? raw : "columns";
}

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
    <article className={`source-card manuscript-card overflow-hidden rounded-[18px] ${!inCorpus ? "opacity-75" : ""}`}>
      <div className="source-card__banner">
        <ArtThumb
          src={collectionImageSrc(item.collection)}
          className="absolute inset-0 h-full w-full"
          imgClassName="object-cover [object-position:center_28%]"
        />
        <div className="art-overlay art-overlay--banner absolute inset-0" />
      </div>
      <div className="source-card__body">
        <div className="flex items-start gap-2.5">
          <span
            className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-amber-200/25 bg-[#0b0b14]/85 backdrop-blur-sm"
            aria-hidden
          >
            <Glyph name={glyph} size="sm" />
          </span>
          <h3 className="source-card__title">{displayCollectionName(item.collection)}</h3>
        </div>
        <div className="source-card__badges font-sans text-[10px] uppercase tracking-[0.12em]">
          <span className={`rounded-full border border-amber-200/15 px-2 py-0.5 ${licenseClass}`}>
            {item.license_label}
          </span>
          {item.provenance_tier_label ? (
            <span
              className={`rounded-full border border-amber-200/15 px-2 py-0.5 ${TIER_TONE[item.provenance_tier] || "text-stone-300"}`}
            >
              {item.provenance_tier_label}
            </span>
          ) : null}
          {item.status === "in_progress" || !inCorpus ? (
            <span className="rounded-full border border-amber-200/15 px-2 py-0.5 text-stone-400">Coming soon</span>
          ) : item.coverage ? (
            <span className="rounded-full border border-amber-200/15 px-2 py-0.5 text-stone-300">{item.coverage}</span>
          ) : (
            <span className="rounded-full border border-amber-200/15 px-2 py-0.5 text-stone-300">
              {item.passages_in_corpus} passages
            </span>
          )}
        </div>

        <p className="source-card__work font-sans text-sm leading-relaxed text-stone-300">{item.original_work}</p>

        <div>
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
          <div className="mt-auto flex flex-wrap items-center gap-x-3 gap-y-1.5 font-sans text-xs">
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

function groupSourcesByTradition(items: SourceAttribution[]) {
  const buckets = new Map<string, SourceAttribution[]>();
  for (const item of items) {
    const key = (item.tradition || "").trim() || displayCollectionName(item.collection) || item.collection;
    const list = buckets.get(key) || [];
    list.push(item);
    buckets.set(key, list);
  }
  const known = TRADITION_ORDER.filter((tradition) => buckets.has(tradition));
  const extra = [...buckets.keys()]
    .filter((tradition) => !(TRADITION_ORDER as readonly string[]).includes(tradition))
    .sort((a, b) => a.localeCompare(b));
  return [...known, ...extra].map((tradition) => ({
    tradition,
    items: (buckets.get(tradition) || []).sort((a, b) =>
      displayCollectionName(a.collection).localeCompare(displayCollectionName(b.collection)),
    ),
  }));
}

export default function SourcesPage() {
  const t = useT();
  const [items, setItems] = useState<SourceAttribution[]>([]);
  const [summary, setSummary] = useState({
    collections_documented: 0,
    collections_in_corpus: 0,
    total_passages: 0,
  });
  const [error, setError] = useState("");
  const [density, setDensity] = useState<SourceDensity>("columns");

  useEffect(() => {
    setDensity(readDensity());
  }, []);

  function chooseDensity(next: string) {
    const value: SourceDensity = next === "open" || next === "tight" ? next : "columns";
    setDensity(value);
    try {
      window.localStorage.setItem(DENSITY_KEY, value);
    } catch {
      /* ignore quota / private mode */
    }
  }

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

  const shelves = useMemo(() => groupSourcesByTradition(items), [items]);

  return (
    <main className="page-shell page-shell--library">
      <div className="section-stack section-stack--tight">
        <header className="library-header">
          <div className="library-header__atmosphere" aria-hidden>
            <ArtBackdrop srcs={generatedArtPool("bg-sources")} variant="subtle" opacity={0.11} />
          </div>
          <div className="library-header__body">
          <p className="passage-reading__meta">{t("sources.meta")}</p>
          <h1 className="library-header__title">{t("sources.title")}</h1>
          <p className="library-header__lede">{t("sources.lede")}</p>

          <section className="mt-8 max-w-[var(--reading-measure)] border-t border-[rgb(240_201_121_/_0.14)] pt-5">
              <div className="flex flex-wrap items-baseline justify-between gap-3">
                <h2 className="text-xl font-medium text-[rgb(250_237_205)]">{t("sources.reconciled")}</h2>
                {summary.total_passages > 0 ? (
                  <p className="font-sans text-xs uppercase tracking-[0.18em] text-stone-500">
                    {t("sources.textsPassages", {
                      texts: summary.collections_in_corpus,
                      passages: summary.total_passages,
                    })}
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

        {shelves.length === 0 && !error ? (
          <p className="soft font-sans text-sm leading-relaxed">
            {t("sources.loading")}
          </p>
        ) : null}

        {shelves.length > 0 ? (
          <div className="flex justify-end">
            <div className="w-full max-w-[16rem]">
              <FilterSelect
                label={t("sources.layout")}
                tone="gold"
                value={density}
                onChange={chooseDensity}
                options={[
                  { value: "open", label: t("sources.layoutOpen"), hint: t("sources.layoutOpenHint") },
                  { value: "columns", label: t("sources.layoutColumns"), hint: t("sources.layoutColumnsHint") },
                  { value: "tight", label: t("sources.layoutTight"), hint: t("sources.layoutTightHint") },
                ]}
              />
            </div>
          </div>
        ) : null}

        {shelves.map((shelf) => (
          <section key={shelf.tradition}>
            <div className="mb-4 flex items-baseline justify-between gap-3">
              <h2 className="layer-heading text-amber-100/90">{shelf.tradition}</h2>
              <p className="soft font-sans text-xs">
                {shelf.items.length} {shelf.items.length === 1 ? "text" : "texts"}
              </p>
            </div>
            <div className={`source-shelf source-shelf--${density}`}>
              {shelf.items.map((item) => (
                <SourceCard key={item.id} item={item} />
              ))}
            </div>
          </section>
        ))}

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
