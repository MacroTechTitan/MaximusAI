# HOWTO — maximus-geo-optimization

Six recipes. Each is a runnable checklist, not theory — pair with `SKILL.md` for the underlying reasoning.

## Recipe A — Prompt mining for your category

**Goal:** find the actual prompts buyers type into LLMs, not the keywords they'd type into Google.

1. Pull raw language from sales call transcripts, support tickets, onboarding surveys, and win/loss notes. Look for how buyers phrase problems, not features.
2. Search Reddit, Quora, G2/Capterra Q&A, and "People also ask" boxes in your category for naturally-phrased questions.
3. Draft 15-30 candidate prompts covering: definitional ("what is X"), comparison ("X vs Y"), "best X for Y" shortlist prompts, troubleshooting, and pricing/ROI.
4. Run every candidate prompt manually through Perplexity, ChatGPT search, and Copilot. Log: which brands got cited, which domains were sourced, whether your brand appeared at all.
5. Cluster the prompts by intent and by which content asset would need to exist to answer them well.
6. Prioritize clusters where you have zero presence today and high buyer intent — that's the biggest GEO gap to close first.
7. Save the full trace (prompts, engines, citations observed) — this becomes your baseline for `maximus-llm-visibility-tracking`.

Worked example: `examples/prompt-mining-trace.md`.

## Recipe B — Audit and configure robots.txt for LLM crawlers

**Goal:** make a deliberate per-bot decision instead of a default block or default allow.

1. Fetch the live `robots.txt` and list every user-agent block already present.
2. Cross-reference each LLM-relevant bot against `references/llm-crawler-directory.md` — note whether it's a training crawler or a live-retrieval/on-demand crawler.
3. Decide policy per bot:
   - Live-retrieval bots that can send you citation traffic (e.g. `PerplexityBot`, `ChatGPT-User`, `Claude-Web`) — default to allow unless you have a specific reason to block.
   - Training-only bots — a business decision: allow if you want inclusion in future model training data and don't mind it, block if you don't.
   - Bulk/undifferentiated scraping bots with no clear citation benefit (e.g. `Bytespider`) — default to block unless proven otherwise.
4. Write explicit `User-agent` blocks for each bot you have an opinion on — don't rely on a generic `User-agent: *` to cover AI crawlers, most of them ignore the wildcard block or require explicit handling.
5. Keep the sitemap directive and make sure any pages you want cited are actually included and not blocked elsewhere (noindex tags, X-Robots-Tag headers, or auth walls override robots.txt intent).
6. Validate syntax (one `User-agent` + directives per block, blank line between blocks) and re-crawl-test after deploying.
7. Re-audit quarterly — new crawlers appear regularly.

Worked example: `examples/robots-config-trace.md`. Full bot list: `references/llm-crawler-directory.md`.

## Recipe C — Build a third-party mention plan

**Goal:** engineer the cross-domain co-occurrence that generative engines use as a trust signal.

1. From the prompt-mining clusters (Recipe A), identify which prompts are comparison/listicle-shaped ("best X for Y", "X alternatives").
2. List the 10-20 sites that already rank or get cited for those prompts today — these are your target placements.
3. Segment targets into: guest-post candidates, existing listicles you could pitch inclusion into, forums/Q&A where genuine participation is appropriate, and review platforms (G2, Capterra, TrustRadius) where you can earn organic reviews.
4. For each target, draft a specific, non-generic pitch tied to a real gap in their existing content (e.g. "your comparison is missing category X, here's why we'd be a fit").
5. Track placements landed, and re-run the Recipe A prompts after 4-6 weeks to see whether citation behavior shifted.
6. Never buy undisclosed placements or fabricate mentions — treat this as PR/outreach, not link-buying.

## Recipe D — Writing for comparison-listicle inclusion

**Goal:** make your own content and your outreach pitch both listicle-ready.

1. Identify the exact comparison shape buyers ask for (find via Recipe A): "best X for [use case]," "X vs Y vs Z," "cheapest X with [feature]."
2. Write a self-hosted comparison page structured the way a listicle would be: one clear criterion set, a scannable table, and an honest note on where you're not the best fit — false-balance-free but not one-sided propaganda, LLMs discount obviously biased self-comparisons.
3. Include concrete, checkable facts (pricing tiers, feature availability, integration lists) — these are the details generative engines most often lift verbatim.
4. Add schema.org `Product` and/or `FAQPage` markup so the comparison table and Q&A pairs are retrieval-friendly (see the structured retrieval hooks lever in `SKILL.md`).
5. Pitch the same underlying facts (not the same page) to independent listicle authors — give them a fact sheet, not your marketing copy, so they can write it in their own independent voice.

## Recipe E — Refreshing content for GEO signals

**Goal:** keep content in the freshness window generative engines favor for anything time-sensitive.

1. Inventory pages that carry perishable facts: pricing, version numbers, "best of" lists, statistics, screenshots of UI.
2. Set a refresh cadence per page type — pricing/version pages monthly, "best of" and stats pages quarterly, evergreen conceptual pages annually.
3. On each refresh: update the visible last-updated date, correct stale facts, re-verify every external citation still resolves, and update the sitemap `lastmod` for that URL.
4. Re-submit the updated URL for re-crawling where the platform supports it (e.g. Google Search Console URL inspection), and confirm LLM crawlers aren't blocked from re-fetching it (Recipe B).
5. Re-run the relevant Recipe A prompts after a refresh cycle to check whether the update changed citation behavior.

## Recipe F — Handoff to visibility tracking

**Goal:** turn the one-time audit into a monitored program.

1. Package the outputs of Recipes A-E: the prompt cluster map, the third-party mention target list and landed-placement log, the finalized robots.txt with rationale, and the freshness cadence.
2. Hand these to `maximus-llm-visibility-tracking` as the baseline data set — that skill is responsible for the ongoing measurement of citation rate, brand-mention share, and sentiment inside generated answers over time.
3. Agree on a recurring cadence (monthly is typical) for visibility tracking to re-run the same prompt set and report drift.
4. Feed tracking results back into this skill's recipes: prompts with declining citation go back through Recipe A/C; crawler or freshness issues surfaced by tracking go back through Recipe B/E.

GEO is a loop, not a one-time project — this recipe is the seam where optimization work and measurement work connect.
