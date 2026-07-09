---
name: maximus-deep-research
description: "Run production-grade multi-source deep research and competitive/market intelligence with cite-or-cut discipline. Use when the user says 'deep research', 'research this thoroughly', 'competitive intel', 'market landscape', 'due diligence lite', 'compare vendors', 'synthesize sources', or 'research report'. Covers two modes: Synthesis (fan out across many sources to answer a complex question) and Competitive Intel (map a market or vendor set into a decision-grade brief). Enforces fan-out-before-narrowing, cross-verification of any load-bearing number, and full inline citation."
metadata:
  pillar: research
  source: maximus
---

# Maximus — Deep Research

Most research failures aren't a lack of information — they're a single confident source treated as ground truth. This skill exists to slow that down: fan out wide before narrowing, cross-verify anything the answer leans on, and cite every claim to the page it came from. If a claim can't be traced to a fetched source, it doesn't ship.

This is heavier than a single search and lighter than a full consulting engagement. Use it when the question needs more than three sources to answer honestly, but doesn't need a dedicated team of analysts.

## When to use

- The user says "deep research", "research this thoroughly", "competitive intel", "market landscape", "due diligence lite", "compare vendors", "synthesize sources", or "research report".
- A question that a single search result cannot honestly answer — it requires reconciling multiple, possibly conflicting, sources.
- Mapping a market or vendor set (competitors, pricing, positioning) into something a decision-maker can act on.
- Any claim that will be quoted, published, or used to justify a decision, where being wrong is costly.

## When NOT to use

- Single lookups or one-question factual answers ("what's Apple's stock price", "when was X founded") — just search or use `finance/finance-markets`.
- Writing tasks that only need light background research, not verified synthesis — go straight to drafting.
- Broad multi-source synthesis with no comparison/decision structure and no need for this skill's fan-out discipline — the built-in `research-assistant` skill may be a lighter fit.
- Large structured data pulls across many entities into a table — that's `wide-search`'s job; this skill delegates to it (see Sibling skills).

## Purpose

Deep research is the discipline of turning "let me look that up" into "here is what's actually true, and here's how I know." Two failure modes dominate bad research: narrowing too early (one source, one framing, done) and citing memory instead of evidence (the model states a number it "knows" instead of one it fetched). This skill installs the counter-pattern: frame the question, fan out before you narrow, cross-verify anything load-bearing, and cite or cut.

## The Two Modes

Pick a mode at the start. They share the core workflow but diverge in shape.

### Mode 1 — Synthesis
Answer a complex question by reconciling many sources into one coherent, cited answer. Output is prose (or a structured brief) with inline citations, not a table of vendors.

Use for: "what's the state of the art in X", "how does Y actually work", "what happened with Z and why", technical/scientific deep dives, policy or historical questions.

Workflow shape: broad fan-out → aggressive dedup (many sources repeat the same three facts) → cross-verify the two or three claims the answer depends on → synthesize into a narrative with citations attached to each claim.

### Mode 2 — Competitive / Market Intelligence
Map a defined set of entities (vendors, competitors, products) across a fixed set of dimensions (pricing, features, positioning, moat, weaknesses) to produce a decision-grade brief.

Use for: "compare vendors", "competitive intel", "market landscape", "due diligence lite" on a company or category.

Workflow shape: define the entity set and dimensions first → per-entity fan-out (primary sources: pricing pages, docs, filings) → normalize into a comparison structure → synthesize a recommendation or landscape summary, not just a data dump.

Both modes end the same way: every material claim has a citation, and anything that couldn't be verified is marked as such rather than smoothed over.

## Core Workflow

1. **Frame.** Restate the question in one sentence. Name what "done" looks like — a paragraph, a table, a recommendation. Identify the 2-4 sub-questions or entities that structure the work. Don't skip this: unframed research produces unfocused fan-out.
2. **Fan-out.** Issue parallel `search_web` queries — 3-5 short, keyword-style queries per sub-question, not one long compound query (see `search_strategy` conventions: separate queries per entity/angle, not "A vs B" crammed together). For academic/technical questions, run `search_vertical` with `vertical="academic"` alongside web search. For people/org-context questions, use `vertical="people"`. If the brief has many entities × many fields (a table), stop and delegate to `wide-search` instead of fanning out by hand.
3. **Collect and dedup.** Fetch the most promising URLs with `fetch_url`, using a targeted `prompt` to extract just the relevant fact or figure. Expect redundancy — many hits repeat the same underlying claim. Collapse duplicates but keep track of *how many independent sources* say the same thing; that count is evidence of reliability, not noise to discard.
4. **Cross-verify.** For every number or claim the final answer leans on, require at least two independent sources, with at least one from a higher tier (see source-quality tiering below). If sources conflict, say so — don't average or silently pick one.
5. **Delegate depth when the sub-question is self-contained.** If a sub-question can be fully answered on its own (e.g., "what is vendor X's current pricing"), consider a `research`-type subagent via `run_subagent` rather than doing it inline — this keeps the parent context focused on synthesis instead of raw fetching. Give the subagent a complete, self-contained brief (it has no access to your conversation history).
6. **Synthesize.** Write the answer in the user's terms. Lead with the finding, not the process. Structure Mode 1 as narrative-with-citations; structure Mode 2 as comparison-plus-recommendation.
7. **Cite.** Every sentence carrying a fact, figure, or claim gets an inline markdown link to the source it came from, named naturally (publication or organization name, not "source" or a raw URL). No claim survives to the final answer without a citation or an explicit "unverified" flag.

## Source-quality tiering

Not all sources carry equal weight. Tier the evidence, don't just count hits.

- **Primary** — SEC/regulatory filings, government statistics, company documentation, pricing pages, academic papers, direct interviews/transcripts. Highest weight; prefer these for any number that matters.
- **Secondary** — major press with named authors and editorial standards, analyst reports (Gartner, Forrester, etc.), reputable industry publications.
- **Tertiary** — aggregators, SEO content farms, unattributed blogs, forums, social media threads. Useful for leads and framing, never as the sole support for a load-bearing claim.

Full detail, red flags, and acceptable-use rules: `references/source-quality-tiers.md`.

## Anti-patterns

- **Single-source claims.** One article, one blog post, one forum answer is a lead, not a fact. Cross-verify before it goes in the answer.
- **LLM-memory-as-source.** Never state a number, date, price, or fact from training data as if it were current. If it wasn't fetched this session, it doesn't go in the answer — or it goes in with an explicit "unverified, based on general knowledge" flag.
- **Unverified numbers presented as precise.** If two sources disagree by 20%, report the range and the disagreement — don't quietly pick the rounder number.
- **Narrowing before fanning out.** Locking onto the first search result's framing and building the rest of the research to confirm it.
- **Aggregator laundering.** Citing a listicle that itself cites no one. Trace back to the primary source it's paraphrasing.

## Sibling skills

- **`maximus-brain`** — Deep research is a "Deep" or "Extreme" tier task under brain's depth framework. If brain is loaded, let it pick the tier; this skill is what brain loads in Pass 3 for research work.
- **Built-in `research-assistant`** — for research that doesn't need the two-mode structure here (single coherent report, no vendor comparison), or when the deliverable needs institutional-grade polish with inline visualizations. This skill is the fan-out/verification discipline layer; `research-assistant` is the heavier deliverable-quality layer. They compose.
- **Built-in `wide-search`** — the tool of choice whenever the brief is many-entities × many-fields (a table/screener). Mode 2 (Competitive Intel) explicitly hands off to `wide-search` for the raw per-vendor data pull, then this skill's synthesis step turns that table into a decision-grade brief.
- **`maximus-write-article`** — once research is synthesized and cited, if the next step is turning it into a published piece, hand off to `maximus-write-article` rather than re-researching inside the writing skill.

## Output

A cited answer or brief (Mode 1: narrative; Mode 2: comparison table + recommendation), saved to a workspace file when substantial. Every material claim traces to a URL fetched this session. Gaps and disagreements between sources are stated, not papered over.
