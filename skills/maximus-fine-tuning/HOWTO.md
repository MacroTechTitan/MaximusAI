# HOWTO — maximus-fine-tuning

Step-by-step recipes for fine-tuning decisions and execution.

---

## Recipe 1: How to decide between fine-tuning, RAG, and prompting

**Goal**: Make a principled, documented decision about which technique to use — before spending any training budget.

**Steps**:
1. **Try prompting first.** Define the task precisely. Write at least 3 different system prompt variants (zero-shot, few-shot with 3 examples, few-shot with 10 examples). Measure task success rate on 50+ representative examples. If success rate ≥ your target: stop here. Ship a prompted solution.
2. **If prompting fails, diagnose why.**
   - Failing because the model lacks knowledge of recent events, documents, or private data → **RAG** (`maximus-rag-pipeline`). Fine-tuning doesn't add updatable knowledge.
   - Failing because the output format is wrong, tone is wrong, or the model won't follow a specific structure consistently → **Fine-tuning** (style/format is the best FT use case).
   - Failing because the task is at the edge of the model's capability (complex reasoning, specialized domain) → try a larger model first. Then consider fine-tuning if cost is prohibitive.
3. **If the task requires external documents that change over time**: use RAG. Fine-tuning bakes in a static knowledge snapshot.
4. **If the task is narrow, format-sensitive, and high-volume**: fine-tuning. A fine-tuned smaller model can match a larger prompted model on a narrow task at lower cost per token.
5. **If you need both knowledge and style**: use both. RAG for retrieval, fine-tuning (or prompting) for format/tone. They compose.
6. Document the decision in the feature spec with: technique chosen, alternatives considered, and the specific failure mode that ruled each out.

**Verification**: Decision is documented with measured task success rates for at least the prompting baseline.

**Common pitfalls**:
- Skipping prompting and going straight to fine-tuning because it "feels more powerful." It's often unnecessary and always more expensive.
- Using fine-tuning to "teach the model facts" — facts go stale. Use RAG.
- Choosing the technique based on what's most interesting to build, not what the task requires.

---

## Recipe 2: How to prepare a fine-tuning dataset

**Goal**: Produce a clean, correctly formatted JSONL dataset ready for instruction tuning or DPO.

**Steps**:
1. **Define the format:**
   - Instruction tuning (SFT): OpenAI Chat format JSONL — one example per line:
     ```json
     {"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
     ```
   - DPO format:
     ```json
     {"prompt": "...", "chosen": "...", "rejected": "..."}
     ```
2. **Determine target size:** format/style tasks: 200–500 examples; task specialization: 1,000–5,000; domain adaptation: 5,000+. More is not always better — noisy data at scale is worse than clean data at smaller scale.
3. **Source examples from real data where possible.** Collect input-output pairs from your existing production system logs (with user consent and PII scrubbing). Real distribution beats synthetic distribution for transfer.
4. **Augment with synthetic data where needed** (see `maximus-ai-data-pipeline` Recipe 2 for safety guards). Tag synthetic examples with provenance metadata.
5. **Apply full data pipeline discipline:** deduplicate (MinHash LSH), toxicity filter, PII scan, label quality check. See `maximus-ai-data-pipeline` SKILL.md.
6. **Split:** 80% train, 10% val, 10% test. Split before any augmentation. For user data, split by user ID.
7. **Validate format:** run a schema validation pass — every JSONL line must parse, every required field must be present, assistant content must not be empty.
8. **Write a dataset card** documenting: source, size, format, split ratios, synthetic fraction, and quality gate results.

**Verification**: `jq -c '.' your_dataset.jsonl | wc -l` matches expected count. No format errors. No PII in any field.

**Common pitfalls**:
- Including the full training dataset prompt in the `system` field of every example. Keep the system prompt short and consistent; it should match the system prompt used at inference.
- Training on outputs that include the model's uncertainty disclaimers ("I'm not sure but...") — the fine-tuned model will reproduce that hedging even when confident.
- Forgetting that the fine-tuned model will reproduce any formatting errors or style inconsistencies in the training data. Review a random 50-example sample manually before training.

---

## Recipe 3: How to run a LoRA fine-tune on an open model

**Goal**: Fine-tune a 7B–13B open model (Llama 3, Mistral, Phi) using LoRA on a single GPU.

**Steps**:
1. **Set up the environment:**
   ```bash
   pip install transformers peft trl datasets accelerate bitsandbytes
   ```
2. **Load the base model and tokenizer** (see `examples/lora-finetune.py` for the complete script):
   ```python
   from transformers import AutoModelForCausalLM, AutoTokenizer
   model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct",
       torch_dtype="auto", device_map="auto")
   ```
3. **Configure LoRA with PEFT:**
   ```python
   from peft import LoraConfig, get_peft_model
   config = LoraConfig(r=16, lora_alpha=32, target_modules=["q_proj","v_proj"],
       lora_dropout=0.05, task_type="CAUSAL_LM")
   model = get_peft_model(model, config)
   ```
4. **Configure SFT trainer with TRL:**
   ```python
   from trl import SFTTrainer, SFTConfig
   training_args = SFTConfig(
       output_dir="./output", num_train_epochs=3,
       per_device_train_batch_size=2, gradient_accumulation_steps=8,
       learning_rate=2e-4, warmup_ratio=0.03,
       evaluation_strategy="steps", eval_steps=100,
       save_strategy="steps", save_steps=100, load_best_model_at_end=True)
   trainer = SFTTrainer(model=model, args=training_args,
       train_dataset=train_ds, eval_dataset=val_ds)
   ```
5. **Train:** `trainer.train()`. Monitor validation loss. Stop when validation loss plateaus or increases (early stopping).
6. **Save the LoRA adapter:** `trainer.model.save_pretrained("./lora-adapter")`. This saves only the adapter weights (typically 10–100 MB), not the full model.
7. **Optionally merge into base weights** (for simpler serving):
   ```python
   from peft import PeftModel
   merged = PeftModel.from_pretrained(base_model, "./lora-adapter").merge_and_unload()
   merged.save_pretrained("./merged-model")
   ```

**Verification**: Validation loss decreases monotonically for the first N steps, then plateaus. Eval perplexity on the val set improves over base model.

**Common pitfalls**:
- `target_modules` varies by model architecture. For Llama models: `["q_proj", "v_proj"]` or `["q_proj", "k_proj", "v_proj", "o_proj"]`. Check the model's attention layer names with `model.named_modules()`.
- Training for too many epochs causes overfitting — the model memorizes training examples instead of generalizing. Use `load_best_model_at_end=True`.
- For QLoRA: add `load_in_4bit=True` and `bnb_4bit_compute_dtype=torch.float16` to the model loading. Reduces VRAM by ~50% at a small quality cost.

---

## Recipe 4: How to evaluate a fine-tuned model before promotion

**Goal**: Verify that the fine-tuned model beats the baseline and doesn't regress on safety or general capability.

**Steps**:
1. **Define evaluation before training.** The test set is locked; it was not used for training or hyperparameter tuning.
2. **Measure primary task metric** on the held-out test set:
   - For generation: human-rated task success rate on 100+ test examples. Use blind evaluation (evaluators don't know which output came from which model).
   - For classification: accuracy, F1, AUC vs. baseline.
   - For format compliance: automated check of schema or format constraints.
3. **Compare to baseline.** Baseline = your best-prompted version of the base model (without fine-tuning). The fine-tuned model must beat the baseline on the primary metric. If it doesn't: the data is the problem, not the hyperparameters.
4. **Check for catastrophic forgetting.** Test on 3–5 tasks adjacent to the fine-tuned task that the base model handles well. Score both base and fine-tuned models. A > 10% regression on adjacent tasks is a red flag.
5. **Run safety evaluation.** Apply the same safety test set used for the base model. A fine-tuned model's safety pass rate must be ≥ base model's safety pass rate (fine-tuning can degrade safety guardrails).
6. **Run latency benchmark.** If the model is now hosted on a smaller GPU or uses 4-bit quantization, verify that P95 latency still meets the budget defined in the product spec.
7. **Document all results in the model card** (from `maximus-ai-safety-governance` Recipe 3). Every version bump gets updated eval results.
8. **Promotion decision.** Fine-tuned model is promoted to staging only if: primary task metric > baseline, safety pass rate ≥ baseline, no catastrophic forgetting beyond threshold. Then follow the staged rollout process from `maximus-ai-product-spec`.

**Verification**: Eval report exists with all five metrics (task, safety, format, forgetting, latency). Baseline comparison is documented.

**Common pitfalls**:
- Evaluating only on the fine-tuning task domain and declaring success. Test adjacent tasks.
- Using the same judge model (e.g., GPT-4o) to evaluate outputs if the training data was also GPT-4o generated. Self-consistency bias inflates scores.
- Promoting based on a single metric. "Task success went up" with no safety check is not a promotion criterion.

---

## Recipe 5: How to estimate fine-tuning cost vs prompt cost

**Goal**: Calculate the break-even point and decide whether fine-tuning is economically justified.

**Steps**:
1. **Estimate current (prompting) cost per call:**
   - Input tokens per call = system prompt tokens + average user message tokens
   - Output tokens per call = average assistant response tokens
   - Monthly cost = (input tokens × input $/M + output tokens × output $/M) × monthly call volume
   - Example (GPT-4o, 1M calls/month, 500 input + 200 output tokens/call):
     - Input: 500M tokens × $2.50/M = $1,250/month
     - Output: 200M tokens × $10/M = $2,000/month
     - Total: $3,250/month
2. **Estimate fine-tuned model cost per call:**
   - If using a fine-tuned GPT-4o mini: same token counts, but input $0.30/M and output $1.20/M
   - Same example: $150 + $240 = $390/month
   - Savings: $2,860/month
3. **Estimate training cost:**
   - OpenAI API-based: training tokens × training cost per M (check current OpenAI pricing — typically ~$25/M for GPT-4o fine-tuning)
   - For 10,000 examples × ~300 tokens each = 3M training tokens: ~$75 one-time
   - Open-source LoRA: GPU hours × $/hour. A 7B model LoRA run on a 2× A100 at $3/h typically completes in 4–8 hours: ~$12–24
4. **Calculate break-even:**
   - Break-even months = training cost / monthly savings
   - In the example: $75 / $2,860 = 0.03 months. Break-even in under 1 day.
5. **Add hidden costs:** data preparation (annotation hours × cost), eval work, ongoing retraining cadence, MLOps infrastructure for serving the model.
6. **Add the risk cost:** a fine-tuned model that performs worse can cost more in user churn, support tickets, or safety incidents than the savings. Quantify this risk and include it in the decision.
7. **Rule of thumb:** fine-tuning pays for itself when: (a) monthly call volume > 50,000, AND (b) the fine-tuned model can use a materially cheaper base than the current prompted model, AND (c) the task is narrow enough that a smaller model can match quality.

**Verification**: A spreadsheet or document exists with the calculation, showing current cost, projected FT cost, training cost, break-even timeline, and hidden cost estimates.

**Common pitfalls**:
- Ignoring annotation cost when calculating training cost. Annotation is often the largest cost line.
- Assuming the fine-tuned model will immediately match the base model quality. Include a ramp period and potential retraining cost.
- Forgetting the ongoing cost: fine-tuned models need retraining as the base model improves or the data distribution shifts. Annualize training cost, not just the initial run.
