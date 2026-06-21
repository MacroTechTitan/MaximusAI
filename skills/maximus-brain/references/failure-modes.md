# Failure modes — what brain is built to prevent

Long-form catalog of the LLM failure modes brain's five-pass loop counters. Each entry: the failure, what it looks like, the pass that catches it, and an example.

---

## 1. Confidently wrong (hallucination)

**The failure**: a fluent, well-structured answer that contains fabricated facts — invented APIs, wrong dates, made-up citations, hallucinated function signatures.

**What it looks like**: "Stripe's `transfer.complete` event…" (the event doesn't exist). "According to the 2024 RAND report on…" (the report doesn't exist). "Use `pandas.read_table_safe()`…" (no such function).

**Caught by**: Pass 5 self-critique — every non-trivial factual claim is verified against tool output or stable, well-known fact before the response ships. Names, APIs, URLs, dollar figures, dates, version numbers.

**Discipline**: if you can't point at the evidence in the same breath as the claim, hedge or verify.

---

## 2. First-interpretation lock-in

**The failure**: the model latches onto the first reading of an ambiguous request and runs with it, never re-checking whether that interpretation matches the user's actual intent.

**What it looks like**: user says "add a payment page" — model builds a Stripe Checkout integration when the user wanted a customer-facing receipt page. The work is good; the goal is wrong.

**Caught by**: Pass 1 Frame — restate the goal *in the user's terms*, name the assumptions explicitly. If the assumption is non-trivial, state it before executing so the user can correct in one turn.

**Discipline**: paraphrase, don't translate. The restated goal should sound like the user's voice.

---

## 3. Skill bypass

**The failure**: doing the work freehand when a Maximus skill (or built-in skill) exists for it. Re-deriving the procedure, missing the encoded gotchas, producing a weaker result than the suite's existing pattern would.

**What it looks like**: building a Stripe integration without `maximus-fintech-payments` loaded (so no idempotency, no audit log, no signature verification). Designing a RAG pipeline without `maximus-rag-pipeline` (so no rerank, no eval loop). Writing a spec from scratch without `maximus-design-spec`.

**Caught by**: Pass 3 Select — scan the skill index for a description match before doing the work. The skill exists precisely to encode the right way to do it.

**Discipline**: if a skill plausibly applies, load it. The cost of loading an unneeded skill is small; the cost of skipping a needed one is the bug it would have prevented.

---

## 4. Context blindness

**The failure**: starting work from scratch when memory or the workspace already contains the answer (or the user's preferences, or prior decisions). The agent feels like it has amnesia.

**What it looks like**: asking the user their company name when it's in `<user_background>`. Re-asking which database the project uses when prior sessions already established Postgres. Suggesting Vercel for a project that the user has previously said deploys on Replit.

**Caught by**: Pass 2 Recall — `memory_search` runs at the start of any context-dependent task. Workspace files get listed/read before the work begins.

**Discipline**: the cost of one focused memory search is a fraction of the cost of one wrong assumption.

---

## 5. Process theater

**The failure**: the agent narrates the loop instead of running it. "Let me think carefully about this…" "I'll start by restating the goal…" "Now I'll search memory…" The loop becomes performance.

**What it looks like**: paragraphs of meta-commentary before any real work, in a response where the actual answer is two sentences.

**Caught by**: the Output section of the SKILL.md — brain runs the loop internally; the user sees the calibrated result, not the protocol.

**Discipline**: the loop is the discipline; the answer is the artifact. Show the artifact.

---

## 6. Stall-asking

**The failure**: asking five clarifying questions when one (or none) would do. Brain is meant to *commit* in the Frame pass — state assumptions and act — not defer until the user does the framing for it.

**What it looks like**: response to "build a feature spec for vendor onboarding" → 6-question intake form instead of a draft spec with assumptions surfaced.

**Caught by**: Pass 1 — ask only when an answer would *change the work*. State assumptions for everything else.

**Discipline**: a confident draft with stated assumptions beats a stalled intake form. The user can correct one assumption faster than they can answer six questions.

---

## 7. Irreversible-action skip

**The failure**: shipping a deploy / sending an email / writing a file / charging a card without a final confirmation pass. The user has no chance to catch the issue before it lands.

**What it looks like**: model writes a 200-line draft and ships it to a Stripe live key without test-mode verification. Sends an email draft as the final action without `confirm_action`. Deletes a branch without checking what's on it.

**Caught by**: Extreme tier promotion + `confirm_action` for destructive moves + explicit verification step before the action.

**Discipline**: irreversible work gets the highest tier, full stop. Confirmation is non-negotiable.

---

## 8. One-size-fits-all depth

**The failure**: running Deep on chat (overhead, ceremony, annoyance) or Fast on a build (sloppy, missed steps, wrong answer).

**What it looks like**:
- "What's 2+2?" → 4 paragraphs of context-setting and assumption-stating.
- "Ship the Stripe integration to prod" → 2 sentences of "looks good, shipping it."

**Caught by**: Pass 1 — commit to a depth tier before working. Re-evaluate if the work proves harder or easier than framed.

**Discipline**: tier matches stakes. Chat is Fast; builds are Deep; money/deploys are Extreme.

---

## 9. Evidence-inference confusion

**The failure**: stating an inference as if it were evidence. Treating a plausible conclusion the same as a verified fact.

**What it looks like**: "The user wants Stripe Express Connect [because that's what most marketplaces use]" — said as fact, when it was actually inference. The user wanted Standard.

**Caught by**: Pass 4 discipline — separate evidence (what a tool returned) from inference (what you concluded). When you state a fact, point at the evidence.

**Discipline**: language matters. "Per the repo's existing config" (evidence) vs "I'm assuming Express based on market norms" (inference). The user can correct an inference; they can't correct a fact stated as ground truth.

---

## 10. Drift on long threads

**The failure**: over a long session, the agent loses track of the *current* goal and answers as if the goal were what it was 10 messages ago. The work is technically good; the target moved.

**What it looks like**: in turn 12 of a thread that has pivoted from "design the data model" to "ship the first endpoint", the agent answers a question with data-model reasoning instead of endpoint reasoning.

**Caught by**: Recipe 7 (manual reset) + Pass 1 — Frame runs at the start of every meaningful task, not just at the start of the thread. The current goal is the goal.

**Discipline**: re-frame at every meaningful pivot. Cheap, prevents the worst kind of drift.

---

## How to call out a failure mode in-session

If you, the user, see brain hit one of these:

1. Name it: "That looks like a hallucination — verify the API."
2. Or: "You skipped memory — check what we said last week."
3. Or: "Too much ceremony — give me the short version."

Brain is responsive to explicit feedback in-session. The catalog above is the shared vocabulary for that feedback.
