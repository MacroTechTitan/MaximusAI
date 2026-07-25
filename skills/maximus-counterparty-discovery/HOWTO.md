# How to use maximus-counterparty-discovery

Six recipes for common counterparty-discovery jobs. Each is meant to be run start-to-finish and produce the four required exports.

## Recipe 1: Managed-futures CTA allocator search

**Goal:** Find family offices, allocators, and CTAs that could suit a $100k managed-futures SMA.

1. Load `references/cta-example.md` for the CTA-specific search logic.
2. Build the search brief: type=allocator, minimum=$100k, geography=US, positive signals=managed-futures/alternatives/macro/trend, exclusions=retail-only, target=50.
3. Run source families in parallel: Form ADV, family-office sites, conference agendas, futures-podcast guest lists, CTA/CPO manager-of-managers records, NFA BASIC.
4. Adversarial pass: check every candidate for regulatory red flags and disciplinary history.
5. Score with `scripts/score_candidates.py`.
6. Export the four files. Include search_log entries for every zero-result query.
7. Route to human compliance review before any outreach.

## Recipe 2: Acquisition-target search in a niche vertical

**Goal:** Find 20 potential acquisition targets in a specific SaaS vertical.

1. Search brief: type=acquisition-target, revenue-band=$1M-$10M, geography=US/Canada, positive-signals=founder-owned/no-institutional-capital.
2. Source families: state incorporation records, product-hunt/similar directories, LinkedIn company pages via approved API, industry news, patent filings.
3. Enrichment pass: founder identification, funding history from Crunchbase/PitchBook (via licensed provider), employee count.
4. Score with capacity=fit-with-buyer-thesis, intent=signals-of-exit-readiness (age of company, founder age, market pressure).
5. Export with methodology.

## Recipe 3: Insolvent-CTA relationship research

**Goal:** From a public bankruptcy or receivership matter, identify lawfully disclosed LPs, feeder funds, or introducing brokers — as **relationship leads**, not outreach targets.

1. Source: CourtListener/PACER (authorized), bankruptcy court dockets, trustee/receiver reports, claims registers.
2. Parse the schedules and exhibits. Record entity names and roles.
3. Never treat loss history as reason to exploit vulnerability. See `references/guardrails.md`.
4. Cross-reference each entity against current regulatory filings (still active? still allocating?).
5. Output labels every entity clearly: `role=former_LP`, `verified_current_status=unknown`.
6. Compliance review is mandatory before any use of this list.

## Recipe 4: SEC Form 4 liquidity-event search

**Goal:** Identify insiders with recent $5M+ open-market sales as a **weak** liquidity signal.

1. Query `site:sec.gov/Archives/edgar/data "Form 4" transaction code S` scoped to a date range.
2. For each hit, parse: shares disposed, price, transaction code, footnotes, ownership type (direct vs indirect), Rule 10b5-1 indicator, gift/exercise/withholding flags.
3. Calculate gross proceeds only when price × shares is reliable. Exclude option exercises, gifts, tax withholding.
4. Weak-signal cap: `capacity_score` cannot exceed 45 based on liquidity alone.
5. Require a second fit signal (interest in alternatives, prior investments, etc.) before ranking as a candidate.
6. Suppress residential addresses from exports.

## Recipe 5: Family-office search from public alt-investment interest

**Goal:** Discover family offices that publicly discuss alt-investment or managed-futures interest.

1. Sources: family-office websites, Family Office Exchange/Institutional Investor coverage, conference speaker lists (SALT, Context Summit, Sohn, iConnections), podcast guest lists.
2. Verify each hit via a second source (LinkedIn, company site, news coverage).
3. Do not assume single-family-office status from a name alone — many single-family offices don't use that label publicly.
4. Score capacity from disclosed AUM or credible public estimate, not property records.
5. Export includes `capacity_source_url` per candidate.

## Recipe 6: Turning discovery output into an outreach-ready list

**Goal:** Take a completed discovery run and produce a review-ready outreach candidate list.

1. Filter `candidates.csv` to `review_status=approved_for_outreach` only.
2. Verify contact data source for every row (`contact_source=user_connected_CRM` or `licensed_business_directory` etc.).
3. Cross-check against suppression list and do-not-contact list.
4. Route through compliance approval per firm policy.
5. Hand off to outreach system with methodology export attached.
6. Never bulk-send from a discovery run without human review of each row.

## Cross-skill combos

- **After discovery:** use `maximus-deep-research-pro` on the top 10 candidates for deeper triangulation before outreach.
- **Before discovery:** use `maximus-brain` to calibrate depth if the brief is ambiguous.
- **For onboarding:** hand off approved candidates to `maximus-fintech-payments` for the payment/KYC flow.
