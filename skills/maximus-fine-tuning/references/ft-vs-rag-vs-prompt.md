# Reference: Fine-Tuning vs RAG vs Prompt Engineering

Quick reference for technique selection. For the full decision tree, see `examples/decision-tree.md`.

---

## One-line summary

- **Prompt engineering**: Adjust behavior without touching weights. Always try first.
- **RAG**: Inject external knowledge at inference time. Use when the model needs to know things it wasn't trained on.
- **Fine-tuning**: Change the model's weights. Use when prompt + RAG can't reliably produce the right behavior on a narrow, stable task.

---

## When each technique is the right tool

### Prompt engineering is right when:

- The base model already has the underlying capability; it just needs direction.
- The behavior needs to change frequently (prompt changes are instant; retraining takes days).
- Budget is limited (prompting is zero training cost).
- You haven't measured that prompting fails yet. (If you haven't measured, you don't know. Measure.)

**Signs prompting won't be sufficient**:
- The model consistently ignores format instructions even with 10+ few-shot examples.
- The model needs to adopt a specific domain vocabulary or abbreviation system that isn't in its training data.
- Context window is too small to fit all necessary few-shot examples.
- Per-call cost from long system prompts is unsustainable at scale.

---

### RAG is right when:

- The task requires knowledge from private documents (internal wikis, product docs, customer data).
- The knowledge changes over time (news, prices, regulations, product updates).
- The model needs to cite specific sources.
- The knowledge base is large and can't fit in the context window.

**Signs RAG won't be sufficient alone**:
- The task is format/style-sensitive and prompting can't enforce it reliably.
- Retrieval quality is poor and injecting retrieved context makes outputs worse. (Retrieval problem, not a RAG vs. FT problem.)
- The model needs to synthesize patterns across many documents, not look up specific facts.

**RAG + FT together**: Fine-tune for format/tone/style; use RAG for factual grounding. Common and effective.

---

### Fine-tuning is right when:

- The task is **narrow**: one well-defined input type and one well-defined output type.
- The task is **stable**: the definition of correct output doesn't change frequently.
- The task is **format/style-sensitive**: the model needs to adopt a specific output structure, vocabulary, or tone that prompting can't enforce consistently.
- The task is **high-volume**: the per-token cost savings from a smaller fine-tuned model amortize the training cost.
- Prompting and RAG have been **measured** and fall short.

**Signs fine-tuning is the wrong tool**:
- The task requires up-to-date factual knowledge → use RAG.
- You have fewer than 100 quality examples → label more first.
- Call volume is < 10,000/month → prompting is cheaper; FT won't break even.
- The behavior needs to change weekly → fine-tuned models are slow to update; use prompting.

---

## Comparison table

| Dimension | Prompt Engineering | RAG | Fine-Tuning |
|-----------|-------------------|-----|-------------|
| Training cost | None | Index build (one-time) | Medium–high (one-time) |
| Per-call cost | Higher (long prompts) | Medium (retrieval + context) | Lower (smaller/faster model) |
| Time to deploy | Hours | Days | Days–weeks |
| Update speed | Instant | Fast (re-index) | Slow (retrain) |
| Knowledge freshness | Static (base model) | Dynamic (updates with index) | Static (training snapshot) |
| Format/style consistency | Medium | Medium | High |
| Task alignment | Medium | Medium | High (narrow) |
| General capability preservation | Full | Full | Partial (forgetting risk) |
| Data requirement | None | Documents only | Labeled input-output pairs |
| Infrastructure | Minimal | Retrieval system | Training compute + serving |

---

## Cost model summary

### Prompt engineering cost

```
Monthly cost = (system_prompt_tokens + avg_user_tokens) × input_$/M tokens
             + avg_output_tokens × output_$/M tokens
             × monthly_call_volume
```

### RAG cost

```
Index build = (total_doc_tokens × embedding_$/M) — one-time
Monthly cost = prompt_engineering_cost (often slightly higher context)
             + embedding API cost per query (small)
```

### Fine-tuning cost

```
Training cost (one-time) = training_tokens × training_$/M tokens    [for API-based FT]
                          OR GPU hours × $/GPU-hour                 [for open-source FT]

Monthly inference cost = (avg_input_tokens × new_input_$/M
                        + avg_output_tokens × new_output_$/M)
                        × monthly_call_volume

Monthly savings = (old_monthly_cost - new_monthly_cost)

Break-even months = training_cost / monthly_savings
```

**Rule of thumb**: Fine-tuning breaks even in < 2 months when:
- Monthly call volume ≥ 50,000
- The fine-tuned model uses a model tier that is ≥ 50% cheaper per token than the current model
- The task is narrow enough that the cheaper model matches quality

---

## Reference architectures

### Pattern 1: Prompt-only (simplest)
```
User query → System prompt (static) + User message → LLM → Response
```
Use when: task is within model capability, volume is low, behavior changes often.

### Pattern 2: RAG
```
User query → Embedding → Vector search → Top-K docs → LLM (query + context) → Response
```
Use when: task requires private or changing knowledge.

### Pattern 3: Fine-tuned model
```
User query → Fine-tuned LLM (smaller/faster) → Response
```
Use when: narrow, stable, high-volume task; prompting + RAG insufficient.

### Pattern 4: Fine-tuned model + RAG (most capable, most complex)
```
User query → Fine-tuned LLM (format/style) + RAG (knowledge) → Response
```
Use when: the task requires both reliable format AND up-to-date knowledge. Typical in enterprise assistants.

### Pattern 5: Distillation (large model → small model)
```
Queries → GPT-4o (teacher) → High-quality outputs
Outputs → Fine-tune smaller model (student) on teacher outputs
Deploy student model at lower cost
```
Use when: GPT-4o achieves the quality target but is too expensive at scale. Fine-tune a 7B model on GPT-4o outputs.

---

## Common combinations in production

| Product type | Typical approach |
|-------------|-----------------|
| Customer support chatbot | Fine-tuned small model for tone/format + RAG for product knowledge |
| Code autocomplete | Fine-tuned model (CodeLlama, Starcoder) on internal codebase |
| Document Q&A | RAG-only (no fine-tuning needed) |
| Content moderation classifier | Fine-tuned small classifier (DistilBERT, RoBERTa) — not an LLM |
| Named entity extraction (structured) | Fine-tuned for format; few-shot prompting often sufficient |
| Personalized writing assistant | RAG (user's previous writing) + prompted base model |
| Enterprise FAQ assistant | RAG for knowledge + fine-tuning for company tone |
