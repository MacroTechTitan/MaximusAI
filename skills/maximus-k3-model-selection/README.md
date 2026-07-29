# maximus-k3-model-selection

**Pick the right model when Kimi K3 is on the shortlist.**

This is a decision skill, not a build skill. It compares Kimi K3 (Moonshot AI's 2.8T open-weight MoE, 1M context, native MXFP4, preserved-thinking) against Claude Fable 5, Claude Opus 4.8, GPT-5.6 Sol, GPT-5.5, and GLM-5.2 on the published benchmarks from the K3 tech report, then layers license, context, cost, and deployment constraints on top.

## What you get

- A structured 5-step decision workflow (task shape → benchmark fit → constraints → recommendation → freshness check)
- Recommendation templates for four common lanes: long-horizon coding, long context, open-weight/commercial, cost-dominated
- Reference tables of published K3 benchmarks with harness notes and source URLs
- Reference on the Kimi K3 License terms and preserved-thinking cost model

## What you do not get

- Prompt tuning for K3 (use the AI Engineering skills)
- Deployment or self-hosting instructions (use `maximus-k3-self-hosting`)
- Pricing quotes (pricing changes; go to the vendor pages)
- Invented or extrapolated benchmark numbers

## Core rule

**Recommend the model that wins the task, not the model in the skill's name.**

If GPT-5.6 Sol or Claude Fable 5 or GLM-5.2 is the better pick, say so. Cite the benchmark. Do not massage the numbers.

## Files in this bundle

- `SKILL.md` — spec and workflow (loaded by the agent)
- `README.md` — this file, human-first overview
- `HOWTO.md` — recipes for the six most common questions
- `examples/coding-agent-recommendation.md` — worked trace for a real coding-agent selection
- `examples/long-context-recommendation.md` — worked trace for a 500K-token doc pipeline
- `references/k3-benchmarks.md` — full benchmark table with source URLs and harness notes
- `references/license-and-terms.md` — Kimi K3 License summary and gotchas
- `references/preserved-thinking-cost.md` — how preserved-thinking mode changes multi-turn token cost

## Freshness

Benchmarks are pulled from the K3 tech report as of **2026-07-28** and reflect the numbers Moonshot AI published at that time. If more than 90 days have passed, refresh the reference file before relying on the recommendations.

## Source

Repo: https://github.com/MoonshotAI/Kimi-K3
Tech report: https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf
API: https://platform.kimi.ai
