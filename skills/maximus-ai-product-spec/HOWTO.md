# HOWTO — maximus-ai-product-spec

Step-by-step recipes for AI feature specification work.

---

## Recipe 1: How to draft an AI feature spec

**Goal**: Produce a complete, reviewable product spec for an AI feature.

**Steps**:
1. Copy `examples/spec-template.md` to `docs/specs/<feature-name>.md` in your project.
2. Fill in: feature name, problem statement, user story (as a [user type], I want [behavior] so that [outcome]).
3. Define the user-visible behavior: what does the user invoke, what do they see on success, what do they see on failure?
4. Write 5–10 golden examples (input → expected output). Cover: typical case, short input, long input, edge case, borderline refusal case.
5. Define output structure: free text, JSON schema, ranked list? If JSON, write the schema inline.
6. Define latency budget: first-token latency (acceptable if streaming), total response latency (hard cap).
7. Fill in the refusal/failure modes section (Recipe 2 covers this in detail).
8. Fill in the eval rubric section (Recipe 3).
9. Fill in the rollout plan section (Recipe 4).
10. Fill in the kill-switch section (Recipe 5).
11. List open questions with an owner and a target-resolution date for each.
12. Share for review with: product, engineering, safety, legal (if regulated domain).

**Verification**: Every section in the template is filled. No TBD without an owner. At least 5 golden examples exist.

**Common pitfalls**:
- Writing "the model will respond helpfully" instead of defining what helpful looks like in output format and length.
- Skipping refusal design because "we'll handle edge cases later."
- Writing the spec after the prompt is already in production. Write it first.

---

## Recipe 2: How to define refusal and failure modes

**Goal**: Enumerate every input category the model should refuse, and what it says when refusing.

**Steps**:
1. List the primary task the model is designed for (e.g., "answer questions about our product documentation").
2. For each of the following categories, decide: refuse or degrade gracefully? Document both the trigger and the response.
   - Off-topic inputs (completely unrelated to the task)
   - Harmful or policy-violating inputs (violence, hate, self-harm, illegal activity)
   - PII in inputs (user submits their own SSN, health data, etc.)
   - Ambiguous inputs (too vague to answer)
   - Inputs in unsupported languages
   - Inputs exceeding length limits
3. For each refusal: write the exact message the user sees. "I can't help with that" is not a refusal — it's a shrug. Write a message that explains why and, where possible, what the user can do instead.
4. For graceful degradation: define the fallback. If the model is unavailable, show [fallback text X]. If confidence is below threshold, show a disclaimer.
5. Define the behavior when the model hallucinates high-confidence incorrect answers. (Common failure mode: no citation, no disclaimer, wrong answer. Define whether a confidence disclaimer or citation is required.)
6. Add all refusal categories to the eval rubric as a "safety pass rate" metric.

**Verification**: Every refusal has a trigger definition and a user-facing message. No refusal says "error" without a user-friendly fallback.

**Common pitfalls**:
- Defining refusals only for obvious harmful content; missing domain-specific edge cases.
- Refusal messages that expose system internals ("our prompt says we can't do that").
- Not testing refusals — they drift with prompt changes unless the eval rubric enforces them.

---

## Recipe 3: How to design the eval rubric

**Goal**: Define quantitative acceptance criteria that make "the AI is working" a testable claim.

**Steps**:
1. Open `examples/eval-rubric.md`. Fill in the feature name.
2. Define the primary task metric. For generation tasks: human-rated task success rate (target ≥ %). For classification: accuracy, F1, or AUC. Write the definition of "success" for human raters.
3. Define safety metrics: safety pass rate on a test set of adversarial inputs (target ≥ 99%). Refusal accuracy on a test set of inputs that should be refused (target ≥ 99%).
4. Define format compliance rate: what percentage of outputs match the required format (JSON schema, length limit, citation format)?
5. Define latency targets: P50 and P95 first-token latency (for streaming) and total response latency.
6. Define user feedback metrics: thumbs-up/down target (as a directional signal, not a sole criterion).
7. Define per-stage thresholds: what does each metric need to be at Stage 1 (internal), Stage 2 (5%), Stage 3 (full)?
8. Add the rubric to the spec document. It becomes the acceptance gate for promotion between rollout stages.

**Verification**: Every metric has a numeric target, a measurement method, and a stage-level threshold.

**Common pitfalls**:
- Setting targets without a baseline measurement from the current state (or a comparable model).
- Using only user thumbs-up as the quality signal — it's noisy and gameable.
- Rubric exists in the spec but no one owns running the evaluation. Assign an owner.

---

## Recipe 4: How to plan a staged rollout

**Goal**: Define the rollout stages, promotion criteria, and hold times to safely expand an AI feature.

**Steps**:
1. Define Stage 0 (Off): Feature flag deployed and disabled. Infrastructure and monitoring in place. Dashboard showing all rubric metrics is live before Stage 1 begins.
2. Define Stage 1 (Internal): Enable for internal team and trusted testers only. Hold for minimum 3 business days. Collect: task success rate, safety incidents, latency. Fix any P0/P1 issues before Stage 2.
3. Define Stage 2 (5%): Random or cohort-based 5% traffic slice. Minimum hold: 7 days OR 1,000 model calls, whichever comes later. Promotion criteria: primary task metric ≥ Stage 1 target, safety pass rate ≥ 99.5%, no P1 incidents in the hold period.
4. Define Stage 3+ (25% → 50% → 100%): Define the hold time and promotion criteria for each increment. Automate the metrics dashboard; promotion should be a deliberate human decision on verified data.
5. Document who approves promotion at each stage (product lead + tech lead minimum).
6. Define the automated signal that triggers a hold or rollback: e.g., safety flag rate > 0.5% in a 1-hour window, latency P95 > 2× target, error rate > 1%.

**Verification**: Every stage has a hold time, promotion criteria, and an approver. Automated rollback triggers are defined.

**Common pitfalls**:
- "Internal" stage that includes 100 people on the first day — meaningless as a gate.
- No dashboard built before Stage 1, so promotion decisions are made on gut feeling.
- Promotion criteria that nobody checks — build a Slack alert or a dashboard that surfaces the go/no-go metrics automatically.

---

## Recipe 5: How to define a kill switch

**Goal**: Ensure the AI feature can be disabled immediately, by one person, with a pre-planned user experience.

**Steps**:
1. Name the feature flag (e.g., `enable_ai_answer_suggestions`). Document it in the spec and in the deployment config.
2. Designate the owner: who is the on-call engineer or product lead who can flip the flag without approval? This must be one person, not a committee.
3. Define automated triggers: specify the metric condition that should automatically trigger an alert (not necessarily an auto-disable — but an alert that wakes someone up). E.g., safety filter flag rate > 1% in a 30-minute window.
4. Define what the user sees when the feature is disabled: a fallback message, the non-AI version of the feature, or a graceful removal of the UI element. Write this fallback copy now.
5. Test the kill switch during Stage 1. Flip it, verify the fallback appears, flip it back. Don't discover it's broken during an incident.
6. Document the escalation path: if the on-call flips the kill switch, who gets notified? (product lead, safety team, engineering manager)

**Verification**: The kill switch has been tested and works. The owner is named. The user-facing fallback is implemented and verified.

**Common pitfalls**:
- Kill switch requires a code deployment to activate — useless in an incident. Must be a runtime flag.
- Fallback is an error page. Users see "500 Internal Server Error." Plan a real user-facing fallback.
- Kill switch owner is "the team." No individual = no accountability = slow response.
