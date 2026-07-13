# maximus-ai-seo-strategy

## What

Keyword research and topical strategy adapted for a search landscape where AI Overviews, Perplexity, ChatGPT search, Claude, and Gemini answer a growing share of queries directly. This skill produces the plan — intent-mapped keyword sets, topical authority trees, query gap analyses, hub-and-spoke cluster designs, and a prioritized backlog — that the tactical SEO skills in this pack then execute against.

It is the strategy layer of the `maximus-seo-pack`. It does not write pages, mark up pages, or audit pages. It decides which pages should exist, in what order, and what "winning" looks like for each.

## When to use

- Starting a new content program for a site, product line, or topic and need a plan before writing anything.
- Building topical authority for a domain that wants to be treated as the reference source on a subject.
- Comparing your content coverage against 2-3 competitors to find winnable gaps.
- Designing a content cluster (hub + spokes) before handing pages to a writer.
- Prioritizing a large backlog of content ideas with a defensible, repeatable scoring method.
- Running a periodic (monthly/quarterly) strategy review as the topical landscape shifts.

## When not to use

- Implementing answer-engine markup on a specific page — use `maximus-aeo-optimization`.
- Tuning existing content so LLMs cite it more often — use `maximus-geo-optimization`.
- Technical/on-page execution (schema, crawlability, internal linking mechanics) — use `maximus-content-seo`.
- Auditing pages already live against the plan — use `maximus-seo-audit`.
- Drafting the actual article — use `maximus-write-article`.
- Tracking rankings or AI citation rates over time — use `maximus-seo-visibility-tracking`.

## Example

**Prompt:** "We sell vendor management SaaS. Build me a 90-day topical authority plan and a first content cluster."

**What this skill does:**
1. Defines the topic boundary ("vendor management for mid-market procurement teams") and maps the subtopic tree using `search_web` against AI Overview panels, "people also ask" data, and forum discussion.
2. Runs a query gap analysis against the 3 competitors currently winning the topic's key queries.
3. Scores every candidate subtopic on volume x intent x difficulty x AI-citation potential (see `references/prioritization-framework.md`).
4. Designs the first hub + 10-spoke cluster from the highest-priority subtopic.
5. Delivers a structured backlog document and hands off cluster slots to `maximus-write-article` for drafting and to `maximus-aeo-optimization` / `maximus-geo-optimization` for the tactical pass.

See `examples/topical-authority-trace.md` and `examples/keyword-cluster-trace.md` for full worked traces.

## Related skills

- `maximus-aeo-optimization` — tactical answer-engine formatting once a target query is set here.
- `maximus-geo-optimization` — tuning content for LLM citation frequency.
- `maximus-content-seo` — technical and on-page SEO execution.
- `maximus-seo-audit` — audits live pages against this plan.
- `maximus-write-article` — drafts the content this skill scopes.
- `maximus-seo-visibility-tracking` — measures whether the plan is working.
- `maximus-brain` — general think-before-act loop; useful for any multi-step strategy build.

## Files

- `SKILL.md` — full skill definition and triggers.
- `HOWTO.md` — six step-by-step recipes.
- `examples/topical-authority-trace.md` — worked topical authority plan.
- `examples/keyword-cluster-trace.md` — worked keyword expansion and cluster design.
- `references/prioritization-framework.md` — scoring rubric, weights, template, tie-breakers.
