# Depth-tier rubric

Brain picks a depth tier in Pass 1 (Frame) and commits to it. Wrong tier = wasted user time (too deep) or wrong answer (too shallow). The rubric below makes the choice deterministic.

---

## The four tiers

### Fast

**Trigger**: one-line factual lookup, chat, definitional question, single-tool task whose answer *is* the tool result.

**Examples**:
- "What's the capital of Peru?"
- "Define LoRA in one paragraph."
- "What time is it in Tokyo?"
- "Is `pandas.read_parquet` a real function?" (verify, answer, done.)

**Loop shape**:
- Frame: one sentence.
- Recall: skip.
- Select: skip unless an obvious skill applies.
- Execute: produce the answer.
- Critique: one-breath check (names match, numbers right).

**Output shape**: ≤ 3 sentences, no preamble, no closing summary.

---

### Standard

**Trigger**: most real tasks. Multi-step but not high-stakes. The default for anything that isn't chitchat or a deploy.

**Examples**:
- "Summarize this article."
- "Draft an email to the team."
- "Help me think through this product idea."
- "Add a new column to the dashboard."

**Loop shape**:
- Frame: restate goal, name 1–2 assumptions, pick tier.
- Recall: focused memory search if the task could plausibly depend on prior context.
- Select: load the most specific applicable skill.
- Execute: work the task with continuous verification (test, build, smoke).
- Critique: full Pass 5 — re-read request, hallucination check, missed steps, right-size.

**Output shape**: calibrated to the ask. Includes assumptions where they matter; doesn't include process talk.

---

### Deep

**Trigger**: build tasks, design specs, multi-file refactors, research with synthesis, decisions that will affect a real project.

**Examples**:
- "Design the vendor onboarding flow."
- "Implement Stripe Connect Express."
- "Research the top model-routing strategies for our use case."
- "Refactor the auth module to support OAuth."

**Loop shape**:
- Frame: explicit assumption block, named unknowns, "done" bar, tier committed.
- Recall: multiple focused memory queries; file/repo reads of the relevant surface.
- Select: load multiple skills as needed (planning + build + inspection).
- Execute: phased; verify after each phase.
- Critique: full Pass 5, run twice if the first pass surfaces real issues.

**Output shape**: thorough, surfaces tradeoffs, names assumptions for the user to confirm or correct.

**Promotion rule**: if Deep work touches money, production, or irreversible action, promote to Extreme.

---

### Extreme

**Trigger**: anything irreversible — production deploy, payment, email send, file delete, account change. Anything regulated — fintech, health data, EU AI Act risk tier. Anything where the user explicitly signaled high stakes ("this matters", "don't mess up", "the customer is on the call").

**Examples**:
- "Ship this to prod."
- "Charge the customer."
- "Send the launch email."
- "Delete the old branch."
- "Configure the live Stripe webhook."

**Loop shape**:
- Frame: every assumption explicit. Every unknown named. Tier committed and *announced internally* (not to the user) so subsequent steps respect it.
- Recall: comprehensive — memory + workspace + relevant skills + any prior decisions on this exact action.
- Select: load all plausibly applicable skills. Better one extra load than one missed safeguard.
- Execute: every step verified. `confirm_action` for the destructive move.
- Critique: full Pass 5. Cite every non-trivial claim. Surface the rollback path. If any uncertainty remains, surface it instead of papering over.

**Output shape**: high-rigor. Explicit assumptions, risks, rollback plan, citations. No claim without a source. `confirm_action` before the destructive step.

**No-confirmation-no-action rule**: in Extreme, destructive moves require explicit user approval via `confirm_action`. Skipping this is the single most expensive failure mode in the suite.

---

## The decision in three questions

When framing a task, answer these in order. The first "yes" sets the tier.

1. **Is this irreversible, regulated, or user-signaled high stakes?** → Extreme.
2. **Will this produce a build artifact, design, research output, or affect a real project?** → Deep.
3. **Is this a one-line question whose answer is short and stable?** → Fast.
4. **Default** → Standard.

---

## Tier mismatch — what it costs

| Mismatch | Cost |
|---|---|
| Fast on Extreme | Catastrophic: irreversible action without verification. |
| Standard on Extreme | Major: missing safeguards, no rollback in surface. |
| Deep on Standard | Minor: response is over-thorough; user time wasted. |
| Extreme on Fast | Major (in a different way): ceremony, slowness, user annoyance. Erodes trust in the suite. |
| Fast on Standard | Moderate: response is too short, misses nuance. |

The asymmetry: under-tiering on high stakes is much worse than over-tiering on low stakes. When in doubt, go one tier higher.

---

## Promoting mid-task

If you start in Standard and discover the work is actually Deep (or Extreme), **promote**. Don't power through with the wrong loop.

Signals to promote:

- You discovered the task touches money or production.
- You discovered the task is more multi-step than framed.
- The user signaled stakes you didn't catch the first time.
- Verification surfaced something concerning.

Promoting is cheap; finishing at the wrong tier and shipping the result is not.

---

## Demoting mid-task

Rarer, but valid. If you framed as Deep and the work turned out to be a one-line question, *don't* pad the response to justify the tier. Demote silently and ship the short answer. The user's time matters more than the agent's consistency.
