# maximus-agent-design

Production-grade multi-step AI agent design: tool definitions, loop control, memory, failure recovery, and the 3-tier eval harness.

## What this skill is

A structured approach to building LLM agents that call external tools across multiple steps — covering tool definition discipline, loop safety, memory architecture (short and long term), recovery from tool failures, and the evaluation discipline needed to ship agents to production without setting the building on fire.

## Why it exists / what problem it solves

Agents have higher blast radius than passive LLM features: a hallucinated tool call can delete data, send an email, or charge a customer. An infinite loop can exhaust a budget. Lost context can repeat expensive operations. This skill encodes the disciplines — hard loop limits, tool-result fencing, explicit memory management, and 3-tier eval — that prevent these failure modes from reaching production.

The core insight: most agent failures are *design* failures, not model failures. A vague tool description produces hallucinated tool calls. No loop limit produces runaway execution. No done condition produces unnecessary steps. Fix the design; the model follows.

## Quick start

1. **Define the task.** Success state? Failure state? Maximum steps? Write them down before coding.
2. **Define your tools.** For each tool: precise `description`, typed parameters with descriptions, and accurate return schema. Use the "precise, honest, complete" template in SKILL.md.
3. **Build the loop.** `step_count = 0; max_steps = 15; while not done and step_count < max_steps`. Never `while True`.
4. **Add error handling.** Wrap every tool call in try/except. Retry once, then inform the model and continue.
5. **Write evals.** Does the agent call the right tools? With the right args? Does it stop at the right time? Does it handle tool failures? Run via `maximus-eval-and-test`.

## When NOT to use it

- When the task is a single LLM call with no tools — that's `maximus-prompt-engineering`.
- When the task is retrieval without orchestration — that's `maximus-rag-pipeline`.
- When the task is a simple chatbot that doesn't need to take actions in external systems.
- When the agent is already working and the problem is model quality, not design — check `maximus-llm-model-selection`.

## Related skills

- `maximus-prompt-engineering` — system prompt for the agent, tool injection hardening
- `maximus-rag-pipeline` — RAG as a tool in the agent's toolkit
- `maximus-eval-and-test` — 3-tier eval harness (PR regression / nightly / prod canary)
- `maximus-llm-model-selection` — pick the right model for agentic tasks
- `maximus-build-feature` — implement the agent loop code

## Glossary

**Tool / Function calling** — A provider feature that allows the model to request execution of a named function with structured arguments. The application executes the function and returns the result to the model.

**Agent loop** — The control loop: model → tool call → execute tool → append result → model → repeat until done or step limit reached.

**ReAct pattern** — Reason + Act: the model produces a reasoning trace before each action, improving accuracy and reducing hallucinated tool calls.

**Hard step cap** — A maximum iteration count for the agent loop, enforced in code. Non-negotiable for production agents.

**Short-term memory** — The agent's context window: conversation history, tool calls, and results for the current session.

**Long-term memory** — Persistent storage (DB, vector store) of knowledge that survives session boundaries: user preferences, past task outcomes, learned patterns.

**Context window eviction** — When the context window fills, older messages must be dropped or summarised. Without explicit management, critical task context can be lost silently.

**Hallucinated tool name** — The model attempts to call a tool that doesn't exist in the available tool list. Prevention: enumerate available tools explicitly in the system prompt; validate tool names before dispatch.

**Runaway loop** — An agent that executes indefinitely without making progress toward task completion. Prevention: hard step cap + explicit done condition.

**Tool-call regression** — A breaking change in agent behaviour where the agent calls different tools or different argument values than before for the same input. Detected by the PR-time regression eval in `maximus-eval-and-test`.

**Injection via tool results** — A prompt injection attack where malicious content in a tool's response contains instructions that override the system prompt.

**Parallel tool calls** — Calling multiple independent tools in a single model turn, reducing round-trip latency.
