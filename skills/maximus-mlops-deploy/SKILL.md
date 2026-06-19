---
name: maximus-mlops-deploy
description: "Deploy and operate ML/LLM systems in production. Use when registering a model, running a canary deploy with eval comparison, setting up drift detection (data drift, concept drift, prompt drift), wiring automatic rollback on quality regression, or running shadow traffic against a new prompt version. Sibling to maximus-devops-ship; focused specifically on model lifecycle, not general application deployment."
metadata:
  pillar: ai-engineering
  source: maximus
---

# Maximus — MLOps Deploy

Shipping a model is not shipping a binary. A binary either works or it crashes. A model degrades — silently, gradually, in ways that only show up in output quality and downstream metrics. The discipline is: version everything, eval before promoting, detect drift early, roll back automatically.

## When to use

- Registering a new model or prompt version in a registry.
- Promoting a model from staging to production with a canary deploy.
- Setting up monitoring for a model already in production.
- Responding to a quality regression alert.
- Running shadow traffic to evaluate a new prompt without user impact.

For general application deployment (containers, CI/CD, infra), use `maximus-devops-ship`. This skill is the model-specific layer on top.

## Core rules

1. **Version everything: model, dataset, prompt, config.** A model version without the dataset it was trained on and the prompt it was evaluated against is not a version — it's a mystery.
2. **Eval before promote.** No model moves to production without passing the eval gate defined in `maximus-eval-and-test`. Canary without evals is guesswork with traffic.
3. **Canary first, full rollout second.** Route 5–10% of production traffic to the new version. Watch quality metrics and error rates for 24 hours (or N requests, whichever comes first). Then promote or roll back.
4. **Drift detection is always on.** Data drift, concept drift, and prompt drift (for LLM apps) each need a detector running in production. Not post-incident. Always.
5. **Automatic rollback is the safety net.** Define the rollback trigger (quality metric below threshold for M minutes). Wire it before the canary starts. The rollback should not require a human to be awake.

## Procedure

1. **Register the artifact.** Log model weights (or API model pointer), dataset version, training config, and eval results to the model registry. Use MLflow or Weights & Biases. Tag with semver: `{task}/{major}.{minor}.{patch}` — e.g., `summarization/2.1.0`. For LLM apps: version the prompt template alongside the model pointer.
2. **Run the eval suite.** Execute the benchmark suite from `maximus-eval-and-test`. Compare to the production baseline. Record: task accuracy, latency p50/p95, cost/call, safety eval pass rate. All must meet or exceed baseline before proceeding.
3. **Stage the canary.** Configure traffic split: 90% production, 10% new version. Use feature flags or your serving infrastructure's traffic shaping (BentoML, Modal routing, Replicate, or Anyscale). Log new version traffic to a separate metrics namespace.
4. **Monitor the canary window.** Watch: output quality (online eval or human sample), error rate, latency, cost/call. Canary window: 24 hours minimum, or 1,000 requests, whichever is longer for low-traffic services.
5. **Promote or roll back.** If all metrics pass: update the production pointer in the registry. Announce the promotion with the eval diff in the deployment log. If any metric fails: roll back automatically (see step 7) and file a regression report.
6. **Run shadow traffic for riskier changes.** For major prompt rewrites or architecture changes: route 100% of production requests to both versions, but serve only the production version to users. Compare outputs offline. No user impact; full signal.
7. **Wire automatic rollback.** Define: metric, threshold, window (e.g., "if task_accuracy < 0.82 for 15 min, roll back"). Implement with your orchestrator's health check (BentoML runner health, Modal app rollback, custom alertmanager webhook). Test the rollback path in staging before the canary starts.
8. **Set up ongoing drift detection.** See `examples/drift-monitor.py` for a working implementation. Monitor: input distribution shift (embedding drift), output distribution shift (label/class drift for classifiers, length/toxicity drift for LLMs), and system prompt integrity (has the prompt been modified in the database?).

## Tool notes

- **MLflow**: Model registry, experiment tracking, artifact logging. Self-hosted or Databricks managed. Best for classical ML and hybrid ML/LLM systems.
- **Weights & Biases**: Experiment tracking, artifact versioning, sweeps. Strong LLM eval integrations. Best when the team already uses W&B for training runs.
- **BentoML**: Model serving, multi-model pipelines, containerized deployment. Good for custom inference with hardware requirements.
- **Modal**: Serverless GPU inference, fast cold starts, built-in secrets management. Best for LLM inference that needs to scale to zero.
- **Replicate**: Hosted model deployment with versioned API endpoints. Minimal infra; best for prototypes or low-traffic features.
- **Anyscale**: Ray-based distributed inference and fine-tuning. Best for large-scale inference or distributed training.

## Cross-references

- Eval suite design: `maximus-eval-and-test`
- Prompt versioning strategy: `maximus-prompt-engineering`
- Fine-tuning workflow that feeds the registry: `maximus-fine-tuning`
- General infra deployment: `maximus-devops-ship`
- Cost impact of model changes: `maximus-ai-cost-control`

## Gotchas

- **Versioning the API pointer but not the prompt** — for LLM apps, the prompt *is* a model parameter. A prompt change without a version bump makes debugging impossible.
- **Canary with insufficient traffic** — a 5% canary on a 100-req/day service gives you 5 requests per day of signal. Either extend the window or use shadow traffic instead.
- **Eval set leakage** — if production data is used to improve the model and also used in the eval, the eval is optimistic. Maintain a held-out test set.
- **Drift detection lag** — statistical drift detectors have a detection lag. Set alert thresholds conservatively (e.g., alert at 1.5σ drift, not 3σ) to catch degradation before it reaches users.
- **Rollback without data versioning** — rolling back the model but not the data pipeline that feeds it leaves the system in an inconsistent state.
- **Skipping shadow traffic for prompt rewrites** — a rewritten system prompt is a different model. Treat it with the same rigor as a weight update.

## Output

A deployment record in the model registry: artifact version, eval results vs baseline, canary window results, promotion timestamp, drift detector config. Plus a runbook entry for the rollback trigger and the drift alert.
