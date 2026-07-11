# maximus-technical-seo

Classic and modern technical SEO for the Maximus suite: crawlability, indexation, Core Web Vitals (LCP, INP, CLS), schema.org/JSON-LD, sitemaps, canonicals, hreflang, log-file analysis, JavaScript SEO (SSR/SSG/hydration), mobile-first, and HTTPS/security.

This is the "plumbing" skill in the `maximus-seo-pack`. It doesn't decide what to write or what keywords to target — it makes sure whatever exists can be crawled, kept in the index, and served fast enough to compete.

## Files

- `SKILL.md` — the skill definition: when to use it, the technical SEO checklist, CWV thresholds, the JS rendering decision tree, the log-file analysis workflow, and anti-patterns.
- `HOWTO.md` — six step-by-step recipes for the most common technical SEO tasks.
- `examples/cwv-diagnosis-trace.md` — a worked example diagnosing and fixing an LCP failure end to end.
- `examples/js-seo-migration-trace.md` — a worked example migrating a Next.js CSR product catalog to SSG/ISR and verifying indexation.
- `references/technical-seo-checklist.md` — a ~50-item checklist across all technical SEO categories, each with pass criteria and how to check.

## When to reach for this skill

Any time the question is "can this be found/kept/served fast" rather than "is this good content" or "should this exist." If Search Console shows an indexation drop, a CWV regression, a sitemap error, or the user mentions robots.txt, canonicals, hreflang, schema markup, or SSR/CSR — this is the skill.

## Sibling skills in `maximus-seo-pack`

- `maximus-ai-seo-strategy` — what to target and why, before this skill makes it deliverable.
- `maximus-content-seo` — on-page content structure and quality.
- `maximus-seo-audit` — the consolidated audit report this skill's findings feed.
- `maximus-aeo-optimization` — schema/answer-format tuning for AI answer surfaces.
- `maximus-geo-optimization` — tuning content so LLMs cite it more often.
- `maximus-llm-visibility-tracking` — tracking rankings/citations over time.
- `maximus-devops-ship` — deploy pipelines and infra; this skill diagnoses deploy-caused performance regressions and coordinates the fix through that pipeline.
