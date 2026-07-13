---
name: maximus-seo-audit
description: "End-to-end site audit combining technical, content, backlink, and AI-visibility dimensions into a single prioritized fix list. USE WHEN: the user says 'seo audit', 'site audit', 'full seo review', 'technical audit', 'content audit', 'backlink audit', 'ai visibility audit', 'diagnose seo problems', or asks why a site's traffic or rankings dropped and needs a holistic diagnosis. This is the umbrella skill that orchestrates the other SEO skills as building blocks and outputs a sequenced action plan, not a raw data export. DO NOT USE for executing a single fix once diagnosed (use the relevant tactical skill directly: maximus-technical-seo, maximus-content-seo, maximus-aeo-optimization, maximus-geo-optimization), for ongoing rank/citation tracking with no audit event (use maximus-llm-visibility-tracking), or for upfront keyword/topical strategy before any pages exist (use maximus-ai-seo-strategy)."
metadata:
  pillar: seo
  source: maximus
---

# Maximus — SEO Audit

An audit that hands back a spreadsheet of 400 issues is not a deliverable, it is homework assigned to someone else. This skill exists to turn a sprawling technical, content, backlink, and AI-visibility investigation into the five or six things a team should actually do this quarter, in the order that matters.

## When to use

- Running a full site audit spanning technical, content, backlink, and AI-visibility health.
- Diagnosing a traffic, ranking, or AI-citation drop when the cause is unknown and could span multiple dimensions.
- The user says "seo audit", "site audit", "full seo review", "technical audit", "content audit", "backlink audit", "ai visibility audit", or "diagnose seo problems".
- Auditing a competitor's site to learn what is working for them before building an own-site strategy.
- Running a post-migration check to confirm a redesign, replatform, or domain move didn't break SEO equity.

## When not to use

- The diagnosis is already done and the task is executing a single fix — go straight to `maximus-technical-seo`, `maximus-content-seo`, `maximus-aeo-optimization`, or `maximus-geo-optimization`.
- The task is ongoing rank or AI-citation tracking with no audit event triggering it — use `maximus-llm-visibility-tracking`.
- The task is upfront keyword or topical planning before any pages exist — use `maximus-ai-seo-strategy`.

## Purpose: a prioritized fix list, not a data dump

Every audit tool on the market is excellent at finding issues and terrible at telling you which ones matter. Screaming Frog will happily report 12,000 warnings on a 10,000-URL site. None of that is useful until it is triaged. The output of this skill is never a raw crawl export — it is always a ranked, sequenced list of fixes with an owner-ready rationale for why each one is worth doing before the next. If the deliverable looks like a data dump, the audit isn't finished.

## The 4 audit dimensions

A complete audit covers four dimensions. Skipping one produces a diagnosis that misses the actual cause of a traffic or visibility problem.

1. **Technical** — crawlability, indexation, Core Web Vitals, site architecture, schema, mobile rendering, redirect chains, canonicalization. Execute with `maximus-technical-seo`.
2. **Content** — thin/duplicate/outdated pages, keyword cannibalization, on-page optimization gaps, internal linking, content decay. Execute with `maximus-content-seo`.
3. **Backlink** — link profile health, toxic/spam links, lost links, competitor link gaps, anchor text distribution. Execute with the backlink-analysis workflows inside `maximus-technical-seo` and `maximus-ai-seo-strategy` (competitor gap methodology), pulling raw link data from Ahrefs/Semrush/GSC.
4. **AI-Visibility** — whether the site is cited by AI Overviews, Perplexity, ChatGPT, Claude, and Gemini for its target queries; whether pages are structured for extraction. Execute with `maximus-aeo-optimization` (on-page answer formatting), `maximus-geo-optimization` (citation tuning), and `maximus-llm-visibility-tracking` (measurement).

This skill does not replace those four; it schedules them, collects their outputs, and cross-weighs findings across all four so a technical fix and a content fix competing for the same sprint slot get compared on the same scale.

## The 6-phase audit workflow

1. **Scope** — define the audit boundary: whole domain or a subsection, which of the 4 dimensions are in scope, site size, business goals (traffic, leads, AI citations), and the audit's deadline. Scope determines how much of phases 2-3 are feasible.
2. **Crawl** — run a technical crawl (Screaming Frog, Sitebulb, or a lightweight `fetch_url`-based crawl for small sites) to establish the URL inventory, status codes, and architecture map before anything else. Nothing downstream is trustworthy without a clean crawl.
3. **Data collection** — pull the dimension-specific data: Core Web Vitals from PageSpeed Insights/CrUX, indexation and query data from GSC, link data from Ahrefs/Semrush, AI citation checks via `maximus-llm-visibility-tracking` or manual prompts against the major assistants.
4. **Analysis** — run each dataset through the relevant sibling skill's diagnostic lens. Technical issues through `maximus-technical-seo`, content issues through `maximus-content-seo`, AI-visibility issues through `maximus-aeo-optimization`/`maximus-geo-optimization`. Tag every finding with dimension, affected URL count, and estimated severity.
5. **Prioritization** — score every finding on impact x effort x urgency (see below) and sequence into a roadmap. This is the phase most audits skip or shortcut — it is the one that makes the audit useful.
6. **Report** — produce the executive summary + critical fixes + warnings + long-term recommendations structure below. Schedule the follow-up checkpoint before delivering; an audit with no re-check date is a one-time event, not a process.

## Prioritization framework: impact x effort x urgency

Score every finding 1-5 on three axes and take the weighted product (not the sum — a high-impact, low-effort fix should visibly outrank a merely additive score):

- **Impact** — how much organic traffic, conversion, or AI-citation share is at stake. Weight by affected URL count and by whether the page/section drives revenue.
- **Effort** — engineering or content hours to fix, and how many teams must sign off. Low effort means one owner, one deploy.
- **Urgency** — is the issue actively decaying (traffic dropping now), a blocker for other fixes (e.g., broken crawl budget blocking indexation of new content), or stable-but-suboptimal.

`Priority score = Impact x Urgency / Effort`. Sort descending. Anything scoring in the top decile is a critical fix; mid-range is a warning; low-impact/high-effort items go to the long-term backlog. Full worked scoring template in `references/audit-checklist-master.md` and a full worked example in `examples/prioritization-trace.md`.

## Report structure

1. **Executive summary** — 3-5 sentences: overall site health, the single biggest lever, and the expected outcome if the top 3 fixes ship.
2. **Critical fixes** — top-decile priority score items. Each gets: finding, affected URLs/pages, dimension, estimated impact, effort estimate, owner recommendation.
3. **Warnings** — mid-priority items worth scheduling but not blocking. Grouped by dimension.
4. **Long-term recommendations** — structural or strategic items (e.g., "rebuild the topical cluster around X" — hand off to `maximus-ai-seo-strategy`) that don't fit a single sprint.

## Tools stack

- **Crawl**: Screaming Frog (small-to-mid sites, desktop) or Sitebulb (visual architecture reports) for the primary crawl. Both export the URL inventory, status codes, and internal-link graph that phase 4 (Analysis) depends on.
- **Backlinks and competitor data**: Ahrefs or Semrush for link profile health, toxic-link flags, and competitor gap analysis.
- **Indexation and query data**: Google Search Console for coverage reports, query-level performance, and manual-action notices.
- **Performance**: PageSpeed Insights and CrUX for Core Web Vitals, both lab and field data.
- **Lightweight audits**: for a small site or a rapid-turnaround engagement where enterprise tooling isn't available or justified, `search_web` and `fetch_url` substitute for a manual crawl — fetch the sitemap, walk the URL list, and spot-check status codes, titles, and headings directly. This trades completeness for speed; see `HOWTO.md` recipe (a) for the full workflow and its limits.
- **AI visibility**: direct prompts against Perplexity, ChatGPT, Claude, and Gemini for the target query set, plus `maximus-llm-visibility-tracking` for a repeatable measurement harness.

## Anti-patterns

- **Data dump reports.** A 40-tab spreadsheet with no ranking is not an audit deliverable — see Purpose above.
- **No prioritization.** Listing findings in the order the crawler found them instead of by impact x effort x urgency.
- **Ignoring AI visibility.** An audit that only checks classic crawlability and ignores whether AI Overviews and chat assistants cite the site is auditing half of today's traffic sources.
- **One-time audits with no follow-up.** An audit with no re-check date or tracking hookup (`maximus-llm-visibility-tracking`) measures nothing after the report is delivered.

## Cadence: an audit is a process, not an event

Schedule the re-check before delivering the report. A quarterly cadence suits most sites; a monthly cadence suits sites in active recovery from a penalty, migration, or traffic drop. Feed the fix list's critical items into `maximus-llm-visibility-tracking` and the relevant tactical skill's own tracking so the next audit starts from "did the fixes work" instead of re-discovering the same issues.

## Sibling skills

- `maximus-technical-seo` — executes the technical dimension: crawlability, indexation, Core Web Vitals, schema, site architecture, redirect and canonicalization fixes. This audit schedules its diagnostics in phase 4 and hands off technical critical fixes to it directly.
- `maximus-content-seo` — executes the content dimension: thin/duplicate content, keyword cannibalization, on-page optimization, internal linking, content decay. This audit's content findings become that skill's work queue.
- `maximus-aeo-optimization` — executes AI-visibility formatting fixes (answer-shaped structure, extractable summaries) on specific pages once the audit flags them as under-formatted for AI Overviews and chat assistants.
- `maximus-geo-optimization` — executes citation-tuning fixes for pages the audit finds are under-cited by LLMs relative to their topical relevance.
- `maximus-llm-visibility-tracking` — the measurement layer that confirms whether audit fixes actually moved AI citation rates; also supplies the AI-visibility data this audit consumes in phase 3.
- `maximus-ai-seo-strategy` — the strategy layer upstream; this audit's structural and coverage gaps feed back into the next planning cycle there, and its topical plan defines what "good coverage" should look like when this audit checks content completeness.

## Output

A prioritized fix list document: executive summary, critical fixes, warnings, long-term recommendations, each finding tagged by dimension and scored by impact x effort x urgency, with a scheduled follow-up date. Never a raw crawl export.
