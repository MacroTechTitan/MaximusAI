# maximus-ai-fluency-for-builders

The meta-skill for using AI well. Not a guide to building AI products — a guide to using AI tools effectively while building *anything*.

## What this skill is

AI fluency is the ability to: decide when to delegate a task to AI, compose a request that gets a useful result, validate the result without re-doing the work, and choose the right tool from a growing ecosystem. It's the difference between a builder who is 7× faster with AI and one who is 1.2× faster and frustrated.

McKinsey's 2024 State of AI report documented a 7× difference in productivity between AI-fluent and non-fluent knowledge workers — the gap wasn't about access to tools, it was about how those tools were used.

This skill encodes that fluency as a repeatable procedure.

## Why it exists / what problem it solves

Most AI usage failures are not model failures. They are:
- **Delegation failures**: handing AI a task it can't do, or not handing it one it could.
- **Specification failures**: vague requests producing plausible but wrong output.
- **Validation failures**: shipping AI output that was never checked.
- **Tool selection failures**: using the wrong AI tool for the job.

This skill fixes all four.

## Quick start

1. **Triage the task.** Ask: can AI do this faster than me, at acceptable quality, with validation I can do in under 20% of the time saved? Use `references/delegation-decision-tree.md`.
2. **Compose the request** using the four-part structure: Context → Goal → Constraints → Verification hook.
3. **Run the task** in the right tool (see the tool-selection table in SKILL.md).
4. **Validate** using `examples/validate-output-checklist.md`. Spot-check three claims, run the code, or read the copy aloud.
5. **Iterate once** with a specific targeted instruction. If you need a third round, the original brief was under-specified — rewrite it.

## When NOT to use it

- **Purely mechanical tasks** (copy-paste, file rename, simple reformatting): just do it.
- **Tasks where you already know the exact output**: just write it.
- **Building an AI product**: this skill covers *using* AI tools. For building AI features, use `maximus-ai-product-spec` and `maximus-build-feature`.
- **Prompt engineering at depth**: this skill covers practical prompt patterns. For chain-of-thought, few-shot, structured outputs, and systematic prompt development, use `maximus-prompt-engineering`.

## Related skills

- `maximus-prompt-engineering` — Prompt engineering in depth (chain-of-thought, few-shot, structured outputs, evals).
- `maximus-llm-model-selection` — Choosing between Claude, GPT-4o, Gemini, and other models for specific tasks.
- `maximus-agent-design` — Designing multi-step agentic workflows.
- `maximus-rag-pipeline` — Building retrieval-augmented generation systems.
- `maximus-ai-product-spec` — Specifying AI features for a product.

## Glossary

**Delegation** — Handing a task to AI rather than doing it yourself. Effective when the task is well-specified and the output is verifiable.

**Four-part request structure** — Context / Goal / Constraints / Verification hook. The minimum structure for a request that gets a useful response.

**Verification hook** — The part of a request that tells the model how to make its output checkable. E.g., "include the URL for each claim" or "output as a numbered list I can test one by one."

**Prompt pattern** — A reusable template for a category of task (planning, research, drafting, code review, copy). Worth saving when it produces consistently good results.

**Prompt drift** — The tendency of a model in a long conversation to forget early constraints. Counter by re-anchoring with the original goal.

**Spot-check** — Verifying a sample of AI output claims against primary sources, rather than re-deriving all of them. The standard validation method for research output.
