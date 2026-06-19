# maximus-prompt-engineering

Production discipline for writing, testing, and versioning LLM prompts.

## What this skill is

A structured approach to crafting LLM system prompts, few-shot example sets, JSON schema constraints, guardrails, and regression tests — applied consistently across Python and TypeScript codebases.

## Why it exists / what problem it solves

Most prompt failures are not model failures; they are specification failures. A vague prompt gets vague results. An untested prompt breaks in production the first time a user sends unexpected input. This skill encodes the patterns that prevent those failures: canonical prompt structure, schema enforcement, injection hardening, version control, and test-before-ship discipline.

## Quick start

1. **Identify the task.** Write one sentence describing the model's role and one sentence describing a perfect output.
2. **Draft the system prompt** using the four-section layout: Role → Context → Instructions → Output format.
3. **Add a JSON schema** via `response_format` if structured output is needed (not just prose instructions).
4. **Write five test cases** (2 happy path, 2 edge case, 1 adversarial) in a `tests/` file.
5. **Run the tests**, fix failures, version the prompt, and commit.

## When NOT to use it

- When the problem is that the model lacks the *information* to answer — that's a retrieval problem (`maximus-rag-pipeline`).
- When the problem is picking the wrong model entirely — that's `maximus-llm-model-selection`.
- When the problem is multi-step agent orchestration — that's `maximus-agent-design`.
- When you're doing a one-off exploratory chat that won't be deployed.

## Related skills

- `maximus-rag-pipeline` — add retrieval context to prompts
- `maximus-agent-design` — prompt engineering for tool-calling agents
- `maximus-llm-model-selection` — pick the right model before tuning the prompt
- `maximus-eval-and-test` — full regression harness for prompt testing
- `maximus-build-feature` — implementing the code that calls the prompt

## Glossary

**System prompt** — The instructions passed in the `system` role (or equivalent) that set the model's behaviour for the entire conversation.

**Few-shot examples** — Input/output pairs embedded in the prompt that demonstrate the desired format or reasoning pattern.

**Response format / JSON mode** — A provider-level parameter that constrains model output to valid JSON matching a specified schema. More reliable than prose instructions.

**Temperature** — Sampling randomness (0 = deterministic, 1 = creative). Set to 0 for structured output tasks.

**Prompt injection** — An attack where a user (or retrieved content) embeds instructions that override the system prompt. Must be hardened against explicitly.

**Prompt versioning** — Treating prompts as source-controlled artefacts with version identifiers, tested before deployment, not mutated in place.

**Guardrails** — Explicit refusal rules and safety constraints embedded in the system prompt to prevent harmful or off-topic outputs.

**Chain-of-thought (CoT)** — A prompting technique that asks the model to reason step-by-step before answering, improving accuracy on multi-step tasks at the cost of output tokens.

**Prompt caching** — A provider feature (Claude, Gemini) that stores processed prompt prefixes to reduce latency and cost on repeated calls with the same system prompt.

**Token budget** — The total context window consumed by the system prompt. Longer prompts leave less room for conversation and retrieved context.
