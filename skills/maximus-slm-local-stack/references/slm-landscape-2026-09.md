# SLM landscape — pulled 2026-09-22

**This file expires.** Every number below has a source URL and a pull date. The
small-model field turns over in weeks. If today is more than roughly two months
past 2026-09-22, re-verify before quoting any of it, and update the filename
date when you do.

Nothing here is from model memory. If a number has no link, it does not belong
in this file.

---

## 1. Model classes worth knowing

The 1B-14B field currently clusters around four families. Independent roundups
converge on the same set: Qwen3 (1.7B-14B), Google Gemma 3 (1B-12B), Meta Llama
3.2 (1B/3B), and Microsoft Phi-4-mini (3.8B), with
[Codersera](https://codersera.com/blog/best-small-llms-to-run-locally-a-comprehensive-guide/)
naming **Qwen3 the safest all-round default** (pulled 2026-09-22).

Newer Gemma 4 and Qwen 3.5/3.6 generations are shipping; a controlled academic
benchmark of Gemma-4-E2B/E4B/26B-A4B, Phi-4-mini-reasoning, Phi-4-reasoning,
Qwen3-8B, and Qwen3-30B-A3B is on
[arXiv](https://arxiv.org/html/2604.07035v1) — prefer it over vendor blog
claims, and check for a newer version before citing.

**Reasoning ceiling in class.** [Local AI Master](https://localaimaster.com/blog/small-language-models-guide-2026)
(pulled 2026-09-22) puts **Phi-4 at 14B as the strongest overall SLM** at 84.8%
MMLU and fitting a 12 GB GPU; for 8 GB hardware it names **Phi-4-mini (3.8B)**
as the best small reasoner at roughly 3 GB VRAM at Q4, and **Gemma 3 4B** where
multilingual matters.

**Multimodal at small size.** [TinyWeights](https://tinyweights.dev/posts/best-small-language-models-2026/)
(pulled 2026-09-22) reports Gemma 3 4B as the only model in the 3-4B class
handling image input natively, scoring 43.6% MMLU-Pro, 89.2% GSM8K, 71.3%
HumanEval, 75.6% MATH.

**Ultra-constrained.** For phone-class deployment,
[Intuz](https://www.intuz.com/blog/best-small-language-models/) (pulled
2026-09-22) points to Llama-3.2-1B for the best-supported edge runtime path,
and Gemma 3n-E2B-IT for on-device multilingual.

Treat all single-source benchmark scores as vendor-adjacent until reproduced.
MMLU in particular is contaminated enough that a 3-point gap means little.

## 2. VRAM by model at Q4

Per-model figures from [LLM Hardware](https://llmhardware.io/guides/qwen3-hardware-requirements)
and [its Phi-4 guide](https://llmhardware.io/guides/phi4-hardware-requirements)
(both pulled 2026-09-22):

| Model | Params | Q4_K_M VRAM | Notes |
|---|---|---|---|
| Phi-4-mini | 3.8B | ~2.5 GB | Runs on any GPU |
| Qwen3-4B | 4B | ~3 GB | Fits anything, CPU-only viable |
| Qwen3-8B | 8B | ~5 GB | Fits an 8 GB card; thinking mode without a second model |
| Phi-4 | 14B | ~9 GB | 1 GB over an 8 GB card — needs 12 GB |
| QwQ-32B | 32B | ~17 GB | Above SLM class; runs on a 16 GB card per [Compute Market](https://www.compute-market.com/blog/qwen-3-local-hardware-guide-2026) |

**Weights rule of thumb:** ~0.6-0.65 GB per billion parameters at Q4_K_M
([CraftRigs](https://craftrigs.com/guides/gpu-vram-calculator-local-llm-model-size-kv-cache/),
pulled 2026-09-22).

## 3. KV cache — the term people omit

- ~**0.75 MB per layer per 1,000 tokens** at FP16 KV
  ([CraftRigs](https://craftrigs.com/guides/gpu-vram-calculator-local-llm-model-size-kv-cache/)).
- Llama 3.1 8B at FP16 KV: ~**4 GB at 32K**, ~**16 GB at 128K** — exceeding the
  Q4 weights ([InsiderLLM](https://insiderllm.com/guides/kv-cache-optimization-guide/),
  pulled 2026-09-22).
- Worked whole-model example: Llama 3.1 70B at 8,192 context = 43.8 GB weights
  + 6.1 GB KV = 49.9 GB ([CraftRigs](https://craftrigs.com/guides/gpu-vram-calculator-local-llm-model-size-kv-cache/)).
- Formula shape: `KV ≈ 2 × n_layers × n_kv_heads × head_dim × context × bytes`
  ([Morgann Riu](https://morgannriu.fr/en/blog/vram-ram-faire-tourner-llm-local-calcul),
  pulled 2026-09-22).

Mitigation order: shorten target context → quantize the KV cache → only then
touch weight precision.

## 4. Quantization levels

| Level | ~bpw | Verdict |
|---|---|---|
| Q8_0 | 8.5 | Only when maximum fidelity is required and memory is abundant |
| Q6_K | 6.6 | Near-lossless, rarely necessary |
| Q5_K_M | ~5.5 | Worth it with spare memory and complex reasoning |
| **Q4_K_M** | ~4.8 | **Default.** Best quality/speed balance |
| Q3_K | ~3.4 | Noticeable degradation, especially under 7B |
| Q2_K | 2.56 | ~27% of FP16 size, significant perplexity increase; only defensible above ~30B |

Sources: [QuantizeLab](https://quantizelab.dev/gguf-quantization) and
[bswen](https://docs.bswen.com/blog/2026-03-15-gguf-quantization-guide/), both
pulled 2026-09-22.

**Magnitude of the Q4_K_M penalty.** Roughly **0.05-0.1 perplexity versus full
precision on 8B-70B models**, while using ~15% less RAM than Q5_K_M and running
10-15% faster ([Misar](https://www.misar.blog/@synor/articles/gguf-q4km-vs-q5km),
pulled 2026-09-22).

**Quantization strategy beats bit count.** Q4_K_M measures a +0.0535 perplexity
delta versus FP16 where legacy Q4_0 measures +0.2499 — same bit budget, far
better allocation ([Morgann Riu](https://morgannriu.fr/en/blog/quantification-gguf-q4-q5-q8-choisir),
pulled 2026-09-22). Never accept a bare "4-bit" claim; the scheme matters.

## 5. Runtimes

Ollama and LM Studio both wrap the same two engines — llama.cpp and Apple MLX
([Autonoma](https://getautonoma.com/blog/lm-studio-vs-ollama), pulled
2026-09-22), so choose on ergonomics. The layered view (front-ends: Ollama, LM
Studio, Jan, GPT4All, Open WebUI; engines: llama.cpp, MLX, ExLlamaV3, MLC-LLM)
is laid out in [this dev.to survey](https://dev.to/sreeraj-sreenivasan/the-complete-guide-to-local-llm-inference-tools-in-july-2026-llamacpp-ollama-vllm-sglang-and-4mh1),
with llama.cpp MIT-licensed and genuinely open source.

Selection by workload shape, from
[Codersera](https://codersera.com/blog/ollama-vs-lm-studio-vs-vllm-vs-llama-cpp-vs-mlx-2026/)
(pulled 2026-09-22): Ollama or LM Studio for a single-user laptop, llama.cpp or
ExLlamaV3 for an enthusiast workstation, vLLM or SGLang for multi-user serving,
TensorRT-LLM with Triton for NVIDIA production scale. vLLM reaches roughly
**16-20x Ollama's concurrent throughput** — a number that only matters with
concurrent users.

## 6. Integration note

Claude Code sends requests in the Anthropic Messages API format, and setting
`ANTHROPIC_BASE_URL` redirects them to any server speaking that format —
now including Ollama, LM Studio, and llama.cpp natively
([KDnuggets](https://www.kdnuggets.com/pairing-claude-code-with-local-models),
pulled 2026-09-22). This is the bridge between a local stack and the
`mtt-claude-cursor` workflow in `packs/devops`.

## 7. What to re-check on refresh

1. Current generation of each family (Qwen, Gemma, Llama, Phi) and whether the
   size classes shifted.
2. Whether per-model VRAM tables still match shipped architectures.
3. Whether KV cache quantization defaults changed in llama.cpp or vLLM.
4. License terms — these change between releases within the same family.
5. Whether a new engine displaced one named in section 5.
