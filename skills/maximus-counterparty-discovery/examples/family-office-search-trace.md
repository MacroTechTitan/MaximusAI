# Worked example: family-office discovery for a managed-futures CTA

Concrete walkthrough of a $100k-minimum managed-futures SMA search. Numbers and names are illustrative.

## Search brief (parsed from user request)

```json
{
  "counterparty_type": "allocator",
  "counterparty_subtypes": ["family_office", "single_family_office", "multi_family_office"],
  "geography": ["US"],
  "minimum": {"currency": "USD", "amount": 100000},
  "strategy_fit": ["managed_futures", "trend_following", "systematic_macro", "alternatives_diversifier"],
  "positive_signals": [
    "existing CTA allocation",
    "alt-investment mandate",
    "public interest in futures/macro"
  ],
  "exclusions": ["retail_only_platforms", "sanctioned_parties", "unresolved_fraud_findings"],
  "recency_window_months": 36,
  "target_count": 40,
  "required_export_fields": "standard"
}
```

## Source plan

| Source family | Provider | Query examples | Expected yield |
|---|---|---|---|
| Regulatory | SEC IAPD, Form ADV | ADV Part 2A search for "managed futures" | Medium |
| Institutional allocators | FOX/Institutional Investor | Family-office member lists | Medium |
| Corporate & liquidity events | SEC Form 4, 8-K | 10b5-1 sales >$5M | Low (weak signal) |
| Social & forums | Reddit r/futures, X | "managed account" allocation discussions | Low (pseudonymous) |
| CTA-to-CTA | NFA BASIC, Form ADV private-fund | Multi-manager pools | Medium |
| Conferences | Context Summit, SALT | Speaker/attendee lists | High |
| Podcasts | Top Traders Unplugged, Chat With Traders | Guest lists | Medium |

## Sample source_log.csv rows

```
source_id,source_family,provider_or_site,query_text,started_at,status,result_count
src_001,regulatory,sec.gov/iapd,"managed futures" alternatives mandate,2026-07-20T14:00Z,ok,142
src_002,social,reddit.com/r/futures,"managed account" allocation $100k,2026-07-20T14:03Z,ok,18
src_003,conferences,contextsummits.com,speakers 2025,2026-07-20T14:07Z,ok,86
src_004,litigation,courtlistener.com,failed CTA feeder fund LP schedule,2026-07-20T14:12Z,ok,4
src_005,regulatory,nfa.futures.org/basic,multi-manager pool CTA-of-CTAs,2026-07-20T14:15Z,ok,31
src_006,social,x.com/search,"trend following" family office allocation,2026-07-20T14:20Z,rate_limited,0
```

## Sample candidate row

```
candidate_id: cand_014
name: Ridgeline Family Office (illustrative)
entity_type: multi_family_office
relationship_target: allocator
organization: Ridgeline FO
title: Chief Investment Officer (person: J. Doe)
city: Chicago
state: IL
country: US
website: [suppressed until verified]
public_profile_url: https://linkedin.com/company/ridgeline-fo (verified via 2 sources)
fit_summary: "Public 2025 Context Summit panel on 'Trend-following in a low-vol regime'."
capacity_summary: "MFO disclosed $2.1B AUA in 2024 industry report."
liquidity_event_summary: "n/a"
regulatory_summary: "No disciplinary history on IAPD/BASIC for named CIO."
litigation_summary: "None material."
forum_summary: "n/a"
minimum_check_fit: true
accreditation_status: verified
suitability_status: needs_review
identity_confidence: 82
fit_score: 78
capacity_score: 72
intent_score: 65
source_quality_score: 80
risk_penalty: 0
total_score: 74.4
last_verified_at: 2026-07-20
review_status: verify
analyst_notes: "CIO panel remarks establish interest but not commitment. Verify current allocation via direct outreach after compliance review."
```

## Sample evidence rows

```
evidence_id: ev_101
candidate_id: cand_014
claim_type: interest_in_trend_following
claim_text: "CIO discussed trend-following diversification benefits on Context Summit 2025 panel."
source_url: https://contextsummits.com/agenda/2025#panel-42
source_publisher: Context Summits
source_type: primary_public_statement
event_date: 2025-11-14
published_at: 2025-11-14
observed_at: 2026-07-20
verbatim_excerpt: "We've added a systematic trend allocation of roughly [redacted%] this year."
confidence: 0.85
primary_source: true

evidence_id: ev_102
candidate_id: cand_014
claim_type: aua_disclosed
claim_text: "Ridgeline FO listed at $2.1B AUA in industry report."
source_url: https://institutionalinvestor.com/example/2024-mfo-report
source_publisher: Institutional Investor
source_type: secondary_industry_report
event_date: 2024-12-01
published_at: 2024-12-15
observed_at: 2026-07-20
verbatim_excerpt: "Ridgeline FO — $2.1B assets under advisement."
confidence: 0.75
primary_source: false
```

## Research summary excerpt

> Ran 47 queries across 8 source families over 3 hours. Produced 88 candidates, of which 34 passed the identity-verification gate (≥2 independent identifiers) and 21 met the fit + capacity threshold. Highest-confidence tier includes 6 multi-family offices with disclosed alternatives mandates and 4 CTAs with active multi-manager programs. Notable gaps: X search rate-limited (retry with licensed provider recommended), several single-family offices are intentionally opaque and require direct-outreach discovery. Compliance review is required before any outreach.

## Key discipline points illustrated

- Every claim has an exact source URL and verbatim excerpt.
- Zero-result and rate-limited queries are logged.
- Suitability is `needs_review` — not asserted from public evidence.
- Capacity_score of 72 required verifiable AUA — a property record alone would cap at 45.
- Litigation and regulatory columns are populated even when empty.
