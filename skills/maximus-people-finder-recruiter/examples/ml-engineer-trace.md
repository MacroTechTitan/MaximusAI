# Worked trace — ML Engineer, Production LLM Experience

This is an illustrative worked trace demonstrating GitHub + academic-paper + LinkedIn triangulation for a technically deep IC role. As with the backend trace, treat placeholders as illustrative of the method — every real run must back each slate row with a live, fetched URL (see `SKILL.md` Anti-patterns: no hallucinated profile URLs, no ghost candidates).

## Step 1 — Intake

Brief as given: "We need an ML engineer who's actually shipped LLM stuff to production, not just fine-tuned a model in a notebook."

Structured intake:

- **Role & level**: ML Engineer, mid-to-senior (3-7 years, assumed from "actually shipped" language implying past production ownership)
- **Stack**: Python (must-have), LLM serving/inference experience (must-have — vLLM, TGI, Triton, or equivalent), evaluation/observability for LLM systems (nice-to-have)
- **Location / remote**: not specified — assumed remote-friendly, no geographic filter applied
- **Comp band**: not specified — flagged as an open question for the recruiter, not assumed
- **Must-haves**: production deployment of an LLM-backed feature (not research-only), inference-serving system experience, Python
- **Nice-to-haves**: published research/papers, open-source contributions to inference-serving frameworks, cost/latency optimization experience
- **Disqualifiers**: research-only background with zero production deployment evidence
- **Target companies**: none named — sourcing is title/skill-led rather than company-led for this role, given the specific and rare must-have combination
- **DEI**: none specified

## Step 2 — Role Decomposition

The key decomposition insight: "fine-tuned a model" and "shipped an LLM feature to production" are different competencies and the brief explicitly wants the second. Core competencies: inference-serving infrastructure, latency/cost tradeoffs at serving time, eval pipelines for non-deterministic outputs, Python + typically PyTorch/JAX familiarity.

Because this is a rare, specific combination, decomposition points to three source types rather than a company list: GitHub (serving-framework contributions), academic papers (systems-track LLM papers, not just modeling papers), and LinkedIn (for current-role/title confirmation).

## Step 3 — Boolean Query Build

1. LinkedIn X-ray: `site:linkedin.com/in ("ML engineer" OR "machine learning engineer") ("LLM" OR "large language model") (production OR "shipped" OR serving)`
2. LinkedIn X-ray variant: `site:linkedin.com/in ("applied scientist" OR "ML engineer") (inference OR "model serving") (vLLM OR "Triton Inference Server" OR TGI)`
3. GitHub: search for contributors to `vllm-project/vllm`, `huggingface/text-generation-inference`, and similar inference-serving repos, filtered to recent (last 6 months) commit activity
4. Academic: `search_vertical` vertical=`academic` for recent papers on LLM serving/inference systems (not modeling papers) to identify systems-track authors
5. GitHub secondary: search `topic:llm-inference` and `topic:model-serving` repos for maintainers/frequent contributors

## Step 4 — Multi-Source Search

Executed all 5 queries. Raw pool: **37 hits** — 19 LinkedIn, 12 GitHub, 6 academic-paper authors (systems track, not pure-modeling papers).

## Step 5 — Enrichment

Cross-referenced across all three source types:
- GitHub contributors were checked against LinkedIn for current employer/title.
- Academic-paper authors were checked against GitHub (do they have an associated repo/implementation) and LinkedIn (are they currently in an industry ML engineering role, not purely academic).
- LinkedIn-only hits without a GitHub or paper corroboration were treated as single-signal.

After enrichment, **14 candidates** had two or more corroborating signals — notably, several of the strongest candidates triangulated across all three source types (a systems paper + a GitHub repo implementing it + a current LinkedIn title matching the must-have).

## Step 6 — Fit Scoring

Scored against the rubric. This role's must-have gate is strict: "production deployment" had to be evidenced (not inferred from a title like "ML Engineer" alone — plenty of ML engineers never touch serving). **4 candidates were cut** here for having strong research signal but no clear production-serving evidence — a classic false-positive this loop is designed to catch (the exact failure mode the brief was written to avoid).

**10 candidates** cleared the must-have gate.

## Step 7 — Verification

Live-checked every remaining URL and re-confirmed the production-deployment claim had a direct source (e.g., a conference talk describing the deployed system, a GitHub repo with production-grade serving code and recent activity, or a company engineering blog post naming the person). **2 candidates were cut** — one had a paper + GitHub repo but the LinkedIn identity match was ambiguous (common name, no strong secondary tie), one had stale evidence (production system described was from a company they left 4+ years ago with no evidence of continued relevant work since).

**8 candidates verified** — minimum-viable slate.

## Step 8 — Delivery

Delivered as a CSV with the standard columns, ranked by fit score, plus a sourcing memo:

- Queries run: 5 (2 LinkedIn X-ray, 2 GitHub, 1 academic)
- Sources covered: LinkedIn, GitHub, academic papers (systems track)
- Funnel: 37 raw -> 14 enriched -> 10 passed must-have gate -> 8 verified
- Notable pattern: the highest-fit candidates in this search triangulated across all three source types — when sourcing rare technical combinations, academic + GitHub + LinkedIn triangulation outperforms any single source run in isolation.
- Suggested next-channel expansion: conference speaker lists (NeurIPS/MLSys systems track, not the main ML track) and Kaggle is explicitly de-prioritized here since it under-indexes for production-serving experience relative to pure modeling skill.

This trace shows why the loop routes to different source weightings per role — the same 8 steps, but step 3's query set and step 4's source mix change with what the must-haves actually require.
