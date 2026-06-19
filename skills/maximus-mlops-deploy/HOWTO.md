# HOWTO — maximus-mlops-deploy

Recipes for deploying and operating ML/LLM systems. Each recipe is a complete, runnable procedure.

---

## Recipe 1: How to register and version a model

**Goal**: Log a trained model (or LLM prompt version) with all artifacts needed for reproducibility and rollback.

**Steps**:
1. Choose your registry: MLflow (self-hosted or Databricks) for classical ML or hybrid systems; W&B Artifacts for teams already using W&B for training.
2. Define the versioning scheme: `{task}/{major}.{minor}.{patch}`. Increment patch for prompt tweaks, minor for architecture changes, major for task redefinition or model family switch.
3. Log the artifact:
   - **Classical ML (MLflow)**:
     ```python
     with mlflow.start_run():
         mlflow.log_params(config)
         mlflow.log_metrics(eval_results)
         mlflow.sklearn.log_model(model, "model")
         mlflow.log_artifact("data/dataset_v3.csv")
     ```
   - **LLM app (W&B)**:
     ```python
     artifact = wandb.Artifact("summarization-prompt", type="prompt")
     artifact.add_file("prompts/summarization_v2.1.0.txt")
     run.log_artifact(artifact)
     ```
4. Log the eval results alongside the artifact: accuracy, latency p50/p95, cost/call, safety eval pass rate. These are the baseline for the next version.
5. Tag the artifact with: git commit hash, dataset version, evaluation date.
6. Register the model to the production-candidate stage (not production yet — that's the canary's job).

**Verification**: The artifact is visible in the registry UI with all logged metadata. Retrieving the artifact by version tag produces the same weights/prompt and the recorded eval results.

**Common pitfalls**:
- Logging model weights without the dataset version. A model is not reproducible without its training data reference.
- Not logging eval results at registration time. "What was the baseline?" should never require a git archaeology session.
- Using `latest` as a version tag in production. `latest` is a moving target. Use explicit semver.

---

## Recipe 2: How to canary deploy a new model version

**Goal**: Route a small percentage of production traffic to a new model version and make a data-driven promote/rollback decision.

**Steps**:
1. Confirm the model is registered and eval results are logged (Recipe 1). Do not start a canary without a registered baseline to compare against.
2. Configure the traffic split: 90% production, 10% new version. Use your serving infrastructure:
   - **BentoML**: `bentoml serve` with a runner weight config.
   - **Modal**: Use a feature flag to route to a different `modal.Function` endpoint.
   - **Kubernetes**: Set `spec.strategy.canary.steps` in the Argo Rollout config.
3. Create a separate metrics namespace for the canary: `{service}_canary`. Log: output quality score, latency p50/p95, cost/call, error rate.
4. Define the promotion gate before the canary starts: all metrics must meet or exceed production baseline over a 24-hour window (or 1,000 requests minimum). Write this down — don't decide ad hoc.
5. Monitor the canary window. Do not intervene unless the automatic rollback trigger fires or there is a safety issue.
6. At the end of the window: compare canary metrics to production baseline. If all gates pass: promote (update the production pointer in the registry; update the traffic split to 100%). If any gate fails: roll back (Recipe 4 handles the automatic path; manually revert the traffic split if the automatic path didn't fire).
7. Announce the promotion: post the eval diff (new vs baseline) in the deployment log or Slack channel.

**Verification**: The canary metrics are logged in a separate namespace. The promotion decision is backed by metric comparison, not intuition. The registry shows the updated production pointer.

**Common pitfalls**:
- Starting a canary on a low-traffic service without adjusting the window. 10% of 50 req/day is 5 requests — not enough signal. Use shadow traffic instead (Recipe 5).
- Not defining the promotion gate before the canary starts. Post-hoc gate definition is a confirmation bias trap.
- Manually promoting without updating the registry. The registry must always reflect what's running in production.

---

## Recipe 3: How to set up online drift detection

**Goal**: Detect data drift, concept drift, and prompt drift automatically before they become user-facing quality regressions.

**Steps**:
1. Choose the detector type based on what you're monitoring:
   - **Input distribution drift** (data drift): compare embedding distributions of incoming requests to the training reference. Use `alibi-detect` (`MMDDrift`) or `evidently` (`DataDriftPreset`).
   - **Output distribution drift**: for classifiers: monitor class distribution over a rolling window. For LLMs: monitor output length, toxicity score, and refusal rate.
   - **Prompt drift**: hash the active system prompt on each serving startup; alert if the hash differs from the registered version.
2. Implement the detector. See `examples/drift-monitor.py` for a complete working example using `evidently` for data drift and a hash check for prompt drift.
3. Set the alert threshold conservatively: alert at 1.5σ drift (not 3σ). Earlier detection gives more time to investigate before users are impacted.
4. Wire the alert to your notification system (PagerDuty, Slack, or an alertmanager webhook). Drift alert should wake someone up at the same severity as a 5xx error spike.
5. Define the response runbook: on alert, (a) pull a sample of recent requests and outputs, (b) compare to training distribution baseline, (c) determine if drift is benign (seasonal pattern) or malignant (data pipeline issue, adversarial input shift), (d) escalate to rollback if malignant.
6. Store a reference snapshot of the input distribution at each model version promotion. The detector compares incoming data to the *model-version-specific* reference, not a global historical baseline.

**Verification**: A synthetic drift injection (adding OOD examples to a test stream) fires the alert within the expected detection lag. The alert fires to the correct channel. The reference snapshot is stored in the registry.

**Common pitfalls**:
- Setting the drift threshold at 3σ: by the time 3σ drift is detected, users have already noticed. Use 1.5σ.
- Comparing to a global baseline instead of the version-specific baseline. A new model version may have legitimately different input handling.
- Monitoring only data drift and missing prompt drift. For LLM apps, prompt drift is the most common and most invisible failure mode.

---

## Recipe 4: How to wire automatic rollback

**Goal**: Configure a pre-defined quality metric trigger that automatically reverts to the previous production model version without requiring human intervention.

**Steps**:
1. Define the rollback trigger *before* the canary starts. Format: "If {metric} < {threshold} for {window_minutes} consecutive minutes, roll back." Example: "If task_accuracy < 0.82 for 15 minutes, roll back."
2. Store the trigger definition in the deployment config (not in someone's head).
3. Implement the rollback trigger:
   - **BentoML/Kubernetes**: Use an Argo Rollout `analysis` step with a Prometheus query. If the analysis fails, Argo automatically rolls back.
   - **Modal**: Use a `modal.cron` health-check function that queries your metrics store and calls the Modal API to revert the deployment if the trigger fires.
   - **Custom**: An alertmanager webhook that calls your deployment API's rollback endpoint.
4. Test the rollback path in staging *before* the canary starts. Inject bad outputs and verify: (a) the metric drops, (b) the trigger fires within the window, (c) traffic reverts to the previous version, (d) the registry is updated to reflect the rollback.
5. Wire a notification: when the automatic rollback fires, alert the team (Slack, PagerDuty). Include: metric name, value at trigger, previous version restored, timestamp.
6. After a rollback: file a regression report. Document what caused the failure and what must be fixed before the next canary attempt.

**Verification**: A staged test rollback (injected quality regression in staging) fires the trigger, reverts traffic, and sends the notification. The whole flow completes in < rollback window + 2 minutes.

**Common pitfalls**:
- Defining the rollback trigger after the canary starts. If the model is already bad, you're already debugging rather than preventing.
- Not testing the rollback path. The canary window is not the time to discover the rollback mechanism is broken.
- Rollback without verifying the previous version is still registered. If someone cleaned up the registry, the rollback target may not exist.

---

## Recipe 5: How to run shadow traffic for a new prompt

**Goal**: Evaluate a new prompt version against 100% of production traffic without any user impact.

**Steps**:
1. Deploy the new prompt version as a shadow endpoint: a parallel inference path that receives all requests but whose responses are logged, not served to users.
2. Route all incoming requests to both the production and shadow endpoints simultaneously. In BentoML: use a fork in the runner pipeline. In Modal: call both functions from the request handler but return only the production result.
3. Log shadow outputs to a separate store (S3, BigQuery, or your eval database). Tag each record with: input hash, production output, shadow output, latency (both), timestamp.
4. Run offline comparison after N requests (typically 500–1,000): use your eval suite from `maximus-eval-and-test` to score both outputs. Metrics: task accuracy, output length, safety eval pass rate, user preference (if you have a judge model).
5. If the shadow version wins on all eval metrics: promote it via the standard canary deploy flow (Recipe 2). If it loses: analyze the failure cases, revise the prompt, and run shadow traffic again.
6. Stop the shadow endpoint after the comparison is complete. Shadow traffic doubles your inference cost for the duration — keep the window short.

**Verification**: Shadow logs contain paired (production, shadow) outputs for N requests. Eval scores are computed for both. A clear promote/iterate decision is documented.

**Common pitfalls**:
- Running shadow traffic indefinitely (cost doubles for the duration). Set a hard stop at N requests or T days.
- Evaluating shadow outputs manually without a structured eval. Manual review of 1,000 output pairs is not feasible. Use an automated eval or LLM-as-judge with a held-out sample.
- Treating shadow traffic as a substitute for canary. Shadow traffic tells you offline quality; canary tells you production behavior under real latency and load. Do both for major changes.
