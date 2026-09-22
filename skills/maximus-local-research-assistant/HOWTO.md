# HOWTO — Local Research Assistant

Five recipes. Read `SKILL.md` first, and `maximus-slm-local-stack` before that
if the hardware and model are not yet settled.

---

## 1. Stand up a private "chat with my documents"

1. **Budget both models.** Generator + embedder must be resident together
   (~6 GB for 8B Q4 plus a small embedder). Add KV cache at real context.
2. **Pick the embedder** from `references/local-rag-components-2026-09.md`.
   Pin the version — changing it invalidates the whole index.
3. **Chunk for a small reader.** Small chunks, real overlap, and document title
   plus section heading kept inside each chunk.
4. **Index locally.** Chroma or pgvector is plenty at personal-corpus scale;
   see `maximus-rag-pipeline` for store selection tradeoffs.
5. **Retrieve 3-5 chunks, not 15.** Add a small reranker before adding a larger
   generator.
6. **Write the grounding prompt** with an explicit refusal string.
7. **Test refusal first** with questions you know are absent.
8. **Add span citations**, then the step-7 verification checks from `SKILL.md`.

## 2. Diagnose "my small model keeps making things up"

Work in this order, because the first two causes account for most cases:

1. **Is it retrieving the right passage at all?** Log the retrieved chunks for
   the failing question and read them yourself. If the answer is not in there,
   this is a retrieval bug and no prompt change will fix it.
2. **Are chunks too big or missing headings?** A 2,000-token chunk with no
   title gives a small model too much to hold and no anchor.
3. **Is refusal even possible?** If the prompt has no refusal contract, the
   model will always produce something.
4. **Too many chunks?** Drop from 10-15 to 3-5 and re-measure.
5. **Is the question multi-hop?** Decompose into single hops with retrieval
   between each, per `SKILL.md` step 5.
6. **Only now** consider a bigger model or a fine-tune.

Report which of the six it was. "Fixed by reducing k from 12 to 4" is a real
finding; "improved the prompt" usually is not.

## 3. Build a study assistant over your own material

1. Index the corpus per recipe 1.
2. **Quiz generation:** retrieve a passage, have the model produce N questions
   plus the source-backed answer plus the supporting span, all in one
   schema-constrained output. Never generate a question without its span.
3. **Flashcards:** same shape, shorter. Store the span with the card so the
   learner can always see where it came from.
4. **Scheduling is code.** Implement spaced repetition (SM-2 or FSRS) in
   Python. Do not ask the model for intervals.
5. **Explanation:** retrieve first, explain from retrieved text, show the
   source under the explanation.
6. **Grading:** compare against the stored span, or present the span and let
   the learner self-grade. Never let the model grade factual correctness from
   its own knowledge.
7. **Spot-check 20 generated items by hand** before trusting a batch of 500.

## 4. Decide what stays local and what routes up

Build the table from `SKILL.md` step 5 for the specific application, then:

- If every hard step can be dropped or decomposed, go fully local. Say what was
  given up.
- If one or two steps need a frontier model and privacy allows, go hybrid, and
  document exactly what leaves the machine — that sentence is the thing a
  privacy-motivated user actually needs.
- If privacy forbids routing up and hard steps remain, state the reliable range
  and refuse outside it. Shipping confident wrong answers is the worse outcome.

## 5. Build the eval set before you need it

Retrieval and generation must be measured separately or you cannot debug
either. Minimum viable eval, 30-50 items:

- **Retrieval:** question plus the chunk ID that should be retrieved. Score
  recall@k. This is the cheapest high-value metric you will build.
- **Generation, answerable:** question, gold answer, expected source span.
- **Generation, unanswerable:** questions absent from the corpus. Expected
  output is the refusal string. **Make this at least a third of the set** —
  refusal is the behavior most likely to regress silently.
- **Numbers:** items whose answers contain figures, since that is where small
  models drift most.

Run it on every change to chunking, embedder, k, reranker, or prompt. See
`maximus-eval-and-test` for harness structure.
