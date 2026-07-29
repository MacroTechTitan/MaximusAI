---
name: maximus-k3-model-selection
description: Decide when Kimi K3 (Moonshot AI's 2.8T open-weight MoE, 104B active, 1M context, MXFP4 native, preserved-thinking) is the right model to pick versus Claude Fable 5, Claude Opus 4.8, GPT-5.6 Sol, GPT-5.5, or GLM-5.2. Load when the user is choosing a model for a specific task, comparing frontier models, budgeting a build, evaluating open-weight vs closed, weighing self-hosting vs hosted API, or asking a "which model should I use" question. Uses only published benchmark data with source URLs, respects the K3 license terms, and never invents scores. Does not cover implementation, deployment, or prompt design — use maximus-k3-self-hosting for deployment and the standard AI Engineering skills for integration. Refuses to recommend K3 when task fit is genuinely worse; a workhorse honest answer beats a partisan one. Every recommendation ships with the specific benchmarks that drove it, the harness those benchmarks used, and the date the numbers were pulled.
---

# WHEN TO USE

Load this skill when the user is choosing a model and Kimi K3 is on the table — either explicitly ("should I use K3?") or implicitly (open-weight frontier work, long-context, agentic coding, self-hosting decision).

Specific triggers:
- "K3 vs [other model] for [task]"
- "Should I switch to K3?"
- "Which model is best for [long-context / coding / agent / multimodal / cheap-per-token]?"
- "Is K3 worth self-hosting?"
- Any procurement / build-vs-buy question involving frontier models where K3 is a candidate

# WHEN NOT TO USE

- User already picked K3 and wants to build → hand off to the standard AI Engineering skills for API integration, or to `maximus-k3-self-hosting` for deployment
- User asks how to prompt K3 → this skill picks the model, it does not tune prompts
- Task fit is clearly not a K3 lane (e.g. sub-second voice latency, on-device mobile) → answer briefly with the standard model-selection heuristics and do not load this skill

# CORE PRINCIPLE

**Recommend the model that wins the task, not the model in the skill's name.** If GPT-5.6 Sol or Claude Fable 5 or GLM-5.2 is the better pick for the user's specific job, say so plainly. Cite the benchmark and the source URL. Do not massage the numbers.

# WORKFLOW

## Step 1 — Extract the decision inputs

Ask the user (or infer from context) five things. Do not skip any.

1. **Task shape** — coding, long-context reasoning, agentic tool use, vision, general chat, multimodal doc extraction, etc.
2. **Context length** — max input tokens expected in a single turn
3. **Deployment constraint** — hosted API only / self-host required / either
4. **License constraint** — commercial use required / research-only OK / must be permissively licensed
5. **Cost sensitivity** — cost-dominated / performance-dominated / balanced

If any input is missing and would change the recommendation, ask once — then proceed.

## Step 2 — Score task fit against the benchmark table

Use `references/k3-benchmarks.md` for the numbers. Never invent or extrapolate scores.

For each candidate model, note:
- The best-fit benchmark(s) for the user's task
- The harness the score was measured under
- Whether K3's number is meaningfully higher, meaningfully lower, or within noise (±1.5 pts)

Score categories from the K3 tech report:
- **Reasoning & knowledge** — GPQA Diamond, CritPt, AA-LCR, HLE-Full
- **Coding** — DeepSWE, ProgramBench, Terminal-Bench 2.1, FrontierSWE, SWE-Marathon, PostTrainBench, MLS-Bench-Lite, SciCode, Kimi Code Bench 2.0
- **Agentic** — BrowseComp, DeepSearchQA, ResearchRubrics, GDPval-AA v2, Toolathlon-Verified, MCPMark-Verified, MCP-Atlas, AutomationBench, JobBench, AA-Briefcase, Agents' Last Exam, APEX-Agents, OfficeQA Pro, SpreadsheetBench 2, OSWorld-Verified, OSWorld 2.0, SaaS-Bench, τ³-Banking, Harvey Lab-AA, CorpFin v2, Finance Agent v2, Legal Research Bench
- **Vision** — WorldVQA, OmniDocBench, PerceptionBench, Video-MME, MMVU, BabyVision, MMMU-Pro, CharXiv, MathVision, ZeroBench

## Step 3 — Layer the non-benchmark constraints

Benchmarks alone do not decide. Overlay:

- **License:** K3 ships under the Kimi K3 License (source-available, model-weights included). Not the same as Apache/MIT. Read it before committing to commercial deployment. See `references/license-and-terms.md`.
- **Context window:** K3 = 1,048,576 tokens. Claude Fable 5 and GPT-5.6 Sol have their own windows; do not assume parity.
- **Self-hosting:** K3 is one of very few 3T-class open-weight models. If self-hosting is a hard requirement, closed models drop out entirely.
- **Multimodal:** K3 handles text + image (native, via MoonViT-V2). Video-MME 90.0 with subs. Not audio.
- **Preserved-thinking cost:** K3 requires `reasoning_content` and `tool_calls` to be echoed back in every follow-up turn — that grows token cost across multi-turn sessions. Budget accordingly.

## Step 4 — Produce the recommendation

Output has five parts, in this order:

1. **Recommendation** — one sentence, one model. Or a short list if two models tie for different sub-tasks.
2. **Why this one** — 2–4 bullets, each anchored to a benchmark with the source citation.
3. **Why not the runner-up** — 1–2 bullets. Honest.
4. **Watch-outs** — license / context / cost / harness caveats that could flip the answer.
5. **Ask-back** — one sentence naming what would change the recommendation, so the user knows what to feed you next time.

Never bury the recommendation. Never open with "it depends."

## Step 5 — Cite freshness

Every benchmark comes with a date and a URL. Numbers older than 90 days get a "stale" tag. If the reference file has not been refreshed in 30 days, say so in the output.

# RECOMMENDATION TEMPLATES

## Template A — Long-horizon coding

> **Pick:** Kimi K3 or GPT-5.6 Sol, depending on harness.
>
> **Why K3:** SWE-Marathon 42.0 vs. GPT-5.6 Sol's 39.0 ([Kimi K3 report](https://github.com/MoonshotAI/Kimi-K3)). Terminal-Bench 2.1 within noise (88.3 vs 88.8, same source). FrontierSWE 81.2 vs. GPT-5.6 Sol's 71.3.
>
> **Why GPT-5.6 Sol instead:** DeepSWE 73.0 vs. K3's 67.5. If your bench looks more like DeepSWE than SWE-Marathon, flip.
>
> **Watch-outs:** K3 SWE-Marathon and Terminal-Bench numbers were measured with the Kimi Code harness; Codex numbers use Codex. Harness matters. See footnotes in the K3 report.
>
> **Ask-back:** Which harness will you actually ship on?

## Template B — Long-context (>200K tokens)

> **Pick:** Kimi K3.
>
> **Why:** 1,048,576-token context, native. BrowseComp 91.2 with context compaction at 300K (90.4 with the full 1M window, no management). See K3 report §3.
>
> **Why not Claude Fable 5 or GPT-5.6 Sol:** Both have shorter effective windows for this class of workload today; check their published limits before rebutting.
>
> **Watch-outs:** Preserved-thinking mode grows the per-turn payload. Budget tokens generously.
>
> **Ask-back:** Is the 1M context a hard requirement, or would 300K plus retrieval work?

## Template C — Open-weight requirement, commercial use

> **Pick:** Kimi K3 if the Kimi K3 License terms fit your use; otherwise GLM-5.2.
>
> **Why K3:** Frontier-class open weights, wins or ties most benchmarks in the K3 report ([source](https://github.com/MoonshotAI/Kimi-K3)).
>
> **Why GLM-5.2:** Different license terms (verify against z.ai's release), simpler serving footprint at smaller sizes.
>
> **Watch-outs:** Read the Kimi K3 License before committing. Do not assume Apache/MIT.
>
> **Ask-back:** What jurisdiction are you deploying in, and does your legal team need to review the license first?

## Template D — Cost-dominated production workload

> **Pick:** GLM-5.2 or a smaller model — not K3, and not Claude Fable 5 / GPT-5.6 Sol.
>
> **Why:** K3 is 2.8T total / 104B active. Serving it economically means self-hosting on H20-class hardware or paying platform.kimi.ai per-token. If cost dominates, drop down.
>
> **Ask-back:** What is your target cost per completion, and what latency budget?

# HARD RULES

1. **Never invent a score.** If it is not in `references/k3-benchmarks.md`, do not use it.
2. **Never present a K3 win as a K3 win without naming the harness.** The K3 report is explicit that harness varies across models.
3. **Never recommend K3 for a task where a competitor clearly wins.** Honest answer beats partisan answer. Every time.
4. **Never quote model API pricing from memory.** Pricing changes. Direct the user to `platform.kimi.ai` and the competing vendors' pricing pages.
5. **Never assume license permissiveness.** The Kimi K3 License is source-available; confirm the terms fit before committing.
6. **When the numbers are within ±1.5 points, say "within noise" and let harness / cost / license decide.**

# OUTPUT FORMAT

Deliver in Markdown, in this exact order:

```
## Recommendation
[one model, one sentence]

## Why this one
- [bullet with benchmark + source URL]
- [bullet with benchmark + source URL]

## Why not the runner-up
- [1–2 bullets, honest]

## Watch-outs
- [license / context / cost / harness caveats]

## Ask-back
[one sentence]
```

Never open with hedging. Never bury the recommendation.
