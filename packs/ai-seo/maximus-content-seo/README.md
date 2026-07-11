# Maximus — Content SEO

On-page and content-level SEO execution skill for the Maximus SEO pack.

## What this skill does

Optimizes individual pages and content programs for classic search ranking:

- Title tag, H1, meta description, and URL patterns
- Heading structure (H2/H3) that maps to a page's subtopic coverage
- Internal linking: hub-spoke architecture, contextual in-body links, breadcrumbs
- E-E-A-T signals: author bios, credentials, sourcing, original data/experience markers
- Content refresh workflow: which stale-but-ranking pages to update, and what to change
- Content pruning workflow: kill, consolidate, or redirect decisions for underperforming pages
- Semantic optimization: entity coverage and related-term breadth, applied after E-E-A-T and structure are solid

## What this skill does not do

- Format content for LLM/AI Overview extraction and citation — see `maximus-aeo-optimization`.
- Run multi-market or multi-language AI-search programs — see `maximus-geo-optimization`.
- Fix crawlability, indexation, Core Web Vitals, or deploy schema at the infrastructure level — see `maximus-technical-seo`.
- Decide which pages should exist or how a topic clusters before anything is written — see `maximus-ai-seo-strategy`.
- Write the first draft of an article — see `maximus-write-article`.
- Audit a whole domain's health to build a triage backlog — see `maximus-seo-audit`.

## Files in this skill

- `SKILL.md` — the skill definition: on-page fundamentals, internal linking model, E-E-A-T signals, refresh workflow, pruning workflow, semantic optimization, anti-patterns.
- `HOWTO.md` — six step-by-step recipes for the most common jobs this skill handles.
- `examples/content-refresh-trace.md` — worked example of refreshing a 2-year-old ranking post that is losing traffic, with before/after diffs.
- `examples/internal-linking-trace.md` — worked example of auditing internal links across a 50-post blog, mapping hub/spoke, and producing a link-add plan.
- `references/on-page-checklist.md` — a comprehensive per-post checklist covering title formulas, meta patterns, heading patterns, URL patterns, image alt patterns, internal linking rules, and E-E-A-T minimums.

## When to load this skill

Load `maximus-content-seo` whenever the task is to optimize a specific page or a set of existing pages for on-page ranking signals — new-post optimization before publishing, an internal linking audit, a refresh pass on a decaying page, a pruning audit across a content library, or retrofitting E-E-A-T onto pages that already rank. See `SKILL.md` for the full trigger list and the explicit hand-off boundaries to sibling skills.
