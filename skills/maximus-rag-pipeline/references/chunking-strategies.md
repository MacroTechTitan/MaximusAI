# Reference: Chunking Strategies

Chunking is the first architectural decision in a RAG pipeline and the one that propagates the most downstream. The wrong chunking strategy cannot be rescued by a better reranker or a smarter prompt. Load this reference when designing or debugging a RAG ingestion pipeline.

---

## The Core Trade-off

| Chunk size | Precision | Recall | Context density |
|------------|-----------|--------|-----------------|
| Small (128 tokens) | High — each chunk is focused | Low — an answer may span multiple chunks | Low — few tokens of context per retrieved chunk |
| Large (1024+ tokens) | Low — chunk may contain irrelevant content | High — answer fits within one chunk | High — more context per chunk, but noisy |
| Medium (512 tokens) | Balanced | Balanced | Balanced |

**Default recommendation:** 512-token chunks with 64-token overlap. Adjust based on your document structure.

---

## Strategy 1: Fixed-Size Character Splitting

**What:** Split text into chunks of N characters, with M characters of overlap between adjacent chunks.

**When to use:**
- Unstructured prose (web pages, articles, emails)
- When you don't know the document structure in advance
- Prototyping any new RAG system

**Parameters:**
- Chunk size: 512 tokens (≈ 2048 chars)
- Overlap: 64 tokens (≈ 256 chars)
- Try to split on sentence boundaries (`.`, `\n\n`) before hard character limits

**Implementation:**
```python
def fixed_split(text: str, chunk_chars: int = 2048, overlap_chars: int = 256) -> list[str]:
    chunks, start = [], 0
    while start < len(text):
        end = start + chunk_chars
        if end < len(text):
            # prefer sentence boundary
            boundary = text.rfind('. ', start + chunk_chars // 2, end)
            if boundary > 0:
                end = boundary + 1
        chunks.append(text[start:end].strip())
        start = end - overlap_chars
    return [c for c in chunks if len(c) > 100]
```

**Gotchas:**
- Does not respect document sections — a chunk may span a heading and start of the next section
- Overlap increases storage cost and retrieval noise; keep it < 20% of chunk size

---

## Strategy 2: Recursive Character Splitting

**What:** Split on a hierarchy of separators: `\n\n` (paragraphs) → `\n` (lines) → `. ` (sentences) → ` ` (words). Falls back to the next level if a split would produce a chunk too large.

**When to use:**
- General-purpose default (LangChain's `RecursiveCharacterTextSplitter` implements this)
- When paragraphs are the natural unit but vary in length
- Best all-around starting point

**Why it's better than fixed-size:** Respects natural text boundaries where they exist; falls back gracefully where they don't.

**Implementation:** Use LangChain's `RecursiveCharacterTextSplitter` with `chunk_size=512` (in tokens) and `chunk_overlap=64`. Use `tiktoken` for token counting, not character counts.

---

## Strategy 3: Semantic Chunking

**What:** Embed each sentence individually, then group consecutive sentences that are semantically similar (cosine similarity above a threshold). Each semantic "burst" becomes a chunk.

**When to use:**
- Long documents with clearly distinct sections that aren't marked up with headers
- Scientific papers, legal documents, technical reports
- When retrieval on fixed-size chunks misses answers that span natural topic boundaries

**How it works:**
1. Split document into sentences.
2. Embed each sentence.
3. Compute cosine similarity between adjacent sentences.
4. Where similarity drops below a threshold (e.g., 0.8), start a new chunk.
5. Merge small groups; split large groups.

**Gotchas:**
- 2–4× more expensive than fixed-size (requires embedding every sentence twice — once for boundary detection, once for storage)
- Chunk sizes are variable; downstream context window budgeting is harder
- Threshold is a hyperparameter that requires tuning per corpus

---

## Strategy 4: Document-Structure Splitting

**What:** Split on document structure — headings, sections, pages — rather than text content.

**When to use:**
- Well-structured documents: PDFs with clear headings, HTML articles, DOCX with styles, Markdown files
- When each section answers a different question and cross-section chunks are noise
- Legal contracts (split on clauses), API docs (split on endpoints), financial reports (split on sections)

**Implementation:**
- HTML/Markdown: split on `<h1>–<h3>` tags or `#` headings
- PDF: use `pdfplumber` to extract text per page, then split on detected headings
- DOCX: use `python-docx` to split on `Heading 1`/`Heading 2` paragraph styles

**Metadata:** Attach the section title and document hierarchy as metadata on each chunk. This enables metadata filtering ("only retrieve from the 'Pricing' section").

**Gotchas:**
- Requires reliable heading detection — fails on PDFs where headings are styled text, not structural markers
- Some sections may be very short (a heading + one sentence) — merge small sections before indexing

---

## Strategy 5: Late Chunking

**What:** Embed the full document (or a long passage), then segment the contextualised embeddings into chunk-level representations post-hoc.

**When to use:**
- When chunks require cross-sentence context for accurate embeddings (e.g., pronoun resolution: "it" refers to a term defined two sentences earlier)
- When you can afford the higher embedding cost
- Native support: Jina AI Embeddings API (pass full document, receive per-chunk embeddings)

**Why it's better for context-sensitive documents:** Traditional chunking embeds each chunk in isolation; late chunking preserves the full-document context in each chunk's embedding.

**Gotchas:**
- Only supported natively by certain embedding APIs (Jina AI as of mid-2026)
- Document must fit in the embedding model's context window
- Not compatible with self-hosted embedding models that don't support it

---

## Strategy 6: Proposition Chunking

**What:** Extract atomic factual statements (propositions) from documents using an LLM, and store each proposition as a chunk.

**When to use:**
- Q&A over fact-dense documents (knowledge bases, FAQs, product specs)
- When answer precision is more important than recall
- When you can afford 10–20× the ingestion cost

**How it works:**
1. Pass document sections to an LLM with prompt: "Extract all factual propositions from this text as a list of standalone sentences."
2. Each proposition is independently stored as a chunk.
3. Each proposition is traceable back to its source section.

**Gotchas:**
- Very expensive — requires an LLM call per section at ingestion time
- LLM may miss or misstate propositions
- Propositions lose surrounding context — retrieval is high precision but may lack explanatory context

---

## Strategy 7: Parent Document Retrieval

**What:** Index small chunks for retrieval precision, but return the parent (larger) chunk for generation context.

**When to use:**
- When small chunks retrieve precisely but don't provide enough context for the generator
- When answers require a few paragraphs of surrounding context

**How it works:**
1. Split documents into large parent chunks (1024–2048 tokens).
2. Split parent chunks into small child chunks (128–256 tokens).
3. Index child chunk embeddings.
4. At retrieval time: retrieve the top-k child chunks, then look up their parent chunks.
5. Pass parent chunks to the generator.

**Gotchas:**
- Parent chunks may contain irrelevant content alongside the relevant passage
- Double storage (both parent and child chunks)
- More complex retrieval implementation

---

## Choosing a Strategy

| Scenario | Recommended strategy |
|----------|---------------------|
| General prose corpus, first build | Recursive character splitting (512/64) |
| Well-structured docs (Markdown, HTML, DOCX) | Document-structure splitting |
| Long docs with topic shifts | Semantic chunking |
| High-precision fact-dense Q&A | Proposition chunking |
| Context-sensitive, cross-sentence content | Late chunking |
| Small chunks miss context at generation time | Parent document retrieval |

---

## Chunk Metadata (Always Attach)

Every chunk must carry:
```json
{
  "doc_id": "string — unique document identifier",
  "doc_title": "string — document display name",
  "url": "string — source URL (optional but critical for citation UI)",
  "page_num": "integer — for paginated documents",
  "section": "string — heading or section title",
  "chunk_index": "integer — position within document",
  "ingested_at": "ISO 8601 timestamp"
}
```

Missing `url` or `doc_title` at ingestion time means citations in the UI are broken forever. There is no retroactive fix for millions of chunks.
