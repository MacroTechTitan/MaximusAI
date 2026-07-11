# Maximus AI SEO Pack

A 7-skill opt-in pack for SEO in the age of answer engines. Covers classic technical SEO, on-page content SEO, and the two disciplines that matter when your buyers are asking LLMs instead of Google: **AEO** (Answer Engine Optimization) and **GEO** (Generative Engine Optimization).

## What's in the pack

| Skill | What it does |
|---|---|
| [`maximus-ai-seo-strategy`](./maximus-ai-seo-strategy) | Keyword research, topical authority, and content-cluster planning adapted for AI answer surfaces. The strategy layer above the tactics. |
| [`maximus-aeo-optimization`](./maximus-aeo-optimization) | Structure content so LLMs cite you — schema markup, entity clarity, quotable atomic claims, factual density. |
| [`maximus-geo-optimization`](./maximus-geo-optimization) | Get surfaced by Perplexity, ChatGPT search, Google AI Overviews, Copilot. Prompt mining, LLM-crawler config, 3rd-party mention strategy. |
| [`maximus-technical-seo`](./maximus-technical-seo) | Crawlability, Core Web Vitals, schema.org/JSON-LD, sitemaps, canonicals, JavaScript SEO, log-file analysis. |
| [`maximus-content-seo`](./maximus-content-seo) | On-page optimization, internal linking, content clusters, E-E-A-T signals, refresh + prune cadence. |
| [`maximus-seo-audit`](./maximus-seo-audit) | End-to-end audit (technical + content + backlink + AI-visibility) producing a prioritized fix list, not a data dump. |
| [`maximus-llm-visibility-tracking`](./maximus-llm-visibility-tracking) | Measure your citation rate and share of voice across Perplexity, ChatGPT, Claude, Gemini, and Google AI Overviews. |

## How the skills fit together

```
                 maximus-ai-seo-strategy
                          │
                          ▼
     ┌──────────────┬─────┴─────┬──────────────┐
     ▼              ▼           ▼              ▼
 technical-seo  content-seo  aeo-optim    geo-optim
     │              │           │              │
     └──────────────┴───┬───────┴──────────────┘
                        ▼
                   seo-audit
                        │
                        ▼
              llm-visibility-tracking
                        │
                        └─► feeds back into strategy
```

- **Strategy** at the top sets the plan.
- **Four tactical skills** execute in parallel.
- **Audit** rolls them up into a prioritized fix list.
- **Visibility tracking** measures the outcome and feeds new signal back into strategy.

## When to use this pack

- You are publishing content, docs, or a marketing site meant to be discovered.
- You want to be cited by Perplexity, ChatGPT, Claude, Gemini, or Google AI Overviews — not just ranked on Google.
- You are auditing an existing site for SEO and AI-visibility issues.
- You are measuring how often your brand appears in LLM answers.

## When not to use this pack

- Pure internal tooling with no public surface.
- One-off blog posts where you just need writing help — use [`maximus-write-article`](../../skills/maximus-write-article) directly.
- Product/UX copy — use `marketing/content-creation` or a copywriting skill.

## Getting started

New to SEO in the AI era? Run these in order:

1. `maximus-ai-seo-strategy` — build the 90-day plan.
2. `maximus-technical-seo` — fix the fundamentals so pages can be crawled + rendered.
3. `maximus-aeo-optimization` — restructure your top-10 pages for citation.
4. `maximus-geo-optimization` — configure LLM crawlers and mine prompts.
5. `maximus-content-seo` — refresh + optimize existing content.
6. `maximus-seo-audit` — full audit to catch what you missed.
7. `maximus-llm-visibility-tracking` — set up ongoing measurement.

Existing site with problems? Start with `maximus-seo-audit` and let it dispatch to the others.

## Related skills outside this pack

- [`maximus-write-article`](../../skills/maximus-write-article) — long-form article writing (used constantly alongside `content-seo` and `aeo-optimization`).
- [`maximus-deep-research`](../../skills/maximus-deep-research) — feed research into topical authority plans.
- [`maximus-brain`](../../skills/maximus-brain) — depth calibration for strategy decisions.
