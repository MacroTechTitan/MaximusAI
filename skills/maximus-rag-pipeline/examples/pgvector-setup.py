"""
pgvector-setup.py
-----------------
A complete, runnable RAG ingestion + retrieval pipeline using:
- PostgreSQL + pgvector for vector storage
- OpenAI text-embedding-3-large for embeddings
- BM25 (full-text search) for sparse retrieval
- RRF merge for hybrid retrieval
- Local cross-encoder reranker (ms-marco-MiniLM-L6-v2)

Requirements:
    pip install openai psycopg2-binary sentence-transformers numpy

Environment variables:
    OPENAI_API_KEY      — OpenAI API key
    DATABASE_URL        — PostgreSQL connection string
                          e.g. postgresql://user:pass@localhost:5432/ragdb

Run migrations with: python pgvector-setup.py migrate
Ingest documents with: python pgvector-setup.py ingest
Query with:           python pgvector-setup.py query "your question here"
"""

import os
import sys
import json
import hashlib
import textwrap
from typing import Optional
import psycopg2
import psycopg2.extras
from openai import OpenAI

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
EMBEDDING_MODEL = "text-embedding-3-large"
EMBEDDING_DIM = 3072
CHUNK_SIZE = 512       # tokens (approximate; using chars / 4 here for simplicity)
CHUNK_OVERLAP = 64
TOP_K_DENSE = 20
TOP_K_BM25 = 20
TOP_K_RERANK = 5

openai_client = OpenAI()

DB_URL = os.environ["DATABASE_URL"]

def get_conn():
    return psycopg2.connect(DB_URL, cursor_factory=psycopg2.extras.RealDictCursor)


# ---------------------------------------------------------------------------
# Migration
# ---------------------------------------------------------------------------
MIGRATION_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE IF NOT EXISTS documents (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    url             TEXT,
    content_hash    TEXT,
    last_indexed_at TIMESTAMPTZ,
    deprecated      BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS chunks (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    doc_id      TEXT NOT NULL REFERENCES documents(id),
    doc_title   TEXT,
    page_num    INTEGER DEFAULT 0,
    section     TEXT DEFAULT '',
    chunk_index INTEGER NOT NULL,
    body        TEXT NOT NULL,
    embedding   VECTOR({dim}),
    body_tsv    TSVECTOR GENERATED ALWAYS AS (to_tsvector('english', body)) STORED,
    ingested_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS chunks_embedding_hnsw
    ON chunks USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS chunks_body_tsv_gin
    ON chunks USING GIN (body_tsv);
""".format(dim=EMBEDDING_DIM)


def run_migration():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(MIGRATION_SQL)
        conn.commit()
    print("Migration complete.")


# ---------------------------------------------------------------------------
# Chunking
# ---------------------------------------------------------------------------
def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Simple recursive character splitter.
    chunk_size and overlap are in approximate tokens (chars // 4).
    For production, use tiktoken for accurate token counting.
    """
    chars_per_chunk = chunk_size * 4
    chars_overlap = overlap * 4
    chunks = []
    start = 0
    while start < len(text):
        end = start + chars_per_chunk
        chunk = text[start:end]
        # Try to break on a sentence boundary
        if end < len(text):
            last_period = chunk.rfind('. ')
            if last_period > chars_per_chunk // 2:
                end = start + last_period + 1
                chunk = text[start:end]
        chunks.append(chunk.strip())
        start = end - chars_overlap
    return [c for c in chunks if len(c) > 50]  # drop tiny trailing chunks


# ---------------------------------------------------------------------------
# Embeddings
# ---------------------------------------------------------------------------
def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts. OpenAI supports up to 2048 texts per request."""
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
        dimensions=EMBEDDING_DIM
    )
    return [item.embedding for item in response.data]


# ---------------------------------------------------------------------------
# Ingestion
# ---------------------------------------------------------------------------
def ingest_document(doc_id: str, title: str, text: str, url: str = "", page_num: int = 0):
    """
    Ingest a single document. Skips if content hash unchanged.
    """
    content_hash = hashlib.sha256(text.encode()).hexdigest()

    with get_conn() as conn:
        with conn.cursor() as cur:
            # Check if already indexed and unchanged
            cur.execute(
                "SELECT content_hash FROM documents WHERE id = %s",
                (doc_id,)
            )
            row = cur.fetchone()
            if row and row["content_hash"] == content_hash:
                print(f"  [skip] {doc_id} — unchanged")
                return

            # Upsert document record
            cur.execute("""
                INSERT INTO documents (id, title, url, content_hash, last_indexed_at)
                VALUES (%s, %s, %s, %s, now())
                ON CONFLICT (id) DO UPDATE SET
                    title = EXCLUDED.title,
                    url = EXCLUDED.url,
                    content_hash = EXCLUDED.content_hash,
                    last_indexed_at = now(),
                    deprecated = FALSE
            """, (doc_id, title, url, content_hash))

            # Delete old chunks for this document
            cur.execute("DELETE FROM chunks WHERE doc_id = %s", (doc_id,))

            # Chunk and embed
            chunks = chunk_text(text)
            print(f"  [index] {doc_id} — {len(chunks)} chunks")
            embeddings = embed_texts(chunks)

            # Insert chunks
            for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                cur.execute("""
                    INSERT INTO chunks (doc_id, doc_title, page_num, chunk_index, body, embedding)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (doc_id, title, page_num, i, chunk, json.dumps(embedding)))

        conn.commit()


# ---------------------------------------------------------------------------
# Hybrid Retrieval
# ---------------------------------------------------------------------------
def rrf_merge(dense_ids: list, sparse_ids: list, k: int = 60) -> list:
    """Reciprocal Rank Fusion."""
    scores = {}
    for rank, doc_id in enumerate(dense_ids):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    for rank, doc_id in enumerate(sparse_ids):
        scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank + 1)
    return sorted(scores, key=scores.get, reverse=True)


def retrieve_hybrid(query: str, top_k: int = TOP_K_RERANK) -> list[dict]:
    """
    Hybrid retrieval: dense (pgvector) + BM25 + RRF + cross-encoder reranking.
    Returns top_k chunks with metadata.
    """
    # Embed the query
    query_embedding = embed_texts([query])[0]
    embedding_str = json.dumps(query_embedding)

    with get_conn() as conn:
        with conn.cursor() as cur:
            # Dense retrieval
            cur.execute(f"""
                SELECT id::text, doc_id, doc_title, body
                FROM chunks
                ORDER BY embedding <=> %s::vector
                LIMIT %s
            """, (embedding_str, TOP_K_DENSE))
            dense_results = cur.fetchall()
            dense_ids = [r["id"] for r in dense_results]
            dense_map = {r["id"]: dict(r) for r in dense_results}

            # BM25 / full-text retrieval
            cur.execute("""
                SELECT id::text, doc_id, doc_title, body,
                       ts_rank(body_tsv, plainto_tsquery('english', %s)) AS rank
                FROM chunks
                WHERE body_tsv @@ plainto_tsquery('english', %s)
                ORDER BY rank DESC
                LIMIT %s
            """, (query, query, TOP_K_BM25))
            sparse_results = cur.fetchall()
            sparse_ids = [r["id"] for r in sparse_results]
            sparse_map = {r["id"]: dict(r) for r in sparse_results}

    # Merge with RRF
    all_map = {**dense_map, **sparse_map}
    merged_ids = rrf_merge(dense_ids, sparse_ids)
    candidates = [all_map[id_] for id_ in merged_ids if id_ in all_map][:20]

    # Rerank
    candidates = rerank(query, candidates, top_k=top_k)
    return candidates


def rerank(query: str, candidates: list[dict], top_k: int = TOP_K_RERANK) -> list[dict]:
    """Cross-encoder reranking using sentence-transformers."""
    try:
        from sentence_transformers import CrossEncoder
        model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L6-v2")
        pairs = [(query, c["body"]) for c in candidates]
        scores = model.predict(pairs)
        ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
        return [c for c, _ in ranked[:top_k]]
    except ImportError:
        print("  [warn] sentence-transformers not installed; skipping rerank")
        return candidates[:top_k]


# ---------------------------------------------------------------------------
# Generation with Citation Grounding
# ---------------------------------------------------------------------------
def generate_answer(query: str, chunks: list[dict]) -> dict:
    """Generate an answer with inline citations."""
    context_block = "\n\n".join(
        f"[CHUNK_ID: {c['id']}] (Source: {c['doc_title']})\n{c['body']}"
        for c in chunks
    )
    system_prompt = textwrap.dedent("""
        You are a precise research assistant.
        Answer the user's question using only the content provided in <retrieved_context>.
        After each factual claim, cite the source inline as [source:CHUNK_ID].
        If the answer cannot be found in the provided context, say exactly:
        "I don't have information about that in the available documents."
        Do not use knowledge from your training data.
        Keep answers concise and factual.
    """).strip()

    response = openai_client.chat.completions.create(
        model="gpt-4o-2024-11-20",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"<retrieved_context>\n{context_block}\n</retrieved_context>\n\nQuestion: {query}"}
        ]
    )
    answer = response.choices[0].message.content
    # Extract cited chunk IDs
    import re
    cited_ids = re.findall(r'\[source:([\w-]+)\]', answer)
    cited_chunks = [c for c in chunks if c["id"] in cited_ids]
    return {"answer": answer, "cited_chunks": cited_chunks}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def demo_ingest():
    """Ingest sample documents for testing."""
    docs = [
        {
            "id": "doc-001",
            "title": "Product Pricing Guide",
            "text": "Our Basic plan costs $29/month and includes 5 users, 10GB storage, and email support. "
                    "The Pro plan costs $99/month and includes unlimited users, 100GB storage, priority support, "
                    "and API access. The Enterprise plan starts at $499/month with custom storage, SLA guarantees, "
                    "dedicated account management, and SSO integration.",
        },
        {
            "id": "doc-002",
            "title": "Refund Policy",
            "text": "Customers may request a refund within 30 days of purchase for any reason. "
                    "Refunds are processed within 5-7 business days. Annual plan refunds are prorated for unused months. "
                    "Usage-based charges are non-refundable. To request a refund, contact billing@example.com "
                    "with your account email and order number.",
        },
    ]
    print("Ingesting sample documents...")
    for doc in docs:
        ingest_document(doc["id"], doc["title"], doc["text"])
    print("Done.")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"

    if cmd == "migrate":
        run_migration()
    elif cmd == "ingest":
        demo_ingest()
    elif cmd == "query" and len(sys.argv) > 2:
        query_text = sys.argv[2]
        print(f"\nQuery: {query_text}\n")
        chunks = retrieve_hybrid(query_text)
        print(f"Retrieved {len(chunks)} chunks.\n")
        result = generate_answer(query_text, chunks)
        print("Answer:")
        print(result["answer"])
        print(f"\nCited sources: {[c['doc_title'] for c in result['cited_chunks']]}")
    else:
        print("Usage:")
        print("  python pgvector-setup.py migrate")
        print("  python pgvector-setup.py ingest")
        print("  python pgvector-setup.py query 'your question'")
