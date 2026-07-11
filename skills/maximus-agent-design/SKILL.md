---
name: maximus-agent-design
description: "Multi-step AI agent design: tool definitions, loop control, memory architecture (short and long term), recovery from tool failures, and the 3-tier eval (PR regression / nightly LLM-judge / prod canary). Use when the user says 'build an agent', 'autonomous task', 'tool-calling loop', 'LLM with tools', 'memory for the AI', 'the agent keeps looping', 'agent hallucinates a tool', 'agent loses context', or any task involving an LLM that calls external tools or runs multi-step. Covers common failure modes: hallucinated tools, runaway loops, lost context, recursive sub-tasks."
metadata:
  pillar: ai-engineering
  source: maximus
---

# Maximus — Agent Design

An agent without a harness is a horse without a rider — it may go somewhere interesting, or it may run through a fence. This skill is the harness: tool definitions that don't lie, loop controls that stop runaway execution, memory that doesn't leak, and an eval loop that catches failures before production does.

## When to use

- Building a system where an LLM controls a multi-step task using tools (function calling).
- Adding tools (web search, code execution, API calls, database queries) to an LLM workflow.
- Debugging agent failures: hallucinated tool calls, infinite loops, lost context, or runaway sub-tasks.
- Designing short-term (session) or long-term (persistent) memory for an agent.

Load `maximus-eval-and-test` for the full eval harness. Load `maximus-prompt-engineering` for the system prompt that governs the agent. Load `maximus-rag-pipeline` if one of the agent's tools is document retrieval.

## Core rules (non-negotiable)

1. **Tools are a contract.** Every tool definition must exactly match the underlying function's behaviour. A tool description that overpromises or underdescribes is the root cause of most agent hallucinations.
2. **Hard loop limits.** Every agent loop must have a maximum step count (hard cap ≤ 20 for most tasks). No exception. A runaway agent is a security and cost incident.
3. **Tool errors are not agent failures.** Design the loop to handle tool errors gracefully — retry once, then fall back, then report. Do not let a single tool failure crash the session.
4. **Memory has a budget.** Short-term memory (the context window) is finite. Design explicitly for what gets kept, summarised, or evicted.
5. **Eval before deploy.** Use the 3-tier harness from `maximus-eval-and-test`: PR-time tool-call regression → nightly LLM-judge → prod canary. Agents have higher blast radius than passive features; eval discipline is non-negotiable.
6. **Read before edit.** Check existing agent code with `read` before adding any new tool or loop logic.

## Procedure

1. **Define the task.** What is the agent trying to accomplish? What's a success state? What's a terminal failure state? Write these down before writing any code.
2. **List the tools.** For each tool: what does it do, what inputs does it take, what does it return, what can go wrong? Write the tool description before writing the implementation.
3. **Implement tool definitions.** Use the provider's function-calling schema. Every parameter must have a `description`. Every tool description must be accurate and complete — the model reasons about tools from descriptions alone.
4. **Build the agent loop.** Implement: `step_count = 0; max_steps = N; while not done and step_count < max_steps: ...`. Never a bare `while True`.
5. **Implement tool-error handling.** Every tool call wrapped in try/except. On error: retry once with backoff, then signal the model that the tool failed and ask it to continue without the result or choose an alternative.
6. **Design memory architecture.** Short-term: everything in the context window (auto). Long-term: decide what to summarise, what to persist to a DB, what to retrieve via RAG. Write the memory management logic explicitly.
7. **Write evals.** At minimum: does the agent call the right tool(s)? Does it call them with the right arguments? Does it reach the correct conclusion? Does it stop when done?
8. **Test adversarial cases.** Prompt injection via tool results, circular tool chains, tool unavailability, hallucinated tool names.
9. **Deploy with observability.** Log every tool call, every tool result, every loop iteration. Alert on: loop limit hit, tool error rate > 5%, latency p95 > threshold.

## Tool definition discipline

```python
# GOOD: precise, honest, complete
{
    "name": "search_knowledge_base",
    "description": "Search the internal product knowledge base for documentation, FAQs, and policies. Returns up to 5 relevant text passages with source titles. Does NOT search the web or external sources. Use for product questions only.",
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The search query. Be specific. Use terms the documentation would use."
            },
            "max_results": {
                "type": "integer",
                "description": "Number of results to return (1-5). Default: 3.",
                "minimum": 1, "maximum": 5
            }
        },
        "required": ["query"]
    }
}

# BAD: vague, overpromises
{
    "name": "search",
    "description": "Search for information.",
    "parameters": {"query": {"type": "string"}}
}
```

## Memory architecture

| Memory type | Scope | Storage | Use for |
|-------------|-------|---------|---------|
| In-context (short-term) | Current session only | LLM context window | Conversation history, current task state, tool results for the current step |
| Session summary | Current session only | Context window (compressed) | Summarise old turns when approaching context limit |
| Long-term episodic | Persistent across sessions | DB or vector store | "User X prefers Y", past task outcomes, learned preferences |
| Long-term procedural | Persistent | DB or skill file | Task-specific patterns, learned tool usage strategies |

Design rule: never let the context window fill silently. Implement a summarisation step when message count > N or token count > 80% of limit.

## Failure modes (see `references/failure-modes.md` for full catalogue)

- **Hallucinated tool names** — the model calls a tool that doesn't exist. Cause: vague or missing tool list. Fix: enumerate available tools explicitly in the system prompt.
- **Runaway loops** — the agent loops without making progress. Cause: no loop limit; task completion condition not clear. Fix: hard step cap + explicit done condition.
- **Lost context** — the agent forgets earlier steps and repeats work. Cause: context window eviction without summarisation. Fix: summarise old turns before eviction.
- **Recursive sub-tasks** — the agent spawns sub-agents that spawn sub-agents. Cause: no recursion depth limit. Fix: pass a `depth` parameter; refuse to spawn at depth ≥ N.
- **Injection via tool results** — tool output contains malicious instructions. Fix: fence tool results; system prompt explicitly states tool outputs are data, not instructions.

## Domain notes

- **ReAct pattern** (Reason + Act): the model produces a `<thinking>` block explaining its plan before calling a tool. Dramatically reduces hallucinated tool calls. Slight token cost.
- **Tool result validation.** After every tool call, validate the result schema. A tool that returns unexpected output corrupts the agent's reasoning. Fail fast with a clear error message.
- **Parallel tool calls.** Most providers support calling multiple tools in one turn. Use for independent queries (e.g., fetch A and B simultaneously). Do not use for dependent steps.
- **Structured tool outputs.** Tool functions should return JSON-serialisable dicts with consistent schemas, not free-form strings. The model reasons better over structured data.
- **Long-running tools.** For tools that take > 2 seconds, use async execution. Return a job ID; poll for completion in the next loop iteration.

## Gotchas

- **Parallelism breaks ordering assumptions.** If your agent relies on result-A before calling tool-B, don't parallelize those two calls.
- **Tool call retry storms.** Retrying a failed tool inside the loop adds iterations. Count retries toward the loop budget.
- **Context window fills with tool results.** Large tool outputs (1000+ tokens each) × 10 iterations = context window exhausted. Summarise or truncate tool results before appending to the message history.
- **Ambiguous done condition.** Without a clear "task complete" signal, the agent will hallucinate additional steps after the real work is done. Always define and check the done condition explicitly.

## Output

A running agent with: tool implementations, the agent loop with hard step cap, tool-error handling, memory management, a test suite covering the happy path + 3 failure modes, and logging of every tool call. Plus a monitoring setup that alerts on loop limit hits and tool error spikes.
