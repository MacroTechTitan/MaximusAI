# HOWTO — Maximus Content SEO

Six recipes for the jobs this skill handles most often. Each recipe names the tools to use, the order to use them in, and what "done" looks like.

## (a) Optimize a new blog post before publishing

1. **Confirm the target.** Get the primary keyword/query and the intent (informational, transactional, comparison) from the brief or from `maximus-ai-seo-strategy`'s cluster plan. If neither exists, don't guess — ask which subtopic slot this post fills.
2. **Title tag.** Write 3 candidates using the formulas in `references/on-page-checklist.md`. Pick the one that leads with the keyword phrasing closest to how the target query is actually typed, keep it ≤60 characters.
3. **H1.** Distinct from the title (not a copy-paste), matches the reader's intent, exactly one per page.
4. **Meta description.** 140-155 characters, states the specific value delivered, ends on a reason to click. Draft with `write`, don't leave the CMS default.
5. **URL slug.** Short, hyphenated, keyword-relevant, lowercase. Lock it now — this is the last easy point to change it before backlinks and indexing make it costly.
6. **Heading structure.** Read the draft (`read`) and check every H2 maps to a distinct subtopic; no heading level skipped; no duplicate H2 phrasing.
7. **Internal links.** Add at least one hub/spoke link (up to the hub or down to a sibling spoke) and at least one contextual in-body link with descriptive anchor text. Confirm at least one other live page will link back in — if not, add that link now on the linking page too (see recipe b for the orphan check).
8. **Images.** Every image gets descriptive alt text following `references/on-page-checklist.md` patterns; filenames are descriptive, not `IMG_4821.jpg`.
9. **E-E-A-T pass.** Author byline with real credentials present; at least one first-hand marker ("we tested," an original screenshot, a named source) if the topic calls for experience; citations for any external claim or statistic.
10. **Final check.** Re-read the rendered preview once, title/meta/H1 in front of you together — do they tell a consistent, non-redundant story? Ship.

## (b) Internal linking audit and fix

1. **Inventory.** Pull every published URL (sitemap via `fetch_url`, or CMS export). Build a simple table: URL, page type (hub/spoke/standalone), inbound link count, outbound link count.
2. **Find orphans.** Any page with zero inbound internal links is an orphan. Flag every one — these are invisible to crawlers that discover pages by following links.
3. **Map hub-spoke gaps.** For each cluster, confirm the hub links to every spoke and every spoke links back. Missing links in either direction are gaps, not just style issues.
4. **Check anchor text quality.** Grep the site export for generic anchors ("click here," "read more," "this article") and replace with descriptive text naming the destination page's topic.
5. **Prioritize fixes.** Orphans first (biggest crawl-discovery risk), then hub-spoke gaps (biggest authority-flow risk), then anchor text cleanup (smallest but easiest wins).
6. **Produce the link-add plan.** A table: source page, target page, anchor text, link type (hub/spoke/contextual). Hand off for implementation.
7. **Re-crawl and confirm.** After links are added, re-pull the sitemap/crawl and confirm the orphan list is empty.

Full worked example: `examples/internal-linking-trace.md`.

## (c) Content refresh workflow for a stale-but-ranking page

1. **Confirm it's a refresh candidate, not a pruning candidate.** Ranking positions 4-15, meaningful existing traffic, and a real decline (10%+ over 3-6 months) or visibly outdated facts. If traffic is near zero and it never ranked well, this is a pruning candidate instead (recipe d).
2. **Diagnose the cause.** Pull the page (`fetch_url`) and check: outdated dates/prices/versions, missing subtopics competitors now cover (`search_web` the target query and read the top 3 results), thin E-E-A-T (no author, no sources), or intent drift (the query now expects a different format, e.g., a list instead of an essay).
3. **Update facts first.** Every date-sensitive claim gets checked and corrected before anything else — a beautifully restructured page with a wrong statistic still fails trust.
4. **Fill coverage gaps.** Add sections for subtopics the diagnosis surfaced as missing; don't pad unrelated sections.
5. **Strengthen E-E-A-T.** Add or update the author byline, add a first-hand data point or test result if the topic supports one, refresh citations.
6. **Re-check title/meta.** If click-through has dropped, this is the moment to also test a new title/meta — but don't change the URL.
7. **Ship and mark the date.** Update the visible "last updated" timestamp. Track ranking and traffic for 4-8 weeks before judging the refresh's effect.

Full worked example with before/after diffs: `examples/content-refresh-trace.md`.

## (d) Content pruning audit — identify kill/consolidate/redirect candidates

1. **Pull the full inventory** with traffic, ranking, and backlink data per URL (from analytics/Search Console export or `maximus-seo-audit`'s output if one already exists).
2. **Sort into buckets:**
   - **Kill** — 12+ months near-zero traffic, no backlinks, no unique information not covered elsewhere on the domain.
   - **Consolidate** — two or more pages compete for the same query (cannibalization) or fragment one topic across several thin pages.
   - **Redirect only** — meaningful backlinks or residual long-tail traffic, but the content itself isn't worth keeping standalone.
   - **Keep as-is** — everything else; don't touch pages that are simply low-priority, only ones that are actively harmful or redundant.
3. **For consolidation candidates**, pick the strongest surviving URL (best current ranking, most backlinks, or most comprehensive) and note what content from the losing page(s) must be merged in before redirecting.
4. **For kill candidates**, confirm zero backlinks one more time before deleting — a backlink means redirect, not delete.
5. **Produce the decision list**: URL, bucket, target URL if consolidating/redirecting, one-line reason.
6. **Execute in order:** redirects and consolidations before deletions, so nothing goes dark before its replacement is live.
7. **Monitor.** Check crawl stats and rankings for the surviving/target pages 4-6 weeks after execution to confirm no unintended traffic loss.

## (e) Building E-E-A-T signals on existing pages

1. **Inventory current state.** For each page: is there a named author with a bio? Are there credentials relevant to the topic? Are external claims cited? Is there any first-hand experience marker?
2. **Prioritize by topic sensitivity.** Health, finance, legal, and safety content ("YMYL" — your money or your life) needs the strongest E-E-A-T; general how-to content needs it but with lower urgency.
3. **Add author infrastructure once, reuse everywhere.** Build (or request) a real author bio page with credentials, then attribute every relevant post to that author instead of "Admin" or no byline.
4. **Inject experience markers.** Where the topic allows, add a first-hand data point: a screenshot from an actual test, a specific result ("we ran this for 30 days and saw X"), a named example instead of a generic one.
5. **Source every external claim.** Any statistic, quote, or "studies show" needs a link to the primary source, checked with `fetch_url` before citing — never cite a source you haven't actually opened.
6. **Add trust infrastructure.** Visible publish and last-updated dates on every page; a contact/about page that isn't a dead end.
7. **Re-audit after a batch.** Confirm the changes actually shipped (byline visible, dates visible, links resolve) before moving to the next batch of pages.

## (f) Writing a title tag and meta description that converts

1. **Read the top 3 ranking pages** for the target query (`search_web`, then `fetch_url` each) — not to copy, but to see what promise is already being made so this page's title makes a different or sharper one.
2. **Draft 3 title candidates** using the formulas in `references/on-page-checklist.md`: direct-match, benefit-led, and specificity-led (number, year, or named method).
3. **Check length and truncation.** ≤60 characters for the title, 140-155 for the meta description; paste into a SERP-preview tool or just count characters — don't guess.
4. **Meta description states the specific payoff**, not a restatement of the title — it should answer "why click this one over the other nine blue links."
5. **Avoid the generic trap.** No "everything you need to know about X" or "the ultimate guide to X" unless the page can prove it's genuinely the most complete one live today.
6. **Pick one, ship, and note the alternates.** Keep the two rejected candidates in the page's notes — they're the first thing to test if CTR underperforms after a few weeks of Search Console data.
