# HOWTO — maximus-seo-audit

Six recipes covering the situations this skill gets invoked for most often. Each recipe follows the same 6-phase workflow from `SKILL.md` (Scope, Crawl, Data collection, Analysis, Prioritization, Report) but adapts the depth and tooling to the situation.

## (a) 48-hour rapid audit for a small site

Use when the site is small (roughly under 500 URLs), there's no budget for enterprise crawl tooling, and the deliverable is needed in one to two days.

1. **Scope (30 min)** — confirm domain, business goal (traffic, leads, or AI citations), and which of the 4 dimensions matter most given the goal. For a small site, all 4 are usually in scope since the total effort is low.
2. **Crawl (2-3 hrs)** — fetch the sitemap.xml with `fetch_url`, walk the URL list, and spot-check status codes, titles, headings, and canonical tags on every page (or a representative sample above ~150 URLs). No enterprise crawler needed at this scale.
3. **Data collection (2-3 hrs)** — pull PageSpeed Insights scores for the 10 highest-traffic pages, GSC coverage and top-query reports if available, a free-tier or spot-check backlink profile (Ahrefs/Semrush free tools), and run 10-15 target queries against Perplexity/ChatGPT/Google AI Overview to check citation presence.
4. **Analysis (3-4 hrs)** — apply the diagnostic checklists from `maximus-technical-seo`, `maximus-content-seo`, `maximus-aeo-optimization`, and `maximus-geo-optimization` to what you found. At this scale, do this by hand rather than waiting on tooling exports.
5. **Prioritization (1-2 hrs)** — score every finding on impact x effort x urgency. Small sites rarely have more than 20-30 findings; this step is fast.
6. **Report (2-3 hrs)** — write the executive summary, critical fixes, warnings, long-term recommendations. Total: one to two working days.

See `examples/rapid-audit-trace.md` for a full worked version of this recipe on a 100-URL SaaS site.

## (b) Full audit for a 10k+ URL site

Use when the site is large enough that manual crawling is infeasible and sampling risks missing systemic issues.

1. **Scope** — segment the site by section (blog, product, docs, marketing) before anything else. A 10k-URL site audited as one undifferentiated blob produces findings too coarse to prioritize; segmented findings can be compared section-to-section.
2. **Crawl** — run Screaming Frog (list mode against the sitemap plus a spider crawl to catch orphans) or Sitebulb for the full crawl. Budget for crawl time — a 10k-URL site can take hours depending on server response time and rate limits. Export the full crawl to a structured file (CSV/database), not just the tool's dashboard.
3. **Data collection** — pull GSC data via the API for the full URL set (UI exports cap at 1,000 rows), backlink data from Ahrefs/Semrush at the domain and top-page level, and CrUX field data (not just PSI lab data) since a 10k-URL site's CWV story is a distribution, not a single number.
4. **Analysis** — aggregate by section and by template/page-type, not just by individual URL. A systemic issue (e.g., a broken canonical tag in a template) affecting 3,000 URLs should surface as one finding with a 3,000-URL impact, not 3,000 separate findings.
5. **Prioritization** — impact scoring naturally favors template-level and architecture-level fixes at this scale, since one fix touches thousands of URLs. Effort should account for the QA burden of a template-level change (staging, regression testing) which is higher than a single-page fix.
6. **Report** — the executive summary should lead with the 2-3 systemic (template/architecture) issues before any individual-page findings; those are almost always the highest-leverage items on a large site.

## (c) Post-migration audit

Use immediately after a redesign, replatform, CMS migration, or domain/URL-structure change — the highest-risk moment for SEO equity loss.

1. **Scope** — get the pre-migration URL inventory and redirect map before starting. Without a "before" state, you cannot tell what broke versus what was never there.
2. **Crawl** — crawl the live site and diff against the pre-migration inventory. Flag: URLs that 404 with no redirect, redirect chains longer than one hop, redirects pointing to the wrong destination (a common migration bug: bulk redirects mapped by pattern instead of 1:1), and any URL that changed content without a corresponding redirect.
3. **Data collection** — pull GSC coverage reports for both the old and new property (if the domain changed) to catch a spike in "not found" or "duplicate without canonical" errors, which are the fastest signal that a migration broke crawlability.
4. **Analysis** — run every 404/broken-redirect finding through `maximus-technical-seo` immediately; these are almost always critical/urgent regardless of the impact x effort math, because they compound daily until fixed.
5. **Prioritization** — urgency dominates in a post-migration audit. Anything actively bleeding indexed pages or link equity jumps the queue ahead of items that would normally score higher on impact alone.
6. **Report** — lead with a redirect/404 remediation list as the critical-fixes section; this is typically the entire critical-fixes section for a post-migration audit. Long-term recommendations should include a migration retrospective (what process gap allowed the break) so the next migration doesn't repeat it.

## (d) Competitor audit (audit their site to learn)

Use when the goal is not to fix a competitor's site but to learn what's working for them before building or revising your own strategy.

1. **Scope** — pick 1-3 competitors who currently win the target queries or topic (rank top 3, or get cited most in AI answers). Scope the audit to their strongest-performing sections, not their whole site.
2. **Crawl** — a lighter crawl than a full self-audit: use `fetch_url` against their sitemap and category pages to build a content inventory; a full technical crawl of a competitor's site is usually unnecessary since you cannot fix their technical issues anyway.
3. **Data collection** — this is where the audit differs most from a self-audit: focus on backlink profile (who links to them and why — via Ahrefs/Semrush), content structure (how they format pages that get cited by AI Overviews — read the actual page, not just metadata), and internal linking patterns (how they build topical authority).
4. **Analysis** — instead of scoring their issues, score their strengths: what structural, content, or backlink patterns correlate with their ranking/citation success. Feed this into `maximus-ai-seo-strategy`'s query gap analysis workflow.
5. **Prioritization** — prioritize by "most learnable and most transferable" rather than impact x effort x urgency, since you're not fixing their site — you're deciding which of their patterns to adopt.
6. **Report** — deliverable is a "what they do that we don't" comparison document, not a fix list. Hand off directly to `maximus-ai-seo-strategy` for translating findings into your own content/backlink backlog.

## (e) AI-visibility-focused audit

Use when the primary concern is whether the site is cited by AI Overviews, Perplexity, ChatGPT, Claude, and Gemini — technical/content health is secondary or already known to be fine.

1. **Scope** — define the target query set: the 20-50 queries where AI citation matters most commercially. This audit is query-set-driven, not URL-driven.
2. **Crawl** — a light technical pass only to confirm nothing structural is blocking extraction (robots.txt, JS-rendering issues that hide content from crawlers that don't execute JS, missing/broken schema).
3. **Data collection** — run every target query against each major AI surface and log: cited or not, which URL got cited (yours, a competitor's, or neither), and the exact snippet/answer given. Use `maximus-llm-visibility-tracking` for a repeatable version of this if the check will recur.
4. **Analysis** — for queries where you're not cited, check via `maximus-aeo-optimization` whether the page lacks answer-shaped structure (no direct answer near the top, no scannable summary) and via `maximus-geo-optimization` whether the page lacks the citation-worthy signals (specificity, data, structured claims) LLMs favor when picking a source.
5. **Prioritization** — weight impact by query commercial value and by how close the page already is to being cited (a page that's almost-cited with one structural gap is higher-leverage than one that would need a rewrite).
6. **Report** — structure the critical-fixes section by query, not by page: "Query X: not cited, competitor Y is cited, gap is missing direct-answer paragraph — fix via maximus-aeo-optimization." This format keeps the business objective (win this query) visible instead of getting lost in page-level detail.

## (f) Building the prioritized fix list

The prioritization phase deserves its own recipe because it's the step audits most often skip or shortcut.

1. Collect every finding from every dimension into one flat list before scoring anything — don't score technical findings against each other first and content findings separately; they need to be on the same list to be compared fairly.
2. Score each on Impact (1-5), Effort (1-5), Urgency (1-5) using the rubric in `SKILL.md` and the worked calibration examples in `references/audit-checklist-master.md`.
3. Compute `Priority score = Impact x Urgency / Effort` for each finding.
4. Sort descending. Top decile = critical fixes. Next tier = warnings. Bottom = long-term backlog.
5. Sanity-check the top 5 against gut judgment and business context — a scoring formula is a tool, not a substitute for knowing that a specific page is under executive scrutiny this week. Adjust and document any manual override.
6. Sequence the critical fixes into a rough timeline (this week, this sprint, this month) accounting for shared dependencies (e.g., a redirect-map fix should land before a content-consolidation fix that depends on it).

See `examples/prioritization-trace.md` for this recipe applied to 40 real findings end-to-end.
