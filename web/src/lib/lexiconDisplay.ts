import type { LemmaScripts, RelatedRelation } from "@/lib/lexiconTypes";

/** Prefer a non-roman native form when present. */
export function nativeScript(scripts?: LemmaScripts): string | undefined {
  if (!scripts) return undefined;
  return (
    scripts.devanagari ||
    scripts.chinese ||
    scripts.greek ||
    scripts.arabic ||
    undefined
  );
}

/** Prefer IAST / pinyin / latin romanization. */
export function romanization(scripts?: LemmaScripts): string | undefined {
  if (!scripts) return undefined;
  return scripts.iast || scripts.pinyin || scripts.latin || undefined;
}

export function traditionLabel(tag: string): string {
  return tag
    .replace(/[_-]+/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

export function relationLabel(relation: RelatedRelation): string {
  switch (relation) {
    case "related_as":
      return "Related as";
    case "diverges_from":
      return "Diverges from";
    case "rough_analogue":
      return "Rough analogue";
    default:
      return relation;
  }
}

export function nativeScriptClass(scripts?: LemmaScripts): string {
  if (scripts?.devanagari) return "source-script";
  if (scripts?.chinese) return "source-script source-script--latin";
  if (scripts?.greek) return "source-script source-script--latin";
  if (scripts?.arabic) return "source-script source-script--latin";
  return "source-script source-script--latin";
}
