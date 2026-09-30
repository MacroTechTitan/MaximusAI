---
name: maximus-slm-local-finetune
description: "Fine-tune a small model on hardware you own and ship it to Ollama: decide whether to fine-tune at all, build the dataset, run LoRA/QLoRA with Unsloth (NVIDIA/AMD/Intel/Mac) or MLX-LM (Apple Silicon), evaluate against the base model, then merge, export GGUF, quantize, and create an Ollama model with the training chat template. Use for 'fine-tune locally', 'LoRA on my GPU', 'QLoRA', 'Unsloth', 'MLX fine-tune', 'export to GGUF', 'put my fine-tune in Ollama'."
metadata: { "openclaw": { "emoji": "🪡", "pillar": "ai-engineering", "source": "maximus" } }
---

# Maximus — SLM Local Fine-Tune

Fine-tuning is the most expensive way to discover that you needed a better
prompt. When it is the right tool, doing it locally is now practical: a 7B
QLoRA fits in single-digit gigabytes. This skill makes you earn the fine-tune,
then carries it all the way into `ollama run` without losing the chat template
on the way.

## Purpose

Produce a local fine-tune that measurably beats the base model on the user's
task, packaged as an Ollama model, with the evaluation that proves it and a
record of every setting needed to reproduce it.

## Scope boundary

| Need | Skill |
|---|---|
| LoRA/QLoRA on your own box → GGUF → Ollama | **this skill** |
| Fine-tune vs RAG vs prompt decision in general; hosted FT APIs; DPO | `maximus-fine-tuning` |
| Dataset curation, labeling, leakage | `maximus-ai-data-pipeline` |
| Proving the tune is better | `maximus-slm-eval` |
| Serving the result | `maximus-ollama-ops` |

## Earn it first

Fine-tune locally only if all three are true:

1. A prompt plus retrieval has been tried and measured, and it falls short on
   **format, style, or a narrow skill**. Fine-tuning teaches behavior. It is a
   poor way to teach facts that change, which is what RAG is for.
2. There are at least a few hundred clean examples of the target behavior, or
   a plan to make them.
3. There is a held-out eval set (`maximus-slm-eval`) and a baseline score.

If any are false, stop and say which one.

## Core workflow

1. **Baseline.** Score the base model on the held-out set with the exact
   prompt format you will train on.
2. **Pick the toolchain by hardware.** Unsloth covers NVIDIA (CUDA capability
   7.0+), AMD, Intel, and Mac. MLX-LM is native on Apple Silicon. Check VRAM
   against the dated table in `references/` (for example, Unsloth lists about
   5 GB for 7B QLoRA and 19 GB for 7B 16-bit LoRA).
3. **Build the dataset in the chat format of the target model.** JSONL with
   `messages` (system/user/assistant), or MLX's `chat` / `tools` /
   `completions` / `text` formats. Deduplicate, strip PII, split
   train/valid/test before looking at the results, and never let test prompts
   leak into train.
4. **Train small first.** QLoRA on a 3-8B model with a short run. Watch
   validation loss. If it rises while training loss falls, you are
   overfitting. On OOM, reduce batch size before anything else.
5. **Evaluate adapter vs base** on the held-out set, same prompt, same
   decoding. No gain means no ship. Also re-run a few general prompts to catch
   collapse elsewhere.
6. **Merge and export.** Unsloth: `save_pretrained_gguf` with a quantization
   method, which also writes a Modelfile carrying the training chat template.
   MLX: `mlx_lm.fuse --export-gguf` exports **fp16 only, and only for Mistral,
   Mixtral, and Llama-style models**. For other architectures, fuse to
   safetensors and convert with llama.cpp.
7. **Quantize and import.** Ollama does not quantize GGUF on import, so
   quantize first (`llama-quantize ... Q4_K_M`). Then `ollama create` from a
   Modelfile whose `TEMPLATE` matches the one used in training.
8. **Re-evaluate the quantized Ollama build.** Quantization can erase a thin
   fine-tune gain. The number that counts is the one from the model you will
   actually serve.
9. **Record it.** Base model and revision, dataset hash, hyperparameters,
   toolchain versions, quant method, and all eval scores, in a `TRAINING.md`
   next to the Modelfile.

## Anti-patterns

- **Fine-tuning facts in.** They go stale and hallucinate at the edges. Use RAG.
- **Mismatched chat template at inference.** Unsloth names this "the most
  common cause" of broken exports.
- **Evaluating the fp16 adapter, shipping the Q4 GGUF.**
- **No held-out set.** Then the claimed improvement is a hope.
- **Training on the eval set by accident** via near-duplicates. Deduplicate
  across splits.
- **Assuming MLX exports any architecture to GGUF.** It does not.

## Output

Dataset splits with hashes, the training config, an eval table (base, adapter,
quantized Ollama build), the Modelfile, and `TRAINING.md`. If the tune did not
beat the base, the output is that finding.
