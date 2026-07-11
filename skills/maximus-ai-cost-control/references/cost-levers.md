# Reference: Cost Levers

A structured map of every lever available for reducing AI inference costs, organized by impact and implementation effort.

---

## The cost equation

```
Total cost = Σ (input_tokens × input_price + output_tokens × output_price) per call
           × calls per user per day
           × daily active users
```

Every lever attacks one of: token count, token price, or call frequency.

---

## Lever 1: Prompt caching (token price)

**What**: Provider stores a fixed prefix and charges 80–90% less for cached token reads.

**Impact**: 80–90% cost reduction on the cached portion. If system prompt is 30% of input tokens and you achieve 85% cache hit rate, total input cost drops ~25%.

**Implementation effort**: Low. Mark the cache boundary in your request; keep the prefix static.

**Providers**:
- Anthropic: `cache_control: {type: "ephemeral"}` on the last content block of the prefix. Minimum 1,024 tokens (Haiku) or 2,048 tokens (Sonnet/Opus). TTL: 5 minutes, refreshed on hit.
- OpenAI: Automatic for prompts ≥1,024 tokens. No configuration required. Cached tokens: ~50% discount.

**Watch out for**: Dynamic content (timestamps, session IDs) in the prefix invalidates the cache. Move all dynamic content to the user turn.

---

## Lever 2: Semantic caching (call frequency)

**What**: Cache full responses by embedding similarity. An incoming query within cosine distance ~0.05 of a cached query returns the cached response, no LLM call made.

**Impact**: Can eliminate 20–60% of LLM calls for FAQ-style or repetitive query products. Varies dramatically by use case.

**Implementation effort**: Medium. Requires a vector store (Redis with RediSearch, Pinecone, Qdrant), an embedding model, and a similarity threshold tuning step.

**Libraries**: GPTCache, LangChain's `SemanticSimilarityExampleSelector`, or a custom Redis pipeline.

**Watch out for**: False positives — queries that are semantically similar but require different answers. Test thoroughly with your query distribution. Also: the embedding call itself has a cost (small, but non-zero).

---

## Lever 3: Result caching (call frequency)

**What**: Exact-match key/value cache for fully deterministic inputs. If input X was seen before, return the stored output.

**Impact**: Eliminates 100% of LLM cost for the cached call. Effective for: templated reports, fixed-question Q&A, batch classification of repeated items.

**Implementation effort**: Low. A Redis SET/GET with a content hash as the key.

**Watch out for**: Only valid when the same input should always produce the same output. Not valid for conversational or context-dependent tasks.

---

## Lever 4: Model routing (token price)

**What**: Route each request to the cheapest model that meets the quality bar for that task class.

**Impact**: 10–50× price difference between frontier and small models. Routing 80% of traffic to small models while maintaining quality for that 80% is a large lever.

**Implementation effort**: Medium-high. Requires: task classification, an offline eval on each task class for each model tier, a routing config, and ongoing monitoring.

**Reference**: `examples/routing-config.md` for a worked implementation.

**Watch out for**: Routing without evals. Silent quality regression is the risk. Always gate routing changes on eval results.

---

## Lever 5: Context compression (input tokens)

**What**: Reduce the number of input tokens by: summarizing conversation history, stripping formatting from retrieved documents, and tightening the system prompt.

**Impact**: Typically 15–40% reduction in input tokens, depending on how much bloat exists. Largest gains from: conversation history (grows unbounded without compression) and verbatim document injection (HTML/markdown adds 20–40% overhead).

**Implementation effort**: Low-medium. Regex stripping is fast. Rolling summarization requires a cheap LLM call (Haiku/GPT-4o mini) every N turns.

**Watch out for**: Compressing too aggressively. Always run evals after context compression. Important instructions that are rare (edge cases, safety rules) are the most dangerous to compress out.

---

## Lever 6: Output length control (output tokens)

**What**: Constrain `max_tokens` and add explicit length instructions to the prompt. Output tokens are 3–5× more expensive per token than input tokens on most frontier models.

**Impact**: If your median response is 800 tokens but 400 would serve the user, you're paying 2× unnecessarily. Particularly important for streaming features where users may not read long responses.

**Implementation effort**: Low. Set `max_tokens` conservatively; add "Be concise. Maximum N sentences." to the prompt.

**Watch out for**: Cutting max_tokens too low causes truncated responses (model stops mid-sentence). Test at p95 output length, not just p50.

---

## Lever 7: Batching async workloads (token price)

**What**: Use provider Batch APIs for non-real-time tasks. Batch API pricing is 50% of real-time pricing.

**Impact**: 50% cost reduction for eligible workloads. Latency: results in 24 hours (Anthropic) or 24 hours (OpenAI).

**Implementation effort**: Low for new workflows; medium for retrofitting existing sync flows.

**Eligible workloads**: Evals, bulk document enrichment, nightly reports, dataset labeling, scheduled summaries.

**Not eligible**: User-facing real-time features.

---

## Lever 8: Fine-tuning (token price + input tokens)

**What**: Fine-tune a smaller model to match frontier quality for your specific task. Reduces both model price (smaller model) and input token count (no few-shot examples needed in the prompt).

**Impact**: Can reduce inference cost by 80%+ for specific tasks at frontier quality, once the fine-tuned model is validated. High one-time training cost; amortizes over volume.

**Implementation effort**: High. Requires labeled dataset, training run, eval, and ongoing maintenance as task distribution drifts.

**Reference**: `maximus-fine-tuning` for the full workflow.

**Watch out for**: Fine-tuning for cost without first proving you can't get there with routing + caching. Fine-tuning is expensive and inflexible; exhaust simpler levers first.

---

## Lever selection guide

| Current cost situation | First lever to try |
|---|---|
| System prompt >1,000 tokens, no caching | Prompt caching |
| FAQ-style product, many repeated queries | Semantic caching |
| High-cost frontier model used for everything | Model routing |
| Input tokens growing unbounded (chat product) | Context compression |
| Eval + batch jobs running at real-time prices | Batching |
| High-quality demand on a specific well-defined task at scale | Fine-tuning |
| Output responses much longer than users need | Output length control |

---

## Cost lever interaction effects

- **Prompt caching + context compression**: compressing the system prompt may drop it below the minimum size for caching. Keep the cached prefix ≥1,024 tokens after compression.
- **Routing + caching**: the routing decision happens before the cache check in most architectures. If a cheaper model handles a task, the cached prefix for that model is different from the frontier model's cached prefix.
- **Fine-tuning + routing**: a fine-tuned model can become the default for its task class in the routing table, improving quality over the cheap-default while keeping cost low.
