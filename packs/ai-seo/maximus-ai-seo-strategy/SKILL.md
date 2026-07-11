---
name: maximus-ai-seo-strategy
description: "Keyword research and topical strategy adapted for AI answer surfaces (Google AI Overviews, Perplexity, ChatGPT search, Claude, Gemini). Covers intent mapping, topical authority planning, query gap analysis, cluster planning, and prioritization frameworks. USE WHEN: the user says 'seo strategy', 'keyword research', 'topical authority', 'ai seo plan', 'content cluster', 'seo roadmap', 'intent mapping', 'query gap analysis', or needs a plan for what to write and why before producing content. This is the strategy layer that sits above tactics. DO NOT USE for on-page AEO markup or answer-snippet formatting (use maximus-aeo-optimization), for LLM-citation/GEO tuning of existing content (use maximus-geo-optimization), for technical crawl/indexation fixes (use maximus-content-seo), for auditing live pages (use maximus-seo-audit), for drafting the article itself (use maximus-write-article), or for rank-tracking dashboards (use maximus-seo-visibility-tracking)."
metadata:
  pillar: seo
  source: maximus
---

# Maximus — AI SEO Strategy

Tactics without strategy is motion without direction: perfect AEO markup on the wrong topic still loses. This skill is the layer that decides *what* to target and *why* before any page gets written or optimized — keyword research, topical authority planning, and cluster design, all re-weighted for a world where the answer is as often served by an AI Overview or a chat assistant as by a blue link.

## When to use

- Building a keyword research or content strategy for a site, product, or topic.
- Planning topical authority for a domain that wants to be the reference on a subject.
- Running a query gap analysis against competitors.
- Designing content clusters (hub + spoke) before writing anything.
- Prioritizing a backlog of content ideas with a defensible framework.
- The user says "seo strategy", "keyword research", "topical authority", "ai seo plan", "content cluster", "seo roadmap", "intent mapping", "query gap analysis".

## When not to use

- The strategy already exists and the task is implementing answer-format markup on a specific page — use `maximus-aeo-optimization`.
- The task is tuning existing content so LLMs cite it more often — use `maximus-geo-optimization`.
- The task is technical (crawlability, schema, Core Web Vitals, indexation) — use `maximus-content-seo`.
- The task is auditing pages already live — use `maximus-seo-audit`.
- The task is writing the actual article body — use `maximus-write-article`.
- The task is tracking rankings, citations, or visibility over time — use `maximus-seo-visibility-tracking`.

## Purpose: strategy above tactics

Every tactical SEO skill in this pack answers "how do I make this page better." This skill answers "which pages should exist, in what order, and what does winning look like." Get this layer wrong and the tactical skills just execute the wrong plan faster. The output of this skill is always a backlog or a plan document — never a finished page.

## The AI-first keyword model

Classic keyword research sorts by informational / navigational / transactional intent, then by volume. That model still applies but is incomplete for 2026 search behavior, where a growing share of queries never reach a results page — they get answered directly by an AI Overview, a Perplexity answer, or a chat assistant turn. Add a fourth category:

- **Informational** — "what is X", "how does X work". Classic top-of-funnel.
- **Navigational** — brand and product name lookups. Low strategic value unless defending a brand query.
- **Transactional** — "buy", "pricing", "best X for Y". Classic bottom-of-funnel.
- **Conversational / multi-turn** — the query a user would type into Perplexity, ChatGPT, or Claude as a follow-up in a dialogue, not a single search box term: "which of these is actually better for a 10-person team", "what would break if I switched providers". These queries are longer, more specific, and often compound two or three sub-questions. They rarely show up in Google Keyword Planner volume data because they were never typed into Google — they live in chat logs and "People also ask" expansions. Surface them by reading actual AI Overview boxes and Perplexity/ChatGPT answers for the seed topic, not just SERP tools.

A page built for AI answer surfaces needs to satisfy the conversational form of the query, not just the keyword-tool form of it. Treat every cluster as needing both: the searchable head term and the conversational tail it triggers.

## Topical authority planning

Search engines and AI answer engines both reward topical depth: a site that comprehensively covers a subject area gets treated as a more trustworthy source than one with a single strong page. Plan authority, not just pages:

1. Define the **topic boundary** — the subject area you are claiming, narrow enough to be coverable, broad enough to matter commercially.
2. Map the **subtopic tree** — every question a genuine expert would expect to be able to answer inside that boundary. Use `search_web` to pull "people also ask," AI Overview panels, and forum threads (Reddit, Quora, industry forums) as raw material.
3. Score **current coverage** — for each subtopic, does a page already exist on the domain? Is it strong, weak, or missing?
4. Sequence **build order** — foundational/definitional pages before advanced/edge-case pages; pages that other planned pages will need to link to come first.
5. Set an **authority milestone** — a concrete signal (e.g., "cited in an AI Overview for 5 of the top 20 subtopic queries," "ranks top 5 for the 3 highest-volume subtopics") that tells you the topic is "owned," not just "covered."

See `examples/topical-authority-trace.md` for a full worked plan.

## Query gap analysis workflow

1. Identify the 3 competitors who currently win the topic (rank top 3, or get cited most often in AI answers for the seed queries).
2. Pull each competitor's visible content inventory with `fetch_url` (sitemap, blog index, or category pages) and `search_web` (`site:` style queries work poorly for AI answer coverage — instead search the actual question and note who gets cited).
3. Build a subtopic-by-competitor matrix: rows are subtopics from the topical authority tree, columns are competitors, cells are "covered / not covered / covered but weak."
4. Gaps are subtopics no competitor covers well, or covers only shallowly. Gaps are the highest-leverage backlog items — they are winnable without displacing an entrenched page.
5. Also flag **overlap-but-beatable**: subtopics everyone covers but none covers well (thin, outdated, or not structured for AI extraction). These are second-priority.

## Cluster planning (hub + spoke)

- One **hub** page per subtopic tree: broad, comprehensive, the page you want to be the canonical answer for the category-defining query. Links out to every spoke.
- Ten (or so) **spoke** pages: each answers one narrow subtopic or conversational variant in depth. Links back to the hub and sideways to 2-3 sibling spokes.
- Internal linking is not optional decoration — it is how both classic crawlers and AI retrieval systems learn that the hub is the authoritative parent.
- A cluster is "done" when every spoke targets a distinct intent (no two spokes competing for the same query) and the hub can be summarized in one sentence that a competitor could not also claim.

See `examples/keyword-cluster-trace.md` for a full worked expansion from seed keyword to hub + spokes.

## Prioritization: volume x intent x difficulty x AI-citation potential

Raw search volume alone misprioritizes for AI answer surfaces, where a lower-volume conversational query with high citation potential can drive more durable value than a high-volume query already dominated by an entrenched competitor. Score every backlog item on four axes and take the weighted product, not the sum. Full rubric, weights, and a scoring template are in `references/prioritization-framework.md`.

## Anti-patterns

- **Chasing pure volume.** The highest-volume keyword in a space is usually the most contested and the least winnable. Volume without a realistic path to ranking or citation is a vanity metric.
- **Ignoring AEO/GEO potential.** A keyword strategy that only optimizes for blue-link rankings is planning for half the traffic. Every cluster plan should note which subtopics are likely to be answered directly by AI Overviews or chat assistants, and plan the page to win the citation, not just the click.
- **No clustering.** A flat list of disconnected keyword targets produces a flat list of disconnected pages. Neither search engines nor AI retrieval systems reward that structure. Cluster first, write second.
- **Skipping the gap analysis.** Prioritizing by internal opinion instead of competitor coverage data leads to building content nobody was missing.
- **Treating the plan as permanent.** Topical landscapes shift monthly as AI answer surfaces change what they cite. Revisit the plan on a cadence (see `HOWTO.md` recipe f), don't set it once a year.

## Sibling skills

- `maximus-aeo-optimization` — implements answer-engine-optimized formatting on a specific page once the strategy names the target query.
- `maximus-geo-optimization` — tunes existing content so LLMs cite it more often; works on pages this skill decided should exist.
- `maximus-content-seo` — technical and on-page SEO execution (schema, crawlability, internal linking mechanics) for pages in the plan.
- `maximus-seo-audit` — audits live pages against the plan this skill produced; feeds gaps back into the next planning cycle.
- `maximus-write-article` — drafts the actual page content once a cluster slot and target query are defined here.
- `maximus-seo-visibility-tracking` — measures whether the plan is working (rankings, AI citations) and feeds results back into the next prioritization pass.
- `maximus-brain` — load for any multi-step strategy build; the framing/recall/select/execute/critique loop applies directly to a 90-day plan.

## Output

A topical authority plan or keyword cluster backlog, written as a structured document (markdown or spreadsheet): subtopics, target queries (searchable + conversational), intent, priority score, cluster assignment (hub/spoke), and current coverage status. Never a finished article — hand off to `maximus-write-article` and the tactical skills for execution.
