# maximus-ai-product-spec

Spec an AI feature like a product, not a demo.

## What it is

This skill provides the discipline for writing a complete product specification for an AI-powered feature — from user-visible behavior through eval rubric, staged rollout, and kill switch. It fills the gap between "we have a cool prompt" and "we have a shippable, measurable, reversible product."

## Why it exists

Most AI feature work fails not because the model is bad but because nobody defined what "working" looks like. Specs written for AI features often describe the happy path only, skip refusal design, have no eval rubric, and plan a big-bang launch. This skill forces those decisions before a line of code is written.

The problem it solves: AI features that ship in permanent beta because nobody agreed on a success criterion.

## Quick start

1. **Create a spec document.** Copy `examples/spec-template.md` to your project. Fill in the feature name, user problem, and user-visible behavior sections.
2. **Define outputs and refusals.** Write 5–10 golden examples (input → expected output). List the input categories that must be refused and what the model says when refusing.
3. **Write the eval rubric.** Copy `examples/eval-rubric.md`. Define at minimum: task success rate target, safety pass rate target, latency P95 budget.
4. **Fill in the rollout table.** Define Stage 0 (off), Stage 1 (internal), Stage 2 (5%), and promotion criteria for each stage.
5. **Define the kill switch.** Name the feature flag, designate who can flip it without approval, and define the automated trigger condition.

## When NOT to use it

- For non-AI features (UI changes, API endpoints without a model call). Use `maximus-design-spec` instead.
- For infrastructure work that doesn't affect user-visible AI behavior.
- For quick experiments or one-off demos. Use this skill when the output is a spec meant to be reviewed and approved, not when hacking together a proof of concept.

## Related skills

- **maximus-design-spec** — the underlying spec discipline this skill builds on for AI-specific features.
- **maximus-prompt-engineering** — implementation of the behavior defined in this spec.
- **maximus-eval-and-test** — building the test suite that implements the eval rubric from this spec.
- **maximus-ai-safety-governance** — safety controls mapped to the refusal/failure modes defined here.
- **maximus-rag-pipeline** — additional retrieval quality spec for RAG-powered features.
- **maximus-agent-design** — tool-call scope and interruption behavior for agentic features.
- **maximus-fine-tuning** — model version pinning and retraining cadence for fine-tuned features.
- **maximus-devops-ship** — feature flag and rollout infrastructure.

## Glossary

**Eval rubric**: A set of quantitative criteria (with threshold values) used to decide whether a model's output is acceptable. The rubric is what makes "the AI is working" a testable claim rather than a feeling.

**Feature flag**: A runtime switch that enables or disables a feature without a code deployment. The kill switch is a feature flag with an agreed response plan.

**Golden examples**: A small set of (input, expected output) pairs that represent correct model behavior. Used to calibrate evaluators and to catch regressions.

**Graceful degradation**: The system behavior when the model is unavailable, slow, or returning low-confidence output. A fallback message, a cached result, or a simpler non-AI version of the feature.

**Kill switch**: The pre-planned capability to disable the AI feature immediately, on one person's authority, in response to an observed problem.

**Staged rollout**: The practice of enabling a feature for a small percentage of users first, measuring results, and expanding only when metric thresholds are met.

**Task success rate**: The proportion of model outputs that a human rater (or automated judge) classifies as correctly completing the user's intent.

**Thumbs-up/down ratio**: In-product user feedback signal. Informative but gameable; always pair with task success rate from blind evaluation.

**Refusal mode**: The defined behavior when the model receives an input it should not process (out-of-scope, harmful, PII, etc.). A spec without defined refusal modes is incomplete.
