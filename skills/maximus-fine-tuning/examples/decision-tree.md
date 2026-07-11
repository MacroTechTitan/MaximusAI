# Fine-Tuning Decision Tree

Use this document to make a principled, documented decision before committing any training budget.

---

## The three tools

| Tool | What it does | When it's right |
|------|-------------|-----------------|
| **Prompt engineering** | Shapes model behavior through the input: system prompts, few-shot examples, chain-of-thought, output format instructions | Task is within the model's capability; behavior needs adjustment, not fundamentally new knowledge or style |
| **RAG (Retrieval-Augmented Generation)** | Retrieves relevant documents at inference time and injects them into the context | Task requires knowledge from external documents, private data, or information that changes over time |
| **Fine-tuning** | Updates model weights (full FT) or trains adapter parameters (LoRA/QLoRA) on labeled examples | Task is narrow, stable, and format/style-sensitive; prompting + RAG have been tried and fallen short |

These tools compose. You can use all three: a fine-tuned model with a system prompt that retrieves context via RAG.

---

## Decision tree

```
START: Define the task precisely.
       What input does the model receive?
       What output should it produce?
       What does "good" look like? (Write 5 golden examples.)
       ↓

[STEP 1] Can prompt engineering alone achieve the task?
  
  Try at minimum:
  a) Zero-shot prompt (clear instruction, no examples)
  b) Few-shot prompt (3–5 golden examples in the context)
  c) Chain-of-thought prompt (ask the model to reason step-by-step before answering)
  d) Structured output prompt (force JSON or specific format)
  
  Measure task success rate on ≥ 50 representative examples.
  
  Success rate ≥ target? ──── YES ──── STOP. Ship a prompted solution.
                         │
                        NO
                         ↓

[STEP 2] Why is prompting failing?

  A) "The model doesn't know about our internal docs / recent events / private data"
     ──── CAUSE: Missing knowledge → USE RAG (see maximus-rag-pipeline)
     Fine-tuning does not add updatable external knowledge. Do not fine-tune for this.

  B) "The model knows the domain but gives the wrong format / tone / structure"
     ──── CAUSE: Style/format mismatch → FINE-TUNING is a strong candidate
     Fine-tuning is excellent at teaching consistent format, vocabulary, and tone.

  C) "The task is genuinely beyond the current model's capability (complex reasoning)"
     ──── Try a larger model first (GPT-4o → o1, or 7B → 70B).
          If a larger model works but is too expensive → fine-tune a smaller model
          on outputs from the larger model (knowledge distillation pattern).
          If no model works → the task definition or training data is the problem.

  D) "The outputs are inconsistent — sometimes good, sometimes bad"
     ──── CAUSE: Model stochasticity OR distribution mismatch in prompting.
          Add more few-shot examples first. If still inconsistent → fine-tuning.
          ↓

[STEP 3] Does the task require external knowledge that changes over time?

  YES ──── Use RAG. Fine-tuning bakes in a static knowledge snapshot.
  
  You can combine: fine-tune for format/tone, use RAG for knowledge.
  If you combine, RAG quality gates still apply (see maximus-rag-pipeline).
  
  NO ↓

[STEP 4] Volume check — does the economics work?

  Estimate: (current cost per call) × (monthly volume) = monthly inference cost
  Estimate: training cost (one-time) + serving cost (monthly, smaller model)
  
  Monthly call volume < 10,000?
    ──── Prompting is almost certainly cheaper. Fine-tuning won't amortize.
    
  Monthly call volume ≥ 50,000 AND fine-tuned model uses a cheaper base?
    ──── Fine-tuning likely pays for itself. Proceed.
    
  See HOWTO.md §"How to estimate FT cost vs prompt cost" for the calculation.
  ↓

[STEP 5] Data check — do you have enough quality data?

  < 100 examples:
    ──── Not enough. Label more data, or use few-shot prompting.
    
  100–500 examples:
    ──── Enough for format/style fine-tuning. May be enough for simple task FT.
    
  500–5,000 examples:
    ──── Good for task specialization FT. Quality must be high (κ ≥ 0.70).
    
  5,000+ examples:
    ──── Good for domain adaptation or complex task FT.
    
  Are the examples high quality (inter-rater κ ≥ 0.70)?
    NO ──── Fix the data first (see maximus-ai-data-pipeline). Noisy data at scale
            hurts more than small clean data.
    YES ↓

[DECISION] FINE-TUNE.
  Choose technique (see below) → Prepare dataset → Train → Evaluate → Deploy.
```

---

## Technique selection

Once you've decided to fine-tune, choose the technique:

```
Do you need maximum task alignment and have multi-GPU infrastructure?
  YES ──── Full fine-tuning (all weights updated)
  NO ↓

Do you need to fit training on a single 24GB GPU (7B–13B model)?
  YES, and you can afford slight quality trade-off ──── QLoRA (4-bit quantized + LoRA)
  YES, and quality is paramount ──── LoRA (full precision base, adapter layers)
  NO ↓

Do you want to align the model's tone/behavior with human preferences
(not just correct format)?
  YES ──── DPO (requires preference-labeled dataset: prompt + chosen + rejected)
  NO ──── Instruction tuning / SFT (requires instruction-response pairs)
```

### Technique comparison table

| Technique | VRAM (7B model) | Training time | Quality vs full FT | Best for |
|-----------|----------------|---------------|-------------------|----------|
| Full fine-tuning | ~80–120 GB | High | Baseline (100%) | Maximum alignment; multi-GPU setups |
| LoRA | ~24–32 GB | Medium | ~97–99% | Most tasks; single GPU |
| QLoRA | ~12–16 GB | Medium | ~95–97% | Resource-constrained; accessibility |
| Instruction tuning (SFT) | Depends on technique | — | Technique-dependent | Format, task, style alignment |
| DPO | Same as SFT + preference data | Medium-high | +3–8% on preference metrics | Tone, helpfulness, safety alignment |

---

## Common decision mistakes

| Mistake | Correct approach |
|---------|-----------------|
| "Fine-tuning is more powerful, so let's fine-tune" | Try prompting first. Measure. Fine-tune only if prompting fails on measured metrics. |
| "We'll fine-tune on our product docs to teach the model facts" | Facts go stale. Use RAG for factual grounding, fine-tuning for format/style. |
| "We have 50 examples, that's enough to start" | 50 examples is few-shot territory. Label to 200+ before fine-tuning. |
| "Let's fine-tune on our eval set to hit the benchmark" | Never. The eval set is untouchable. See SKILL.md §Core rules. |
| "Fine-tuning once is enough" | Models and data distributions drift. Plan a retraining cadence from day one. |

---

## Decision record template

Document this in the feature spec (`maximus-ai-product-spec`):

```markdown
## Technique decision

**Decision date**: YYYY-MM-DD  
**Decision**: [Prompt engineering / RAG / Fine-tuning / Combined]

**Alternatives considered**:
- Zero-shot prompting: task success rate = [X]% on 50 test examples. Not sufficient because [reason].
- Few-shot prompting (N=5): task success rate = [X]%. Not sufficient because [reason].
- RAG (if considered): [why ruled out / why included]

**Decision rationale**: [Why fine-tuning was chosen]

**Chosen technique**: [Full FT / LoRA / QLoRA / SFT / DPO]

**Cost estimate**: Training = $[X]. Monthly savings vs. current approach = $[Y]. Break-even = [Z] months.

**Data status**: [N] examples available. Inter-rater κ = [X.XX]. Quality gate: [pass/fail].

**Owner**: [Name]
```
