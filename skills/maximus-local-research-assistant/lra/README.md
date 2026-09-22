# maximus-local-research-assistant

Build a research or learning assistant on a small local model that you can
actually trust — private, offline, zero marginal cost.

**The premise.** A small model is a careful reader with no reliable memory.
Hand it the page and it does good work; ask what it recalls and it invents.
Every design decision here follows from that: grounding over prompting,
decomposition over bigger context, refusal as a default output, and verification
before display.

**What it covers.** Two-model memory budgeting (generator + embedder), local
embedding model selection, chunking tuned for a small reader rather than a
frontier one, a refusal contract that gets tested first, task decomposition that
names which steps must route to a larger model, span-level citation, cheap
automatic verification, and study tooling — quiz and flashcard generation,
grounded explanation, spaced repetition — where the ground truth lives in the
corpus instead of the weights.

**Triggers.** "local research assistant", "offline RAG", "chat with my documents
privately", "study assistant", "learning app with a local model", "private
knowledge base", "no data leaves my machine", "small model keeps making things
up".

**Files.**
- `SKILL.md` — the 8-step workflow and anti-patterns
- `HOWTO.md` — five recipes, including a six-step hallucination diagnosis
- `references/local-rag-components-2026-09.md` — dated, sourced embedding/memory/grounding data
- `examples/study-assistant-design.md` — a full worked design on 16 GB of hardware

**Siblings.** `maximus-slm-local-stack` (read first — hardware, model, quant,
runtime). `maximus-rag-pipeline` for the production cloud counterpart.
`maximus-chain-of-verification` when cheap checks are not enough.
`maximus-eval-and-test` for the harness.
