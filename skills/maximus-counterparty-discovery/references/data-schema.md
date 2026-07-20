# Data and Export Schema

## candidates.csv

`candidate_id,name,entity_type,relationship_target,organization,title,city,state,country,website,public_profile_url,fit_summary,capacity_summary,liquidity_event_summary,regulatory_summary,litigation_summary,forum_summary,minimum_check_fit,accreditation_status,suitability_status,identity_confidence,fit_score,capacity_score,intent_score,source_quality_score,risk_penalty,total_score,last_verified_at,review_status,analyst_notes`

Allowed status values:
- `accreditation_status`: verified, self_attested, inferred_unverified, unknown
- `suitability_status`: verified, needs_review, unknown, unsuitable
- `review_status`: new, verify, approved_for_outreach, rejected, do_not_contact

## evidence.csv

`evidence_id,candidate_id,claim_type,claim_text,source_id,source_url,source_title,source_publisher,source_type,event_date,published_at,observed_at,verbatim_excerpt,confidence,primary_source,contradicts_evidence_id,notes`

## source_log.csv

`source_id,source_family,provider_or_site,query_text,query_url_or_endpoint,started_at,completed_at,status,result_count,relevant_count,pagination_depth,rate_limit_or_access_issue,terms_basis,notes`

Log unsuccessful and blocked searches with `result_count=0` or the applicable status.

## Scoring

Score each component from 0-100.

- Fit: mandate, strategy, counterparty type, geography, minimum size, timing.
- Capacity: verified AUM/net-worth proxy, disclosed allocations, qualifying liquidity events.
- Intent: direct statements, prior investments, active searches, forum or interview evidence.
- Source quality: primary-source coverage, freshness, identity certainty, corroboration.
- Risk penalty: regulatory issues, litigation, sanctions, fraud indicators, stale identity, privacy concerns.

`total_score = 0.35*fit + 0.30*capacity + 0.20*intent + 0.15*source_quality - risk_penalty`

Clamp to 0-100. A single weak wealth proxy cannot yield `capacity_score > 45`. Pseudonymous forum content alone cannot yield `identity_confidence > 35` or `intent_score > 50`.
