# Example: Model Routing Config

A worked routing configuration for a multi-task AI product. Includes the YAML config and a Python dispatcher.

---

## Routing philosophy

Cheap by default, expensive when needed. The routing table defines:
1. A default model for each task class.
2. The quality floor (minimum eval score) that the default model must achieve.
3. Escalation conditions that trigger the frontier model.

This example is calibrated for a product with four task classes: classification, summarization, Q&A, and code generation. Prices are approximate as of 2025 and should be verified against current provider pricing.

---

## routing-config.yaml

```yaml
# Model routing configuration
# Update eval_min_score after each eval run against your task suite
# Verify current pricing at: https://anthropic.com/pricing and https://openai.com/pricing

version: "1.2.0"
updated: "2025-06"

models:
  cheap:
    anthropic: "claude-haiku-3-5"
    openai: "gpt-4o-mini"
  frontier:
    anthropic: "claude-sonnet-4-5"
    openai: "gpt-4o"

default_provider: "anthropic"

task_classes:
  classification:
    default_model: cheap
    eval_min_score: 0.90
    max_input_tokens: 2048
    max_output_tokens: 128
    escalation_conditions:
      - type: "explicit_user_request"
        trigger: "best_answer"
      - type: "input_length"
        threshold_tokens: 4000
    notes: "Binary and multi-class classification. Haiku handles this well."

  summarization:
    default_model: cheap
    eval_min_score: 0.82
    max_input_tokens: 16000
    max_output_tokens: 512
    escalation_conditions:
      - type: "explicit_user_request"
        trigger: "best_answer"
      - type: "document_type"
        values: ["legal", "medical", "financial"]
    notes: "General summarization. Escalate for high-stakes document types."

  question_answering:
    default_model: cheap
    eval_min_score: 0.78
    max_input_tokens: 8000
    max_output_tokens: 1024
    escalation_conditions:
      - type: "explicit_user_request"
        trigger: "best_answer"
      - type: "confidence_score"
        threshold: 0.65
        note: "Requires a confidence classifier upstream"
    notes: "General Q&A over retrieved context. Escalate on low confidence."

  code_generation:
    default_model: frontier
    eval_min_score: 0.88
    max_input_tokens: 16000
    max_output_tokens: 4096
    escalation_conditions: []
    notes: "Code quality delta between cheap and frontier models is too large. Frontier by default."

cost_guard:
  max_output_tokens_global: 8192
  per_user_daily_input_tokens: 100000
  per_user_daily_output_tokens: 20000
  alert_on_routing_anomaly: true
  anomaly_threshold_pct: 25  # alert if frontier model usage increases >25% in 1 hour
```

---

## Python dispatcher

```python
"""
model_router.py — Reads routing-config.yaml and dispatches to the correct model.
"""
import yaml
import anthropic
from pathlib import Path


class ModelRouter:
    def __init__(self, config_path: str = "routing-config.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.client = anthropic.Anthropic()

    def _get_model(self, task_class: str, context: dict) -> str:
        """Determine which model to use for this request."""
        task_config = self.config["task_classes"].get(task_class)
        if not task_config:
            raise ValueError(f"Unknown task class: {task_class}")

        model_tier = task_config["default_model"]

        # Check escalation conditions
        for condition in task_config.get("escalation_conditions", []):
            if condition["type"] == "explicit_user_request":
                if context.get("user_preference") == condition["trigger"]:
                    model_tier = "frontier"
                    break
            elif condition["type"] == "input_length":
                if context.get("input_tokens", 0) > condition["threshold_tokens"]:
                    model_tier = "frontier"
                    break
            elif condition["type"] == "confidence_score":
                if context.get("confidence", 1.0) < condition["threshold"]:
                    model_tier = "frontier"
                    break
            elif condition["type"] == "document_type":
                if context.get("document_type") in condition["values"]:
                    model_tier = "frontier"
                    break

        provider = self.config["default_provider"]
        return self.config["models"][model_tier][provider]

    def complete(
        self,
        task_class: str,
        messages: list[dict],
        context: dict | None = None,
        system: str = "",
    ) -> anthropic.types.Message:
        """Route and complete a request."""
        context = context or {}
        model = self._get_model(task_class, context)

        task_config = self.config["task_classes"][task_class]
        max_tokens = min(
            task_config["max_output_tokens"],
            self.config["cost_guard"]["max_output_tokens_global"],
        )

        # Log routing decision for audit
        print(f"[router] task={task_class} model={model} context_keys={list(context.keys())}")

        return self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )


# Usage
if __name__ == "__main__":
    router = ModelRouter()

    # Standard request → routes to cheap model
    response = router.complete(
        task_class="summarization",
        messages=[{"role": "user", "content": "Summarize: ..."}],
    )
    print(response.model)  # claude-haiku-3-5

    # Legal document → escalates to frontier
    response = router.complete(
        task_class="summarization",
        messages=[{"role": "user", "content": "Summarize: ..."}],
        context={"document_type": "legal"},
    )
    print(response.model)  # claude-sonnet-4-5
```

---

## Testing the router

```python
# test_router.py
import pytest
from model_router import ModelRouter


def test_routes_summarization_to_cheap():
    router = ModelRouter()
    model = router._get_model("summarization", {})
    assert "haiku" in model.lower()


def test_escalates_legal_summarization():
    router = ModelRouter()
    model = router._get_model("summarization", {"document_type": "legal"})
    assert "sonnet" in model.lower()


def test_code_generation_always_frontier():
    router = ModelRouter()
    model = router._get_model("code_generation", {})
    assert "sonnet" in model.lower()


def test_explicit_best_answer_escalates():
    router = ModelRouter()
    model = router._get_model("classification", {"user_preference": "best_answer"})
    assert "sonnet" in model.lower()
```

---

## Notes

- Update `version` and `updated` fields whenever you change the routing table. The routing config is a versioned artifact — treat it like code.
- Run the eval suite (`maximus-eval-and-test`) after any routing change. A routing bug is silent at the API level but visible in output quality.
- The `anomaly_threshold_pct` guard in `cost_guard` should be wired to a monitoring alert. A sudden spike in frontier model usage is a routing bug until proven otherwise.
