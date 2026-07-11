# Worked Trace — Hypothesis Falsification

**Task:** "Does prompt caching actually save 90% on inference cost?" (A claim commonly repeated after major LLM providers announced prompt/context caching features.)

This trace shows the full 8-step inference loop, including the point where the adversarial pass changes the conclusion.

---

## Step 1 — Frame Hypothesis

**Hypothesis (as commonly stated):** "Prompt caching reduces inference cost by approximately 90% in production use."

**Falsifiable form:** for this to hold, cached-token discounts (typically ~90% off cached input tokens, per provider pricing pages) must apply to a large share of *actual* production traffic — not just to a benchmark request repeated verbatim.

**What would confirm it:** independent measurements showing ~90% effective cost reduction across a realistic, varied workload.

**What would kill it:** evidence that real-world cache hit rates are much lower than benchmark conditions, making the *effective* savings far below the *per-token* discount.

**What's being conflated (named up front, since it's the likely failure mode):** "90% discount per cached token" (a pricing fact) versus "90% total cost reduction" (a workload-dependent outcome). These are not the same claim.

## Step 2 — Fan-Out

Parallel `search_web` queries:
- "prompt caching cost savings announcement"
- "prompt caching pricing discount percentage"
- "prompt caching production cost savings real world"
- "prompt caching cache hit rate"

`search_vertical(vertical="academic")`:
- "KV cache reuse LLM serving cost"

## Step 3 — Extract Facts

- Provider pricing pages state cached input tokens are billed at a fraction (commonly cited around 90% off) of standard input token price — this is a pricing-page fact, tier: primary source, direct citation.
- Vendor announcement blog posts repeat "up to 90% cost savings" — tier: vendor-authored, direct citation, same underlying claim as the pricing page (not an independent confirmation).
- Independent engineering blog posts describe caching benefits mostly in benchmark or single-session contexts (e.g., long system prompt reused across many calls in a tight loop).

At this point, the evidence looks confirming: multiple sources, same number. **This is exactly where a first-pass (aggregation-only) research process would stop and report "confirmed, 90% savings."**

## Step 4 — Cross-Source Inference

Connecting the facts rather than just counting them: the "90%" figure applies specifically to tokens that hit the cache. It says nothing about *what fraction of total tokens in a real workload will hit the cache*. That fraction depends on how much of the prompt prefix is identical across consecutive requests — a fact about traffic patterns, not about the discount itself.

**Inference type: deduction.** If (a) the discount applies only to cache hits, and (b) hit rate depends on prefix stability across requests, then (c) total cost savings equal roughly `hit_rate × 90%`, not a flat 90%, unless hit rate is close to 100%. This derived relationship is not stated by any single source — it follows from combining the pricing mechanics with basic reasoning about traffic.

## Step 5 — Adversarial Verification

Designed specifically to surface disconfirming evidence, not to re-confirm:

- `search_web`: "prompt caching cache hit rate degradation production"
- `search_web`: "prompt caching worst case cost increase"
- `search_web`: "prompt caching doesn't help variable prompts"

Result: a practitioner report describes a production workload with variable user-specific content early in the prompt (breaking prefix stability), where the effective cache hit rate stayed well below the benchmark scenario, and overall cost reduction landed closer to 30-40% rather than 90%, despite the same per-token discount applying whenever a hit did occur.

**This is a real contradiction of the "90% typical" framing** — not of the pricing fact, but of the generalized claim that 90% is what production users should expect.

## Step 6 — Confidence Ledger

| claim | evidence | confidence tier | counter-evidence | inference type |
|---|---|---|---|---|
| Cached tokens are billed at ~90% discount vs. standard input tokens | Provider pricing pages | high | none — this is a stated pricing mechanic, not a workload outcome | direct citation |
| Total cost savings from caching equal roughly `hit_rate × discount`, not a flat 90% | Derived from pricing mechanics + traffic-pattern reasoning | high | none found; this is a deductive consequence of an established mechanic | deduction |
| "Prompt caching saves ~90% on inference cost" (as a general production expectation) | Vendor posts + benchmark blog posts (originally) | medium, revised down from initial "high" | practitioner report showing ~30-40% effective savings under variable-prefix production traffic | direct citation (initial), overturned in part by negative/contradicting case evidence |
| Savings are highest for workloads with long, stable, reused prefixes (e.g., fixed system prompts, RAG contexts reused across many queries) | Cross-source inference from mechanic + practitioner report | high | none — consistent across all evidence, including the contradicting case, which confirms the mechanism even while showing lower real-world hit rates | triangulation |

## Step 7 — Gap Analysis

- **Unknown - could probe with X:** exact hit-rate distributions across common workload types (chatbot vs. RAG vs. agent-with-tools) are not systematically published. Could probe by running a controlled benchmark, or by searching for provider-published hit-rate telemetry if any exists.
- **Unknown - public:** any given company's actual internal hit rate and realized savings are not publicly disclosed unless they blog about it. Treat any single-company number as an anecdote, not a population estimate.

## Step 8 — Synthesize Reasoning Trace

**Executive answer (medium confidence, workload-dependent):** The "90%" figure is real but describes the *discount on cache hits*, not the *total cost reduction* a typical production system should expect. Realized savings scale with how often requests actually hit the cache, which depends on prefix stability. Workloads with long, stable, reused prefixes (fixed system prompts, repeated RAG context) can approach the 90% figure; workloads with variable content early in the prompt have been observed, in at least one independent practitioner report, to land closer to 30-40% — the mechanism still works, but "90%" is the ceiling, not the typical outcome.

**What changed the conclusion:** the adversarial pass in Step 5. Without it, the answer would have shipped as "confirmed: ~90% savings" on the strength of three sources that were, on inspection, one claim repeated three times rather than three independent confirmations.

**Sources referenced in this trace (illustrative — replace with live fetches when running this for real):** provider pricing documentation, vendor announcement posts, independent engineering practitioner reports, and academic literature on KV-cache reuse in LLM serving.
