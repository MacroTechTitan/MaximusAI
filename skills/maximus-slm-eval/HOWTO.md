# HOWTO — SLM Eval

Four recipes. Flags and formats: `references/slm-eval-2026-09.md`.

---

## 1. promptfoo side by side on Ollama

```yaml
# promptfooconfig.yaml
prompts:
  - file://prompt.txt           # identical for every provider
providers:
  - ollama:chat:qwen3-8b-16k
  - ollama:chat:gemma3-12b-16k
  - ollama:chat:phi4-mini-16k
defaultTest:
  options: { provider: { config: { temperature: 0 } } }
tests: file://cases.yaml
```

```yaml
# cases.yaml (excerpt)
- vars: { doc: file://docs/invoice-017.txt }
  assert:
    - type: is-json
    - type: javascript
      value: JSON.parse(output).total === "1,240.00"
- vars: { doc: file://docs/memo-004.txt }
  assert:
    - type: contains
      value: "[p.2]"          # must cite the passage
```

```bash
npx promptfoo@latest eval && npx promptfoo@latest view
```

The `-16k` tags are Modelfile builds with `num_ctx` set (see
`maximus-ollama-ops`), so every candidate runs the same context.

## 2. Quant degradation with lm-eval-harness

```bash
llama-server -m model-Q4_K_M.gguf --port 8080 &
lm_eval --model gguf --model_args base_url=http://127.0.0.1:8080 --tasks hellaswag
# repeat with the Q8_0 file, compare
```

This needs a llama.cpp release from December 2024 or later (modern logprobs
format). For a raw GGUF through the `hf` backend, pass a separate `tokenizer=`.
Without it, tokenizer reconstruction can take hours.

## 3. Throughput at real depth

```bash
llama-bench -m model-Q4_K_M.gguf -p 512 -n 128 -d 0,8192,16384 -r 5 -fa on
```

Read the `pp512 @ d16384` and `tg128 @ d16384` rows. Those are what you will
feel at 16K.

## 4. Decision memo

Fill in `examples/decision-memo.md`. If two candidates are within noise,
pick the smaller or faster one and say that it was a tie.
