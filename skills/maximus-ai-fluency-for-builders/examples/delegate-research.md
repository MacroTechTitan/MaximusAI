# Example: Delegate a Research Task to AI

A worked example of the four-part request structure applied to a real research task.

---

## The task

You are building a vector search feature. You need to choose a vector database. You have 30 minutes to make a call.

## Bad delegation (what not to do)

> "What's the best vector database?"

**Problems**:
- No context (scale, use case, infra constraints).
- No output format specified.
- No source requirement.
- "Best" is undefined.

Result: a generic marketing-speak comparison that doesn't help you decide anything.

---

## Good delegation (four-part structure)

### Context
> We are building a semantic search feature for a SaaS product. Expected scale: 5–10 million vectors at launch, 100M+ within 18 months. Infra: AWS, Kubernetes. Existing stack: Python, FastAPI, Postgres. Team size: 2 engineers. We don't have a dedicated ML infra team.

### Goal
> Compare the top 3 actively maintained open-source vector databases for this use case. For each: name, license, index type (HNSW/IVF/other), query latency benchmark at 10M vectors (p99), horizontal scalability approach, managed cloud option, and a one-sentence honest tradeoff.

### Constraints
> - Focus on solutions with production deployments at the stated scale, not just benchmarks.
> - Cite primary sources (official docs or published benchmarks) for latency figures. Include URLs.
> - Do not include databases where the open-source version is significantly limited vs. the commercial version without noting it.
> - Output as a markdown table, followed by a recommendation paragraph.

### Verification hook
> Include the benchmark source URL for each latency figure. I'll spot-check 2 of them.

---

## What the output should look like

| Database | License | Index type | p99 latency @10M | Horizontal scale | Managed option | Tradeoff |
|---|---|---|---|---|---|---|
| Qdrant | Apache 2.0 | HNSW | ~15ms | Distributed mode (v1.1+) | Qdrant Cloud | Younger ecosystem; excellent Rust performance |
| Weaviate | BSD 3-Clause | HNSW | ~20ms | Multi-node sharding | Weaviate Cloud | Rich filtering; heavier resource footprint |
| Milvus | Apache 2.0 | HNSW + IVF | ~12ms | Built-in distributed | Zilliz Cloud | Most mature at scale; more complex to operate |

*Sources: [Qdrant benchmarks](https://qdrant.tech/benchmarks/), [ANN Benchmarks](https://ann-benchmarks.com/), [Weaviate benchmarks](https://weaviate.io/developers/weaviate/benchmarks)*

**Recommendation**: For your scale trajectory and team size, Qdrant is the starting recommendation — managed option available, simpler operational model than Milvus, and the distributed mode handles your 100M+ target. Revisit Milvus if you need the IVF index for memory efficiency at scale.

---

## Validation steps run on this output

1. Opened the Qdrant benchmarks URL → confirms ~15ms p99 at 10M vectors with default HNSW settings. ✓
2. Checked Weaviate license on GitHub → BSD 3-Clause confirmed. ✓
3. Verified Milvus distributed mode exists in v2.x docs. ✓

**Time saved**: ~25 minutes of manual research. **Validation time**: ~5 minutes. Net gain: ~20 minutes.

---

## Reusable prompt template

```
Context: [your stack, scale, constraints]
Goal: Compare [N] options for [decision]. For each: [columns].
Constraints:
- Cite primary sources. Include URLs.
- Output as a markdown table + recommendation paragraph.
- Do not include [exclusions].
Verification hook: Include source URLs for each [key claim]. I'll spot-check [N] of them.
```
