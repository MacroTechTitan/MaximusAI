# maximus-mlops-deploy

Deploy and operate ML/LLM systems in production. The model-specific deployment layer: versioning, canary deploys with eval comparison, drift detection, and automatic rollback.

## What this skill is

Getting a model to production is not `git push`. Models degrade silently. Prompt changes are invisible unless versioned. Drift accumulates until it's a user complaint. This skill is the operational discipline for ML systems: version everything, eval before promote, monitor always, roll back automatically.

It is a sibling to `maximus-devops-ship` (which handles general application deployment) and adds the ML-specific layer on top: model registry, canary eval comparison, shadow traffic, and drift detection.

## Why it exists / what problem it solves

ML systems fail in ways that standard DevOps doesn't catch:

- **Silent quality regression** — the service is up, latency is fine, but the outputs are worse. No error rate alert fires.
- **Prompt drift** — the system prompt was edited directly in the database two sprints ago. No one tracked the change. Now a rollback is impossible.
- **Undetected distribution shift** — the input data distribution changed three weeks ago. The model is extrapolating. Nobody noticed until a customer escalation.
- **Rollback without a plan** — the new model is bad, but the old weights weren't saved properly and the eval results weren't logged.

This skill prevents all four.

## Quick start

1. **Register the artifact.** Log model weights (or API model pointer), dataset version, training config, and eval results to MLflow or W&B. Tag with semver: `{task}/{major}.{minor}.{patch}`.
2. **Run the eval suite.** Compare to the production baseline using `maximus-eval-and-test`. All metrics must meet or exceed baseline.
3. **Stage the canary.** 10% of traffic to the new version. Separate metrics namespace.
4. **Monitor the canary window.** 24 hours or 1,000 requests, watching quality, latency, cost, and error rate.
5. **Promote or roll back.** Pass all gates → update production pointer. Fail any gate → automatic rollback fires.

## When NOT to use it

- **General application deployment** (containers, CI/CD, infra scaling): use `maximus-devops-ship`.
- **First-time model training setup**: this skill assumes you already have a trained model or an LLM API integration. Use `maximus-fine-tuning` for the training workflow.
- **Offline batch inference with no quality SLA**: the canary and rollback discipline is for production-serving paths. Batch jobs with manual review can use a lighter process.

## Related skills

- `maximus-devops-ship` — General application deployment, CI/CD, container orchestration.
- `maximus-eval-and-test` — Designing the eval suite that gates promotion.
- `maximus-fine-tuning` — Training workflow that produces versioned artifacts for the registry.
- `maximus-prompt-engineering` — Prompt versioning strategy.
- `maximus-ai-cost-control` — Cost impact analysis for model version changes.

## Glossary

**Model registry** — A versioned store of model artifacts, configs, datasets, and eval results. MLflow Model Registry and W&B Artifact Registry are common implementations.

**Canary deploy** — Routing a small percentage (5–10%) of live traffic to a new model version while the majority continues to use the current production version. Allows quality comparison with real users at limited blast radius.

**Shadow traffic** — Routing 100% of requests to both versions, but serving only the production version to users. The new version's outputs are logged and compared offline.

**Eval gate** — A minimum quality threshold (e.g., task accuracy ≥ 0.82, safety eval pass rate = 100%) that a new model version must pass before it can be promoted to production.

**Data drift** — A shift in the statistical distribution of inputs to the model relative to the training distribution. Detected via embedding distance or feature statistics.

**Concept drift** — A shift in the relationship between inputs and correct outputs (i.e., the world changed, not just the data). Harder to detect automatically; requires periodic ground-truth collection.

**Prompt drift** — For LLM apps: an untracked change to the system prompt or few-shot examples. Equivalent to a weight update; must be versioned.

**Automatic rollback** — A pre-configured trigger that reverts the production model pointer to the previous version when a quality metric falls below threshold for a defined window.
