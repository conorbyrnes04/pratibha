# Pratibha Content Scorecard

The generated `quality_score_unit` values currently measure schema completeness, not editorial maturity. Use this scorecard for content review.

## Scoring Dimensions

Each dimension is scored from 0-5.

- **Source Fidelity** — passage is complete, source basis is explicit, and original-language material is accurate or clearly marked pending.
- **Translation Integrity** — translation renders the passage in a readable voice without turning into commentary.
- **Commentary Specificity** — commentary makes a claim that could not be attached to a different passage without obvious mismatch.
- **Key Term Strength** — terms include etymology, contextual meaning, and translation stakes.
- **Resonance Quality** — parallels are passage-specific, structurally precise, and include divergence.
- **Practice Specificity** — practice is executable, second-person or imperative, and derived from this exact passage.

## Editorial Bands

- **27-30: Publishable** — ready for public-facing corpus after copyedit.
- **22-26: Strong Draft** — content is sound, but one or two layers need polish.
- **16-21: Needs Rewrite Pass** — useful material exists, but generic or incomplete layers weaken the unit.
- **0-15: Structural Draft Only** — schema exists; content should not be treated as mature.

## Initial Triage

- `data/raw_texts/#Zhuangzi_pratibha_manuscript.md`: Publishable / style exemplar.
- `data/raw_texts/#Phaedo_pratibha_manuscript.md`: Publishable / style exemplar.
- `data/raw_texts/#Bhagavad_Gita_pratibha_manuscript.md`: Strong Draft; translation layer often behaves like commentary.
- `data/raw_texts/#Vijnana_Bhairava_pratibha_manuscript.md`: Mixed; Yukti 1-37 strong draft, Yukti 38-112 needs rewrite pass.
- `data/raw_texts/#siva_sutra_pratibha_manuscript.md`: Strong concept draft; needs exact Pratibha layer normalization and copyedit.
- `data/yaml/mandukya_upanishad_karika/mandukya_001.yml`: Structural draft only; content is misplaced into commentary.
- `data/yaml/yoga_spandakarika/SP_01.yaml`: Structural draft; translation/commentary appear source-derived but not yet Pratibha-layered.
