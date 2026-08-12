# Contradiction patterns — how to spot them, how to report them

The Contradiction Hunt (Phase 4) is what separates this skill from aggregation research. This reference maps the most common contradiction shapes in investigative work.

## Pattern 1 — Timeline conflict

**Shape:** Two sources give different dates for the same event.

**How to spot:** Any date in the timeline table (Phase 3) that appears with conflicting values across sources.

**How to report:** Both entries stay in the timeline with a "conflict" flag and the sources cited. Do not silently pick one. In the narrative, note the conflict and — if possible — indicate which source is more likely correct (based on which is closer to primary).

**Common causes:**
- One source dates the announcement, the other dates the effective date
- Press-release date vs filing date vs public knowledge date
- Time zones (a US press release at 11pm PT vs an EU outlet reporting the next day)

## Pattern 2 — Number conflict

**Shape:** Two sources give different figures for the same metric.

**How to spot:** Any load-bearing number in the developing narrative that appears with different values in different sources.

**How to report:** Show both figures, cite both sources, name the delta. If a primary source (SEC filing, audited report) exists, treat it as authoritative and note the secondary source is wrong or stale. If both are secondary, flag as unresolved.

**Common causes:**
- Old figure vs updated figure (source didn't refresh)
- Different fiscal-year cutoffs
- Different definitions (revenue vs bookings; MAU vs registered users)
- Rounding or unit differences

## Pattern 3 — Entity self-contradiction over time

**Shape:** The entity itself said different things at different points.

**How to spot:** Compare the entity's own statements from t+0, t+1 month, t+1 year. Read old press releases and old S-1s alongside new ones.

**How to report:** Quote both statements with dates. Frame as a change in the entity's position, not necessarily as bad faith — but do not smooth it away.

**Common causes:**
- Business model pivots
- Legal exposure motivating a walk-back
- New leadership changing the narrative
- Genuine correction

## Pattern 4 — Official statement vs public record

**Shape:** The entity's public statement contradicts what court records, regulatory filings, or contemporaneous reporting show.

**How to spot:** For any claim the entity has publicly made, check the corresponding filings or records. Do they match?

**How to report:** Present the statement, present the record, name the delta. This is often the strongest story in an investigation.

**Common causes:**
- Public statement made before a filing came out
- Statement made in a jurisdiction with different disclosure requirements
- Intentional shading

## Pattern 5 — Anonymous claim vs named-source contradiction

**Shape:** An anonymous source claims X; a named source claims not-X.

**How to spot:** Any anonymous-source claim in a secondary source. Check whether any named source has spoken to the same fact.

**How to report:** Default to the named source. Flag the anonymous claim as "unverified" or exclude if there is no corroboration.

## Pattern 6 — Source-chain contradiction (citation drift)

**Shape:** Source A cites Source B for a claim. Source B does not actually make that claim, or makes a materially different one.

**How to spot:** Every citation gets re-fetched (Recipe 4 — citation chain walk).

**How to report:** Cite the actual origin, not the intermediate misattribution. Note the drift if it is material to the story.

**Common causes:**
- Paraphrase that changed meaning
- "Up to X" reported as "X"
- Preprint reported as peer-reviewed
- Correlation reported as causation

## Pattern 7 — Adversarial source contradicts primary

**Shape:** A competitor filing, court complaint, or critical outlet claims something that contradicts the entity's official position.

**How to spot:** Explicit search in Phase 2 for adversarial sources.

**How to report:** Both positions get airtime. Do not treat the entity's version as the truth by default; the adversarial source may be motivated but often has evidence. Follow the evidence, not the source's alignment.

## What "surfaces contradictions" actually looks like in the report

The final report has a section called **"Contradictions"** that lists every unresolved conflict, in the format:

```
### Contradiction 1: [one-line summary]

- Source A (primary/secondary/adversarial): [claim] — [URL]
- Source B (primary/secondary/adversarial): [conflicting claim] — [URL]
- Delta: [what specifically differs]
- Our reading: [if any evidence lets us weight one over the other, say so; otherwise "unresolved"]
```

**Do not:**
- Average conflicting numbers ("sources report between X and Y")
- Silently pick one
- Move the contradiction into a footnote or annex to hide it
- Frame contradictions as a "healthy debate" when the delta is factual

**Do:**
- Surface the conflict at the level of a top-level section
- Attach both sources with their tiers
- Say explicitly when it is unresolved
