# Worked example — robots.txt audit trace

**Scenario:** a mid-size B2B SaaS marketing site currently has a robots.txt that predates the AI-crawler era. Goal: audit it, decide per-bot policy, and produce a corrected file with rationale, following Recipe B in `HOWTO.md`.

## Step 1 — Starting robots.txt (as found)

```
User-agent: *
Disallow: /admin/
Disallow: /internal/

Sitemap: https://example.com/sitemap.xml
```

**Audit finding:** no AI-crawler-specific blocks exist at all. Because the wildcard block only disallows `/admin/` and `/internal/`, every LLM crawler that respects the `User-agent: *` block is implicitly allowed everywhere else — but many AI crawlers do not reliably honor the wildcard block and require their own explicit line, so this file is ambiguous rather than deliberate ([Priso's AI-bot robots.txt reference](https://priso.nl/en/blog/ai-bots-robots-txt-allow-or-block)). This is the "default by accident" state the anti-patterns section in `SKILL.md` warns against.

## Step 2 — Classify each relevant bot

Using `references/llm-crawler-directory.md`:

| Bot | Function | Site's goal |
|---|---|---|
| `GPTBot` | OpenAI training crawler | Business wants ChatGPT citations but is undecided on training — leans allow, revisit in 6 months |
| `OAI-SearchBot` | ChatGPT Search retrieval/indexing | Want citations — allow |
| `ChatGPT-User` | ChatGPT live fetch during a user chat | Want citations — allow |
| `ClaudeBot` | Anthropic training crawler | Same undecided-training stance as GPTBot — allow |
| `Claude-SearchBot` | Claude.ai web-search retrieval | Want citations — allow |
| `Claude-User` | Claude live fetch during a chat | Want citations — allow |
| `PerplexityBot` | Perplexity's primary indexing crawler | Perplexity is a named priority channel for this business — allow |
| `Perplexity-User` | Perplexity live fetch during a query | Allow |
| `Google-Extended` | Gemini/Vertex AI training (separate from classic Googlebot) | Same undecided-training stance — allow, since blocking it does not affect classic Google Search ranking |
| `CCBot` | Common Crawl, feeds many third-party model training sets | No direct citation benefit and broad reuse beyond the business's control — block |
| `Bytespider` | ByteDance/TikTok AI crawler | Documented history of ignoring robots.txt; block as a matter of policy even though enforcement isn't guaranteed | 
| `Applebot-Extended` | Apple Intelligence training signal (does not affect Siri/Spotlight indexing, which uses classic `Applebot`) | Undecided training stance — allow |
| `Amazonbot` | Amazon's crawler, used for Alexa and AI training | No clear citation channel for this business today — block, revisit if Alexa+ becomes relevant |

**Rationale pattern applied:** allow retrieval/citation bots by default (they drive visibility in the actual product this skill targets); make training bots a deliberate business call rather than an accident; block bots with no citation upside and a track record of non-compliance.

## Step 3 — Path-level carve-outs

The business has a gated `/reports/` directory (paywalled research) and a `/app/` directory (the logged-in product). Both should stay out of any crawler's reach, AI or not:

```
Disallow: /app/
Disallow: /reports/
```

These lines apply under `User-agent: *` and are also worth repeating under the specific AI bots that are otherwise allowed everywhere, since some AI crawlers only respect their own explicit block list.

## Step 4 — Final robots.txt

```
User-agent: *
Disallow: /admin/
Disallow: /internal/
Disallow: /app/
Disallow: /reports/

User-agent: GPTBot
Allow: /
Disallow: /app/
Disallow: /reports/

User-agent: OAI-SearchBot
Allow: /
Disallow: /app/
Disallow: /reports/

User-agent: ChatGPT-User
Allow: /
Disallow: /app/
Disallow: /reports/

User-agent: ClaudeBot
Allow: /
Disallow: /app/
Disallow: /reports/

User-agent: Claude-SearchBot
Allow: /
Disallow: /app/
Disallow: /reports/

User-agent: Claude-User
Allow: /
Disallow: /app/
Disallow: /reports/

User-agent: PerplexityBot
Allow: /
Disallow: /app/
Disallow: /reports/

User-agent: Perplexity-User
Allow: /
Disallow: /app/
Disallow: /reports/

User-agent: Google-Extended
Allow: /
Disallow: /app/
Disallow: /reports/

User-agent: Applebot-Extended
Allow: /
Disallow: /app/
Disallow: /reports/

User-agent: CCBot
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: Amazonbot
Disallow: /

Sitemap: https://example.com/sitemap.xml
```

## Step 5 — Rationale summary (what to tell stakeholders)

- Retrieval/citation bots (search-indexing and live-fetch variants of GPT, Claude, Perplexity) are allowed everywhere except the gated app and paid reports — this is the direct lever for GEO citations.
- Training-only bots (`GPTBot`, `ClaudeBot`, `Google-Extended`, `Applebot-Extended`) are allowed under a deliberate policy: the business is comfortable with model-training inclusion for now and will revisit annually. This line item should be reviewed with legal/brand stakeholders, not just SEO.
- `CCBot`, `Bytespider`, and `Amazonbot` are blocked because they offer no direct citation channel for this business today and (`Bytespider` specifically) have a documented history of poor robots.txt compliance ([Priso's AI-bot robots.txt reference](https://priso.nl/en/blog/ai-bots-robots-txt-allow-or-block)).
- Robots.txt is a request, not an enforcement mechanism — bots that don't comply need server-level controls (Cloudflare WAF AI-scraper rules, platform firewall rules, or rate limiting), which is a follow-up item for the infra team, not something this file can guarantee on its own.

## Step 6 — Validation checklist

- Each `User-agent` line is followed only by `Allow`/`Disallow`/`Sitemap` directives, with a blank line separating blocks — valid per the robots.txt spec.
- No bot has conflicting directives (an `Allow: /` above a more specific `Disallow:` in the same block is fine — the most specific path wins).
- The sitemap URL resolves and returns 200.
- Re-fetch and diff this file quarterly — new crawlers appear often enough that a stale file drifts back into "default by accident."
