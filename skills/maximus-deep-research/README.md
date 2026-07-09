# Maximus — Deep Research

## What

A skill for running production-grade multi-source research on Perplexity Computer. It covers two related jobs under one workflow:

- **Synthesis** — answer a complex question by reconciling many sources into one cited, coherent answer.
- **Competitive / Market Intelligence** — map a set of vendors, competitors, or a market category into a decision-grade brief (pricing, features, positioning, moat, weaknesses).

Both modes run the same core discipline: frame the question, fan out across parallel searches before narrowing, deduplicate repeated claims, cross-verify anything the answer leans on, synthesize in the user's terms, and cite every material claim to the source it came from.

## When to use

Load this skill when the task is:

- Triggered by phrases like "deep research", "research this thoroughly", "competitive intel", "market landscape", "due diligence lite", "compare vendors", "synthesize sources", or "research report".
- A question that a single search can't honestly answer — it requires reconciling multiple, possibly conflicting sources.
- A vendor or market comparison that needs to hold up to scrutiny (a decision-maker will act on it).

Do **not** load it for single-fact lookups, one-question answers, or writing tasks that only need light background — those are faster served by a plain search or the built-in `research-assistant` skill.

## Example

> "Do a competitive teardown of AI code review tools — Greptile, CodeRabbit, Qodo, Bito, Codacy, and Graphite Reviewer. I need pricing, positioning, and where each one is weak."

This is Mode 2 (Competitive Intel). The skill would map the six vendors, pull pricing/feature data (delegating the raw pull to `wide-search` if it's a large field set), cross-verify claims that appear on marketing pages against independent reviews or docs, and produce a comparison table plus a short recommendation — every cell traceable to a URL.

> "What's actually driving the recent wave of stablecoin regulation in the US and EU, and how do the two approaches differ?"

This is Mode 1 (Synthesis). The skill would fan out across primary sources (regulatory text, agency statements), secondary sources (major financial press), fact-check the two or three claims the comparison depends on, and write a synthesized, cited answer.

## How it works

See `SKILL.md` for the full workflow (Frame → Fan-out → Dedup → Cross-verify → Synthesize → Cite), the source-quality tiering system, and the anti-patterns this skill is designed to prevent.

See `HOWTO.md` for six concrete recipes covering synthesis, competitive teardown, market sizing, technical deep dives, large data-table research (via `wide-search`), and handoff to `maximus-write-article`.

See `examples/` for two fully worked traces — one Synthesis, one Competitive Intel — showing the fan-out plan, source list, dedup, and final cited output.

See `references/source-quality-tiers.md` for the primary/secondary/tertiary tiering rules and red flags.

## Related skills

- **`maximus-brain`** — the cognitive loop that decides when a task needs "Deep" tier work and loads this skill for it.
- Built-in **`research-assistant`** — for polished single-report research deliverables that don't need this skill's explicit two-mode/vendor-comparison structure.
- Built-in **`wide-search`** — the delegate for any many-entities × many-fields data pull; this skill's Competitive Intel mode leans on it directly.
- **`maximus-write-article`** — the handoff target once research is synthesized and cited and the next step is publishing it.
