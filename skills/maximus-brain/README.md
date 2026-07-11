# maximus-brain

The cognitive operating system for the Maximus skill suite.

## What it is

A meta-skill that shapes *how* the LLM works on any non-trivial task. It doesn't change the model — it installs a deliberate workflow that runs before, during, and after every meaningful piece of work:

1. **Frame** the task before acting.
2. **Recall** memory and prior context.
3. **Select** the right skill or tool instead of reinventing.
4. **Execute** with minimum change and continuous verification.
5. **Self-critique** the draft before sending.

Brain is the difference between a fluent answer and a correct one.

## Why it exists

The most expensive LLM failures look the same: confident, fluent, and wrong. They almost always come from skipping the framing step, ignoring memory, freehanding work that a skill covers, or shipping the first draft. Brain is the protocol that closes those gaps.

It also right-sizes the cognitive effort. Some tasks need Fast (chat, lookup). Others need Extreme (deploys, money, irreversible action). Running Deep on everything wastes the user's time; running Fast on everything burns the field. Brain picks the tier in the first pass and commits.

## Quick start

Once installed, brain auto-fires on any non-trivial task. You don't have to name it. To explicitly trigger it on a small task, say one of:

- "Think hard about this."
- "Be careful here."
- "Use your brain."
- "Check your work before answering."
- "This matters."

To explicitly *skip* it (rare):

- "Quick one — don't overthink."

## What it does on a typical task

Given: "Add Stripe Connect onboarding to the marketplace."

Without brain: model jumps to writing code, asks the user for clarifications it could have inferred, may invent a Stripe API that doesn't exist, ships a draft.

With brain:

1. **Frame** — restates the goal in user's terms, flags assumptions (Standard Connect? Express?), picks **Deep** tier (money + integration).
2. **Recall** — pulls prior `maximus-fintech-payments` decisions from memory; reads the repo's existing Stripe wiring.
3. **Select** — loads `maximus-fintech-payments`, `maximus-design-spec`, `maximus-plan-implementation`.
4. **Execute** — works the plan, reads-before-edits, verifies after each commit.
5. **Critique** — re-checks every Stripe API call against actual docs, confirms idempotency + signed webhooks + audit log are in place, surfaces the rollback plan.

The user-visible difference: a correct answer the first time, with the right skills firing automatically.

## When NOT to use it

- One-line factual lookups ("what's the capital of Peru?").
- Casual conversation.
- Continuations where brain already fired earlier in the same turn.
- Tasks where the user explicitly asked for speed over rigor.

The cost of running brain on a small task is one paragraph of internal thinking. Cheap, but real — don't run Extreme tier on chat.

## Related skills

Brain is the conductor of the rest of the suite:

- `maximus-design-spec`, `maximus-plan-implementation` — invoked in the Frame pass for non-trivial work.
- `maximus-build-feature` — Execute pass for code work.
- `maximus-code-review`, `maximus-eval-and-test` — Critique pass for code and AI outputs.
- `maximus-devops-ship`, `maximus-fintech-payments` — auto-loaded for Extreme tier (production, money).
- `maximus-ai-fluency-for-builders` — the user-facing sibling. Brain teaches the AI to use itself well; fluency teaches the *user* to use AI well.
- `maximus-ai-safety-governance` — fires under brain in any task touching PII, prompt injection, or audit.
- All AI engineering skills (`maximus-prompt-engineering`, `maximus-rag-pipeline`, `maximus-agent-design`, `maximus-llm-model-selection`, `maximus-ai-cost-control`, `maximus-mlops-deploy`, `maximus-ai-ux-patterns`) — brain decides which ones fire in the Select pass.

## Glossary

- **Loop** — the five-pass sequence (Frame, Recall, Select, Execute, Critique).
- **Depth tier** — Fast, Standard, Deep, or Extreme. Picked in the Frame pass.
- **Self-critique** — the pre-response review that catches hallucinations, missed steps, and drift.
- **Evidence vs inference** — separating what a tool returned from what you concluded. Brain requires both to be traceable.
- **Memory hygiene** — searching memory at the start of any context-dependent task; writing durable facts as they appear.
- **Read-before-edit** — never write to a file you haven't read first. The Execute pass enforces this for code.
- **Confidently wrong** — the failure mode brain exists to prevent: fluent answers with no evidence behind them.

## Files in this skill

- `SKILL.md` — the spec the agent loads.
- `README.md` — this file.
- `HOWTO.md` — concrete recipes for triggering and verifying brain.
- `examples/` — worked traces showing the loop in action.
- `references/` — long-form material loaded on demand (failure-mode catalog, depth-tier rubric).
