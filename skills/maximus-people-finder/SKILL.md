---
name: maximus-people-finder
description: "Deep multi-step agent for locating people or shortlists outside DevOps-agency recruiting — investors, journalists, partners, potential hires, subject matter experts, decision-makers at target companies, board members, advisors, and alumni networks. Runs a named 7-step loop (Intake, Query Expansion, Multi-Channel Search, Enrichment, Deduplication, Ranking, Verification/Delivery) rather than a single search. Triggers: 'find this person', 'find investors who', 'find journalists covering', 'find partners for', 'find experts in', 'who at company X does Y', 'find decision makers at', 'find board members'. Use for fundraising, PR/comms, BD/partnerships, advisory building, event/podcast booking, alumni mining. Do NOT use for DevOps/software agency recruiting — that goes to `recruiter-deep-find`. Do NOT use for generic company research with no person-level output — use `maximus-deep-research` instead."
metadata:
  pillar: research
  source: maximus
---

# Maximus — People Finder

Most "find me some people" requests get answered with a single search and five plausible-looking names. That fails the moment someone clicks the LinkedIn link and it's the wrong person, or emails a "journalist" who stopped covering the beat two years ago. This skill exists to replace that shortcut with a loop: expand the query past the obvious phrasing, search across every channel a real person leaves a trail on, enrich each hit with independent facts, collapse duplicates, rank by fit, and verify every survivor against the original brief before it ships. If a candidate can't be traced to at least one piece of fetched evidence, they don't make the final list.

## Purpose — broad people-finding, not agency recruiting

This skill is the generalist sibling to **`recruiter-deep-find`**, which is scoped tightly to sourcing candidates at DevOps agencies, software dev shops, IT outsourcing firms, MSPs, and technical staffing agencies. That skill's agency-first workflow (enumerate agencies, then enumerate people inside them) is purpose-built for that one population and should not be reinvented here.

Everything else that reduces to "find a specific person or a ranked shortlist of people" belongs here:

- Investors who match a fundraising thesis (stage, sector, check size, recent activity).
- Journalists, analysts, and newsletter writers covering a beat.
- Partnership or BD contacts — decision-makers at named target companies.
- Potential hires outside the agency population (in-house engineers, operators, executives).
- Subject-matter experts for an advisory board, panel, or diligence call.
- Board members and advisors with a specific background.
- Alumni of a company/school now working somewhere relevant.
- Anyone who has publicly engaged with a topic (commented, posted, spoken) recently.

If a brief arrives that's actually agency recruiting, say so and redirect to `recruiter-deep-find` rather than running this loop on the wrong population.

## The Deep Loop — 7 steps, run in order

This is a **deep multi-step agent, not a single-shot search.** Each step is a discrete pass with its own inputs, outputs, and a quality gate before you proceed. Don't collapse steps to save time — the loop is what turns "five plausible names" into "ten verified names with receipts." Full formal spec with iteration rules: `references/deep-loop-spec.md`.

1. **Intake** — Normalize the brief into a structured target profile: who, what evidence of fit looks like, how many, any hard constraints (geography, timing, seniority, must-have credentials), and what "verified" means for this brief. State assumptions explicitly if the brief is underspecified; don't stall on a clarifying question when you can reasonably infer intent.
2. **Query Expansion** — Never search on the brief's literal wording alone. Generate query variants across role synonyms, adjacent titles, company/portfolio lists, topic keywords, and time windows. A thin query set is the single biggest cause of a thin candidate pool.
3. **Multi-Channel Search** — Fan out in parallel across every channel plausible for this population (see Sources below). One channel is a lead; multiple channels finding the same person is a signal.
4. **Enrichment** — For every raw hit, pull the fields in the Enrichment section below from at least one fetched source per field where possible. No enrichment field is asserted from memory.
5. **Deduplication** — Collapse the same person appearing under multiple channels/spellings/company-name variants into one record, merging evidence rather than picking one source and discarding the rest.
6. **Ranking** — Score surviving candidates against the Step 1 target profile. Rank, don't just list. State the ranking rationale per candidate in one line.
7. **Verification / Delivery** — Re-check each candidate against the original brief one more time before shipping: does the evidence actually match, is the role/title current (not stale), is there more than one corroborating source. Deliver the ranked, cited output.

**Iterate, don't pad.** If Step 6 leaves fewer verified candidates than the brief asked for, go back to Step 2 with broader queries rather than lowering the verification bar or inventing candidates to hit a headcount. See the spec for the exact iteration trigger.

## Adapting the loop to Perplexity Computer's tools

- **Step 3 (Multi-Channel Search)** — `search_vertical(vertical="people", ...)` for profile discovery; `search_web` for news/press/bylines; `search_vertical(vertical="academic", ...)` for authorship/affiliation trails; `fetch_url` for company team pages, SEC filings, Crunchbase/PitchBook pages, and conference agendas.
- **Step 4 (Enrichment)** — batch `fetch_url` calls per candidate for profile pages, company pages, and recent posts. For a candidate list beyond roughly 15-20 people, use `run_subagent` to enrich in parallel: give each subagent one candidate (or a small cluster) and a complete, self-contained brief — it has no access to your conversation history, so hand it the name, known affiliations, and exactly which fields to verify and return.
- **Step 3/Step 4 connectors** — before hand-rolling a LinkedIn or Crunchbase search, call `list_external_tools` to check whether a connected data source already exists (e.g. a Crunchbase or PitchBook connector); prefer the connector over a raw fetch when one is available.
- **Step 6 (Ranking) at scale** — if the brief is really a wide table (many target companies x one role each), consider delegating the raw per-company pull to `wide-search` and reserve this skill's loop for verification and ranking on top of that pull.

## Multi-channel search sources

Run these in parallel where the brief's population makes them relevant — don't rely on one channel:

- **LinkedIn-equivalent profiles** — `search_vertical(vertical="people", ...)` for role/company/location combinations.
- **Company sites** — About/Team/Leadership pages, press pages, careers pages for org-chart signals.
- **News and press** — `search_web` for recent coverage, funding announcements, quote attribution.
- **X/Twitter** — recent posts, bios, and reply threads for topic engagement and current affiliation.
- **GitHub** — for technical experts: repo ownership, org membership, commit activity, README bios.
- **Academic papers** — `search_vertical(vertical="academic")` for authorship, affiliation, and citation trails.
- **Podcasts and conference speaker lists** — guest rosters and agenda pages for topic-authority signals.
- **SEC filings (EDGAR)** — executive officer and board listings for public-company decision-makers.
- **Crunchbase / PitchBook** — via `list_external_tools` connectors where connected; otherwise their public pages through `fetch_url`.
- **Newsletter bylines and Substack** — for journalist/analyst discovery specifically.

Full source-by-source guidance (best-for, rate limits, verification difficulty): `references/source-map.md`.

## Enrichment fields (per candidate)

- Name
- Current role and company
- Location
- Contact hint (public-only: company email pattern, published contact page, public social handle — never a scraped personal phone or home address)
- Mutual-connection or warm-path signal, if visible
- Recent activity (a post, talk, article, filing, or comment within a relevant time window)
- Why-this-person justification, one line, tied to the Step 1 target profile
- Source URL(s) for every field above that isn't a direct restatement of the brief

## Verification pass

Before any candidate ships, ask and answer explicitly:

- Does the evidence actually match the brief's criteria, or does it just look adjacent?
- Is the role/title current, or is this a stale mention (job change, fund wind-down, beat change)?
- Is there more than one independent source, or is this a single unverified claim?
- Could this be a name collision (same name, different person)?

A single source is a lead, not a hit. Two independent, corroborating signals is the bar for anything that ships as "verified." Anything short of that ships labeled "unverified — one source" rather than silently included.

## Delivery format

Default to a ranked table (CSV or markdown table) plus a short cover summary:

`rank, name, current_role, company, location, why_fit, confidence (verified / likely / unverified), source_urls, outreach_hook`

Save to a workspace file (e.g. `/home/user/workspace/people_finder_run_<timestamp>/candidates.csv`) and share it. The cover summary restates the brief, states how many channels were searched, and flags any gaps (e.g. "found only 6 of the requested 10; broadened queries twice; recommend widening geography").

## Worked examples

Two full traces showing the 7-step loop end to end, with explicit query expansion, parallel search, dedup, and a final ranked CSV:

- `examples/find-investors-trace.md` — 10 seed-stage investors for an AI-native recruiting SaaS, thesis-matched on stage, sector, and recent HR-tech seed leads.
- `examples/find-journalists-trace.md` — journalists covering AI infrastructure, sourced from bylines, newsletters, and recent X activity, delivered with pitch angles.

## Anti-patterns

- **Hallucinated profile URLs.** Never construct a LinkedIn/X/GitHub URL from a guessed username pattern. Only include a URL you actually fetched or that a search tool returned.
- **Stale role data.** A person's last-known title from a two-year-old article is not their current role. Confirm recency before ranking someone on a current-decision-maker brief.
- **Single-source claims presented as fact.** One mention is a lead. State confidence honestly rather than smoothing a thin trail into a confident-sounding bullet.
- **PII overreach.** No personal phone numbers, home addresses, or non-public contact info. Public professional contact paths only (company email pattern, public profile, published contact form).
- **Padding to hit a headcount.** If the brief asked for 10 and only 6 verify, deliver 6 and say so — don't fill the rest with weak matches.
- **Treating one channel as sufficient.** LinkedIn alone, or X alone, misses people and produces false confidence. Fan out per the source map.

## Sibling skills

- **`recruiter-deep-find`** (user skill) — the DevOps-agency-specific sibling. Redirect there for agency recruiting; this skill explicitly does not duplicate its agency-first workflow.
- **`maximus-brain`** — this is a "Deep" or "Extreme" tier task under brain's depth framework; let brain pick the tier and load this skill in its Pass 3 skill-selection step.
- **`maximus-deep-research`** — shares the fan-out-before-narrowing and cite-or-cut discipline; use it for entity/market research that isn't person-shaped, or hand off to it when a candidate's employer needs a deeper company-level dossier.
- **Built-in `search` skill, `people-research` recipe** — the underlying people-search patterns (query construction, profile matching, disambiguation) that this skill's Step 3 and Step 5 lean on. Load it via `load_skill(name="search")` before heavy people-vertical work.
- **`wide-search`** — when the brief is really a table across many entities (e.g. "one decision-maker per company for 50 companies"), delegate the raw per-entity pull to `wide-search` and use this skill's loop for the verification/ranking layer on top.

## Output

A ranked, cited candidate table (CSV + short cover summary), saved to a workspace file and shared with the user. Every row traces to at least one fetched source URL; anything short of two-source verification is labeled accordingly. The cover summary states channels searched, iteration count, and any gaps between what was asked for and what verified.
