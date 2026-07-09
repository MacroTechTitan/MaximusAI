# Maximus — People Finder

## What

A deep, multi-step agent skill for locating specific people or building a verified, ranked shortlist of people — investors, journalists, partners, potential hires, subject-matter experts, decision-makers at target companies, board members, advisors, and alumni networks. It is not a single search: it runs a named **7-step loop** (Intake, Query Expansion, Multi-Channel Search, Enrichment, Deduplication, Ranking, Verification/Delivery) with quality gates between steps and an explicit rule for going back and broadening the search if too few candidates survive verification.

The core discipline: a name is not a hit until it's been enriched from a fetched source, deduplicated against every other channel it showed up on, ranked against the actual brief, and re-checked one more time before it ships. Single-source, stale-role, or hallucinated-URL candidates get caught in Step 7, not discovered by the user after the fact.

## When to use

- "Find 10 seed investors who led HR-tech rounds in the last two years."
- "Find journalists covering AI infrastructure I should pitch."
- "Who are the decision-makers on platform partnerships at these 20 companies?"
- "Find subject-matter experts for our advisory board on [topic]."
- "Find speakers for our podcast/conference on [topic]."
- "Find people who worked at [Company X] and are now at [Company Y]."
- "Find people who've been commenting publicly on [topic] recently."
- "Find this person — I think they work at [Company], last name [Name]."

## When NOT to use

- DevOps agencies, software dev shops, IT outsourcing firms, MSPs, or technical staffing agencies — that's `recruiter-deep-find`'s job. It owns the agency-first workflow (enumerate agencies, then enumerate people inside them) and this skill deliberately does not duplicate it.
- You already have the person's verified profile URL and just need to confirm current role — a single `fetch_url` + a sanity check is enough; the full loop is overkill.
- Pure company/market research with no person-level deliverable — use `maximus-deep-research` or `wide-search`.

## Example

**Brief:** "Find 10 seed-stage investors for an AI-native recruiting SaaS, must have led seed rounds in HR tech between 2024 and 2026."

**What happens:** Intake normalizes the brief (stage=seed, sector=HR tech/recruiting, evidence=led a seed round 2024-2026, N=10). Query expansion generates variants across "HR tech investor," "recruiting SaaS seed lead," "future of work fund," portfolio-company backtracking, and time-boxed funding announcements. Multi-channel search runs in parallel across news/funding announcements, X, fund portfolio pages, and Crunchbase/PitchBook. Enrichment pulls fund, check size, portfolio fit, and a recent deal per candidate. Dedup collapses the same investor found via a TechCrunch article and their fund's portfolio page into one record. Ranking scores against thesis fit. Verification re-checks that each investor's most recent seed lead is actually in HR tech, not just adjacent SaaS. Delivery is a ranked CSV with source URLs and an outreach hook per investor.

See `examples/find-investors-trace.md` for the full step-by-step trace, and `examples/find-journalists-trace.md` for a second worked example (journalist discovery with pitch angles).

## Related

- `recruiter-deep-find` (user skill) — DevOps-agency-specific sibling; redirect agency recruiting there.
- `maximus-brain` — picks the depth tier and loads this skill in its Pass 3 skill-selection step for people-finding work.
- `maximus-deep-research` — shares fan-out-before-narrowing and cite-or-cut discipline for non-person-shaped research.
- Built-in `search` skill, `people-research` recipe — underlying people-search query patterns this skill's loop leans on.
- `wide-search` — for briefs that are really a wide table across many entities (e.g. one decision-maker per company across 50 companies).

## Files in this skill

- `SKILL.md` — the skill definition and the 7-step loop.
- `HOWTO.md` — recipes for common request shapes.
- `examples/find-investors-trace.md`, `examples/find-journalists-trace.md` — full worked traces.
- `references/deep-loop-spec.md` — formal spec of the loop: inputs/outputs, quality gates, iteration rule.
- `references/source-map.md` — source-by-source guidance: best-for, cost/rate limits, verification difficulty.
