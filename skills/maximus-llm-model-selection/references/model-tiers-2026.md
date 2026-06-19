# Reference: LLM Model Tiers — Mid-2026

Capability, context window, pricing, and use-case fit for production model selection. All prices are per 1M tokens (input / output) from published provider list prices as of May–June 2026. Prices change; verify at provider docs before committing to a budget.

Sources: [APIpulse Q2 2026 pricing report](https://www.getapipulse.com/blog-q2-2026-pricing-report.html), [Talki Academy cost benchmark May 2026](https://academy.talki-app.fr/en/blog/cost-benchmark-claude-gpt4-gemini-2026/), [AIStackHub May 2026](https://aistackhub.ai/ai-api-pricing-comparison-2026), [LLM routing research](https://zylos.ai/research/2026-01-29-llm-routing-intelligent-model-selection).

---

## Frontier Tier

### Claude Opus 4 (Anthropic)
- **Context:** 200K tokens
- **Pricing:** $15.00 in / $75.00 out
- **Cached input:** $1.50/1M
- **Strengths:** Strongest available model for complex reasoning, multi-step analysis, nuanced writing, long-document processing. Best-in-class for tasks requiring judgment.
- **Weaknesses:** Highest cost; output ($75/1M) is 7.5× GPT-4.1 output. Not suitable for high-volume production without routing.
- **When to use:** Tasks that demonstrably fail on mid-tier models. Complex financial or legal analysis. Novel problem-solving. Rare; gate with routing.

### o3 (OpenAI)
- **Context:** 200K tokens
- **Pricing:** $10.00 in / $40.00 out
- **Strengths:** Best reasoning model for mathematical problems, complex code, multi-step logical deduction. Extended thinking mode produces a visible reasoning chain.
- **Weaknesses:** High latency (15–120s with extended thinking). Not suitable for real-time, user-facing features.
- **When to use:** Automated reasoning tasks, complex code review, mathematical verification, research analysis. Batch mode preferred for cost.

---

## Strong Mid Tier

### GPT-4.1 (OpenAI)
- **Context:** 1M tokens
- **Pricing:** $2.00 in / $8.00 out
- **Cached input:** Available at 50% discount
- **Strengths:** Strong coding performance, reliable function calling, consistent JSON output. Long context (1M) covers most document processing needs. Good cost/quality ratio.
- **Weaknesses:** Less strong than Opus 4 on highly complex reasoning. Output tokens are not cheap at scale.
- **When to use:** Default mid-tier choice for coding, agent reasoning, RAG generation, API integration. The "safe default" for new production features.

### Claude Sonnet 4.5 (Anthropic)
- **Context:** 200K tokens
- **Pricing:** $3.00 in / $15.00 out
- **Cached input:** $0.30/1M (4× cheaper than GPT-4o cache — critical for RAG cost calculation)
- **Strengths:** Excellent instruction following, reliable tool use, strong long-document processing. Cache pricing advantage makes it cost-competitive for RAG despite higher list price.
- **Weaknesses:** Higher output cost than GPT-4.1. 200K context vs GPT-4.1's 1M.
- **When to use:** RAG generation (cache advantage reduces effective cost), document Q&A, customer-facing agents where instruction adherence is critical.

### Gemini 2.5 Pro (Google)
- **Context:** 1M tokens (pricing tiers: $1.25/1M input ≤ 200K; $2.50/1M above 200K)
- **Pricing:** $1.25–$2.50 in / $10.00–$15.00 out
- **Cached input:** $0.31–$0.63/1M
- **Strengths:** Largest context window in the mid-tier. Best for tasks that require processing entire codebases, long contracts, or full transcripts in-context. Multimodal. Competitive pricing.
- **Weaknesses:** Google API reliability historically lower than OpenAI/Anthropic; verify for your region. Pricing jumps at 200K tokens.
- **When to use:** Any task requiring > 200K context that would otherwise require chunking. Full-codebase analysis, large document comparison, multi-hour transcript processing.

---

## Budget Tier

### GPT-4o mini (OpenAI)
- **Context:** 128K tokens
- **Pricing:** $0.15 in / $0.60 out
- **Cached input:** $0.075/1M
- **Strengths:** Fast, cheap, reliable JSON mode, strong at classification and extraction. 50% batch discount available.
- **Weaknesses:** 128K context limits long-document use. Quality drops on complex reasoning.
- **When to use:** Classification, entity extraction, short summarisation, structured output, high-volume routing (when quality holds on your task — test first). Default budget choice for OpenAI-ecosystem teams.

### Gemini 2.0 Flash (Google)
- **Context:** 1M tokens
- **Pricing:** $0.10 in / $0.40 out
- **Cached input:** $0.025/1M
- **Strengths:** Cheapest large-context option. 1M context at budget pricing — uniquely valuable for long-document tasks that don't require mid-tier quality.
- **Weaknesses:** Quality gap vs mid-tier is larger than GPT-4o mini's gap. Less ecosystem tooling than OpenAI.
- **When to use:** Long-document processing at budget price. High-volume tasks where quality testing shows it meets the bar.

### Claude Haiku 4.5 (Anthropic)
- **Context:** 200K tokens
- **Pricing:** $0.80 in / $4.00 out (significantly higher than GPT-4o mini and Gemini 2.0 Flash)
- **Cached input:** $0.08/1M
- **Strengths:** Best instruction following in the budget tier. 200K context. Reliable tool use.
- **Weaknesses:** 6–10× more expensive on input than GPT-4o mini; 7× more expensive on output. Hard to justify vs GPT-4o mini unless you need the 200K context or Anthropic tool use format.
- **When to use:** Budget-tier agent tasks requiring 200K context. Teams already on Anthropic who need a cheap escalation option.

---

## Open-Source / Local Models

### Llama 4 Scout (Meta)
- **Context:** 10M tokens (largest available context in any model, mid-2026)
- **License:** Free under 700M MAU; attribution required; separate commercial license above threshold
- **Params:** 109B total (MoE architecture)
- **Strengths:** Unmatched context window. Multimodal. Strong English instruction following. Widest fine-tuning ecosystem.
- **Weaknesses:** 10M context requires significant VRAM to serve. License requires attribution; commercial terms apply above scale threshold.
- **When to use:** Extreme long-context use cases (entire repositories, book-length documents). Privacy-sensitive workloads needing maximum context. Fine-tuning with open weights.

### Qwen 3.5 72B (Alibaba)
- **Context:** 128K (most variants); Qwen 3.6 Plus extends to 1M
- **License:** Apache 2.0 — most permissive of the major open-source families
- **Strengths:** Strong coding (SWE-bench competitive), mathematical reasoning (84% MATH), multilingual (29 languages), native JSON mode. Full family from 0.8B to 397B covers all deployment scales.
- **Weaknesses:** Alibaba-origin model may face enterprise procurement objections in some jurisdictions.
- **When to use:** Privacy-sensitive workloads. Fine-tuning for domain specialisation. Teams wanting Apache 2.0 licensing with no usage caps or royalties.

### Mistral Small 4 (Mistral)
- **Context:** 256K tokens
- **License:** Apache 2.0
- **Params:** 119B total, 6B active (MoE)
- **Strengths:** Efficient MoE architecture (only 6B active params → fast inference). 256K context. Multimodal. Configurable reasoning depth. Apache 2.0.
- **Weaknesses:** Newer model; less fine-tuning ecosystem than Llama or Qwen.
- **When to use:** European-origin model with strong compliance story for GDPR contexts. Efficient inference for teams with limited GPU budget. Long-context local deployment (256K).

---

## Routing Savings Reference

RouteLLM (ICLR 2025 peer-reviewed): **85% cost reduction on MT-Bench at 95% of GPT-4 quality** by routing only 14% of queries to the strong model. Production reports from large deployments show **40–50% savings** are consistently achievable with rule-based routing on real-world mixed traffic.

Budget models handle approximately **50–70% of production traffic** without quality loss for typical applications (classification, extraction, summarisation, structured output).

---

## Deprecation Watch (mid-2026)

- **GPT-4o (non-pinned aliases):** Actively updated; pin to a specific snapshot.
- **GPT-4 Turbo snapshots:** Several deprecated 2024–2025. If running any `gpt-4-turbo-*` pin, check EOL.
- **Claude 2.x:** EOL. If any system still uses `claude-2`, migrate immediately.
- Monitor: https://platform.openai.com/docs/deprecations and https://docs.anthropic.com/en/docs/model-deprecations

---

## Quick Decision Matrix

| Need | Model |
|------|-------|
| Cheapest, reliable JSON output | GPT-4o mini or Gemini 2.0 Flash |
| Best cost/quality for general production | GPT-4.1 |
| Best for RAG with repeated system prompts | Claude Sonnet 4.5 (cache advantage) |
| > 200K context, managed API | Gemini 2.5 Pro or GPT-4.1 |
| Maximum reasoning quality | Claude Opus 4 or o3 |
| Data privacy / on-premises | Qwen 3.5 72B or Llama 4 Maverick |
| Apache 2.0 + fine-tuning | Qwen 3.5 |
| Extreme long context (> 1M tokens) | Llama 4 Scout |
| Low-latency local inference | Mistral Small 4 (6B active params) |
