"use client";

import { useState } from "react";
import Link from "next/link";
import type { KeyTerm, PratibhaLayer, Resonance } from "@/lib/types";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { containsCjk, containsDevanagari, containsTibetan, isLongNativeScript } from "@/lib/sanskritScript";
import { InlineMarkdown } from "@/components/InlineMarkdown";
import {
  Collapsible,
  CollapsibleContent,
  CollapsibleTrigger,
} from "@/components/ui/collapsible";
import { ListenButton } from "@/components/ListenButton";
import { useT } from "@/components/LocaleProvider";
import { layerKindKey } from "@/i18n";
import type { ListenSection } from "@/lib/api";

/**
 * Pick the font treatment for an "Original" layer. Devanagari (or any Indic
 * script) gets the Devanagari serif; romanized/IAST text gets a Latin serif
 * with full diacritic coverage so it doesn't render glyph-by-glyph.
 */
function originalScriptClass(body?: string): string {
  if (containsTibetan(body)) return "source-script source-script--tibetan";
  if (containsCjk(body)) return "source-script source-script--cjk";
  if (containsDevanagari(body)) return "source-script";
  return "source-script source-script--latin";
}

function isKeyTerm(item: unknown): item is KeyTerm {
  return Boolean(item && typeof item === "object" && "term" in item && "definition" in item);
}

function isResonance(item: unknown): item is Resonance {
  return Boolean(item && typeof item === "object" && "citation" in item && "resonance" in item);
}

export function LayerBlock({
  layer,
  compact = false,
  defaultCollapsed = false,
  bare = false,
  variant = "card",
  verseId,
}: {
  layer: PratibhaLayer;
  compact?: boolean;
  defaultCollapsed?: boolean;
  /**
   * Render only the layer body (no surrounding card, heading, or built-in
   * collapse) so the block can live inside a <Disclosure> panel that already
   * supplies its own chrome and progressive-disclosure behaviour.
   */
  bare?: boolean;
  /** plain = typographic section without card chrome (study reading flow). */
  variant?: "card" | "plain";
  verseId?: string;
}) {
  const t = useT();
  const items = Array.isArray(layer.items) ? layer.items : [];
  const kindKey = layerKindKey(layer.kind);
  const label = kindKey ? t(kindKey) : layer.label;
  const isOriginal = layer.kind === "original";
  const isPractice = layer.kind === "practice";
  const isAppendix = layer.kind === "appendix";
  const cardClass = isOriginal ? "manuscript-card" : isPractice ? "practice-card" : "card";
  const longBody = (layer.body || "").length > 1200;
  const startCollapsed = !bare && variant === "card" && (defaultCollapsed || (isAppendix && longBody));
  const [open, setOpen] = useState(false);

  if (bare) {
    return (
      <div>
        {layer.kind === "translation" && layer.layer_provenance ? (
          <p className="soft mb-3 font-sans text-xs leading-relaxed text-stone-400">
            {layer.layer_provenance}
          </p>
        ) : null}
        {renderLayerBody(layer, items, { compact, isOriginal, t })}
      </div>
    );
  }

  const listenSection =
    verseId && (layer.kind === "translation" || layer.kind === "commentary" || layer.kind === "practice")
      ? (layer.kind as ListenSection)
      : null;

  if (variant === "plain") {
    const shell =
      isPractice
        ? "passage-practice"
        : `passage-layer passage-layer--${layer.kind}`;
    const labelClass =
      layer.kind === "iast" || layer.kind === "original"
        ? "passage-layer__label passage-layer__label--muted"
        : "passage-layer__label";
    return (
      <section className={shell}>
        {listenSection && verseId ? (
          <ListenButton verseId={verseId} section={listenSection} variant="layer" />
        ) : null}
        <h2 className={labelClass}>{label}</h2>
        {layer.kind === "translation" && layer.layer_provenance ? (
          <p className="soft mt-2 font-sans text-xs leading-relaxed text-stone-400">
            {layer.layer_provenance}
          </p>
        ) : null}
        {renderLayerBody(layer, items, { compact, isOriginal, t })}
      </section>
    );
  }

  return (
    <section className={`${cardClass} mt-5 p-5 sm:mt-6 sm:p-6`}>
      {startCollapsed ? (
        <Collapsible open={open} onOpenChange={setOpen}>
          <CollapsibleTrigger className="w-full cursor-pointer text-left outline-none focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--accent-bright)]">
            <div className="flex items-center justify-between gap-3">
              <h2 className="layer-heading">{label}</h2>
              <span className="font-sans text-xs text-stone-400">{open ? t("common.collapse") : t("common.expand")}</span>
            </div>
            {!open ? <p className="soft mt-2 line-clamp-3 text-sm">{layer.body}</p> : null}
          </CollapsibleTrigger>
          <CollapsibleContent>
            <div
              className={`chat-markdown mt-4 ${
                isOriginal
                  ? `${originalScriptClass(layer.body)} whitespace-pre-wrap text-2xl leading-relaxed text-stone-100`
                  : compact
                    ? "text-sm leading-relaxed"
                    : "reading-prose"
              }`}
            >
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{layer.body || ""}</ReactMarkdown>
            </div>
          </CollapsibleContent>
        </Collapsible>
      ) : (
        <>
          <h2 className="layer-heading">{label}</h2>
          {layer.kind === "translation" && layer.layer_provenance ? (
            <p className="soft mt-2 font-sans text-xs leading-relaxed text-stone-400">
              {layer.layer_provenance}
            </p>
          ) : null}
          {renderLayerBody(layer, items, { compact, isOriginal, t })}
        </>
      )}
    </section>
  );
}

function renderLayerBody(
  layer: PratibhaLayer,
  items: unknown[],
  opts: { compact: boolean; isOriginal: boolean; t: (key: string) => string },
) {
  const { compact, isOriginal, t } = opts;
  if (layer.kind === "key_terms" && items.some(isKeyTerm)) {
    return (
      <div className="mt-4 space-y-3">
        {items.filter(isKeyTerm).map((term) => (
          <article key={`${term.lemma_id || ""}:${term.term}`} className="citation-card p-3">
            <h3 className="text-lg text-amber-100">
              {term.lemma_id ? (
                <Link
                  href={`/glossary/${encodeURIComponent(term.lemma_id)}`}
                  className="inline-flex items-center gap-1 underline decoration-amber-200/30 underline-offset-2 transition hover:decoration-amber-200/70"
                >
                  <InlineMarkdown>{term.term}</InlineMarkdown>
                  <span aria-hidden className="text-[10px] text-amber-200/60">
                    →
                  </span>
                </Link>
              ) : (
                <InlineMarkdown>{term.term}</InlineMarkdown>
              )}
            </h3>
            <p className="soft mt-1 text-sm leading-relaxed">
              <InlineMarkdown>{term.definition}</InlineMarkdown>
            </p>
          </article>
        ))}
      </div>
    );
  }
  if (layer.kind === "resonances" && items.some(isResonance)) {
    return (
      <div className="mt-4 space-y-3">
        {items.filter(isResonance).map((entry) => (
          <article key={entry.citation} className="citation-card p-3">
            <h3 className="text-lg text-amber-100">
              <InlineMarkdown>{entry.citation}</InlineMarkdown>
            </h3>
            <p className="soft mt-1 text-sm leading-relaxed">
              <InlineMarkdown>{entry.resonance}</InlineMarkdown>
            </p>
            {entry.divergence ? (
              <p className="mt-2 text-sm leading-relaxed text-stone-300">
                <span className="font-semibold text-amber-100">{t("layers.divergence")}:</span>{" "}
                <InlineMarkdown>{entry.divergence}</InlineMarkdown>
              </p>
            ) : null}
          </article>
        ))}
      </div>
    );
  }
  const bodyClass = isOriginal
    ? `${originalScriptClass(layer.body)} whitespace-pre-wrap text-2xl leading-relaxed text-stone-100`
    : compact
      ? "text-sm leading-relaxed"
      : "reading-prose";

  if (isOriginal && isLongNativeScript(layer.body)) {
    return <LongNativeScript body={layer.body || ""} className={bodyClass} t={t} />;
  }

  return (
    <div className={`chat-markdown ${bodyClass}`}>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{layer.body || ""}</ReactMarkdown>
    </div>
  );
}

function LongNativeScript({
  body,
  className,
  t,
}: {
  body: string;
  className: string;
  t: (key: string) => string;
}) {
  const [open, setOpen] = useState(false);
  return (
    <div>
      <div className={`chat-markdown ${className} ${open ? "" : "original-window"}`}>
        {open ? (
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{body}</ReactMarkdown>
        ) : (
          <p className="whitespace-pre-wrap">{body}</p>
        )}
      </div>
      <button type="button" className="passage-reading__toggle mt-3" onClick={() => setOpen((v) => !v)}>
        {open ? t("layers.collapseOriginal") : t("layers.expandOriginal")}
      </button>
    </div>
  );
}
