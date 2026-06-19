# maximus-ai-cost-control

Token economics and cost management for AI products. The skill that decides whether an AI feature is a business or a burn rate.

## What this skill is

Every LLM API call has a price — input tokens, output tokens, and (increasingly) context tokens. A product that works beautifully in a demo can become unprofitable at 10,000 users if the cost architecture was never designed. This skill covers the full cost control stack: caching, batching, model routing, context compression, budget setting, and anomaly alerting.

## Why it exists / what problem it solves

AI product teams consistently underestimate the cost of production LLM usage. Common failure modes:

- **System prompt sent fresh on every call** — cacheable, but not cached.
- **Frontier model used for all tasks** — GPT-4o and Claude 3.5 Sonnet are 10–20× the cost of capable smaller models for many task classes.
- **No per-user budget** — one heavy user can spike the monthly bill.
- **Cost discovered on the invoice** — no monitoring, no alerts, no early warning.

This skill prevents all four.

## Quick start

1. **Map the cost surface.** List every LLM call: model, input tokens (p50/p95), output tokens (p50/p95), calls/user/day. Multiply out to get $/user/month.
2. **Apply the caching hierarchy.** Enable provider prompt caching for stable system prompts. Add semantic caching for FAQ-style queries. Add result caching for deterministic outputs.
3. **Build a routing table.** Assign cheap models (e.g., Claude Haiku, GPT-4o mini) as defaults. Define escalation conditions for frontier models.
4. **Set budgets and alerts.** Per-user token budgets in your application layer. Provider-level hard limits as a backstop. Your own monitoring alert as the first line of defense.
5. **Do the unit-economics check.** LLM cost / ARPU. If cost exceeds 20% of ARPU on the free tier, adjust before scaling.

## When NOT to use it

- **Pre-API product** — if you're not yet calling an LLM in production, read `maximus-ai-product-spec` first.
- **Offline batch workflows with no latency requirement** — those are already cheap via the Batch API; this skill's routing and caching design is primarily for real-time paths.
- **Training cost optimization** — this skill covers inference costs. Training and fine-tuning cost optimization is in `maximus-fine-tuning`.

## Related skills

- `maximus-ai-product-spec` — Product specification that shapes the cost architecture.
- `maximus-prompt-engineering` — Prompt design that minimizes token waste.
- `maximus-eval-and-test` — Eval gates for model routing decisions.
- `maximus-mlops-deploy` — Deploying and versioning cost models alongside ML models.
- `maximus-fine-tuning` — Fine-tuning to replace expensive few-shot prompting.

## Glossary

**Prompt caching** — Provider feature that stores a prefix of the prompt and charges a reduced rate (≈10% of full price) for subsequent calls using the same prefix. Requires the cached prefix to be structurally identical across calls.

**Semantic caching** — Caching by embedding similarity rather than exact match. A new query within cosine distance 0.05 of a cached query returns the cached result without an LLM call.

**Result caching** — Exact-match key caching for fully deterministic outputs. No LLM call at all on a hit.

**Model routing** — Directing requests to different models based on task class, complexity, or confidence score. The core lever for cost/quality tradeoff management.

**Context compression** — Reducing input token count by summarizing conversation history, trimming retrieved chunks, and stripping non-semantic formatting from injected documents.

**Unit economics check** — The comparison of LLM cost per active user per month against average revenue per user (ARPU). The gate for scaling decisions.

**Batching** — Using provider Batch APIs (Anthropic, OpenAI) to process requests asynchronously at 50% of real-time pricing. Suitable for evals, enrichment, and scheduled jobs.
