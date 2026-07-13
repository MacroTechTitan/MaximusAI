---
name: maximus-content-seo
description: "On-page/content SEO execution: title/H1 patterns, meta descriptions, URL structure, internal linking (hub-spoke, contextual, breadcrumbs), E-E-A-T signals (author bios, credentials, sources, original data), content refresh cadence, content pruning (kill/consolidate/redirect), semantic optimization (entity coverage, LSI terms). WHEN TO USE: user says 'on-page seo', 'content optimization', 'internal linking', 'content cluster', 'e-e-a-t', 'content refresh', 'content pruning', 'meta description', 'title tag', 'seo copywriting', or asks to optimize a page/post for ranking. WHEN NOT TO USE: LLM-citation formatting (use maximus-aeo-optimization), multi-market AI-search rollouts (use maximus-geo-optimization), crawlability/schema/Core Web Vitals (use maximus-technical-seo), portfolio-level keyword strategy before anything is written (use maximus-ai-seo-strategy), first-draft writing (use maximus-write-article), or whole-site health audits (use maximus-seo-audit)."
metadata:
  pillar: seo
  source: maximus
---

# Maximus — Content SEO

Rankings are won on the page, one element at a time: the title that earns the click, the heading that tells the crawler what the section is about, the link that tells it what else matters. This skill is the execution layer for on-page and content-level SEO — the concrete edits that turn a written page into one search engines trust and rank.

## Purpose

Take a page (new or existing) and make every on-page signal work: title, H1, meta description, URL, heading structure, internal links, E-E-A-T markers, and semantic coverage. This is tactical execution, not strategy — it assumes a topic and target query already exist (from `maximus-ai-seo-strategy`) and a draft already exists or is being written (`maximus-write-article`). It answers "is this specific page as strong as it can be," not "which pages should exist."

## On-page fundamentals

- **Title tag** — lead with the primary keyword or its natural phrasing, keep to ~50-60 characters so it doesn't truncate in the SERP, and make it distinct from every other title on the domain. One promise, not three.
- **H1** — matches the title's intent but doesn't have to be identical; write it for the human reading the page, not just the crawler. Exactly one H1 per page.
- **Meta description** — 140-155 characters, states the specific value the page delivers, includes the primary keyword naturally, and ends with a reason to click (not a cutoff sentence). Not a ranking factor directly, but it drives click-through, which is.
- **URL** — short, lowercase, hyphenated, keyword-relevant, stable once published. Changing a URL after it has ranked requires a 301 redirect (see pruning workflow) — avoid unless the consolidation payoff is clear.
- **Headings (H2/H3)** — one H2 per subtopic, matching the subtopic tree the page is supposed to cover; H3s break down a single H2 further, never skip a level. Headings are both a scanning aid for readers and a topic map for crawlers — treat them as the page's outline, not decoration.

Full field-by-field checklist: `references/on-page-checklist.md`.

## Internal linking model

Three link types, each doing a different job:

1. **Hub-spoke** — the hub page (broad, comprehensive) links to every spoke (narrow, specific); every spoke links back to the hub and sideways to 2-3 sibling spokes. This is the backbone structure from `maximus-ai-seo-strategy`'s cluster plan — this skill implements the actual `<a>` tags and anchor text.
2. **Contextual** — in-body links placed where a claim naturally needs supporting depth, using descriptive anchor text (never "click here" or "read more"). Add these during drafting or refresh, not as a bolted-on afterthought pass.
3. **Breadcrumbs** — a visible, structured trail (Home > Category > Page) that reinforces site hierarchy for both users and crawlers; pairs with `BreadcrumbList` schema, which is `maximus-technical-seo`'s territory to deploy.

A page with zero inbound internal links is an orphan — invisible to crawlers that discover pages by following links, and starved of the authority internal links pass. Every new page needs at least one contextual inbound link and one hub/spoke link before it ships. See `HOWTO.md` recipe (b) and `examples/internal-linking-trace.md` for the audit method.

## E-E-A-T signals

Google's Experience, Expertise, Authoritativeness, Trust framework is not a checkbox — it's the set of signals that separate a page a reader (and a ranking algorithm) trusts from one they don't:

- **Experience** — first-hand markers: "we tested," "in our benchmark," original screenshots, a named person who actually did the thing. Generic restated knowledge has no experience signal.
- **Expertise** — an author byline with real credentials relevant to the topic, not just a name; a bio page that establishes why this person can be trusted on this subject.
- **Authoritativeness** — citations to primary sources, original data or research, and recognition signals (other reputable sites linking in, mentions, quoted expertise).
- **Trust** — accurate, verifiable claims; visible publish/update dates; clear correction policy or contact info; no deceptive claims or unattributed statistics.

Build these into the page, don't bolt them on after. See `HOWTO.md` recipe (e) for retrofitting E-E-A-T onto pages that already rank but lack it.

## Content refresh workflow

Not every page needs a refresh, and refreshing the wrong ones wastes effort while stale winners keep decaying. Prioritize:

1. **Candidate selection** — pages that: rank positions 4-15 (movable, not stuck at #40 or already #1), show a traffic decline of 10%+ over the last 3-6 months, or contain facts/dates/pricing/versions that are now outdated.
2. **Diagnose why it's stale** — outdated facts, a competitor that shipped a more comprehensive page, search intent drift (the query now expects a different answer format), or simple content decay (thin by today's standard).
3. **What to change** — update every date-sensitive claim, add sections covering subtopics competitors now cover that this page doesn't, strengthen E-E-A-T (add/refresh author info, add original data if none existed), tighten the title/meta if CTR has dropped, add or repair internal links pointing in and out.
4. **What to preserve** — the URL (never change it on a refresh unless consolidating), the core structure if it's still winning, and any section still getting engagement.
5. **Ship and mark** — update the visible "last updated" date, and track ranking/traffic for 4-8 weeks post-refresh before deciding whether it worked.

Full worked example: `examples/content-refresh-trace.md`. Recipe: `HOWTO.md` (c).

## Content pruning workflow

Thin, outdated, or cannibalizing pages drag down a domain's overall quality signal. Triage every page into one of three buckets:

- **Kill (noindex or delete + redirect)** — near-zero traffic for 12+ months, no backlinks, no ranking potential, and no unique information not covered elsewhere.
- **Consolidate** — two or more pages compete for the same query (cannibalization) or each covers a fragment of a topic better handled as one comprehensive page; merge into the strongest URL, 301-redirect the others.
- **Redirect only** — a page has backlinks or residual traffic worth preserving but the content itself isn't worth keeping standalone; 301 to the best matching live page.

Never prune a page with meaningful backlinks without redirecting — that traffic and authority evaporates instead of transferring. Full workflow and decision tree: `HOWTO.md` recipe (d).

## Semantic optimization

Do this **after** E-E-A-T and structure are solid, not before — semantic breadth on a thin, untrustworthy page just produces a longer thin, untrustworthy page. Once the foundation is right:

- **Entity coverage** — name the related people, tools, standards, and concepts an expert would mention when discussing this topic; missing entities is a signal of shallow coverage.
- **LSI / related terms** — use the vocabulary a genuine expert uses (synonyms, adjacent terms, the terminology competitors' top-ranking pages use), not keyword variants stuffed for density. Pull these from top-ranking competitor pages and "people also ask" boxes, then write them in naturally.
- **Comprehensiveness check** — does the page answer every sub-question the topic implies, or does a reader have to leave to get the full picture? A page that keeps the reader satisfied on-page is the semantic-optimization goal, not a keyword count.

## Anti-patterns

- **Title-tag stuffing** — cramming multiple keywords into one title produces a truncated, spammy SERP snippet and rarely improves ranking; one clear promise beats three vague ones.
- **Orphan pages** — publishing a page with no inbound internal link; crawlers may never find it and it gets none of the site's internal authority.
- **Refreshing the wrong pages** — pouring effort into a page stuck on page 4 of results with no backlink profile, while an actual decaying page-1 winner rots untouched.
- **Ignoring E-E-A-T** — treating on-page SEO as purely mechanical (titles, headings, keywords) while shipping anonymous, uncredentialed, unsourced content that both readers and ranking systems distrust.
- **Over-pruning** — killing pages with real backlinks or long-tail traffic without redirecting, or consolidating pages that actually serve distinct intents, destroying accumulated authority for a "clean site" aesthetic.

## Sibling skills

- `maximus-aeo-optimization` — extraction-focused formatting (quotable claims, schema, FAQ blocks) for LLM/AI Overview citation; load once this skill's on-page foundation is solid and the goal shifts to being lifted verbatim, not just ranked.
- `maximus-geo-optimization` — generative engine optimization across multi-market/multi-language AI search surfaces; load when the content-SEO work spans more than one locale.
- `maximus-technical-seo` — crawlability, indexation, Core Web Vitals, and schema deployment at the site-architecture level; load when an on-page fix depends on a technical/infrastructure change.
- `maximus-ai-seo-strategy` — portfolio-level keyword research and cluster planning; load before this skill to decide which pages should exist and how they cluster, before optimizing any single page.
- `maximus-write-article` — first-draft long-form writing; load first when the content doesn't exist yet, then apply this skill to optimize the draft for on-page ranking signals.
- `maximus-seo-audit` — full-site health audits that surface which pages need this skill's refresh, pruning, or on-page fixes; load first when triaging a whole domain rather than a single page.
- `maximus-brain` — load for any multi-page or whole-domain content SEO program; the framing/recall/select/execute/critique loop keeps a large refresh or pruning pass from drifting.

## Output

Either an optimized page (title, H1, meta, URL, headings, internal links, E-E-A-T elements in place) or a structured plan document (refresh backlog, pruning decision list, internal-link-add plan) ready for execution — matching the recipe in `HOWTO.md` that was run.
