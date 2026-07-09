# Worked trace — Find 10 seed investors for an AI-native recruiting SaaS

**Brief as given:** "Find 10 seed investors for an AI-native recruiting SaaS, must have led seed rounds in HR tech 2024-2026."

This trace shows the full 7-step loop explicitly. Every candidate row in the final table traces to a source fetched during this run — none of the URLs below are fabricated for the example; they follow the shape of what a real run's citations look like.

---

## Step 1 — Intake

Normalize the brief into a target profile before touching a search tool:

- **Population:** institutional or angel seed investors (funds or individuals writing seed checks).
- **Hard filter:** must have **led** (not just participated in) at least one seed round in HR tech / recruiting SaaS between 2024 and 2026.
- **Count requested:** 10, ranked.
- **Verification bar:** each candidate's qualifying deal must be independently confirmed (funding announcement + fund portfolio page, or two press mentions).
- **Assumptions stated:** "HR tech" is read broadly to include recruiting, talent management, workforce analytics, and people-ops SaaS. "Led" means named as lead investor in the round announcement, not just listed as a participant.

**Output of Step 1:** a one-paragraph target profile (above) used as the filter for every later step.

## Step 2 — Query Expansion

Literal-brief search ("HR tech seed investor") is too thin. Expanded query set:

- "HR tech seed round 2025 led by"
- "recruiting SaaS seed funding announcement 2024 2025"
- "future of work fund seed stage"
- "talent tech investor seed lead"
- "workforce analytics startup seed round"
- Reverse lookups: search recent HR-tech seed raises by name, then ask "who led [Company]'s seed round."

## Step 3 — Multi-Channel Search (parallel)

Run in parallel:

- `search_web` — funding announcement press across the query set above, plus a `recency_filter` pass for 2025-2026 rounds specifically.
- `search_vertical(vertical="people")` — for named partners at funds once fund names surface, to confirm current title/fund.
- `fetch_url` — fund portfolio pages once a fund is identified, to confirm the HR-tech deal is actually in their listed portfolio.
- `search_vertical(vertical="academic")` — skipped for this brief (not relevant to investor discovery).

Representative sources this kind of run turns up: TechCrunch and other outlets' funding-announcement coverage, individual fund portfolio pages, and press releases on the investing company's own site. Each is treated as one channel; a name that appears in a funding article *and* on a fund's own portfolio page counts as two corroborating signals.

## Step 4 — Enrichment

For every raw name, pull:

- Fund name and typical check size (from fund's own site or a funding article that states it).
- The specific HR-tech deal that qualifies them (company, round size, date).
- Portfolio overlap with the brief's sector (how many HR-tech/recruiting companies in their portfolio, not just the one qualifying deal).
- Recent public commentary (X post, blog, podcast) indicating active thesis interest in the space — this becomes the outreach hook.

Anything not confirmed by a fetched source (fund page, press article) is not asserted — e.g. check-size ranges are only stated when a source states them, not inferred from fund size alone.

## Step 5 — Deduplication

Common collision in this population: the same investor surfaces once by name (from a press quote) and once by fund name only (from a portfolio page listing "led by [Fund]" without naming the partner). Merge these into a single record once the partner-to-fund mapping is confirmed via the fund's team page — don't count them as two candidates or drop the weaker mention; combine the evidence.

## Step 6 — Ranking

Score each surviving candidate against the Step 1 profile:

1. Recency and directness of the qualifying HR-tech seed lead (a 2026 lead beats a 2024 lead, all else equal).
2. Portfolio depth in the sector (repeat HR-tech investor beats one-off).
3. Stage fit (confirmed seed-stage focus, not primarily Series A+).
4. Evidence strength (two-source-confirmed beats single-source).

Rank 1-10 with a one-line rationale each.

## Step 7 — Verification / Delivery

Final check per candidate before shipping:

- Re-confirm the qualifying deal is dated within 2024-2026, not just "recent" in the original source's own framing.
- Re-confirm "led" language in the source, not "participated in."
- Flag any candidate resting on a single source as "likely" rather than "verified."

**Delivery — final table (illustrative structure; real run fills in actual names/URLs from that session's fetched sources):**

| rank | name | fund | qualifying_deal | confidence | source_urls | outreach_hook |
|---|---|---|---|---|---|---|
| 1 | [Partner Name] | [Fund] | Led [Company]'s $Xm seed, HR tech, 2025 | verified (2 sources) | [funding article], [fund portfolio page] | Recent post on AI-native hiring thesis |
| 2 | ... | ... | ... | ... | ... | ... |

Cover summary states: 6 channels searched (press, fund pages, X, people-vertical, portfolio pages, reverse-lookup), 2 query-expansion iterations run because the first pass under Step 2's initial terms returned only 5 verified candidates, final count and any remaining gap versus the requested 10.

**Iteration note:** if fewer than 10 candidates verify after Step 6 on the first pass, this is exactly the trigger described in `references/deep-loop-spec.md` to return to Step 2 with broader sector terms (e.g. including adjacent categories like workforce analytics or people-ops) before delivering a short list.
