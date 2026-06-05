import type { KeyTerm, PratibhaLayer, Resonance } from "@/lib/types";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function isKeyTerm(item: unknown): item is KeyTerm {
  return Boolean(item && typeof item === "object" && "term" in item && "definition" in item);
}

function isResonance(item: unknown): item is Resonance {
  return Boolean(item && typeof item === "object" && "citation" in item && "resonance" in item);
}

export function LayerBlock({ layer, compact = false }: { layer: PratibhaLayer; compact?: boolean }) {
  const items = Array.isArray(layer.items) ? layer.items : [];
  const isOriginal = layer.kind === "original";
  const isPractice = layer.kind === "practice";
  const cardClass = isOriginal ? "manuscript-card" : isPractice ? "practice-card" : "card";

  return (
    <section className={`${cardClass} mt-4 p-5 sm:p-6`}>
      <h2 className="layer-heading">{layer.label}</h2>
      {layer.kind === "key_terms" && items.some(isKeyTerm) ? (
        <div className="mt-4 space-y-3">
          {items.filter(isKeyTerm).map((term) => (
            <article key={term.term} className="citation-card p-3">
              <h3 className="text-lg text-amber-100">{term.term}</h3>
              <p className="soft mt-1 text-sm leading-relaxed">{term.definition}</p>
            </article>
          ))}
        </div>
      ) : layer.kind === "resonances" && items.some(isResonance) ? (
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
      ) : (
        <div
          className={`chat-markdown mt-4 ${
            isOriginal ? "source-script whitespace-pre-wrap text-2xl leading-relaxed text-stone-100" : compact ? "text-sm leading-relaxed" : "reading-prose"
          }`}
        >
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{layer.body || ""}</ReactMarkdown>
        </div>
      )}
    </section>
  );
}
