# HOWTO — maximus-ai-seo-strategy

Six recipes. Each assumes access to `search_web`, `fetch_url`, and `memory_search`. Where a step says "search," use `search_web` with short natural-language queries (2-3 per batch, per the tool's guidance) rather than one long compound query.

## Recipe A — Build a 90-day topical authority plan

1. **Bound the topic.** Write one sentence defining what you are claiming authority over and for whom. Narrow enough to cover in 90 days, broad enough to matter commercially. Check `memory_search` for prior planning work on this domain before starting from zero.
2. **Map the subtopic tree.** Run 3-5 `search_web` queries against the seed topic and its obvious sub-questions. Pull "people also ask" boxes, AI Overview panel headers, and the question threads on Reddit/Quora/industry forums. Build a flat list, then group into 4-8 subtopic branches.
3. **Score current coverage.** For each subtopic, check whether the domain already has a page (search `site:domain.com subtopic` or check the sitemap via `fetch_url`). Mark: strong / weak / missing.
4. **Sequence the build order.** Foundational/definitional subtopics first (other pages will link to them), then supporting, then advanced/edge-case. Missing + high-priority subtopics go first regardless of tier if they're gap-analysis winners (Recipe D).
5. **Lay out the 90 days.** Three 30-day blocks: block 1 = hub pages and foundational spokes, block 2 = remaining spokes, block 3 = advanced/edge-case pages plus first refresh pass on block-1 pages based on early performance signal.
6. **Set the authority milestone.** One concrete, checkable signal for "this topic is owned" by day 90 (e.g., "cited in AI Overviews for 5 of the top 20 subtopic queries" or "top-5 ranking for the 3 highest-volume subtopics"). Write it down before you start; it's the finish line, not a retrospective guess.
7. **Save the plan** as a structured document (subtopic, page type hub/spoke, target query, intent, coverage status, priority score, target block). Hand blocks to `maximus-write-article` in sequence.

Full worked example: `examples/topical-authority-trace.md`.

## Recipe B — Keyword research adapted for AI answer engines

1. **Start with the seed keyword** as you would classically — the head term a user would type into a search box.
2. **Expand with a keyword tool proxy.** Since this skill has no direct keyword-volume API, use `search_web` on the seed term and read the related-searches / "people also ask" data returned in results, plus autocomplete-style suggestions surfaced in AI Overview boxes.
3. **Read actual AI answers, not just SERPs.** Search the seed term and 3-4 obvious variants, then read what the AI Overview / featured answer actually says. Note every sub-question it addresses — these are conversational-intent queries that never show up in traditional volume tools.
4. **Classify each keyword** into informational / navigational / transactional / conversational (see SKILL.md's AI-first keyword model). Conversational queries are usually longer and compound 2-3 sub-asks — keep them intact rather than splitting them into single keywords, because the page needs to answer the compound form.
5. **Tag AI-citation potential.** For each keyword, note whether an AI Overview or chat-assistant answer currently appears for it, and whether the citation is a source you could realistically become. High-citation-potential + currently-weak-source = high-value target.
6. **Output a keyword table**: keyword, intent, estimated volume tier (high/med/low, since exact volume isn't reliably available), AI-citation potential (high/med/low), notes on the conversational variant.

## Recipe C — Content cluster design (hub + 10 spokes)

1. **Pick the hub subtopic** — the broadest, most category-defining query in the cluster. This is the page you want cited as the canonical answer.
2. **Draft the hub's one-sentence claim** — what this page will be the definitive source for, phrased so a competitor could not credibly claim the same sentence about their version.
3. **List 10 spoke candidates** — narrower subtopics or conversational variants that a comprehensive treatment of the hub topic would need to cover. Pull these from the subtopic tree (Recipe A) or fresh `search_web` expansion of the hub query.
4. **Deduplicate intent.** Check that no two spokes are actually competing for the same query — if two overlap, merge them or split by a genuine distinction (e.g., by company size, by use case, by "how" vs "why").
5. **Assign internal links.** Every spoke links to the hub. Each spoke also links to 2-3 sibling spokes with genuinely related content — not a link farm, an actual reading path.
6. **Sanity-check coverage.** Would a genuine expert reading only the hub + 10 spokes feel the subject was fully covered? If there's an obvious missing angle, add an 11th spoke rather than force it into an existing one.

Full worked example: `examples/keyword-cluster-trace.md`.

## Recipe D — Query gap analysis vs top 3 competitors

1. **Identify the top 3 competitors** for the topic — the ones ranking top 3 or getting cited most often in AI answers for your seed queries. Confirm with 2-3 `search_web` queries on the highest-value seed terms; note who shows up in the AI Overview / cited-sources list, not just the blue-link ranking.
2. **Pull each competitor's content inventory.** Use `fetch_url` on their sitemap.xml or blog/resource index. If no sitemap, use `fetch_url` on their category or hub pages and follow the visible link structure.
3. **Build the subtopic x competitor matrix.** Rows = subtopics from your topical tree. Columns = each competitor + you. Cells = covered-strong / covered-weak / not covered.
4. **Flag pure gaps** — subtopics none of the 3 competitors cover well. These are top-priority backlog items: winnable without displacing an entrenched page.
5. **Flag overlap-but-beatable** — subtopics everyone covers, but shallowly, with outdated data, or not structured for AI extraction (no clear direct-answer paragraph, no defined terms, no comparison table). Second-priority.
6. **Flag defended territory** — subtopics one competitor covers deeply and recently. Deprioritize unless you have a genuinely differentiated angle.
7. **Feed the matrix into prioritization** (Recipe E) — gap status is one input to the AI-citation-potential score.

## Recipe E — Prioritization scoring template

1. **List every backlog candidate** — one row per subtopic/query from Recipes A-D.
2. **Score four axes per `references/prioritization-framework.md`**: volume tier, intent value, difficulty, AI-citation potential. Use the 1-5 scale defined there for each.
3. **Compute the weighted score** using the formula and weights in the reference file — it's a weighted product, not a sum, so a zero on any axis meaningfully drags the score down.
4. **Apply tie-breakers** (freshness of competitor content, internal linking leverage, business-priority override) when scores land within 1 point of each other.
5. **Sort and cut the backlog** into the current planning block (see Recipe A step 5) rather than trying to sequence the entire list at once — re-score every cycle since the landscape shifts.
6. **Save the scored backlog** as the canonical planning artifact for the cycle; this is what `maximus-write-article` and the tactical skills pull their queue from.

## Recipe F — Monthly strategy review cadence

1. **Pull visibility data** from `maximus-seo-visibility-tracking` output (rankings, AI citation counts) for pages shipped in the last cycle.
2. **Re-run a light gap check** (abbreviated Recipe D) on the 3-5 highest-priority subtopics — has a competitor shipped something new? Has an AI Overview format changed?
3. **Re-score anything that moved.** Difficulty and AI-citation potential are the axes most likely to shift month to month; volume and intent are more stable.
4. **Retire or merge dead backlog items** — subtopics that got answered adequately by a shipped page, or that turned out to be duplicates of another cluster.
5. **Add newly surfaced subtopics** from search trend shifts, new competitor content, or product changes on your own side.
6. **Re-issue the prioritized backlog** for the next block. Note explicitly what changed and why, so the next cycle's reviewer isn't re-deriving the same reasoning.
