# Preserved-thinking cost — reference

**What it is:** Kimi K3 is trained in preserved-thinking-history mode. For multi-turn conversations and tool-call sequences, the [Kimi K3 API](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart) requires the full assistant message — including `reasoning_content` and `tool_calls` — to be echoed back in the `messages` array as-is on the next turn. This differs from most OpenAI-compatible integrations, which only round-trip `content`.

**Why the skill cares:** Preserved-thinking mode multiplies input tokens across a session. Model-selection recommendations that ignore this will under-estimate K3's cost per multi-turn task versus single-turn or non-preserved-thinking competitors.

## What the pattern looks like

Quoted from the K3 README:

```python
messages = [
    {"role": "user", "content": "Tell me three random numbers."},
    {
        "role": "assistant",
        "reasoning_content": "I'll start by listing five numbers: 473, 921, 235, 215, 222, and I'll tell you the first three.",
        "content": "473, 921, 235"
    },
    {"role": "user", "content": "What are the other two numbers you have in mind?"}
]
```

The `reasoning_content` string on turn 1 becomes input tokens on turn 2. In a multi-turn agent, this compounds.

## Rough-order-of-magnitude thinking

If the average assistant turn has:
- ~500 tokens of `content`
- ~2,000 tokens of `reasoning_content` at `reasoning_effort=max`

Then a 10-turn session has a preserved-thinking overhead of roughly 10 × 2,000 = 20,000 input tokens across the session that a non-preserved-thinking model would not carry.

At `reasoning_effort=low`, that overhead shrinks materially — but so does K3's task performance on the harder benches. This is a knob, not a free choice.

## What the skill must recommend

- For **single-turn** workloads (one prompt, one response), preserved-thinking overhead is not a factor.
- For **multi-turn agentic** workloads, budget an extra 15–40% input tokens versus a non-preserved-thinking model — the exact number depends on `reasoning_effort` and average turn depth.
- For **long-session coding agents** (Kimi Code, 50+ turns), preserved-thinking is a first-order cost driver. Include it in any TCO comparison against Claude Fable 5 or GPT-5.6 Sol.

## Reasoning effort trade

Per the K3 README, `reasoning_effort` supports `"low"`, `"high"`, and `"max"` (default `"max"`). The benchmark table in `k3-benchmarks.md` is at `max`. Real-world deployments often ship at `high` or `low` for cost reasons. When recommending K3, name which `reasoning_effort` your recommendation assumes.

## Source

- [Kimi K3 Quickstart](https://platform.kimi.ai/docs/guide/kimi-k3-quickstart)
- [Thinking Effort guide](https://platform.kimi.ai/docs/guide/use-thinking-effort)
- [Kimi K3 tech report](https://github.com/MoonshotAI/Kimi-K3) — see the "Model Usage" section

Last reviewed: **2026-07-28**.
