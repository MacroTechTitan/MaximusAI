# Worked Trace — Triangulation

**Task:** "Roughly how much annual revenue does private Company Z (a mid-stage B2B SaaS company) likely have?" No source states this directly — it's private, and no financials are disclosed. This trace shows how to combine 3+ independent facts into an inferred estimate, with the inference chain shown explicitly rather than hidden behind a single number.

---

## Step 1 — Frame Hypothesis

**Hypothesis:** "Company Z's annual recurring revenue (ARR) falls within a specific inferable range, derivable from public proxies, even though no source states it directly."

**Falsifiable form of the estimate:** the range should be internally consistent across at least three independent proxy signals. If the signals imply wildly different ranges, the hypothesis (that a usable estimate is derivable at all) fails, and the honest answer becomes "not reliably inferable from public data."

**What would confirm it:** headcount-based, funding-based, and market-comp-based estimates converge on a similar range.

**What would kill it:** the proxies disagree sharply, or key inputs (headcount, funding size, comp levels) turn out to be unreliable/outdated.

## Step 2 — Fan-Out

Parallel `search_web` and `search_vertical(vertical="people")` queries:
- "Company Z headcount LinkedIn"
- "Company Z funding round size date"
- "Company Z engineering salary levels"
- "Company Z competitors revenue per employee SaaS benchmark"
- "Company Z layoffs OR hiring freeze" (planted here for the later adversarial pass, but useful early context too)

## Step 3 — Extract Facts (independent, atomic, sourced)

1. **Headcount:** ~180 employees, per LinkedIn company page trend, roughly flat over the last two quarters. *(Fact A — independent proxy #1.)*
2. **Most recent funding round:** raised at a $250M valuation roughly 18 months prior, per a funding-database/press report. *(Fact B — independent proxy #2, but note: valuation is not revenue; needs a multiple assumption to connect.)*
3. **Comp levels:** engineering job postings and comp-aggregator data suggest fully-loaded cost per employee (salary + benefits + overhead) in the $180-220K range, consistent with market-rate B2B SaaS engineering comp. *(Fact C — feeds a cost-based cross-check.)*
4. **Sector benchmark:** for growth-stage B2B SaaS companies of similar headcount, publicly reported revenue-per-employee benchmarks (from comparable public companies' filings and industry surveys) commonly fall in the $150K-$300K range per employee at this maturity stage. *(Fact D — independent proxy #3, sourced from public comps, not from Company Z itself.)*
5. **Valuation multiple context:** growth-stage private SaaS companies in the same round-size/valuation bracket have recently priced, per market reports, at roughly 8-15x forward ARR depending on growth rate. *(Fact E — independent proxy #4.)*

Every fact above keeps its own source and is individually true without saying anything about Company Z's revenue on its own. The inference happens in Step 4.

## Step 4 — Cross-Source Inference (the core of the trace)

**Inference chain, shown explicitly:**

- **Proxy 1 — revenue-per-employee (triangulation).** Fact A (180 employees) × Fact D (sector benchmark $150K-$300K revenue/employee) implies ARR roughly in the range of $27M-$54M. *Inference type: triangulation (independent headcount fact × independent sector-benchmark fact).*
- **Proxy 2 — valuation-multiple back-solve (deduction).** Fact B ($250M valuation) ÷ Fact E (8-15x forward ARR multiple) implies forward ARR roughly in the range of $17M-$31M. *Inference type: deduction (if valuation = multiple × ARR, and valuation and multiple range are known, ARR follows arithmetically).* Note this estimates *forward* ARR (what the round was priced against), which is typically higher than *trailing* ARR at time of raise — a distinction worth flagging, not smoothing over.
- **Proxy 3 — cost-structure sanity check (elimination-style reasoning).** Fact C (loaded cost per employee ~$200K) × Fact A (180 employees) implies a total headcount cost base of roughly $36M/year. For a company to sustainably run near that cost base, its ARR would need to be in a range that supports a plausible gross margin and burn rate for its stage — typically this rules out ARR much below roughly $20M (implausibly high burn for the round size in Fact B) and ARR much above roughly $70M (would imply headcount unusually low for revenue scale in this sector). This proxy doesn't pinpoint a number; it *eliminates* the tails of the other two ranges.

**Combined estimate:** the three proxies' ranges overlap in roughly the $25M-$35M ARR band. That overlap — not any single proxy — is the inferred estimate. The convergence across independently-derived proxies is itself the evidence for the range; no single source or fact produced it.

## Step 5 — Adversarial Verification

Queries designed to break this estimate, not confirm it:
- `search_web`: "Company Z layoffs" — checks whether headcount (Fact A) is stale or declining, which would break Proxy 1 and Proxy 3.
- `search_web`: "Company Z revenue disappointing OR miss OR down round" — checks for signals the valuation (Fact B) no longer reflects current performance.
- `search_web`: "Company Z competitors revenue multiple 2026" — checks whether the multiple range (Fact E) used is current, since multiples compress and expand with market conditions.

Result (illustrative): no layoff signal found; one press mention notes headcount growth slowed but did not reverse. No down-round or revenue-miss signal found in the search window. Multiple range (Fact E) confirmed as broadly consistent with recent comparable reports. **No contradiction surfaced** — the estimate survives the adversarial pass, which raises (but does not maximize) confidence.

## Step 6 — Confidence Ledger

| claim | evidence | confidence tier | counter-evidence | inference type |
|---|---|---|---|---|
| Company Z headcount ~180, roughly flat | LinkedIn company page trend | high | none found | direct citation |
| Company Z last raised at ~$250M valuation ~18 months ago | Funding-database/press report | high | none found | direct citation |
| Sector revenue-per-employee benchmark $150K-$300K at this stage | Public company filings, industry survey | medium | benchmarks vary by sub-sector; Company Z's exact sub-sector fit not fully confirmed | expert consensus (industry survey aggregation) |
| Company Z ARR is approximately $25M-$35M | Combination of Facts A-E above | medium | none found in adversarial pass, but estimate rests on multiple assumption-laden proxies, not a disclosed number | triangulation |
| No signal of revenue decline or distress in the adversarial search window | Absence of layoff/down-round/miss coverage | medium | absence of bad news is suggestive, not conclusive — private companies can avoid press before problems become public | negative evidence |

## Step 7 — Gap Analysis

- **Unknown - public:** actual disclosed ARR, gross margin, and net revenue retention are not public for a private company and will not be closable from public sources.
- **Unknown - could probe with X:** a more precise sub-sector revenue-per-employee benchmark (rather than a broad SaaS-stage benchmark) could narrow Proxy 1's range — probeable via a follow-up `search_vertical(vertical="academic")` or industry-report search focused on Company Z's specific vertical.

## Step 8 — Synthesize Reasoning Trace

**Executive answer (medium confidence):** Company Z's ARR is most plausibly in the $25M-$35M range, inferred from convergence across three independent proxies — headcount-based revenue-per-employee benchmarking, a valuation-multiple back-solve from its last funding round, and a cost-structure sanity check — none of which individually states the answer, and none of which was contradicted in an adversarial search pass. This is an inferred range, not a disclosed figure, and should be presented as such.

**Why this is triangulation, not aggregation:** no source says "$25M-$35M." Aggregating the five facts above without connecting them would produce five true statements and no answer. The estimate exists only because the facts were combined with explicit arithmetic and cross-checked against each other — that combination is the deliverable, and it is shown here rather than collapsed into a single unexplained number.
