---
name: maximus-chain-of-verification
description: Apply Chain-of-Verification (CoVe) to any draft answer, research report, or synthesis to catch and fix hallucinated claims before delivery. Published research shows 40–60% hallucination reduction versus direct-answer generation. Load when the user asks to "fact-check," "verify," "reduce hallucinations," "double-check the claims," "grade the confidence," or "produce a verified report." Runs a 4-phase loop — draft → generate independent verification questions → answer each in isolation without the draft in context → revise — and outputs a claim-by-claim confidence ledger with revised text. Works on top of any Maximus research skill (deep-research, deep-research-pro, investigative-research, literature-review) or standalone drafts. Never labels a claim "verified" without independent-context confirmation. Never invents a source URL. Every removed claim keeps a "why removed" note.
---

# WHEN TO USE

Load this skill when the deliverable is a factual claim, research synthesis, report, memo, or brief and the cost of a hallucinated claim is real.

Specific triggers:
- "Fact-check this"
- "Verify these claims"
- "Reduce hallucinations in this draft"
- "Double-check before I send"
- "Grade the confidence on each claim"
- "Which of these numbers can we actually trust?"
- Any high-stakes deliverable — legal, clinical, financial, journalistic, competitive intel, board-facing

Also load when the user just finished a deep-research or synthesis pass and is about to publish, present, or send it. CoVe as a final layer catches what a first-pass draft misses.

# WHEN NOT TO USE

- Casual conversation, brainstorming, creative writing → CoVe is expensive; do not spend the tokens
- Answers that are purely opinion or subjective judgment (no verifiable claims) → nothing to verify
- Single-sentence lookups → simpler to just re-run the search
- User already ran a verification pass in the same session → do not re-run without new information

# CORE PRINCIPLE

**Independent verification means independent context.** The verification questions must be answered without the draft in the model's context. If the draft is still visible, the model will re-confirm its own claims — that is not verification, that is a rubber stamp.

# WORKFLOW

## Phase 1 — Draft (input)

The draft is either provided by the user, produced by an upstream skill (maximus-deep-research, maximus-deep-research-pro, maximus-write-article, maximus-investigative-research, maximus-literature-review), or generated in the same turn. Do not attempt to run CoVe on an empty input.

## Phase 2 — Question generation

Scan the draft. Extract every verifiable claim. For each claim, generate 1–3 independent verification questions.

Rules:
- **Verifiable claims only.** Numbers, dates, names, quotes, causal claims, attributions, benchmark scores, product features. Skip opinions, style, framing.
- **Neutral questions.** "What is X?" not "Is it true that X = 42?" — leading questions bias the verification.
- **Atomic.** One question per fact. Do not bundle.
- **Answerable independently.** The verification question must be answerable without the draft being visible. If it references "the study mentioned above," rewrite.

Store as `verification-questions.json` (see `references/output-format.md`).

## Phase 3 — Independent answering

Answer each verification question **without the draft in context**. Use fresh tool calls (search, fetch, connectors) as if the draft did not exist.

Rules:
- **Fresh context per question.** In practice: spawn a sub-agent or clear context before answering. The skill's runner script does this automatically.
- **Say "I don't know."** If the verification cannot confirm a claim, that is a first-class outcome. Do not hedge into a soft confirmation.
- **Capture source URLs.** Every confirmed answer keeps its source. Every "cannot confirm" records what was searched.
- **Do not re-cite the draft's own sources without re-fetching them.** A URL might have said something different than the draft claimed; re-check.

Store as `verification-answers.json`.

## Phase 4 — Revision

Merge verification answers back into the draft. For each claim:

- **Confirmed by independent verification** → keep the claim, keep the source, mark confidence: high.
- **Partially confirmed** (verification found a different number, close but not exact) → revise the claim to match the verified value, mark confidence: medium, note the correction inline.
- **Contradicted by verification** → remove the claim OR replace with the verified version, mark confidence: high (for the replacement), keep a "was: [original]" note.
- **Cannot confirm** → either soften ("appears to be" / "reportedly") with an explicit confidence: low tag, or remove the claim outright. Never silently keep an unconfirmed claim.
- **Opinion or subjective framing** → pass through unchanged. Not CoVe's job.

Output the revised draft plus a claim-by-claim ledger.

# OUTPUT FORMAT

Deliver three things, in this order:

## 1. Revised draft

The corrected text, ready to use. Any inline citations point to sources that the verification pass actually re-fetched.

## 2. Claim ledger

Table of every verifiable claim with:

| # | Claim (verbatim) | Verification question | Verified answer | Source URL | Confidence | Action |
|---|---|---|---|---|---|---|
| 1 | [claim] | [Q] | [A] | [URL] | high / medium / low | kept / revised / removed |

## 3. Change summary

Three-line rollup:
- Claims kept as-is: N
- Claims revised: N (list any that changed materially)
- Claims removed: N (list each with the reason)

# HARD RULES

1. **Never verify a claim in the draft's own context.** Independent context is the whole point. If it is not independent, it is not verification.
2. **Never invent a source URL.** If verification cannot find a supporting source, the claim is not confirmed. Full stop.
3. **Never label a claim "verified" that was only checked against the same source the draft used.** Re-fetch or use an independent source.
4. **Never suppress a "cannot confirm."** Users need to see what could not be checked.
5. **Never silently rewrite the draft.** Every material change goes in the ledger.
6. **Never run CoVe on non-factual content.** Opinions, style, framing, and narrative are out of scope.
7. **Never treat a verification pass as final.** If the user pushes back on a specific claim, run a targeted second pass on that claim only.

# INTEGRATION WITH OTHER MAXIMUS SKILLS

CoVe is a **post-processing skill**. It wraps other research skills:

- After `maximus-deep-research` (aggregation) → catches over-eager synthesis
- After `maximus-deep-research-pro` (inference) → catches inference that outran its evidence
- After `maximus-investigative-research` → catches single-source claims that need corroboration
- After `maximus-literature-review` → catches citation drift (paper A cited for a claim actually from paper B)
- After `maximus-write-article` → last pass before publishing
- After `maximus-counterparty-discovery` → mandatory before any external outreach or compliance-relevant claim

# RESEARCH BASIS

Chain-of-Verification originated in [Dhuliawala et al., 2023 (arXiv:2309.11495)](https://arxiv.org/abs/2309.11495). Reported hallucination reduction is 40–60% across list-based questions, closed-book QA, and long-form generation, depending on domain and base model.

The skill implements the "factored" variant — independent verification questions answered in isolation — which the original paper found strongest. Do not use the "joint" variant (all questions answered together with the draft visible); it under-performs and is what most naive fact-check prompts collapse into.

See `references/cove-paper-notes.md` for method details and `references/reliability-comparison.md` for how CoVe fits alongside RAG grounding, self-consistency, and process supervision.

## Recent (2026) practice notes

- **Anthropic's alignment/process-supervision work** (2026) shows chain-of-thought verification reduces error rate ~35% vs direct answer. CoVe is a specific, well-defined instance of this family.
- **Clinical and legal deployments** (2026) commonly pair CoVe with retrieval grounding — see `references/high-stakes-domains.md`.
- **Token cost:** CoVe roughly doubles output tokens versus a direct answer. Budget accordingly. It is not a default-on layer; it is a "before you send" layer.

# OUTPUT TEMPLATE

Deliver in this exact order:

```
## Revised draft

[corrected text]

## Claim ledger

| # | Claim | Q | Verified answer | Source | Confidence | Action |
|---|---|---|---|---|---|---|
[rows]

## Change summary

- Kept: N
- Revised: N — [list material changes]
- Removed: N — [list each with reason]

## Cannot confirm

[list of claims whose verification returned "no confirming source" — surfaced explicitly so the user decides whether to keep, soften, or cut]
```
