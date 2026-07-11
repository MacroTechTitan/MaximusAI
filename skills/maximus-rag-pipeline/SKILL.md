---
name: maximus-rag-pipeline
description: "Production retrieval-augmented generation: chunking, embeddings, vector database selection (pgvector, Pinecone, Qdrant, Weaviate, Chroma), hybrid search (BM25 + dense), reranking, citation grounding, and the evaluation loop. Use when the user says 'build a RAG system', 'add document search', 'connect the LLM to our knowledge base', 'citations from documents', 'retrieval pipeline', 'semantic search over docs', or any task involving making an LLM answer questions from a corpus. Production-grade, not a demo."
metadata:
  pillar: ai-engineering
  source: maximus
---

# Maximus — RAG Pipeline

You can't make a horse remember last Tuesday's field notes by whispering harder. You have to give it the notes. RAG is how you give the model the right notes, at the right time, from the right pile — and make sure it cites them honestly.

## When to use

- Building a Q&A or search feature over a document corpus.
- Giving an LLM access to private or recent knowledge it wasn't trained on.
- Grounding LLM answers in specific source citations.
- The user says "hallucinations from our knowledge base", "the model makes up facts", or "document search".

If the problem is the prompt structure around retrieval, load `maximus-prompt-engineering` too. If the problem is model selection for the generator, load `maximus-llm-model-selection`.

## Core rules (non-negotiable)

1. **Chunking strategy is architecture.** The wrong chunk size or boundary makes every downstream step worse. Decide chunking before building anything else.
2. **Measure retrieval quality separately from generation quality.** A retrieval precision problem looks like a generation hallucination. Don't conflate them.
3. **Always ground citations.** Every claim in LLM output must trace to a specific retrieved chunk with source metadata (document ID, page, section). Never let the model cite from training memory.
4. **Evaluate continuously.** RAG quality degrades silently as the corpus changes. Wire an eval loop from day one. Load `maximus-eval-and-test` for the full harness.
5. **Hybrid search is the production default.** Dense-only retrieval misses exact terms; sparse-only misses semantic similarity. Hybrid (BM25 + dense + reranker) outperforms both in nearly all benchmarks.
6. **Read before edit.** Check the existing pipeline code with `read` before adding any new stage.

## Procedure

1. **Inventory the corpus.** What documents? What formats (PDF, HTML, DOCX, plain text)? What's the update frequency? Answers determine chunking strategy and indexing pipeline design.
2. **Choose a chunking strategy.** (See `references/chunking-strategies.md`.) Default: recursive character splitting at 512 tokens with 64-token overlap for general prose. Use semantic chunking for structured documents with clear sections.
3. **Choose an embedding model.** Default mid-2026: `text-embedding-3-large` (OpenAI, 3072 dims, best retrieval quality), `text-embedding-3-small` (cheaper, adequate for most), or `nomic-embed-text-v1.5` (open-source, 768 dims, runs locally). Dimension reduce if storing in pgvector at scale.
4. **Choose a vector store.** (See domain notes below.) Start with pgvector if you already have Postgres; graduate to Qdrant or Pinecone at > 5M vectors or when you need managed scaling.
5. **Build the ingestion pipeline.** Parse → chunk → embed → upsert. Attach metadata: `{source_id, doc_title, page_num, section, chunk_index, ingested_at}`.
6. **Build the retrieval stage.** Dense retrieval (k=20 candidates), BM25 sparse retrieval (k=20 candidates), RRF merge, rerank top-5 with a cross-encoder (`ms-marco-MiniLM-L6-v2` or Cohere Rerank 3).
7. **Build the generation stage.** Pass retrieved chunks as fenced context (XML tags). System prompt must instruct: "Answer using only the provided context. Cite the source_id for each claim." Set `temperature=0`.
8. **Implement citation grounding.** Map each sentence (or paragraph) in the answer back to the chunk ID it came from. Surface source metadata to the user.
9. **Run the eval loop.** Build a golden eval set: 50–100 question/answer pairs with known relevant documents. Measure: retrieval recall@k, answer faithfulness (does answer match context?), answer correctness.
10. **Monitor in production.** Log retrieval latency, chunk IDs retrieved, and answer faithfulness scores. Alert on faithfulness drops.

## Vector store selection

| Store     | Best for                                           | Managed | Self-host | Notes                                    |
|-----------|---------------------------------------------------|---------|-----------|------------------------------------------|
| pgvector  | ≤ 5M vectors; already on Postgres; simple ops      | via RDS/Supabase | Yes | No ANN at > 1M without tuning HNSW      |
| Qdrant    | > 1M vectors; need filtering + payload search     | Yes (Qdrant Cloud) | Yes | Best payload filtering; Rust-native     |
| Pinecone  | Fully managed; no infra ops; team prefers SaaS    | Yes     | No        | Fastest time-to-prod; higher cost/query |
| Weaviate  | GraphQL queries; multi-modal; modules ecosystem   | Yes     | Yes       | Steeper config; powerful for complex schemas |
| Chroma    | Local dev, prototyping, single-node prod          | No      | Yes       | Not production-hardened at scale; good for < 500K |

## Domain notes

- **Chunk overlap.** 64–128 tokens of overlap between chunks prevents answers being split across chunk boundaries. Too much overlap wastes storage and retrieval budget.
- **Late chunking.** Embed the full document, then segment embeddings to chunks post-hoc (late chunking). Preserves cross-sentence context. Supported natively by Jina AI's embedding API.
- **Reranking is not optional in prod.** Dense retrieval at k=20 will always include irrelevant chunks. A cross-encoder reranker is cheap ($0.002/1000 requests with Cohere Rerank 3) and materially improves precision.
- **Context window usage.** At 512-token chunks × 5 reranked = 2 560 tokens of context minimum, plus system prompt. Budget accordingly. Do not stuff 20 chunks into the generation prompt.
- **Metadata filtering.** Always filter by metadata (date range, document type, team) before vector search. Filtering first reduces the effective search space and improves both speed and precision.
- **Incremental indexing.** Don't re-index the entire corpus on every update. Track `last_indexed_at` per document; re-index only changed or new documents.
- **Faithfulness vs. correctness.** Faithfulness: is the answer supported by the retrieved context? Correctness: is the answer true? A faithful answer to bad retrieved context is still wrong. Measure both.

## Gotchas

- **Semantic search misses exact product codes, SKUs, and proper nouns.** Add BM25 (or keyword search) for these. Pure dense retrieval fails on exact-match queries.
- **PDF extraction is lossy.** Tables, headers, and multi-column layouts extract poorly with naive PDF parsers. Use `pdfplumber` or `unstructured` for production PDF parsing.
- **Embedding model drift.** If you switch embedding models, you must re-index the entire corpus. The old and new embedding spaces are incompatible.
- **System prompt over-retrieval.** Stuffing 10+ chunks into the generation prompt causes the model to hallucinate connections between unrelated chunks. Rerank to 3–5 before generation.
- **Missing source metadata at ingestion time** is the most painful pipeline failure. You can't add metadata retroactively after millions of chunks are indexed. Attach it at parse time.
- **Vector dimension mismatch.** The embedding dimension in your schema must match the embedding model's output dimension exactly. Adding a new model means a schema migration.

## Output

A running ingestion pipeline, a retrieval function with hybrid search + reranking, a generation function with citation grounding, an eval dataset of ≥ 50 question-answer pairs, and a retrieval precision@5 score ≥ 0.8. Plus a monitoring dashboard or logging setup that surfaces faithfulness per query.
