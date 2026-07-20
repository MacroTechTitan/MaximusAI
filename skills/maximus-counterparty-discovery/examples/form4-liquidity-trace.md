# Worked example: SEC Form 4 liquidity-event discovery

Concrete walkthrough of using recent $5M+ Form 4 open-market sales as a **weak** liquidity signal. Names illustrative.

## Search brief

Find individual insiders with $5M+ open-market stock sales in the last 6 months who have a **second** fit signal for a managed-futures $100k SMA program.

## Sources

- SEC EDGAR Form 4 filings, filtered to `transaction_code=S` (open-market sale)
- 10b5-1 disclosures (parse for pre-planned status)
- Rule 144 filings for planned sales
- Corresponding 8-K/proxy for role verification

## Step 1: Query and parse

Query: `site:sec.gov/Archives/edgar/data/ "Form 4" "transaction code S"` scoped to last 180 days.

For each filing, extract:
- filer name, CIK, role at issuer
- transaction date, shares sold, price per share
- transaction code (S=open market, F=tax withholding, G=gift, M=option exercise, etc.)
- ownership form (D=direct, I=indirect through trust/fund)
- footnotes (10b5-1 reference, indirect ownership explanation, gift recipient)

**Do not** count option exercises, gifts, tax-withholding, or Rule 10b5-1 pre-planned trades as active liquidity decisions — they may still be capacity indicators, but flag them.

## Step 2: Calculate gross proceeds

`gross_proceeds = shares_sold * price_per_share`

For a filing showing 50,000 shares at $110 = $5.5M gross. Verify against filing footnotes.

## Step 3: Second fit signal (required)

**A Form 4 sale alone caps `capacity_score` at 45. It cannot alone yield a high total_score.**

Search for a second signal per candidate:
- LinkedIn/company bio mentioning finance/derivatives background
- Prior LP investments in alt-investment vehicles (public disclosures only)
- Public statements about alt-investment interest
- Board seats or advisory roles at alt-investment firms
- Podcast/conference appearances discussing macro/trend/futures

## Sample candidate row

```
candidate_id: cand_027
name: Alex Q. Insider (illustrative)
entity_type: individual
relationship_target: accredited_investor_prospect
organization: [current employer]
title: EVP, Corp Dev
city: [suppressed - metro only]
state: NY
country: US
website: n/a
public_profile_url: https://linkedin.com/in/alexqinsider (verified)
fit_summary: "Prior LP disclosure in a public alt fund (2022); podcast guest discussing trend-following (2024)."
capacity_summary: "Form 4 filed 2026-05-15: 45,000 shares open-market sale at $135 = $6.075M gross. Direct ownership. No 10b5-1 reference in footnote."
liquidity_event_summary: "See capacity_summary."
regulatory_summary: "No disciplinary history."
minimum_check_fit: true
accreditation_status: inferred_unverified
suitability_status: unknown
identity_confidence: 88
fit_score: 65
capacity_score: 45  # capped due to single liquidity signal
intent_score: 55    # prior LP + podcast = medium
source_quality_score: 85
risk_penalty: 0
total_score: 57.5
last_verified_at: 2026-07-20
review_status: verify
analyst_notes: "Second signal confirms alt-investment interest. Capacity capped per policy — verify AUM/net worth via direct qualification. Home address suppressed."
```

## Sample source_log rows

```
src_101,corporate,sec.gov/edgar,"Form 4" transaction code S price 100 to 200,2026-07-20T15:00Z,ok,347
src_102,corporate,sec.gov/edgar,Rule 10b5-1 planned sales 2026,2026-07-20T15:04Z,ok,89
src_103,professional,linkedin.com,alex insider corp dev,2026-07-20T15:08Z,ok,3
src_104,social,reddit.com,alex insider,2026-07-20T15:10Z,ok,0
```

## Compliance callouts

- **Home address suppressed**: even if visible in filings, exports show metro only.
- **Accreditation is inferred, not verified**: even a $6M sale doesn't formally confirm accreditation. Marked `inferred_unverified`.
- **10b5-1 flag**: pre-planned sales aren't reactive liquidity decisions; annotate but don't exclude.
- **Suitability**: `unknown` — a separate determination beyond wealth.
- **No home-sale, inheritance, or anonymous boasting sources** were used as capacity evidence.

## Key discipline points illustrated

- Weak signal is honestly labeled as weak (cap at 45).
- Second fit signal is mandatory before ranking.
- Every calculation is reproducible from the filing.
- Footnotes are parsed, not ignored.
- Compliance suppression is applied at export time, not left to the analyst.
