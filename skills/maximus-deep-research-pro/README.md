# Maximus — Deep Research Pro

## What

An inference-driven research skill. It doesn't just collect and cite what sources say — it starts from a falsifiable hypothesis, reasons across independently-sourced facts to derive conclusions no single source states, and actively tries to disprove its own conclusion before presenting it. Every claim in the output carries a confidence tier and a record of counter-evidence, not just a citation.

## When

Use it when:

- A claim needs to survive scrutiny before it drives a decision, a publication, or money ("did Company X really hit $10M ARR?").
- The answer requires triangulating across facts that no single source states together (revenue from headcount + comp + burn rumors + market comps).
- Two authoritative sources disagree and a reasoned position is needed, not a shrug.
- Technical or causal claims need active stress-testing ("does this architecture actually hold at scale?", "did event Y cause outcome Z?").
- A decision brief needs its unknowns explicitly flagged, not smoothed over.

Don't use it for a single clean lookup, or when a synthesized-and-cited summary is all that's needed — see "Why this is different" below.

## Why this is different from `maximus-deep-research`

`maximus-deep-research` is aggregation: fan out across sources, cross-verify anything load-bearing, cite everything, produce a synthesized answer or comparison. It answers "what do the sources collectively say?"

`maximus-deep-research-pro` is inference: it uses that same fan-out discipline as raw material, but adds a layer on top — frame a falsifiable hypothesis first, connect facts across sources to reach conclusions none of them state individually, then actively search for evidence that would break the conclusion before accepting it. It answers "what is actually true, and how confident should I be — and what would change my mind?"

Concretely: aggregation stops at "three sources say X." Inference asks "given fact A from source 1, fact B from source 2, and the absence of expected signal C, what does that imply — and what's the strongest evidence against it?" and shows that reasoning chain explicitly, along with a confidence tier and any disagreement found.

Aggregation without inference under-delivers on a claim that requires reasoning. Inference without aggregation has no raw material to reason over. This skill assumes the aggregation discipline and builds on it — it does not replace `maximus-deep-research` for tasks that only need aggregation.

## Quick example

**Task:** "Did Company X really hit $10M ARR, like their press release claims?"

1. Frame hypothesis: "Company X's ARR is at or above $10M as of the press release date." Name what would confirm it (customer count × avg contract value consistent with $10M; hiring pace consistent with that revenue) and what would kill it (headcount/burn data implying a much smaller base; contradicting analyst estimates).
2. Fan out: press coverage, LinkedIn headcount trend, any funding filings, analyst commentary, competitor comps.
3. Extract atomic facts with sources attached.
4. Cross-source inference: headcount growth rate and typical SaaS revenue-per-employee for the sector triangulate a plausible ARR range.
5. Adversarial pass: search specifically for skepticism, layoffs, or churn signals that would contradict the claim.
6. Confidence ledger: tier each claim, note any counter-evidence found.
7. Gap analysis: true ARR is not publicly disclosed in detail — flag as unknown-public beyond the triangulated range.
8. Synthesize: executive answer with confidence tier, full reasoning trace, ledger, and gaps.

See `examples/triangulation-trace.md` and `examples/hypothesis-falsification-trace.md` for full worked versions.

## Related skills

- **`maximus-deep-research`** — the aggregation sibling this skill builds on top of.
- **`maximus-brain`** — depth-tier calibration for how many iterative loops a task warrants.
- **`maximus-write-article`** — publish the finding once the reasoning trace and ledger exist.
- Built-in **`research-assistant`** — for shallow lookups that don't need hypothesis framing or falsification.

## Files in this skill

- `SKILL.md` — the full procedure (8-step inference loop, ledger format, adversarial protocol, output format).
- `HOWTO.md` — recipes for common inference-driven research tasks.
- `examples/hypothesis-falsification-trace.md` — worked trace where adversarial verification overturns initial confirming evidence.
- `examples/triangulation-trace.md` — worked trace inferring an answer no source states directly.
- `references/inference-patterns.md` — catalog of inference types with examples.
- `references/confidence-ledger-spec.md` — full ledger field spec and tier rules.
- `references/adversarial-verification.md` — falsification protocol and query patterns.
