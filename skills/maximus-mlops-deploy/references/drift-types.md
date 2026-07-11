# Reference: Drift Types in ML/LLM Systems

A structured taxonomy of drift types, detection methods, and response playbooks for production ML systems.

---

## Why drift matters

A model is a snapshot of a relationship between inputs and outputs, learned from data at a point in time. The world keeps changing after training. Drift is the gap between the model's learned world and the current world. Unlike bugs, drift is gradual and silent — no error rate spikes, no alerts, just quietly degrading quality until a user complains.

---

## Type 1: Data Drift (Input Distribution Drift)

**Definition**: The statistical distribution of inputs to the model shifts away from the training distribution.

**Example**: A customer service classification model trained on 2023 product support tickets starts receiving queries about a new product category launched in 2024. The new query distribution is outside the training distribution.

**Why it matters**: The model is being asked to generalize to inputs it has never seen. Performance degrades in unpredictable ways — not uniformly, but specifically on the new input patterns.

**Detection methods**:
- **Embedding distance**: Encode recent inputs with the same encoder used at training. Compare the centroid (or full distribution) of recent embeddings to the reference centroid. Alert at cosine distance > 1.5σ from baseline.
- **Feature statistics**: For tabular inputs: track mean, variance, and quantiles of each feature. Alert when KL divergence or Population Stability Index (PSI > 0.2) exceeds threshold.
- **Evidently DataDriftPreset**: Automated statistical tests per feature column, with a drift report.

**Response**:
1. Sample recent drifted inputs and review manually.
2. Determine if drift is benign (seasonal pattern, new user cohort) or malignant (data pipeline bug, adversarial input).
3. If benign: log and monitor. Consider adding drifted examples to the training set for the next version.
4. If malignant: fix the data pipeline. Consider rollback if quality is severely degraded.

---

## Type 2: Concept Drift (Label/Relationship Drift)

**Definition**: The relationship between inputs and correct outputs changes — not just the inputs, but what the right answer is for a given input.

**Example**: A sentiment classifier trained on pre-pandemic restaurant reviews encounters reviews written during/after the pandemic where the same language patterns ("clean", "spaced out", "good ventilation") now carry different sentiment signals.

**Why it matters**: The model's learned mapping from input → output is wrong, even for inputs it has seen before. This is the hardest drift to detect because it requires ground truth — you must know what the correct output should be, which requires human annotation or a downstream proxy metric.

**Detection methods**:
- **Ground truth collection**: Periodic sampling of model outputs for human annotation. Compare labels to model predictions.
- **Downstream proxy metrics**: If model output drives a downstream action (click, purchase, resolution), track the action rate over time. A significant drop may indicate concept drift.
- **A/B test performance**: When deploying a new model version, if the new version (trained on more recent data) substantially outperforms the old version on recent examples but not historical examples, concept drift is likely.

**Response**:
1. Collect ground truth on a sample of recent production inputs.
2. Measure accuracy on recent vs historical examples.
3. If significant gap: retrain on recent data, with the drifted period overrepresented. See `maximus-fine-tuning`.
4. Consider a more frequent retraining cadence for rapidly changing domains.

---

## Type 3: Prompt Drift (LLM-specific)

**Definition**: The system prompt or few-shot examples for an LLM application are modified without a version bump or eval gate.

**Example**: An engineer edits the system prompt in the production database to fix a "small" tone issue. The edit inadvertently removes an instruction that was preventing a category of hallucination. No version was bumped; no eval was run.

**Why it matters**: For LLM apps, the prompt *is* a model parameter. A prompt change is equivalent to a weight update. Unlike weight updates (which require a deployment), prompts are often stored in databases and can be changed without any deployment gating.

**Detection methods**:
- **Prompt hash monitoring**: SHA-256 hash the active prompt at every serving startup. Alert if the hash differs from the registered hash for that model version. This is cheap, deterministic, and catches all modifications.
- **Registry cross-check**: On each deploy, fetch the active prompt and compare its hash to the hash stored in the model registry at that version.

**Response**:
1. Alert immediately on hash mismatch (this is always critical — no benign version of an untracked prompt change).
2. Identify who made the change and why.
3. Either: (a) register the new prompt as a new version with an eval run, or (b) restore the original prompt.
4. Lock the prompt storage: production prompts should not be editable without a deployment process. Move prompts from a mutable database to a versioned artifact store.

---

## Type 4: Covariate Shift (Special case of data drift)

**Definition**: The marginal distribution of inputs changes, but the conditional distribution P(Y|X) remains the same. The model's accuracy on the new inputs is lower because it was not trained on them, not because the correct answer changed.

**Example**: A model trained primarily on English-language inputs starts receiving more non-English inputs as the product expands internationally. The task hasn't changed, but the model performs worse on the new input distribution.

**Detection**: Same as data drift (embedding distance, feature statistics). Covariate shift is diagnosed when you confirm that the correct labels for drifted examples are consistent with the original task definition.

**Response**: Collect labeled data from the new distribution and add it to the training set. Consider a multilingual model or fine-tuning on the new distribution.

---

## Type 5: Feedback Loop Drift

**Definition**: The model's outputs influence the distribution of future inputs, creating a self-reinforcing loop.

**Example**: A content recommendation model learns to recommend certain content types. Users who see more of that content engage with it, which is logged as positive signal. The training data increasingly reflects the model's own biases.

**Why it matters**: This is a long-horizon, systemic failure. The model gradually optimizes for engagement with its own outputs, not with users' underlying needs.

**Detection**: Track the diversity of model outputs over time (entropy of recommendation distribution, category coverage). Alert when diversity drops significantly.

**Response**: Introduce diversity objectives into training. Log held-out exploration traffic that is not fed back into the training loop.

---

## Drift detection lag reference

| Detector type | Detection lag | Notes |
|---|---|---|
| Prompt hash | Immediate (next startup) | Zero lag for any prompt change |
| Embedding centroid | 1–6 hours | Depends on window size and traffic volume |
| Feature statistics | 1–24 hours | Depends on window size |
| Ground truth collection | Days to weeks | Requires annotation; the slowest but most reliable for concept drift |
| Downstream proxy metrics | Hours to days | Faster than GT collection; noisier |

---

## Severity levels

| Drift type | Typical severity | Typical response time |
|---|---|---|
| Prompt drift (any) | Critical | Immediate (< 1 hour) |
| Data drift (cosine dist > 0.25) | Critical | < 4 hours |
| Data drift (cosine dist 0.15–0.25) | Warning | < 24 hours |
| Output length shift > 30% | Warning | < 24 hours |
| Refusal rate > 10% | Critical | < 4 hours |
| Concept drift (accuracy drop > 5%) | High | < 48 hours |
| Feedback loop drift | High | < 1 week |
