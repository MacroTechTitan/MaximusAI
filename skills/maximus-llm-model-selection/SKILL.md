---
name: maximus-llm-model-selection
description: "Pick the right LLM for production: capability tiers (frontier vs mid vs small), cost vs latency vs quality tradeoffs, when to use local/open-source (Llama, Qwen, Mistral), routing strategies, fallback chains, A/B harness, and deprecation handling. Use when the user says 'which model should I use', 'too expensive', 'too slow', 'should I use open source', 'model routing', 'fallback if rate limited', 'model upgrade', 'A/B test models', or any task requiring a deliberate model choice or cost optimisation. Based on mid-2026 pricing and capabilities."
metadata:
  pillar: ai-engineering
  source: maximus
---

# Maximus — LLM Model Selection

Picking a model is like choosing a plough horse for the field: a heavy Clydesdale for breaking new ground, a nimble quarter horse for quick work, a small pony for the footpath. Using the wrong one costs you money, time, or both. This skill is the decision framework for choosing well — and for routing intelligently between them at runtime.

## When to use

- Choosing a model for a new feature or pipeline.
- Cutting inference costs on a running production system.
- Deciding between closed-source API models and self-hosted open-source models.
- Implementing routing (send complex queries to a frontier model, simple ones to a cheap model).
- Setting up fallback chains (rate limit on primary → fall back to secondary).
- Managing a model deprecation or upgrade.
- A/B testing two models for quality comparison.

If the problem is the prompt, not the model, load `maximus-prompt-engineering`. If the problem is agent orchestration, load `maximus-agent-design`.

## Core rules (non-negotiable)

1. **Match capability to task.** Don't use a frontier model for a task a budget model handles equally well. The price spread is up to 400× between the cheapest and most expensive; routine tasks should not pay frontier prices.
2. **Measure before switching.** A model change is a prompt change — test the new model against your eval set before promoting to production. Load `maximus-eval-and-test`.
3. **Pin to snapshots in production.** Never use floating aliases (e.g., `gpt-4o`, `claude-sonnet`) in production. Pin to dated snapshots. Floating aliases update without warning.
4. **Read before edit.** Check the current model config with `read` before changing it.
5. **Routing saves real money.** Intelligent routing reduces costs by 40–85% (RouteLLM on MT-Bench: 85% cost reduction at 95% of GPT-4 quality). Budget routes for simple tasks are not a compromise — they are correct engineering.
6. **Deprecation is a planned event.** Monitor provider deprecation notices. A 90-day runway for migration is normal; treat it as a scheduled engineering task.

## Procedure

1. **Classify the task.** Is this a complex reasoning task, a standard production task, or a high-volume simple task? (See tier table below.)
2. **Check capability requirements.** Does the task require: long context (> 200K tokens)? Multimodal input? Tool calling? Structured output? Code generation? These constrain your options.
3. **Set the cost and latency budget.** What's the maximum acceptable p50 latency? Maximum cost per 1K requests?
4. **Select a model (or model pair for routing).** Use the tier table and tradeoffs below.
5. **Test the model against your eval set.** At minimum: 20 representative queries, measure quality score and latency.
6. **Implement routing if applicable.** Route by task complexity (classifier or heuristic) to appropriate tier.
7. **Set up fallback chain.** Primary → secondary → tertiary. Each with retry logic and logging.
8. **Pin the model version.** Replace floating aliases with dated snapshots.
9. **Set a deprecation reminder.** Calendar alert for known EOL dates; subscribe to provider release notes.

## Capability tier table (mid-2026)

| Tier | Models | Context | Input $/1M | Output $/1M | Best for |
|------|--------|---------|-----------|------------|---------|
| **Frontier** | Claude Opus 4 (Anthropic), o3 (OpenAI) | 200K | $15 / $10 | $75 / $40 | Complex reasoning, multi-step analysis, novel tasks |
| **Strong mid** | GPT-4.1 (OpenAI), Claude Sonnet 4.5 (Anthropic), Gemini 2.5 Pro (Google) | 200K–1M | $2–$3 | $8–$15 | Production workloads, RAG, agents, coding, long docs |
| **Budget** | GPT-4o mini (OpenAI), Gemini 2.0 Flash (Google), Claude Haiku 4.5 (Anthropic) | 128K–1M | $0.10–$0.80 | $0.40–$4 | Classification, extraction, high-volume tasks |
| **Local / open-source** | Llama 4 Scout/Maverick (Meta), Qwen 3.5 72B (Alibaba), Mistral Small 4 (Mistral) | 128K–10M | Compute only | Compute only | Privacy-sensitive data, cost elimination, offline, fine-tuning |

## Cost vs. latency vs. quality tradeoffs

- **Cost:** Budget tier is 10–100× cheaper than frontier. For 70% of production traffic (routine, well-bounded tasks), budget models match frontier quality. Route aggressively.
- **Latency:** Budget models are generally faster (smaller, less compute per token). Frontier models with extended thinking (o3, Claude Opus 4 extended) can take 30–120s — unsuitable for synchronous user-facing features.
- **Quality:** Frontier models win on: novel reasoning, complex multi-step tasks, ambiguous instructions, difficult code. Budget models match frontier on: classification, extraction, summarisation, structured output, repetitive tasks.
- **Context window:** Gemini 2.5 Pro (1M tokens) and Claude models (200K) dominate for long documents. GPT-4o is mid-pack at 128K. Llama 4 Scout supports 10M tokens but at self-hosting cost.

## When to use open-source / local models

| Reason | Model recommendation |
|--------|---------------------|
| Data privacy (PII, regulated data cannot leave premises) | Llama 4 Maverick or Qwen 3.5 72B on-premises |
| Zero inference cost at scale (> 10M tokens/day) | Qwen 3.5 or Mistral Small 4 self-hosted |
| Fine-tuning for domain specialisation | Llama 4 or Qwen 3.5 (permissive Apache 2.0 license) |
| Very long context (> 200K tokens) without per-token cost | Llama 4 Scout (10M context, free under 700M MAU) |
| Offline or air-gapped environments | Any GGUF model via llama.cpp or Ollama |

Open-source trade-offs: no per-token cost, but you pay for GPU infra, ops, and latency tuning. Break-even vs. API typically at 1–5M tokens/day depending on GPU cost.

## Routing strategies

1. **Rule-based routing** (lowest overhead): classify task type at the application layer → assign to tier. Example: `if task_type in ("classification", "extraction") → budget_model`. Captures 30–50% cost reduction with zero added latency.
2. **Complexity heuristic routing**: estimate query complexity (length, presence of reasoning keywords, domain signals) → route to tier. Simple heuristic: short queries + structured output → budget; long queries + open-ended → mid/frontier.
3. **Cascade routing**: try the budget model first; if confidence is low (or output fails validation), escalate to a higher tier. Highest quality parity, adds latency for the escalated fraction.
4. **Managed routing**: OpenRouter, Not Diamond, Martian, Unify — provide out-of-box routing, fallback, and observability. Best for rapid deployment; less control than custom routing.

## Fallback chains

```
Primary (strong mid) → timeout/rate-limit
  → Secondary (different provider, same tier) → timeout/rate-limit
    → Tertiary (budget model) → always available
      → Hard failure (return error, alert on-call)
```

Implement with a wrapper that catches `RateLimitError`, `Timeout`, and `ServiceUnavailable` and routes to the next chain member. Log every fallback event.

## Domain notes

- **Prompt caching.** Claude (Anthropic) offers 4× cheaper cached input ($0.30/1M vs $1.25 for GPT-4o). For RAG pipelines with repeated system prompts, Claude's effective cost is often lower despite higher list price.
- **Batch APIs.** OpenAI and Anthropic both offer 50% batch discounts for non-real-time jobs (results within 24h). Nightly eval runs, document processing pipelines, and bulk extraction should use batch.
- **Extended thinking.** o3 and Claude Opus 4 extended thinking are powerful but expensive and slow. Gate them on tasks that demonstrably need them. Most production tasks don't.
- **Model deprecation timeline.** Providers typically give 6–12 months notice on model retirement. Subscribe to provider release notes. Pin snapshots; when a snapshot is deprecated, treat migration as a planned project with testing.

## Gotchas

- **Floating aliases in production** (`gpt-4o`, `claude-sonnet`): they silently update. Your prompt stops working one morning with no warning. Always pin.
- **Benchmark ≠ your task.** MT-Bench and MMLU rankings do not predict performance on your specific domain. Run your own evals.
- **Routing overhead.** A classifier-based router adds 200–500ms latency. For latency-critical paths, use heuristic routing (zero added latency) instead.
- **Cost per session vs. cost per token.** Agentic tasks with many tool calls accumulate output tokens fast. Budget at the session level, not just per request.
- **Open-source infra ops burden.** Self-hosting requires: GPU provisioning, model serving stack (vLLM, TGI, Ollama), autoscaling, monitoring, version management. Factor this into the build vs. buy decision.

## Output

A documented model selection decision: chosen model(s), routing logic (if applicable), fallback chain, eval results before and after switch, pinned version string, and deprecation calendar entry. If multiple models were evaluated, a comparison table: model / quality score / latency p50 / cost per 1K requests / decision.
