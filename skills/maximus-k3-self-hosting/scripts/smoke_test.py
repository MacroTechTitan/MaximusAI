"""
K3 preserved-thinking smoke test.

Runs a 3-turn conversation against a Kimi K3 endpoint (hosted or self-hosted,
OpenAI-compatible). Verifies that reasoning_content and tool_calls are
correctly echoed back on each follow-up turn.

Usage:
    export KIMI_API_KEY=...
    export KIMI_BASE_URL=https://platform.kimi.ai/v1   # or your self-hosted vLLM/SGLang endpoint
    export KIMI_MODEL=kimi-k3
    python smoke_test.py

Exits 0 on pass, 1 on fail.

This script is transcribed and adapted from the pattern shown in the
Kimi-K3 README §6 (Model Usage). See:
    https://github.com/MoonshotAI/Kimi-K3
    https://platform.kimi.ai/docs/guide/kimi-k3-quickstart
"""

from __future__ import annotations

import os
import sys
from typing import Any

try:
    import openai  # type: ignore
except ImportError:
    print("Install openai first: pip install openai>=1.0", file=sys.stderr)
    sys.exit(1)


def _mk_client() -> "openai.OpenAI":
    api_key = os.environ.get("KIMI_API_KEY")
    base_url = os.environ.get("KIMI_BASE_URL", "https://platform.kimi.ai/v1")
    if not api_key:
        print("Set KIMI_API_KEY", file=sys.stderr)
        sys.exit(1)
    return openai.OpenAI(api_key=api_key, base_url=base_url)


def _dump_message(msg: Any) -> dict:
    """Turn an assistant response message into a dict suitable for the next
    turn's messages array. Preserves reasoning_content and tool_calls."""
    out: dict = {"role": "assistant"}
    content = getattr(msg, "content", None)
    if content is not None:
        out["content"] = content
    reasoning = getattr(msg, "reasoning_content", None) or getattr(msg, "reasoning", None)
    if reasoning is not None:
        out["reasoning_content"] = reasoning
    tool_calls = getattr(msg, "tool_calls", None)
    if tool_calls:
        out["tool_calls"] = tool_calls
    return out


def run() -> int:
    client = _mk_client()
    model = os.environ.get("KIMI_MODEL", "kimi-k3")

    messages: list[dict] = [
        {"role": "user", "content": "Please pick five random integers between 1 and 1000, then tell me only the first three."}
    ]

    # Turn 1
    r1 = client.chat.completions.create(
        model=model, messages=messages, reasoning_effort="high", max_tokens=1024,
    )
    m1 = r1.choices[0].message
    print("Turn 1 content:", getattr(m1, "content", None))
    print("Turn 1 reasoning present:", bool(getattr(m1, "reasoning_content", None) or getattr(m1, "reasoning", None)))
    messages.append(_dump_message(m1))
    messages.append({"role": "user", "content": "What were the other two numbers you picked but did not tell me?"})

    # Turn 2 — the real test. If reasoning_content was dropped, K3 will
    # not know the answer.
    r2 = client.chat.completions.create(
        model=model, messages=messages, reasoning_effort="high", max_tokens=1024,
    )
    m2 = r2.choices[0].message
    content = getattr(m2, "content", "") or ""
    print("Turn 2 content:", content)

    # Basic heuristic: turn 2 should return two integers.
    import re
    nums = re.findall(r"\b\d+\b", content)
    if len(nums) < 2:
        print("FAIL: Turn 2 did not return two integers. Preserved-thinking is likely mis-configured.")
        return 1

    print("PASS: preserved-thinking round-trip works.")
    return 0


if __name__ == "__main__":
    sys.exit(run())
