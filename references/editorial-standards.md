# Pratibha Editorial Standards

## Frozen Style Exemplars

Use these units as the current house standard for tone, specificity, and layer quality:

- `data/raw_texts/#Zhuangzi_pratibha_manuscript.md` — primary exemplar for imagistic, practice-near commentary that stays faithful to the source's form.
- `data/raw_texts/#Phaedo_pratibha_manuscript.md` — primary exemplar for argument-driven philosophical commentary.
- `data/yaml/tao_te_ching/tao_te_ching_md_001.yml` — primary exemplar for philological key terms and high-density cross-tradition resonance.
- `data/yaml/epictetus_works/epictetus_enchiridion_001.yml` — primary exemplar for Greek term work and structural comparison.
- `data/yaml/svetasvatara_upanishad/svetasvatara_001.yml` — primary exemplar for source-grounded Indic metaphysical exposition.

## Content Bar

Every finished unit must satisfy these checks:

- The title makes a claim about the unit's philosophical movement, not merely its topic.
- The body preserves the passage's actual sequence and does not replace it with summary.
- The translation is distinguishable from commentary: it renders; it does not over-explain.
- The commentary opens with a claim and names the contested move.
- Key terms explain etymology, source-specific meaning, and what the default translation misses.
- Resonances cite a specific passage, name the structural homology, and include a divergence clause.
- Practice is a single executable instruction derived from the unit, not a generic meditation prompt.

## Canonical YAML Contract

New canonical units should expose Pratibha layers explicitly instead of burying them inside commentary text. Use this display order:

1. `original`
2. `iast`
3. `translation`
4. `commentary`
5. `key_terms`
6. `resonances`
7. `practice`
8. `appendix`

Recommended unit fields:

```yaml
editorial_maturity: publishable # publishable | strong_draft | needs_rewrite | structural_draft
editorial_score: 28
pratibha_layers:
  - kind: translation
    label: Pratibha Translation
    body: "..."
  - kind: key_terms
    label: Key Terms
    body: "..."
    items:
      - term: "dharma (धर्म)"
        definition: "etymology -> source-specific meaning -> translation stakes"
  - kind: resonances
    label: Cross-Tradition Resonances
    body: "..."
    items:
      - citation: "Epictetus, Enchiridion 1"
        resonance: "structural homology"
        divergence: "where the parallel breaks"
```

Legacy fields such as `translation_literal`, `commentary`, `sanskrit_devanagari`, `sanskrit_iast`, `practice`, and `appendixes` remain accepted by the app loader, but new generation should write `pratibha_layers` so the reader, chat context, and pgvector ingestion share one contract.

## Red Flags

Flag a unit for rewrite when any of these appear:

- The same commentary paragraph could apply to several unrelated passages.
- Key terms repeat generic definitions such as "default translation often misses this operative force in practice."
- Resonances rely on broad tradition names without passage-level specificity.
- Practice says "choose one anchor from this verse" without naming the actual anchor.
- A high schema score masks thin, incomplete, or malformed content.
