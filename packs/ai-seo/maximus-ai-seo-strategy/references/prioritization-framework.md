# Prioritization framework: volume x intent x difficulty x AI-citation potential

Raw volume misprioritizes for AI answer surfaces. A backlog item is worth building when the product of four scores is high — not when any single score is high. A perfect intent match on an unwinnable, saturated query is still a bad bet; a modest-volume conversational query with a wide-open citation gap can outperform it.

## The four axes

Score every candidate 1-5 on each axis.

### 1. Volume (estimated demand)

Since this pack has no direct keyword-volume API, estimate tier from `search_web` signal: how many related discussions, forum threads, and AI Overview appearances the query and its close variants generate.

| Score | Meaning |
|---|---|
| 5 | Head term, clearly high-demand category query |
| 4 | Strong sub-term, consistent search/discussion signal |
| 3 | Moderate, niche-specific but recurring demand |
| 2 | Low, long-tail, occasional demand |
| 1 | Speculative — no clear evidence of search demand yet |

### 2. Intent value (commercial/strategic weight)

How much does satisfying this query advance the actual business or authority goal — not just traffic.

| Score | Meaning |
|---|---|
| 5 | Transactional/decision-stage, directly commercial |
| 4 | Strong buying-consideration or high-trust informational (comparison, buying guide) |
| 3 | General informational, supports authority but not directly commercial |
| 2 | Navigational or low-relevance informational |
| 1 | Off-strategy — satisfies curiosity but doesn't advance any goal |

### 3. Difficulty (inverted — lower difficulty scores higher)

How hard is it to actually win this query, whether "win" means ranking or being cited.

| Score | Meaning |
|---|---|
| 5 | Wide open — no strong competitor, no entrenched AI-cited source |
| 4 | Light competition, beatable with a solid page |
| 3 | Moderate — 1-2 decent competitors, winnable with a genuinely better page |
| 2 | Heavy — several strong, well-linked competitors |
| 1 | Dominated — entrenched brand(s) or a single canonical source AI answers consistently cite |

### 4. AI-citation potential

Is this a query where an AI Overview / chat-assistant answer is likely to appear, and is the current cited source (if any) weak or absent.

| Score | Meaning |
|---|---|
| 5 | AI answer appears for this query and the current cited source is weak, outdated, or absent |
| 4 | AI answer format is likely (checklist, comparison, definition) and coverage is thin |
| 3 | AI answer sometimes appears; competitive landscape for citation is unclear |
| 2 | AI answer format unlikely for this query type (e.g., pure navigational) |
| 1 | No realistic path to AI citation for this query |

## Scoring formula

```
priority_score = volume x intent_value x difficulty x ai_citation_potential
```

Multiplicative, not additive — a 1 on any axis meaningfully suppresses the total, which is intentional: a query nobody searches for, or one you cannot realistically win, or one with no path to being seen, should not out-rank a solid all-around candidate just because it's strong on one axis.

Maximum possible score: 625 (5x5x5x5). Treat scores as relative ranking within a single backlog, not as an absolute standard across projects.

## Template

| Query / subtopic | Volume (1-5) | Intent value (1-5) | Difficulty (1-5) | AI-citation potential (1-5) | Priority score | Cluster role | Notes |
|---|---|---|---|---|---|---|---|
| how to choose a vendor management tool | 4 | 4 | 4 | 4 | 256 | Hub | Buying-guide framing, low competition at mid-market segment |
| what breaks past 50 vendors in spreadsheets | 2 | 4 | 5 | 5 | 200 | Spoke | Conversational, no direct competitor answer exists |
| vendor management software | 5 | 5 | 1 | 2 | 50 | Reference only | Head term, dominated by 3 enterprise brands — not a realistic near-term target |

(Rows are illustrative, drawn from `examples/keyword-cluster-trace.md`.)

## Tie-breakers

When two candidates land within roughly 10% of each other's score, break the tie with, in order:

1. **Internal linking leverage** — does building this page unblock or strengthen other planned pages (e.g., a foundational/definitional page that several spokes need to link to)? Prefer it.
2. **Freshness of competitor content** — if the current best competitor page is more than 12-18 months old or references outdated data, prefer the candidate that displaces it; stale pages are the easiest wins.
3. **Business-priority override** — if one candidate maps directly to an active product launch, sales priority, or seasonal window, it can jump the queue even at a lower score — but log the override explicitly so the next review cycle knows it was a deliberate exception, not a scoring error.
4. **Effort asymmetry** — if two candidates score equally but one is a straightforward single-page build and the other requires new research, data, or SME interviews, prefer the lower-effort item to keep cadence.

## Re-scoring cadence

Difficulty and AI-citation potential are the most volatile axes — competitors ship content and AI answer formats change month to month. Volume and intent value are comparatively stable. Re-score at minimum on the monthly review cadence (`HOWTO.md` Recipe F); re-score immediately if a competitor ships new content on a top-10 backlog item.
