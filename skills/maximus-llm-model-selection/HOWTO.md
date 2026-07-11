# HOWTO — LLM Model Selection

Concrete recipes for common model selection and routing tasks. Each recipe has a goal, numbered steps, a verification check, and pitfalls to avoid.

---

## Recipe 1: Select a model for a new feature

**Goal:** Choose the right model (and tier) for a new production feature.

**Steps:**

1. **Classify the task.** Write one sentence describing what the model must do. Then assign a complexity tier:
   - *Frontier* — novel reasoning, complex multi-step analysis, ambiguous open-ended problems
   - *Mid-tier* — standard production tasks: RAG generation, agent reasoning, coding assistance, long-document processing
   - *Budget* — high-volume routine: classification, extraction, structured output, summarisation of short text

2. **Check hard requirements.** Does the task need:
   - **Long context (> 128K tokens)?** → Gemini 2.5 Pro (1M) or Claude models (200K); rules out GPT-4o
   - **Multimodal input (images/audio)?** → GPT-4o, Gemini 2.5 Pro, Claude Sonnet 4.5
   - **Data privacy / on-premises?** → Llama 4 or Qwen 3.5 self-hosted
   - **p50 latency < 1s?** → Rules out extended thinking modes
   - **Structured output (JSON schema)?** → All mid-tier and frontier models support it; budget models are reliable too

3. **Start with the mid-tier default.** For most production features: GPT-4.1, Gemini 2.5 Pro, or Claude Sonnet 4.5. These cover 90% of use cases at a fraction of frontier cost.

4. **Test on your eval set.** 20 representative inputs. Measure: quality score (task-specific), latency p50, cost per 1K requests.

5. **Try the budget tier if quality holds.** Run the same eval with GPT-4o mini, Gemini 2.0 Flash, or Claude Haiku 4.5. If quality score drops < 5%, use the budget tier.

6. **Document the decision.** Model name + pinned snapshot, quality score, latency p50, cost/1K, why this model was selected.

**Verification:** Eval quality score ≥ your quality threshold. Latency p50 ≤ latency budget. Decision documented.

**Common pitfalls:**
- Defaulting to the most powerful model "to be safe" — this is correct for prototyping, wrong for production.
- Not testing the task with the actual production prompt — benchmark performance ≠ your task performance.

---

## Recipe 2: Implement rule-based model routing

**Goal:** Route simple tasks to a budget model and complex tasks to a mid-tier model, reducing cost by 30–50%.

**Steps:**

1. Define task types and their tiers in a routing table:
   ```python
   ROUTING_TABLE = {
       # Budget tier: $0.10-$0.80/1M input
       "classification":      "gpt-4o-mini",
       "extraction":          "gpt-4o-mini",
       "structured_output":   "gemini-2.0-flash",
       "short_summarisation": "gpt-4o-mini",
       # Mid-tier: $1.25-$3.00/1M input
       "rag_generation":      "gpt-4.1",
       "coding":              "claude-sonnet-4-5-20251022",
       "long_document":       "gemini-2.5-pro",
       "agent_reasoning":     "gpt-4.1",
       # Frontier: $10-$15/1M input (gate carefully)
       "complex_reasoning":   "o3-2025-04-16",
   }
   ```
2. In your application layer, classify each request before calling the LLM:
   ```python
   def select_model(task_type: str, context_tokens: int = 0) -> str:
       # Hard requirement overrides routing table
       if context_tokens > 128_000:
           return "gemini-2.5-pro"  # only 1M context model
       return ROUTING_TABLE.get(task_type, "gpt-4.1")  # default to mid-tier
   ```
3. Log every routing decision: `{task_type, model_selected, context_tokens, timestamp}`.
4. Review routing logs weekly for the first month. Verify the distribution matches expectations.
5. Measure cost per task type before and after routing. Target: > 30% overall reduction.

**Verification:** In routing logs, ≥ 50% of requests route to budget tier. Quality score on budget-routed tasks is within 5% of mid-tier baseline.

**Common pitfalls:**
- Defaulting unknown task types to the frontier model — default to mid-tier, escalate to frontier explicitly.
- Not logging routing decisions — you can't measure savings or audit misroutes without logs.

---

## Recipe 3: Set up a fallback chain

**Goal:** Ensure availability when the primary model is rate-limited or unavailable.

**Steps:**

1. Define the chain: primary → secondary → tertiary.
   ```python
   FALLBACK_CHAIN = [
       {"model": "gpt-4.1",               "provider": "openai"},
       {"model": "claude-sonnet-4-5-...",  "provider": "anthropic"},
       {"model": "gemini-2.5-pro",         "provider": "google"},
   ]
   ```
2. Implement the fallback wrapper:
   ```python
   def call_with_fallback(messages: list, **kwargs) -> dict:
       for i, tier in enumerate(FALLBACK_CHAIN):
           try:
               return call_model(tier["model"], tier["provider"], messages, **kwargs)
           except (RateLimitError, TimeoutError, ServiceUnavailableError) as e:
               log.warning(f"Model {tier['model']} failed (attempt {i+1}): {e}")
               if i < len(FALLBACK_CHAIN) - 1:
                   time.sleep(2 ** i)  # exponential backoff
               else:
                   raise  # all tiers failed
   ```
3. Log every fallback event: `{primary_model, fallback_model, reason, timestamp}`.
4. Alert when the fallback rate for any primary model exceeds 5% over a rolling 1-hour window.
5. Choose secondary/tertiary from a different provider than primary — provider outages are the most common fallback trigger.

**Verification:** Mock the primary model to always throw `RateLimitError`. Confirm the chain falls back to secondary and completes successfully. Confirm fallback event is logged.

**Common pitfalls:**
- Secondary from the same provider as primary — when the provider is down, both fail simultaneously.
- Not applying backoff — retrying immediately under a rate limit makes the problem worse.
- Not alerting on high fallback rates — sustained fallbacks indicate a capacity problem requiring human intervention.

---

## Recipe 4: A/B test two models for quality comparison

**Goal:** Rigorously compare two models on a production task before switching.

**Steps:**

1. Define the comparison. State: what you're measuring (quality score, latency, cost), the null hypothesis ("model B performs no differently from model A"), and the success threshold ("model B quality score within 5% and cost 20% lower").
2. Use the same eval set for both models. Same prompts, same inputs — do not change the prompt between models unless you're A/B testing the prompt + model combination.
3. Run each model on the full eval set. Collect: quality score per case, latency per case, total cost.
4. Statistical test: for quality scores (0–1), use a paired t-test or Wilcoxon signed-rank test. Sample size ≥ 50 for reliable results.
5. Report: mean quality score, std dev, latency p50/p95, cost per 1K, p-value from statistical test.
6. Promote model B only if: quality is not significantly worse (p > 0.05 or delta < 5%) AND cost / latency improvement meets the threshold.

See `examples/ab-harness.py` for a runnable implementation.

**Verification:** The report includes a p-value. The promotion decision is tied to pre-defined thresholds, not gut feel.

**Common pitfalls:**
- Changing the prompt when switching models and attributing quality differences to the model — isolate the variable.
- Testing on too few examples (< 20) — insufficient statistical power.
- Ignoring latency when quality is equal — the cheaper/faster model is strictly better.

---

## Recipe 5: Pin model versions and handle deprecation

**Goal:** Eliminate silent regressions from floating aliases and manage deprecations as planned events.

**Steps:**

1. **Find all floating aliases** in your codebase:
   ```bash
   grep -r '"gpt-4o"' src/ | grep -v "snapshot\|2024\|2025\|2026"
   grep -r '"claude-sonnet"' src/ | grep -v "\-202"
   grep -r '"gemini-2.5-pro"' src/ | grep -v "\-202"
   ```
2. **Replace each with a pinned snapshot:**
   - `"gpt-4o"` → `"gpt-4o-2024-11-20"`
   - `"claude-sonnet-4-5"` → `"claude-sonnet-4-5-20251022"` (verify latest snapshot with `fetch_url` to provider docs)
   - `"gemini-2.5-pro"` → `"gemini-2.5-pro-preview-05-06"` (check current recommended pin)
3. **Set a deprecation calendar alert** for 90 days before the known EOL date of each pinned snapshot.
4. **When a deprecation notice arrives:** treat it as a planned project. Tasks: (a) identify the replacement snapshot, (b) run your full eval set against the new model, (c) update prompts if needed, (d) deploy, (e) update the pin and reset the deprecation calendar.
5. **Subscribe to provider release notes:**
   - OpenAI: https://platform.openai.com/docs/deprecations
   - Anthropic: https://docs.anthropic.com/en/docs/model-deprecations
   - Google: https://ai.google.dev/gemini-api/docs/models/gemini

**Verification:** `grep` for floating aliases returns zero results. Each model pin has a calendar entry for deprecation review.

**Common pitfalls:**
- Treating deprecation as an emergency — it shouldn't be if you have 90-day runway and an eval set.
- Assuming a new snapshot is drop-in compatible — always re-run your eval set before promoting.

---

## Recipe 6: Decide between API model and self-hosted open source

**Goal:** Make a data-driven build-vs-buy decision on closed-source API vs. self-hosted open-source.

**Steps:**

1. **Calculate API cost at your volume:**
   ```python
   # Rough monthly cost estimate
   daily_requests = 100_000
   avg_input_tokens = 500
   avg_output_tokens = 200
   price_input_per_m = 2.50   # GPT-4.1
   price_output_per_m = 8.00

   monthly_cost = 30 * daily_requests * (
       avg_input_tokens * price_input_per_m / 1_000_000 +
       avg_output_tokens * price_output_per_m / 1_000_000
   )
   ```
2. **Estimate self-hosting cost:**
   - A100 80GB GPU: ~$2.50/hr on AWS/GCP
   - Qwen 3.5 72B requires 2× A100 for fp16 (80GB VRAM)
   - 2× A100 × $2.50 × 730 hr/mo = $3,650/mo (before idle optimization)
   - Throughput: ~500–1000 tokens/sec per A100 pair at fp16
3. **Break-even analysis:** At what monthly token volume does self-hosting cost less than the API?
4. **Add ops cost.** Self-hosting requires engineering time for: deployment, scaling, monitoring, model updates. Estimate 0.25–0.5 FTE/yr for a maintained deployment.
5. **Check non-cost factors:**
   - Data privacy requirement → forced to self-host
   - Fine-tuning requirement → strong reason to self-host (API fine-tuning is expensive and limited)
   - Latency requirement → self-hosting can be faster if GPU is geographically close
   - Team infra expertise → self-hosting is not free of operational complexity
6. **Decision:** If monthly API cost > 2× self-hosting cost AND team has GPU infra capability → evaluate self-hosting. Otherwise, API is the correct default.

**Verification:** A spreadsheet or table with: monthly API cost estimate, monthly self-hosting cost estimate, break-even token volume, non-cost factors, final decision with rationale.

**Common pitfalls:**
- Ignoring ops/engineering cost of self-hosting — it's real and ongoing.
- Comparing API cost at current volume without accounting for growth — self-hosting at 10× volume may be the break-even point.
- Assuming open-source model quality = closed API quality — run your eval set before committing.
