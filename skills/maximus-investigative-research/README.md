# maximus-investigative-research

**Research the way a working journalist or intelligence analyst does it — not the way a search engine does it.**

Where `maximus-deep-research` synthesizes across many sources and `maximus-deep-research-pro` tests a hypothesis with adversarial verification, this skill produces a **story with a spine**: leads pursued, sources named, timelines reconstructed, contradictions surfaced.

The mental model is a reporter with a notebook, not a search engine with a summarizer.

## When to reach for it

Load this skill when the request has investigative shape:
- "Investigate X" / "Dig into what happened with Y"
- "Research this like a reporter would"
- "Trace this back" / "Connect the dots"
- "Who is really behind X?" / "What's the story here?"
- Journalist story development
- Intelligence-analyst entity or event reconstruction
- Fact-checking a viral claim
- Reconstructing a timeline from scattered public records

## When NOT to reach for it

- Topic summary → `maximus-deep-research`
- Hypothesis testing → `maximus-deep-research-pro`
- Systematic academic review → `maximus-literature-review`
- Finding a person → `maximus-people-finder`
- Structured counterparty export → `maximus-counterparty-discovery`
- Single-question lookup → just search

## The 6-phase loop

1. **Lead intake** — primary question, stakes, scope, starting sources
2. **Source mapping** — primary / secondary / adversarial tiers
3. **Timeline construction** — dated events with source per entry
4. **Contradiction hunt** — actively seek what conflicts with the emerging picture
5. **Corroboration pass** — every load-bearing claim tagged single- or multi-sourced
6. **Report with confidence tags** — narrative + timeline + gaps + source ledger

## What you get

- A narrative report with a defined spine and named sources
- A timeline with per-event confidence
- Explicit list of contradictions (unresolved, not smoothed away)
- Explicit list of what could not be established
- Source ledger by tier

## What you do not get

- Smoothed-over disagreement between sources — contradictions stay in
- Anonymous claims presented as facts — they get flagged or cut
- Wikipedia citations — Wikipedia is a navigation tool, not a source
- Paywall bypass or scraping — public sources only
- Claims without a URL that was actually re-fetched during the investigation

## Files in this bundle

- `SKILL.md` — spec and workflow (loaded by the agent)
- `README.md` — this file
- `HOWTO.md` — 6 recipes for common investigative patterns
- `examples/entity-investigation.md` — worked trace on a private-company investigation
- `examples/event-reconstruction.md` — worked trace on reconstructing an incident from public records
- `references/source-tiers.md` — primary / secondary / adversarial source classification with 2026 outlet notes
- `references/contradiction-patterns.md` — common contradiction shapes and how to handle each
- `references/ethics-and-limits.md` — what this skill will not do (paywalls, private data, illegal collection)

## Integration

- **Downstream:** always run `maximus-chain-of-verification` on the final report before external delivery. Investigative reports get quoted back; every claim needs to survive CoVe.
- **Upstream:** `maximus-brain` should route requests with investigative shape here (not to the aggregation skill).
- **Sibling:** `maximus-deep-research-pro` for hypothesis-first analysis, `maximus-deep-research` for aggregation.

## Freshness

Investigative reports are time-bound. Every source citation carries a fetched date. Do not re-publish an old investigation without re-verifying primary sources.

Last reviewed: **2026-07-31**.
