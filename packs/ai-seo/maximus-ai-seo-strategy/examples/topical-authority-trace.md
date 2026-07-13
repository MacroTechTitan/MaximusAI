# Worked example: topical authority plan for "AI-assisted recruiting"

Scenario: a mid-market ATS (applicant tracking system) vendor wants to own the topic of AI-assisted recruiting for talent teams at 50-500 person companies over the next 90 days.

## Step 1 — Bound the topic

**Claim:** "The practical guide to using AI in recruiting workflows for in-house talent teams at 50-500 person companies — not enterprise HR suites, not solo-recruiter tools."

Narrow enough that a 90-day plan can plausibly cover it; broad enough to intersect with the vendor's product (an ATS with AI screening features) and drive commercial intent.

## Step 2 — Map the subtopic tree

Pulled via `search_web` against the seed term and its obvious sub-questions, reading AI Overview panels and "people also ask" boxes, plus a scan of r/humanresources and r/recruiting threads.

Branch 1 — Fundamentals
- What is AI-assisted recruiting (definitions, scope)
- How AI screening tools actually rank candidates
- AI recruiting vs traditional ATS keyword matching

Branch 2 — Evaluation & buying
- Best AI recruiting tools for mid-market teams
- AI recruiting software pricing models
- Build vs buy: in-house AI screening vs vendor tools

Branch 3 — Risk & compliance
- Is AI resume screening legal (bias, EEOC, NYC Local Law 144 style disclosure rules)
- How to audit an AI screening tool for bias
- Candidate disclosure requirements for AI-assisted hiring

Branch 4 — Implementation
- How to roll out AI screening without alienating recruiters
- Measuring time-to-hire improvement from AI tools
- Common failure modes when adopting AI recruiting tools

Branch 5 — Conversational / multi-turn variants (surfaced from reading actual AI Overview answers, not keyword tools)
- "Which of these tools actually reduces bias vs just speeds up screening"
- "What would break if we turned off human review entirely"
- "How do we explain to candidates why an AI touched their application"

## Step 3 — Score current coverage

| Subtopic | Coverage |
|---|---|
| What is AI-assisted recruiting | Weak (old glossary page, no depth) |
| How AI screening ranks candidates | Missing |
| AI recruiting vs traditional ATS | Missing |
| Best AI recruiting tools (mid-market) | Missing (only enterprise-focused comparison exists) |
| Pricing models | Weak (buried in a pricing FAQ) |
| Build vs buy | Missing |
| Is AI resume screening legal | Missing |
| How to audit for bias | Missing |
| Candidate disclosure requirements | Missing |
| Rollout without alienating recruiters | Missing |
| Measuring time-to-hire improvement | Weak (one old case study) |
| Common failure modes | Missing |
| Conversational variants (3) | Missing (highest AI-citation potential — no one answers these directly) |

## Step 4 — Sequence build order

Foundational (must exist before others link to them): "What is AI-assisted recruiting," "How AI screening ranks candidates," "AI recruiting vs traditional ATS." These become the hub-tier pages.

Supporting: buying/evaluation branch and risk/compliance branch — both link back to fundamentals and drive commercial + trust signal.

Advanced/edge-case: implementation branch and the three conversational variants — highest AI-citation potential but need the foundational pages to link from.

## Step 5 — 90-day plan

- **Days 1-30:** Ship the 3 foundational pages (this becomes the cluster hub — see `keyword-cluster-trace.md` for how "How AI screening ranks candidates" becomes the hub with the other two as early spokes). Fix the weak pricing and glossary pages.
- **Days 31-60:** Ship the evaluation branch (3 pages) and risk/compliance branch (3 pages). These are the gap-analysis winners (see Recipe D) — no mid-market-focused competitor covers "is AI resume screening legal" well.
- **Days 61-90:** Ship the implementation branch (3 pages) and the 3 conversational-variant pages, framed as direct-answer sections addressing the compound question rather than generic explainer format. Run first refresh pass on the day 1-30 pages based on early ranking/citation signal from `maximus-seo-visibility-tracking`.

## Step 6 — Authority milestone

By day 90: cited in AI Overviews or chat-assistant answers for at least 5 of the 13 mapped subtopic queries, and ranking top 5 for the 3 foundational queries. Checked via `maximus-seo-visibility-tracking`.

## Handoff

Each page in the sequence above becomes a work item for `maximus-write-article` (drafting), then `maximus-aeo-optimization` (answer-format pass) and `maximus-geo-optimization` (citation-tuning pass), with `maximus-content-seo` handling schema and internal linking mechanics. `maximus-seo-audit` checks the shipped pages against this plan at the day-30 and day-60 marks.
