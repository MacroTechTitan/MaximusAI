# HOWTO — maximus-brain recipes

Concrete recipes for invoking brain, verifying it ran, and steering it. Each recipe has Goal / Steps / Verification / Common pitfalls.

---

## Recipe 1 — Force brain on a small task

**Goal:** Get the brain loop on a task it might otherwise skip (e.g., a quick code edit that actually has stakes).

**Steps:**
1. State the stakes in the request: "this is going to prod" / "the user is on the call" / "don't mess this up".
2. Or use the explicit trigger: "Use your brain on this." / "Think hard." / "Be careful here."
3. Brain frames the task, picks at least **Deep** tier, and runs the full five-pass loop.

**Verification:**
- The response opens with the actual work, not a preamble announcing the loop.
- Sources / file reads / memory pulls are visible in the work.
- A critique-level self-check is implied by the calibration of the answer (no fabricated APIs, no missed steps).

**Common pitfalls:**
- Naming the loop explicitly in the response is process theater. Brain runs the loop; it doesn't narrate it.
- Asking 4 clarifying questions instead of stating assumptions. Brain stalls only on questions whose answer would change the work.

---

## Recipe 2 — Skip brain on chitchat

**Goal:** Keep brain from running heavy on a one-line question.

**Steps:**
1. Ask the question conversationally, no stakes signal.
2. Or be explicit: "Quick one —" / "Just a fact check —" / "No need to overthink".
3. Brain stays in **Fast** tier: one-sentence frame, no skill load, one-breath critique.

**Verification:**
- Response is ≤ 3 sentences for a one-line question.
- No skill is loaded, no memory call, no tool call unless one is obviously needed.

**Common pitfalls:**
- Brain over-firing is the agent's bias; if you see it adding ceremony to a chat, you can say "lighter" and it should drop tier.

---

## Recipe 3 — Verify the Frame pass happened

**Goal:** Make sure brain actually framed the task instead of jumping to action.

**Steps:**
1. Give a request with an obvious ambiguity ("add auth to the app").
2. A good Frame pass will either ask the one clarifying question that matters (OAuth or password? which provider? scope?) **or** state the assumption explicitly ("Assuming Google OAuth based on prior work in this repo — proceeding…").
3. A bad pass jumps into code with no framing.

**Verification:**
- The first action is either a focused clarifying question or a stated assumption — never silent guesswork.
- If you read the response and don't know what was assumed, the Frame pass was skipped.

**Common pitfalls:**
- Stall-asking — burying the user in 5 clarifying questions when 1 would do. The Frame pass is meant to *commit*, not to defer.

---

## Recipe 4 — Catch a skipped Recall pass

**Goal:** Spot when brain ignored memory or prior context.

**Steps:**
1. Reference something from a prior session indirectly ("for the Stripe project").
2. Brain should run `memory_search` and surface the relevant context before doing the work.
3. If it asks "which Stripe project?" without searching first, Recall was skipped.

**Verification:**
- The agent's response references prior decisions or files without you having to repeat them.
- "Based on the prior session…" or "From the existing repo…" appears in the work, not just at the end.

**Common pitfalls:**
- Recall returning nothing relevant is fine — but brain should still have *tried*. Silent skip is the failure.

---

## Recipe 5 — Force Extreme tier for irreversible action

**Goal:** Get the highest-rigor protocol before a deploy, payment, send, or delete.

**Steps:**
1. Frame the action as irreversible: "ship this to prod", "send the email", "charge the customer", "delete the branch".
2. Brain promotes to **Extreme** tier: explicit verification step, `confirm_action` for the destructive move, every non-trivial claim cited, rollback path stated.

**Verification:**
- Before the destructive action, you see a draft + a `confirm_action` prompt.
- The response names what gets reverted on rollback and how.
- Stripe / payment / deploy paths cite the actual API or doc, not a generic recollection.

**Common pitfalls:**
- Skipping `confirm_action` is the most expensive miss in the suite — brain should never destruct silently on Extreme.

---

## Recipe 6 — Trigger the self-critique pass

**Goal:** Catch hallucinations or missed steps before the response ships.

**Steps:**
1. Ask for something fact-heavy ("write a summary of the EU AI Act risk tiers with article references").
2. Brain's Pass 5 should verify every non-trivial claim before responding.
3. If something can't be verified, brain hedges ("the Act distinguishes four tiers; the exact article numbers are best confirmed against the [official text]") rather than fabricating.

**Verification:**
- Citations link to real URLs from the tool calls in the trace, not invented references.
- Numbers, model names, library APIs match the actual sources.
- When brain doesn't know, it says so — and offers a verifiable path forward.

**Common pitfalls:**
- "Confident wrong" is the failure mode this recipe targets. If you ever see fabricated citations, the critique pass didn't run. Call it out — brain learns from explicit feedback during the session.

---

## Recipe 7 — Reset brain on a long thread

**Goal:** Re-anchor brain when a long session has drifted.

**Steps:**
1. Say: "Let's reset — what is the goal now?" or "Restate the goal in your own words."
2. Brain runs Pass 1 again from scratch, surfacing the current goal, assumptions, and depth tier.
3. The rest of the work resumes from a clean frame.

**Verification:**
- Brain restates the goal in *your* terms, not its own paraphrase.
- It names the assumptions it's working under, including any inherited from earlier in the thread.

**Common pitfalls:**
- Long threads accumulate drift. The reset is cheap and worth doing whenever the work feels off.
