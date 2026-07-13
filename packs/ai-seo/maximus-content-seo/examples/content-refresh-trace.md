# Worked example — refreshing a 2-year-old ranking post losing traffic

## Setup

Page: `/blog/best-project-management-software` — published 24 months ago, currently ranks position 7 for "best project management software," and has lost 34% of organic traffic over the last 5 months per the analytics export. Position 7 is squarely in the refresh zone from `HOWTO.md` recipe (c) — movable, not stuck at page 4, and showing a real decline, not a fluke.

## Step 1 — confirm it's a refresh candidate, not a pruning candidate

Traffic is down but not gone; the page still ranks on page 1. This is a refresh candidate: real existing value, decaying. A page with near-zero traffic and no ranking history would instead go to the pruning workflow (recipe d).

## Step 2 — diagnose the cause

Pulling the page and the current top 3 competitors for the query surfaces three problems:

1. **Outdated facts.** The post lists pricing tiers for five tools; three of the five have since changed their pricing structure. The post still shows the old numbers.
2. **Missing coverage.** All three current top-3 competitors now include a comparison table and an "AI features" section. This post has neither — it predates the current wave of AI features in the category, and reads as dated because of the omission.
3. **Thin E-E-A-T.** The post has no byline (published under a generic "Team" account), no first-hand testing claims, and no citations for its "most popular" and "best for teams" claims — they read as the author's unsupported opinion.

## Step 3 — before/after diffs

### Title tag

- **Before:** `Best Project Management Software 2024`
- **After:** `Best Project Management Software in 2026: 9 Tools Tested`
- Diff: year updated (freshness signal), added "Tools Tested" to signal first-hand evaluation (E-E-A-T experience marker), stayed under 60 characters.

### Meta description

- **Before:** `Looking for the best project management software? We break down the top options for teams of all sizes.`
- **After:** `We tested 9 project management tools for 3 weeks each. Compare pricing, AI features, and team-size fit — updated for 2026.`
- Diff: added the specific test methodology (139 characters, within the 140-155 target once trimmed), replaced vague "top options" with concrete comparison axes.

### Pricing section

- **Before:** `Tool B costs $9/user/month on the Standard plan.`
- **After:** `Tool B costs $12/user/month on the Standard plan (checked June 2026; pricing pages change — verify before purchase).`
- Diff: corrected the number, added a checked-date marker and a hedge that signals active maintenance rather than a stale, unverified claim.

### New section added

- **Before:** no AI-features section existed.
- **After:** added an "AI Features Compared" H2 with a comparison table across all 9 tools, matching the structural pattern competitors were already using. Table format chosen specifically because structured rows/columns are what current top-ranking pages and AI Overview extraction both favor for this kind of comparison.

### E-E-A-T

- **Before:** byline "Team," no citations, no testing claim.
- **After:** byline changed to a named product reviewer with a one-line credential ("has managed PM rollouts for three 50+ person teams"), added a methodology note ("each tool used for real sprint planning across 3 weeks before scoring"), and cited the vendor pricing page directly for every price quoted.

### Internal links

- **Before:** 2 outbound internal links, both to unrelated posts.
- **After:** added a link up to the category hub (`/blog/project-management`) and two contextual links to sibling spoke posts ("How to Choose a PM Tool for Remote Teams" and "PM Software Pricing Guide"), following the hub-spoke model in `SKILL.md`.

## Step 4 — what was deliberately not changed

- **URL** — left untouched (`/blog/best-project-management-software`) to preserve existing backlinks and ranking history. Changing it would have required a 301 and risked a temporary ranking dip for no benefit.
- **Overall structure** — the core "top 5 picks" format stayed, since it was still winning; only the missing sections and outdated facts were addressed, per the "what to preserve" guidance in `SKILL.md`.

## Step 5 — ship and monitor

Updated the visible "Last updated: July 2026" marker at the top of the post. Plan: check Search Console position and click data at week 4 and week 8 post-refresh to confirm the decline reversed before considering the page fully resolved.
