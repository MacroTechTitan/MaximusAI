# Worked trace — Senior Backend Engineer, Series B Fintech

This is an illustrative worked trace showing how the 8-step deep loop runs end to end for a realistic brief. Candidate names, companies, and URLs below are illustrative placeholders for demonstrating the method — in an actual run, every row in the final slate must be backed by a real, fetched URL (see Verification, step 7, and the Anti-patterns section of `SKILL.md`: never fabricate a profile URL).

## Step 1 — Intake

Brief as given: "Find a senior backend engineer for our Series B fintech, remote US, must know Go and distributed systems."

Filled-in structured intake (assumptions stated where the brief was silent):

- **Role & level**: Senior Backend Engineer, IC4 equivalent
- **Stack**: Go (must-have), distributed systems experience (must-have); Postgres, Kafka, gRPC (nice-to-have, assumed typical for this stack)
- **Location / remote**: Remote, US timezones only (assumed from "remote US")
- **Comp band**: Not given — assumed Series B fintech backend band, $170-210k base + equity (stated as assumption, not surfaced to candidates)
- **Must-haves**: Go in production, distributed-systems scope (not just microservices CRUD), 5+ years total experience
- **Nice-to-haves**: fintech/payments domain experience, Kafka/event-driven systems, prior startup (not just Big Tech) experience
- **Disqualifiers**: no visa sponsorship available this cycle (assumed standard for Series B; flagged as assumption)
- **Target companies**: assumed peer set of Series B/C fintechs with Go backends — to be confirmed via search in step 2
- **DEI**: none specified

## Step 2 — Role Decomposition

Core competencies: distributed systems design, Go proficiency at a production scale, ledger/payments-adjacent correctness thinking even if not fintech-specific.

Target-company archetypes identified via a quick market scan (`search_web`: "Series B fintech companies Go backend 2025 2026"):
1. Direct peers — Series B/C fintech companies known to use Go
2. Adjacent-stack companies — non-fintech companies with distributed-systems-heavy Go backends (infra, logistics)
3. Stretch targets — Series D+/public fintechs, for engineers open to a smaller-company step-down for equity upside

## Step 3 — Boolean Query Build

Query set (LinkedIn X-Ray via `search_web`, run as distinct queries, not one combined query):

1. `site:linkedin.com/in ("senior backend engineer" OR "staff backend engineer") (Go OR Golang) (fintech OR payments)`
2. `site:linkedin.com/in ("senior software engineer") ("distributed systems") (Go OR Golang) -recruiter -"talent acquisition"`
3. `site:linkedin.com/in ("backend engineer") (Kafka) (Go OR Golang) (remote)`
4. GitHub: search users/repos by `language:Go topic:distributed-systems`, filter to accounts with recent (last 6 months) commit activity
5. GitHub: search for contributors to well-known Go fintech-adjacent open-source projects (payment SDKs, ledger libraries)

## Step 4 — Multi-Source Search

Ran the 5 queries above across LinkedIn (via `search_vertical` vertical=`people` and `search_web` X-ray) and GitHub. Raw pool: **41 hits** (28 LinkedIn, 13 GitHub) after removing obvious non-matches (recruiters, students, unrelated "Go" as in "go-getter" false positives from keyword overlap).

## Step 5 — Enrichment

For each of the 41 raw hits, pulled a second signal:
- LinkedIn hits: cross-checked against GitHub (same name/company) or a company engineering blog post naming them.
- GitHub hits: cross-checked against LinkedIn for current title/employer and against commit history for recency.

After enrichment, **15 candidates** had at least two corroborating signals (e.g., LinkedIn title + GitHub commit activity, or LinkedIn title + a named appearance in a company engineering blog post). The remaining 26 either had only one weak signal or corroboration contradicted the initial hit (e.g., title changed, no longer at a qualifying company) and were dropped.

## Step 6 — Fit Scoring

Scored the 15 enriched candidates against the rubric (must-have 40 / nice-to-have 20 / recency 20 / passive-vs-active 20). Two were cut for failing the must-have floor (Go listed as a secondary/legacy skill, not a current one). **13 candidates** cleared the must-have gate.

## Step 7 — Verification

Re-checked every remaining URL resolved live and every claimed fact (current employer, Go usage, distributed-systems scope) had a fetchable source at time of check. **5 candidates** were cut at this step — two had stale LinkedIn data (company acquired/renamed, current role unclear), two had inference-only Go usage (job title implied it but no direct evidence), one GitHub profile could not be confidently linked to the LinkedIn identity (name collision, no matching secondary signal).

**8 candidates verified** — this is the minimum-viable slate.

## Step 8 — Delivery

Delivered as a CSV (`name, role, company, tenure, location, linkedin_url, github_url, fit_score, evidence, outreach_hook, sourced_from_url`), ranked by fit score, plus a sourcing memo:

- Queries run: 5 (3 LinkedIn X-ray, 2 GitHub)
- Sources covered: LinkedIn, GitHub
- Funnel: 41 raw -> 15 enriched -> 13 passed must-have gate -> 8 verified
- Suggested next-channel expansion if a larger slate is wanted: Stack Overflow careers profiles tagged Go + distributed-systems, and conference speaker lists (GopherCon, KubeCon Go-track talks) for additional passive candidates.
- Two candidates were flagged "single-signal — recruiter should verify before outreach" rather than dropped entirely, per the rapid-turnaround convention in `HOWTO.md` recipe (g), since the recruiter indicated urgency in the original ask.

This trace demonstrates the shape of the loop. In a live run, replace every placeholder company/candidate reference with actual fetched search results, and never advance a row past step 7 without a live, resolvable URL behind it.
