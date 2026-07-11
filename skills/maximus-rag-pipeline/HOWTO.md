# HOWTO — RAG Pipeline

Concrete recipes for common RAG tasks. Each recipe has a goal, numbered steps, a verification check, and pitfalls to avoid.

---

## Recipe 1: Set up pgvector for a small corpus (< 1M chunks)

**Goal:** A Postgres database ready for vector search, with the right schema and indexes.

**Steps:**

1. Enable the extension:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
2. Create the chunks table:
   ```sql
   CREATE TABLE chunks (
     id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
     doc_id      TEXT NOT NULL,
     doc_title   TEXT,
     page_num    INTEGER,
     section     TEXT,
     chunk_index INTEGER,
     body        TEXT NOT NULL,
     embedding   VECTOR(3072),   -- match your embedding model's output dimension
     ingested_at TIMESTAMPTZ DEFAULT now()
   );
   ```
3. Create the HNSW index (pgvector ≥ 0.5):
   ```sql
   CREATE INDEX ON chunks USING hnsw (embedding vector_cosine_ops)
     WITH (m = 16, ef_construction = 64);
   ```
4. Create a GIN index for BM25 keyword search via `pg_trgm` (or use `ts_vector`):
   ```sql
   ALTER TABLE chunks ADD COLUMN body_tsv TSVECTOR
     GENERATED ALWAYS AS (to_tsvector('english', body)) STORED;
   CREATE INDEX ON chunks USING GIN (body_tsv);
   ```
5. Test with a sample embedding query:
   ```sql
   SELECT id, doc_title, body
   FROM chunks
   ORDER BY embedding <=> '[0.1, 0.2, ...]'::vector
   LIMIT 5;
   ```

**Verification:** Query returns results in < 50ms for a 100K-chunk corpus. EXPLAIN shows index scan, not sequential scan.

**Common pitfalls:**
- Creating the HNSW index *before* bulk inserting data — build the index after the initial bulk load, not before.
- Mismatching embedding dimensions in the schema vs. the model output — Postgres will reject inserts silently or error at query time.

---

## Recipe 2: Build a hybrid retrieval function (dense + BM25 + RRF)

**Goal:** A Python function that retrieves the top-k most relevant chunks using hybrid search.

**Steps:**

1. Install dependencies: `pip install openai psycopg2-binary rank_bm25 numpy`
2. Implement RRF merge:
   ```python
   def rrf_merge(dense_ids: list, sparse_ids: list, k: int = 60) -> list:
       """Reciprocal Rank Fusion of two ranked lists."""
       scores = {}
       for rank, doc_id in enumerate(dense_ids):
           scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
       for rank, doc_id in enumerate(sparse_ids):
           scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
       return sorted(scores, key=scores.get, reverse=True)
   ```
3. Implement the dense retrieval query against pgvector (or your vector store's SDK).
4. Implement the BM25 query against the `body_tsv` column using `to_tsquery`.
5. Merge with RRF, take top 20 candidates.
6. Rerank the top 20 with a cross-encoder (see Recipe 3).
7. Return top 5 reranked chunks with full metadata.

**Verification:** Run 10 test queries. Check that chunks returned include at least one exact-term match (validates BM25 is working) and at least one semantically similar but term-different result (validates dense is working).

**Common pitfalls:**
- Running dense and BM25 at k=5 each before merging — you lose recall. Run at k=20 each, merge, then rerank to 5.
- Not normalising BM25 scores before merging — use RRF (rank-based, not score-based) to avoid scale mismatch.

---

## Recipe 3: Add a cross-encoder reranker

**Goal:** Improve retrieval precision by reranking top-20 candidates to top-5 using a cross-encoder.

**Steps:**

1. **Option A — Local model** (no API cost, ~100ms/batch):
   ```python
   from sentence_transformers import CrossEncoder
   reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")

   def rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
       pairs = [(query, c["body"]) for c in candidates]
       scores = reranker.predict(pairs)
       ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
       return [c for c, _ in ranked[:top_k]]
   ```
2. **Option B — Cohere Rerank 3** (managed API, ~$0.002/1000 requests):
   ```python
   import cohere
   co = cohere.Client()  # COHERE_API_KEY from env

   def rerank(query: str, candidates: list[dict], top_k: int = 5) -> list[dict]:
       docs = [c["body"] for c in candidates]
       result = co.rerank(query=query, documents=docs, model="rerank-english-v3.0", top_n=top_k)
       return [candidates[r.index] for r in result.results]
   ```
3. Wire the reranker between your RRF merge and the generation step.
4. Log reranker latency and measure Precision@5 improvement against your eval set.

**Verification:** Precision@5 should improve by ≥ 0.05 over RRF-only on your golden eval set.

**Common pitfalls:**
- Reranking only 5 candidates — the cross-encoder needs a diverse pool (≥ 15) to have something to rerank.
- Not caching the reranker model on the local option — cold-loading adds 2–5 seconds per request.

---

## Recipe 4: Implement citation grounding

**Goal:** Every sentence in the LLM's answer attributes to a specific retrieved chunk ID.

**Steps:**

1. In your generation prompt, instruct the model to cite chunk IDs inline:
   ```
   ## Instructions
   - Answer using only the content provided in <retrieved_context>.
   - After each claim, cite the source using [source:chunk_id] notation.
   - If a claim cannot be grounded in the provided context, say "I don't have information about that."

   ## Retrieved context
   <retrieved_context>
   [CHUNK_ID: abc123] ... chunk text ...
   [CHUNK_ID: def456] ... chunk text ...
   </retrieved_context>
   ```
2. Parse the model's response to extract citation markers: `re.findall(r'\[source:([\w-]+)\]', answer)`.
3. Look up each cited chunk ID in your database to retrieve `{doc_title, page_num, section, url}`.
4. Return the answer with citations as footnotes or inline links in your UI.
5. For faithfulness validation: use an LLM judge to check "Is this claim supported by the cited chunk?" Score each claim 0/1. Target faithfulness ≥ 0.95.

**Verification:** Send 20 queries to the system. Every answer either cites a chunk or explicitly says it lacks information. Zero "I know from my training that..." answers.

**Common pitfalls:**
- Not including the chunk ID in the retrieved context passed to the model — the model cannot cite what it hasn't seen.
- Leaving the citation format ambiguous — the model will invent its own format. Specify exactly.
- Not validating faithfulness programmatically — citation presence doesn't guarantee citation accuracy.

---

## Recipe 5: Build the RAG eval loop

**Goal:** A repeatable evaluation that measures retrieval and generation quality independently.

**Steps:**

1. Create a golden eval set: 50–100 question-answer pairs where you know which document(s) contain the answer. Include:
   - 20 factual lookups (specific facts from specific documents)
   - 15 multi-document synthesis questions
   - 10 questions with no answer in the corpus (expect "I don't know")
   - 5 adversarial/injection attempts
2. Measure **retrieval recall@5**: for each question, did the top-5 retrieved chunks include the known relevant document? Target ≥ 0.80.
3. Measure **answer faithfulness**: for each non-"I don't know" answer, does every cited chunk support the claim? Use an LLM judge. Target ≥ 0.95.
4. Measure **answer correctness**: is the final answer factually correct? Compare against the golden answer. Target ≥ 0.80.
5. Record all scores per run: `{date, embedding_model, reranker, k, precision_at_5, faithfulness, correctness}`.
6. Run this eval: (a) before any pipeline change, (b) after any corpus update > 10% of documents, (c) on a nightly schedule.

**Verification:** You have a CSV/DB of eval run history. Any metric drop > 0.05 triggers an alert and blocks pipeline promotion.

**Common pitfalls:**
- Measuring only end-to-end correctness — if correctness drops, you can't tell if the retrieval or generation step failed.
- Not including "unanswerable" questions in the eval set — the system must know when to say "I don't know".
- Re-using eval questions as few-shot examples — always hold the eval set out from the prompt.

---

## Recipe 6: Handle incremental corpus updates

**Goal:** Index only new and changed documents without re-indexing the full corpus.

**Steps:**

1. Add a `content_hash` column to your documents table:
   ```sql
   ALTER TABLE documents ADD COLUMN content_hash TEXT;
   ALTER TABLE documents ADD COLUMN last_indexed_at TIMESTAMPTZ;
   ```
2. At ingestion time, compute `SHA256(document_bytes)` and store in `content_hash`.
3. On each ingestion run:
   - Fetch all documents from source.
   - Compare `content_hash` against the stored hash.
   - Skip documents where hash matches and `last_indexed_at` is recent.
   - Re-index documents where hash changed.
   - Insert new documents.
   - Mark deleted documents (not present in source) as `deprecated = true`; exclude from retrieval.
4. After re-indexing, delete old chunks for the changed document and insert new chunks.
5. Log: documents processed / unchanged / updated / new / deprecated per run.

**Verification:** A second run over the same corpus with no changes processes 0 documents. A run after editing one document processes exactly 1 document.

**Common pitfalls:**
- Forgetting to delete old chunks for updated documents — the old and new chunks coexist, degrading retrieval.
- Not marking deleted documents as deprecated — the model will still cite documents that no longer exist.
