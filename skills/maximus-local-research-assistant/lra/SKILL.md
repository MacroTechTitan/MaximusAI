---
name: maximus-local-research-assistant
description: "Build a trustworthy research or learning assistant on top of a small local model (roughly 1B-14B). Covers local RAG with local embeddings, refuse-when-unretrieved grounding, span-level citation, task decomposition that keeps an SLM inside its competence, a verification pass to compensate for higher hallucination rates, and study tooling (quiz and flashcard generation, concept explanation) grounded in your own corpus. Use when the user says 'local research assistant', 'offline RAG', 'chat with my documents privately', 'study assistant', 'learning app with a local model', 'private knowledge base', 'no data leaves my machine', or 'small model keeps making things up'. For choosing hardware, model, quantization, and runtime, use maximus-slm-local-stack first."
metadata: { "openclaw": { "emoji": "📚", "pillar": "ai-engineering", "source": "maximus" } }
---

# Maximus — Local Research Assistant

A small model is a careful reader with no memory of what it read last year.
Hand it the page and it will do fine work; ask it what it recalls and it will
invent something plausible. Every design decision in this skill follows from
that one sentence.

## Purpose

Turn a local SLM into a research and learning tool whose output you can
actually rely on. The engineering problem is not making a small model smarter.
It is arranging the system so the model is only ever asked to do things a small
model does well — read provided text, extract, summarize, reformat, quiz —
while the facts come from a corpus and every claim stays traceable to a span.

This is the application layer. `maximus-slm-local-stack` decides what runs on
the machine; this skill decides what to build on it.

## The reframe that makes this work

Most "SLM hallucinates too much" complaints are architecture bugs reported as
model bugs. A small model produces fewer errors when grounded in retrieved
evidence — retrieval boosts factuality and interpretability by supplying
supporting passages at inference time, while adding its own dependency on
retrieval accuracy and latency ([SciTePress, knowledge placement in small
language models](https://www.scitepress.org/Papers/2026/144557/144557.pdf)).
Model size is also not destiny for hallucination rate: small models have posted
competitive hallucination scores on Vectara's HHEM leaderboard, which Intel
documents for a 7B model ([Intel](https://www.intel.com/content/www/us/en/developer/articles/technical/do-smaller-models-hallucinate-more.html)).

There is working prior art at this scale worth studying rather than
reinventing: [Local Deep Research](https://github.com/LearningCircuit/local-deep-research)
is an open-source self-hosted research assistant spanning 10+ sources including
arXiv, PubMed, and private documents, and reports roughly **95% accuracy on
SimpleQA** ([review](https://andrew.ooo/posts/local-deep-research-self-hosted-ai-research-review/)).
Read its architecture before designing your own.

So the four levers, in order of impact:

1. **Grounding** — the model answers from retrieved text, never from weights.
2. **Decomposition** — no single step exceeds the model's competence.
3. **Refusal** — "not in the corpus" is a correct, expected, frequent output.
4. **Verification** — a second pass checks claims against spans.

## Scope boundary

| Need | Skill |
|---|---|
| Build a grounded local research or study tool | **this skill** |
| Pick the model, quant, runtime, hardware | `maximus-slm-local-stack` |
| Production cloud RAG at scale | `maximus-rag-pipeline` |
| Verify a finished draft's claims | `maximus-chain-of-verification` |
| Research the open web with a frontier model | `maximus-deep-research` |
| Systematic academic review | `maximus-literature-review` |
| Teach a small model a domain's style or format | `maximus-fine-tuning` |

`maximus-rag-pipeline` is the sibling to read alongside this one. It assumes
cloud embeddings and a frontier reader; this skill assumes neither, and the
differences below are deliberate, not simplifications.

## Core workflow

### 1. Budget both models before writing code

An assistant needs a generator **and** an embedder resident at once. Add them:
roughly 5 GB for an 8B at Q4 plus ~0.7 GB for the embedder needs 6 GB minimum,
which fits an 8 GB card comfortably ([CraftRigs, local RAG hardware](https://craftrigs.com/articles/63-hardware-for-local-rag-system/)).
Scale up the generator and that headroom disappears fast. Run the arithmetic in
`maximus-slm-local-stack` step 2, including the KV cache at your real context.

### 2. Choose a local embedding model deliberately

Retrieval quality caps the whole system — a grounded answer over the wrong
passage is still wrong. Local embedders are no longer a compromise: as of April
2026, three open embedding models matched or beat `text-embedding-3-large` on
retrieval accuracy in one practitioner's RAG benchmarks, at zero cost per
million tokens and running on a $300 GPU ([Local AI Master](https://localaimaster.com/blog/local-vs-openai-embeddings)).

Current practical picks, per [d-central](https://d-central.tech/local-embedding-models/)
(pulled 2026-09-22): `nomic-embed-text` for the easiest start at ~0.3 GB via
Ollama; **`Qwen3-Embedding-0.6B` for best quality per VRAM** at 70.7 MTEB-eng-v2,
Apache-2.0, ~1.5 GB; `bge-m3` when you need multilingual plus hybrid
dense/sparse retrieval in one model. On 8 GB laptops, bge-m3 or Nomic Embed v2
both run comfortably ([Local AI Zone](https://local-ai-zone.github.io/guides/best-ai-embedding-models-ultimate-ranking-2026.html)).

Verify these against `references/local-rag-components-2026-09.md` and re-check
the file's date before trusting it.

### 3. Chunk for a small reader, not a large one

This is where cloud RAG guidance actively misleads. A frontier model can be
handed twelve loosely relevant chunks and sort it out. A 4B model cannot — it
gets distracted by the irrelevant ones and starts blending them.

- **Fewer, tighter chunks.** Retrieve 3-5, not 15. Precision over recall.
- **Smaller chunks with real overlap**, so a retrieved span is self-contained.
- **Keep structural context in the chunk** — document title, section heading,
  page number. A small model given a naked paragraph often cannot tell what it
  is about, and the heading is also what makes a citation useful.
- **Rerank if memory allows.** A small cross-encoder reranker improves the top
  3 more than a larger generator would. Spend the VRAM there first.

### 4. Make refusal the default, not the exception

Write the prompt so the absence of evidence produces an explicit non-answer.
Concretely: instruct the model to answer only from the provided passages, to
quote the span it relied on, and to reply with a fixed refusal string when the
passages do not contain the answer. Then **test the refusal path first**, with
questions you know are absent from the corpus. A system that never refuses is
not grounded; it is guessing with extra steps.

Prompt construction for this belongs to `maximus-prompt-engineering` —
particularly the guardrail and JSON-schema sections, which make refusal
machine-detectable rather than a phrase you hope to see.

### 5. Decompose so no step is too hard

Split what you want into steps a small model reliably completes, and keep the
hard reasoning out of the model:

| Step | Who does it |
|---|---|
| Query expansion / rephrase | SLM (easy) |
| Retrieval, filtering, ranking | Code, not the model |
| Extract relevant span from a passage | SLM (easy) |
| Summarize one document | SLM (easy) |
| Synthesize across many documents with conflicting claims | **hard** — either route up or reduce to pairwise comparisons |
| Multi-hop reasoning chains | **hard** — decompose into explicit single hops with retrieval between each |

When a step is genuinely too hard and privacy permits, route that step to an
API model and keep the rest local — a hybrid is usually the honest design.
When privacy forbids it, say plainly that this class of question is outside the
system's reliable range instead of shipping something that answers confidently
and wrongly.

### 6. Cite at span level

Every claim carries document, section or page, and the quoted span. Two
reasons. The obvious one: the user can check it. The load-bearing one: span
citation converts hallucination from invisible to detectable, because a
fabricated claim has no span to point at, and a mismatched span can be
verified mechanically.

### 7. Verify before display

Run a cheap automatic check over every generated answer:

- Does each claim have a cited span?
- Does the cited span actually contain the claim? (String or embedding
  similarity between claim and span catches a surprising share of drift.)
- Are there numbers in the answer absent from the retrieved text? Numbers are
  where small models drift most often, and unsourced digits are the highest
  yield thing to flag.

Failed checks should degrade to "I found related material but cannot support a
direct answer," with the passages shown. For high-stakes output, escalate to
the full loop in `maximus-chain-of-verification`.

### 8. Learning applications — the genuinely good fit

Study tooling is the strongest use case for a local SLM, because the ground
truth sits in the corpus rather than in the weights:

- **Quiz and flashcard generation** from a chapter, where the model transforms
  provided text rather than recalling facts.
- **Concept explanation** grounded in retrieved passages, with the source
  shown so a wrong explanation is traceable.
- **Spaced repetition scheduling**, which is arithmetic in code, not a model
  task. Do not ask the model to schedule.
- **Socratic questioning** over provided material.

The one rule: never let it grade factual correctness from its own knowledge.
Grade against the source span, or have it produce the question and the
source-backed answer together, and let the learner compare.

## Anti-patterns

- **Blaming the model for an architecture failure.** "It hallucinates" usually
  means retrieval is weak, chunks are too big, or refusal was never built.
- **Porting cloud RAG defaults unchanged.** Retrieving 15 chunks for a 4B
  reader degrades the answer. Retrieve fewer, better.
- **Naked chunks with no structural context.** Hurts answer quality and makes
  citations useless.
- **Never testing the refusal path.** Test absent-answer questions before
  present-answer ones.
- **Asking the model to do arithmetic or scheduling.** Code does that.
  Deterministic work belongs outside the model.
- **Trusting a summary of summaries.** Hierarchical summarization compounds
  small-model drift. Keep a path back to source spans at every level.
- **Shipping without measuring retrieval separately from generation.** If you
  cannot say whether a bad answer came from bad retrieval or bad generation,
  you cannot fix either.
- **Treating the learning case as low-stakes.** Confidently wrong study
  material is worse than no study material; the learner cannot tell.

## Sibling skills

- **`maximus-slm-local-stack`** — read first; hardware, model, quant, runtime.
- **`maximus-rag-pipeline`** — the production cloud counterpart, deeper on
  vector stores, hybrid search, and reranking mechanics.
- **`maximus-chain-of-verification`** — the heavyweight verification loop when
  step 7's cheap checks are not enough.
- **`maximus-prompt-engineering`** — refusal guardrails and schema-constrained
  output.
- **`maximus-eval-and-test`** — build the retrieval and answer eval sets before
  you need them.
- **`maximus-literature-review`** — when the corpus is academic and the task is
  systematic synthesis rather than lookup.

## Output

A local assistant design containing: the two-model memory budget, the embedding
model with its retrieval justification, chunking parameters tuned for a small
reader, the grounding prompt with its refusal contract, the decomposition table
naming which steps stay local and which route up, the citation format at span
level, the verification checks that run before display, and an eval set that
separates retrieval failures from generation failures. Volatile numbers carry
source URLs and pull dates.
