---
name: maximus-k3-self-hosting
description: Plan and execute a self-hosted Kimi K3 deployment on your own GPUs. Load when the user wants to run K3 outside the platform.kimi.ai hosted API — sizing hardware, choosing vLLM vs SGLang vs TokenSpeed, deploying with native MXFP4 weights and MXFP8 activations, configuring the OpenAI/Anthropic-compatible endpoint, tuning preserved-thinking mode across turns, or deciding whether self-hosting is worth it versus the hosted API. Covers the 2.8T-parameter / 104B-active MoE architecture with 1M-token context and quantization-aware-trained MXFP4 weights. Enforces license review before commercial deployment (Kimi K3 License is source-available, not Apache/MIT). Never invents hardware requirements not published by Moonshot AI or the inference engines. Does not cover model selection versus other frontier models — use maximus-k3-model-selection for that. Every recommendation cites the inference-engine recipe URL and names the exact hardware assumption behind any latency or throughput claim.
---

# WHEN TO USE

Load this skill when the user is planning, executing, or debugging a self-hosted Kimi K3 deployment.

Specific triggers:
- "How do I self-host K3?"
- "vLLM vs SGLang for K3?"
- "What hardware do I need for K3?"
- "How do I serve K3 with MXFP4?"
- "K3 API is slow / expensive — can I run it myself?"
- Any deployment / infra / MLOps question naming K3

# WHEN NOT TO USE

- User is deciding *whether* K3 is the right model → use `maximus-k3-model-selection`
- User is asking how to *build with* K3 via the hosted API → use the standard AI Engineering skills
- User is asking about a different Moonshot model (K2, prior releases) → this skill is K3-specific
- User is asking about mobile / on-device deployment → K3 is not that model

# CORE PRINCIPLE

**Self-hosting is a real commitment.** A 2.8T-parameter open-weight frontier model is not a weekend project. Before recommending self-hosting, name (a) the hardware, (b) the operational load, and (c) the break-even token volume versus the hosted API. If the user's volume is below break-even, say "use platform.kimi.ai" and stop.

# WORKFLOW

## Step 1 — Confirm self-hosting is the right call

Ask (or infer) four things:

1. **Volume:** tokens per day, tokens per month
2. **Latency budget:** p50 / p99 targets
3. **Hardware access:** owned GPUs, cloud rental, or shopping list
4. **Ops maturity:** who runs the inference stack in production

If volume is low (<~100M tokens/day sustained), latency is not tight, and there is no operational bench to run inference, **recommend platform.kimi.ai** and stop. Self-hosting is real work.

## Step 2 — Pick the inference engine

Moonshot AI officially supports three, per the K3 README §5:

- **vLLM** — [https://github.com/vllm-project/vllm](https://github.com/vllm-project/vllm), recipes at [https://recipes.vllm.ai/moonshotai/Kimi-K3](https://recipes.vllm.ai/moonshotai/Kimi-K3)
- **SGLang** — [https://github.com/sgl-project/sglang](https://github.com/sgl-project/sglang), cookbook at [https://docs.sglang.io/cookbook/autoregressive/Moonshotai/Kimi-K3](https://docs.sglang.io/cookbook/autoregressive/Moonshotai/Kimi-K3)
- **TokenSpeed** — [https://lightseek.org/tokenspeed](https://lightseek.org/tokenspeed), recipes at [https://lightseek.org/tokenspeed/recipes/models#kimi-k3](https://lightseek.org/tokenspeed/recipes/models#kimi-k3)

Decision inputs:
- **vLLM:** widest community, most third-party integrations, strong OpenAI-compatible serving
- **SGLang:** stronger on structured decoding and agentic workloads with heavy tool-call sequences
- **TokenSpeed:** newer, optimized for the K3 architecture specifically

**Never claim performance numbers not published in the engine's own docs.** If you cite throughput, cite the source.

## Step 3 — Size the hardware

Kimi K3 is:
- **2.8T total parameters**
- **104B activated parameters** per token (MoE)
- **896 experts, 16 activated per token, 2 shared experts**
- **93 layers** (69 KDA + 24 Gated MLA)
- **1,048,576-token context**
- **Native MXFP4 weights + MXFP8 activations** (quantization-aware trained)

Because K3 is quantization-aware trained at MXFP4, its native VRAM footprint is meaningfully smaller than a bf16 equivalent — but "meaningfully smaller than 2.8T bf16" is still very large. See `references/hardware-sizing.md` for the sizing worksheet.

**Do not quote a specific GPU count from memory.** Point the user to the engine recipes and the K3 report footnotes. The K3 report notes H20 GPUs were used for benchmark reruns; that is a data point, not a full sizing recommendation.

## Step 4 — Deploy

The recipes cover the actual commands. This skill guides the workflow around them:

1. Read the license: [Kimi K3 License](https://huggingface.co/moonshotai/Kimi-K3/blob/main/LICENSE). Legal review before commercial deployment.
2. Pull weights from Hugging Face: `moonshotai/Kimi-K3`.
3. Follow the recipe for your chosen engine. Do not deviate from the recipe until it runs end-to-end.
4. Verify with a smoke test — a preserved-thinking multi-turn exchange (see `examples/smoke-test-preserved-thinking.md`).
5. Expose the OpenAI/Anthropic-compatible endpoint. K3 supports both.

## Step 5 — Configure preserved-thinking

K3 is trained in preserved-thinking-history mode. Your client code **must** echo `reasoning_content` and `tool_calls` back to the model on every follow-up turn in `messages`, not just `content`. See the example in the K3 README §6 and `examples/smoke-test-preserved-thinking.md`.

`reasoning_effort` supports `"low"`, `"high"`, and `"max"` (default `"max"`). Lower it if latency or cost is dominant; measure task performance against your eval before shipping.

Full guides:
- [Kimi K3 Quickstart](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)
- [Thinking Effort](https://platform.kimi.ai/docs/guide/use-thinking-effort)

## Step 6 — Operate

- Monitor token throughput per GPU and p50/p99 latency.
- Watch for expert-routing imbalance across the 896 experts — MoE serving needs routing observability.
- Cache the KV state aggressively for long-context workloads; the 1M window is expensive if you re-encode.
- Version your deployment against the exact Hugging Face weights hash.

# HARD RULES

1. **Never invent a hardware requirement.** If it is not in the K3 report or the engine recipe, do not claim it.
2. **Never quote throughput numbers you cannot cite.** Vague performance claims mislead planners.
3. **Never recommend commercial self-hosting without pointing to the Kimi K3 License.** It is source-available, not Apache/MIT.
4. **Never skip the "should you self-host" gate.** Below break-even volume, `platform.kimi.ai` wins.
5. **Never bypass the recipe.** The vLLM, SGLang, and TokenSpeed teams know K3's quirks better than any general MLOps knowledge does. Follow the recipe first, tune second.
6. **Never assume MXFP4 means "half the VRAM of bf16."** Quantization-aware training changes both weight storage and activation compute — see `references/quantization-mxfp4.md`.

# OUTPUT FORMAT

For a full deployment plan, deliver in this order:

```
## Deploy vs. use hosted?
[one-sentence recommendation with the break-even reasoning]

## Engine choice
[vLLM / SGLang / TokenSpeed + one sentence why]

## Hardware
[point at the sizing worksheet; do not quote GPU counts from memory]

## Deployment steps
1. Read license: [URL]
2. Pull weights: [Hugging Face path]
3. Follow recipe: [URL]
4. Smoke test: [preserved-thinking multi-turn]
5. Expose endpoint

## Preserved-thinking config
[reasoning_effort recommendation + one code example reference]

## Operational watch-outs
- KV cache
- expert routing observability
- weights versioning

## Ask-back
[one sentence naming what would refine the plan]
```

Do not open with hedging. Do not skip the "should you self-host" gate.
