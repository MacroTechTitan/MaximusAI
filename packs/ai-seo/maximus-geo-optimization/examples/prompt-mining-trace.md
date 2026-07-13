# Worked example — Prompt mining trace

**Category:** B2B expense management SaaS (hypothetical brand: "Ledgerly")

This trace shows the full workflow from Recipe A in `HOWTO.md`: source real buyer language, draft candidate prompts, test them against live generative engines, cluster the results, and map clusters to a content plan.

## Step 1 — Source language

Pulled phrasing patterns from (illustrative, not live-fetched) sales call notes, support tickets, and public forum threads in the category:

- "how do I stop employees from submitting duplicate receipts"
- "what's the difference between Expensify and Ramp"
- "best expense software for a 50 person startup"
- "does [tool] integrate with Quickbooks"
- "cheapest expense management tool with mileage tracking"

## Step 2 — Draft 20 candidate prompts

| # | Prompt | Intent cluster |
|---|---|---|
| 1 | What is the best expense management software for a 50-person startup? | Best-for shortlist |
| 2 | Expensify vs Ramp vs Brex for expense tracking | Comparison |
| 3 | Cheapest expense management tool with mileage tracking | Best-for shortlist (price-constrained) |
| 4 | How do I stop employees from submitting duplicate expense receipts? | Troubleshooting / how-to |
| 5 | Does Ramp integrate with QuickBooks? | Feature/integration lookup |
| 6 | What is expense management software? | Definitional |
| 7 | Best free expense tracking app for freelancers | Best-for shortlist |
| 8 | How does automated receipt scanning work? | Definitional / how-it-works |
| 9 | Ramp alternatives for small business | Comparison / alternatives |
| 10 | What expense software works best with Netsuite? | Feature/integration lookup |
| 11 | How much does Expensify cost per user? | Pricing |
| 12 | Best corporate card with built-in expense management | Best-for shortlist |
| 13 | How to set up expense approval workflows | How-to |
| 14 | Is Brex good for startups with international teams? | Suitability / comparison |
| 15 | What's the ROI of automating expense reports? | Definitional / business case |
| 16 | Expense management software with real-time budget alerts | Feature-driven shortlist |
| 17 | How do I audit expense reports for policy violations? | How-to |
| 18 | Best expense tool for remote teams | Best-for shortlist |
| 19 | Difference between corporate card programs and expense software | Definitional / comparison |
| 20 | What expense software has the best mobile app? | Feature-driven shortlist |

## Step 3 — Test against live engines

Each prompt would be run manually against Perplexity, ChatGPT search, and Bing Copilot, logging: which brands are named, which domains are cited as sources, and whether Ledgerly appears. (In a live engagement this step produces a raw log table — brand × engine × cited-or-not — which becomes the visibility baseline handed to `maximus-llm-visibility-tracking`.)

Illustrative finding pattern to expect: incumbents (Expensify, Ramp, Brex) dominate citations on "best-for" and comparison prompts because they have deep third-party mention density (G2, Capterra, TechCrunch coverage, integration marketplace listings). Prompts 4, 8, 13, 15, 17 (how-to/definitional) are usually far more open — fewer incumbents have written the definitive answer, which is where a smaller brand can win a citation first.

## Step 4 — Cluster

| Cluster | Prompts | Competitive density | Priority |
|---|---|---|---|
| Best-for shortlist | 1, 3, 7, 12, 16, 18, 20 | High (incumbents dominate) | Medium — needs 3rd-party mentions, not just owned content |
| Comparison / alternatives | 2, 9, 14, 19 | High | Medium — owned comparison page + PR |
| Feature/integration lookup | 5, 10 | Medium | High — factual, easy to win with a clear integration doc |
| Pricing | 11 | Medium | High — factual, easy to win with a clear pricing page |
| How-to / troubleshooting | 4, 13, 17 | Low | High — open field, first clear answer often wins the citation |
| Definitional / business case | 6, 8, 15 | Low | High — open field, good for structured FAQ content |

## Step 5 — Map to content plan

- **How-to cluster (4, 13, 17):** Publish three standalone how-to guides with FAQ schema, each answering one prompt directly in the H1/first paragraph. Lowest competitive density, highest near-term citation odds.
- **Definitional cluster (6, 8, 15):** One glossary-style pillar page ("What is expense management software," with FAQ blocks for the ROI and receipt-scanning sub-questions).
- **Feature/integration + pricing (5, 10, 11):** Dedicated integration pages per major platform (QuickBooks, Netsuite) and a transparent, regularly-updated pricing page — both are quick wins because incumbents often gate this information behind sales calls, leaving the direct-answer prompt open.
- **Best-for and comparison clusters (1, 2, 3, 7, 9, 12, 14, 16, 18, 19, 20):** Do not rely on owned content alone — route these into the third-party mention plan (Recipe C) targeting G2/Capterra reviews, independent "best expense tools" roundups, and startup-finance newsletters, since incumbent density means owned pages alone rarely win the citation.

## Step 6 — Re-check cadence

Re-run all 20 prompts monthly against the same three engines and log deltas. Feed the log to `maximus-llm-visibility-tracking` as the recurring measurement artifact.
