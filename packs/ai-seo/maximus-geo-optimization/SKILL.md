---
name: maximus-geo-optimization
description: "Generative Engine Optimization: getting content surfaced and cited by generative search engines (Perplexity, Google AI Overviews/SGE, ChatGPT search, You.com, Bing Copilot, Claude with web). WHEN TO USE: 'geo', 'generative engine optimization', get surfaced by Perplexity, LLM search optimization, SGE optimization, Copilot optimization, GPTBot, LLM crawler, robots.txt for AI bots, brand mentions in LLM answers. Covers the 5 GEO levers (source authority, 3rd-party mention density, LLM-crawler access, structured retrieval hooks, prompt-mined content), prompt mining, mention strategy, robots.txt for GPTBot/ClaudeBot/PerplexityBot/CCBot/Google-Extended. WHEN NOT TO USE: snippet/position-zero extraction (maximus-aeo-optimization), content quality/keywords (maximus-content-seo), crawlability/speed (maximus-technical-seo), measuring existing citations (maximus-llm-visibility-tracking), AI-search roadmap (maximus-ai-seo-strategy)."
metadata:
  pillar: seo
  source: maximus
---

# Maximus — GEO Optimization

Generative engines don't rank pages, they synthesize answers. Getting cited inside that synthesized answer is a different game than getting a blue link on page one — this skill is how you play it.

## Purpose

GEO is the discipline of making your brand, product, and expertise show up *inside* the answers that Perplexity, Google AI Overviews, ChatGPT search, You.com, Bing Copilot, and Claude-with-web generate — as a cited source, a named brand, or a quoted fact. It is a surfacing problem, not an extraction problem: the content might already be well-structured for snippets and still never get pulled into a generated answer if the model doesn't trust the source, can't crawl it, or has never seen the brand mentioned anywhere else.

## GEO vs AEO vs SEO

| | Optimizes for | Unit of success |
|---|---|---|
| **SEO** | Ranking in a list of links | Position on the SERP |
| **AEO** | Being the answer, verbatim | Featured snippet / position zero |
| **GEO** | Being cited or named inside a generated answer | Citation, brand mention, or quote inside an LLM response |

SEO gets you *ranked*. AEO gets you *extracted*. GEO gets you *surfaced* — chosen by a generative model, from potentially thousands of candidate sources, as worth citing or naming. A page can rank well and even win snippets and still be invisible to GEO if the model has no independent signal that the brand or source is authoritative. Load `maximus-aeo-optimization` for the extraction half of this pair; this skill is the surfacing half.

## The 5 GEO levers

1. **Source-authority signals.** LLMs weight sources by signals that look a lot like old-school authority: citations from other reputable sites, consistent factual accuracy over time, clear authorship/expertise (author bios, credentials), and presence in the corpora the model actually trusts (Wikipedia, major trade press, .gov/.edu, well-known industry publications). Build these deliberately — don't assume good content alone earns trust.
2. **Brand-mention density on third-party sites.** Generative engines cross-reference. If your brand is mentioned favorably across independent sites — reviews, comparisons, forums, listicles — that co-occurrence is itself a ranking signal for retrieval and a trust signal for generation. Your own site mentioning your own product is worth far less than ten other domains doing it.
3. **LLM-crawler accessibility.** If GPTBot, ClaudeBot, PerplexityBot, and Google-Extended can't fetch your pages, you cannot be cited from them directly (you may still be cited via third-party mentions). Audit robots.txt deliberately — see the crawler directory below.
4. **Structured retrieval hooks.** Clear headings that match real questions, FAQ blocks, schema.org markup (Organization, Article, FAQPage, Product), and tight self-contained paragraphs make it easier for a retrieval system to chunk, embed, and re-surface your content accurately.
5. **Prompt-mined content.** Content written to directly answer the actual prompts buyers type into LLMs — not just the keywords they'd type into Google — has a much higher hit rate for being retrieved when those prompts are asked for real.

## Prompt mining workflow

Find out what your buyers actually ask generative engines before writing anything.

1. Collect real or plausible buyer prompts: sales call transcripts, support tickets, community/forum questions, "People also ask," Reddit/Quora threads in your category.
2. Run the candidate prompts through Perplexity, ChatGPT search, and Copilot yourself. Record which brands/sources get cited and which don't.
3. Cluster prompts by intent (comparison, "best X for Y," troubleshooting, definitional, pricing).
4. Map each cluster to a content asset that directly answers it, and to which third-party sites you'd want mentioning you when that cluster is asked.
5. Re-check the same prompts monthly — generative answers drift as models and indices update.

Full worked trace: `examples/prompt-mining-trace.md`.

## Third-party mention strategy

Since generative engines corroborate across sources, a mention plan matters as much as an owned-content plan:

- **Guest posts** on sites the target LLMs already trust and cite in your category.
- **Comparison/listicle inclusion** ("best tools for X") — write your own comparison content but also actively pitch inclusion in independently-run listicles.
- **Forum and Q&A answers** (Reddit, Quora, Stack Exchange, G2/Capterra reviews) where genuine, disclosed participation adds durable brand co-occurrence.
- **Digital PR / press mentions** that get picked up and re-syndicated — syndication multiplies co-occurrence across the corpus.

Never fabricate mentions or pay for undisclosed placements — generative engines and their training pipelines increasingly penalize detected link-schemes and sponsored-content spam, and it is bad practice regardless.

## robots.txt / allowlist for LLM crawlers

Default-blocking every AI crawler kills your GEO ceiling; default-allowing every crawler gives away training rights you may not intend to grant. Decide per-bot, deliberately. See `references/llm-crawler-directory.md` for the full table and `examples/robots-config-trace.md` for a worked audit. Minimal pattern:

```
User-agent: PerplexityBot
Allow: /

User-agent: GPTBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Disallow: /

Sitemap: https://example.com/sitemap.xml
```

## Content freshness signals

Generative engines favor recency for anything time-sensitive (pricing, versions, "best of" lists, statistics). Keep a visible last-updated date, update stats and pricing on a schedule, resubmit updated URLs in your sitemap with accurate `lastmod`, and prune or rewrite stale pages that no longer reflect reality — a wrong but well-optimized page can get you cited for the wrong reason.

## Anti-patterns

- **Blocking all LLM crawlers by default.** "Better safe than sorry" on robots.txt makes you invisible to direct citation — decide per-bot instead of reaching for a blanket `Disallow: /`.
- **Ignoring third-party mentions.** Optimizing only your own domain ignores the cross-referencing behavior that actually drives generative citation.
- **No prompt research.** Writing for search keywords without ever checking what buyers actually type into an LLM wastes the content budget on the wrong questions.
- **Chasing every crawler equally.** Not all bots serve the same purpose (training vs. live retrieval) — treat them differently, see the crawler directory.
- **One-time setup.** Robots.txt and prompt sets both go stale. Re-audit on a schedule, not once.

## Sibling skills

- `maximus-aeo-optimization` — extraction-side counterpart: winning featured snippets and direct answer boxes.
- `maximus-content-seo` — on-page content quality, keyword targeting, editorial standards.
- `maximus-technical-seo` — crawlability, indexing, site performance for traditional search engines.
- `maximus-llm-visibility-tracking` — measuring whether you are actually being cited, and by whom, over time.
- `maximus-ai-seo-strategy` — org-level roadmap, prioritization, and budget across the whole AI-search program.

## Output

A GEO plan should leave behind: a prompt-mining cluster map, a third-party mention target list, a decided (not default) robots.txt for LLM crawlers, and a freshness/re-audit cadence. Hand off measurement to `maximus-llm-visibility-tracking`.
