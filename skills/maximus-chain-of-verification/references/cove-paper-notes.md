# CoVe — method notes from the original paper + 2026 replications

## Original paper

Dhuliawala, Komeili, Xu, Raileanu, Li, Celikyilmaz, Weston. *Chain-of-Verification Reduces Hallucination in Large Language Models.* [arXiv:2309.11495](https://arxiv.org/abs/2309.11495) (September 2023).

## The 4 phases (verbatim from the paper's framing)

1. **Generate baseline response** — produce the initial draft answer as-is.
2. **Plan verifications** — generate a list of verification questions targeting the factual claims in the baseline.
3. **Execute verifications** — answer each verification question. Best variant: **factored**, meaning each question is answered in a separate context with no visibility into the baseline or the other questions/answers.
4. **Generate final verified response** — revise the baseline in light of the verification answers.

## Variants (from the paper's ablations)

- **Joint** — all verification questions answered in one prompt, with the baseline visible. **Worst variant.** Model rubber-stamps its own baseline. Do not use.
- **2-step** — verification questions answered together, baseline hidden. Better than joint but still cross-contaminates between questions.
- **Factored (recommended)** — each question in a fresh context, baseline hidden, no cross-contamination. **Strongest across all benchmarks in the paper.**
- **Factor+Revise** — factored plus an explicit consistency check between the baseline claim and the verification answer. Marginal improvement over factored alone.

**This skill implements factored (Phase 3 spawns fresh contexts per question).** If you cannot spawn sub-agents, you can approximate factored by clearing the message history between verification questions — but sub-agents are cleaner.

## Reported gains (original paper)

- **List-based question tasks** (Wikidata list questions): baseline 0.15 F1 → CoVe factored 0.35 F1 (~130% relative improvement).
- **Closed-book QA** (MultiSpanQA): baseline 0.36 → CoVe 0.42.
- **Long-form biography generation** (FactScore metric): baseline 0.56 → CoVe factored 0.71 (~27% relative improvement).

Absolute numbers vary by base model and task. The 40–60% "hallucination reduction" figure commonly cited in 2026 practice is a rough aggregate across settings, not a single-paper number.

## 2026 replications and extensions

- **Chain-of-Verification variants** — multiple 2025–2026 papers extend CoVe with retrieval grounding, self-consistency voting on the verification step, and per-claim confidence scoring. Search arXiv for "Chain-of-Verification" post-2025 to find them.
- **Anthropic process-supervision (2026)** — Claude's internal alignment work confirms chain-of-thought verification reduces error rate ~35% versus direct answer, consistent with CoVe's mechanism.
- **Clinical / legal deployments (2026)** — CoVe paired with RAG has become common in high-stakes domains. Reported error rates approach 1–2% when the verification step must resolve to a primary source. See `references/high-stakes-domains.md`.

## Practical parameter notes

- **Question generation:** aim for 1–3 verification questions per claim. More than 3 is diminishing returns and cost.
- **Question style:** neutral form ("What is X?"), not leading form ("Is it true that X = 42?"). The paper's ablations show leading questions bias verification toward confirmation.
- **Atomicity:** one fact per question. "What is the revenue and headcount of X?" is two questions.
- **Independence:** never allow the draft to be visible during Phase 3. The whole method depends on this.
- **Token cost:** CoVe roughly doubles output tokens (baseline + verifications + revision). Budget accordingly.

## What the method does not fix

- **Systematic bias in training data.** If the base model has a wrong prior about a topic and no external source is consulted, CoVe cannot fix it. Pair with retrieval when the topic is domain-specific.
- **Undetectable hallucinations.** Claims that look identical to real facts but are false will pass verification against the model's own knowledge. This is why 2026 practice pairs CoVe with retrieval-grounding.
- **Multi-step reasoning errors.** CoVe verifies claims, not reasoning chains. For reasoning-chain verification, look at process supervision or step-by-step self-critique.

Last reviewed: **2026-07-31**.
