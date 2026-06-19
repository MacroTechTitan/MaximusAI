# maximus-llm-model-selection

Decision framework for choosing the right LLM: capability tiers, cost/latency/quality tradeoffs, open-source options, routing, fallbacks, and deprecation management.

## What this skill is

A structured approach to model selection for production AI systems — covering the mid-2026 capability landscape (frontier, mid-tier, budget, open-source), cost optimisation through routing, fallback chain design, A/B testing, and model deprecation planning.

## Why it exists / what problem it solves

The price spread between the cheapest and most expensive LLM available in mid-2026 is roughly 400×. Using a frontier model for tasks a budget model handles equally well is pure waste. Using a budget model for complex reasoning tasks produces silent quality regressions. Routing intelligently between them — backed by measurement, not guessing — is the leverage point. This skill encodes the measurement, routing, and lifecycle patterns that make that leverage real.

Key data point: RouteLLM demonstrated 85% cost reduction on MT-Bench benchmarks while maintaining 95% of GPT-4 quality by routing only 14% of queries to the strong model.

## Quick start

1. **Classify your task** — complex reasoning, standard production, or high-volume simple. This maps to a capability tier.
2. **Check hard requirements** — context window size, multimodal, tool calling, latency budget, data privacy.
3. **Pick a model from the tier table** in SKILL.md. Start with the mid-tier (GPT-4.1, Gemini 2.5 Pro, Claude Sonnet 4.5) as the default production choice.
4. **Test against your eval set** — 20 representative queries minimum. Compare latency p50 and quality score.
5. **Add routing** if > 30% of your traffic is routine/simple tasks. Rule-based routing by task type is the lowest-overhead starting point.

## When NOT to use it

- When the current model is working fine and the issue is the prompt — that's `maximus-prompt-engineering`.
- When you're exploring models in a notebook and haven't shipped anything — use the provider playgrounds.
- When the problem is retrieval quality, not model quality — that's `maximus-rag-pipeline`.
- When you've already selected the model and the next problem is agent loop design — that's `maximus-agent-design`.

## Related skills

- `maximus-prompt-engineering` — tune the prompt for the selected model
- `maximus-eval-and-test` — A/B harness and quality evaluation across models
- `maximus-agent-design` — model selection for multi-step agent tasks
- `maximus-rag-pipeline` — model selection for the retrieval generator
- `maximus-build-feature` — implement the routing and fallback code

## Glossary

**Frontier model** — The most capable model tier: Claude Opus 4, OpenAI o3. Used for tasks requiring complex reasoning, novel problem-solving, or maximum quality. 10–100× more expensive than budget tier.

**Mid-tier model** — Strong production models: GPT-4.1, Gemini 2.5 Pro, Claude Sonnet 4.5. Covers the majority of production use cases at a fraction of frontier cost.

**Budget model** — Small, fast, cheap: GPT-4o mini, Gemini 2.0 Flash, Claude Haiku 4.5. Matches frontier on routine tasks (classification, extraction, structured output) at 10–100× lower cost.

**Open-source / local model** — Models with publicly available weights: Llama 4 (Meta), Qwen 3.5 (Alibaba), Mistral Small 4 (Mistral). Self-hosted; zero per-token cost; requires GPU infrastructure.

**Model routing** — Dynamically assigning requests to different model tiers based on task complexity, query type, or cost constraints. Can reduce costs by 40–85% with minimal quality loss.

**Fallback chain** — A sequence of models to try in order when the primary model is unavailable (rate limit, timeout, error). Ensures availability at the cost of potentially lower quality.

**Cascade routing** — Try the cheaper model first; escalate to the stronger model only if the cheaper model's output is low-confidence or fails validation.

**Prompt caching** — Provider feature (Claude, Gemini) that stores processed prompt prefixes to reduce cost on repeated calls with the same system prompt. Dramatically changes cost calculations for RAG and agent pipelines.

**Snapshot pinning** — Using a specific dated model version (`gpt-4o-2024-11-20`) rather than a floating alias (`gpt-4o`) in production. Prevents silent behaviour changes when providers update their models.

**Extended thinking** — A mode in reasoning-focused models (o3, Claude Opus 4) where the model produces a long internal reasoning chain before answering. Improves accuracy on hard problems at high token cost and latency.

**Context window** — Maximum total tokens (input + output) the model can process in one request. Critical constraint for long-document tasks: GPT-4o = 128K, Claude models = 200K, Gemini 2.5 Pro = 1M, Llama 4 Scout = 10M.

**Batch API** — Provider feature for asynchronous, non-real-time jobs. Returns results within 24 hours at 50% discount. Suitable for nightly evals, bulk processing, and document indexing.
