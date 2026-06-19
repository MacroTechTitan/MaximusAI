---
name: maximus-ai-safety-governance
description: "Responsible AI controls for production systems. Use when building or auditing AI features that must detect and redact PII, defend against prompt injection, filter output content, produce immutable audit logs, write model cards, evaluate for bias and toxicity, or comply with EU AI Act risk tiers or NIST AI RMF. Trigger phrases: 'prompt injection defense', 'PII redaction', 'AI audit log', 'model card', 'EU AI Act compliance', 'NIST AI RMF', 'responsible AI controls', 'content filtering', 'bias evaluation', 'AI governance'."
metadata:
  pillar: ai-engineering
  source: maximus
---

# Maximus — AI Safety & Governance

Safety is not a checklist you add after shipping. It's the load-bearing wall of the feature. This skill covers the practical controls — PII handling, injection defense, output filtering, audit logging, bias evaluation, and regulatory mapping — that keep AI features in production and out of the news.

## When to use

- Building any user-facing AI feature that processes user input or produces user-visible output.
- Auditing an existing AI feature for compliance with EU AI Act or NIST AI RMF.
- Writing a model card for an internally trained or externally sourced model.
- Investigating a safety incident (unexpected output, PII leak, prompt injection success).

## Core rules

1. **Defense in depth.** No single control is sufficient. Layer PII detection, input sanitization, output filtering, and logging. One layer failing should not cause a breach.
2. **Audit logs are immutable.** Log every model call: inputs (after PII scrub), outputs, model version, latency, user ID hash. Write-only store. No delete path.
3. **Refusal is not censorship.** Define refusal categories in the spec (`maximus-ai-product-spec`) before implementing them here. A refusal without a defined category is an untestable control.
4. **Regulatory tier first.** Determine the EU AI Act and NIST AI RMF tier before building. High-risk features have different control requirements than minimal-risk ones.
5. **Model cards ship with models.** A deployed model without a model card is an unverified asset.

## Procedure

1. **Classify the feature under EU AI Act risk tiers.**
   - Prohibited (Article 5): biometric manipulation, social scoring, subliminal manipulation — do not build.
   - High-risk (Annex III): employment, credit, education, law enforcement, critical infrastructure — mandatory conformity assessment.
   - Limited risk (Article 50): chatbots, deepfakes — transparency obligations only.
   - Minimal risk: everything else — voluntary codes of practice.
   - Use `references/eu-ai-act-risk-tiers.md` for the full mapping. Document the tier in the feature spec.

2. **Map to NIST AI RMF functions.**
   - GOVERN: establish accountability, policies, roles, and documentation.
   - MAP: identify risks and affected stakeholders.
   - MEASURE: implement metrics, evals, red-teaming.
   - MANAGE: apply mitigations, monitor in production, escalate incidents.
   - Assign an owner to each function per feature.

3. **Implement PII detection and redaction.**
   - Scan all user inputs before they reach the model. Use a presidio or equivalent pipeline.
   - Scrub before logging; never log raw PII.
   - Define what to do when PII is found: redact and continue, or refuse and explain.
   - Keep a list of PII categories in scope (names, emails, SSN, credit card, health identifiers).
   - See `examples/pii-redaction.py` for a working implementation.

4. **Defend against prompt injection.**
   - Apply instruction hierarchy: system prompt > retrieved context > user input. Never allow user input to override system instructions.
   - Use delimiters (`<user_input>...</user_input>`) to clearly bound user-controlled text.
   - Validate and sanitize output: if the output is used downstream (e.g., parsed as JSON, used to call a tool), apply strict schema validation.
   - For agentic features, scope tool access to the minimum required; validate tool call parameters before execution.
   - See `examples/prompt-injection-defense.md` for concrete patterns.

5. **Implement output content filtering.**
   - Apply a classifier (OpenAI moderation API, Perspective API, or a fine-tuned classifier) to model outputs before they reach the user.
   - Categories to filter: harmful content, hate speech, sexual content, self-harm, PII in outputs.
   - Define thresholds per category and the action when a threshold is crossed (block, warn, escalate).
   - Log filtered outputs with the classifier score for model card and audit purposes.

6. **Implement immutable audit logging.**
   - Log: timestamp (UTC), user ID (hashed or pseudonymized), session ID, model name + version, input token count, output token count, latency ms, safety filter result, any applied redactions.
   - Use an append-only store (S3 with Object Lock, a write-only database table, or a SIEM).
   - Retention period: consult legal. EU AI Act Article 12 requires high-risk systems to retain logs for a minimum defined period.

7. **Write a model card.**
   - Sections: Model details, Intended uses, Out-of-scope uses, Training data summary, Evaluation results (overall + by subgroup), Quantitative analysis (bias metrics), Ethical considerations, Caveats and recommendations.
   - Base format on [Hugging Face model card schema](https://huggingface.co/docs/hub/model-cards) or the Mitchell et al. (2019) original.
   - Refresh the card when the model is retrained or fine-tuned.

8. **Evaluate for bias and toxicity.**
   - Use a structured evaluation set that includes demographic parity slices (by inferred gender, ethnicity, age group — in the prompts, not from user profiles).
   - Measure: toxic output rate, disparate refusal rate across demographic proxies, task success rate by slice.
   - Tools: `evaluate` library (Hugging Face), Perspective API, ToxiGen, WinoBias, BBQ.
   - Document results in the model card. Publish known limitations.

9. **Cross-reference the product spec.** Every safety control maps to a refusal or failure mode defined in `maximus-ai-product-spec`. If the product spec has no safety section, add one before implementing controls.

## Domain notes

- **EU AI Act (Regulation (EU) 2024/1689)** entered into force 1 August 2024. Prohibited practices (Article 5) apply from 2 February 2025; high-risk obligations (Annex III) from 2 August 2026. Prepare now.
- **NIST AI RMF 1.0** (January 2023) is the US voluntary framework. Its four functions (Govern, Map, Measure, Manage) are the canonical US enterprise governance structure.
- **Presidio** (Microsoft, Apache 2.0) is the practical open-source choice for PII detection. It supports custom recognizers, supports 20+ entity types, and integrates with Hugging Face NER models.
- **OpenAI Moderation API** is free and sufficient for most output filtering. For custom categories or higher accuracy, fine-tune your own classifier.
- **Prompt injection** in agentic systems is a first-class threat (OWASP LLM Top 10, item LLM01). Do not treat it as a model problem — it's an architecture problem.

## Gotchas

- PII in model outputs (the model regurgitating training data) is different from PII in inputs. Both need controls, but different ones.
- "Our system prompt tells the model not to do X" is not a safety control. It's a hint. Implement real controls on top.
- GDPR deletion requests apply to data used to train or fine-tune models. Coordinate with `maximus-ai-data-pipeline` for deletion workflows.
- High-risk AI systems under the EU AI Act require a conformity assessment *before* market deployment. That's not a legal team problem — engineering needs to build the evidence trail.
- Audit logs that contain PII are themselves a GDPR liability. Scrub before logging, always.

## Output

Model card document, audit log schema, PII redaction pipeline (see examples), prompt-injection defense patterns (see examples), EU AI Act tier classification, NIST AI RMF function assignments, bias evaluation report (numbers + methodology).
