---
name: maximus-slm-local-stack
description: "Choose and deploy a small language model (roughly 1B-14B) on hardware you own, for local, private, or offline work. Covers the hardware-tier to model to quantization to runtime decision, explicit VRAM math including KV cache, GGUF quantization tradeoffs, runtime selection (Ollama, LM Studio, llama.cpp, MLX, vLLM), air-gapped install, and benchmarking your own box instead of trusting published tokens/sec. Use when the user says 'run a model locally', 'which SLM', 'small language model', 'offline LLM', 'Ollama', 'LM Studio', 'llama.cpp', 'GGUF', 'quantization', 'how much VRAM', 'will this fit on my GPU', 'air-gapped', or 'no cloud API'. For building a research or learning application on top of the stack, use maximus-local-research-assistant. For datacenter-scale self-hosting, use maximus-k3-self-hosting."
metadata: { "openclaw": { "emoji": "🖲️", "pillar": "ai-engineering", "source": "maximus" } }
---

# Maximus — SLM Local Stack

A draft horse and a pit pony are both horses. You do not get a draft horse by
feeding the pony more oats, and you do not get frontier capability by
quantizing a 4B model more carefully. This skill picks the right small animal
for the work you actually have, then gets it running on the hardware you
actually own.

## Purpose

Take a user from "I want to run this locally" to a working, measured local
inference setup — with an honest statement of what that setup can and cannot
do. The deliverable is a stack decision with the memory arithmetic shown, not
a model name.

The hard part is not installation. Installation is one command. The hard part
is that most local-LLM advice quotes model weights and ignores the KV cache,
so people size a machine for the model and then run out of memory the first
time they paste in a long document.

## Scope boundary

| Need | Skill |
|---|---|
| Pick and run a 1B-14B model on your own hardware | **this skill** |
| Build local RAG, study tools, or a research assistant on top | `maximus-local-research-assistant` |
| Choose between API providers, or route between cloud models | `maximus-llm-model-selection` |
| Self-host a frontier MoE on datacenter GPUs | `maximus-k3-self-hosting` |
| Specialize a small model on your own data | `maximus-fine-tuning` |
| Cut spend on a cloud API bill | `maximus-ai-cost-control` |

## The honest preamble

Before any model recommendation, state the tradeoff plainly. A local SLM buys
privacy, zero marginal cost, offline operation, and no rate limits. It costs
capability, and the loss is not uniform:

- **Holds up well.** Summarization of provided text, extraction to a schema,
  classification, reformatting, translation of common language pairs, code
  completion in a familiar language, and any task where the answer is present
  in the input.
- **Degrades sharply.** Unretrieved factual recall, multi-step reasoning
  chains, long-horizon agentic work, instruction-following under many
  simultaneous constraints, and anything requiring knowledge the model was
  never densely trained on.

A 4B model asked an open-ended factual question is a confident fiction
generator. That is not a prompt problem, and this skill does not pretend
otherwise — the architectural answer is grounding, which is
`maximus-local-research-assistant`.

If the user's task lives in the second list and privacy is not a hard
requirement, say so and recommend an API model. A skill that recommends its
own subject matter unconditionally is marketing, not engineering.

## Core workflow

### 1. Establish the hardware ceiling first

Never start from the model. Start from what the machine has, because that is
the constraint you cannot prompt your way around. Collect:

- **GPU VRAM** in GB, and the GPU family (CUDA, ROCm, or Apple Silicon
  unified memory).
- **System RAM**, which matters because CPU offload of overflow layers is
  possible but slow.
- **Apple Silicon**: unified memory is shared with the OS. Budget roughly
  70-75% of total as usable for inference.

On Apple Silicon, memory bandwidth predicts tokens/sec better than core count.
On discrete GPUs, VRAM sets what fits and bandwidth sets how fast it runs.

### 2. Do the memory arithmetic, out loud

Two terms, and the second is the one people forget.

**Weights.** At Q4_K_M, budget roughly **0.6-0.65 GB per billion parameters**
([CraftRigs VRAM guide](https://craftrigs.com/guides/gpu-vram-calculator-local-llm-model-size-kv-cache/)).
An 8B model lands near 5 GB, a 14B near 9 GB.

**KV cache.** This grows linearly with context length and is the trap. Roughly
**0.75 MB per layer per 1,000 tokens** at FP16 on typical architectures
([CraftRigs](https://craftrigs.com/guides/gpu-vram-calculator-local-llm-model-size-kv-cache/)).
The practical consequence, worth quoting to any user planning long-context
work: for Llama 3.1 8B at FP16 KV, the cache alone is around **4 GB at 32K
context and about 16 GB at 128K — more than the Q4 weights**
([InsiderLLM](https://insiderllm.com/guides/kv-cache-optimization-guide/)).

So the budget is:

```
total ≈ (params_B × bytes_per_weight) + KV_cache(context) + ~1 GB overhead
```

Two levers when it does not fit: reduce target context, or enable KV cache
quantization (Q8 KV roughly halves the cache with modest quality cost). Cutting
weight precision further is the *last* lever, not the first.

### 3. Match a model to the ceiling

Pull specific model names and sizes from
`references/slm-landscape-2026-09.md`, and re-verify them — that file has a
date in its name because this landscape turns over in weeks, not years. Select
on three axes:

1. **Fits** with your real target context, per step 2.
2. **Task shape** — reasoning-heavy, multilingual, multimodal, or coding.
3. **License** — check it if anything commercial is downstream. "Open weights"
   is not "permissive license."

Prefer a **smaller model at higher precision over a larger model crushed to
2-bit**. Below roughly Q3, quality loss stops being academic, and for models
under about 7B it is severe — small models have less redundancy to spare.

### 4. Choose the runtime for the workload shape

The runtime layer matters more than newcomers expect, and much of the
comparison content online confuses wrappers with engines. Ollama and LM Studio
are front-ends over the same two engines underneath — llama.cpp and Apple MLX
([Autonoma](https://getautonoma.com/blog/lm-studio-vs-ollama)). So "Ollama vs
LM Studio" is an ergonomics question, not a performance one.

The real fork is single-user versus concurrent serving:

| Workload | Runtime |
|---|---|
| One developer, any OS, CLI-first | Ollama |
| GUI model browser, Mac or Windows | LM Studio |
| Maximum control, custom flags, enthusiast workstation | llama.cpp directly |
| Apple Silicon, want the fastest path | MLX |
| Multiple concurrent users, NVIDIA/AMD GPU | vLLM |

vLLM's advantage is throughput under concurrency —
[roughly 16-20x Ollama's concurrent throughput](https://codersera.com/blog/ollama-vs-lm-studio-vs-vllm-vs-llama-cpp-vs-mlx-2026/)
— and it is irrelevant for a single user at a laptop. Do not route someone to
vLLM for personal use; the ops burden is real and buys nothing.

### 5. Benchmark the actual box

Published tokens/sec numbers assume a GPU, a quant, a context length, and a
batch size that are probably not yours. Measure before promising anything:

- **Prompt eval (prefill) speed** — governs how long a long document takes
  before the first token.
- **Generation speed** at your real context length, not at 512 tokens.
- **Time to first token** with a realistically full context.
- **Peak memory** while running, to confirm headroom rather than assume it.

Record the numbers with the hardware, model, quant, and context alongside.
A tokens/sec figure without those four is not a measurement.

### 6. Air-gapped and offline setup

When there is no network at runtime, the download step must be done
deliberately in advance:

- Pull model weights on a connected machine, verify checksums, transfer
  physically.
- Pin the runtime version and keep the installer alongside the weights.
- Pre-cache any tokenizer or embedding model too — these are the forgotten
  dependency that breaks an air-gapped install at first run.
- Test with the network physically disabled, not merely firewalled. A tool
  that silently phones home for a manifest will pass a firewall test and fail
  in the field.

### 7. Write down the ceiling

Close with a short statement of what this stack does well, what it should not
be asked to do, and the first upgrade that would change the answer. Users who
know the ceiling stop blaming the prompt.

## Anti-patterns

- **Sizing for weights and ignoring the KV cache.** The single most common
  planning error. See step 2.
- **Quantizing to 2-bit to fit a bigger model.** A well-quantized smaller
  model beats a mangled larger one at the same memory budget, especially under
  ~7B.
- **Recommending vLLM to a solo laptop user.** Concurrency throughput is not
  the constraint; ergonomics is.
- **Quoting benchmark tokens/sec as if portable.** Different GPU, quant, or
  context makes the number fiction. Measure locally.
- **Treating a local SLM as a drop-in for a frontier API model.** It is a
  different instrument with a different competence envelope. Say the envelope
  out loud.
- **Assuming open weights means permissive license.** Read the license when
  anything commercial is downstream.
- **Letting the reference file rot.** If `references/slm-landscape-2026-09.md`
  is more than a couple of months stale, re-verify before quoting it.

## Sibling skills

- **`maximus-local-research-assistant`** — the application layer: grounding,
  local RAG, citation, and verification that make an SLM trustworthy.
- **`maximus-llm-model-selection`** — the cloud-side counterpart, and the
  right skill when privacy is not a hard constraint.
- **`maximus-fine-tuning`** — when a small model needs to be specialized
  rather than merely selected.
- **`maximus-k3-self-hosting`** — the same discipline at the opposite scale.
- **`maximus-brain`** — run the frame/critique loop around any hardware
  recommendation that involves the user spending money.

## Output

A stack recommendation containing: the hardware ceiling as collected, the VRAM
budget with weights and KV cache shown separately, a named model with quant
level and license, a runtime with the reason for that choice, the benchmark
commands to verify it locally, and an explicit statement of the capability
ceiling. Every volatile number carries its source URL and the date it was
pulled.
