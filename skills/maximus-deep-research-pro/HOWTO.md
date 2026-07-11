# HOWTO — Deep Research Pro Recipes

Each recipe below is a compressed pass through the 8-step inference loop (`SKILL.md`) tuned for a specific task shape. All of them still end with a confidence ledger and labeled gaps — that part never gets skipped.

## (a) Investigate a specific claim

*"Did Company X really hit $10M ARR?"*

1. **Frame hypothesis.** Write the claim as stated, then write its falsified form: "Company X's actual ARR is materially below $10M." Name concrete disconfirming signals up front: layoffs, churn commentary, contradicting analyst notes, headcount inconsistent with the claim.
2. **Fan-out.** Search the press release itself, follow-up coverage, LinkedIn/headcount trend, any funding or hiring filings.
3. **Extract facts** with `fetch_url` — pull exact numbers and dates, not paraphrases.
4. **Cross-source inference.** Headcount × typical revenue-per-employee for the sector gives a plausible range (base-rate reasoning). Compare that range to the claim.
5. **Adversarial pass.** Search explicitly for "[Company X] layoffs", "[Company X] churn", "[Company X] revenue skeptic" — queries built to surface the falsified form, not confirm the original.
6. **Ledger.** Tier the ARR claim based on whether the range triangulated in step 4 is consistent with the stated number, and note any adversarial findings.
7. **Gaps.** True ARR is rarely public in detail for a private company — flag the residual as unknown-public, with the triangulated range as the best available substitute.
8. **Trace.** Executive answer states the range and confidence, not a false yes/no.

## (b) Triangulate a metric no single source states

*"What's Company Y's approximate headcount-adjusted burn rate?"*

Use when the metric literally does not exist in any single document. Gather 3+ independent facts (headcount from LinkedIn, average comp from Levels.fyi-style data or job postings, funding round size and date, runway rumors from press) and combine them with explicit arithmetic, showing every step. See `examples/triangulation-trace.md` for the full worked version — do not skip showing the inference chain; the chain is the deliverable, not the final number alone.

## (c) Evaluate contradicting claims from two authoritative sources

*Source A (vendor benchmark) says X; Source B (independent lab) says not-X.*

1. Frame the hypothesis as the disagreement itself: "Which claim holds under independent scrutiny, and why do they differ?"
2. Check source tier and independence for both — is B truly independent, or downstream of A's methodology?
3. Look for a third source, ideally a different methodology entirely, to break the tie (triangulation).
4. If no tiebreaker exists, don't average the two claims. Report both, the likely reason for the divergence (methodology, sample, incentive), and a confidence tier reflecting the unresolved disagreement — usually medium or low, not high.
5. Adversarial pass: search for the methodology or dataset each side used — divergent methodology is itself a form of counter-evidence for whichever claim rests on the weaker one.

## (d) Due diligence on a private company or founder

1. Frame hypotheses per dimension: team credibility, market size claim, traction claim, competitive moat claim. Each gets its own falsifiable form.
2. Fan-out per dimension; use `search_vertical(vertical="people")` for founder background, `search_vertical(vertical="academic")` if the moat claim rests on technical IP.
3. Delegate self-contained dimensions (e.g., "verify founder's prior company outcome") to a `research`-type subagent via `run_subagent` — keep the parent thread on cross-dimension inference.
4. Adversarial pass per dimension: litigation search on the founder, "[company] lawsuit", "[company] competitor teardown", "[founder] previous startup failure".
5. Ledger rows per dimension, not one blended score — a diligence brief that collapses everything into one number hides exactly the disagreement a reader needs to see.
6. Gaps: private financials, cap table, and real churn are almost always unknown-public. Say so.

## (e) Technical investigation — does approach X actually work at scale?

*"Does prompt caching actually save 90% on inference cost?"*

1. Frame hypothesis with the specific boundary condition that makes it falsifiable: "at production scale" or "under variable-prefix traffic," not a vague "does it work."
2. Fan-out: vendor documentation and benchmarks (primary but interested), `search_vertical(vertical="academic")` for independent measurement, practitioner reports (forums, engineering blogs) for real-world variance.
3. Cross-source inference: reconcile the vendor's best-case number against practitioner-reported variance — deduce the conditions under which each holds.
4. Adversarial pass: search specifically for "[approach] doesn't work", "[approach] limitations", "[approach] worst case" — the failure-mode query, not the benchmark-repeat query.
5. Ledger: tier the claim as conditional ("high confidence under condition A, medium under condition B") rather than a single number. See `examples/hypothesis-falsification-trace.md`.

## (f) Causal reasoning — did event Y cause outcome Z?

1. Frame the hypothesis as a causal claim with an explicit alternative: "Y caused Z" vs. "Z would have happened anyway / had another cause."
2. Fan-out for timeline precision — causal claims collapse fast when the timeline doesn't actually support the sequence.
3. Look for a natural comparison (a similar case where Y didn't happen — did Z still occur?) — this is elimination-style reasoning applied to causation.
4. Adversarial pass: search for alternative explanations explicitly — "[outcome Z] reasons", "[outcome Z] analysts attribute to" — don't just search for confirmation of Y's role.
5. Ledger: causal claims rarely earn "high" confidence from public sources alone unless there's a controlled comparison or expert consensus with cited mechanism. Default to medium/low and say why.

## (g) Forecasting with base rates

*"What's the probability that X happens by [date]?"*

1. Frame as a probability, not a binary — "will X happen" is the wrong frame; "what's P(X) given current evidence" is the right one.
2. Establish the base rate first: how often does this class of event happen, historically, independent of the specific case (base-rate reasoning).
3. Fan-out for case-specific evidence that should move the probability up or down from that base rate.
4. Adversarial pass: search for the strongest case against the specific-evidence adjustment — is the case-specific evidence itself reliable, or overconfident?
5. Ledger: report a range or qualitative probability band (e.g., "more likely than not, roughly 60-70%") with the base rate and adjustment shown separately — never present a single-point probability as more precise than the evidence supports.

## (h) Gap-flagging pass for a decision brief

Use this when a brief already exists (yours or someone else's) and the task is specifically to audit its unknowns, not produce new research from scratch.

1. Read the existing brief and extract every claim it makes.
2. For each claim, ask: is there a citation? Is it single-source? Was it ever adversarially checked?
3. Reclassify each claim into the confidence ledger with an honest tier — most first-pass briefs over-claim "high" confidence on claims that are really "medium."
4. Run an adversarial query for the 2-3 claims the brief's recommendation most depends on.
5. Produce a short gap-flagging addendum: which claims hold, which dropped a tier, and what remains unknown-public vs. unknown-probeable. This addendum, not a full rewrite, is often the highest-value deliverable — it tells the decision-maker exactly where the brief is solid and where it's guessing.
