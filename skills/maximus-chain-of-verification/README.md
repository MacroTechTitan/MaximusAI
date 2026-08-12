# maximus-chain-of-verification

**Catch hallucinated claims before they leave the room.**

Chain-of-Verification (CoVe) is a documented technique for reducing hallucinated claims in LLM outputs by 40–60%. It works by drafting an answer, generating independent verification questions about each factual claim in the draft, answering those questions **without the draft in context**, and revising the draft to match the verified answers.

Method paper: [Dhuliawala et al., 2023](https://arxiv.org/abs/2309.11495).

This skill is not a fact-check prompt. Naive fact-check prompts collapse into "does the draft agree with itself?" — which the model always says yes to. CoVe forces independent context per verification, which is what actually works.

## When to reach for it

The high-stakes final layer. Load CoVe when:
- You just finished a deep-research or investigative pass and are about to publish/send
- The deliverable involves numbers, names, dates, quotes, benchmark scores, or attributions
- The domain is legal, clinical, financial, journalistic, or competitive intelligence
- The user says "fact-check," "verify," "double-check," or "grade the confidence"

Do not reach for it on brainstorming, creative writing, or opinion pieces. CoVe is expensive (~2x output tokens) and there is nothing to verify.

## What you get

- 4-phase workflow: Draft → Question generation → Independent answering → Revision
- Claim ledger: every claim tagged high / medium / low confidence, with source URLs from the re-fetch (not the draft's originals)
- Change summary: kept / revised / removed counts with reasons
- "Cannot confirm" list: claims the verification pass could not support, surfaced explicitly so you decide keep, soften, or cut

## What you do not get

- A rubber stamp. CoVe finds problems and shows them.
- A guarantee of zero hallucinations. It cuts the rate materially — not to zero.
- Style or opinion review. Wrong skill.
- Silent rewrites. Every material change goes in the ledger.

## Core rule

**Independent verification means independent context.** If the model can see the draft while answering the verification question, it is not verifying — it is re-confirming. The runner script (`scripts/run_cove.py`) enforces context isolation.

## Files in this bundle

- `SKILL.md` — spec and workflow (loaded by the agent)
- `README.md` — this file
- `HOWTO.md` — 6 recipes covering the most common CoVe patterns
- `examples/single-report-cove.md` — worked trace on a research memo
- `examples/list-question-cove.md` — worked trace on a list-answer question (highest historical hallucination rate)
- `references/cove-paper-notes.md` — method details from the original paper + 2026 replications
- `references/reliability-comparison.md` — how CoVe compares to RAG grounding, self-consistency, process supervision
- `references/high-stakes-domains.md` — clinical, legal, financial deployment notes for 2026
- `references/output-format.md` — JSON shapes for verification-questions.json and verification-answers.json
- `scripts/run_cove.py` — reference runner enforcing independent-context isolation

## Integration

CoVe is a post-processing skill. It wraps other skills — it does not replace them.

- After `maximus-deep-research` → catches over-eager synthesis
- After `maximus-deep-research-pro` → catches inference outrunning evidence
- After `maximus-investigative-research` → catches single-source claims
- After `maximus-literature-review` → catches citation drift
- After `maximus-write-article` → last pass before publish
- After `maximus-counterparty-discovery` → mandatory before outreach

## Freshness

Method: original [Dhuliawala et al., 2023](https://arxiv.org/abs/2309.11495). 2026 practice notes reflect state of the field as of **2026-07-31**. Refresh `references/` if using in production more than 6 months from that date — hallucination-reduction techniques evolve.
