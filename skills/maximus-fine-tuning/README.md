# maximus-fine-tuning

When to fine-tune — and how to do it right.

## What it is

This skill covers the full fine-tuning workflow: the decision between fine-tuning, RAG, and prompt engineering; dataset preparation; training techniques (full fine-tuning, LoRA, QLoRA, instruction tuning, DPO/preference tuning); training platform selection (OpenAI/Anthropic APIs, Hugging Face, Together, Replicate); evaluation before promotion; and the cost math for when fine-tuning actually pays for itself.

## Why it exists

Fine-tuning is the most misreached-for tool in the AI engineering toolkit. Teams fine-tune when prompting would have worked, or skip fine-tuning when it would have cut costs by 80%. This skill provides the decision framework, the process, and the economics so the right tool gets picked for the right reason.

The problem it solves: expensive, underperforming fine-tuning efforts that happen because the team skipped the decision step, or missed opportunities where fine-tuning would have made a narrow task fast and cheap.

## Quick start

1. **Run the decision tree.** See `references/ft-vs-rag-vs-prompt.md`. Try prompt engineering first. If the task requires external knowledge that changes, add RAG. Fine-tune only when prompting + RAG can't reliably produce the right format, tone, or task behavior.
2. **Prepare the dataset.** Format examples as OpenAI Chat JSONL (`{"messages": [...]}`) or DPO triples (`{"prompt": ..., "chosen": ..., "rejected": ...}`). Apply deduplication, quality filtering, and train/val/test splits. See `maximus-ai-data-pipeline`.
3. **Choose a platform.** For GPT-4o or GPT-4o mini: use the OpenAI Fine-Tuning API. For open models (Llama, Mistral, Phi): use Hugging Face + `peft` + `trl`, Together AI, or Replicate. For enterprise Claude: contact Anthropic.
4. **Train with LoRA first.** Use LoRA rank=16, alpha=32, learning rate 2e-4, 3 epochs. It's faster, cheaper, and within ~1% of full fine-tune performance on most narrow tasks.
5. **Evaluate before promoting.** Run the fine-tuned model against the held-out test set. It must beat the baseline (best-prompt base model) on the primary task metric. If it doesn't, fix the data, not the hyperparameters.

## When NOT to use it

- When prompt engineering hasn't been thoroughly tried. Fine-tuning a model that could be fixed with a better system prompt is expensive and unnecessary.
- When the task requires up-to-date external knowledge. Fine-tuning bakes in knowledge at training time; it goes stale. Use RAG instead.
- When you have fewer than ~100 high-quality labeled examples. You don't have enough data yet. Label more, or use few-shot prompting.
- When call volume is low (< ~10,000 calls/month). The training cost won't amortize at low volume. Use prompting.

## Related skills

- **maximus-prompt-engineering** — the first thing to try before fine-tuning. Often sufficient.
- **maximus-rag-pipeline** — the alternative for knowledge-heavy tasks. Often preferable to fine-tuning for factual grounding.
- **maximus-ai-data-pipeline** — dataset preparation that feeds fine-tuning.
- **maximus-ai-product-spec** — staged rollout and kill switch for the fine-tuned model feature.
- **maximus-eval-and-test** — evaluation implementation for the fine-tuned model.
- **maximus-ai-safety-governance** — model card requirements and bias evaluation for fine-tuned models.
- **maximus-mlops-deploy** — serving and monitoring fine-tuned models in production.

## Glossary

**LoRA (Low-Rank Adaptation)**: A parameter-efficient fine-tuning technique that adds trainable low-rank matrices to the attention layers of a frozen base model. Trains ~0.1–1% of parameters. Standard technique for most fine-tuning tasks.

**QLoRA**: LoRA applied to a 4-bit quantized base model. Reduces VRAM requirements significantly (e.g., a 7B model fits on a 16 GB GPU). Small quality trade-off; large accessibility gain.

**PEFT (Parameter-Efficient Fine-Tuning)**: The umbrella term for techniques (LoRA, QLoRA, prefix-tuning, adapters) that fine-tune a small number of parameters while keeping base model weights frozen.

**DPO (Direct Preference Optimization)**: A technique for aligning model behavior with human preferences using (prompt, chosen, rejected) triples, without requiring a separate reward model. Alternative to RLHF.

**Instruction tuning**: Supervised fine-tuning on (instruction, response) pairs to teach a base model to follow user instructions. Standard practice for making a pre-trained model task-ready.

**Catastrophic forgetting**: The degradation of a model's general capabilities after fine-tuning on a narrow task. More severe with full fine-tuning; mitigated by LoRA and careful data mixing.

**FSDP (Fully Sharded Data Parallel)**: A PyTorch technique for distributing model parameters across multiple GPUs during training. Enables full fine-tuning of large models on multi-GPU clusters.

**TRL (Transformer Reinforcement Learning)**: Hugging Face library implementing SFT, DPO, and PPO trainers for open-source models. The standard library for preference-aligned fine-tuning.

**Break-even point**: The call volume at which the per-call inference savings from a fine-tuned (typically smaller/cheaper) model equals the fixed training cost. Below this volume, prompting is cheaper.

**vLLM**: High-throughput inference server for open-source models. The standard production serving option for fine-tuned open models. Supports tensor parallelism and PagedAttention for efficient batching.
