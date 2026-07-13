# maximus-seo-audit

## What

An end-to-end SEO audit skill that combines four dimensions — technical, content, backlink, and AI-visibility — into a single prioritized fix list. It is the umbrella skill of the `maximus-seo-pack`: it does not do the tactical work itself, it orchestrates the other SEO skills as building blocks, collects their findings, and cross-weighs everything on one impact x effort x urgency scale so a team gets a sequenced roadmap instead of a raw data export.

The deliverable is always: executive summary, critical fixes, warnings, long-term recommendations. Never a 40-tab spreadsheet of every issue a crawler found.

## When to use

- Running a full site audit spanning technical, content, backlink, and AI-visibility health.
- Diagnosing a traffic, ranking, or AI-citation drop when the cause is unknown and could span multiple dimensions.
- Auditing a competitor's site to learn what is working for them.
- Running a post-migration check after a redesign, replatform, or domain move.
- Any prompt containing "seo audit", "site audit", "full seo review", "technical audit", "content audit", "backlink audit", "ai visibility audit", or "diagnose seo problems".

## When not to use

- The diagnosis is already done and the task is executing a single fix — go directly to `maximus-technical-seo`, `maximus-content-seo`, `maximus-aeo-optimization`, or `maximus-geo-optimization`.
- Ongoing rank or AI-citation tracking with no audit event triggering it — use `maximus-llm-visibility-tracking`.
- Upfront keyword or topical planning before any pages exist — use `maximus-ai-seo-strategy`.

## Example

**Prompt:** "Our organic traffic dropped 30% over the last two months and we don't know why. Run a full SEO audit."

**What this skill does:**
1. Scopes the audit (whole domain, all 4 dimensions, deadline set by the urgency of the traffic drop).
2. Runs or requests a technical crawl to establish the current URL inventory and status-code map.
3. Collects Core Web Vitals, GSC coverage/query data, backlink data, and AI-citation checks.
4. Routes each dataset through the matching sibling skill's diagnostic lens — `maximus-technical-seo`, `maximus-content-seo`, `maximus-aeo-optimization`, `maximus-geo-optimization`.
5. Scores every finding on impact x effort x urgency and sequences a roadmap.
6. Delivers a report: executive summary, critical fixes (e.g., "redirect chain broke crawl budget after the last deploy"), warnings, long-term recommendations, and a follow-up date.

See `examples/rapid-audit-trace.md` for a full small-site audit and `examples/prioritization-trace.md` for the scoring mechanics on 40 raw findings.

## Related skills

- `maximus-technical-seo` — technical dimension execution (crawlability, CWV, schema, architecture).
- `maximus-content-seo` — content dimension execution (thin/duplicate content, on-page, internal linking).
- `maximus-aeo-optimization` — AI-visibility formatting execution on flagged pages.
- `maximus-geo-optimization` — LLM citation-tuning execution on flagged pages.
- `maximus-llm-visibility-tracking` — measurement layer; supplies AI-visibility data in and confirms fixes worked after.
- `maximus-ai-seo-strategy` — upstream strategy layer; receives this audit's structural/coverage gaps for the next planning cycle.

## Files

- `SKILL.md` — full skill definition, triggers, the 4 dimensions, 6-phase workflow, prioritization framework, report structure.
- `HOWTO.md` — six step-by-step recipes covering rapid, large-site, post-migration, competitor, AI-visibility-focused audits, and building the fix list.
- `examples/rapid-audit-trace.md` — worked 48-hour audit of a ~100-URL SaaS site, phase by phase.
- `examples/prioritization-trace.md` — worked scoring of 40 raw findings into a sequenced roadmap.
- `references/audit-checklist-master.md` — master checklist organized by the 4 dimensions, cross-referencing specific sibling-skill recipes for each item.
