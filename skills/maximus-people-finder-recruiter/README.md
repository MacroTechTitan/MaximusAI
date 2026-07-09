# maximus-people-finder-recruiter

Deep multi-step recruiter agent for sourcing named candidates or role profiles — across DevOps agencies, software dev shops, IT outsourcing firms, MSPs, technical staffing agencies, and general engineering/product/design/data employers of any type.

This is the "deeper" sibling of **recruiter-deep-find**. Where `recruiter-deep-find` is the intake-form-driven, agency-first workflow (and its standalone app), this skill generalizes the method into an explicit **8-step loop** — Intake, Role Decomposition, Boolean Query Build, Multi-Source Search, Enrichment, Fit Scoring, Verification, Delivery — and widens source coverage beyond agencies to GitHub, Stack Overflow, Kaggle, Behance/Dribbble, conference speaker lists, patent records, OSS contributor lists, and alumni networks.

## Why this exists

A single search pass on a recruiter brief regresses to the most generic, already-tapped candidate pool. Good sourcing is iterative: decompose the role, run many boolean variants across many sources, corroborate every hit with a second independent signal, score against must-haves as a gate (not an average), and only then hand over a slate. This skill encodes that loop so it runs the same way every time, instead of being reinvented — or skipped — per request.

## What's in this skill

- **`SKILL.md`** — the full skill definition: when to use/not use, the 8-step deep loop, intake fields, sources, fit-scoring rubric, boolean query patterns, delivery format, anti-patterns, and privacy rules. Load this first.
- **`HOWTO.md`** — eight ready-to-run recipes covering common recruiting scenarios, from Series B fintech backend hiring to rapid 24-hour intake-to-slate turnaround.
- **`examples/senior-backend-trace.md`** — a full worked trace for a senior backend engineer search: intake through decomposition, boolean queries, raw pool, enrichment, verification, and the final ranked slate.
- **`examples/ml-engineer-trace.md`** — the same full trace for an ML engineer with production LLM experience, showing GitHub + academic paper + LinkedIn triangulation.
- **`references/deep-loop-spec.md`** — the formal specification of the 8-step loop: inputs, outputs, exit criteria, and iteration rules for each step.
- **`references/boolean-query-cookbook.md`** — proven boolean patterns for LinkedIn X-Ray search, GitHub advanced search, Google/Bing site-search, common gotchas, and how to avoid overly narrow queries that under-return.

## How to use it

Load `SKILL.md` when a request matches a recruiter-sourcing trigger ("find candidates for", "source engineers for", "find a senior X at Y", "passive candidate search", "boolean search LinkedIn", "intake for role", "recruiter deep dive", "source for open role", "find candidates matching brief"). Run the 8-step loop start to finish; don't collapse it into a single search call. Deliver a minimum-viable slate (5-8 verified candidates) as a CSV, expanding only on request.

## Sibling skills

- **recruiter-deep-find** — intake-form sibling; agency-first method for DevOps/outsourcing-firm sourcing. Use its agency-enumeration approach as the source list when the brief specifically targets agency/MSP/outsourcing-firm talent.
- **maximus-people-finder** — broader, non-recruiter sibling for investors, journalists, partners, and general person lookups. Redirect there when the ask isn't a hiring req.
- **maximus-brain** — the cognitive loop this skill's 8 steps instantiate for the recruiting domain.

## Privacy

Public professional-profile discovery only — no personal phone numbers, home addresses, or personal email guesses. See the Privacy section in `SKILL.md`.
