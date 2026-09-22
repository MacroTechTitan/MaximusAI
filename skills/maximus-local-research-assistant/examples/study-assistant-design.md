# Worked design — offline study assistant on 16 GB Apple Silicon

An illustrative end-to-end design following `SKILL.md`. The numbers trace to
`references/local-rag-components-2026-09.md` and to the VRAM method in
`maximus-slm-local-stack`. **No code here has been run** — it is a design
walkthrough, not a tested implementation.

**Scenario.** A graduate student wants to study from ~400 PDFs (papers, lecture
notes, textbook chapters) on a 16 GB M3 laptop. No document may leave the
machine. Needs: ask questions of the corpus, generate quizzes per chapter, and
get explanations that cite the source.

---

## Step 1 — Two-model budget

Usable memory: ~11-12 GB of 16 GB, since unified memory is shared with the OS.

| Component | Estimate |
|---|---|
| Qwen3-8B generator @ Q4_K_M | ~5.0 GB |
| KV cache, 32 layers @ 32K context | ~0.8 GB |
| `Qwen3-Embedding-0.6B` | ~1.5 GB |
| Small cross-encoder reranker | ~0.4 GB |
| Runtime overhead | ~1.0 GB |
| **Total** | **~8.7 GB** |

Fits with ~2-3 GB headroom. Runtime: MLX, or LM Studio as a GUI over it.

The reranker earns its 0.4 GB here. With only 3-5 chunks going to a small
reader, top-k precision matters more than generator size — this is the trade
`SKILL.md` step 3 recommends making.

## Step 2 — Embedder choice

`Qwen3-Embedding-0.6B`: best quality per VRAM in the current reference table at
70.7 MTEB-eng-v2, Apache-2.0, Ollama-native. Version pinned in a manifest
beside the index, because swapping the embedder invalidates every stored vector.

Rejected: `nomic-embed-text` (lighter, but memory is not the binding constraint
here) and `bge-m3` (multilingual and hybrid retrieval are unused in an
English-only corpus).

## Step 3 — Chunking

- ~400 tokens per chunk, ~80 tokens overlap.
- Prepended to every chunk: source filename, paper or chapter title, section
  heading, page number.
- PDFs parsed with layout awareness; two-column academic PDFs otherwise
  interleave columns and produce chunks that are grammatically plausible and
  semantically scrambled — the failure is easy to miss because the text *looks*
  fine.
- Figures and tables extracted separately, with captions kept as their own
  chunks. A small model handles "what does Table 3 report" far better when the
  caption is its own retrievable unit.

Retrieval: top 12 by vector similarity → rerank → **top 4 to the generator**.

## Step 4 — Grounding contract

The system prompt requires: answer only from provided passages; quote the span
relied on; if the passages do not contain the answer, reply exactly
`NOT_IN_CORPUS` and name what was searched. Schema-constrained output so
`NOT_IN_CORPUS` is machine-detectable rather than a phrase to grep for.

**Built and tested before anything else:** 15 questions known to be absent from
the corpus. Target is 15/15 refusals. Anything less means the contract is not
holding, and no amount of answerable-question success compensates.

## Step 5 — Decomposition

| Task | Placement |
|---|---|
| Rephrase the student's question | local SLM |
| Retrieve, rerank, filter | code |
| Extract the relevant span | local SLM |
| Summarize one paper | local SLM |
| Generate quiz items from a chapter | local SLM |
| Spaced-repetition scheduling | **code** (FSRS) |
| "How do these three papers disagree?" | **decomposed** — summarize each separately, then pairwise comparison, never all three at once |
| "What's the state of the field?" | **outside reliable range** — refuse, and say why |

Privacy forbids routing up, so the last row is a stated limitation rather than a
hybrid. That is the honest trade for a no-data-leaves-the-machine requirement.

## Step 6 — Citations

Every answer renders as: claim, then `[Author Year, §Section, p.N]`, then the
quoted span in a collapsible block. The span is stored with the answer so it can
be re-verified later without re-retrieving.

## Step 7 — Verification before display

1. Every claim has a cited span, or the answer degrades.
2. Embedding similarity between claim and cited span exceeds a threshold tuned
   on the eval set.
3. Any number in the answer must appear in the retrieved text. This check alone
   catches most of the drift that matters in a technical corpus.

Failures degrade to "found related material, cannot support a direct answer,"
with passages shown.

## Step 8 — Study features

- **Quiz:** retrieve chapter passages → generate 10 items, each with question,
  source-backed answer, and supporting span, schema-constrained.
- **Flashcards:** same shape, shorter, span stored with the card.
- **Explanation:** retrieve → explain from retrieved text only → source shown
  underneath.
- **Grading:** against the stored span. The model never grades from its own
  knowledge.
- **Hand check:** 20 generated items reviewed manually before trusting a batch.

## Eval set

45 items: 15 retrieval (question → expected chunk ID, scored recall@4), 15
answerable generation (question, gold answer, expected span), 15 unanswerable
(expect `NOT_IN_CORPUS`). Run on every change to chunking, embedder, k,
reranker, or prompt.

## What this design gives up

Cross-document synthesis and open-ended "state of the field" questions. Those
need a frontier model, and the privacy requirement rules that out. The system
says so rather than answering anyway — which is the whole point of building it
this way.
