# maximus-counterparty-discovery

Discover, verify, score, and export potential counterparties from a natural-language description — with source-by-source provenance and finance-grade compliance guardrails.

## What it does

Turns a request like *"family offices and CTAs that allocate to managed-futures programs with $100k+ SMAs"* into an auditable research operation:

1. Parses the request into a structured search brief.
2. Builds a source plan (regulator databases, court dockets, filings, licensed contact data, permitted public web).
3. Runs parallel queries and logs every one — including zero-result and blocked searches.
4. Extracts candidates with one evidence record per claim.
5. Resolves identity conservatively (never merges on name alone).
6. Scores fit, capacity, intent, source quality, and risk.
7. Exports `candidates.csv`, `evidence.csv`, `source_log.csv`, and `research_summary.md`.

## When to trigger

- "Find investors for X strategy"
- "Discover allocators / LPs / buyers / sellers / lenders"
- "Source acquisition targets in Y sector"
- "Build a prospect list with sources"
- "Investor / counterparty discovery"
- "Find CTAs allocating to CTAs"
- Any counterparty search that requires citations, court records, filings, or an audit trail

## When NOT to use

- Generic person-finding (journalists, hires, partners) → use `maximus-people-finder`
- Recruiter candidate sourcing → use `maximus-people-finder-recruiter`
- Aggregation-only research → use `maximus-deep-research`
- Free-text due-diligence writeups without an export → use `maximus-deep-research-pro`

## What ships in this skill

- `SKILL.md` — instructions + workflow
- `references/source-playbook.md` — 8 source families, query construction rules
- `references/data-schema.md` — exact CSV field definitions and scoring formula
- `references/guardrails.md` — compliance, privacy, PII, and sanctioned-party rules
- `references/cta-example.md` — worked example for a managed-futures $100k SMA search
- `scripts/score_candidates.py` — reproducible scoring script
- `examples/family-office-search-trace.md` — worked family-office discovery
- `examples/form4-liquidity-trace.md` — worked SEC Form 4 liquidity-event search
- `agents/openai.yaml` — display metadata
- `replit-prompt.md` — production-app spec for building the full discovery platform

## Guardrails (short version)

- Public, licensed, or user-connected sources only.
- Never bypass CAPTCHAs, login walls, or platform terms.
- No exact home addresses, family-member data, private emails, or personal routines.
- No targeting people because they suffered a bankruptcy, fraud, or bereavement.
- Wealth, accreditation, liquidity, and intent are all `unverified` until documented.
- Discovery does not authorize solicitation — human review gate before any outreach.

Full rules in `references/guardrails.md`.

## Related skills

- [`maximus-people-finder`](../maximus-people-finder) — broader person-finding
- [`maximus-people-finder-recruiter`](../maximus-people-finder-recruiter) — recruiter workflow
- [`maximus-deep-research-pro`](../maximus-deep-research-pro) — inference-driven research
- [`maximus-fintech-payments`](../maximus-fintech-payments) — for downstream onboarding
- [`maximus-brain`](../maximus-brain) — depth calibration
