---
name: maximus-ai-product-spec
description: "Spec an AI feature like a product, not a demo. Use when designing an AI-powered feature end-to-end: user-visible behavior, expected outputs, refusal and failure modes, eval rubric, staged rollout (off → internal → 5% → 100%), kill switch, and success metrics. Trigger phrases: 'spec an AI feature', 'write a product spec for', 'define AI behavior', 'plan rollout for AI', 'AI acceptance criteria', 'define success metrics for AI', 'how do we know the model is working'."
metadata:
  pillar: ai-engineering
  source: maximus
---

# Maximus — AI Product Spec

A demo is a model doing something impressive once. A product is a model doing the right thing reliably, failing gracefully, and improving measurably. This skill turns the gap between those two into a structured artifact.

## When to use

- Designing any user-facing AI feature from scratch.
- Expanding an existing AI feature (new inputs, new modalities, new use cases).
- Preparing for an internal or external launch where the team needs alignment on behavior.
- When someone asks: "what should the AI actually do?" or "how do we know it's working?"

If the feature doesn't involve a model (LLM, classifier, ranking, embedding, recommendation), use `maximus-design-spec` instead.

## Core rules

1. **Behavior first, model second.** Define what the user sees, what the system returns, and what happens when it fails — before choosing a model or prompt strategy.
2. **Refusals are features.** Document the cases where the model must decline. Silence on refusal design = accidental compliance issues.
3. **Eval before launch.** Every AI feature ships with a rubric. No rubric = no launch criteria = perpetual "almost ready."
4. **Staged rollout is not optional.** AI features can fail in subtle ways that only appear at scale. Gate each stage with explicit metrics thresholds.
5. **Kill switch at day one.** Plan the off-ramp before you need it.

## Procedure

1. **Load the prior art.** Read any existing design doc, PRD, or `maximus-design-spec` artifact. Note open questions. Use `search_web` to check if comparable features exist in the market.

2. **Define the user-visible behavior.**
   - What does the user invoke? (button, text field, API call, background trigger)
   - What do they see when the model succeeds? (format, length, tone, citations)
   - What do they see when the model fails or refuses?
   - What latency budget is acceptable? (< 1 s streaming first token, < 5 s full response?)

3. **Define expected outputs.**
   - Specify output structure: free text, JSON schema, ranked list, classification label.
   - Write 5–10 golden examples covering the core use case, edge cases, and boundary conditions.
   - Specify language, tone, and length constraints explicitly.

4. **Define refusal and failure modes.**
   - List the categories of inputs that must be refused (off-topic, harmful, PII, out-of-scope).
   - Define what the model says when refusing (never a blank 400 error to the user).
   - Define graceful degradation: if the model is slow, unavailable, or returning low-confidence output, what fallback do you show?

5. **Write the eval rubric.** See HOWTO.md §"How to design the eval rubric." At minimum:
   - Task success rate (human-rated or automated)
   - Safety pass rate (refusal on harmful inputs)
   - Format compliance rate
   - Latency P50/P95
   - User thumbs-up/thumbs-down ratio

6. **Plan the staged rollout.**
   - Stage 0: Off (feature flag disabled, infrastructure deployed).
   - Stage 1: Internal (team + trusted testers only).
   - Stage 2: 5% traffic (random or cohort-based).
   - Stage 3: 25% → 50% → 100% with defined hold times and metric thresholds between each.
   - Define the promotion criteria for each gate (e.g., "task success ≥ 80%, safety pass ≥ 99.5%, no P1 incidents in 72 h").

7. **Define the kill switch.**
   - Feature flag name and owner.
   - Who can flip it without approval? (on-call engineer, product lead?)
   - What automated trigger trips it? (error rate spike, latency breach, safety flag rate spike)
   - What does the user see when it's flipped? (fallback text, graceful removal of the feature)

8. **Define success metrics.**
   - Leading: task success, format compliance, thumbs-up rate, refusal accuracy.
   - Lagging: retention impact (D7, D30), feature engagement rate, support ticket rate.
   - Anti-metrics: what signals would indicate the feature is hurting (e.g., users deleting AI outputs and rewriting manually).

9. **Write the spec artifact.** Use `examples/spec-template.md` as the base. Populate all sections. Leave no TBD without an owner and date.

10. **Review with stakeholders.** AI specs need sign-off from: product, engineering, safety/trust-and-safety, and legal (if the feature touches regulated domains). Cross-reference `maximus-ai-safety-governance` for safety controls.

## Domain notes

- **Prompt engineering is implementation detail.** The spec describes behavior; `maximus-prompt-engineering` covers how to achieve it. Keep them separate.
- **RAG features** need an additional section: retrieval quality (recall, precision) and the behavior when retrieval returns nothing. See `maximus-rag-pipeline`.
- **Agent features** need tool-call scope, max iterations, and interruption behavior. See `maximus-agent-design`.
- **Fine-tuned models** need a base model version pinned in the spec and a plan for retraining cadence. See `maximus-fine-tuning`.
- **Eval rubrics** map directly to test suites. See `maximus-eval-and-test` for implementation.

## Gotchas

- Specs that say "the model will use judgment" without defining what good judgment looks like are not specs — they're wishes.
- Thumbs-up rate is gameable; pair it with task-success rate from blind human eval.
- Staged rollout only works if you actually measure metrics at each stage. Build the dashboard before Stage 1.
- A kill switch that requires 3 approvals is not a kill switch. Make it a one-person action.
- "We'll add refusal cases later" always means never. Write them in the spec.

## Output

A populated spec document (from `examples/spec-template.md`), an eval rubric (from `examples/eval-rubric.md`), a rollout plan table, and a list of open questions with owners and target-resolution dates.
