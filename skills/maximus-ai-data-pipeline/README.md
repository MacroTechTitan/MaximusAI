# maximus-ai-data-pipeline

Data preparation discipline for AI systems — distinct from generic data engineering.

## What it is

This skill covers the end-to-end process of building high-quality datasets for training, fine-tuning, and evaluating ML models: curation strategy, annotation design and execution, inter-rater agreement measurement, synthetic data generation with safety guards, quality gating, data versioning (DVC, LakeFS), train/val/test isolation, leakage detection, dataset cards, and deletion compliance under GDPR and CCPA.

## Why it exists

Generic data engineering skills (ETL pipelines, data warehouses, SQL transformations) do not cover the AI-specific concerns: label quality, annotator agreement, benchmark leakage, model training reproducibility, and the legal obligation to delete training data on request. Teams that treat data pipeline work as "just engineering" ship models with hidden quality problems that don't surface until the model is in production.

The problem it solves: datasets that look fine but contain label noise, train/test leakage, undocumented splits, or unversioned changes — all of which produce misleading benchmarks and unreliable models.

## Quick start

1. **Write a curation spec.** Define the task, data source, in-scope and out-of-scope examples, and volume target before collecting any data.
2. **Initialize data versioning.** Run `dvc init` in the project repo, `dvc add data/raw/`, configure an S3 or GCS remote. Commit the `.dvc` file to git.
3. **Design labeling guidelines.** Write label definitions with positive examples, negative examples, and hard cases. Create a gold set of 50–100 pre-labeled examples.
4. **Pilot labeling and measure agreement.** Have 3–5 annotators label the gold set independently. Calculate Cohen's κ. If κ < 0.7, revise the guidelines before scaling.
5. **Apply quality gates and split.** Run deduplication, toxicity filtering, and PII scanning. Split by user (for user data) or by time (for temporal data). Run `examples/leakage-check.py` to verify isolation.

## When NOT to use it

- For analytics engineering or BI pipelines that don't feed model training. Use a standard data engineering workflow.
- For feature engineering on already-clean, already-split data. This skill covers the upstream pipeline, not feature transformation.
- For experiment tracking and model registry work. Use MLflow or Weights & Biases for those; this skill covers the data that feeds them.

## Related skills

- **maximus-fine-tuning** — consumes the dataset built here; dataset format and quality requirements for fine-tuning.
- **maximus-ai-safety-governance** — PII detection and deletion compliance that this pipeline must implement.
- **maximus-eval-and-test** — the evaluation set built here feeds the eval pipeline in that skill.
- **maximus-prompt-engineering** — few-shot examples in prompts are a lightweight alternative to labeled datasets for some tasks.
- **maximus-rag-pipeline** — document corpus curation for retrieval systems follows similar discipline.

## Glossary

**Inter-rater agreement (IRA)**: A statistical measure of how consistently multiple annotators label the same examples. Cohen's κ is standard for categorical tasks; Krippendorff's α handles multi-label and ordinal cases. Target κ ≥ 0.7 before scaling labeling.

**Gold set**: A curated set of examples with known-correct labels, used to calibrate annotators and measure annotator drift over time.

**DVC (Data Version Control)**: A git-adjacent tool for versioning large datasets and ML pipelines. Stores data in a remote (S3, GCS, etc.) and tracks pointers in git, enabling reproducible experiments.

**LakeFS**: An open-source data lake versioning system with git-like branch-and-merge semantics. Suitable for large parquet/delta table datasets at scale.

**Dataset card**: A document describing a dataset's contents, source, annotation methodology, quality metrics, known limitations, and licensing. Based on Gebru et al. (2021) "Datasheets for Datasets."

**Label noise**: Incorrect or inconsistent labels in a dataset. Causes models to learn incorrect patterns. More damaging than small dataset size.

**Train/val/test leakage**: When examples from the validation or test set influence model training (directly or via feature engineering). Causes inflated benchmark scores that don't reflect real-world performance.

**MinHash LSH**: A locality-sensitive hashing technique for fast approximate nearest-neighbor deduplication of text. Used to find near-duplicate examples across large datasets efficiently.

**Synthetic data**: Machine-generated examples, typically from an LLM, used to augment a training dataset. Requires human review or automated filtering to maintain quality. Must be flagged with provenance.

**Right to erasure (GDPR Article 17)**: The legal right of an EU resident to have their personal data deleted. For AI systems trained on user data, this may require removing rows from datasets and potentially retraining affected models.
