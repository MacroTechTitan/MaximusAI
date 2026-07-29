# maximus-k3-self-hosting

**Run Kimi K3 on your own GPUs, or decide honestly not to.**

Kimi K3 is Moonshot AI's 2.8T-parameter, 104B-active open-weight MoE, with a 1M-token context and native MXFP4/MXFP8 quantization-aware training. It ships under the source-available [Kimi K3 License](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE). Moonshot officially supports three inference engines: vLLM, SGLang, and TokenSpeed.

This skill handles the deployment lifecycle end to end.

## What you get

- A 6-step deployment workflow (should you self-host → engine choice → hardware sizing → deploy → preserved-thinking config → operate)
- A "should you self-host" gate that recommends `platform.kimi.ai` when volume, latency, or ops maturity do not justify running K3 yourself
- Reference tables for engine trade-offs, hardware sizing inputs, and MXFP4 quantization behavior
- Worked example: a preserved-thinking smoke test that catches the #1 K3 integration bug (dropping `reasoning_content` across turns)
- Worked example: a full deployment plan for a 500M-tokens-per-day workload

## What you do not get

- Model selection versus other frontier models (use `maximus-k3-model-selection`)
- API integration guidance for platform.kimi.ai (use the standard AI Engineering skills)
- Made-up hardware requirements or throughput claims
- Made-up license permissiveness — the Kimi K3 License is source-available, not Apache/MIT

## Core rule

**Self-hosting a 3T-class open-weight model is real work.** If the user's volume and ops maturity do not clear the bar, the honest answer is "use the hosted API." A workhorse says that plainly.

## Files in this bundle

- `SKILL.md` — spec and workflow (loaded by the agent)
- `README.md` — this file
- `HOWTO.md` — 6 recipes for the most common deployment questions
- `examples/smoke-test-preserved-thinking.md` — end-to-end multi-turn smoke test with `reasoning_content` handling
- `examples/deployment-plan-500m-daily.md` — worked deployment plan
- `references/engines-compared.md` — vLLM vs SGLang vs TokenSpeed with source URLs
- `references/hardware-sizing.md` — sizing worksheet based on K3's published architecture
- `references/quantization-mxfp4.md` — what MXFP4/MXFP8 means for VRAM and throughput
- `references/license-and-terms.md` — Kimi K3 License summary and gotchas
- `scripts/smoke_test.py` — small Python script the smoke test walks through

## Source

- Repo: https://github.com/MoonshotAI/Kimi-K3
- Tech report: https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf
- Weights: https://huggingface.co/moonshotai/Kimi-K3
- License: https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE
- Hosted API: https://platform.kimi.ai

## Freshness

Last refreshed against the K3 README on **2026-07-28**. Verify engine recipes at their upstream URLs before deployment — they update independently of this skill.
