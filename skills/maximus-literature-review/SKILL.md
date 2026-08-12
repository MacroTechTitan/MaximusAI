---
name: maximus-literature-review
description: Systematic literature review the way a researcher trained in evidence synthesis would do it — PRISMA-style flow, explicit inclusion/exclusion criteria, quality appraisal, grade-of-evidence tags, and a paper-level extraction table. Load when the user says "literature review," "lit review," "systematic review," "state of the field on X," "synthesize the research on Y," "what does the peer-reviewed evidence say," or "review the academic literature." Runs a 7-phase workflow — Scope + PICO/PECO → Search protocol → Screening → Extraction table → Quality appraisal → Synthesis with confidence grading → Report. Distinguishes peer-reviewed evidence from preprints and grey literature. Grades confidence per finding, not per paper. Names what the literature does not answer. Distinct from maximus-deep-research (web-scale aggregation) and maximus-investigative-research (narrative reconstruction).
---

# WHEN TO USE

Load this skill when the user wants a structured synthesis of an academic literature — the kind of output a research assistant with graduate-level methods training would produce. Not a topic explainer. Not a web-scan summary. A defensible synthesis with explicit method.

Specific triggers:
- "Literature review on X"
- "Lit review" / "systematic review"
- "State of the field on Y"
- "Synthesize the research on Z"
- "What does the peer-reviewed evidence say about..."
- "Meta-analysis lite" (full meta-analyses need statistical extraction — this skill produces the pre-meta-analysis synthesis)
- "Review the academic literature"
- "Evidence brief on..."

Also use for:
- Grant applications requiring a literature-review section
- Thesis / dissertation background chapters
- Systematic evidence briefs for policy or clinical decision-making
- Pre-registered review protocols
- Grounding a new research question in the existing literature

# WHEN NOT TO USE

- **General topic explainer** ("what is X?") → use `maximus-deep-research`
- **Investigating an entity or event** → use `maximus-investigative-research`
- **Hypothesis-first inference from multiple sources** → use `maximus-deep-research-pro`
- **Full statistical meta-analysis** (pooled effect sizes, forest plots) → this skill produces the pre-analysis synthesis but does not run the stats; use a proper meta-analysis tool (R `metafor`, Python `pymare`, RevMan)
- **A single-paper summary** → just summarize the paper
- **Grey-literature-only synthesis** (industry reports, white papers) → grey literature is included in this skill's Phase 2 but treated separately; if the user only wants grey lit, use `maximus-deep-research`

# CORE PRINCIPLE

**A defensible literature review is transparent about method, not just about findings.** Anyone reading it should be able to see: what was searched, how papers were selected, why some were excluded, how quality was appraised, and what the confidence of each finding is.

This skill produces both **findings** and the **method that produced the findings** — the second is what makes the review defensible when someone asks "why isn't [famous paper] in here?"

# THE 7-PHASE WORKFLOW (PRISMA-inspired)

## Phase 1 — Scope + PICO/PECO

Define the review question in a structured frame. For clinical/health, use **PICO**:

- **P**opulation / **P**roblem — who or what is the topic
- **I**ntervention / **I**ndicator — what is being applied or measured
- **C**omparison — what is it being compared to (if any)
- **O**utcome — what is the outcome of interest

For epidemiology / observational research, use **PECO**:

- **P**opulation
- **E**xposure (instead of intervention)
- **C**omparison
- **O**utcome

For non-health domains, adapt to the field's equivalent — e.g. in ML research: **T**ask / **M**ethod / **B**aseline / **M**etric.

Output: a one-paragraph scope statement plus the PICO/PECO/TMBM table. If any element is ambiguous, ask the user before searching.

## Phase 2 — Search protocol

Build the search protocol **before** searching. Includes:

**Sources searched:**
- Peer-reviewed databases (PubMed, Web of Science, Scopus, ACM Digital Library, IEEE Xplore, PsycINFO, etc. — pick by field)
- Preprint servers (arXiv, bioRxiv, medRxiv, SSRN) — treated as separate tier
- Google Scholar (as a completeness check, not a primary database — pagination and completeness are unreliable)
- Grey literature (industry reports, gov reports, working papers) — treated as separate tier
- Reference-list mining of key papers (backward citation search)
- Forward citation search on foundational papers

**Search strategy:**
- Boolean query per database (log verbatim — reviewers may ask)
- Date range
- Language restrictions (if any)
- Study-type filters (if any)

**Records log:**
- Total records identified per source
- Deduplication method (e.g. Zotero, DOI + title match)
- Records after deduplication

Output: `search-protocol.md` documenting every search executed.

## Phase 3 — Screening (two passes)

**Pass A: Title + Abstract screening**
- Apply pre-defined inclusion/exclusion criteria
- Flag: include, exclude, unclear (unclear → move to full-text screening)
- Log every excluded paper with a one-word reason (out-of-scope population, wrong outcome, non-empirical, etc.)

**Pass B: Full-text screening**
- Read the full paper for the "include" and "unclear" set
- Apply the criteria again with more evidence
- Log every full-text exclusion with reason

**Inclusion/exclusion criteria (defined upfront):**
- Population match: yes / no
- Study type: (e.g. RCT, cohort, cross-sectional, qualitative, review — specify)
- Outcome measured: yes / no
- Peer-reviewed vs preprint vs grey lit: how each is handled
- Date range: papers before X excluded
- Language: papers not in [languages] excluded

Output: PRISMA-style flow diagram counts:
- Records identified: N
- After dedup: N
- Screened (title/abstract): N included / N excluded
- Full-text assessed: N included / N excluded
- Included in synthesis: N

## Phase 4 — Extraction table

For every included paper, extract:

| Paper | Year | Design | N | Population | Intervention/Exposure | Comparison | Outcome | Effect size or key finding | Limitations noted by authors |
|---|---|---|---|---|---|---|---|---|---|

- One row per paper.
- Verbatim quotes for key findings — do not paraphrase load-bearing claims at this stage.
- Note the effect size and confidence interval where reported (this is what makes a real meta-analysis possible downstream).
- Note the authors' own limitations section — this is a good signal for quality appraisal.

Output: `extraction-table.csv` or `.md`.

## Phase 5 — Quality appraisal

Grade each paper's methodological quality using an appropriate framework:

- **RCTs:** Cochrane Risk of Bias 2 (RoB 2) tool
- **Observational studies:** Newcastle-Ottawa Scale (NOS) or ROBINS-I
- **Diagnostic accuracy:** QUADAS-2
- **Systematic reviews:** AMSTAR 2
- **Qualitative research:** CASP qualitative checklist
- **ML / CS research:** field-specific — evaluate reproducibility (code released? datasets available? seeds specified?), evaluation-set rigor (train/test contamination?), and baseline strength.

Grade each paper: low risk / some concerns / high risk (or field equivalent). Do not exclude papers based on quality alone — extract the finding and let quality appraisal weight the synthesis.

Output: quality appraisal added to the extraction table as a column.

## Phase 6 — Synthesis with confidence grading

Synthesize findings **at the level of each research question**, not paper-by-paper. For each finding:

- How many papers support it?
- What is the range of effect sizes?
- What is the risk of bias across the supporting papers?
- Are there contradicting findings? Why might they differ (population? method? era?)?

Grade each finding using **GRADE** (Grading of Recommendations, Assessment, Development and Evaluations):

- **High:** further research is very unlikely to change our confidence in the estimate
- **Moderate:** further research is likely to have an important impact and may change the estimate
- **Low:** further research is very likely to have an important impact and is likely to change the estimate
- **Very low:** we are very uncertain about the estimate

GRADE considers: risk of bias, inconsistency, indirectness, imprecision, publication bias.

Output: findings block with a GRADE tag per finding.

## Phase 7 — Report with PRISMA-style flow

Deliver in this shape:

```
## Review question

[PICO/PECO statement]

## Method

- Databases searched: [list]
- Date range: [dates]
- Boolean queries: [reference to search-protocol.md]
- Inclusion/exclusion criteria: [list]
- Quality appraisal tool: [name]

## PRISMA-style flow

- Records identified: N
- After dedup: N
- Title/abstract screened: N (X excluded, reasons: ...)
- Full-text assessed: N (X excluded, reasons: ...)
- Included: N

## Findings

### Finding 1: [statement]
- Supporting papers: N (of N included)
- Effect range: [range]
- GRADE: high / moderate / low / very low
- Notes: [contradictions, subgroups, caveats]

### Finding 2: [...]

## What the literature does not answer

[Explicit gaps — questions the review question implied but the evidence base does not resolve]

## Included papers

[Full extraction table]

## Excluded papers with reasons

[Papers that made it to full-text screen and were excluded, with reasons — reviewers will ask]
```

# HARD RULES

1. **Never claim to have run a "systematic review" without executing all 7 phases.** A skimmed set of papers is a scoping review, not a systematic review — label accordingly.
2. **Never treat preprints as peer-reviewed.** Preprints are a distinct tier. Include them, but tag them, and note when a preprint has since been peer-reviewed.
3. **Never use Wikipedia, blog summaries, or LLM-generated summaries as literature.** The literature is the primary papers themselves. Fetch them.
4. **Never synthesize a finding without a GRADE tag.** Ungraded findings mislead the reader.
5. **Never exclude a paper for disagreeing with the emerging synthesis** — that is confirmation bias. Exclusions must map to pre-defined criteria.
6. **Never suppress the "what the literature does not answer" section.** Gaps are findings.
7. **Never fabricate citations.** Every citation is a paper you have actually fetched. DOIs and titles must match.
8. **Never present a review as complete when Google Scholar is the only source.** Field-specific databases have coverage Scholar lacks; Scholar has coverage they lack. Use both plus preprints.
9. **Never bury conflicts of interest** disclosed in included papers. Report them.
10. **Never treat "n significant papers found" as a finding.** Vote-counting (X papers positive, Y papers negative) is a discredited method; use effect sizes and GRADE.

# INTEGRATION WITH OTHER MAXIMUS SKILLS

- **Upstream:** none — this skill is the top of the research stack for academic questions.
- **Downstream:** run `maximus-chain-of-verification` on the final report before external delivery, especially for high-stakes domains (clinical, legal). Citation drift is a specific CoVe target this skill catches upstream but CoVe catches downstream.
- **Sibling:** `maximus-deep-research` for web-scale synthesis, `maximus-investigative-research` for narrative reconstruction, `maximus-deep-research-pro` for hypothesis-first inference across many sources.
- **Feed forward:** the extraction table from Phase 4 can feed a proper statistical meta-analysis (`metafor` in R, `pymare` in Python) — this skill produces the synthesis; the stats tool runs the pooling.

# WHAT THIS SKILL IS NOT

- **Not a meta-analysis.** Meta-analysis runs statistical pooling. This skill produces the synthesis that feeds a meta-analysis.
- **Not a scoping review** (though the workflow adapts down — just skip Phases 5 and 6 formality, keep the PRISMA-style flow).
- **Not a narrative review** (narrative reviews do not require pre-defined criteria; this skill does).
- **Not a rapid review** (rapid reviews are systematic reviews with methodology shortcuts; this skill can be adapted but the shortcuts must be declared).

# FRESHNESS

- Literature reviews are time-stamped. A review from 2024 is not a review as of 2026.
- The extraction table date-stamps every paper's fetch.
- The review report's date is the "search cutoff date" — every claim is as-of that date.
- Do not re-publish an old review without re-running the search.

Last reviewed: **2026-07-31**.
