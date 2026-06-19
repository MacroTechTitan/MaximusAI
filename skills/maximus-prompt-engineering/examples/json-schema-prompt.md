# Example: JSON Schema Enforcement — OpenAI and Anthropic

Demonstrates enforcing structured JSON output using the provider's native schema enforcement, not just prose instructions.

---

## OpenAI (Python) — Strict JSON Schema

```python
# json_schema_openai.py
# Requires: openai>=1.30.0
# Tests against: gpt-4o-2024-11-20

from openai import OpenAI
import json

client = OpenAI()  # uses OPENAI_API_KEY from env

SCHEMA = {
    "type": "object",
    "properties": {
        "intent": {
            "type": "string",
            "enum": ["billing", "account_access", "product_usage", "feature_request", "complaint", "other"]
        },
        "urgency": {
            "type": "string",
            "enum": ["low", "medium", "high", "critical"]
        },
        "sentiment": {
            "type": "string",
            "enum": ["positive", "neutral", "negative"]
        },
        "summary": {
            "type": "string",
            "description": "One sentence summary of the user's request, max 100 chars.",
            "maxLength": 100
        },
        "suggested_action": {
            "type": "string",
            "description": "Recommended next step for the support agent."
        }
    },
    "required": ["intent", "urgency", "sentiment", "summary", "suggested_action"],
    "additionalProperties": False
}

SYSTEM_PROMPT = """You are a customer support triage assistant.
Classify the user's message and return a JSON object matching the provided schema.
Be precise about urgency: use 'critical' only if the user cannot use the product at all."""

def triage(user_message: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-2024-11-20",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "support_triage",
                "schema": SCHEMA,
                "strict": True
            }
        }
    )
    return json.loads(response.choices[0].message.content)


# --- Test ---
if __name__ == "__main__":
    cases = [
        "I was charged $99 twice this month and I want a refund immediately.",
        "Can you help me reset my 2FA? I got locked out of my account.",
        "The app is completely down for our entire team. Nobody can log in.",
        "Just wanted to say the new dashboard is amazing, great work!",
    ]
    for msg in cases:
        result = triage(msg)
        print(f"Input: {msg[:60]}...")
        print(f"Output: {json.dumps(result, indent=2)}\n")
```

---

## Anthropic (Python) — Tool-based JSON Enforcement

Anthropic enforces schemas via tool definitions. The model "calls" a tool with the structured output, which enforces the schema.

```python
# json_schema_anthropic.py
# Requires: anthropic>=0.28.0

import anthropic
import json

client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY from env

TRIAGE_TOOL = {
    "name": "record_triage",
    "description": "Record the triage classification for a support message. Always call this tool.",
    "input_schema": {
        "type": "object",
        "properties": {
            "intent": {
                "type": "string",
                "enum": ["billing", "account_access", "product_usage", "feature_request", "complaint", "other"]
            },
            "urgency": {
                "type": "string",
                "enum": ["low", "medium", "high", "critical"]
            },
            "sentiment": {
                "type": "string",
                "enum": ["positive", "neutral", "negative"]
            },
            "summary": {
                "type": "string",
                "description": "One sentence summary, max 100 chars."
            },
            "suggested_action": {
                "type": "string"
            }
        },
        "required": ["intent", "urgency", "sentiment", "summary", "suggested_action"]
    }
}

SYSTEM_PROMPT = """You are a customer support triage assistant.
Classify the user's message by calling the record_triage tool.
Use 'critical' urgency only when the user is completely blocked from using the product."""

def triage(user_message: str) -> dict:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=512,
        temperature=0,
        system=SYSTEM_PROMPT,
        tools=[TRIAGE_TOOL],
        tool_choice={"type": "tool", "name": "record_triage"},  # force tool call
        messages=[{"role": "user", "content": user_message}]
    )
    # Extract the tool call input
    for block in response.content:
        if block.type == "tool_use" and block.name == "record_triage":
            return block.input
    raise ValueError("Model did not call record_triage tool")


# --- Test ---
if __name__ == "__main__":
    cases = [
        "I was charged $99 twice this month and I want a refund immediately.",
        "The app is completely down for our entire team.",
    ]
    for msg in cases:
        result = triage(msg)
        print(f"Input: {msg[:60]}...")
        print(f"Output: {json.dumps(result, indent=2)}\n")
```

---

## Notes

- Both approaches achieve schema enforcement at the API level, not just by asking nicely in prose.
- OpenAI's `strict: True` with `json_schema` mode is the most reliable for complex nested schemas.
- Anthropic's `tool_choice: {"type": "tool", "name": "..."}` forces the model to call a specific tool, guaranteeing schema compliance.
- Always set `temperature=0` for classification tasks.
- Validate the result with `jsonschema.validate(result, SCHEMA)` in production — a belt-and-suspenders check.
