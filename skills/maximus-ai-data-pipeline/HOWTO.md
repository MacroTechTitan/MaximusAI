# HOWTO — maximus-ai-data-pipeline

Step-by-step recipes for AI data pipeline work.

---

## Recipe 1: How to build a labeled dataset

**Goal**: Produce a clean, consistently labeled dataset ready for model training or evaluation.

**Steps**:
1. Write the labeling guidelines document before any annotation begins. Include: label definitions, positive examples (3+ per label), negative examples (3+ per label), hard cases with correct answers explained.
2. Build a gold set: select 100–200 examples with known-correct labels. These are pre-labeled by a domain expert, not an annotator. Store separately; use only for calibration and agreement measurement.
3. Recruit annotators. For specialized tasks: domain experts or trained contractors. For general tasks: platforms like Scale AI, Labelbox, or Amazon Mechanical Turk (with careful quality filtering).
4. Run a calibration pilot: have 3–5 annotators label the gold set independently. Calculate inter-rater agreement (Cohen's κ for binary/categorical; Krippendorff's α for ordinal/multi-label). See `references/labeling-disciplines.md`.
5. If κ < 0.6: the guidelines are unclear. Convene a consensus session, identify the disagreement patterns, revise the guidelines. Re-pilot before scaling.
6. If κ ≥ 0.7: proceed to full-scale labeling. Seed each annotator's queue with 10% gold-set examples (randomly mixed) to monitor drift.
7. Review batches: after every 500 annotations, recalculate per-annotator agreement against the gold set. Flag annotators below κ = 0.65 for retraining or removal.
8. Apply majority vote (or expert adjudication for hard cases) to examples with disagreements. Log the resolution method per example.
9. Version the final dataset with DVC (Recipe 4). Write the dataset card (included in `references/labeling-disciplines.md`).

**Verification**: Overall κ ≥ 0.7 on the gold set. Per-annotator κ ≥ 0.65. Dataset card is populated.

**Common pitfalls**:
- Writing guidelines that are clear to the domain expert but not to the annotators. Pilot tests reveal this.
- Scaling before achieving acceptable agreement — produces a large, noisy dataset faster than a small clean one.
- Gold set drift: adding examples to the gold set over time without re-calibrating. Freeze the gold set once annotation begins.

---

## Recipe 2: How to generate synthetic data safely

**Goal**: Augment a training dataset with LLM-generated examples while maintaining quality and preventing contamination.

**Steps**:
1. Define the generation purpose: rare class augmentation, edge case coverage, or adversarial example generation. Synthetic data for the core distribution should be minimized — real data is always preferable.
2. Write a generation prompt that produces diverse examples. Include: format specification, diversity instructions ("vary sentence length, vocabulary, and framing"), and exclusion instructions ("do not reproduce training examples verbatim").
3. Generate in batches. Tag every synthetic example with `{"provenance": "synthetic", "generator_model": "gpt-4o-2024-08-06", "generation_date": "..."}` as metadata. Never mix provenance silently.
4. Apply the same quality gates as real data: deduplication against the existing dataset, toxicity filtering, PII scanning.
5. Human review gate: for training data, require human review of at least 20% of synthetic examples (random sample). For evaluation data, require 100% human review — a synthetic eval set is not a real eval set.
6. Contamination check: if the generating model might have been trained on your evaluation domain (e.g., generating examples that look like known benchmarks), use held-out prompts or domain-shifted generation. Document the risk in the dataset card.
7. Quantify the synthetic fraction: in the dataset card, report the percentage of examples that are synthetic, by split.

**Verification**: Every synthetic example has provenance metadata. 20%+ human review pass rate recorded. Contamination risk documented in dataset card.

**Common pitfalls**:
- Using GPT-4o to generate training data for a task where GPT-4o is also the evaluation oracle. You're measuring whether GPT-4o agrees with GPT-4o.
- Synthetic examples that are cleaner and more idealized than real user inputs. The trained model won't transfer.
- Not documenting the generation prompt. Reproducibility requires prompt + model + sampling parameters.

---

## Recipe 3: How to prevent train/test leakage

**Goal**: Ensure the test set is a true holdout — no information from test examples influenced model training.

**Steps**:
1. Split the raw dataset before any preprocessing, feature engineering, or augmentation. Splitting on preprocessed data means preprocessing statistics (vocabulary, normalization) can leak.
2. For user-level data: split by user ID, not by interaction. If user 123 appears in train, all of user 123's interactions are in train. This prevents user-specific stylistic cues from leaking.
3. For temporal data: split by time. Train on [T0, T1), val on [T1, T2), test on [T2, T3). Never shuffle before splitting temporal data.
4. Deduplicate across splits: run MinHash LSH or embedding-similarity deduplication after splitting, checking for near-duplicates between train and val/test. Remove them from train (not from test).
5. Run `examples/leakage-check.py` to verify no example IDs overlap across splits, and to check for near-duplicate contamination.
6. Lock the test set: after the initial split, the test set is write-protected. No new examples are added. No examples are removed based on model performance. No one trains on it until final evaluation.
7. Document the split methodology in the dataset card. Include: split ratios, split method (user-based, time-based, random), deduplication method, and any examples removed from train due to cross-split similarity.

**Verification**: `examples/leakage-check.py` reports zero ID overlaps and zero near-duplicate overlaps between train/test and val/test.

**Common pitfalls**:
- Hyperparameter tuning on the test set ("we tried 10 checkpoints and the best one got 92% on test"). This is test set leakage. Use validation.
- Deduplication run on the full dataset before splitting — removes cross-split duplicates you needed to detect.
- "We removed outliers from the test set because they were hard" — this inflates test performance. The hard cases are exactly what you want in the test set.

---

## Recipe 4: How to version a dataset with DVC

**Goal**: Make every version of a dataset reproducible, tied to a git commit, and accessible without duplicating storage.

**Steps**:
1. Initialize DVC in your project: `dvc init` (in the same directory as your git repo). Commit the `.dvc/` directory to git.
2. Configure a remote storage backend:
   ```bash
   dvc remote add -d myremote s3://your-bucket/dvc-cache
   dvc remote modify myremote region us-east-1
   ```
3. Add your dataset directory: `dvc add data/raw/`. This creates `data/raw.dvc` (the pointer file) and adds `data/raw/` to `.gitignore`. Commit the `.dvc` file: `git add data/raw.dvc .gitignore && git commit -m "data: add raw dataset v1.0.0"`.
4. Push data to remote: `dvc push`. The actual files go to S3; the pointer goes to git.
5. Tag dataset versions: `git tag -a data-v1.0.0 -m "Raw dataset, 5000 examples, unfiltered"`. Use semantic versioning: `data-v1.1.0` for filtered, `data-v2.0.0` for new labeling pass.
6. To reproduce any historical dataset version: `git checkout data-v1.0.0` then `dvc pull`. The exact files from that version are restored.
7. For pipelines (preprocessing, filtering, splitting): use `dvc run` or define a `dvc.yaml` pipeline. Each stage has defined inputs, outputs, and command. `dvc repro` reruns only stages with changed inputs.
8. In experiment tracking (MLflow, W&B), log the git commit hash (which pins the DVC pointer) alongside each training run. This creates the data ↔ model version link.

**Verification**: Check out a prior git tag, run `dvc pull`, confirm the dataset files match the expected version. Run `dvc status` to verify no uncommitted changes.

**Common pitfalls**:
- Committing large data files directly to git. They belong in DVC, not git. Use `.gitignore` to prevent this.
- DVC remote credentials hardcoded in the repo. Use `dvc remote modify myremote credentialpath ~/.aws/credentials` or environment variables.
- Not tagging dataset versions — making it impossible to reproduce a training run from 6 months ago.

---

## Recipe 5: How to handle a deletion (right-to-be-forgotten) request for training data

**Goal**: Fulfill a GDPR Article 17 / CCPA Section 1798.105 deletion request when the data subject's data is in a training dataset.

**Steps**:
1. Confirm this is in scope: does the deletion request cover data that was used to train or fine-tune a model? (If only used for analytics, standard deletion applies — simpler.)
2. Look up the data subject's row IDs in the training dataset using the user ID → row ID mapping maintained at ingestion time. (If this mapping doesn't exist, you have a compliance gap — add it immediately for future data ingestion.)
3. Remove the rows from all dataset versions. With DVC, create a new dataset version with the rows removed and push: `dvc add data/`, `git commit`, `dvc push`, `git tag data-v2.1.0-deletion`.
4. Assess the trained model impact:
   - If the affected rows were < 0.1% of training data: document the deletion, flag the existing model as "trained on partially deleted dataset," and plan to retrain at the next scheduled cycle.
   - If the affected rows were > 0.1% or the data subject's data was disproportionately influential: treat as requiring retraining from the clean snapshot.
5. Retrain from the clean dataset snapshot (if required). Promote the new model through the standard staged rollout.
6. Confirm deletion: document the deleted row IDs, the dataset version before and after, any model versions trained on the affected data, and the retraining decision (and rationale) in a deletion log.
7. Respond to the data subject within the GDPR deadline (1 month, extendable by 2 months for complexity — document the extension if used).

**Verification**: Deletion log records: request date, row IDs removed, dataset versions affected, model versions affected, retraining decision, response date.

**Common pitfalls**:
- No user ID → row ID mapping. This means you cannot verify deletion without scanning the entire dataset. Add the mapping at ingestion time.
- Deleting from the active dataset but not from archived dataset versions. All versions that predate the deletion are flagged; downstream use of those versions is restricted.
- Assuming deletion from the dataset is sufficient — if the model was trained on the data, the data's patterns may be in the weights. Document this residual risk and the retraining plan.
