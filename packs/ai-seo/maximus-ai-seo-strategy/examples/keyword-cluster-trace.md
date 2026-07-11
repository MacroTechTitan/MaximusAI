# Worked example: keyword cluster design for "vendor management software"

Scenario: a vendor management SaaS company (think: tracking third-party vendors, contracts, risk, and spend for mid-market procurement teams) needs a first content cluster. Seed keyword: **"vendor management software."**

## Step 1 — Seed keyword

`vendor management software` — high-volume head term, transactional-leaning intent, heavily contested by enterprise procurement suites.

## Step 2 — Expand

Via `search_web` on the seed term and its natural variants, plus reading the AI Overview answer text and "people also ask" boxes:

- vendor management software vs vendor management system
- best vendor management software for small business
- vendor management software pricing
- how to choose a vendor management tool
- vendor risk management software
- vendor management software features checklist
- vendor onboarding software
- third-party risk management vs vendor management
- vendor scorecarding tools
- vendor management software integrations (Slack, ERP, procurement)
- "what actually breaks if we manage vendors in spreadsheets past 50 vendors" (conversational variant, surfaced from an AI Overview's own example framing)
- "do we need a dedicated tool or can our procurement system handle this" (conversational variant)

## Step 3 — Classify intent

| Keyword | Intent | AI-citation potential |
|---|---|---|
| vendor management software | Transactional | Low (dominated by 3 entrenched enterprise brands) |
| vendor management software vs system | Informational | Medium (terminology confusion is genuinely underserved) |
| best vendor management software for small business | Transactional | Medium (segment-specific, less contested) |
| vendor management software pricing | Transactional | Medium |
| how to choose a vendor management tool | Informational | High (buying-guide framing is what AI Overviews prefer to cite) |
| vendor risk management software | Transactional | Low (adjacent category, heavily covered) |
| vendor management software features checklist | Informational | High (checklist format is highly extractable) |
| vendor onboarding software | Transactional | Medium |
| third-party risk vs vendor management | Informational | High (definitional confusion, thin existing coverage) |
| vendor scorecarding tools | Informational | Medium |
| vendor management software integrations | Informational | Medium |
| "what breaks past 50 vendors in spreadsheets" | Conversational | High (nobody answers this directly; strong pain-point framing) |
| "do we need a dedicated tool" | Conversational | High (decision-framing question, ideal for direct-answer AEO format) |

## Step 4 — Cluster into hub + spokes

**Hub:** "How to choose a vendor management tool" — broad, comprehensive, buying-guide framing. One-sentence claim: *"The only vendor management buying guide written for procurement teams choosing between spreadsheets, a point tool, and a full suite — not just a features list."* A pure enterprise-suite competitor cannot credibly claim that sentence because they only sell one point on that spectrum.

**Spokes (10):**
1. Vendor management software vs vendor management system (definitional, links to hub)
2. Best vendor management software for small business (segment-specific buying variant)
3. Vendor management software pricing (buying-stage spoke, feeds commercial intent)
4. Vendor management software features checklist (extractable checklist format, high AI-citation potential)
5. Vendor onboarding software (adjacent workflow spoke)
6. Third-party risk management vs vendor management (definitional, high gap potential)
7. Vendor scorecarding tools (evaluation-stage spoke)
8. Vendor management software integrations (technical-fit spoke)
9. What breaks past 50 vendors in spreadsheets (conversational, pain-point framing, links to hub and to the pricing spoke)
10. Do we need a dedicated tool or can our procurement system handle this (conversational, decision-framing, links to hub and to spoke 1)

## Step 5 — Deduplicate intent check

Spokes 1 and 6 both handle terminology confusion but for different term pairs (system vs software; third-party risk vs vendor management) — kept separate since they answer genuinely different reader questions. Spokes 9 and 10 both address "do we even need this," but 9 is pain-point framed (spreadsheet failure) and 10 is decision-framed (build vs buy) — distinct enough to keep separate, with a cross-link between them.

## Step 6 — Internal linking plan

- Every spoke links to the hub in its introduction.
- Spoke 9 <-> Spoke 10 (both address the "do we need this" moment, natural reading path).
- Spoke 1 <-> Spoke 6 (both are definitional/terminology spokes).
- Spoke 3 <-> Spoke 4 (pricing and features checklist naturally sit in the same evaluation session).
- Hub links out to all 10 spokes in a structured "what to read next" section, ordered by the buying journey (definitional -> evaluation -> decision).

## Step 7 — Coverage sanity check

A reader landing only on the hub + 10 spokes could go from "I don't know what this category is" to "I know which type of tool to buy and what to check before signing" without leaving the cluster. No obvious 11th spoke needed at launch; revisit after the first `maximus-seo-visibility-tracking` cycle to see which spoke drives the most AI citations and whether a follow-on spoke (e.g., "vendor management software implementation timeline") is worth adding.

## Handoff

Priority-scored per `references/prioritization-framework.md`, then handed to `maximus-write-article` for drafting in the order: hub first, then spokes 4 and 9 (highest AI-citation potential), then the remaining spokes.
