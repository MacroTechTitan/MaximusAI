---
name: maximus-people-finder-recruiter
description: "Deep multi-step recruiter agent for sourcing named candidates or role profiles across DevOps agencies, software dev shops, IT outsourcing firms, MSPs, technical staffing agencies, and general engineering/product/design/data employers of any type. Runs an 8-step intake-to-slate loop instead of a single-shot search. Triggers: 'find candidates for', 'source engineers for', 'find a senior X at Y', 'passive candidate search', 'boolean search LinkedIn', 'intake for role', 'recruiter deep dive', 'source for open role', 'find candidates matching brief'. Produces a verified, outreach-ready CSV slate with evidence and sourced-from URLs for every row."
metadata:
  pillar: research
  source: maximus
---

# Maximus — People Finder (Recruiter)

Sourcing is not a search query, it's a loop. A recruiter brief compresses a lot of judgment into a few lines — level, stack, comp band, must-haves — and a single search pass will always regress to the most generic interpretation of it. This skill exists to unpack the brief, search from multiple angles, and only hand over people whose fit you can point at with a URL.

## When to use

- "Find candidates for [role] at [company/company-type]."
- "Source [engineers/SREs/designers/data scientists] for [an open req]."
- "Find a senior [title] at [target company or company type]."
- Passive-candidate search: people not actively applying, found via GitHub, papers, conference talks, OSS contributions.
- "Boolean search LinkedIn for [skill combo]."
- Recruiter intake for a role — turning a job description or intake call into a sourced slate.
- DevOps agencies, software dev shops, IT outsourcing firms, MSPs, technical staffing agencies — the original `recruiter-deep-find` territory — AND general engineering, product, design, and data roles at any company (startups, enterprises, agencies alike).

## When NOT to use

- Broad, non-recruiter people-finding — investors, journalists, conference speakers as a general lookup, potential partners, sales prospects, or "who is this person" identity lookups. Redirect to **maximus-people-finder**.
- Simple company or headcount lookups with no named-person target. That's company research, not sourcing.
- Extracting personal contact details (home address, personal phone/cell) for any candidate. Out of scope everywhere — see Privacy below.
- Sourcing a single already-named individual for background/reference checks unrelated to a live req — that's diligence, not sourcing; treat as a one-off `search_web`/`search_vertical` task, not this loop.

## Purpose

Turn a recruiter brief into an outreach-ready slate: **intake → sourced list → verified evidence → ranked, exportable CSV**. Every candidate row must trace back to at least one real URL a recruiter can click. No row exists on inference alone.

## The Deep Loop (8 steps)

This is a loop, not a single-shot search. Run all 8 steps in order; steps 3-6 typically iterate more than once before step 7 is satisfied. Full formal spec: `references/deep-loop-spec.md`.

1. **Intake** — Capture or infer the structured brief (see Intake fields below). If the user gave a bare title ("find backend engineers"), state the assumptions you're filling in and proceed — don't stall on clarifying questions.
2. **Role Decomposition** — Break the role into: core competencies, tech-stack fingerprints, seniority signals (years, scope, team size led), and 3-6 target-company archetypes (direct competitors, adjacent-stack companies, agencies/consultancies known for the skill).
3. **Boolean Query Build** — Construct 5-10 distinct boolean/X-ray queries per source (LinkedIn, GitHub, etc.) using the must-have/nice-to-have matrix. See `references/boolean-query-cookbook.md`. Never run just one query — narrow queries miss passive candidates.
4. **Multi-Source Search** — Execute the query set across every relevant source (see Sources below), not just LinkedIn. Aim for a wide raw pool first (target: 30-50+ raw hits) before narrowing.
5. **Enrichment** — For each promising raw hit, pull a second and third data point (GitHub activity, conference talk, OSS repo, company bio page, patent record) to corroborate the LinkedIn/profile claim. Minimum two corroborating signals per candidate before it advances.
6. **Fit Scoring** — Score every enriched candidate against the rubric below. Drop or flag anything that fails a disqualifier.
7. **Verification** — Re-check every URL resolves, every claim has a live source, and no profile was invented from a plausible-sounding name/title pairing. This is the step most agents skip; it's the one that matters most.
8. **Delivery** — Produce the ranked CSV plus a short sourcing memo (what worked, what didn't, where to expand next). Deliver a minimum-viable slate (5-8 verified names) first; expand only if asked.

If step 7 fails for a candidate, that candidate is cut or explicitly marked "unverified — needs recruiter confirmation." Never silently promote an unverified hit into the final slate.

## Intake fields

Capture explicitly, or state the assumption if inferred:

- **Role & level** (e.g., Senior Backend Engineer, IC4/Staff)
- **Stack** (languages, frameworks, cloud, specific tools)
- **Location / remote policy** (onsite city, hybrid radius, remote-eligible countries/timezones)
- **Comp band** (base + equity/bonus range, used to filter realistic targets, never surfaced to candidates)
- **Must-haves** (non-negotiable skills/experience — the disqualifier line)
- **Nice-to-haves** (differentiators, not blockers)
- **Disqualifiers** (e.g., no visa sponsorship available, no agency/contract-to-hire background if role is FTE-only)
- **Target companies** (named competitors, company archetypes, or agency/MSP categories)
- **DEI considerations** (if the intake specifies a diverse-slate goal, treat it as a sourcing-channel requirement — see HOWTO recipe (f) — never as a filter that excludes anyone)

## Sources

- **LinkedIn** via `search_vertical` (vertical=`people`) and X-ray patterns (`site:linkedin.com/in`) via `search_web`.
- **GitHub** — for engineers/ML: search by language, repo topic, org membership, contribution graphs. Corroborates "hands-on" claims LinkedIn can't.
- **Stack Overflow careers / user profiles** — tag expertise as a secondary signal.
- **Kaggle** — for data scientists/ML engineers: competition rank, published notebooks.
- **Behance / Dribbble** — for product/visual designers: portfolio quality is itself evidence.
- **Conference speaker pages** (KubeCon, PyCon, NeurIPS, Config, Figma Config, etc.) — strong passive-candidate signal, high credibility.
- **Patent databases** (Google Patents, USPTO) — for deep technical ICs, especially hardware/ML/infra.
- **Open-source contributor lists** (CNCF, Apache, major framework CONTRIBUTORS.md) — direct evidence of scope and skill.
- **Alumni networks** (target-company alumni pages, bootcamp/university alumni directories) for warm-path sourcing.
- For the agency/MSP/outsourcing-firm angle specifically (DevOps shops, staffing firms, IT outsourcers), start from the agency-first method in **recruiter-deep-find**: enumerate target firms (Clutch, AWS/GCP/Azure partner directories, CNCF KCSP, HashiCorp partners, The Manifest) before searching for people inside them.

## Fit-scoring rubric

Score each candidate 0-100 across four weighted components:

| Component | Weight | What it measures |
|---|---|---|
| Must-have match | 40 | Fraction of must-haves with direct evidence (not inferred from title alone) |
| Nice-to-have match | 20 | Fraction of nice-to-haves present |
| Recency signals | 20 | How current the evidence is — recent commits, recent talk, current employer tenure vs. stale 5-year-old profile |
| Passive-vs-active hints | 20 | Open-to-work flag, recent job-change cadence, "not actively looking" language, agency/bench status if applicable |

A candidate below 50% must-have match does not make the slate regardless of total score — must-haves are a floor, not an averaged input.

## Boolean query patterns

Full cookbook: `references/boolean-query-cookbook.md`. Summary:

- **LinkedIn X-Ray**: `site:linkedin.com/in ("senior backend engineer" OR "staff engineer") ("Go" OR "Golang") (Kubernetes) -"looking for opportunities"` run via `search_web`.
- **Google/Bing site search**: `site:github.com "kubernetes-operator" language:Go` style queries for repo/topic discovery.
- **Boolean combos**: build a must-have AND chain, an OR chain across synonyms (SRE / DevOps Engineer / Platform Engineer), and a NOT chain to exclude recruiters, students, and obviously irrelevant roles.
- Rotate title synonyms and stack synonyms across query variants — a single fixed phrase under-returns by design of how these indexes work.

## Delivery format

Deliver a CSV with these columns for every candidate:

`name, role, company, tenure, location, linkedin_url, github_url (if applicable), fit_score, evidence, outreach_hook, sourced_from_url`

- `evidence` — one line citing the specific fact and its corroborating source (e.g., "led migration to Go microservices, per company eng blog").
- `outreach_hook` — a genuine, specific reason to reach out (shared conference, relevant OSS project, blog post) — never generic ("noticed your profile").
- `sourced_from_url` — the exact URL the candidate was discovered through, so the recruiter can retrace the path.

Deliver the CSV as a real file (write tool), not a chat table, once the slate exceeds ~5 rows.

## Anti-patterns

- **Single-title match** — treating "Senior Software Engineer" as sufficient without checking the actual stack, scope, or must-haves.
- **Ignoring must-haves** — letting a high nice-to-have score compensate for a missing must-have. Must-haves are a gate, not a weight to average away.
- **Hallucinated profile URLs** — never construct a plausible-looking LinkedIn/GitHub URL from a name and title. Every URL must come from an actual search or fetch result.
- **Ghost candidates** — including anyone without at least two independently verifiable, live-checked pieces of evidence. "This person probably exists and probably fits" is not a slate entry.
- **Single-pass search** — running one query and calling it sourced. The loop exists because query 1 always returns the obvious, already-tapped pool.
- **Silent scope creep on comp/visa/location disqualifiers** — if a candidate fails a stated disqualifier, cut them or flag explicitly; don't quietly include them anyway because they look otherwise strong.

## Privacy

Public professional-profile discovery only. Never extract or report home addresses, personal phone numbers, personal email guesses, or any non-work-related personal data. LinkedIn/GitHub/company-page public info and professional contact paths (company email pattern, LinkedIn InMail) are in scope; personal contact info is not.

## Sibling skills

- **recruiter-deep-find** — the intake-form sibling. It's the agency-first, DevOps/outsourcing-firm-focused workflow (and the standalone Replit app) that this skill deepens with the explicit 8-step loop and broader employer coverage (general engineering/product/design/data, not just agencies). Use `recruiter-deep-find`'s agency-enumeration method as the source list when the brief is specifically about DevOps/MSP/outsourcing-firm talent.
- **maximus-people-finder** — the broader, non-recruiter sibling for investors, journalists, partners, and general "find this person" tasks. Redirect there when the ask isn't a hiring req.
- **maximus-brain** — load for the think-before-act loop, memory hygiene, and depth-tier selection; this skill's 8-step loop is the recruiter-domain instance of brain's Deep tier (Frame → Recall → Select → Execute → Critique maps onto Intake/Decomposition → Query Build/Search/Enrichment → Fit Scoring/Verification → Delivery).

## Output

A minimum-viable slate (5-8 verified candidates) delivered as a CSV file plus a short sourcing memo: queries run, sources covered, raw-to-verified funnel counts, and where to expand if the recruiter wants more. Expand only on request — don't over-deliver an unverified 40-name dump when 8 verified names answer the brief.
