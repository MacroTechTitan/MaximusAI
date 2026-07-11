# Worked example — designing a 30-prompt tracking set

Category: **AI-assisted recruiting SaaS** (mid-market companies, 200-2000 employees, hiring volume high enough to justify software spend).

This trace shows the reasoning behind each design decision, then the full 30-prompt set structured as a tracking sheet, following `HOWTO.md` recipe (a).

## Step 1 — Precision on the category

"Recruiting software" is too broad — it would pull in applicant tracking systems, background-check vendors, and payroll platforms that aren't real competitors. "AI-assisted recruiting SaaS for mid-market companies" narrows the field to tools that (a) use AI/ML meaningfully in the product, (b) target the mid-market buyer, not enterprise or SMB. This framing is what should show up in the prompts themselves — buyers describe their own size and need, not a category label.

## Step 2 — Named competitors for this trace

Four named competitors used throughout the comparison-tier prompts: **HireLogic**, **ScreenSmart**, **TalentPilot**, **RecruitIQ** (illustrative names for this worked example — substitute real competitors when running this for an actual brand).

## Step 3 — The 30 prompts, by tier

### Awareness tier (10 prompts — no brand names, category-level)

| ID | Prompt | Notes |
|---|---|---|
| AW-01 | What are the best AI recruiting tools for mid-size companies? | Core category query |
| AW-02 | How can AI help speed up hiring for a 500-person company? | Use-case framing, no product ask |
| AW-03 | What software helps reduce time-to-hire using AI? | Outcome-framed |
| AW-04 | Recommend tools for AI-powered resume screening. | Feature-framed |
| AW-05 | What's the difference between an ATS and an AI recruiting platform? | Educational/definitional |
| AW-06 | How do companies use AI to reduce hiring bias? | Adjacent-concern framing |
| AW-07 | What tools automate candidate sourcing with AI? | Feature-framed, sourcing angle |
| AW-08 | Best recruiting software for a company scaling from 300 to 800 employees. | Growth-stage framing |
| AW-09 | How does AI improve the candidate screening process? | Process-framed, educational |
| AW-10 | What should a mid-market company look for in AI recruiting software? | Buying-criteria framing |

### Comparison tier (10 prompts — named entities, competitive)

| ID | Prompt | Notes |
|---|---|---|
| CM-01 | HireLogic vs ScreenSmart — which is better for mid-market hiring? | Direct competitor pairing |
| CM-02 | What are alternatives to TalentPilot? | Displacement-testing prompt |
| CM-03 | How does RecruitIQ compare to other AI recruiting platforms? | Named-entity, open comparison |
| CM-04 | Is HireLogic good for companies with high hiring volume? | Named-entity, use-case qualifier |
| CM-05 | Compare pricing across top AI recruiting SaaS platforms. | Comparison + pricing angle |
| CM-06 | Which AI recruiting tool integrates best with Workday? | Comparison + integration angle |
| CM-07 | ScreenSmart vs TalentPilot for reducing screening bias. | Named pairing + adjacent concern |
| CM-08 | What do reviewers say are the pros and cons of RecruitIQ? | Sentiment-revealing prompt |
| CM-09 | Best AI recruiting tool according to G2 or Capterra reviews. | Third-party-source framing |
| CM-10 | Which AI recruiting platforms are recommended for regulated industries? | Comparison + compliance angle |

### Decision tier (10 prompts — high intent, close to purchase)

| ID | Prompt | Notes |
|---|---|---|
| DC-01 | Does [YourBrand] integrate with Greenhouse? | Feature-specific, named brand |
| DC-02 | What is the pricing for [YourBrand]'s recruiting platform? | Pricing, named brand |
| DC-03 | Is [YourBrand] suitable for a 600-person healthcare company? | Use-case fit, named brand |
| DC-04 | How long does implementation take for AI recruiting software? | Decision-stage logistics |
| DC-05 | What's the ROI of switching to an AI-assisted recruiting platform? | Business-case framing |
| DC-06 | Does [YourBrand] support multi-language candidate screening? | Feature-specific, named brand |
| DC-07 | What security certifications do AI recruiting platforms typically have? | Procurement/compliance framing |
| DC-08 | Which AI recruiting tool has the best customer support reputation? | Post-sale concern |
| DC-09 | Can [YourBrand] handle hiring for both technical and non-technical roles? | Use-case breadth, named brand |
| DC-10 | What contract terms are typical for mid-market AI recruiting software? | Procurement framing |

## Step 4 — Tracking sheet structure

Columns used in the live spreadsheet (one row per prompt):

`prompt_id | prompt_text | intent_tier | engines_tracked | date_added | date_last_reviewed | status | notes`

Example rows:

```
AW-01, "What are the best AI recruiting tools for mid-size companies?", awareness, "perplexity,chatgpt,gemini,claude,aio", 2026-01-15, 2026-07-01, active, "core category query"
CM-01, "HireLogic vs ScreenSmart — which is better for mid-market hiring?", comparison, "perplexity,chatgpt,gemini,claude,aio", 2026-01-15, 2026-07-01, active, "direct competitor pairing"
DC-01, "Does [YourBrand] integrate with Greenhouse?", decision, "perplexity,chatgpt", 2026-01-15, 2026-07-01, active, "feature-specific, named brand"
```

## Step 5 — Quarterly review note (illustrative)

At the Q3 2026 review, AW-05 ("difference between ATS and AI recruiting platform") was retired — the market had matured enough that this educational question was no longer commonly asked, per a sample of live search/chat query data. It was replaced with AW-11: "What's the best AI recruiting tool for reducing time-to-fill?" — a newer, more outcome-specific phrasing. This change was logged with date, reason, and the exact prompt swapped, per `SKILL.md`'s Methodology transparency requirement.
