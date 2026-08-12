# HOWTO — maximus-literature-review

Six recipes for the lit-review shapes that come up most.

---

## Recipe 1 — Clinical intervention review (RCTs)

**Trigger:** "systematic review of [intervention X] for [condition Y]"

**Structure:**
- **PICO:** Population (condition, age range, setting), Intervention (X), Comparison (usual care / placebo / active comparator), Outcome (primary + secondary)
- **Databases:** PubMed, Embase, Cochrane CENTRAL, Web of Science, plus trial registries (ClinicalTrials.gov, ISRCTN)
- **Study types included:** randomized controlled trials, possibly cluster-RCTs
- **Quality appraisal tool:** Cochrane RoB 2
- **Synthesis:** GRADE per outcome, not per paper. If effect sizes are extractable, this becomes the pre-meta-analysis synthesis.

**Common pitfalls:**
- Trial registration but no published results → note in "what the literature does not answer"
- Multiple publications from the same trial → deduplicate at the trial level, not the paper level
- Selective outcome reporting → flag in quality appraisal

---

## Recipe 2 — Observational epidemiology review

**Trigger:** "review of [exposure] and [outcome]" where RCTs are not feasible

**Structure:**
- **PECO** instead of PICO (Exposure instead of Intervention)
- **Databases:** PubMed, Embase, Scopus, plus field-specific (e.g. Environ Health for environmental exposures)
- **Study types:** cohort, case-control, cross-sectional
- **Quality appraisal tool:** Newcastle-Ottawa Scale or ROBINS-I
- **Synthesis:** GRADE tends to start "low" for observational studies but can be upgraded for large effect, dose-response, or all-plausible-confounding-would-reduce-effect

**Common pitfalls:**
- Ecological fallacy (aggregate-level findings applied to individuals)
- Confounding not addressed
- Reverse causation possible → flag when the direction of association is not established

---

## Recipe 3 — ML / CS methods review (non-clinical field adaptation)

**Trigger:** "review of [method X] for [task Y]" in ML/AI/CS

**Structure adapted for the field:**
- **TMBM:** Task, Method, Baseline, Metric — instead of PICO
- **Databases:** ACM Digital Library, IEEE Xplore, arXiv (treated as preprint tier), NeurIPS/ICML/ICLR proceedings, Papers With Code
- **Study types:** experimental (with released code / benchmarks), theoretical
- **Quality appraisal (adapted):**
  - Reproducibility: code released? datasets available? seeds specified?
  - Evaluation rigor: train/test contamination check? held-out benchmarks? statistical tests?
  - Baseline strength: are the baselines competitive or straw-men?
  - Fair comparison: same compute budget? same data? same tokenization?
- **Synthesis:** report state-of-the-art per benchmark with the exact date and setup

**Common pitfalls:**
- Reporting benchmark scores without noting compute or data used
- Preprint scores that never got peer-reviewed
- Cherry-picked baselines
- Test-set contamination in LLM benchmarks (a huge issue in 2024–2026 — see `references/database-coverage.md`)

---

## Recipe 4 — Rapid review

**Trigger:** "quick lit review on X — need it by [deadline]"

**When rapid is acceptable:** early-stage exploration, feasibility for a full review, urgent decision-support (with acknowledgment of shortcuts)

**Adjustments to the 7-phase workflow:**
- Phase 2: one database instead of 3–5, English-only, tighter date range
- Phase 3: single reviewer instead of dual-independent screening
- Phase 4: extract fewer fields (essentials only)
- Phase 5: quality appraisal on top-tier findings only
- Phase 6: still grade with GRADE

**Rule:** declare every shortcut in the method section. "Rapid review, single reviewer, PubMed only" is honest. "Systematic review" is not.

---

## Recipe 5 — Scoping review

**Trigger:** "what is the landscape of research on X" / "map the field"

**Different goal from a systematic review:** the scoping review answers "what is out there" instead of "what is the answer."

**Adjustments:**
- Phase 1: broader research question, no PICO required
- Phase 2: same as systematic review
- Phase 3: same, with looser inclusion criteria
- Phase 4: extraction table is descriptive (topic, method, sample, gap)
- Phase 5 and 6: **skip** — scoping reviews do not appraise or synthesize evidence quality; they map the field

**Rule:** call it a scoping review, not a systematic review. They have different purposes.

---

## Recipe 6 — Systematic review update

**Trigger:** "update the review from [year X]" / "what's changed since [existing review]"

**Method:**
1. Fetch the existing review
2. Extract its search protocol and cutoff date
3. Re-run the search from cutoff date to today
4. Screen the delta (new papers only)
5. Extract, appraise, synthesize new papers using the existing review's method
6. Compare: what has changed? Any findings overturned? Any new subgroups?
7. Report: "update to [existing review]. Delta: [N new papers]. Findings: [changed / confirmed]."

**Common pitfalls:**
- Not re-running the search — old databases sometimes retract or reclassify papers
- Not re-appraising papers whose quality flags may have changed (e.g. new corrections, retractions)
- Not checking whether an included paper has been retracted since original review

---

## When to bypass this skill and use a sibling

- **Just want a topic explainer** → `maximus-deep-research`
- **Just want a narrative story reconstruction** → `maximus-investigative-research`
- **Just want to test a specific hypothesis** → `maximus-deep-research-pro`
- **Need full statistical meta-analysis** → the extraction table from this skill feeds `metafor` in R
