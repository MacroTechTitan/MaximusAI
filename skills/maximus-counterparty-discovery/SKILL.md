---
name: maximus-counterparty-discovery
description: Discover, verify, score, and export potential counterparties from a natural-language description. Use for investor, allocator, buyer, seller, lender, strategic partner, acquisition target, vendor, expert, or other counterparty searches that require deep public-web research, social and forum discovery, regulatory filings, litigation records, transaction signals, source-by-source evidence, and an auditable export. Includes a managed-futures CTA example with a $100,000 minimum, but never bundles or reuses sample prospect data.
---

# Maximus Counterparty Discovery

Turn a counterparty description into an evidence-led research operation. Search only lawful, permitted, public or licensed sources. Preserve provenance for every claim.

## Workflow

1. Parse the request into a `Counterparty Search Brief`:
   - counterparty type and relationship sought
   - geography and entity/person scope
   - minimum financial or operational threshold
   - strategy/product fit
   - positive signals, exclusions, recency window, target count
   - required export fields and allowed connectors
2. Build a source plan before searching. Read `references/source-playbook.md`.
3. Generate source-specific queries and execute searches in parallel where tools permit.
4. Create one evidence record per finding. Never merge two people or entities merely because names match.
5. Resolve identity using at least two independent identifiers when possible: full name plus employer, location, filing CIK/CRD/NFA ID, domain, or transaction party.
6. Score each candidate with `scripts/score_candidates.py` or the equivalent formula in `references/data-schema.md`.
7. Apply compliance and privacy review from `references/guardrails.md`.
8. Export candidates and source logs. Include every location searched, including searches that returned no useful result.
9. Summarize limitations, stale fields, paywalled gaps, unresolved identities, and recommended human verification.

## Search behavior

- Prefer primary sources: regulator databases, court dockets, official filings, company sites, government property records, and direct public statements.
- Use secondary sources for discovery, then verify material claims independently.
- Search Reddit and public forums for self-disclosed experience or interests, but label usernames as pseudonymous and confidence as low until identity is independently established.
- Search social platforms through approved APIs, licensed providers, platform-native search, or ordinary public web indexing. Do not bypass login walls, CAPTCHAs, robots controls, rate limits, or platform terms.
- For litigation and insolvency research, search complaints, judgments, bankruptcy schedules, receivership reports, claims registers, exhibits, and regulatory enforcement releases. Treat named investors or LPs as leads, not proof of present liquidity or interest.
- For property transactions, retain only the transaction, approximate value, date, jurisdiction, and source. Do not export a private residence street address, household-member data, or inferred personal routines.
- For SEC insider sales, parse Form 4 transaction codes and footnotes. Distinguish open-market sales from option exercises, gifts, tax withholding, Rule 10b5-1 activity, indirect ownership, and derivative transactions. Estimate gross proceeds only when price and disposed shares support it.
- Never assert accredited-investor, qualified-purchaser, suitability, liquidity, or intent from one wealth signal. Mark these as `unverified` unless documented or confirmed directly.

## CTA managed-account example

When the brief seeks investors for a managed-futures CTA program with a $100,000 minimum, load `references/cta-example.md`. Use it as search logic only. Do not import sample prospects or prior exports.

## Required outputs

Produce:

1. `search_brief.json`
2. `candidates.csv` and optionally `candidates.json`
3. `source_log.csv` with every query, source, timestamp, result count, and status
4. `evidence.csv` with one row per claim/source pair
5. `research_summary.md` explaining methods, strongest candidates, caveats, and uncovered gaps

Use the exact field definitions in `references/data-schema.md`.

## Quality rules

- Do not fabricate names, assets, emails, transaction amounts, registrations, or citations.
- Put an exact URL or stable filing/docket identifier behind every material claim.
- Record `observed_at`, `published_at`, and `event_date` separately.
- Preserve contradictory evidence instead of silently choosing one version.
- A candidate may rank highly only when fit evidence and capacity evidence are both present.
- Contact data must come from a business-public, consented, licensed, or user-provided source. Never infer personal emails from private data.


## Sibling skills

- `maximus-people-finder` — broad person-finding (investors, journalists, partners) without the finance-grade provenance requirements.
- `maximus-people-finder-recruiter` — recruiter workflow for candidate sourcing.
- `maximus-deep-research-pro` — inference-driven research when triangulation is needed to establish identity or capacity.
- `maximus-fintech-payments` — for onboarding flows after a candidate passes compliance review.
- `maximus-brain` — depth calibration when the brief is ambiguous.
