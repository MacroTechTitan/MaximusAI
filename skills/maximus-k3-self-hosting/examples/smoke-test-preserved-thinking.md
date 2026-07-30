# Example — preserved-thinking smoke test

**Goal:** verify that your K3 client (against the hosted API or your self-hosted vLLM/SGLang/TokenSpeed endpoint) correctly echoes `reasoning_content` across turns. This is the #1 K3 integration bug — dropping `reasoning_content` makes K3 behave worse on turn 2+, and the failure is quiet.

## Why this smoke test exists

From the [K3 README §6](https://github.com/MoonshotAI/Kimi-K3):

> "Kimi K3 was trained in the preserved thinking history mode. For multi-turn conversations and tool calls, Kimi K3 requires the complete assistant message returned by the API to be passed back to `messages` as-is — including `reasoning_content` and `tool_calls`, not just `content`."

Most OpenAI-compatible integrations round-trip `content` only. That works fine for models without preserved-thinking. K3 will not raise an error if `reasoning_content` is missing — it will silently perform worse on turn 2 onward.

## The test

Three turns:

1. **Turn 1 (user):** "Pick five random integers between 1 and 1000, then tell me only the first three."
2. **Turn 1 (assistant):** returns three integers as `content`, and the full list of five appears in `reasoning_content`.
3. **Turn 2 (user):** "What were the other two numbers you picked but did not tell me?"
4. **Turn 2 (assistant):** must return the remaining two integers.

If turn 2 returns "I don't remember" or invents new numbers, your client is dropping `reasoning_content`.

## Run it

```bash
export KIMI_API_KEY=sk-...
export KIMI_BASE_URL=https://platform.kimi.ai/v1   # or your self-hosted endpoint
export KIMI_MODEL=kimi-k3
python scripts/smoke_test.py
```

The script (in `scripts/smoke_test.py`) exits 0 on pass, 1 on fail.

## What "pass" looks like

```
Turn 1 content: 473, 921, 235
Turn 1 reasoning present: True
Turn 2 content: The other two numbers were 215 and 222.
PASS: preserved-thinking round-trip works.
```

## What "fail" looks like

```
Turn 1 content: 473, 921, 235
Turn 1 reasoning present: True
Turn 2 content: I don't remember the other numbers. Would you like me to pick a new list?
FAIL: Turn 2 did not return two integers. Preserved-thinking is likely mis-configured.
```

## The fix, if you fail

In your client wrapper that appends assistant messages back into `messages`, do this instead of copying only `content`:

```python
out = {"role": "assistant"}
if msg.content is not None:
    out["content"] = msg.content
reasoning = getattr(msg, "reasoning_content", None) or getattr(msg, "reasoning", None)
if reasoning is not None:
    out["reasoning_content"] = reasoning
if getattr(msg, "tool_calls", None):
    out["tool_calls"] = msg.tool_calls
messages.append(out)
```

Then re-run the smoke test.

## What this test does not cover

- Tool calls (add a tool-use turn if your agent uses tools)
- Vision input (add an image turn if your agent processes images)
- `reasoning_effort` tuning (this test uses `high`; production likely differs)

## Source

- [Kimi K3 Quickstart](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)
- [Thinking Effort guide](https://platform.kimi.ai/docs/guide/use-thinking-effort)
- [Kimi K3 README §6](https://github.com/MoonshotAI/Kimi-K3) — "Model Usage"
