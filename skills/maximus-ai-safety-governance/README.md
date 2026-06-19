# maximus-ai-safety-governance

Responsible AI controls for production systems. Practical, not academic.

## What it is

This skill covers the safety and governance layer that every production AI feature requires: PII detection and redaction, prompt-injection defense, output content filtering, immutable audit logging, model cards, bias/toxicity evaluation, and regulatory classification (EU AI Act, NIST AI RMF). It is the implementation guide for the safety controls that `maximus-ai-product-spec` specifies.

## Why it exists

Regulatory exposure from AI systems is now concrete. The EU AI Act is in force. GDPR right-to-erasure applies to training data. Prompt injection in agentic systems is a first-class attack vector. This skill exists so that safety controls are built in from the start, not bolted on after an incident.

The problem it solves: AI features that go to production without defined controls, audit trails, or regulatory classification — and then generate legal exposure, user harm, or reputational damage.

## Quick start

1. **Classify the feature.** Read `references/eu-ai-act-risk-tiers.md`. Determine the risk tier (prohibited / high-risk / limited / minimal) and document it in the feature spec.
2. **Implement PII detection.** Install Microsoft Presidio (`pip install presidio-analyzer presidio-anonymizer`). Run `examples/pii-redaction.py` against your input pipeline. Verify that raw PII never reaches the model or the audit log.
3. **Implement prompt-injection defenses.** Apply the patterns in `examples/prompt-injection-defense.md`: delimiters around user input, instruction hierarchy enforcement, output schema validation.
4. **Set up audit logging.** Create a write-only log table (or append-only S3 bucket with Object Lock). Log: timestamp, hashed user ID, model name + version, token counts, latency, safety filter result.
5. **Write a model card.** Use the Hugging Face model card format. Fill in intended uses, out-of-scope uses, training data summary, evaluation results, and known limitations. Commit it alongside the model.

## When NOT to use it

- For features that contain no AI/ML model calls. Standard security and privacy controls apply.
- For red-teaming or adversarial testing design (though this skill informs what to test). Use `maximus-eval-and-test` for test design.
- As a substitute for legal counsel on high-risk AI Act classification. This skill helps you understand the framework; consult legal for binding compliance decisions.

## Related skills

- **maximus-ai-product-spec** — defines the refusal/failure modes that safety controls implement.
- **maximus-ai-data-pipeline** — data-side safety controls (PII in training data, deletion compliance).
- **maximus-prompt-engineering** — instruction hierarchy and delimiter patterns at the prompt level.
- **maximus-eval-and-test** — building the evaluation suite that measures safety metrics.
- **maximus-agent-design** — tool-call scoping and injection defense for agentic systems.

## Glossary

**Audit log**: An immutable, append-only record of every model call. Contains: timestamp, user identifier (pseudonymized), model version, input token count, output token count, latency, and safety filter outcome. Never contains raw PII.

**EU AI Act (Regulation (EU) 2024/1689)**: EU regulation classifying AI systems by risk and imposing conformity requirements. Prohibited practices apply from February 2025; high-risk system obligations from August 2026.

**Model card**: A document published alongside a deployed model describing its intended use, training data, evaluation results, known biases, and limitations. Based on Mitchell et al. (2019).

**NIST AI RMF**: National Institute of Standards and Technology AI Risk Management Framework (January 2023). Four functions: Govern, Map, Measure, Manage. The US voluntary governance framework.

**PII (Personally Identifiable Information)**: Any data that can identify a natural person directly (name, email, SSN) or indirectly (combination of age + ZIP + gender). Regulated under GDPR in the EU and CCPA in California.

**Presidio**: Microsoft's open-source PII detection and anonymization library. Supports 20+ entity types, custom recognizers, and integration with Hugging Face NER models.

**Prompt injection**: An attack where malicious content in user input or retrieved context overrides the system's instructions to the model. Equivalent to SQL injection for LLM systems.

**Content filtering**: A post-model classifier that screens outputs for harmful, unsafe, or policy-violating content before they reach the user.

**Instruction hierarchy**: The precedence order of instructions to a model: system prompt > tool/context injection > user input. User input must not be able to override system-level instructions.

**Conformity assessment**: The EU AI Act process by which high-risk AI systems are evaluated for compliance before market deployment. May be self-assessed or require third-party audit depending on the system type.
