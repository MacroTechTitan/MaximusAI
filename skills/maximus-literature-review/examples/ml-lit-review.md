# Worked example — ML methods lit review

**Scenario:** A user asks: *"Systematic review of Chain-of-Verification and related self-verification methods for reducing LLM hallucinations."*

Illustrative example — the workflow shape is real; specific numbers are pedagogical.

## Phase 1 — Scope + TMBM

**Review question:** Do self-verification methods (Chain-of-Verification and adjacent techniques) reduce factual hallucinations in LLM outputs compared to direct-answer baselines, and under what conditions?

| Element | Specification |
|---|---|
| Task | Factual QA, list-based questions, long-form generation |
| Method | Chain-of-Verification (Dhuliawala et al., 2023) and adjacent self-verification methods |
| Baseline | Direct-answer generation (no verification pass) |
| Metric | Hallucination rate (FactScore, human eval, benchmark-specific) |

## Phase 2 — Search protocol

- **Databases:** ACM Digital Library, IEEE Xplore, arXiv, NeurIPS/ICML/ICLR proceedings, Papers With Code
- **Search dates:** 2022-01-01 to 2026-07-31
- **Languages:** English only
- **Study types:** experimental papers with released code or reproducible protocols; theoretical papers included if they inform the method

**Illustrative Boolean query (arXiv):**
```
("chain of verification" OR "self-verification" OR "self-consistency" OR "verification loop")
AND (LLM OR "language model" OR GPT OR Claude OR Llama)
AND (hallucination OR "factual accuracy" OR "factual error" OR "fact check")
```

**Results (illustrative counts):**
- arXiv: 178
- ACM DL: 22
- IEEE Xplore: 14
- Conference proceedings (NeurIPS/ICML/ICLR 2023–2026): 31
- Papers With Code: 9
- **Total: 254 → 187 after dedup**

## Phase 3 — Screening

**Pass A — Title/abstract screening (187 records):**
- Included: 34
- Excluded: 153
- Top exclusion reasons:
  - Not about self-verification (n=68) — different reliability technique (RAG only, calibration only)
  - No hallucination-metric comparison (n=42) — theoretical only, no experiment
  - Not applied to LLMs (n=18) — traditional ML classification
  - Position papers / editorials (n=25)

**Pass B — Full-text screening (34 records):**
- Included: 14
- Excluded: 20
- Full-text exclusion reasons:
  - No usable effect metric (n=8) — reported "improved" without numbers
  - Code not released, protocol not reproducible (n=5)
  - Test-set contamination not addressed (n=3) — LLM evaluated on training-data-known benchmark
  - Preprint later withdrawn (n=2)
  - Duplicate reporting (n=2)

**PRISMA-style flow:**

```
Identified: 254
    ↓ dedup (67 removed)
After dedup: 187
    ↓ title/abstract (153 excluded)
Full-text assessed: 34
    ↓ full-text (20 excluded)
Included in synthesis: 14
```

## Phase 4 — Extraction table (excerpt, 3 of 14 rows)

| Paper | Year | Method variant | Base model | Task | Baseline hallucination rate | Method hallucination rate | Δ | Code released | Peer-reviewed |
|---|---|---|---|---|---|---|---|---|---|
| Dhuliawala et al. 2023 | 2023 | CoVe (factored) | Llama-2 65B | Wikidata list Q | 0.15 F1 | 0.35 F1 | +0.20 F1 | Yes | arXiv only at review date |
| [Hypothetical] 2024 | 2024 | CoVe + RAG | GPT-4-turbo | Clinical QA | 12.3% | 2.1% | −10.2pp | Yes | ACL 2024 |
| [Hypothetical] 2026 | 2026 | Iterative CoVe (3 rounds) | Claude Fable 5 | Long-form biography | FactScore 0.56 | FactScore 0.78 | +0.22 | Yes | arXiv, under review |

## Phase 5 — Field-adapted quality appraisal

Applied dimensions from `references/quality-appraisal-tools.md`:

| Paper | Reproducibility | Eval rigor | Baseline strength | Peer-review | Grade |
|---|---|---|---|---|---|
| Dhuliawala 2023 | Strong (code + benchmarks released) | Strong (multiple tasks, ablations) | Strong (compared to CoT, Self-consistency, RAG) | arXiv originally; widely replicated | **Strong** |
| [Hyp] 2024 | Adequate (code released, benchmarks proprietary) | Adequate (single domain, held-out test) | Strong | ACL 2024 | **Adequate** |
| [Hyp] 2026 | Strong (full open source) | Adequate (contamination check performed) | Strong | Under review | **Adequate** |

Of the 14 included: 8 Strong, 5 Adequate, 1 Weak.

## Phase 6 — Synthesis with GRADE (adapted for ML)

### Finding 1: Factored Chain-of-Verification reduces hallucination rate versus direct answer

- Supporting: 12 of 14 studies show directional improvement; 11 statistically significant (paired eval or CI)
- Effect range: +0.15 to +0.30 improvement on task-specific metrics (F1, FactScore, human-rated accuracy)
- Largest gains on **list-based questions** (Dhuliawala 2023 replicated in [Hyp] 2024)
- Smaller but consistent gains on **long-form generation**
- 2 studies null result — both used weak base models where the baseline was already near ceiling
- **GRADE (adapted): MODERATE-to-HIGH.** Consistent direction, strong replication, but variability in effect size means we should not overclaim a specific % improvement.

### Finding 2: CoVe combined with RAG produces further gains in domain-specific tasks

- Supporting: 5 studies, all in clinical or legal domains
- Effect: hallucination rates 1–3% with combined stack vs 10–30% baseline
- **GRADE: MODERATE.** Evidence base is smaller and domain-specific; generalization to other domains unproven.

### Finding 3: Iterative / multi-round CoVe shows diminishing returns after ~3 rounds

- Supporting: 3 studies
- Effect: gains from round 1→2 are ~2x gains from round 2→3
- **GRADE: LOW.** Only 3 studies, one with high reviewer concerns about eval design; generalization unclear.

### Finding 4: Test-time compute cost roughly doubles under CoVe

- Reported by 9 of 14 studies
- Range: 1.8x–2.4x baseline tokens
- **GRADE: HIGH.** Consistent across implementations. Well-established.

## Phase 7 — Report (illustrative)

### Review question

Do self-verification methods reduce factual hallucinations in LLM outputs, and under what conditions?

### Method

- Databases: ACM DL, IEEE Xplore, arXiv, NeurIPS/ICML/ICLR proceedings, Papers With Code
- Date range: 2022-01-01 to 2026-07-31
- Field-adapted quality appraisal (see method section)
- Synthesis: GRADE (adapted for ML)

### PRISMA-style flow

Identified 254 → dedup 187 → title/abstract 34 (153 excluded) → full-text 14 (20 excluded) → **14 included**

### Findings

- **Finding 1:** Factored CoVe reduces hallucination vs direct answer; **GRADE: MODERATE-HIGH**
- **Finding 2:** CoVe + RAG yields further gains in domain-specific tasks; **GRADE: MODERATE**
- **Finding 3:** Iterative CoVe shows diminishing returns; **GRADE: LOW**
- **Finding 4:** Compute cost ~2x baseline; **GRADE: HIGH**

### What the literature does not answer

- Effect on reasoning-chain errors (as opposed to individual claim errors)
- Behavior under adversarial prompting (jailbreak-style attacks)
- Long-horizon (multi-turn) verification consistency
- Non-English hallucination rates
- Cost-benefit tradeoff for low-stakes applications

### Included papers

[full 14-row extraction table]

### Excluded papers with reasons

[20 full-text exclusions with reasons — reviewers will ask]

## What this example demonstrates

- Non-clinical field-adaptation: TMBM instead of PICO, field-adapted quality tool
- Test-set contamination is an active reason for exclusion (2024–2026 issue)
- Findings graded per outcome, not per paper — mixing across the 14 papers to grade specific claims
- Code-release status feeds into quality appraisal (weak code release = weak reproducibility)
- The synthesis provides direction ("CoVe helps") plus caveats ("effect size varies," "long-horizon behavior unknown") — the shape of a defensible ML lit review
