---
name: maximus-fine-tuning
description: "When to fine-tune vs RAG vs prompt engineering, and how to do it right. Covers the decision tree, dataset prep, full fine-tuning, LoRA, QLoRA, instruction tuning, DPO/preference tuning, hosting options (OpenAI/Anthropic FT APIs, HuggingFace, Together, Replicate), eval before promotion, and cost math. Use when deciding how to specialize a model for a task, or when implementing a fine-tune. Trigger phrases: 'fine-tune a model', 'LoRA', 'QLoRA', 'when to fine-tune', 'fine-tune vs RAG', 'DPO', 'instruction tuning', 'PEFT', 'OpenAI fine-tuning API', 'custom model training'."
metadata:
  pillar: ai-engineering
  source: maximus
---

# Maximus — Fine-Tuning

Fine-tuning is a sharp tool. Used right, it teaches a model your specific vocabulary, format, and judgment in ways prompting never will. Used wrong, it's an expensive way to break a model that was working fine. This skill covers the decision, the process, and the economics.

## When to use

- You've exhausted prompt engineering and RAG and the model still can't do the task reliably.
- You need to teach the model a stable format or domain vocabulary that changes prompts can't encode consistently.
- You're reducing inference cost: a smaller fine-tuned model can match a larger base model on a narrow task.
- You need lower latency: a fine-tuned 7B model can be faster and cheaper than GPT-4o for the same narrow task.

**Start with the decision tree** (`references/ft-vs-rag-vs-prompt.md`) before any training work.

## Core rules

1. **Prompt first, then RAG, then fine-tune.** Fine-tuning is the highest-cost, highest-commitment option. Do not reach for it when prompting or RAG would suffice.
2. **Garbage in, garbage out.** 1,000 clean, diverse, correctly labeled examples beat 50,000 noisy ones. See `maximus-ai-data-pipeline` for data quality discipline.
3. **Eval before promotion.** A fine-tuned model that hasn't beaten the baseline on a held-out evaluation set does not go to production. No exceptions.
4. **Pin versions everywhere.** Base model version, dataset version, hyperparameters, training code — all pinned and reproducible. A model you can't reproduce is a model you can't debug.
5. **Cost math is mandatory.** Calculate the break-even point before committing to training. Fine-tuning has fixed training costs; savings come from cheaper per-token inference at scale.

## Procedure

1. **Run the decision tree.**
   - Can prompt engineering alone achieve the task? Try at least 3 different prompting approaches (`maximus-prompt-engineering`).
   - Does the task require knowledge of external documents that change over time? Use RAG (`maximus-rag-pipeline`).
   - Is the task narrow, stable, and format-sensitive? Fine-tuning is the right tool.
   - Is the required model behavior a matter of style/tone/format rather than factual knowledge? Fine-tuning beats RAG for style.
   - See `references/ft-vs-rag-vs-prompt.md` for the full decision tree with examples.

2. **Choose the technique.**
   - **Full fine-tuning**: Update all weights. Requires GPU memory equal to ~6× model parameters in mixed precision (for Adam optimizer). Practical only for models ≤ 7B unless you have multi-GPU setup or use FSDP/DeepSpeed. Best for maximum task alignment.
   - **LoRA (Low-Rank Adaptation)**: Add trainable low-rank matrices to attention layers. Trains ~1% of parameters. Same quality as full FT on most tasks. Practical on consumer GPUs (24 GB VRAM for 7B models). The default choice for most fine-tuning tasks.
   - **QLoRA**: LoRA + 4-bit quantized base weights. Practical on a single 16 GB GPU for 7B models. Small quality trade-off vs. LoRA; large accessibility gain.
   - **Instruction tuning**: Supervised fine-tuning on (instruction, response) pairs. Standard practice for making a base model follow instructions. Use this format for task specialization.
   - **DPO (Direct Preference Optimization)**: Train on (prompt, chosen, rejected) triples without a reward model. Better aligned with human preferences than SFT alone. Use for tone, helpfulness, and safety alignment. Requires a preference-labeled dataset.

3. **Prepare the dataset.**
   - Target size: 100–500 examples for format/style; 1,000–10,000 for task specialization; 10,000+ for domain adaptation. Quality > quantity.
   - Format for instruction tuning: `{"messages": [{"role": "system", ...}, {"role": "user", ...}, {"role": "assistant", ...}]}` (OpenAI Chat format, also used by most open-source trainers).
   - Format for DPO: `{"prompt": ..., "chosen": ..., "rejected": ...}`.
   - Apply full data pipeline discipline: dedup, quality filter, train/val/test split, dataset card. See `maximus-ai-data-pipeline`.
   - See `examples/lora-finetune.py` for the data loading pattern.

4. **Choose a training platform.**
   - **OpenAI Fine-Tuning API**: Supports GPT-4o, GPT-4o mini, GPT-3.5-turbo. Upload JSONL, call the API, get a fine-tuned model ID. Simplest path for OpenAI-based production systems. No GPU infrastructure needed.
   - **Anthropic Fine-Tuning**: Available via partnership/enterprise tier on Claude. Contact Anthropic directly for access.
   - **Hugging Face + AutoTrain / PEFT + TRL**: Open-source stack. Use `transformers` + `peft` + `trl` for LoRA/QLoRA/DPO on any open model (Llama, Mistral, Phi, Gemma). Full control, full responsibility.
   - **Together AI Fine-Tuning API**: REST API, pay-per-GPU-hour, supports major open models. Simpler than self-managed HF infra.
   - **Replicate**: Trains and hosts open models. Good for small teams without MLOps infrastructure.
   - **Modal / Vast.ai / Lambda Labs**: Rent GPU compute by the hour for custom training scripts.

5. **Configure hyperparameters.**
   - Learning rate: 1e-5 to 5e-5 for full FT; 1e-4 to 3e-4 for LoRA (higher allowed because LoRA matrices start from zero).
   - Epochs: 2–5 for instruction tuning. Stop at validation loss convergence, not a fixed epoch count.
   - LoRA rank: 8–64. Higher rank = more parameters = better capacity = more memory. Start at 16.
   - LoRA alpha: typically 2× rank (e.g., alpha=32 for rank=16).
   - Batch size: maximize to fit in VRAM; use gradient accumulation to simulate larger batches.
   - Warmup steps: 3–5% of total training steps.

6. **Evaluate before promotion.**
   - Run the fine-tuned model against the held-out test set.
   - Compare to baseline (base model with your best prompt).
   - Required: fine-tuned model must beat baseline on the primary task metric AND not regress on safety metrics.
   - Check for catastrophic forgetting: test on tasks the base model handles that are adjacent to your fine-tuned task.
   - See `maximus-eval-and-test` for evaluation implementation.

7. **Deploy and monitor.**
   - Register the fine-tuned model with its base model version, dataset version, and hyperparameters.
   - Use the same staged rollout process as any AI feature. See `maximus-ai-product-spec` §staged rollout.
   - Monitor for distribution shift: if production inputs diverge from training inputs, the model degrades. Track input embedding distribution over time.
   - Plan retraining cadence: fine-tuned models go stale. Schedule based on measured performance drift, not calendar.

8. **Calculate cost math.**
   - Training cost: (GPU-hours × $/GPU-hour) or (tokens × $/M tokens for API-based FT).
   - Break-even: if the fine-tuned model uses a cheaper base model or fewer tokens per call, calculate (cost saved per call × monthly call volume) vs. training cost.
   - Rule of thumb: fine-tuning pays for itself at ≥ 50,000 calls/month when replacing GPT-4o with a fine-tuned GPT-4o mini or open 7B model on a narrow task.
   - See HOWTO.md §"How to estimate FT cost vs prompt cost" for the full calculation template.

## Domain notes

- **PEFT** (Parameter-Efficient Fine-Tuning) is the umbrella term for LoRA, QLoRA, prefix-tuning, and adapters. The `peft` library (Hugging Face) implements them all.
- **TRL** (Transformer Reinforcement Learning, Hugging Face) is the standard library for SFT, DPO, and PPO fine-tuning on open models.
- **vLLM** and **llama.cpp** are the standard serving options for fine-tuned open models in production.
- **Mergekit** allows merging a LoRA adapter into the base weights for deployment simplicity.
- Catastrophic forgetting is real. A 3-epoch fine-tune on a narrow task will measurably degrade performance on general tasks. If you need both, evaluate both, and use a system prompt + RAG approach for the general tasks.
- OpenAI's fine-tuning cost (as of mid-2025): GPT-4o mini at ~$0.003/1K training tokens; inference at ~$0.30/1M output tokens vs $0.60/1M for base model. The margin is real but small at low volumes.

## Gotchas

- **Overfitting on format**: a model fine-tuned on 200 examples in a rigid format will refuse to deviate from that format even when the task requires it. Inject format variation in training data.
- **Benchmark contamination via synthetic data**: if you use GPT-4o to generate training data and then evaluate on standard benchmarks, you may be training the model to replicate GPT-4o's benchmark answers. Use held-out evaluation sets.
- **"We'll just fine-tune on the eval set"** is the most expensive way to destroy a benchmark. The eval set is untouchable. Always.
- **LoRA merging artifacts**: merging a LoRA adapter into base weights with a scale factor > 1.0 can cause instability. Test thoroughly post-merge.
- **Forgetting to update the model card and dataset card** when retraining. Every new version needs updated documentation. See `maximus-ai-safety-governance` for model card requirements.

## Output

Decision tree recommendation (FT / RAG / prompt), prepared dataset (JSONL, DVC-tracked), training config file, training run logs (loss curves, eval metrics), fine-tuned model registered with metadata, eval report (fine-tuned vs. baseline on task metric and safety metric), cost math spreadsheet.
