# Worked example — Clinical intervention review (RCTs)

**Scenario:** A user asks: *"Systematic review of [hypothetical intervention] for [hypothetical condition] — I need the evidence brief for a grant application."*

Illustrative example. All specific numeric results below are fabricated for pedagogy; the workflow shape is real.

## Phase 1 — Scope + PICO

**Review question:** In adults with [Condition X], does [Intervention Y] compared to usual care reduce [Outcome Z] at 12 months?

| Element | Specification |
|---|---|
| Population | Adults ≥18y with Condition X, primary-care setting |
| Intervention | Intervention Y, any dose or duration |
| Comparison | Usual care or active comparator |
| Outcome (primary) | Outcome Z at 12 months |
| Outcome (secondary) | Adverse events, quality of life (validated instrument), all-cause mortality |

## Phase 2 — Search protocol

- **Databases searched:** PubMed, Embase, Cochrane CENTRAL, Web of Science, ClinicalTrials.gov
- **Search dates:** 2015-01-01 to 2026-07-31
- **Languages:** English, Spanish, French
- **Study types:** randomized controlled trials (RCTs), including cluster-RCTs

**Illustrative Boolean query (PubMed):**
```
("Condition X"[MeSH] OR "condition X"[tiab])
AND ("Intervention Y"[MeSH] OR "intervention Y"[tiab])
AND (randomized controlled trial[pt] OR randomised controlled trial[pt])
Filters: English, Spanish, French; 2015-01-01:2026-07-31
```

Equivalent Boolean logic applied to each database with database-specific vocabulary.

**Results (illustrative counts):**
- PubMed: 342 records
- Embase: 418 records
- Cochrane CENTRAL: 89 records
- Web of Science: 205 records
- ClinicalTrials.gov: 47 registered trials
- **Total: 1,101 records → 623 after deduplication (Zotero, DOI + title match)**

## Phase 3 — Screening

**Pass A — Title/abstract screening (623 records):**
- Included: 47
- Excluded: 576
- Top exclusion reasons:
  - Wrong population (n=241) — pediatric or non-target adults
  - Wrong intervention (n=178) — different active agent
  - Not an RCT (n=94) — observational, review, protocol
  - Wrong outcome (n=63) — did not measure Outcome Z

**Pass B — Full-text screening (47 records):**
- Included: 18
- Excluded: 29
- Full-text exclusion reasons:
  - Outcome measured but at wrong timepoint (n=11)
  - Insufficient reporting (n=7) — could not extract effect size
  - Non-active comparator issue (n=6)
  - Retracted paper (n=1) — logged
  - Duplicate of already-included trial (n=4)

**PRISMA-style flow (illustrative):**

```
Identified: 1,101
    ↓ deduplication (478 removed)
After dedup: 623
    ↓ title/abstract screen (576 excluded)
Full-text assessed: 47
    ↓ full-text screen (29 excluded)
Included in synthesis: 18
```

## Phase 4 — Extraction table (excerpt, 3 of 18 rows)

| Paper | Year | Design | N | Population | Intervention | Comparison | Outcome | Effect size | Author-noted limitations |
|---|---|---|---|---|---|---|---|---|---|
| Smith 2019 | 2019 | RCT, parallel | 240 | Adults 45–75, primary care | Y 200mg daily × 12mo | Placebo | Z at 12mo: −4.2 points (95% CI −5.8 to −2.6) | Single-center, limited ethnic diversity |
| Ali 2021 | 2021 | Cluster-RCT | 620 | Adults 30–65, community | Y 100mg daily × 12mo | Usual care | Z at 12mo: −2.1 (95% CI −3.5 to −0.7) | Adherence ~72% |
| Rossi 2023 | 2023 | RCT, parallel | 156 | Adults 50–70, secondary care | Y 200mg daily × 12mo | Active comparator | Z at 12mo: −1.4 (95% CI −3.1 to +0.3) | Small N, high loss-to-followup |

## Phase 5 — Quality appraisal (Cochrane RoB 2, illustrative summary)

| Paper | Randomization | Deviations | Missing data | Outcome measurement | Reported result | Overall |
|---|---|---|---|---|---|---|
| Smith 2019 | Low | Low | Low | Low | Low | **Low** |
| Ali 2021 | Low | Some concerns | Some concerns | Low | Low | **Some concerns** |
| Rossi 2023 | Low | Low | High (loss to followup 28%) | Low | Low | **High** |

Of the 18 included studies (illustrative): 7 Low, 8 Some concerns, 3 High risk of bias.

## Phase 6 — Synthesis with GRADE

### Finding 1: Intervention Y reduces Outcome Z at 12 months versus usual care

- Supporting: 14 of 18 studies show a directional benefit; 8 statistically significant
- Effect range: −0.8 to −4.6 points on the Outcome Z scale
- 4 studies null; 0 studies show harm
- Heterogeneity moderate (illustrative I² ~55%) — likely explained by dose (higher-dose studies show larger effect)
- Risk of bias: mixed (7 Low, 8 Some concerns, 3 High)
- Publication bias: not formally assessed (would require funnel plot in a full meta-analysis)
- **GRADE: MODERATE.** Downgraded one level for inconsistency (moderate heterogeneity). Would upgrade to High with a formal meta-analysis showing consistent effect after subgroup analysis.

### Finding 2: Intervention Y is associated with mild adverse events but no serious safety signals

- Reported by 15 of 18 studies
- Common events: [event A], [event B] — both <10% incidence
- No serious adverse event signal in 18 studies (N=~3,800 total)
- **GRADE: MODERATE.** Downgraded one level for imprecision — total N adequate for common events but underpowered for rare serious events.

### Finding 3: Effect on all-cause mortality is uncertain

- Only 6 studies reported mortality
- All 6 studies were short (12–18 months) — mortality events rare
- Confidence interval crosses null in 5 of 6 studies
- **GRADE: VERY LOW.** Downgraded for imprecision (rare events, short followup) and indirectness (studies not powered for mortality).

## Phase 7 — Report (illustrative)

### Review question

In adults with Condition X, does Intervention Y compared to usual care reduce Outcome Z at 12 months?

### Method

- Databases: PubMed, Embase, Cochrane CENTRAL, Web of Science, ClinicalTrials.gov
- Date range: 2015-01-01 to 2026-07-31
- Boolean queries: see `search-protocol.md`
- Inclusion: adults ≥18, RCT, measured Outcome Z at 12mo
- Quality appraisal: Cochrane RoB 2
- Synthesis: GRADE

### PRISMA-style flow

Identified 1,101 → dedup to 623 → title/abstract screen (576 excluded) → full-text 47 (29 excluded, 1 retracted) → **18 included**

### Findings

- **Finding 1** (Outcome Z reduction): supported by 14/18 studies, effect range −0.8 to −4.6, **GRADE: MODERATE**
- **Finding 2** (adverse events): common mild events, no serious signal, **GRADE: MODERATE**
- **Finding 3** (all-cause mortality): uncertain, **GRADE: VERY LOW**

### What the literature does not answer

- Long-term (>2 year) outcomes
- Effect in specific subgroups (older adults ≥75, ethnic minorities under-represented)
- Cost-effectiveness (only 2 studies reported economic outcomes)
- Optimal dose (studies used 100–400mg daily)

### Included papers

[full extraction table — 18 rows]

### Excluded papers with reasons

[list of 29 full-text-excluded papers with reasons + 1 retracted]

## What this example demonstrates

- The review reports **method visibly** — a reviewer can reproduce the search
- Findings are graded with GRADE, not vote-counted
- The "what the literature does not answer" section is a first-class output
- Retracted paper is explicitly noted — not silently dropped
- Full extraction table (in the actual output) lets a downstream researcher run a proper meta-analysis in R `metafor`
