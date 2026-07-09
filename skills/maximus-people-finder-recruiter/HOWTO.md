# HOWTO — maximus-people-finder-recruiter

Eight recipes for common recruiting scenarios. Each assumes the 8-step deep loop from `SKILL.md`; the notes below are what changes per scenario — sources emphasized, query patterns, and scoring adjustments.

## (a) Senior backend engineer at Series B fintechs

- **Decomposition emphasis**: distributed systems, payments/ledger correctness, language (Go/Java/Kotlin/Rust common at this tier), scale signals (requests/sec, data volume) rather than raw years of experience.
- **Target companies**: 8-12 named Series B/C fintechs with similar stack (check Crunchbase-style funding databases via `search_web` for recent Series B fintech raises if the user doesn't supply names), plus 2-3 tier-up companies (Series D+/public fintech) as stretch targets for people ready to step down in company size for equity upside.
- **Boolean pattern**: `site:linkedin.com/in ("senior backend engineer" OR "staff engineer") (fintech OR payments OR ledger) (Go OR Golang OR Kotlin) -recruiter`. Run separate variants per language.
- **Enrichment**: GitHub commit history for payments/ledger repos, conference talks (e.g., Money20/20, fintech infra meetups).
- **Scoring note**: weight "recency signals" up — fintech backend hiring moves fast; a profile last updated 3+ years ago is a weak signal even with a strong stack match.
- Full worked trace for this exact scenario: `examples/senior-backend-trace.md`.

## (b) SRE at MSP-type agencies (DevOps focus)

- This is squarely **recruiter-deep-find** territory — use its agency-first method as step 2 of this loop's Role Decomposition: enumerate target MSPs/DevOps agencies first (Clutch, AWS/GCP/Azure partner directories, CNCF KCSP, HashiCorp partners, The Manifest), then search for SREs inside them.
- **Boolean pattern**: `site:linkedin.com/in ("site reliability engineer" OR SRE OR "platform engineer") (Kubernetes OR Terraform) ("[Agency Name]" OR "managed services")`.
- **Verification emphasis**: agency staff often list client work under NDA — corroborate seniority via certifications (AWS/GCP/Azure professional-level, CKA/CKS) and public conference/webinar appearances rather than named client projects.
- **Non-solicit flag**: per `recruiter-deep-find` convention, flag candidates at agencies with known non-solicit clauses as "moderate/high risk" in the outreach notes — don't drop them, but note it for the recruiter.

## (c) ML engineer with LLM production experience

- **Decomposition emphasis**: distinguish "trained/fine-tuned a model" from "shipped an LLM feature to production" — the must-have is production deployment experience (serving, latency, cost, eval pipelines), not research-only exposure.
- **Sources**: GitHub (inference-serving repos, vLLM/TGI/LangChain contributions), academic papers (`search_vertical` vertical=`academic` for recent LLM systems papers — corroborates deep technical background), LinkedIn, Kaggle (less central here than for classic ML/data roles).
- **Boolean pattern**: `site:linkedin.com/in ("ML engineer" OR "machine learning engineer") ("LLM" OR "large language model") (production OR "shipped" OR inference)`.
- **Triangulation**: a strong candidate should show up in at least two of {GitHub, papers, LinkedIn} independently — that's the two-signal verification bar.
- Full worked trace for this exact scenario: `examples/ml-engineer-trace.md`.

## (d) Product designer with fintech portfolio

- **Sources shift**: Behance/Dribbble become primary evidence sources, not secondary. Portfolio quality and fintech-specific case studies (onboarding flows, KYC UX, dashboard/data-viz work) are the strongest signal.
- **Boolean pattern**: `site:linkedin.com/in ("product designer" OR "senior product designer") (fintech OR banking OR payments)` paired with a direct Behance/Dribbble search (`search_vertical` vertical=`image` or a targeted `search_web` query like `site:behance.net fintech onboarding case study`).
- **Fit-scoring adjustment**: "must-have match" should include portfolio-visible evidence (an actual shipped fintech flow), not just a job title that says "fintech company."

## (e) Passive candidate targeting via GitHub

- **When to use**: role is a hands-on IC (backend, infra, ML) where code output is a better signal than resume text, and the goal is explicitly people *not* actively job-searching.
- **Method**: search GitHub by language + repo topic + recent commit activity (last 3-6 months) rather than by job title. Cross-reference the GitHub profile's linked company/LinkedIn to confirm current employer.
- **Passive-signal scoring**: active, recent commits at a *current* employer's org (not a personal side project) plus no "open to work" LinkedIn badge is the strongest passive-candidate signal — score it high on the "passive-vs-active hints" component.
- **Outreach hook**: reference the specific repo/PR/commit — this is the single best outreach differentiator for engineering candidates.

## (f) Diverse slate sourcing

- Treat a diverse-slate requirement as a **sourcing-channel requirement**, never a candidate filter. Expand the channel list: women-in-tech/underrepresented-group professional communities, HBCU/MSI alumni networks, affinity-group conference speaker lists (e.g., Grace Hopper, AfroTech, Lesbians Who Tech), in addition to the standard channels.
- Run the full boolean query set against these additional channels the same way as the standard set — same must-have gate, same two-signal verification. The goal is a wider net into the funnel, not different scoring criteria once someone is in it.
- Report channel coverage in the delivery memo (which channels were searched) so the recruiter can see the funnel, not just the outcome.

## (g) Rapid intake-to-slate under 24h

- Compress steps but do not skip them. Time-box: Intake + Decomposition (fast, ~15 min equivalent), Boolean Query Build (prepare 5 queries per source, not 10), Multi-Source Search (limit to top 3 sources for the role type instead of all), Enrichment (one corroborating signal minimum instead of two, but flag every such candidate as "single-signal — recruiter should verify before outreach"), Fit Scoring, Verification (still mandatory — never skip), Delivery.
- Deliver the minimum-viable slate (5 names) first; state explicitly in the memo which steps were time-boxed so the recruiter knows the confidence level.

## (h) Exporting an outreach CSV

- Once the slate is verified, write a CSV file (not a chat table) with the exact delivery-format columns from `SKILL.md`: `name, role, company, tenure, location, linkedin_url, github_url, fit_score, evidence, outreach_hook, sourced_from_url`.
- Sort by `fit_score` descending. Keep `evidence` and `outreach_hook` specific and non-generic — a recruiter should be able to open the outreach message from that one cell.
- Include a short sourcing memo as a separate section or file: queries run, sources covered, raw-to-verified funnel counts (e.g., "42 raw hits -> 16 enriched -> 8 verified"), and suggested next channels if the recruiter wants an expanded slate.
