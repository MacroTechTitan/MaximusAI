# Worked example: prioritizing 40 raw audit findings into a sequenced roadmap

This trace follows recipe (f) from `HOWTO.md`. Scenario: a mid-size ecommerce site (~4,000 URLs) audit produced 40 raw findings across the 4 dimensions. Below is the full scoring pass and the resulting roadmap.

## Step 1 — the flat findings list (abbreviated to 40 items, all dimensions mixed)

Findings are listed as collected, before any scoring — this is deliberately unordered to demonstrate why scoring, not collection order, must drive the roadmap.

1. Product pages (1,200 URLs) missing schema.org Product markup
2. Category pages have thin content (under 100 words) on 60 of 85 categories
3. Site-wide LCP of 3.8s on mobile (large hero carousel images, unoptimized)
4. 340 product URLs return soft-404 (page loads, shows "item unavailable," status 200)
5. Checkout flow has a redirect loop on 2 payment methods
6. Blog has 90 posts, 30 of which haven't been updated in 3+ years
7. No canonical tags on faceted-navigation URLs, creating ~8,000 near-duplicate crawlable URLs
8. Robots.txt accidentally blocks `/category/` paths (regression from last deploy)
9. Toxic backlinks: 45 links from clearly spammy link farms
10. Referring domains down 12% over 6 months (losing links faster than gaining)
11. Zero AI-Overview or chat-assistant citations across 25 target "best X" queries; top 3 competitors average 9 citations
12. Product pages lack a clear, extractable spec/comparison table (likely cause of finding 11)
13. Internal linking: category pages don't link to their top products; products don't link to related categories
14. Title tags duplicated across 200+ product variants (color/size variants sharing one title)
15. Mobile tap targets too small on the category filter UI (CWV/UX issue)
16. XML sitemap includes 400 URLs that 404
17. Blog posts have no internal links to product pages (missed conversion path)
18. Structured data errors: existing Review schema fails validation on 90% of product pages
19. Site search results pages are indexable and duplicate product-listing content
20. No hreflang tags despite serving 3 country versions of the site
21. Core product category ("winter coats") has keyword cannibalization across 4 separate URLs
22. Image alt text missing on 70% of product images
23. Pagination on category pages uses `?page=2` params with no rel=next/prev, and is duplicated in the index
24. 12 high-traffic legacy blog URLs 301 to the homepage instead of a relevant live page (link equity waste)
25. Author bio pages for blog (8 URLs) are indexed but empty/thin
26. Page speed: JS bundle size flagged as "large" (600kb+) on product pages, contributing to CLS
27. Backlink anchor text over-optimized on 30% of external links (exact-match anchor risk)
28. FAQ content on product pages not marked up with FAQ schema despite matching AI-Overview FAQ formatting elsewhere
29. Competitor gap: competitors have buying-guide content for 15 subtopics Ledgerly-style comparison lacks (site has none)
30. Out-of-stock products (900 URLs) show no alternative product recommendations, just an empty page
31. Duplicate content: 3 CDN/staging subdomains fully indexed, mirroring live site
32. No breadcrumb schema despite breadcrumb UI existing
33. Meta descriptions missing on 55% of category pages
34. Google Search Console shows a manual action warning for "thin content with little added value" issued 2 weeks ago
35. Product page URLs inconsistent: some use `/product/slug`, others `/p/slug` (legacy pattern), both live and both crawlable
36. Server response time (TTFB) averaging 1.2s on product pages under load
37. No internal search analytics tracked — unknown what users search for and don't find
38. Video content on 20 product pages has no VideoObject schema
39. Backlink profile has zero links from the 3 publications competitors are consistently cited from
40. Old sitemap still references a discontinued `/deals/` section (410 pages), confusing crawl priority

## Step 2 — score every finding (Impact / Effort / Urgency, 1-5 each)

Selected findings shown with scoring rationale; full 40-row table follows the same method.

| # | Finding | Impact | Effort | Urgency | Score (I x U / E) |
|---|---|---|---|---|---|
| 34 | GSC manual action: thin content warning | 5 | 3 | 5 | 8.3 |
| 8 | Robots.txt blocking /category/ (regression) | 5 | 1 | 5 | 25.0 |
| 5 | Checkout redirect loop, 2 payment methods | 5 | 2 | 5 | 12.5 |
| 4 | 340 soft-404 product URLs | 4 | 3 | 4 | 5.3 |
| 7 | No canonical on faceted nav (~8,000 URLs) | 5 | 3 | 3 | 5.0 |
| 11 | Zero AI-citation vs competitors' 9 avg | 5 | 4 | 3 | 3.75 |
| 12 | No extractable spec/comparison tables | 4 | 3 | 3 | 4.0 |
| 1 | Missing Product schema, 1,200 URLs | 4 | 2 | 3 | 6.0 |
| 3 | Mobile LCP 3.8s (hero carousel) | 4 | 2 | 3 | 6.0 |
| 21 | Keyword cannibalization, "winter coats" | 3 | 2 | 3 | 4.5 |
| 31 | Staging subdomains indexed | 3 | 1 | 3 | 9.0 |
| 16 | Sitemap includes 400 dead URLs | 2 | 1 | 3 | 6.0 |
| 40 | Sitemap references discontinued /deals/ | 2 | 1 | 3 | 6.0 |
| 18 | Review schema fails validation, 90% of PDPs | 3 | 2 | 2 | 3.0 |
| 9 | 45 toxic backlinks | 2 | 1 | 2 | 4.0 |
| 29 | Competitor buying-guide content gap | 4 | 5 | 2 | 1.6 |
| 39 | Zero links from 3 key publications | 3 | 5 | 2 | 1.2 |
| 25 | Empty author bio pages, 8 URLs | 1 | 1 | 1 | 1.0 |
| 6 | 30 stale blog posts (3+ yrs) | 2 | 3 | 2 | 1.3 |
| 37 | No internal search analytics | 2 | 2 | 2 | 2.0 |

(Remaining 20 findings scored identically; omitted here for length but included in the client-facing version of this trace.)

## Step 3 — sort and tier

**Critical fixes (score ≥ 8, ship this week):**
- #8 Robots.txt regression (score 25.0) — one-line config revert. Blocking `/category/` is actively deindexing the site right now.
- #5 Checkout redirect loop (score 12.5) — revenue-blocking, not just SEO; escalate outside the audit too.
- #31 Staging subdomains indexed (score 9.0) — duplicate-content risk compounding daily; add noindex + robots block.
- #34 GSC manual action (score 8.3) — direct ranking risk; must be addressed and a reconsideration request filed once fixed.

**Warnings (score 3-8, this sprint/month):**
- #7 Faceted-nav canonicals, #1 Product schema, #3 Mobile LCP, #16/#40 sitemap cleanup, #4 soft-404s, #12 extractable comparison tables, #21 cannibalization, #18 Review schema validation, #9 toxic backlinks.

**Long-term backlog (score < 3, next quarter+):**
- #29 Competitor buying-guide gap (hand off to `maximus-ai-seo-strategy` — this is a content strategy build, not a quick fix).
- #39 Publication link gap (hand off to backlink/PR workstream).
- #6 Stale blog refresh, #25 author bios, #37 search analytics instrumentation.

## Step 4 — sequencing notes

- #8 and #31 ship same day — both are config/indexing fixes with near-zero engineering cost and compounding daily cost if left.
- #5 (checkout loop) escalates immediately regardless of audit cadence — this is a revenue bug wearing an SEO-audit disguise.
- #34 (manual action) blocks the reconsideration request until the underlying thin-content issue (#2, category pages under 100 words) is actually fixed — sequence #2 before filing reconsideration, even though #2 itself scores lower in isolation. Document this dependency explicitly; the formula doesn't see it.
- #11 (AI-citation gap) and #12 (no extractable tables) are linked findings — fixing #12 is very likely the mechanism that improves #11. Sequence #12 first and treat #11 as the success metric via `maximus-llm-visibility-tracking`, not as a separate fix.

## Output

Roadmap handed to the team as: this week (4 items), this sprint (9 items), this quarter (remaining warnings), backlog (3 strategic items routed to `maximus-ai-seo-strategy`). Re-check scheduled at 30 days for the critical fixes and 90 days for a full re-audit.
