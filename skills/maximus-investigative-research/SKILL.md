---
name: maximus-investigative-research
description: Investigative research the way a working journalist or intelligence analyst does it — not the way a search engine does it. Load when the user says "investigate," "dig into," "find out what happened with," "research this like a reporter would," "who is really behind X," "what's the story with Y," "trace this back," "connect the dots," or wants a report shaped by leads, sources, timelines, and corroboration rather than a topic summary. Runs a 6-phase human-analyst loop — Lead intake → Source mapping (primary/secondary/adversarial) → Timeline construction → Contradiction hunt → Corroboration pass → Report with confidence tags. Distinguishes single-sourced from multi-sourced claims. Names what is not known. Surfaces contradictions instead of averaging them away. Distinct from maximus-deep-research (aggregation) and maximus-deep-research-pro (hypothesis testing) — this skill produces a story with a spine, not a synthesis.
---

# WHEN TO USE

Load this skill when the user wants research shaped like a working investigator would produce it — a story with a spine, leads pursued, sources named, contradictions surfaced, timeline reconstructed. Not a topic summary. Not a market landscape. A narrative with claims tied to specific sources.

Specific triggers:
- "Investigate X"
- "Dig into what happened with Y"
- "Research this like a reporter would"
- "Who is really behind Z?"
- "Trace this back to the source"
- "Connect the dots on [event / entity]"
- "Find the story here"
- "What's the actual sequence of events?"
- "Was that number really from that source?"

Also use for:
- Journalist workflows — story development, source triangulation
- Intelligence analyst workflows — entity investigation, event reconstruction
- Due diligence on a specific person, company, or claim (short of formal legal DD)
- Fact-checking a viral claim or story
- Reconstructing a timeline from scattered public records

# WHEN NOT TO USE

- **General topic summary** ("what is X?") → use `maximus-deep-research`
- **Hypothesis testing / analytical inference** ("is thesis X true?") → use `maximus-deep-research-pro`
- **Systematic academic review** → use `maximus-literature-review`
- **Finding a person from a description** → use `maximus-people-finder`
- **Structured counterparty export** → use `maximus-counterparty-discovery`
- **Single-question lookup** → just search
- **Any task requiring circumvention of paywalls, robots.txt, auth, or private data** → refuse

# CORE PRINCIPLE

**A human investigator does not average sources. They rank them, chase the primary, and surface the contradictions.**

This skill is built around that discipline. Where `maximus-deep-research` synthesizes across many sources, this skill picks a spine — the strongest available primary source — and traces claims back to it. Where the aggregation skill would smooth over disagreement between two sources, this skill records the disagreement in the report as evidence, not noise.

The mental model is a reporter with a notebook, not a search engine with a summarizer.

# THE 6-PHASE LOOP

## Phase 1 — Lead intake

Extract the specific claim, entity, event, or question the user wants investigated. Restate it as:

- **The primary question** (one sentence — what are we trying to establish?)
- **The stakes** (why does this matter — external delivery? Legal? Reputational?)
- **The scope** (time window, geography, entities in bounds)
- **The known starting sources** (any URLs, documents, or leads the user provided)

If any of these are ambiguous, ask the user before spending tokens. Investigation without a defined question wanders.

## Phase 2 — Source mapping

Build the source stack before extracting facts. Three tiers:

**Primary sources** — the entity or event's own outputs.
- SEC filings, court records, court opinions, regulatory filings
- Official press releases and corporate blog posts
- Direct statements attributed to named individuals
- Contracts, patents, permits, licenses
- Original data releases (studies, datasets)

**Secondary sources** — reporting *about* the primary sources.
- Reputable outlets (per your outlet's own standards — Bloomberg, Reuters, WSJ, FT, NYT, WaPo, plus verticals)
- Analyst reports where the analyst is named
- Wikipedia (only as a **navigation** tool to find the primary sources; never as a citation)

**Adversarial sources** — sources with a known angle *against* the entity or claim.
- Competitor filings
- Litigation records
- Investigative reports from outlets known for critical coverage
- Short-seller reports (for financial subjects — treat as motivated but read carefully)
- Whistleblower statements (when documented)

For each source tier, note:
- What we have (URLs, dates fetched)
- What we are missing (gaps)
- Any source we suspect exists but cannot access (paywall, private, non-public)

## Phase 3 — Timeline construction

For any investigation involving events over time, build the timeline **before** writing narrative. Format:

| Date | Event | Source | Confidence |
|---|---|---|---|
| YYYY-MM-DD | [what happened, one sentence] | [URL] | high / medium / low |

Rules:
- Every entry has at least one source.
- Contradictions in the timeline (two sources give different dates for the same event) get **both entries** with a "conflict" flag — do not silently pick one.
- Undated events go in a separate "sequence-known, dates-unknown" block.

## Phase 4 — Contradiction hunt

Actively look for claims that conflict with the emerging picture. For each major claim in the developing narrative, ask:

- **Who benefits from this claim being true?**
- **Who benefits from it being false?**
- **What would the entity's critics or competitors say about this?**
- **Is there a court record or regulatory filing that contradicts this?**
- **Has the entity said something different about this at a different time?**

Every contradiction found gets logged. Do not skip past uncomfortable ones. Contradictions are the whole point.

## Phase 5 — Corroboration pass

For every load-bearing claim in the narrative, ask: *is this single-sourced or multi-sourced?*

- **Multi-sourced (2+ independent sources agreeing):** high confidence. Present as fact.
- **Single-sourced (only one source, uncorroborated):** medium confidence at best. Flag inline: "per [source]" — do not present as general fact.
- **Single-sourced from an adversarial source:** flag as "reportedly, per [source]" — the story is a lead, not a fact.
- **Anonymous-sourced:** requires independent corroboration or gets excluded.

## Phase 6 — Report with confidence tags

Deliver the report in this shape:

```
## The primary question

[one sentence]

## What we established

[multi-sourced, high-confidence claims — the spine of the story]

## What we found but cannot fully corroborate

[single-sourced or partially-supported claims, each flagged]

## Contradictions

[unresolved conflicts between sources — presented as evidence, not smoothed away]

## Timeline

[table from Phase 3]

## What we do not know

[explicit gaps — questions we could not answer, sources we could not access]

## Source ledger

[every source used, tier (primary/secondary/adversarial), date fetched]
```

# HARD RULES

1. **Never fabricate a source.** If a claim cannot be attributed to an actual URL that you re-fetched, cut the claim.
2. **Never present single-sourced claims as facts.** Flag them.
3. **Never bury contradictions.** Contradictions are the point — surface them.
4. **Never rely on Wikipedia as a citation.** Use it to navigate to the primary source; cite the primary.
5. **Never launder a claim through paraphrase.** If the source says "up to $X," do not report "approximately $X" without flagging the softening.
6. **Never anonymize a source that has a name.** If a claim came from a named person or filing, name it.
7. **Never present anonymous-source claims without independent corroboration.**
8. **Never bypass paywalls, auth, robots.txt, or captchas.** Public sources only. If a source is behind a paywall your user has access to, they can provide the content — you do not scrape it.
9. **Never publish a report that has not been through the Contradiction Hunt.** Skipping Phase 4 defeats the skill.
10. **Never treat a first-page search result as the story.** The story is upstream of the search result. Trace back.

# INTEGRATION WITH OTHER MAXIMUS SKILLS

- **Upstream:** `maximus-brain` should trigger this skill when the user's request has investigative shape (lead, entity, event, sequence).
- **Downstream:** always run `maximus-chain-of-verification` on the final report before external delivery. Investigative reports get quoted back; every claim needs to survive CoVe.
- **Sibling:** `maximus-deep-research-pro` for hypothesis-first analysis, `maximus-deep-research` for aggregation. This skill is neither — it is narrative reconstruction.
- **Adjacent:** `maximus-people-finder` for finding a person to interview; `maximus-counterparty-discovery` for structured due-diligence exports.

# OUTPUT DISCIPLINE

- Every claim in the report has a source citation.
- Every citation is a URL that was **actually fetched during this investigation** — not a URL remembered from training.
- Confidence tags (high / medium / low) appear inline where confidence is not high.
- The "What we do not know" section is not optional. If the investigation had gaps, name them.

# FRESHNESS

Investigative research is time-bound. A report is only as fresh as its sources. Every source citation carries a "fetched" date. Never re-publish an old investigative report without re-verifying the primary sources — entities file new documents, court records change, and previously-confirmed facts can be superseded.
