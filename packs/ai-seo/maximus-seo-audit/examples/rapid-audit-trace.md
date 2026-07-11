# Worked example: 48-hour rapid audit of a small SaaS site

Site: a fictional B2B SaaS product, "Ledgerly" (invoicing software for freelancers), ~100 URLs total: marketing pages, a 40-post blog, a docs section, and a pricing page. Traffic has been flat for two quarters and the founder wants a diagnosis before the next content push. This trace follows recipe (a) from `HOWTO.md`.

## Phase 1 — Scope (30 min)

- Domain: `ledgerly.example` (fictional).
- Business goal: grow organic signups; blog traffic is flat, pricing page conversion is fine.
- All 4 dimensions in scope given the site's small size and the low cost of covering all of them.
- Deadline: 2 working days.

## Phase 2 — Crawl (2.5 hrs)

Fetched `ledgerly.example/sitemap.xml` with `fetch_url`, got 98 URLs (2 more found via internal links not in the sitemap — a finding in itself). Walked all 98 with `fetch_url`, logging status code, title, H1, canonical tag, and word count.

Findings from the crawl pass:
- 3 blog posts return a 404 (deleted without a redirect) but are still linked from the blog index.
- 12 blog posts have no meta description; 8 have a duplicate title with another post.
- The docs section (18 pages) has no internal links back to the blog or marketing pages — an orphaned silo.
- 2 URLs found via internal links are missing from the sitemap entirely (a sitemap generation bug).
- Canonical tags are present and correct on 94/98 pages; 4 pricing-page variants (A/B test URLs) have no canonical, risking duplicate-content dilution.

## Phase 3 — Data collection (2.5 hrs)

- **PageSpeed Insights** on the 10 highest-traffic pages (homepage, pricing, top 8 blog posts by historical traffic): homepage LCP 4.1s (poor), pricing page LCP 2.3s (needs improvement), blog posts averaging 2.8s (needs improvement) — mobile scores worse across the board, largely driven by an unoptimized hero image on the homepage and a third-party chat widget script loading render-blocking.
- **GSC**: top queries show impressions holding steady but clicks declining slightly — average position for the top 15 queries slipped from ~6 to ~9 over the past quarter, consistent with the "flat traffic" complaint being a slow ranking slide, not a sudden drop.
- **Backlink spot-check** (Ahrefs free tool): referring domains flat at 340 for 8 months — no active link acquisition, and 6 links from clearly spammy directories that add no value and carry minor toxicity risk.
- **AI-visibility check**: ran 12 target queries ("best invoicing software for freelancers", "how to invoice as a freelancer", etc.) against Perplexity and ChatGPT search. Ledgerly is cited in 1 of 12; two direct competitors are cited in 8 and 6 respectively. The one citation is for a docs page, not a marketing or blog page — meaning the blog content that took months to write is essentially invisible to AI answer surfaces.

## Phase 4 — Analysis (3.5 hrs)

Running the four datasets through the sibling-skill lenses:

- **Technical** (`maximus-technical-seo` lens): the 3 broken blog links, the missing-canonical A/B pages, the sitemap gap, and the homepage LCP issue are all classic technical findings. The chat-widget-blocking-render issue is a common CWV culprit worth flagging specifically.
- **Content** (`maximus-content-seo` lens): duplicate titles and missing meta descriptions are on-page gaps; the orphaned docs silo is an internal-linking architecture gap; the ranking slide on 15 queries despite stable impressions suggests content decay — competitors may have refreshed pages Ledgerly hasn't touched since publish.
- **Backlink**: flat referring domains for 8 months is a growth problem, not a health problem; the 6 spammy links are low-severity but worth a disavow note.
- **AI-visibility** (`maximus-aeo-optimization` / `maximus-geo-optimization` lens): 1/12 citation rate versus competitors' 8/12 and 6/12 is the single most important finding in this audit — it explains why blog investment isn't showing up in the queries that increasingly get answered by AI before a user ever clicks a blue link. The cited docs page, on inspection, has a clear direct-answer paragraph near the top and a scannable list — the blog posts don't; they open with a narrative intro before getting to the answer.

## Phase 5 — Prioritization

| Finding | Impact | Effort | Urgency | Score |
|---|---|---|---|---|
| Blog posts lack answer-shaped structure (low AI citation) | 5 | 3 | 4 | 6.7 |
| Homepage LCP 4.1s / render-blocking chat widget | 4 | 2 | 4 | 8.0 |
| 3 broken blog links (404, no redirect) | 3 | 1 | 4 | 12.0 |
| Docs section orphaned from blog/marketing | 3 | 2 | 3 | 4.5 |
| 15 tracked queries sliding in average position (content decay) | 4 | 3 | 3 | 4.0 |
| Sitemap missing 2 live URLs | 2 | 1 | 2 | 4.0 |
| Duplicate titles (8 posts) / missing meta descriptions (12 posts) | 2 | 1 | 2 | 4.0 |
| A/B pricing variants missing canonical | 3 | 1 | 3 | 9.0 |
| Flat backlink growth (8 months) | 3 | 4 | 2 | 1.5 |
| 6 low-value/spammy backlinks | 1 | 1 | 1 | 1.0 |

(Full scoring mechanics and rubric: `references/audit-checklist-master.md`; general method: `examples/prioritization-trace.md`.)

## Phase 6 — Report

**Executive summary:** Ledgerly's flat traffic is a slow ranking slide plus near-total invisibility to AI answer surfaces (1 of 12 target queries cited, versus 6-8 for competitors), compounded by a fixable homepage performance issue and a handful of quick technical fixes. Shipping the top 4 fixes should recover the broken-link/canonical technical debt within a week and start moving AI-citation rate within a month once blog posts are restructured.

**Critical fixes (this week):**
1. Fix 3 broken blog links (redirect to live equivalents or remove from blog index) — `maximus-technical-seo`.
2. Add canonical tags to the 4 A/B pricing variants — `maximus-technical-seo`.
3. Fix homepage LCP: defer/lazy-load the chat widget script, compress hero image — `maximus-technical-seo`.
4. Restructure the top 5 highest-traffic blog posts to lead with a direct-answer paragraph and scannable summary — `maximus-aeo-optimization`.

**Warnings (this sprint):**
- Fix duplicate titles and missing meta descriptions across 20 posts — `maximus-content-seo`.
- Link the docs section into blog and marketing navigation — `maximus-content-seo`.
- Add the 2 missing URLs to the sitemap — `maximus-technical-seo`.
- Refresh the 15 queries showing position decay with updated data/examples — `maximus-content-seo`.

**Long-term recommendations:**
- Build a backlink acquisition plan; 8 months flat is a strategy gap, not a one-off fix — hand off to `maximus-ai-seo-strategy`.
- Apply the answer-shaped restructuring pattern (fix #4) across the remaining 35 blog posts on a rolling basis, tracked with `maximus-llm-visibility-tracking`.
- Disavow the 6 spammy backlinks at the next quarterly link review.

**Follow-up:** re-run the AI-visibility check and PageSpeed scores in 30 days; full re-audit in one quarter.
