# HOWTO — SLM Tool Calling

Four recipes. Sources: `references/slm-tool-calling-2026-09.md`.

---

## 1. Regression set in 15 minutes

```jsonl
{"id":"t01","prompt":"What's in README.md?","expect":{"tool":"read_file","args":{"path":"README.md"}}}
{"id":"t02","prompt":"Run the tests","expect":{"tool":"run_tests","args":{}}}
{"id":"t03","prompt":"Thanks, that's all","expect":{"tool":null}}
{"id":"t04","prompt":"Read config.yaml then fix the port to 8080","expect":{"chain":["read_file","edit_file"]}}
```

Score each case on four booleans: parsed, tool, args, chain. Report rates, not
anecdotes. `maximus-slm-eval` turns this into a promptfoo suite.

## 2. Constrain only the action block (llama.cpp server)

```bash
curl http://127.0.0.1:8080/v1/chat/completions -d '{
  "messages": [{"role":"user","content":"Read README.md"}],
  "response_format": {"type":"json_schema","json_schema":{"schema":{
    "type":"object",
    "properties":{
      "tool":{"type":"string","enum":["read_file","edit_file","run_tests"]},
      "args":{"type":"object"}},
    "required":["tool","args"]}}}
}'
```

For think-then-act, run two calls: a free-text reasoning call, then a
constrained call that sees the reasoning and must return the action.

## 3. Same thing on Ollama

```python
from ollama import chat
schema = {"type":"object","properties":{
  "tool":{"type":"string","enum":["read_file","edit_file","run_tests"]},
  "args":{"type":"object"}},"required":["tool","args"]}
r = chat(model="qwen3-64k", messages=msgs, format=schema, options={"temperature":0})
```

Or use native `tools=[...]` and read `r.message.tool_calls`. Try native first,
and fall back to `format` if the model's pass rate is poor. Illustrative; run
it against your regression set.

## 4. One tool per step

```python
plan = ["read_file", "edit_file"]          # decided in code, or by one planning call
for tool in plan:
    r = chat(model=M, messages=msgs, tools=[TOOLS[tool]])   # only this tool offered
    result = run(r.message.tool_calls[0])
    msgs += [r.message, {"role":"tool","content":truncate(result, 4000)}]
```

The model never chooses from more than one tool, and never sees a raw
50 KB result.
