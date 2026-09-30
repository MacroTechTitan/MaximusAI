---
name: maximus-slm-tool-calling
description: "Make small local models (roughly 3B-32B) call tools and emit JSON reliably. Covers native chat-template tool calling vs prompted JSON, grammar-constrained decoding (llama.cpp GBNF / JSON schema, Ollama format), shrinking the tool surface, one-tool-per-step decomposition, tool-result truncation, and a malformed-call regression test. Use for 'local model won't call tools', 'agent writes the tool call as text', 'invalid JSON from Ollama', 'GBNF', 'constrained decoding', 'function calling with a small model'."
metadata: { "openclaw": { "emoji": "🧰", "pillar": "ai-engineering", "source": "maximus" } }
---

# Maximus — SLM Tool Calling

Frontier models make tool calling look like a solved problem. Small models
expose how narrow the channel really is: the call wrapped in an apology, `file`
where the schema said `path`, or a perfectly worded description of the call
instead of the call itself. None of that is fixed by writing "please" in
capitals.

## Purpose

Take a local agent that fails at tool calls and make its failure rate
measurable, then low. Work through the fixes in order of impact, and prove
each one with a regression set rather than a single lucky run.

## Scope boundary

| Need | Skill |
|---|---|
| Reliable tool calls / JSON from a small model | **this skill** |
| Agent loop design, memory, recovery (any model) | `maximus-agent-design` |
| Prompt and schema wording | `maximus-prompt-engineering` |
| Runtime config (`format`, templates, context) | `maximus-ollama-ops` |
| Measuring pass rate across models | `maximus-slm-eval` |

## The three ways a model calls a tool

1. **Native, via the chat template.** The model was trained to emit calls in
   a format its template encodes, and the server returns a structured
   `tool_calls` field. The most reliable path, when it exists.
2. **Prompted JSON.** Tools are described in the prompt and the harness parses
   the reply. Works with any model and fails far more often, because nothing
   enforces the shape.
3. **Edit formats.** Diffs or search/replace blocks instead of a schema.
   Weaker models handle text formats better, and the failures are visible.

## Core workflow — fixes in order of impact

1. **Build the regression set first.** Collect 20-50 real prompts with their
   expected tool and arguments, including multi-step chains and a few where no
   tool is the right answer. Score: parses, right tool, right arguments,
   chain completes. Without this, every "fix" is anecdote.
2. **Use a model trained for tool use.** Reliability is a training property:
   two models of the same size can differ enormously. Prefer agentic or coder
   tunes, and confirm `ollama show` lists the `tools` capability.
3. **Confirm the template.** A GGUF imported without its tool-call template
   silently degrades to prompted JSON. Check `ollama show --template`.
4. **Constrain the decode.** Grammar-constrained decoding masks every token
   that would break the schema, so invalid JSON is never produced. llama.cpp
   converts JSON Schema to GBNF (`json_schema` on completions,
   `response_format` on `/chat/completions`, `--grammar-file` on the CLI).
   Ollama takes a schema in `format`. Constrain the *action block*, not the
   whole reply: forcing structure at every token can suppress the reasoning
   the model would otherwise do first.
5. **Shrink the tool surface.** Fewer tools, shorter descriptions, enum-typed
   arguments. Each tool definition is also context the model must hold.
6. **Decompose chains.** Small models commonly lose the tool-call pattern after
   the first tool result. Give each step one tool, with the orchestration in
   code rather than in the model.
7. **Truncate tool results.** Large outputs push the model past its effective
   working memory. Summarize or slice before feeding them back.
8. **Validate and retry once.** Parse against the schema. On failure, send
   the exact validation error back once, then fail loudly. Never loop.

## Grammar gotchas

- llama.cpp supports a **subset** of JSON Schema. Unsupported features are
  skipped silently, so test the converted grammar with the Python converter
  or `llama-gbnf-validator`.
- Objects default to **no additional properties** in the converter.
- Patterns like `x? x? x? ...` can make sampling very slow; use `x{0,N}`.
- Constrained shape is not correctness. A schema-valid call to the wrong
  tool with the wrong ID still needs checking.

## Anti-patterns

- **"You MUST call the tool" as the whole fix.** It helps a little, and it
  does not replace a template or a grammar.
- **Twelve tools on a 7B model.** Split the agent.
- **Grammar over the whole reply** on a reasoning task. Let it think, then
  constrain.
- **Judging from one run.** Tool-call failure is a rate; measure it.
- **Retrying until it parses.** That hides a broken setup and burns latency.

## Output

The regression set, a before/after pass-rate table per fix applied, the final
schema or grammar, and a one-line statement of the residual failure rate the
user is accepting.
