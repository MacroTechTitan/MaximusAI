# Example: Model Routing Table

A production routing table mapping task types to model tiers, with decision rationale, cost estimates, and implementation guidance.

---

## Mid-2026 Routing Reference

Pricing sources: provider list prices as of May–June 2026. All prices per 1M tokens unless noted.

### Tier definitions

| Tier | Example models | Input cost | Output cost | Notes |
|------|---------------|-----------|------------|-------|
| Budget | GPT-4o mini, Gemini 2.0 Flash, Gemini 2.5 Flash-Lite | $0.10–$0.15 | $0.40–$0.60 | Fastest, cheapest; matches frontier on routine tasks |
| Mid | GPT-4.1, Gemini 2.5 Pro, Claude Sonnet 4.5 | $1.25–$3.00 | $8–$15 | Default production tier; strong on all standard tasks |
| Frontier | Claude Opus 4, o3 | $10–$15 | $40–$75 | Reserve for tasks that demonstrably need it |
| Local | Qwen 3.5 72B, Llama 4 Maverick, Mistral Small 4 | GPU cost only | GPU cost only | Privacy, scale, fine-tuning |

---

## Task Routing Table

| Task type | Recommended model | Tier | Rationale | Notes |
|-----------|-----------------|------|-----------|-------|
| Binary classification | GPT-4o mini | Budget | 95%+ accuracy at frontier cost; JSON mode reliable | Temperature=0 |
| Multi-class classification (< 20 classes) | GPT-4o mini or Gemini 2.0 Flash | Budget | Same as binary | |
| Named entity extraction | GPT-4o mini | Budget | JSON schema mode highly reliable | Strict schema enforcement |
| Short summarisation (< 4K input) | GPT-4o mini | Budget | Summary quality matches mid-tier | |
| Long document summarisation (> 100K tokens) | Gemini 2.5 Pro | Mid | Requires 1M context window; GPT-4o (128K) cannot do this in-context | |
| RAG answer generation | GPT-4.1 or Claude Sonnet 4.5 | Mid | Faithful citation following; reliable JSON | Claude wins on cache-heavy RAG due to 4× cheaper cached input |
| Code generation (< 200 lines) | GPT-4.1 | Mid | Strong benchmark performance; consistent output format | |
| Code generation (complex, multi-file) | Claude Opus 4 or GPT-4.1 | Frontier / Mid | Frontier only if complexity genuinely needs it | Test mid-tier first |
| SQL generation | GPT-4.1 | Mid | Consistent schema adherence | |
| Agent reasoning / tool calling | GPT-4.1 or Claude Sonnet 4.5 | Mid | Reliable function call format; lower hallucinated-tool rate | Claude for Anthropic tool use; GPT-4.1 for OpenAI |
| Complex multi-step reasoning | o3 or Claude Opus 4 | Frontier | Extended thinking improves accuracy on hard problems | Latency: 15–120s; not for real-time features |
| Customer-facing chat | GPT-4o mini or GPT-4.1 | Budget / Mid | Route by query complexity classifier | |
| Document Q&A (private PII data) | Qwen 3.5 72B self-hosted or Llama 4 Maverick | Local | Data cannot leave premises | Requires GPU infra |
| Embeddings (for RAG) | text-embedding-3-large (OpenAI) | — | $0.13/1M tokens; best retrieval quality | Or nomic-embed-text-v1.5 for open-source |
| Reranking | Cohere Rerank 3 or ms-marco-MiniLM-L6-v2 | — | $0.002/1K requests (Cohere); free local (MiniLM) | |

---

## Python Implementation

```python
# routing.py
# Production model router with task-type → model mapping

from enum import Enum
from dataclasses import dataclass

class TaskType(Enum):
    CLASSIFICATION = "classification"
    EXTRACTION = "extraction"
    SHORT_SUMMARY = "short_summary"
    LONG_SUMMARY = "long_summary"          # > 100K tokens
    RAG_GENERATION = "rag_generation"
    CODE_GENERATION = "code_generation"
    AGENT_REASONING = "agent_reasoning"
    COMPLEX_REASONING = "complex_reasoning"
    CUSTOMER_CHAT = "customer_chat"

@dataclass
class ModelConfig:
    model_id: str
    provider: str
    tier: str
    max_tokens: int
    temperature_default: float

ROUTING_TABLE: dict[TaskType, ModelConfig] = {
    TaskType.CLASSIFICATION: ModelConfig(
        model_id="gpt-4o-mini",
        provider="openai",
        tier="budget",
        max_tokens=256,
        temperature_default=0.0,
    ),
    TaskType.EXTRACTION: ModelConfig(
        model_id="gpt-4o-mini",
        provider="openai",
        tier="budget",
        max_tokens=1024,
        temperature_default=0.0,
    ),
    TaskType.SHORT_SUMMARY: ModelConfig(
        model_id="gpt-4o-mini",
        provider="openai",
        tier="budget",
        max_tokens=512,
        temperature_default=0.0,
    ),
    TaskType.LONG_SUMMARY: ModelConfig(
        model_id="gemini-2.5-pro-preview-05-06",
        provider="google",
        tier="mid",
        max_tokens=4096,
        temperature_default=0.0,
    ),
    TaskType.RAG_GENERATION: ModelConfig(
        model_id="gpt-4.1-2025-04-14",
        provider="openai",
        tier="mid",
        max_tokens=2048,
        temperature_default=0.0,
    ),
    TaskType.CODE_GENERATION: ModelConfig(
        model_id="gpt-4.1-2025-04-14",
        provider="openai",
        tier="mid",
        max_tokens=4096,
        temperature_default=0.2,
    ),
    TaskType.AGENT_REASONING: ModelConfig(
        model_id="gpt-4.1-2025-04-14",
        provider="openai",
        tier="mid",
        max_tokens=4096,
        temperature_default=0.0,
    ),
    TaskType.COMPLEX_REASONING: ModelConfig(
        model_id="o3-2025-04-16",
        provider="openai",
        tier="frontier",
        max_tokens=8192,
        temperature_default=1.0,  # o3 uses temperature=1 with reasoning effort instead
    ),
    TaskType.CUSTOMER_CHAT: ModelConfig(
        model_id="gpt-4o-mini",    # escalate to gpt-4.1 via cascade if needed
        provider="openai",
        tier="budget",
        max_tokens=1024,
        temperature_default=0.3,
    ),
}

def get_model_config(
    task_type: TaskType,
    context_tokens: int = 0,
    privacy_required: bool = False
) -> ModelConfig:
    """
    Select a model config with hard-requirement overrides.

    Args:
        task_type: The type of task to perform.
        context_tokens: Total input tokens. Triggers long-context model if > 128K.
        privacy_required: If True, must use local/on-premises model.
    """
    if privacy_required:
        # Replace with your self-hosted model endpoint
        return ModelConfig(
            model_id="qwen3.5-72b",
            provider="local",
            tier="local",
            max_tokens=4096,
            temperature_default=0.0,
        )

    if context_tokens > 128_000:
        # Only Gemini 2.5 Pro and Claude models handle this
        return ModelConfig(
            model_id="gemini-2.5-pro-preview-05-06",
            provider="google",
            tier="mid",
            max_tokens=4096,
            temperature_default=0.0,
        )

    return ROUTING_TABLE.get(task_type, ROUTING_TABLE[TaskType.RAG_GENERATION])
```

---

## Cost Projection Example

Assuming 100K daily requests, mixed task types:

| Task type | Daily requests | Avg tokens in | Avg tokens out | Model | Daily cost |
|-----------|---------------|--------------|---------------|-------|-----------|
| Classification | 40,000 | 200 | 50 | gpt-4o-mini | $1.30 |
| Extraction | 20,000 | 400 | 200 | gpt-4o-mini | $3.60 |
| Short summary | 20,000 | 1,000 | 300 | gpt-4o-mini | $6.60 |
| RAG generation | 15,000 | 2,500 | 500 | gpt-4.1 | $81.75 |
| Agent reasoning | 5,000 | 3,000 | 800 | gpt-4.1 | $47.00 |
| **Total** | **100,000** | | | | **$140.25/day = ~$4,207/mo** |

Without routing (all gpt-4.1): $2.00 × ((200+400+1000+2500+3000)/5)/1M × (40K+20K+20K+15K+5K) ≈ dramatically higher.

The budget routing on the first three task types alone saves > 90% on those categories.
