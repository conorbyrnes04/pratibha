import type { KeyTerm, PratibhaLayer, Resonance } from "@/lib/types";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { containsDevanagari } from "@/lib/sanskritScript";

/**
 * Pick the font treatment for an "Original" layer. Devanagari (or any Indic
 * script) gets the Devanagari serif; romanized/IAST text gets a Latin serif
 * with full diacritic coverage so it doesn't render glyph-by-glyph.
 */
function originalScriptClass(body?: string): string {
  return containsDevanagari(body) ? "source-script" : "source-script source-script--latin";
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
}: {
  layer: PratibhaLayer;
  compact?: boolean;
  defaultCollapsed?: boolean;
}) {
  const items = Array.isArray(layer.items) ? layer.items : [];
  const isOriginal = layer.kind === "original";
  const isPractice = layer.kind === "practice";
  const isAppendix = layer.kind === "appendix";
  const cardClass = isOriginal ? "manuscript-card" : isPractice ? "practice-card" : "card";
  const longBody = (layer.body || "").length > 1200;
  const startCollapsed = defaultCollapsed || (isAppendix && longBody);

  return (
    <section className={`${cardClass} mt-4 p-5 sm:p-6`}>
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
            <h3 className="text-lg text-amber-100">{term.term}</h3>
            <p className="soft mt-1 text-sm leading-relaxed">{term.definition}</p>
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
            <h3 className="text-lg text-amber-100">{entry.citation}</h3>
            <p className="soft mt-1 text-sm leading-relaxed">{entry.resonance}</p>
            {entry.divergence ? (
              <p className="mt-2 text-sm leading-relaxed text-stone-300">
                <span className="text-amber-100">Divergence:</span> {entry.divergence}
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
        isOriginal ? `${originalScriptClass(layer.body)} whitespace-pre-wrap text-2xl leading-relaxed text-stone-100` : compact ? "text-sm leading-relaxed" : "reading-prose"
      }`}
    >
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{layer.body || ""}</ReactMarkdown>
    </div>
  );
}
