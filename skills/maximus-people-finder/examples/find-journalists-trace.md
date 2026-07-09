# Worked trace — Find journalists covering AI infrastructure

**Brief as given:** "Find journalists covering AI infrastructure I should pitch about our new inference-optimization product."

---

## Step 1 — Intake

- **Population:** journalists, analysts, and newsletter writers currently covering AI infrastructure (compute, inference, data centers, GPU supply, ML ops) — not general AI/tech journalists who mention the topic in passing.
- **Deliverable shape:** ranked list with a **pitch angle per journalist**, since the end use is outreach, not just a name list.
- **Verification bar:** must have a byline or newsletter piece on the beat within roughly the last 3-6 months (recency matters more here than for most people-finding briefs — a reporter who covered infra in 2023 may have moved on).
- **Assumption stated:** "AI infrastructure" is read to include inference/serving, GPU/compute supply, data center buildout, and ML ops tooling — not general "AI" coverage.

## Step 2 — Query Expansion

Beat language varies a lot by outlet. Expanded terms:

- "AI infrastructure reporter"
- "GPU supply chain journalist"
- "inference cost coverage"
- "ML ops newsletter"
- "data center AI buildout reporter"
- Outlet-first search: identify which outlets have a dedicated AI/infra beat (The Information, Semafor, TechCrunch, The Register, SemiAnalysis-style independents), then find the named reporter/writer per outlet.

## Step 3 — Multi-Channel Search (parallel)

- `search_web` — recent bylines matching the expanded query set, with a `recency_filter` set to `month` to bias toward current coverage.
- Newsletter/Substack search — independent analysts publishing on inference economics and infra (a distinct population from staff reporters, often more targetable for a product pitch).
- X search — reporter bios ("covers AI infra for X") and recent threads on the topic, which double as a read on their current angle/interests.
- Outlet staff pages (`fetch_url`) — to confirm beat assignment directly from the source, which is more reliable than inferring from a single article.

## Step 4 — Enrichment

Per candidate:

- Outlet and current beat (confirmed via staff page or masthead where possible, not just inferred from one article).
- 1-2 most recent relevant pieces (title, date, link) — this is also the evidence for the recency check in Step 7.
- Angle/slant signal — do they write skeptically about infra hype, or do they cover product launches straight? This shapes the pitch angle.
- Contact path — public byline contact link, outlet's tips page, or public X handle. No non-public contact info.

## Step 5 — Deduplication

Watch for: the same writer appearing under a staff byline at one outlet and also running a personal newsletter — treat as one person with two channels, and note both in the outreach-hook field (a pitch might target the newsletter first if it's less gatekept).

## Step 6 — Ranking

Score on:

1. Recency and specificity of coverage to inference/infra specifically (not general AI).
2. Outlet reach and relevance to the product's audience.
3. Demonstrated angle fit (has the writer shown interest in cost/performance stories, which this pitch is).
4. Responsiveness signal if discoverable (e.g. publicly stated they take reader tips).

## Step 7 — Verification / Delivery

- Re-confirm each writer's most recent piece is within the stated recency window — a reporter who covered the beat heavily in 2024 but has since moved to a different desk should be flagged, not ranked as if still active on it.
- Re-confirm the outlet/newsletter is still active (some independent newsletters go dormant).
- Distinguish "verified active on beat" from "covered it once, unclear if still active."

**Delivery — final table (illustrative structure):**

| rank | name | outlet | recent_piece | angle | confidence | source_urls | pitch_angle |
|---|---|---|---|---|---|---|---|
| 1 | [Reporter Name] | [Outlet] | "[Recent headline]" (date) | Cost/performance skeptic | verified | [staff page], [recent article] | Lead with inference-cost benchmark data, not feature list |
| 2 | ... | ... | ... | ... | ... | ... | ... |

Cover summary: channels searched, number of query-expansion passes, and an explicit note on any writer excluded for recency (moved beats, dormant newsletter) so the user understands why they're not on the list rather than assuming they were missed.
