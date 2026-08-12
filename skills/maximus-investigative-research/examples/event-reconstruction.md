# Worked example — Event reconstruction

**Scenario:** A user asks *"reconstruct what actually happened in the [June 2026 AI outage] at [hyperscaler X] — I want a defensible timeline."*

For a realistic, non-defamatory example we use a **hypothetical outage at "Cloudscape"** with public-record shape. All specific details below are illustrative and follow the workflow pattern.

## Phase 1 — Lead intake

- **Primary question:** What was the timeline, cause, and impact of the June 2026 Cloudscape AI-services outage, per public record?
- **Stakes:** User is preparing a partner-facing incident-response postmortem and needs a defensible external-facing timeline.
- **Scope:** 2026-06-14 through 2026-06-21. All public-facing information about the outage.
- **Known starting sources:** Company status page, one Reuters report.

## Phase 2 — Source mapping

**Primary:**
- Cloudscape official status page (archived snapshots via Wayback Machine)
- Cloudscape official postmortem blog post (2026-06-19)
- Cloudscape 8-K filed with SEC (2026-06-17) — material disclosure of the incident
- Twitter/X posts from Cloudscape's verified corporate account with timestamps

**Secondary:**
- Reuters live coverage (2026-06-14 through 2026-06-15)
- Bloomberg follow-up (2026-06-16)
- The Register (technical trade press)
- Downdetector aggregated user reports (as signal, not fact)

**Adversarial:**
- Competitor status pages during the same window (context)
- Analyst notes questioning the postmortem timeline (2 named analysts)
- Enterprise customer public statements about impact

## Phase 3 — Timeline

| Date & Time (UTC) | Event | Source | Confidence |
|---|---|---|---|
| 2026-06-14 14:23 | Cloudscape status page updates: "investigating elevated error rates on AI-Inference API" | Status page (Wayback) | high |
| 2026-06-14 14:47 | First Twitter customer reports spike | Downdetector + user tweets | high |
| 2026-06-14 15:02 | Status page updates: "identified — deployment rollout affected control plane" | Status page (Wayback) | high |
| 2026-06-14 15:15 | Reuters publishes first report | Reuters archive | high |
| 2026-06-14 16:41 | Status page: "mitigation in progress" | Status page (Wayback) | high |
| 2026-06-14 18:30 | Status page: "monitoring — service restored for majority" | Status page (Wayback) | high |
| 2026-06-14 22:14 | Status page: "resolved" | Status page (Wayback) | high |
| **2026-06-15 09:00** | **Second, related outage on the same service** | **Status page + Bloomberg** | **high** |
| 2026-06-15 11:30 | Second outage resolved | Status page | high |
| 2026-06-17 08:00 | Cloudscape files 8-K with SEC — discloses "significant service interruption" | SEC EDGAR | high |
| 2026-06-19 | Full postmortem published on Cloudscape blog | Cloudscape blog | high |
| 2026-06-20 | Analyst A publishes note questioning postmortem's stated root cause | Analyst A note | high |

## Phase 4 — Contradiction hunt

**Claim under investigation (from Cloudscape postmortem):** "Root cause was a bad configuration change in the control plane rollout, deployed at 14:00 UTC on 2026-06-14."

- **Timeline check:** status page shows "investigating" at 14:23 — consistent with a 14:00 deployment triggering issues within 23 minutes.
- **Reuters check:** contemporary Reuters report at 15:15 quotes Cloudscape saying "we are investigating" — matches.
- **Adversarial check:** Analyst A's note (2026-06-20) argues the postmortem understates the *scope* of the impact and did not address the second-day outage's causal link. Analyst A does not dispute the root-cause claim itself.
- **Contradiction found:** the postmortem does not explicitly connect the 2026-06-15 second outage to the same underlying issue. Reuters, Bloomberg, and Analyst A all note the second outage happened on the same service within 24 hours — but Cloudscape's own postmortem frames them as separate.

**Second claim under investigation:** Cloudscape's public statement said "majority of customers restored by 18:30 UTC." The SEC 8-K used "significant service interruption" language.

- **Adversarial check:** three enterprise customers publicly stated they were still degraded past 21:00 UTC.
- **Contradiction:** the "majority restored by 18:30" claim conflicts with named-customer public statements of continued degradation. The company's language ("majority") is technically true if measured by request volume, but the enterprise-customer experience contradicts a simple reading.

## Phase 5 — Corroboration pass

| Claim | Single or multi-sourced? | Confidence |
|---|---|---|
| Outage began ~14:23 UTC on 2026-06-14 | Multi (status page + Reuters + user reports) | high |
| Root cause was control-plane config change | Single (Cloudscape postmortem) — no independent verification | medium |
| Second outage on 2026-06-15 | Multi (status page + Bloomberg) | high |
| "Majority restored by 18:30" | Company statement, contradicted by named-customer statements | medium (partial) |
| Financial impact disclosed as "significant" | Primary (SEC 8-K) | high |
| Named analyst dispute of scope | Primary (analyst note) | high |

## Phase 6 — Report

### The primary question

Reconstruct the June 2026 Cloudscape AI-services outage from public record, with defensible confidence tags.

### What we established (high confidence)

- Outage began approximately 14:23 UTC on 2026-06-14, on the AI-Inference API service (multi-sourced)
- Second, related outage on 2026-06-15 09:00 UTC (multi-sourced, though Cloudscape's postmortem frames these as separate)
- Cloudscape filed an 8-K with SEC on 2026-06-17 disclosing the incident as material
- Cloudscape published a postmortem on 2026-06-19
- Named analyst A (2026-06-20) has publicly questioned the scope characterization

### What we found but cannot fully corroborate

- **Stated root cause** (control-plane configuration change during deployment rollout): appears only in Cloudscape's own postmortem. No independent technical verification exists in the public record. Confidence: medium.
- **"Majority restored by 18:30 UTC"** claim: technically likely true measured by request volume, but three named enterprise customers publicly reported continued degradation past 21:00. Confidence: medium — the company's language and customer experience diverge.

### Contradictions

**Contradiction 1: Framing of the two-day outage**
- Source A (primary — Cloudscape postmortem, 2026-06-19): frames 06-14 and 06-15 as separate incidents.
- Source B (secondary — Bloomberg, 2026-06-16): frames them as related.
- Source C (adversarial — Analyst A note): argues the postmortem "does not adequately address the recurrence."
- Delta: framing, not fact — but material for anyone building a fix or considering exposure.
- Our reading: the second outage on the same service within 24 hours is more plausibly related than not. Cloudscape's postmortem framing may reflect legal caution rather than technical reality. **Unresolved without additional public information.**

**Contradiction 2: Scope of impact**
- Source A (primary — Cloudscape): "majority restored by 18:30 UTC"
- Source B (adversarial — 3 named enterprise customers): continued degradation past 21:00 UTC
- Delta: definition of "majority" — request-volume basis vs customer-experience basis
- Our reading: both are true under different definitions. External communications should note this rather than repeat Cloudscape's phrasing without context.

### Timeline

[table from Phase 3]

### What we do not know

- Technical detail of the configuration change beyond Cloudscape's high-level description
- Financial impact figure (SEC 8-K used qualitative "significant," no dollar figure disclosed)
- Whether the 06-15 outage was fully causally linked to the 06-14 issue
- Enterprise-customer full impact — only 3 spoke publicly; others may have been affected

### Source ledger

| # | Tier | Source | URL | Fetched |
|---|---|---|---|---|
| 1 | primary | Cloudscape status page (via Wayback) | [URL] | 2026-07-31 |
| 2 | primary | Cloudscape postmortem blog | [URL] | 2026-07-31 |
| 3 | primary | SEC EDGAR 8-K filing | [URL] | 2026-07-31 |
| 4 | primary | Cloudscape corporate Twitter | [URL] | 2026-07-31 |
| 5 | secondary | Reuters | [URL] | 2026-07-31 |
| 6 | secondary | Bloomberg | [URL] | 2026-07-31 |
| 7 | secondary | The Register | [URL] | 2026-07-31 |
| 8 | adversarial | Analyst A note (named) | [URL] | 2026-07-31 |
| 9 | adversarial | 3 enterprise customer statements | [URLs] | 2026-07-31 |

## What this example demonstrates

- Timeline built **before** narrative — the sequence is verifiable independent of interpretation
- The two contradictions (framing of two outages, scope of "majority restored") stay in the report as findings, not smoothed away
- Confidence tags let the user cite the multi-sourced items in an external doc and flag the medium-confidence items as "Cloudscape says X — independent verification pending"
- Explicit "What we do not know" section prevents the report from appearing more complete than it is
