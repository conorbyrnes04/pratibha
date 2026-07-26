import type { KeyTerm, PratibhaLayer, Resonance } from "@/lib/types";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { containsDevanagari, containsTibetan } from "@/lib/sanskritScript";
import { InlineMarkdown } from "@/components/InlineMarkdown";

/**
 * Pick the font treatment for an "Original" layer. Devanagari (or any Indic
 * script) gets the Devanagari serif; romanized/IAST text gets a Latin serif
 * with full diacritic coverage so it doesn't render glyph-by-glyph.
 */
function originalScriptClass(body?: string): string {
  if (containsTibetan(body)) return "source-script source-script--tibetan";
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
}) {
  const items = Array.isArray(layer.items) ? layer.items : [];
  const isOriginal = layer.kind === "original";
  const isPractice = layer.kind === "practice";
  const isAppendix = layer.kind === "appendix";
  const cardClass = isOriginal ? "manuscript-card" : isPractice ? "practice-card" : "card";
  const longBody = (layer.body || "").length > 1200;
  const startCollapsed = !bare && variant === "card" && (defaultCollapsed || (isAppendix && longBody));

  if (bare) {
    return (
      <div>
        {layer.kind === "translation" && layer.layer_provenance ? (
          <p className="soft mb-3 font-sans text-xs leading-relaxed text-stone-400">
            {layer.layer_provenance}
          </p>
        ) : null}
        {renderLayerBody(layer, items, { compact, isOriginal })}
      </div>
    );
  }

  if (variant === "plain") {
    const shell =
      isPractice
        ? "passage-practice"
        : `passage-layer passage-layer--${layer.kind}`;
    return (
      <section className={shell}>
        <h2 className="layer-heading">{layer.label}</h2>
        {layer.kind === "translation" && layer.layer_provenance ? (
          <p className="soft mt-2 font-sans text-xs leading-relaxed text-stone-400">
            {layer.layer_provenance}
          </p>
        ) : null}
        {renderLayerBody(layer, items, { compact, isOriginal })}
      </section>
    );
  }

  return (
    <section className={`${cardClass} mt-5 p-5 sm:mt-6 sm:p-6`}>
      {startCollapsed ? (
        <details className="group">
          <summary className="cursor-pointer list-none">
            <div className="flex items-center justify-between gap-3">
              <h2 className="layer-heading">{layer.label}</h2>
              <span className="font-sans text-xs text-stone-400 group-open:hidden">Expand</span>
            </div>
            <p className="soft mt-2 text-sm group-open:hidden line-clamp-3">{layer.body}</p>
          </summary>
          <div
            className={`chat-markdown mt-4 ${
              isOriginal ? `${originalScriptClass(layer.body)} whitespace-pre-wrap text-2xl leading-relaxed text-stone-100` : compact ? "text-sm leading-relaxed" : "reading-prose"
            }`}
          >
            <ReactMarkdown remarkPlugins={[remarkGfm]}>{layer.body || ""}</ReactMarkdown>
          </div>
        </details>
      ) : (
        <>
          <h2 className="layer-heading">{layer.label}</h2>
          {layer.kind === "translation" && layer.layer_provenance ? (
            <p className="soft mt-2 font-sans text-xs leading-relaxed text-stone-400">
              {layer.layer_provenance}
            </p>
          ) : null}
          {renderLayerBody(layer, items, { compact, isOriginal })}
        </>
      )}
    </section>
  );
}

function renderLayerBody(
  layer: PratibhaLayer,
  items: unknown[],
  opts: { compact: boolean; isOriginal: boolean },
) {
  const { compact, isOriginal } = opts;
  if (layer.kind === "key_terms" && items.some(isKeyTerm)) {
    return (
      <div className="mt-4 space-y-3">
        {items.filter(isKeyTerm).map((term) => (
          <article key={term.term} className="citation-card p-3">
            <h3 className="text-lg text-amber-100">
              <InlineMarkdown>{term.term}</InlineMarkdown>
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
                <span className="font-semibold text-amber-100">Divergence:</span>{" "}
                <InlineMarkdown>{entry.divergence}</InlineMarkdown>
              </p>
            ) : null}
          </article>
        ))}
      </div>
    );
  }
  return (
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
  );
}
