# Worked example — Entity investigation (private company)

**Scenario:** A user asks: *"Investigate [pre-IPO AI infrastructure startup] — what do we actually know, what's the story?"*

For a realistic, non-defamatory example we use a **hypothetical company "Novaflow AI"** so the workflow shape is clear. All specific facts below are illustrative.

## Phase 1 — Lead intake

- **Primary question:** What is Novaflow AI's actual scale, funding, product, and legal exposure?
- **Stakes:** User is considering a partnership. Needs a defensible view before signing.
- **Scope:** Company activity from founding (~2023) through 2026-07. US operations.
- **Known starting sources:** Company website, one TechCrunch profile (Feb 2026).

## Phase 2 — Source mapping

**Primary sources located:**
- Delaware Secretary of State — incorporation filing (2023-04)
- USPTO — 3 patent applications, 1 granted
- LinkedIn — 47 employees listed, up from 12 in Feb 2026
- Company blog — 8 posts, most recent 2026-06
- Corporate press releases — Series A announcement (2024-08), Series B announcement (2026-03)

**Secondary sources:**
- TechCrunch profile (Feb 2026) — the starting source
- The Information — brief in "AI infra roundup," May 2026
- Named analyst commentary (SemiAnalysis newsletter, 1 mention)

**Adversarial sources:**
- Court records: 1 breach-of-contract complaint filed against Novaflow by a former vendor (Q1 2026)
- Glassdoor reviews (as signal, not fact source) — 4.2 avg, 12 reviews
- Former-employee posts on X — 2 identified, both consistent with corporate story

**Gaps:**
- No SEC filings (private, sub-threshold)
- No audited financials
- Series B lead investor unnamed in press release — cannot independently verify

## Phase 3 — Timeline

| Date | Event | Source | Confidence |
|---|---|---|---|
| 2023-04-15 | Incorporated in Delaware | DE Secretary of State filing | high |
| 2023-09 | First patent application filed | USPTO record | high |
| 2024-08-12 | Series A announced — $18M led by [named VC] | Press release + PitchBook | high |
| 2025-04 | First patent granted | USPTO record | high |
| 2026-02-08 | TechCrunch profile published | TechCrunch (direct) | high |
| **2026-Q1** | **Breach-of-contract complaint filed by former vendor** | **CA state court docket** | **high** |
| 2026-03-11 | Series B announced — "$60M" per company blog | Corporate blog + The Information note | medium (unnamed lead) |
| 2026-06 | Latest blog post — product v2 announced | Corporate blog | high |

## Phase 4 — Contradiction hunt

**Claim under investigation:** "Novaflow AI raised $60M Series B led by tier-1 investor" (per corporate blog + TechCrunch)

- **Who benefits from this being true?** The company (fundraising credibility, hiring, sales).
- **Independent corroboration?** The Information notes the raise but does not name the lead. PitchBook has no Series B entry as of the fetch date. No SEC Form D filing found.
- **Adversarial signal?** Breach-of-contract complaint from Q1 2026 (before Series B announcement) suggests vendor unpaid. Could indicate cash-crunch pre-round; could be an unrelated dispute.

**Second claim under investigation:** "Novaflow has 47 employees" (per company blog + LinkedIn)

- LinkedIn shows 47 people with Novaflow AI as current employer.
- Job postings across LinkedIn and Wellfound show 12 open roles.
- Consistent with the company's Q2 growth claim.

**Contradiction found:** The Series B lead investor is publicly unnamed. The company's blog post uses the phrase "led by a leading enterprise-AI investor." Neither PitchBook, Crunchbase, nor The Information can name the lead. This is unusual for a $60M Series B and worth noting.

## Phase 5 — Corroboration pass

| Claim | Single or multi-sourced? | Confidence |
|---|---|---|
| Founded 2023-04 | Multi (state filing + press releases + LinkedIn) | high |
| Delaware incorporation | Primary (state filing) | high |
| 47 employees | Multi (LinkedIn + blog + job postings) | high |
| Series A $18M | Multi (press release + PitchBook + The Information) | high |
| Series B $60M | Single (corporate blog only; secondary mentions do not confirm figure) | **medium** |
| Series B lead investor | **Not disclosed** | cannot confirm |
| First patent granted | Primary (USPTO) | high |
| Product v2 launched | Single (corporate blog) — no third-party validation yet | medium |
| Breach-of-contract complaint | Primary (court docket) | high |

## Phase 6 — Report

### The primary question

What is Novaflow AI's actual scale, funding, product, and legal exposure as of 2026-07-31?

### What we established (high confidence)

- Delaware-incorporated April 2023
- 47 employees as of 2026-07 (from 12 in Feb 2026 — ~4x growth in 5 months)
- Series A of $18M led by [named VC] in Aug 2024 (fully corroborated)
- 3 patent applications, 1 granted
- Active breach-of-contract complaint filed by a former vendor in California state court, Q1 2026

### What we found but cannot fully corroborate

- **Series B of "$60M":** claim appears in company blog only. The Information mentions the round but does not confirm the figure. No PitchBook / Crunchbase entry as of fetch date. No SEC Form D. **Confidence: medium. Recommend requesting verification from the company before treating as fact.**
- **Series B lead investor:** publicly undisclosed. Unusual for a raise of the claimed size. Ask the company or wait for Form D to appear.
- **Product v2 launch:** claim appears in company blog only. No independent customer references or press coverage as of fetch date.

### Contradictions

**Contradiction 1: Series B financial claim vs external record**

- Source A (primary — company blog, 2026-03-11): "$60M Series B led by a leading enterprise-AI investor"
- Source B (adversarial signal — Q1 2026 breach-of-contract complaint from vendor): suggests pre-round cash-flow issue
- Source C (secondary — PitchBook, The Information): confirm round happened, do not confirm size or lead
- Delta: The company's own figure is unconfirmed by any external source. The vendor complaint is consistent with (but does not prove) pre-round cash strain.
- Our reading: **unresolved.** The $60M figure could be accurate but has not passed external verification. The vendor complaint may be unrelated.

### Timeline

[table from Phase 3]

### What we do not know

- Series B lead investor identity
- Series B actual raise size (only the company's claim)
- Revenue, gross margin, or any P&L figures (private, no filings)
- Customer count (company claims "50+" — no verifiable source)
- Outcome of the breach-of-contract case

### Source ledger

| # | Tier | Source | URL | Fetched |
|---|---|---|---|---|
| 1 | primary | DE Secretary of State | [URL] | 2026-07-31 |
| 2 | primary | USPTO | [URL] | 2026-07-31 |
| 3 | primary | Corporate press releases | [URL] | 2026-07-31 |
| 4 | primary | LinkedIn (employee count) | [URL] | 2026-07-31 |
| 5 | primary | CA state court docket | [URL] | 2026-07-31 |
| 6 | secondary | TechCrunch | [URL] | 2026-07-31 |
| 7 | secondary | The Information | [URL] | 2026-07-31 |
| 8 | secondary | PitchBook | [URL] | 2026-07-31 |
| 9 | secondary | SemiAnalysis newsletter | [URL] | 2026-07-31 |

## What this example demonstrates

- The workflow produces a **story with a spine** — the founding through Series B chronology, tied to primary sources
- Contradictions are surfaced (Series B figure unverified, vendor complaint unresolved) rather than smoothed
- Confidence tags are explicit — the user can act on high-confidence items with full trust and treat medium-confidence items appropriately
- Gaps are named ("What we do not know" section)

Compare to an aggregation-mode research report on the same company: that report would summarize the company's own story, present the $60M as a fact, likely miss the vendor complaint, and not distinguish confidence tiers. The investigative-shape report gives the user a defensible view.
