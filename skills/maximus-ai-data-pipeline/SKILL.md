---
name: maximus-ai-data-pipeline
description: "Data preparation for AI systems: dataset curation, labeling discipline, synthetic data generation, quality gates, data versioning with DVC or LakeFS, train/val/test isolation, leakage prevention, dataset cards, and deletion/right-to-be-forgotten compliance. Use when building or auditing training data pipelines for ML models — distinct from generic ETL or analytics engineering. Trigger phrases: 'build a training dataset', 'labeling guidelines', 'inter-rater agreement', 'synthetic data', 'data versioning', 'DVC', 'train test split', 'leakage prevention', 'dataset card', 'GDPR deletion training data'."
metadata:
  pillar: ai-engineering
  source: maximus
---

# Maximus — AI Data Pipeline

The model is only as good as the data it was trained on, and the data is only as good as the discipline behind it. This skill covers AI-specific data work: curation strategy, labeling rigor, synthetic generation, quality gates, versioning, and the legal obligations that trail every labeled example.

## When to use

- Building a new training, fine-tuning, or evaluation dataset.
- Auditing an existing dataset for quality, leakage, or compliance gaps.
- Setting up reproducible data versioning for a model training workflow.
- Responding to a deletion (right-to-be-forgotten) request on data used in training.

Do not use this skill for generic data engineering (ETL pipelines that don't feed model training). For those, a standard data engineering workflow applies.

## Core rules

1. **Dataset card before labeling.** Define the dataset's intended use, source, annotation schema, and known limitations before a single annotation is made. Cards drafted after the fact omit the decisions that matter most.
2. **Train/val/test are sacred splits.** No model developer touches the test set until final evaluation. Ever. Leakage is the silent killer of believable benchmarks.
3. **Label quality beats label quantity.** Ten thousand noisy examples hurt more than one thousand clean ones. Define a quality bar and enforce it with inter-rater agreement before scaling.
4. **Version everything.** Data + code + model = one reproducible artifact. Use DVC or LakeFS. "We trained on the latest CSV" is not a reproducible experiment.
5. **Deletion is a day-one concern.** If user data goes into training, plan the deletion workflow before you train, not after the legal letter arrives.

## Procedure

1. **Define the curation strategy.**
   - What is the task? (classification, generation, ranking, extraction)
   - What is the data source? (user logs, web crawl, curated manual, synthetic, purchased third-party)
   - What are the in-scope and out-of-scope examples? Write a 1-page curation spec.
   - Set a volume target: how many examples per class/task for the statistical power you need? Use a power analysis or a heuristic (fine-tuning typically needs 100–10,000 labeled examples; evaluation sets need ≥ 200 per slice).

2. **Set up data versioning.**
   - Use **DVC** (`dvc init`, `dvc add data/`, remote configured to S3 or GCS) for file-level versioning tied to git commits.
   - Use **LakeFS** if you need branch-and-merge semantics on a data lake (parquet/delta tables at scale).
   - Tag every dataset version: `v1.0.0-raw`, `v1.1.0-filtered`, `v2.0.0-augmented`. Never overwrite a prior version.
   - Store the DVC pointer file (`.dvc`) in git so any commit can reproduce its exact dataset.

3. **Design the labeling schema and guidelines.**
   - Write explicit labeling guidelines: definition of each label, positive examples, negative examples, hard cases.
   - Define a gold set (50–200 pre-labeled examples with known-correct labels) for annotator calibration.
   - Run a pilot: 3–5 annotators label the gold set independently. Measure inter-rater agreement (Cohen's κ for categorical; Krippendorff's α for multi-label or ordinal). Target κ ≥ 0.7 before scaling.
   - See `references/labeling-disciplines.md` for agreement metrics and thresholds.

4. **Execute labeling at scale.**
   - Use Label Studio (open source), Scale AI, Labelbox, or Argilla depending on volume and budget.
   - Seed every batch with gold-set examples (10% of each annotator's queue) to detect annotator drift.
   - Flag and adjudicate disagreements (majority vote, expert review, or consensus session).
   - Track per-annotator agreement continuously. Remove annotators below threshold.

5. **Generate synthetic data (when needed).**
   - Use LLM-generated synthetic data to: augment rare classes, cover edge cases, generate adversarial inputs.
   - Apply a quality gate: every synthetic example is reviewed by at least one human annotator, or filtered by an automated classifier with a known precision threshold.
   - Document the generation method, model, prompt, and filter in the dataset card. Do not mix synthetic and human-labeled examples silently — flag provenance per row.
   - Contamination risk: if the LLM was trained on data similar to your evaluation domain, synthetic examples may leak benchmark answers. Use held-out prompts or out-of-distribution generation.

6. **Apply quality gates.**
   - Deduplication: remove near-duplicates (MinHash LSH or embedding similarity). Duplicates between train and eval inflate benchmark scores.
   - Toxicity filter: run the dataset through a content classifier; remove or quarantine flagged examples.
   - PII scan: use Presidio or equivalent to detect and remove personal information. Coordinate with `maximus-ai-safety-governance`.
   - Distribution check: plot label distribution, input length distribution, and (for NLP) vocabulary coverage. Flag unexpected skews.

7. **Enforce train/val/test isolation.**
   - Split before any feature engineering or augmentation (split on raw examples, not derived features).
   - For time-series or temporal data: split by time, not randomly.
   - For user-level data: split by user, not by interaction (to prevent user-level leakage).
   - Never use validation or test data to tune hyperparameters.
   - See `examples/leakage-check.py` for automated leakage detection.

8. **Write the dataset card.**
   - Use the Hugging Face dataset card schema or Gebru et al. (2021) "Datasheets for Datasets" as the template.
   - Required sections: Dataset description, Source data, Annotation process, Quality metrics (agreement scores, pass rates), Known limitations, Licensing, Maintenance.
   - Publish the card with the versioned dataset. Update it on every major version bump.

9. **Implement deletion/right-to-be-forgotten compliance.**
   - Maintain a mapping from user ID → data row IDs in the dataset.
   - On deletion request: remove rows from all dataset versions and from any downstream fine-tuned model checkpoints (this may require retraining from a clean snapshot).
   - If exact removal from trained model weights is required, assess machine unlearning options or plan to retrain from the next clean snapshot.
   - Document the deletion SLA in the dataset card.

## Domain notes

- **DVC** (Data Version Control, MIT license) is the standard for file-based ML dataset versioning. Works alongside git. `dvc repro` reruns the full pipeline from source.
- **LakeFS** (open source / cloud) adds git-like branching to S3/GCS object stores — useful for teams running large-scale experiments on parquet tables.
- **Argilla** is the best open-source tool for LLM data annotation and RLHF preference collection.
- **Cohen's κ** is the standard for categorical tasks; **Krippendorff's α** handles ordinal, interval, and multi-annotator cases.
- **GDPR Article 17** (right to erasure) and **CCPA Section 1798.105** require deletion of personal data on request. There is active legal debate about whether this requires model retraining; assume yes for high-risk systems.
- Machine unlearning is an active research area. For production, plan for retraining from a clean data snapshot as the pragmatic fallback.

## Gotchas

- Deduplication that runs on train + val + test together will remove cross-split duplicates you needed to find. Dedup train separately, then check for overlap against val/test.
- "We'll label more later" without a quality process produces a growing pile of inconsistent examples. Fix the guidelines first.
- Synthetic data that works in the lab often fails in production because the LLM generates cleaner, more idealized examples than real user inputs. Weight synthetic data accordingly.
- DVC remote credentials in the git repo is a credential leak. Use environment variables or a secret manager.
- Dataset versioning is only useful if you also track which dataset version trained which model. Use experiment tracking (MLflow, W&B) to link them.

## Output

Versioned dataset (DVC-tracked), dataset card, labeling guidelines document, quality gate report (dedup count, toxicity filter count, PII scan results, label distribution, inter-rater agreement score), train/val/test split manifest, deletion compliance plan.
