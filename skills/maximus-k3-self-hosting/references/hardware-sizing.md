# Hardware sizing worksheet — Kimi K3

**Read this first:** This is a *worksheet*, not a specific hardware recommendation. Specific GPU counts change as inference engines improve MoE serving. Consult the [vLLM](https://recipes.vllm.ai/moonshotai/Kimi-K3), [SGLang](https://docs.sglang.io/cookbook/autoregressive/Moonshotai/Kimi-K3), or [TokenSpeed](https://lightseek.org/tokenspeed/recipes/models#kimi-k3) recipe for the current published minimums.

## Published architecture (from K3 README §2)

| Property | Value |
|---|---|
| Total parameters | 2.8T |
| Activated parameters (per token) | 104B |
| Number of layers | 93 (69 KDA + 24 Gated MLA) |
| Number of dense layers | 1 |
| Attention hidden dimension | 7168 |
| Number of attention heads | 96 |
| Latent MoE dimension | 3584 |
| MoE hidden dimension (per expert) | 3072 |
| Number of experts | 896 |
| Selected experts per token | 16 |
| Number of shared experts | 2 |
| Vocabulary size | 160K |
| Context length | 1,048,576 |
| Attention mechanism | KDA & Gated MLA |
| Activation function | SiTU-GLU |
| Vision encoder | MoonViT-V2 (401M params) |
| Quantization | MXFP4 weights, MXFP8 activations (QAT) |
| Modality | Text, Image |

## What matters for sizing

1. **Total weights = 2.8T at MXFP4.** MXFP4 stores each weight in ~4 bits. Raw weight footprint is on the order of terabytes, not bf16-equivalent.
2. **Active weights per token = 104B.** MoE serving means the memory bandwidth pattern is 104B, but the *storage* requirement is still the full 2.8T because you cannot predict which experts will fire.
3. **1M context KV cache.** With 93 layers and 7168 hidden, the KV cache at max context is substantial. Engines mitigate this with paged attention, but plan for it.
4. **Vision encoder adds 401M.** Small in the context of 2.8T but not free.

## Break-even reasoning (self-host vs hosted API)

The skill's Step 1 gate says: below sustained ~100M tokens/day, self-hosting rarely wins. The math is roughly:

- **Hosted API cost** = tokens × price/token from [platform.kimi.ai](https://platform.kimi.ai) (check current pricing)
- **Self-hosted cost** = GPU rental or amortized capex + power + ops + engineering time
- Below ~100M/day sustained, the fixed cost of running the stack usually exceeds the API bill

This is a rule of thumb, not a guarantee. For high-latency-sensitivity workloads, self-hosting can win at lower volume; for high-compliance workloads, self-hosting is the only option.

## Where to get real numbers

- **VRAM minimum:** the engine recipe you choose. Check the recipe page.
- **Throughput:** the engine's own benchmark reports, plus your own load test.
- **Latency:** measure on your hardware with your `reasoning_effort` setting.
- **Hardware Moonshot themselves used for recent benchmark reruns:** the K3 report footnotes name H20 GPUs for several benches (SWE-Marathon reruns, PostTrainBench). That is a data point about training-adjacent workloads, not a serving recommendation.

## What this file must never do

- Never quote a specific GPU count as "the answer."
- Never claim MXFP4 makes K3 fit on N GPUs without pointing at the engine recipe.
- Never compare throughput between engines without a source URL.

## Source

- [Kimi-K3 README §2 "Model Summary"](https://github.com/MoonshotAI/Kimi-K3)
- [Kimi-K3 tech report PDF](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf)
- Engine recipes linked above

Last reviewed: **2026-07-28**.
