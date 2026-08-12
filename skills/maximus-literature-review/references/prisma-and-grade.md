# PRISMA 2020 + GRADE reference

The two frameworks this skill inherits from. Sources cited so a reader can go deeper.

## PRISMA 2020

**PRISMA** — Preferred Reporting Items for Systematic Reviews and Meta-Analyses.

**Canonical reference:** Page MJ, McKenzie JE, Bossuyt PM, et al. *The PRISMA 2020 statement: an updated guideline for reporting systematic reviews.* BMJ. 2021;372:n71. [DOI 10.1136/bmj.n71](https://doi.org/10.1136/bmj.n71)

**What PRISMA 2020 covers:**
- 27-item checklist for what to report
- Flow diagram template (records identified → included, with reasons for exclusion)
- Explanation and elaboration document
- Website: [prisma-statement.org](https://www.prisma-statement.org/)

**What this skill inherits from PRISMA:**
- Explicit search protocol before searching
- Two-pass screening (title/abstract, then full-text)
- Every excluded paper gets a reason
- Flow diagram counts at every stage
- Full extraction table

**What this skill does NOT do that a full PRISMA-compliant review does:**
- Register the protocol prospectively (PROSPERO or equivalent)
- Dual independent review (two reviewers screening in parallel, resolving disagreement)
- Formal statistical meta-analysis with heterogeneity metrics (I², τ²)
- Sensitivity analyses and subgroup meta-analyses

If the deliverable needs to be publishable as a peer-reviewed systematic review, the human researcher should complete these steps beyond this skill's output.

## GRADE

**GRADE** — Grading of Recommendations, Assessment, Development and Evaluations.

**Canonical reference:** Guyatt GH, Oxman AD, Vist GE, et al. *GRADE: an emerging consensus on rating quality of evidence and strength of recommendations.* BMJ. 2008;336(7650):924-926. [DOI 10.1136/bmj.39489.470347.AD](https://doi.org/10.1136/bmj.39489.470347.AD)

**GRADE working group website:** [gradeworkinggroup.org](https://www.gradeworkinggroup.org/)

**The four grades:**

| Grade | Meaning |
|---|---|
| **High** | We are very confident that the true effect lies close to that of the estimate. |
| **Moderate** | We are moderately confident: the true effect is likely close to the estimate, but there is a possibility it is substantially different. |
| **Low** | Our confidence is limited: the true effect may be substantially different from the estimate. |
| **Very low** | We have very little confidence in the estimate: the true effect is likely to be substantially different. |

**Factors that DOWNGRADE evidence:**
1. Risk of bias (based on quality appraisal — RoB 2, NOS, ROBINS-I, etc.)
2. Inconsistency (unexplained heterogeneity in effect sizes)
3. Indirectness (population, intervention, comparison, or outcome does not match the review question)
4. Imprecision (wide confidence intervals, small total sample size)
5. Publication bias (funnel plot asymmetry, missing negative studies)

**Factors that UPGRADE evidence (only for observational studies starting at "Low"):**
1. Large effect size
2. Dose-response gradient
3. All plausible confounding would bias against the observed effect

**Starting point:**
- RCTs start at HIGH
- Observational studies start at LOW
- Both can be moved up or down based on the factors above

**How this skill applies GRADE:**
- Grade **each finding**, not each paper. A finding may be supported by 5 papers of varying quality — the grade reflects the aggregate confidence.
- Report the grade inline with each finding.
- Show the reasoning (which factors caused a downgrade or upgrade).

## Common failures the two frameworks prevent

- **Vote-counting synthesis** — "X papers positive, Y papers negative" is not a synthesis. GRADE forces reasoning about effect sizes and quality.
- **Silent exclusion** — PRISMA requires reasons for every exclusion at every stage. A review with no exclusions log is not systematic.
- **Overgrading** — starting all evidence at "high" regardless of design misleads the reader about what the evidence supports.
- **Cherry-picked findings** — the extraction table plus GRADE grading makes cherry-picking visible.

## What NOT to do

- **Do not use GRADE without extracting the underlying evidence.** GRADE is meaningless without the extraction table it grades.
- **Do not label a review "PRISMA-compliant" without executing all 27 items.** This skill produces a PRISMA-*style* review — inspired by, structured after, but not certified compliant without the additional rigor (protocol registration, dual review).
- **Do not use GRADE for scoping reviews.** GRADE grades the strength of evidence for a specific outcome; scoping reviews map fields, not conclusions.

Last reviewed: **2026-07-31**.
