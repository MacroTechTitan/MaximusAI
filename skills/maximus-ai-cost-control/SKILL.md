---
name: maximus-ai-cost-control
description: "Token economics and cost management for AI products. Use when designing the cost architecture of an AI feature, auditing a surprise billing spike, setting up prompt caching, routing requests to cheaper models, compressing context, or defining $/request and $/user budgets before scaling. The skill that determines whether an AI product is a business or a burn rate."
metadata:
  pillar: ai-engineering
  source: maximus
---

# Maximus — AI Cost Control

A language model is a metered API. Every token in and out costs money. Ship without a cost model and you will discover your unit economics at the worst possible time — when you're trying to scale. Build the cost model first.

## When to use

- Designing the cost architecture for a new AI feature before it ships.
- Auditing a cost spike in production.
- Setting up caching, batching, or model routing.
- Doing the unit-economics check before a growth push.
- Monitoring $/request and $/active-user on an ongoing basis.

If you're not yet calling an LLM in production, the caching and monitoring sections are premature — read `maximus-ai-product-spec` first to get to a deployable spec.

## Core rules

1. **Know the unit before you scale.** $/request and $/active-user must be defined before marketing spend or growth investment. A 10× growth at negative unit economics is 10× the problem.
2. **Cheap by default, expensive when needed.** Route to the cheapest model that passes quality eval for the task class. Reserve frontier models for tasks that demonstrably require them.
3. **Cache aggressively.** The cheapest token is one you never send. Prompt caching, semantic caching, and result caching each attack a different part of the bill.
4. **Compress context, don't truncate naively.** Summarize earlier turns; keep the system prompt tight; strip formatting from retrieved documents before embedding them in context.
5. **Alert before the invoice.** Set cost anomaly alerts at the API or infrastructure layer. A runaway eval loop or a forgotten batch job should not be discovered on billing day.

## Procedure

1. **Map the cost surface.** For each LLM call in your product: input tokens (median, p95), output tokens (median, p95), model, calls/user/day. Build the table in `examples/cost-dashboard.md`.
2. **Apply the caching hierarchy.**
   - **Prompt caching**: For repeated system prompts or few-shot blocks, use the provider's prompt-caching feature (Anthropic prefix caching, OpenAI prompt caching). A cached prefix is 80–90% cheaper than sending it fresh.
   - **Semantic caching**: For question-answering features, cache by embedding similarity (e.g., GPTCache, Redis with vector search). If the incoming query is within cosine distance 0.05 of a cached query, return the cached result.
   - **Result caching**: For deterministic outputs (fixed input → fixed output), cache with an exact-match key. Cheapest possible — no model call at all.
3. **Build the routing table.** Assign each task class a default model and a threshold for escalation. See `examples/routing-config.md` for a worked example. Escalation triggers: user explicitly requests "best answer", confidence score below threshold, task type is in the "frontier-only" set.
4. **Compress context.** At each call: (a) summarize conversation history older than N turns, (b) trim retrieved chunks to the relevant passage only, (c) strip HTML/markdown formatting from injected documents, (d) audit system prompt for redundancy every sprint.
5. **Set budgets and alerts.** Per-user token budgets enforce cost isolation. Provider-level alerts (AWS Budgets, Anthropic spend limits, OpenAI hard limits) are the last-resort backstop. Your own monitoring layer should fire first.
6. **Run the unit-economics check.** At current usage: LLM cost per active user per month. Compare to ARPU. If LLM cost > 20% of ARPU on the free tier, the business model needs adjustment before scaling.
7. **Audit spikes.** When $/request spikes: check for context length regression, model routing misconfiguration, caching miss-rate increase, and runaway retry loops. See HOWTO.md → "How to audit a sudden cost spike".

## Domain notes

- Prompt caching requires prefixes to be structurally stable. Dynamic content (timestamps, user IDs) in the system prompt defeats caching. Move dynamic content to the user turn.
- Semantic caching introduces latency for cache misses. Warm the cache with your most common query classes on deploy.
- Batching (Anthropic Batch API, OpenAI Batch API) is 50% cheaper than real-time for async workloads. Use for evals, bulk enrichment, and nightly jobs — not for user-facing latency-sensitive paths.
- Model routing logic should be tested with the same rigor as product code. A routing bug that sends all traffic to the frontier model is a silent cost explosion.

## Cross-references

- Quality gates for routed models: `maximus-eval-and-test`
- Prompt structure that minimizes tokens: `maximus-prompt-engineering`
- Deploying and versioning the cost model itself: `maximus-mlops-deploy`
- System design that affects cost architecture: `maximus-ai-product-spec`

## Gotchas

- **Caching with non-deterministic prompts** — any dynamic value in a cached prefix (timestamp, session ID) causes a cache miss every time. Audit prompts for hidden dynamism.
- **Routing to a cheaper model without an eval gate** — quality regressions are invisible until users complain. Run evals before and after any routing change.
- **Ignoring output token costs** — on GPT-4o and Claude 3.5 Sonnet, output tokens are 3–5× more expensive than input. Streaming verbose responses is a bill, not a feature.
- **Context window waste** — retrieved documents injected verbatim often contain boilerplate (headers, nav, ads) that contributes tokens but not signal. Pre-process before injection.
- **Forgetting eval costs** — running an LLM-as-judge eval at scale is itself an LLM cost. Factor it into the total model of the system.

## Output

A cost architecture document covering: the cost-surface table, caching strategy, routing table, compression plan, budget thresholds, and alert configuration. Runnable with `examples/cost-dashboard.md` as the monitoring template.
