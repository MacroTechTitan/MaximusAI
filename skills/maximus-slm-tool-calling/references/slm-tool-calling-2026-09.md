# SLM tool-calling sources — pulled 2026-09-30

**This file expires.** Model recommendations here age fastest. Re-verify after
about two months.

- Fixes in order of impact: a model whose chat template has native tool-call
  support, JSON-schema-constrained decoding, and a small tool surface. Native
  template calls are "the most reliable"; prompted JSON "fails at a much higher
  rate". Over-constraining can suppress reasoning, so constrain only the final
  action block. "Tool-call reliability is a training property, not an emergent
  one." Names Devstral-2 22B and the Qwen3-Coder line as agentic tunes
  ([LLM Configurator](https://llmconfigurator.com/en/guides/coding-agents/tool-calling-local-models), 2026-08-04).
- 7B/8B models "often lose track" of the tool-call pattern after the first
  tool result. Suggested fixes: one tool per sub-agent, minimal tool
  descriptions, truncating tool output, and explicit call-format instructions
  ([n8n community](https://community.n8n.io/t/tool-calling-chain-with-local-ollama-models-7b-14b-2nd-tool-never-executed/280320/4), 2026-03-24).
- llama.cpp GBNF: `--grammar` / `--grammar-file` on the CLI; JSON Schema via
  `json_schema` on completion endpoints and `response_format` on
  `/chat/completions`. Only a subset of JSON Schema is supported, and
  "Unsupported features are skipped silently". Objects default to no additional
  properties. `x? x? ...` repetition "may result in extremely slow sampling";
  use `x{0,N}` ([llama.cpp grammars README](https://github.com/ggml-org/llama.cpp/blob/master/grammars/README.md)).
- Ollama structured outputs via `format` (JSON schema) or `response_format`
  over the OpenAI-compatible API. Tool calls return in `message.tool_calls`
  ([Structured outputs](https://docs.ollama.com/capabilities/structured-outputs),
  [Tool calling](https://docs.ollama.com/capabilities/tool-calling)).
