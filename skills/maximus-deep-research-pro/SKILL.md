---
name: maximus-deep-research-pro
description: "Inference-driven deep research that goes beyond aggregation: it reasons across sources to derive conclusions no single source states, actively tries to falsify its own hypothesis before confirming it, and tracks confidence and disagreement explicitly. Use for 'deep research pro', 'research and reason', 'go beyond search', 'infer from sources', 'hypothesis-driven research', 'falsify this claim', 'what does the evidence actually say', 'adversarial research', 'reasoning trace', 'cross-source inference', 'due diligence', 'investigate this'. Runs an 8-step inference loop with a confidence ledger and adversarial verification pass. WHEN NOT TO USE: single-question lookups (just search), aggregation-only synthesis with no inference required (use maximus-deep-research), or tasks needing only plain web search (use built-in research-assistant)."
metadata:
  pillar: research
  source: maximus
---

# Maximus — Deep Research Pro

`maximus-deep-research` answers "what do the sources say?" This skill answers "what is actually true, and how confident should I be?" Aggregation collects and cites. Inference reasons across what's collected to reach a conclusion that no single fetched page states outright — then tries to break that conclusion before it ships.

Most research failures at this tier aren't missing sources. They're a plausible-sounding conclusion that was never actually attacked. This skill installs the counter-pattern: state the hypothesis before searching, search to falsify it, only accept it if it survives, and carry a visible confidence and disagreement ledger the whole way through.

## When to use

- The user says "deep research pro", "research and reason", "go beyond search", "infer from sources", "hypothesis-driven research", "falsify this claim", "what does the evidence actually say", "adversarial research", "reasoning trace", "cross-source inference", "due diligence", or "investigate this".
- The answer requires connecting independent facts that no single source states together (triangulating a private company's revenue, inferring whether a technical claim holds at scale, reasoning about causation).
- Two authoritative sources disagree and the user needs a reasoned position, not a shrug.
- A claim needs active stress-testing before it's relied on for a decision, a publication, or money.

## When NOT to use

- Single-question lookups with one clean answer ("what's the current 10-year yield") — just search.
- Aggregation-only tasks: the user wants a synthesized, cited summary of what sources say, with no derived conclusion beyond that. Use `maximus-deep-research`.
- Tasks needing only web search with light synthesis and no falsification discipline. Use the built-in `research-assistant`.

## Purpose: inference over aggregation

Aggregation asks: *what do the sources collectively say?* It fans out, dedups, cross-verifies, and cites. It is necessary but not sufficient when the real question is one no source answers directly — a private valuation, whether an architecture actually holds up under load, whether an event caused an outcome, the true probability of something happening.

Inference asks: *given what the sources say, what follows — and could I be wrong?* It starts with a falsifiable hypothesis, uses aggregation as raw material, then reasons across facts (triangulation, deduction, elimination, base rates) to a conclusion, and spends real effort trying to break that conclusion before presenting it. The deliverable is not a cited summary — it's a reasoning trace with a confidence tier attached to every load-bearing claim.

## The 8-Step Inference Loop

Run these in order. Each step's output feeds the next. Do not skip to synthesis before the adversarial pass — that's the single most common failure mode this skill exists to prevent.

1. **Frame Hypothesis.** State the claim or question as a falsifiable proposition, not a vague topic. "Company X has ~$10M ARR" is falsifiable; "how is Company X doing" is not. Name what evidence would confirm it and what evidence would kill it, before searching for either.
2. **Fan-Out.** Issue parallel `search_web` queries across the sub-questions the hypothesis breaks into. Use `search_vertical(vertical="academic")` for primary research literature, `search_vertical(vertical="people")` for founder/team background. For self-contained sub-questions, delegate to a `research`-type subagent via `run_subagent` with a complete, standalone brief. Check `memory_search` first for anything already established in prior sessions.
3. **Extract Facts.** Fetch promising sources with `fetch_url` using a targeted extraction prompt. Pull out atomic, attributable facts — not summaries. Each fact keeps its source URL and publication date.
4. **Cross-Source Inference.** Connect independent facts the sources never connected themselves. Name the inference type used for each derived claim (see Inference types below) — this is what separates this skill from citation-stitching.
5. **Adversarial Verification.** For every claim the conclusion leans on, run at least one query *designed to disprove it* — not a confirming rephrase. See the Adversarial verification protocol below. This step is mandatory, not optional, even when the first pass felt conclusive.
6. **Confidence Ledger.** For every claim in the emerging answer, record evidence, inference type, confidence tier, and any counter-evidence found in step 5. See the Confidence Ledger format below.
7. **Gap Analysis.** Identify what remains unknown after steps 2–6. Classify each gap as unknown-but-probeable (name the next query or source) or unknown-from-public-sources (say so plainly; don't paper over it with a confident guess).
8. **Synthesize Reasoning Trace.** Write the executive answer, then show the chain that produced it: hypothesis → evidence → inference → adversarial result → confidence → residual gaps. The trace is not an appendix — it's the point of the deliverable.

If step 5 surfaces a real contradiction, loop back to step 1 with a revised hypothesis rather than forcing the original claim to survive. Revision is success, not failure.

Worked micro-example (full traces live in `examples/`): hypothesis — "Vendor A's caching layer cuts inference cost by 90% at production scale." Fan-out finds the vendor's own benchmark plus two independent blog posts repeating it (direct citation, one source underneath three mentions — not three data points). Adversarial pass searches specifically for "cache hit rate degradation production" and "prompt caching worst case cost" and turns up a practitioner report where cache hit rate collapsed under variable-prefix traffic, cutting the savings to roughly 40%. Conclusion revises from "90% typical" (high confidence) to "up to 90% under favorable prefix-reuse patterns, closer to 40% under variable traffic" (medium confidence, workload-dependent) — the adversarial pass changed the shape of the answer, not just its footnotes.

## The Iterative Depth Loop

After the first pass through steps 1–8, ask explicitly: **"What single piece of evidence would change this conclusion?"** Then go find it, specifically — not more of the same evidence you already have. Repeat this depth loop until either (a) the answer stops changing across a full iteration, or (b) the remaining unknowns are flagged unknown-from-public-sources rather than chased further. Depth is a deliberate choice, not an accident of how many searches happened to run — see `maximus-brain`'s depth-tier framework for calibrating how many loops the task actually warrants.

## The Confidence Ledger format

Every material claim in the final answer gets a row:

| claim | evidence | confidence tier | counter-evidence | inference type |
|---|---|---|---|---|
| one sentence, falsifiable | URLs + one-line summary | high / med / low | what was found against it, or "none found after adversarial pass" | direct citation / triangulation / deduction / elimination / base-rate / expert consensus / negative evidence |

Tiers are assigned by evidence structure, not by gut feel: **high** requires 2+ independent sources (or one primary source plus a survived adversarial pass) and no unresolved counter-evidence; **medium** requires at least one credible source plus a plausible inference chain, with counter-evidence noted but not decisive; **low** means a single source, a thin inference chain, or unresolved counter-evidence that couldn't be run down further. Full field spec, tier criteria, and CSV/markdown templates: `references/confidence-ledger-spec.md`.

## Inference types

- **Direct citation** — a source states the claim outright. Weakest form of "inference" — really just aggregation. Fine for a starting fact, not enough alone for a load-bearing derived conclusion.
- **Triangulation** — 3+ independent sources each state a different fact; combined, they imply the answer none of them states.
- **Deduction** — if A is true and B is true, C follows necessarily.
- **Elimination** — enumerate plausible alternatives, rule out all but one with evidence.
- **Base-rate reasoning** — combine a prior (how often does this class of thing happen) with case-specific evidence to get a probability, not a binary.
- **Expert consensus** — weighted by both expertise and independence; five people quoting the same original analyst is not five data points.
- **Negative evidence** — the absence of an expected signal is itself evidence (a company silent on a metric it would trumpet if good is informative).

Full catalog with worked examples: `references/inference-patterns.md`.

## Adversarial verification protocol

For each key claim, before it enters the confidence ledger as anything above "low," run one search specifically engineered to surface disconfirming evidence — not a neutral rephrase of the confirming query. If the query returns a real contradiction, the claim's tier drops and the counter-evidence is recorded, not argued away. Defending a claim against its own falsification test defeats the purpose of running the test.

Full protocol, falsifiability query patterns, and what to do on a genuine contradiction: `references/adversarial-verification.md`.

## Gap flagging

Two distinct kinds of "I don't know," and they are not interchangeable:

- **Unknown - public.** No public source will answer this (private financials, internal decisions, unpublished data). State it plainly. Do not fill it with an LLM-memory guess dressed as an estimate.
- **Unknown - could probe with X.** Answerable in principle, just not yet answered — name the specific next source, document, filing, or subagent query that would close it.

A gap-analysis pass that produces zero "unknown" entries is a warning sign, not a clean bill of health — it usually means the search for disconfirming or missing evidence stopped too early.

## Output format

1. **Executive answer** — the conclusion, in one paragraph, with its overall confidence tier.
2. **Reasoning trace** — the inference chain: hypothesis, key evidence, how facts were connected, what the adversarial pass found, how that changed (or didn't change) the conclusion.
3. **Confidence ledger** — the full table.
4. **Open gaps** — unknown-public vs. unknown-probeable, explicitly labeled.

Save substantial output to a workspace file. The reasoning trace ships with the answer — it is not optional detail cut for brevity.

## Depth vs. rigor — when to stop looping

More loops are not automatically better. Stop the iterative depth loop when either condition holds:

- A full additional iteration changed no confidence tier and surfaced no new counter-evidence — the answer has converged.
- The remaining open question is unknown-from-public-sources — no amount of additional searching will close it, so further looping burns budget without changing the answer.

Continuing to loop past convergence is its own anti-pattern: it manufactures the appearance of rigor without adding information.

## Tooling on Perplexity Computer

This skill maps directly onto Computer's native tools — no external research stack required:

- **`search_web`** — parallel, keyword-style queries for fan-out (step 2). Run confirming and falsifying queries as separate calls; don't cram both intents into one query.
- **`search_vertical(vertical="academic")`** — primary research literature for technical or scientific hypotheses; prefer this over general web search when the claim is empirical and likely to have been studied.
- **`search_vertical(vertical="people")`** — background on founders, executives, or named experts feeding an expert-consensus claim.
- **`fetch_url` with a targeted `prompt`** — fact extraction (step 3); ask for the specific figure or statement, not a general summary, to keep extracted facts atomic and attributable.
- **`run_subagent` (research-type)** — delegate a self-contained sub-hypothesis so the parent thread stays focused on cross-source inference rather than raw fetching. Give the subagent the falsifiable claim, not just a topic.
- **`memory_search`** — check for prior findings on this entity or claim before re-running fan-out from zero; prior sessions may already carry ledger rows worth reusing (with a fresh `last_verified` check).

## Anti-patterns

- **Confirmation bias.** Searching only for evidence that supports the hypothesis. Step 5 exists specifically to prevent this — skipping it reintroduces it.
- **Single-source claims.** One source is a lead, not a fact, especially for a claim that will drive a decision.
- **LLM-memory-as-source.** A number or date recalled from training data, not fetched this session, does not enter the ledger as evidence.
- **False certainty.** Presenting a "med" or "low" confidence claim with the same tone as a "high" one. The tier is part of the claim, not a footnote.
- **Aggregating without inferring.** Reporting what five sources say without ever connecting them into a conclusion none of them stated — that's `maximus-deep-research`'s job, not this skill's.

## Sibling skills

- **`maximus-deep-research`** — the aggregation sibling: fan-out, cross-verify, cite. Use it when the deliverable is a synthesized, cited answer to what sources say, with no derived conclusion required beyond that. This skill consumes the same fan-out discipline but adds the hypothesis/falsification/inference layer on top.
- **`maximus-brain`** — supplies the depth-tier calibration for how many iterative depth loops a given task actually warrants, and the think-before-act framing this skill's Step 1 draws from.
- **`maximus-write-article`** — once a reasoning trace and confidence ledger exist, hand off to it for turning the finding into a published piece. Don't re-research inside the writing skill.
- **Built-in `research-assistant`** — for shallow lookups or tasks that don't need hypothesis framing, falsification, or a confidence ledger.

## Output

A reasoning-trace document with executive answer, inference chain, confidence ledger, and labeled open gaps, saved to a workspace file. Every claim above "low" confidence has survived an adversarial pass and traces to a URL fetched this session.
