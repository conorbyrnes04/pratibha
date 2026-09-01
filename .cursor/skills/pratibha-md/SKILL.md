---
name: pratibha-md
description: >
  Use this skill whenever Conor asks to produce a Pratibha MD document, process
  a canonical text into the Pratibha format, generate layers for a philosophical
  passage, or add units to the Pratibha corpus. Triggers include mentions of
  "Pratibha", "pratibha-md", "canonical MD", "add this to the corpus", or
  requests to translate and annotate philosophical texts in the multi-layer
  format.
---

# Pratibha MD Generation Skill

## What This Skill Is

Pratibha is a multi-tradition contemplative anthology. Each unit contains a
primary passage with seven annotated layers.

Before producing output, enforce these three constraints:
- Resonances must cite specific passages and structural homology.
- Commentary must make a philosophical claim, not paraphrase translation.
- Key Terms must do etymological and contextual work, not list words.

## Unit Structure (Exact Order)

Every unit must contain exactly these layers, in this order:

```md
## [Title]
**Source:** [Author, Text, Section/Chapter/Verse reference]

[Body — complete passage, never truncated]

---

### Devanagari [or: Original]
### IAST
### Pratibha Translation
### Pratibha Commentary
### Key Terms
### Cross-Tradition Resonances
### Practice (Abhyasa)
```

## Layer Rules

### Title
- Thematic claim, not just verse number.
- Good: "The Division That Liberates"
- Bad: "Enchiridion §1"

### Body
- Full passage only, never truncated.
- Never paraphrase.
- For dialogue: preserve argument arc (setup -> development -> punchline).

### Devanagari / Original
- Sanskrit: Devanagari required and source-verified.
- Greek/Chinese/Arabic/Persian: use `Original` and provide source script when available.
- If unavailable, explicitly label the source-language basis.

### IAST
- Full diacritics required for Sanskrit.
- Break compounds at morpheme boundaries.
- Preserve canonical spellings: `pratyabhijna`, `Ksemaraja`, `Siva`, `Sakti`, `Atman`, `prana`.

### Pratibha Translation

Require:
- Present tense for general philosophical claims.
- Readable aloud; modern but precise.
- Technical terms preserved on first occurrence in brackets.
- Prefer active voice and specificity.

Avoid:
- Archaic inflation ("verily", "thus saith") unless textually necessary.
- Flat literalism that destroys intelligibility.
- Smoothing away philosophical precision.

### Pratibha Commentary

Minimum 150 words. Must:
1. Open with explicit philosophical claim.
2. Name the contested/counterintuitive move.
3. Avoid restating the translation.
4. Situate the claim in the source tradition.
5. Point toward existential application.

Failure modes:
- Opening with "In this passage..."
- Hedge-heavy academic phrasing.
- Generic summary detached from the actual line-level logic.

### Key Terms

Include only terms doing real philosophical work.
Format:

```md
**term (script)** — etymology -> tradition-specific meaning in this passage -> what default translation misses and why it matters
```

On first appearance in a document, include robust entries for:
- `ajatvada`
- `pratyabhijna`
- `spanda`
- `vikalpa`
- `prohairesis`
- `hegemonikon`
- `wuwei`

### Cross-Tradition Resonances

2-4 entries per unit.

Each entry must include:
1. Structural homology (not just shared theme).
2. Specific cited passage.
3. Divergence clause explaining where the parallel breaks and why it is productive.

Format:

```md
**[Tradition/Author, Text, Passage]:** [Structural resonance.]
*Divergence:* [Where the parallel fails and why that matters.]
```

### Practice (Abhyasa)
- Present tense, second person.
- Single executable instruction.
- Derive from this exact passage, not generic tradition.
- No dependence on specialist tools/lineage requirements.

## Source-Type Routing

### Aphoristic texts
- One unit per numbered section.
- Preserve terseness; avoid over-generalization.

### Dialogic texts
- Segment by argument arcs, not paragraphs.
- Keep dialogic framing intact.

### Verse + commentary traditions
- Root verse remains primary unit.
- Traditional commentary integrated into Pratibha Commentary layer.

### Treatise/discourse
- Segment by philosophical move, not heading labels.

## Corpus Conventions

### Indic
- Devanagari + full IAST.
- Keep `ajatvada`, `pratyabhijna`, `spanda`, `vikalpa` untranslated, with strong Key Terms.

### Greek
- Prefer Greek for key lines; transliterated terms required in Key Terms.

### Chinese
- Traditional characters in `Original`; pinyin with tones in Key Terms.

### Arabic/Persian
- Mark source language clearly; ALA-LC style transliteration in Key Terms.

### Christian mystical
- Use original language where available for anchor lines.

## Quality Checklist

- [ ] Title is thematic claim
- [ ] Body complete, no truncation
- [ ] IAST with full diacritics and clear compounds
- [ ] Commentary >= 150 words and claim-led
- [ ] Key Terms are etymology + contextual semantics + translation departure
- [ ] Resonances are structural, specific, and include divergence
- [ ] Practice is executable and passage-specific

## References

- `references/resonance-log.md`
- `references/translation-decisions.md`
- Full-work ingest (PD source, ≥25 units, ten heroes, mandala, TTS): `.cursor/skills/text-ingest/SKILL.md`
