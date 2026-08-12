# maximus-literature-review

**Systematic literature review the way a researcher trained in evidence synthesis would do it.**

Where `maximus-deep-research` aggregates across the web and `maximus-investigative-research` reconstructs a story from primary records, this skill produces a defensible synthesis of an **academic body of work** — with the method visible alongside the findings.

Anyone reading the output should be able to see: what was searched, how papers were selected, why some were excluded, how quality was appraised, and what the confidence of each finding is.

## When to reach for it

- "Literature review on X" / "Lit review" / "Systematic review"
- "State of the field on Y" / "Synthesize the research on Z"
- "What does the peer-reviewed evidence say about..."
- "Meta-analysis lite" (this skill produces the pre-meta-analysis synthesis)
- Grant applications requiring a literature-review section
- Thesis or dissertation background chapters
- Evidence briefs for policy or clinical decision-making

## When NOT to reach for it

- General topic explainer → `maximus-deep-research`
- Investigating an entity or event → `maximus-investigative-research`
- Hypothesis-first inference → `maximus-deep-research-pro`
- Full statistical meta-analysis (forest plots, pooled effect sizes) → use `metafor` in R or `pymare` in Python; this skill produces the synthesis that feeds the stats
- Single-paper summary → just summarize
- Grey-literature-only synthesis → use `maximus-deep-research`

## The 7-phase workflow (PRISMA-inspired)

1. **Scope + PICO/PECO** — structured review question
2. **Search protocol** — databases, dates, Boolean queries, dedup method
3. **Screening** — title/abstract pass, then full-text pass, with reasons
4. **Extraction table** — one row per included paper
5. **Quality appraisal** — Cochrane RoB 2, NOS, ROBINS-I, QUADAS-2, AMSTAR 2, or field equivalent
6. **Synthesis with confidence grading** — findings tagged with GRADE (high / moderate / low / very low)
7. **Report with PRISMA-style flow** — counts, findings, gaps, full extraction table

## What you get

- Structured review question in PICO/PECO/TMBM format
- Documented search protocol (reviewers can reproduce it)
- PRISMA-style flow diagram counts (records identified → included)
- Full extraction table (paper × attributes)
- Quality appraisal per paper
- Findings graded with GRADE
- Explicit "what the literature does not answer" section
- Full list of excluded papers with reasons

## What you do not get

- Vote-counting synthesis ("X papers positive, Y negative") — a discredited method
- Preprints presented as peer-reviewed
- Blog summaries or LLM-generated summaries as literature
- A "systematic review" label if all 7 phases were not executed
- Silent exclusion of papers that disagree with the emerging picture

## Files in this bundle

- `SKILL.md` — spec and workflow (loaded by the agent)
- `README.md` — this file
- `HOWTO.md` — 6 recipes covering the most common lit-review shapes
- `examples/clinical-lit-review.md` — worked trace on a clinical intervention review (RCTs)
- `examples/ml-lit-review.md` — worked trace on an ML-methods review (non-clinical field adaptation)
- `references/prisma-and-grade.md` — PRISMA 2020 flow + GRADE grading rubric with sources
- `references/quality-appraisal-tools.md` — which tool for which study design, with source links
- `references/database-coverage.md` — coverage notes for major databases (2026)

## Integration

- **Downstream:** run `maximus-chain-of-verification` on the final report before external delivery — catches citation drift.
- **Feed forward:** the Phase 4 extraction table feeds a proper statistical meta-analysis in `metafor` (R) or `pymare` (Python).
- **Sibling:** `maximus-deep-research` for web-scale, `maximus-investigative-research` for narrative, `maximus-deep-research-pro` for hypothesis-first.

## Freshness

Literature reviews are dated. Every extraction row date-stamps its paper. The review report's date is its "search cutoff." Do not re-publish an old review without re-running the search.

Last reviewed: **2026-07-31**.
