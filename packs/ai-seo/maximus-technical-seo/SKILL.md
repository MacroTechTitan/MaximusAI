---
name: maximus-technical-seo
description: "Classic and modern technical SEO: crawlability, indexation, Core Web Vitals (LCP, INP, CLS), schema.org/JSON-LD, sitemaps, canonicals, hreflang, log-file analysis, JavaScript SEO (SSR/SSG/hydration), mobile-first, and HTTPS/security. USE WHEN: the user says 'technical seo', 'core web vitals', 'crawlability', 'indexation', 'sitemap', 'canonical', 'schema markup', 'json-ld', 'hreflang', 'log file analysis', 'javascript seo', 'ssr for seo', 'lcp inp cls', or needs a page/site to be crawlable, indexable, fast, and correctly marked up. DO NOT USE for keyword/topical strategy (use maximus-ai-seo-strategy), for writing or restructuring article content (use maximus-content-seo), for a full page/site audit report synthesizing multiple signals (use maximus-seo-audit), for answer-snippet/AEO formatting of existing content (use maximus-aeo-optimization), or for deploy pipelines/infra unrelated to page performance (use maximus-devops-ship, though CWV regressions from a bad deploy are this skill's territory)."
metadata:
  pillar: seo
  source: maximus
---

# Maximus — Technical SEO

Content can be brilliant and still rank nowhere if a crawler can't reach it, an indexer won't keep it, or a browser renders it too slowly to pass Core Web Vitals. This skill is the plumbing layer: the part of SEO that has nothing to do with what the page says and everything to do with whether a search engine can fetch it, understand it, and trust it enough to show it. Get the plumbing wrong and no amount of great writing fixes it.

## When to use

- Diagnosing why a page or site section isn't being crawled, indexed, or ranking despite good content.
- Investigating a Core Web Vitals regression (LCP, INP, CLS) flagged in Search Console or a lab tool.
- Auditing crawlability on a new or migrated site: robots.txt, sitemap, internal linking, orphan pages.
- Fixing canonical tags, duplicate content, or pagination issues.
- Implementing hreflang for a multi-locale site.
- Running log-file analysis to find crawl-budget waste.
- Deciding SSR vs. SSG vs. CSR vs. hybrid rendering for an SEO-sensitive route.
- Validating structured data (JSON-LD) for rich-result eligibility.
- The user says: "technical seo", "core web vitals", "crawlability", "indexation", "sitemap", "canonical", "schema markup", "json-ld", "hreflang", "log file analysis", "javascript seo", "ssr for seo", "lcp inp cls".

## When not to use

- Deciding *what* topics or keywords to target — that's `maximus-ai-seo-strategy`.
- Improving article structure, headings, or on-page copy quality — that's `maximus-content-seo`.
- Producing a full consolidated audit report across technical + content + AI-visibility signals — that's `maximus-seo-audit`, which this skill feeds.
- Formatting content for AI Overviews / answer boxes once it's already indexable — that's `maximus-aeo-optimization`.
- General CI/CD, infra, or deploy pipeline work not tied to a page-performance regression — that's `maximus-devops-ship`.
- Tuning content so LLMs cite it more (GEO) — that's `maximus-geo-optimization`.

## Purpose

Technical SEO answers three questions in order: **can it be found** (crawlability), **will it be kept** (indexation), and **is it good enough to serve** (Core Web Vitals, structured data, security). Every fix here is diagnostic-first — never apply a change (a redirect, a canonical, a rendering strategy) without first confirming the underlying failure with real tool output (Search Console, PageSpeed Insights, server logs), not assumption.

## The technical SEO checklist

Work top-down; a failure upstream masks everything below it.

- **Crawlability** — robots.txt doesn't block CSS/JS/critical paths; internal links reach every indexable page within a few clicks; no orphan pages; crawl budget isn't wasted on faceted-navigation or parameter explosions.
- **Indexation** — pages return 200s, not soft-404s; `noindex` is intentional, not accidental; Search Console's "Page indexing" report matches expectations; paginated/duplicate content resolves to one canonical version.
- **Core Web Vitals** — LCP, INP, CLS pass at the 75th percentile of real-user data (CrUX), not just in a single lab run.
- **Structured data** — JSON-LD validates, matches visible page content, and targets schema types with real rich-result eligibility.
- **Sitemap / robots** — sitemap.xml lists only canonical, indexable, 200-status URLs and is referenced in robots.txt; robots.txt is minimal and reviewed after every major site change.
- **Canonicals** — one canonical per page, self-referencing on the canonical version, absolute URLs, no cross-domain surprises.
- **Internationalization** — hreflang is bidirectional (return tags present), covers all locale variants including x-default, and matches the sitemap.
- **JS rendering** — indexable content is present in the initial HTML response (SSR/SSG) or reliably rendered by Googlebot's renderer, verified with "URL Inspection" in Search Console.
- **Security** — HTTPS everywhere, no mixed content, valid certificate chain, HSTS considered.

See `references/technical-seo-checklist.md` for the full ~50-item version with pass criteria and check methods.

## Core Web Vitals thresholds

| Metric | Good | Needs Improvement | Poor |
|---|---|---|---|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5s–4.0s | > 4.0s |
| INP (Interaction to Next Paint) | < 200ms | 200ms–500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1–0.25 | > 0.25 |

Thresholds are evaluated at the 75th percentile of field data (CrUX / Search Console), not a single lab score. A page can pass Lighthouse and still fail CWV in the field on slower devices or networks.

## JS SEO decision tree

1. **Is the content indexable-critical (product info, article body, prices)?**
   - No (pure interactivity, e.g., a cart widget) → CSR is fine.
   - Yes → continue.
2. **Does content change per-request based on user identity/session?**
   - Yes → SSR (server-render on each request) or CSR with server-rendered fallback shell.
   - No → continue.
3. **Does content change frequently but not per-user (e.g., inventory, price)?**
   - Yes → SSG + ISR (Incremental Static Regeneration) or SSR with caching (CDN edge cache + revalidate).
   - No → continue.
4. **Is content essentially static (marketing pages, docs, evergreen articles)?**
   - Yes → SSG (build-time static generation). Fastest, cheapest, easiest to verify indexation for.
5. **Hybrid sites**: use SSG/ISR for indexable routes, CSR for authenticated/interactive routes, and confirm the split with `next build` output (Static vs. Server vs. Dynamic per route) before shipping.

Rule of thumb: if Googlebot must run JavaScript to see the content, verify with Search Console's "URL Inspection → View Crawled Page" that the rendered HTML actually contains it — don't assume the renderer behaves like a browser.

## Log-file analysis workflow

1. Pull raw web-server or CDN logs (not analytics — logs, because analytics misses bots) filtered to verified search-engine user agents (verify by reverse-DNS, not user-agent string alone).
2. Aggregate hits by URL path and status code; find the ratio of crawl hits to indexable pages.
3. Flag waste: high-frequency crawls of non-indexable, parameterized, or redirect-chain URLs; low/no crawls of important pages.
4. Cross-reference crawl frequency against last-modified dates — pages that change often but get crawled rarely are under-served; static pages crawled constantly are over-served.
5. Check crawl date coverage against sitemap `lastmod` to confirm the sitemap is actually driving discovery.
6. Turn findings into action: block/noindex waste sources, fix redirect chains, strengthen internal links to under-crawled priority pages.

## Anti-patterns

- **Blocking CSS/JS in robots.txt** — starves the renderer of what it needs to see the real page; almost never the right call today.
- **Orphan pages** — pages reachable only via sitemap with no internal links pointing to them; crawlers deprioritize what the link graph doesn't reinforce.
- **Duplicate/conflicting canonicals** — multiple canonical tags, or a canonical pointing to a redirect/404/noindexed page, both signal confusion the algorithm resolves unpredictably.
- **Missing hreflang return tags** — locale A pointing to locale B without B pointing back invalidates the whole cluster.
- **CSR-only for indexable content** — shipping a blank shell with content injected client-side and hoping the crawler waits; verify, don't hope.

## Sibling skills

- `maximus-ai-seo-strategy` — decides what to target before this skill decides how to make it crawlable/fast.
- `maximus-content-seo` — on-page content structure and quality; this skill assumes the content exists and is technically deliverable.
- `maximus-seo-audit` — the consolidated report this skill's findings feed into.
- `maximus-aeo-optimization` — schema and answer-format tuning once the page is already indexable and fast.
- `maximus-devops-ship` — deploy-time performance regressions (bundle bloat, missing caching headers, CDN misconfig) are diagnosed here but fixed in coordination with that skill's pipeline.
- `maximus-ai-seo-strategy` and `maximus-geo-optimization` sit above and beside this one on strategy; this skill is pure execution of the technical layer.
