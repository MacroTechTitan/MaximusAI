# maximus-aeo-optimization

Answer Engine Optimization skill for the Maximus SEO pack. Structures content so LLM-driven answer engines — ChatGPT, Claude, Gemini, Perplexity, and Google AI Overviews — cite it or extract it as an answer, instead of merely ranking it.

## What this is

AEO is not SEO with a new acronym. SEO optimizes for ranking (get clicked); AEO optimizes for extraction (get quoted, paraphrased, and attributed — often with no click at all). This skill encodes the six levers that move extraction odds, the content structures that make a paragraph liftable, and the schema.org markup that removes ambiguity for the crawler.

## Files in this skill

| File | Purpose |
|---|---|
| `SKILL.md` | Core skill definition: purpose, the 6 AEO levers, structure patterns, schema priorities, citation-hook writing, anti-patterns, sibling skills. Load this first. |
| `HOWTO.md` | Six step-by-step recipes: restructuring an article, adding FAQPage schema, writing quotable claims, auditing citation potential, building a definition post, and handing off to visibility tracking. |
| `examples/aeo-restructure-trace.md` | Worked example — a bloated blog draft rebuilt lever-by-lever, before and after, with real JSON-LD. |
| `examples/quotable-claims-trace.md` | Worked example — ten claims rewritten from vague to atomic, quotable, and attributed, with reasoning for each. |
| `references/schema-markup-cookbook.md` | Copy-paste JSON-LD templates: FAQPage, HowTo, Article, Organization, Product, Person, BreadcrumbList. Gotchas and validation tools. |

## When to use this skill

Load it whenever the task is about getting a specific page or piece of content cited, quoted, or extracted by an AI assistant or AI Overview — not general ranking work. See the WHEN TO USE / WHEN NOT TO USE section inside `SKILL.md`'s frontmatter for the exact trigger phrases and boundary cases.

## How it fits the Maximus SEO pack

This skill is one of seven SEO-pillar siblings:

- `maximus-aeo-optimization` (this skill) — per-page extraction/citation optimization.
- `maximus-geo-optimization` — multi-market, multi-language generative engine optimization.
- `maximus-content-seo` — classic keyword/ranking-focused on-page SEO.
- `maximus-technical-seo` — crawlability, indexation, site-wide structured data.
- `maximus-ai-seo-strategy` — portfolio-level prioritization across an AI-search program.
- `maximus-write-article` — first-draft long-form content creation.
- `maximus-llm-visibility-tracking` — monitoring which pages actually get cited over time.

A typical flow: write with `maximus-write-article` → restructure for extraction with `maximus-aeo-optimization` → mark up with schema from `references/schema-markup-cookbook.md` → publish → close the loop with `maximus-llm-visibility-tracking`.

## Quick start

1. Read `SKILL.md` for the six levers and anti-patterns.
2. Have a draft in hand (existing page or fresh `maximus-write-article` output).
3. Follow `HOWTO.md` recipe (a) to restructure it.
4. Pull the matching JSON-LD template from `references/schema-markup-cookbook.md` and validate it.
5. Use `examples/quotable-claims-trace.md` as a model for tightening individual sentences.
