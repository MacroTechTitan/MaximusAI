---
title: "Two Kimi K3 skills join Maximus"
date: 2026-07-29
excerpt: "maximus-k3-model-selection and maximus-k3-self-hosting — pick the right frontier model when Kimi K3 is on the shortlist, and run K3 on your own GPUs (or honestly decide not to). Suite now at 39 skills."
---

# Two Kimi K3 skills join Maximus

Moonshot AI shipped [Kimi K3](https://github.com/MoonshotAI/Kimi-K3) — a 2.8T-parameter open-weight MoE with 104B active parameters, a 1,048,576-token context window, native MXFP4/MXFP8 quantization, preserved-thinking mode, and an OpenAI/Anthropic-compatible API on [platform.kimi.ai](https://platform.kimi.ai).

A frontier open-weight model at that scale changes two conversations at once:

1. **Which model do I pick for this task?** K3 is now a real option against Claude Fable 5, Claude Opus 4.8, GPT-5.6 Sol, GPT-5.5, and GLM-5.2 — and the answer is honestly mixed. K3 wins some benchmarks, loses others, and the harness matters.
2. **Do I self-host?** Open weights make self-hosting possible. That does not make it wise. The break-even math and the license terms are non-obvious.

Maximus now ships two skills to handle both.

## maximus-k3-model-selection

A decision skill. Load it when someone asks "should I use K3 for X?" and it walks the 5-step decision:

1. **Extract inputs** — task shape, context length, deployment constraint, license constraint, cost sensitivity.
2. **Score benchmark fit** — using only published K3-report numbers, with harness notes.
3. **Layer non-benchmark constraints** — license, context, self-hosting, preserved-thinking cost.
4. **Deliver the recommendation** — one model, cited benchmarks, honest runner-up section.
5. **Cite freshness** — every number carries a date.

The core rule is the one that makes this skill worth loading:

> Recommend the model that wins the task, not the model in the skill's name.

If GPT-5.6 Sol wins DeepSWE for the user's workload, the skill says so. If Claude Fable 5 wins FrontierSWE, the skill says so. Partisan model advice is worse than no model advice.

Reference bundle includes the full published benchmark table with source URLs, the Kimi K3 License summary and its commercial-use gotchas, and the preserved-thinking cost model — because multi-turn K3 sessions carry a token overhead that vanilla model comparisons ignore.

**Recipes cover:** K3 vs Claude Fable 5 for coding, long-context (>500K) pipelines, open-weight commercial requirements, agentic tool use, "is switching worth it," and cost-dominated workloads.

Skill: [`skills/maximus-k3-model-selection`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-k3-model-selection)

## maximus-k3-self-hosting

An ops skill. Load it when someone is planning, executing, or debugging a K3 deployment on their own GPUs — with a hard "should you self-host at all" gate at the front.

The 6-step workflow:

1. **Should you self-host?** — volume, latency, hardware access, ops maturity. Below ~100M tokens/day sustained and without a dedicated ops bench, the honest answer is "use platform.kimi.ai."
2. **Pick an engine** — vLLM, SGLang, or TokenSpeed. Moonshot officially supports all three, with dedicated K3 recipes for each.
3. **Size the hardware** — using the sizing worksheet and each engine's recipe as source of truth. This skill does not quote GPU counts from memory.
4. **Deploy** — read license, pull weights, follow recipe, smoke-test preserved-thinking, expose OpenAI-compatible endpoint.
5. **Configure preserved-thinking** — with a runnable smoke-test script that catches the #1 K3 integration bug: dropping `reasoning_content` across turns.
6. **Operate** — KV cache, expert-routing observability, weights version pinning, hosted-API fallback.

**Recipes cover:** the self-hosting gate, engine comparison, hardware sizing, preserved-thinking debugging, latency tuning, and the license review triggers for commercial deployment.

The bundle includes a ready-to-run [smoke test](https://github.com/MacroTechTitan/MaximusAI/blob/main/skills/maximus-k3-self-hosting/scripts/smoke_test.py) — a 3-turn preserved-thinking exchange that fails loudly if your client is dropping `reasoning_content` (which most OpenAI-compatible clients do by default).

Skill: [`skills/maximus-k3-self-hosting`](https://github.com/MacroTechTitan/MaximusAI/tree/main/skills/maximus-k3-self-hosting)

## What these two skills share

Both are workhorse skills — no hype, no vendor cheerleading. K3 is a strong frontier model with real strengths and real trade-offs. These skills name both, cite the sources, and refuse to invent numbers that Moonshot did not publish.

Specifically:

- No throughput claims without a source URL
- No hardware counts from memory
- No license permissiveness assumptions (the Kimi K3 License is source-available, not Apache/MIT)
- No K3 recommendation when a competitor wins the user's task

## The suite so far

**Total: 39 skills across 5 pillars.**

- **Cognitive OS (1)** — maximus-brain
- **Build & Ship (10)** — the engineering loop, one skill per stage
- **AI Engineering (14)** — agents, RAG, fine-tuning, MLOps, cost control, safety, UX, and now Kimi K3 model-selection + self-hosting
- **Writing / Research / People (7)** — deep research, people-finding, counterparty discovery, contact intelligence
- **AI SEO Pack (7, opt-in)** — AEO + GEO + technical SEO + citation tracking

Everything open, everything readable as plain Markdown, everything triggered only when the load fits.

## Try them

- Repo: [github.com/MacroTechTitan/MaximusAI](https://github.com/MacroTechTitan/MaximusAI)
- Site: [maximus.macrotechtitan.com](https://maximus.macrotechtitan.com)
- Kimi K3: [github.com/MoonshotAI/Kimi-K3](https://github.com/MoonshotAI/Kimi-K3) · [platform.kimi.ai](https://platform.kimi.ai)
