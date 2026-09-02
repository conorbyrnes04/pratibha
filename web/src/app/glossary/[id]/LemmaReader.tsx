"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { getLemma, getLemmaPassages } from "@/lib/api";
import type { Lemma, LemmaPassageRef } from "@/lib/lexiconTypes";
import {
  nativeScript,
  nativeScriptClass,
  relationLabel,
  romanization,
  traditionLabel,
} from "@/lib/lexiconDisplay";
import { InlineMarkdown } from "@/components/InlineMarkdown";
import { cn } from "@/lib/utils";
import { recordPractice } from "@/lib/glyphUnlock";
import { buttonVariants } from "@/components/ui/button";

export default function GlossaryLemmaPage() {
  const params = useParams();
  const id = typeof params?.id === "string" ? params.id : Array.isArray(params?.id) ? params.id[0] : "";

  const [lemma, setLemma] = useState<Lemma | null>(null);
  const [passages, setPassages] = useState<LemmaPassageRef[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!id) return;
    let active = true;
    setLoading(true);
    setError("");
    setLemma(null);
    setPassages([]);

    Promise.all([getLemma(id), getLemmaPassages(id)])
      .then(([doc, refs]) => {
        if (!active) return;
        if (!doc) {
          setError("This lemma was not found in the lexicon.");
          return;
        }
        setLemma(doc);
        setPassages(refs);
        recordPractice(`glossary:${doc.id}`);
      })
      .catch(() => {
        if (!active) return;
        setError("Could not load this lemma. Is the Pratibha backend online?");
      })
      .finally(() => {
        if (active) setLoading(false);
      });

    return () => {
      active = false;
    };
  }, [id]);

  const native = nativeScript(lemma?.scripts);
  const roman = romanization(lemma?.scripts) || lemma?.id || id;
  const extraScripts = Object.values(lemma?.scripts || {}).filter(
    (val) => Boolean(val) && val !== native && val !== roman,
  );

  return (
    <main className="page-shell page-shell--reading">
      <nav className="passage-reading__crumb mb-6" aria-label="Breadcrumb">
        <Link href="/glossary">Glossary</Link>
      </nav>

      {loading ? (
        <p className="soft text-lg">Opening lemma…</p>
      ) : error || !lemma ? (
        <section className="py-8 text-center">
          <p className="text-2xl text-amber-100">Lemma unavailable</p>
          <p className="soft mx-auto mt-3 max-w-md">{error || "Not found."}</p>
          <Link href="/glossary" className={cn(buttonVariants({ variant: "secondary" }), "mt-6")}>
            Back to Glossary
          </Link>
        </section>
      ) : (
        <>
          <header className="glossary-lemma-hero">
            {native ? (
              <p className={`glossary-lemma-hero__native ${nativeScriptClass(lemma.scripts)}`}>
                {native}
              </p>
            ) : null}
            <h1 className="glossary-lemma-hero__roman source-script source-script--latin">{roman}</h1>
            {extraScripts.length > 0 ? (
              <p className="soft mt-2 font-sans text-sm tracking-wide">{extraScripts.join(" · ")}</p>
            ) : null}
            {(lemma.aliases || []).length > 0 ? (
              <p className="soft mt-3 font-sans text-sm">Also: {(lemma.aliases || []).join(", ")}</p>
            ) : null}
            {(lemma.traditions || []).length > 0 ? (
              <p className="mt-4 font-sans text-xs uppercase tracking-[0.16em] text-stone-500">
                {(lemma.traditions || []).map(traditionLabel).join(" · ")}
              </p>
            ) : null}
            <p className="mt-5">
              <Link href="/glossary/study" className={buttonVariants({ variant: "secondary", size: "sm" })}>
                Drill sacred terms →
              </Link>
            </p>
          </header>

          <div className="ornament my-8" />

          <section className="space-y-8">
            <h2 className="layer-heading">Senses</h2>
            {(lemma.senses || []).map((sense) => (
              <article key={sense.id} className="glossary-sense">
                <h3 className="text-2xl text-amber-100">{sense.label}</h3>
                <p className="soft mt-2 text-lg leading-relaxed">{sense.short}</p>
                {sense.etymology ? (
                  <p className="mt-3 font-sans text-sm leading-relaxed text-stone-300">
                    <span className="font-semibold text-amber-100/90">Etymology.</span>{" "}
                    <InlineMarkdown>{sense.etymology}</InlineMarkdown>
                  </p>
                ) : null}
                {(sense.traps || []).length > 0 ? (
                  <div className="mt-3">
                    <p className="layer-heading mb-1">Traps</p>
                    <ul className="list-disc space-y-1 pl-5 font-sans text-sm leading-relaxed text-stone-300">
                      {(sense.traps || []).map((trap) => (
                        <li key={trap}>
                          <InlineMarkdown>{trap}</InlineMarkdown>
                        </li>
                      ))}
                    </ul>
                  </div>
                ) : null}
                {sense.body ? (
                  <p className="mt-4 text-[1.05rem] leading-relaxed text-stone-200">
                    <InlineMarkdown>{sense.body}</InlineMarkdown>
                  </p>
                ) : null}
              </article>
            ))}
          </section>

          {(lemma.related || []).length > 0 ? (
            <section className="mt-12">
              <h2 className="layer-heading">Related</h2>
              <ul className="mt-4 space-y-3">
                {(lemma.related || []).map((rel) => (
                  <li key={`${rel.lemma_id}-${rel.relation}`}>
                    <Link
                      href={`/glossary/${encodeURIComponent(rel.lemma_id)}`}
                      className="group inline-flex flex-wrap items-baseline gap-x-2 gap-y-1 text-amber-100 underline decoration-amber-200/25 underline-offset-4 transition hover:decoration-amber-200/70"
                    >
                      <span className="source-script source-script--latin text-xl">{rel.lemma_id}</span>
                      <span className="font-sans text-xs uppercase tracking-[0.14em] text-stone-500">
                        {relationLabel(rel.relation)}
                      </span>
                    </Link>
                    {rel.note ? <p className="soft mt-1 font-sans text-sm">{rel.note}</p> : null}
                  </li>
                ))}
              </ul>
            </section>
          ) : null}

          {passages.length > 0 ? (
            <section className="mt-12">
              <h2 className="layer-heading">In the manuscript</h2>
              <ul className="mt-4 space-y-3">
                {passages.map((p) => (
                  <li key={`${p.id}-${p.term || ""}`}>
                    <Link
                      href={`/read/${encodeURIComponent(p.id)}`}
                      className="group block border-b border-amber-200/10 pb-3 transition hover:border-amber-200/25"
                    >
                      <span className="text-lg text-amber-100 group-hover:underline group-hover:decoration-amber-200/40 group-hover:underline-offset-4">
                        {p.title || p.id}
                      </span>
                      {p.collection ? (
                        <span className="mt-1 block font-sans text-xs uppercase tracking-[0.14em] text-stone-500">
                          {p.collection}
                        </span>
                      ) : null}
                      {p.term || p.definition ? (
                        <span className="soft mt-1 block font-sans text-sm leading-relaxed">
                          {p.term ? <em className="text-stone-200 not-italic">{p.term}</em> : null}
                          {p.term && p.definition ? " — " : null}
                          {p.definition || null}
                        </span>
                      ) : null}
                    </Link>
                  </li>
                ))}
              </ul>
            </section>
          ) : null}
        </>
      )}
    </main>
  );
}
