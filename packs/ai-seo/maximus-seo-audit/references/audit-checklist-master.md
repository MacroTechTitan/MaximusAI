# Master audit checklist

Organized by the 4 dimensions from `SKILL.md`. Each item cross-references the sibling skill and specific recipe that executes the fix once the audit flags it. Use this as the working checklist during phase 3 (Data collection) and phase 4 (Analysis) of the 6-phase workflow — check items off as data is collected, not as fixes are made; fixing happens after prioritization.

## Scoring calibration reference

Before using the checklist, calibrate Impact / Effort / Urgency scoring (1-5 each) against these anchors:

- **Impact 5** — affects revenue-driving pages or >20% of indexed URLs, or blocks indexation entirely (e.g., robots.txt regression).
- **Impact 3** — affects a meaningful page cluster or a mid-funnel query set, but not the site's core revenue path.
- **Impact 1** — affects a handful of low-traffic pages with no clear conversion role.
- **Effort 5** — requires multiple teams, a staged rollout, or a rebuild (e.g., URL structure migration).
- **Effort 3** — a scoped engineering or content task, one owner, days not weeks.
- **Effort 1** — a config change or single-file edit, hours.
- **Urgency 5** — actively decaying right now (manual action, indexation drop, revenue-blocking bug) or blocking other fixes.
- **Urgency 3** — degrading slowly or a known risk that hasn't triggered yet.
- **Urgency 1** — stable but suboptimal; no clock running.

`Priority score = Impact x Urgency / Effort`. See `examples/prioritization-trace.md` for this applied to 40 real findings.

## 1. Technical dimension

Primary execution skill: `maximus-technical-seo`.

- [ ] Crawlability: robots.txt not blocking anything unintended; no accidental noindex on live sections. Verify with a fresh crawl comparison after any deploy.
- [ ] Indexation: GSC coverage report shows no unexpected spike in "excluded" or "error" pages. Cross-check against the sitemap.
- [ ] Sitemap hygiene: sitemap contains only live, indexable, canonical URLs — no 404s, no redirects, no discontinued sections.
- [ ] Core Web Vitals: LCP, CLS, INP within "good" thresholds on the top-traffic pages, using both PSI lab data and CrUX field data. For the full CWV diagnostic and fix workflow, run `maximus-technical-seo` recipe (a).
- [ ] Redirect chains: no chain longer than one hop; no redirect loops (especially in checkout/conversion flows — treat as urgency 5 regardless of page count).
- [ ] Canonicalization: every indexable page has a correct self-referencing or cross-referencing canonical; faceted-navigation and parameterized URLs are canonicalized or blocked from crawl.
- [ ] Duplicate content: no staging/CDN subdomains indexed; no near-duplicate category/filter pages competing with the canonical version.
- [ ] Schema/structured data: markup present and valid (not just present — validate) for the page types that benefit: Product, Article, FAQ, Review, Breadcrumb, VideoObject as applicable. For schema implementation specifics, run `maximus-technical-seo` recipe covering structured data.
- [ ] Mobile rendering: pages render and are usable on mobile viewport; tap targets sized correctly; no mobile-specific blocking issues.
- [ ] Site architecture: no orphaned sections (pages with no internal inlinks); crawl depth from homepage to any indexable page reasonable (ideally under 4 clicks).
- [ ] International: hreflang present and correct if multiple country/language versions exist.
- [ ] Server performance: TTFB reasonable under load; no server-side bottleneck masquerading as a front-end CWV issue.

## 2. Content dimension

Primary execution skill: `maximus-content-seo`.

- [ ] Thin content: no indexable page under a reasonable word-count/depth threshold for its type (a 50-word category page is a finding; a 50-word product spec sheet may not be).
- [ ] Duplicate/cannibalizing content: no two URLs targeting the same primary query; consolidate or differentiate.
- [ ] On-page optimization: title tags unique and descriptive per URL (not templated duplicates across variants); meta descriptions present; heading structure logical (one H1, nested H2/H3).
- [ ] Content decay: pages that have lost ranking position or traffic over the audit window, especially ones untouched for years — flag for refresh.
- [ ] Internal linking: every page links to and from at least one topically relevant sibling; hub pages link to all spokes; no dead-end pages.
- [ ] Image alt text: present and descriptive on content-bearing images, especially product and instructional images.
- [ ] Content completeness against the topical plan: compare live content against the subtopic tree from `maximus-ai-seo-strategy` — flag subtopics that are missing or shallow.
- [ ] Manual actions: check GSC for any active manual action related to content quality; this overrides normal prioritization — treat as urgency 5.

## 3. Backlink dimension

Primary data source: Ahrefs/Semrush/GSC. Competitor-gap methodology: `maximus-ai-seo-strategy`. Remediation execution: `maximus-technical-seo` (technical disavow/redirect mechanics) and outreach handled outside this skill pack.

- [ ] Referring domain trend: growing, flat, or declining over the audit window. Flat/declining for 6+ months without an active link-building program is a strategic gap, not a quick fix.
- [ ] Toxic link check: identify links from clearly spammy/link-farm domains; assess disavow need (usually low urgency unless volume is high or a manual action is present).
- [ ] Anchor text distribution: check for over-optimization (excessive exact-match anchors), which can trigger algorithmic distrust.
- [ ] Lost links: identify high-value links lost recently and whether recoverable (e.g., a page moved without notifying the linking site).
- [ ] Competitor link gap: identify publications/domains that link to competitors but not to this site — feed into `maximus-ai-seo-strategy`'s query gap and outreach planning.
- [ ] Internal "backlink" equivalent — internal link equity: confirm high-authority pages pass link equity to priority pages via internal linking, not just external links.

## 4. AI-Visibility dimension

Primary execution skills: `maximus-aeo-optimization` (on-page answer formatting), `maximus-geo-optimization` (citation tuning). Measurement: `maximus-llm-visibility-tracking`.

- [ ] Citation rate: for the target query set, what fraction are answered with a citation to this domain versus competitors? Establish a baseline; this is the metric the whole dimension optimizes.
- [ ] Answer-shaped structure: do priority pages lead with a direct, extractable answer near the top rather than a narrative introduction? For the formatting fix workflow, run `maximus-aeo-optimization`.
- [ ] Extractability blockers: is content hidden behind JS rendering that non-JS-executing crawlers/retrievers can't see? Check rendered vs. raw HTML.
- [ ] FAQ/comparison formatting: do pages that naturally answer comparison or FAQ-style queries use matching schema and visible structure (tables, lists)?
- [ ] Specificity and citation-worthiness: do pages contain the concrete data, examples, or claims that make a source worth citing, versus generic marketing language? Run `maximus-geo-optimization` for the citation-tuning diagnostic and fix.
- [ ] Competitive citation gap: for queries where a competitor is cited and this site isn't, what structural or content difference explains it? Document per-query, not just in aggregate.
- [ ] Tracking hookup: is there a repeatable mechanism to re-check citation rate after fixes ship? If not, set one up via `maximus-llm-visibility-tracking` before closing the audit.

## Using this checklist

1. Work top to bottom within each dimension during Data collection (phase 3) — don't skip a section because "it's probably fine"; note "checked, no issue found" explicitly so the report can state coverage was complete.
2. Every checked item that surfaces a finding gets scored using the calibration reference above and moves into the flat findings list for Prioritization (phase 5) — see `examples/prioritization-trace.md`.
3. Cross-reference the named sibling skill for the actual fix; this checklist diagnoses, it does not execute.
