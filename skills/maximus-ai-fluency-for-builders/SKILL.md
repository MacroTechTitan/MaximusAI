---
name: maximus-ai-fluency-for-builders
description: "The meta-skill for using AI well on real tasks. Use when deciding whether to delegate a task to AI, composing a request that gets a useful answer, validating AI output without re-doing the work, or choosing between Computer, Claude, Perplexity search, and other tools. Covers delegation heuristics, prompt patterns for planning/research/drafting/code review/copy, and output validation. The fluency layer that makes every other skill faster."
metadata:
  pillar: ai-engineering
  source: maximus
---

# Maximus — AI Fluency for Builders

Knowing which AI tool to use, how to ask it, and when to trust the answer — that is the skill. The model does not replace your judgment; it amplifies it when you direct it well and wastes your time when you don't.

## When to use

- Deciding whether to do a task yourself or hand it to AI.
- Writing a request and not getting what you wanted on the first try.
- Verifying AI output before shipping it.
- Choosing between Perplexity Computer, Perplexity search, Claude, Cursor, or another tool for the current task.
- Composing a multi-step workflow where AI handles some steps and you handle others.

If the task is purely mechanical (copy-paste, rename), just do it. If the task is purely creative and you already know what you want, just write it. AI fluency is for the large middle ground.

## Core rules

1. **Delegate tasks, not vibes.** A good delegation has: context (what already exists), goal (what done looks like), constraints (format, length, tone, dependencies), and verification step (how you'll check it).
2. **Match tool to task.** Fast lookup → Perplexity search. Deep multi-step work → Computer. Code editing in a repo → Cursor or Computer with `bash`/`edit`. Structured extraction → model with JSON schema.
3. **The first draft is a proposal.** AI output is raw material, not final output. You are the editor, not the transcriptionist.
4. **Validate by spot-check and structure, not by re-doing.** Check claims against sources, check structure against the spec, check code by running it — not by rewriting from scratch.
5. **Iterate with specificity.** "This isn't right" teaches the model nothing. "The second paragraph contradicts the constraint in the brief — tighten it to one sentence" teaches it exactly what you need.

## Procedure

1. **Triage the task.** Answer: Can AI do this faster than me, at acceptable quality, with validation I can do in under 20% of the time saved? If yes, delegate. If no, do it yourself or use AI only for a sub-task.
2. **Select the right tool.** Use the tool-selection table in `references/delegation-decision-tree.md`. The default is: Perplexity Computer for multi-step tasks, Perplexity search for lookups, Cursor for in-repo code edits.
3. **Compose the request.** Follow the four-part structure: Context → Goal → Constraints → Verification hook. Include a negative example ("not like X") when tone or format matters. For code: include the function signature, the test case, and the error you're seeing.
4. **Run the task.** For long tasks, break into checkpoints. Ask for an outline before the full draft. Ask for pseudocode before the full implementation.
5. **Validate output.** Run the skill's verification checklist (see `examples/validate-output-checklist.md`). For factual content: spot-check three claims against primary sources. For code: run the tests. For copy: read aloud.
6. **Iterate or accept.** One targeted revision round is standard. Two is acceptable. Three suggests the original request was under-specified — rewrite the brief, not the output.
7. **Capture the pattern.** If a prompt structure worked well, save it in `examples/` for reuse. Fluency compounds.

## Tool-selection cheat sheet

| Task type | Best tool |
|---|---|
| Multi-step research + synthesis | Perplexity Computer |
| Single-fact lookup | Perplexity search |
| In-repo code edit | Cursor / Computer with bash+edit |
| Structured data extraction | Computer with schema prompt |
| Iterative copy drafting | Computer or Claude |
| Long-context document review | Computer (large context) |
| Image generation | Computer media skill |
| Scheduled/automated tasks | Computer cron + programmatic tools |

## Prompt patterns by use case

- **Planning**: "Given [context], produce a numbered plan for [goal]. Each step: what, why, how to verify. Flag any blocking unknowns."
- **Research**: "Find [N] sources on [topic]. For each: title, URL, one-sentence relevance. Prioritize primary sources over summaries."
- **Drafting**: "Write a [format] for [audience] that achieves [goal]. Tone: [adjective]. Max [N] words. Do not include [exclusion]."
- **Code review**: "Review this diff for: correctness, edge cases, security issues, and style violations against [conventions]. Output: numbered findings with severity."
- **Copy**: "Rewrite this paragraph for [audience]. Keep the core claim. Cut to [N] words. Match the voice in [example]."

## Domain notes

- For RAG and agent tasks, read `maximus-rag-pipeline` and `maximus-agent-design` — AI fluency is the meta-layer, not the implementation guide.
- For model selection (Claude vs GPT-4o vs Gemini), read `maximus-llm-model-selection`.
- For prompt engineering at depth (chain-of-thought, few-shot, structured outputs), read `maximus-prompt-engineering`.

## Gotchas

- **Over-delegating low-stakes tasks** slows you down. Writing a two-sentence Slack reply yourself is faster than prompting for one.
- **Under-specifying** is the primary cause of bad AI output. The model fills gaps with plausible content, not correct content.
- **Trusting without verifying** — AI output is statistically plausible, not necessarily factually correct. Always run the verification step.
- **Prompt drift in iterative sessions** — after several back-and-forths, the model forgets early constraints. Re-anchor by restating the original goal.
- **Treating the first response as the ceiling** — the first response is a floor. Targeted iteration reliably raises quality.

## Output

A completed task (research doc, draft, plan, code snippet) that you can verify and ship, plus a note on whether the prompt pattern is worth saving for reuse.
