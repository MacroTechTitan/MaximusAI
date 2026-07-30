# Inference engines for Kimi K3 — reference

Moonshot AI officially supports three inference engines for Kimi K3, per the K3 README §5 ("Deployment"):

| Engine | Repo | K3 recipe |
|---|---|---|
| vLLM | https://github.com/vllm-project/vllm | https://recipes.vllm.ai/moonshotai/Kimi-K3 |
| SGLang | https://github.com/sgl-project/sglang | https://docs.sglang.io/cookbook/autoregressive/Moonshotai/Kimi-K3 |
| TokenSpeed | https://lightseek.org/tokenspeed | https://lightseek.org/tokenspeed/recipes/models#kimi-k3 |

## Decision guide

### Pick vLLM when
- You already run vLLM in production for other models — operational fit dominates raw throughput
- You need the widest possible community and integration surface (LiteLLM, Ray Serve, LangChain, etc.)
- You want an OpenAI-compatible endpoint with minimal glue
- You value stability over cutting-edge features

### Pick SGLang when
- You are running an agentic workload with heavy tool-call sequences
- You need structured decoding (JSON schemas, regex-constrained outputs)
- You want strong support for K3's preserved-thinking mode in a multi-turn agent loop
- You value throughput on long-context batched serving

### Pick TokenSpeed when
- You need optimizations specifically tuned to K3's architecture (KDA + Gated MLA + Latent MoE)
- You are pushing the 1M-context envelope and need engine-level context management
- You are willing to run a newer engine with a smaller community

## What this reference does not tell you

- **Specific throughput numbers.** These change with every release. Consult the engine's own benchmarks, and run your own on your hardware.
- **VRAM minimums.** These change as engines improve MoE serving. Consult the recipe for the current minimum.
- **Latency at load.** Depends on hardware, batch size, request pattern, and `reasoning_effort`. Measure, do not extrapolate.

## Anti-pattern

Do not switch engines mid-deployment based on a single blog post claiming a throughput win. The K3 recipes are the authoritative source; changes to K3's own attention implementation (KDA, Gated MLA) land in each engine at different times. Pick one, get it working end to end, then A/B on your workload.

## Source

- [Kimi-K3 README §5](https://github.com/MoonshotAI/Kimi-K3) — "Deployment"
- Individual engine recipes linked above

Last reviewed: **2026-07-28**.
