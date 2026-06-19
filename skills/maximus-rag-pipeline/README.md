# maximus-rag-pipeline

Production-grade retrieval-augmented generation: from document ingestion to grounded, cited answers.

## What this skill is

A structured approach to building RAG pipelines that work in production — covering chunking strategies, embedding models, vector store selection, hybrid search, reranking, citation grounding, and the continuous evaluation loop needed to keep quality high as corpora change.

## Why it exists / what problem it solves

Most RAG demos work in notebooks with 10 clean PDFs. Production RAG must handle thousands of documents, noisy PDFs, exact-term queries, metadata filtering, answer faithfulness tracking, and retrieval regressions as documents are added or updated. This skill encodes the decisions and disciplines that close the gap between demo and production.

The central insight: retrieval quality and generation quality are separate problems. Bad retrieval produces hallucinations that look like generation failures. Measure them independently; fix them independently.

## Quick start

1. **Inventory your corpus.** Document formats, count, update frequency, and access pattern (bulk + incremental, or bulk-only).
2. **Set up chunking and embedding.** Recursive character split at 512 tokens / 64-token overlap. Embed with `text-embedding-3-large` (OpenAI) or `nomic-embed-text-v1.5` (open source).
3. **Choose a vector store.** pgvector if you have Postgres and < 5M vectors. Qdrant for filtered search at scale. Pinecone for zero-infra managed.
4. **Build hybrid retrieval.** Dense (k=20) + BM25 (k=20) → RRF merge → rerank top-5 with `ms-marco-MiniLM-L6-v2` or Cohere Rerank 3.
5. **Ground citations.** Every LLM answer sentence must trace to a chunk ID and source metadata. Surface doc title, page, and section to the user.

## When NOT to use it

- When the model just needs better prompting to use its training knowledge — that's `maximus-prompt-engineering`.
- When you're doing a one-off lookup that doesn't need a persistent index.
- When the "corpus" is a single document that fits in the model's context window — just stuff it in directly.
- When you need fine-tuning to bake knowledge into model weights — that's a different skill (maximus-fine-tuning).

## Related skills

- `maximus-prompt-engineering` — craft the generation prompt that wraps retrieved context
- `maximus-agent-design` — build agents that call RAG as one of their tools
- `maximus-eval-and-test` — retrieval precision, faithfulness, and regression eval harness
- `maximus-llm-model-selection` — choose the right generator model for RAG tasks
- `maximus-build-feature` — implement the ingestion and retrieval code

## Glossary

**Chunking** — Splitting documents into segments that are individually embedded and stored. Chunk size and overlap determine retrieval granularity.

**Embedding** — A dense vector representation of text. Semantically similar texts have similar embeddings (high cosine similarity).

**Vector store / vector database** — A database optimised for approximate nearest-neighbour (ANN) search over embedding vectors. Examples: pgvector, Qdrant, Pinecone, Weaviate.

**Hybrid search** — Combining dense (embedding) search with sparse (BM25/keyword) search. Catches both semantic similarity and exact term matches.

**BM25** — A classic term-frequency-based ranking algorithm (Okapi BM25). Excels at exact-term queries and proper nouns where dense retrieval underperforms.

**RRF (Reciprocal Rank Fusion)** — An algorithm for merging results from multiple ranked lists. Takes the rank position from each list and combines them without needing score normalisation.

**Reranking** — A second-stage ranking step that takes candidate retrieved chunks (e.g., top-20) and re-scores them using a cross-encoder model (which sees query + chunk together) for higher precision.

**Cross-encoder** — A model architecture for reranking: the query and candidate chunk are concatenated and scored together, producing better relevance estimates than embedding similarity alone.

**Citation grounding** — Attributing each claim in an LLM-generated answer to a specific retrieved chunk with source metadata. Prevents hallucination from training memory.

**Faithfulness** — A RAG quality metric: is the answer supported by the retrieved context? Measured separately from correctness.

**Precision@k** — The fraction of the top-k retrieved chunks that are relevant to the query. The primary retrieval quality metric.

**Incremental indexing** — Re-indexing only new or changed documents, not the full corpus. Critical for corpora that update frequently.

**Late chunking** — Embedding the full document first, then segmenting into chunk-level embeddings, preserving cross-sentence context.
