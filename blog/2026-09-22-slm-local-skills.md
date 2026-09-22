# Maximus grows to 51 — hallucination is usually an architecture bug

*2026-09-22 · Macro Tech Titan*

The most common complaint about small local models is some version of "it just
makes things up." I have said it myself, about a 4B model, on a laptop, at
midnight, after it invented a citation with an author, a year, and a journal
that do not exist.

The instinct is to blame the model. Four billion parameters, what did you
expect. The instinct is wrong often enough to be expensive, because it sends
people looking for a bigger model when the actual defect is in the system built
around the small one.

Two skills ship today. One gets a small model running on hardware you own. The
other makes what you build on top of it trustworthy. Suite total: 51.

## The problem with the honest framing

A small language model is not a miniature frontier model. It is a different
instrument with a different competence envelope, and the envelope is lopsided
in a specific way.

It holds up well on: summarizing text you provide, extracting to a schema,
classification, reformatting, translation of common pairs, code completion in a
familiar language. Anything where the answer is present in the input.

It degrades sharply on: unretrieved factual recall, multi-step reasoning chains,
long-horizon agentic work, following many simultaneous constraints.

Read those two lists again and the design implication falls out. A small model
asked an open-ended factual question is a confident fiction generator — not
because it is badly trained, but because you asked it to do the one thing it
cannot do. The fix is not a better prompt. The fix is to stop asking.

## What I rejected first

My first pass at this was one skill called something like `maximus-slm-local`,
covering the whole story: pick hardware, pick a model, quantize it, build RAG on
it, done.

I killed it before writing a line of it. The two halves fail differently. One is
a memory-arithmetic and runtime problem where the answer is a number and a
command. The other is an application-architecture problem where the answer is a
retrieval design and a refusal contract. Jamming them together produces exactly
the vague middle that makes most local-LLM writeups useless — a paragraph on
VRAM, a paragraph on chunking, no arithmetic in either.

So: two skills, with an explicit handoff between them.

## `maximus-slm-local-stack` — the substrate

Hardware ceiling, then memory budget, then model, then quantization, then
runtime, then benchmark the actual box.

The load-bearing content is the part nearly everyone omits. Advice online quotes
model weights — roughly 0.6-0.65 GB per billion parameters at Q4_K_M — and stops
there. Then people size a machine for the model and run out of memory the first
time they paste in a long document, because the KV cache grows linearly with
context and nobody told them. For Llama 3.1 8B at FP16 KV, the cache alone is
around [4 GB at 32K context and about 16 GB at
128K](https://insiderllm.com/guides/kv-cache-optimization-guide/) — more than
the Q4 weights it sits beside.

That single fact reorders the whole conversation. "Will an 8B model fit in 8 GB"
is unanswerable until someone says how much context they need. So the skill asks
that first, shows both terms separately, and gives the mitigation order:
shorten context, then quantize the KV cache, and only then touch weight
precision.

On quantization it takes a position rather than listing options. Q4_K_M is the
default, costing roughly [0.05-0.1 perplexity versus full
precision](https://www.misar.blog/@synor/articles/gguf-q4km-vs-q5km) on 8B-70B
models. And the scheme matters more than the bit count — Q4_K_M measures a
+0.0535 perplexity delta against FP16 where legacy Q4_0 measures
[+0.2499](https://morgannriu.fr/en/blog/quantification-gguf-q4-q5-q8-choisir) at
the same bit budget. Never accept a bare "4-bit" claim.

It also settles a comparison that wastes a lot of people's time: Ollama versus
LM Studio is not a performance question, because [both wrap the same two
engines](https://getautonoma.com/blog/lm-studio-vs-ollama) — llama.cpp and Apple
MLX. Pick on ergonomics. The real fork is single-user versus concurrent serving,
and vLLM's roughly 16-20x concurrent throughput advantage is irrelevant to one
person at a laptop.

## `maximus-local-research-assistant` — the application

This is where the hallucination complaint actually gets solved, with four levers
in order of impact: grounding, decomposition, refusal, verification.

The interesting design work is in departing from cloud RAG guidance rather than
inheriting it. `maximus-rag-pipeline`, already in the suite, assumes cloud
embeddings and a frontier reader. Port its defaults to a 4B model and the output
gets worse:

- **Retrieve 3-5 chunks, not 15.** A frontier model can be handed twelve loosely
  relevant passages and sort it out. A small model gets distracted by the
  irrelevant ones and starts blending them.
- **Keep structural context inside the chunk** — title, section heading, page.
  A small model given a naked paragraph often cannot tell what it is about.
- **Spend spare VRAM on a reranker before a bigger generator.** With only four
  chunks reaching the reader, top-k precision beats parameter count.

Then the part I think matters most: refusal is a default output, not an edge
case. The prompt carries an explicit refusal contract, and you **test the
refusal path first**, with questions you know are absent from the corpus. A
system that never refuses is not grounded — it is guessing with extra steps.

Two things worth knowing if you assume local means compromised. Open embedding
models now [match or beat `text-embedding-3-large` on retrieval
accuracy](https://localaimaster.com/blog/local-vs-openai-embeddings) at zero cost
per million tokens. And there is working prior art at this scale:
[Local Deep Research](https://github.com/LearningCircuit/local-deep-research)
runs fully self-hosted across arXiv, PubMed, web, and private documents, and
reports [~95% on SimpleQA](https://andrew.ooo/posts/local-deep-research-self-hosted-ai-research-review/).
SimpleQA is a narrow short-answer benchmark and a high score there does not
transfer to open-ended synthesis — but it does dispose of the idea that local
means toy.

The best fit for a small model turns out to be studying. Quiz generation,
flashcards, grounded explanation — all transformations of text you supply, where
the ground truth sits in your corpus rather than in the weights. One rule: never
let the model grade factual correctness from its own knowledge. Grade against the
source span.

## The tradeoff I am not hiding

Both skills refuse to recommend themselves unconditionally. If your task needs
frontier reasoning and privacy is not a hard requirement, they say so and route
you to `maximus-llm-model-selection` and an API model.

The worked example in the second skill ends by naming what its design gives up:
cross-document synthesis and open-ended "state of the field" questions. Those
need a bigger model, the privacy requirement rules that out, and the system says
so instead of answering anyway.

That is the same argument as [last week's post about approval
prompts](./2026-09-15-mtt-claude-cursor.md), pointed at a different target.
A permission system that fires on everything protects nothing. A research
assistant that answers everything tells you nothing. In both cases the fix is
structural, and in both cases the honest version is less impressive to
demo — and considerably more useful on a Tuesday.

## Try them

```bash
git clone https://github.com/MacroTechTitan/MaximusAI.git
cd MaximusAI && ./install.sh
```

Both land in core, so they install by default: `maximus-slm-local-stack` and
`maximus-local-research-assistant`. The volatile parts — model names, VRAM
tables, embedding leaderboards — live in dated reference files with a source URL
and a pull date on every figure, because this field turns over in weeks. When
they go stale, they are meant to look stale.

Free, MIT, no tier. 51 skills.
