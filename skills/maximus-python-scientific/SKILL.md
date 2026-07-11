---
name: maximus-python-scientific
description: "Build reproducible Python pipelines for scientific computing, ML, and data analysis. Use when writing code that produces results others must reproduce, when the user mentions science, research, paper, journal, experiment, reproducibility, DVC, MLflow, Jupyter-to-production, or when building a data pipeline that will run more than once. Enforces pinned dependencies, fixed seeds, versioned data, config files instead of hard-coded params, CI verification, and Docker/Binder packaging. Covers Python with NumPy, pandas, scikit-learn, PyTorch, and TensorFlow."
metadata:
  pillar: build
  source: maximus
---

# Maximus — Python Scientific & Reproducible Pipelines

A scientific result is only as credible as its reproducibility. A pipeline that only runs on the author's laptop is folklore, not science. This skill is the discipline that makes Python work re-executable by anyone, including future-you.

## When to use

- Building any analysis, experiment, or model that produces results others (or future-you) need to reproduce.
- Promoting an exploratory Jupyter notebook to production or to a paper submission.
- The user mentions: research, paper, journal, experiment, reproducibility, seeds, DVC, MLflow, deterministic, Binder, Zenodo, or "make this reproducible".
- Building a data pipeline that will run on a schedule or be handed off to a teammate.

## The four pillars of reproducibility

1. **Locked environment** — exact library versions captured.
2. **Versioned code** — full git history; tagged releases for submissions.
3. **Versioned data** — provenance, checksums, and ideally DVC or git-LFS.
4. **Automated, single-command pipeline** — `make all` or `python run.py` reproduces everything from raw data to final outputs.

If any pillar is missing, results are not reproducible. Period.

## Procedure

### 1. Environment lock

- Use a virtual environment per project: `python -m venv .venv` or `uv venv`. Activate before any install.
- Pin **exact** versions in `requirements.txt` (or `pyproject.toml` with a lock file). `numpy==1.26.4`, not `numpy>=1.26`.
- Record the Python version: `python --version >> environment_info.txt`. Record OS and arch — results can differ between Linux/macOS and x86/ARM.
- For team or paper-grade reproducibility, ship a `Dockerfile`:
  ```dockerfile
  FROM python:3.12-slim
  WORKDIR /app
  COPY requirements.txt .
  RUN pip install --no-cache-dir -r requirements.txt
  COPY . .
  CMD ["python", "run_analysis.py"]
  ```

### 2. Seeds and determinism

Set seeds at the top of every entry-point script:

```python
import os, random
import numpy as np

SEED = 42
os.environ["PYTHONHASHSEED"] = "0"
random.seed(SEED)
np.random.seed(SEED)
# rng = np.random.default_rng(SEED)  # preferred for new code

# Framework-specific
# torch.manual_seed(SEED); torch.cuda.manual_seed_all(SEED); torch.use_deterministic_algorithms(True)
# tf.random.set_seed(SEED)
# sklearn: pass random_state=SEED to every estimator and split
```

Report the seed in the methods section / README so exact reproduction is possible.

### 3. Code structure

- `data/` (raw, immutable; gitignored or DVC-tracked), `src/` (pipeline code as importable modules), `notebooks/` (exploration only, never production), `tests/`, `configs/`, `results/` (generated, gitignored), `Dockerfile`, `Makefile`, `README.md`.
- **Notebooks are for exploration, not production.** When a notebook's logic is final, extract functions into `src/` modules and call them from a slim driver script. Then write a unit test against the extracted function.
- **Pipeline as a sequence of pure functions:**
  ```python
  raw = load_data(cfg.input_path)
  clean = clean_data(raw)
  features = build_features(clean, cfg)
  model = train(features, cfg)
  save_results(model, evaluate(model, features), cfg.output_path)
  ```
- **Checkpoints between expensive steps**: `cleaned.to_parquet("checkpoints/01_cleaned.parquet")`. Add a `--resume` flag that skips completed checkpoints.

### 4. Configuration

- No hard-coded paths, thresholds, or hyperparameters in code. Put them in `configs/<name>.yaml`:
  ```yaml
  seed: 42
  data:
    input: data/raw/observations.csv
    train_split: 0.8
  model:
    type: random_forest
    n_estimators: 200
  ```
- Load with `yaml.safe_load`. Pass the loaded config object through the pipeline.
- Commit configs to git. Every result traces back to a config + a git SHA.

### 5. Data versioning and provenance

- Raw data is immutable. Never edit raw files; transformations write to `data/processed/`.
- Record provenance: URL/query, download date, and checksum.
  ```python
  import hashlib
  with open("data/raw/observations.csv", "rb") as f:
      checksum = hashlib.sha256(f.read()).hexdigest()
  ```
- For large data, use DVC or git-LFS to version files alongside code without bloating git.

### 6. Testing

- Unit tests for every transformer in `src/`: given known input, produce known output.
- Schema and null-rate tests at the data-loading boundary (pandera, great_expectations, or a hand-rolled check). Bad data is the most common silent failure.
- End-to-end smoke test on a tiny sample dataset — runs in seconds, exercises the full pipeline. Wire it to CI.

### 7. CI

- GitHub Actions workflow that installs the locked environment, runs unit tests, then runs the end-to-end smoke pipeline on each push. This catches reproducibility-breaking changes immediately rather than during peer review.

### 8. Packaging for sharing

- For a paper/journal submission: archive on Zenodo or Figshare to get a DOI. Include raw data (or instructions to obtain), all code, environment files, README with run instructions, and expected outputs for verification.
- For interactive sharing: add a `requirements.txt` and a Binder badge.

### 9. ML-specific additions

- **Versioned experiments**: MLflow or Weights & Biases. Log every run with seed, config, git SHA, metrics, and artifact paths.
- **Data validation gate**: schema + distribution check before the model trains. Block the run if it fails.
- **Model evaluation gate**: defined threshold a candidate must beat to be promoted. Automated; not a human eyeball.
- **Pipeline object, not loose transforms**: `sklearn.pipeline.Pipeline` or equivalent — bake every transform into the same object you serialize, so train-time and inference-time transforms cannot diverge.
- **No hard-coded column names** in transformers. Pull column lists from config or from the schema.

## Gotchas

- **Notebook-only science** doesn't reproduce. Extract functions and test them.
- **`numpy>=1.26`** is not a pin. Use `==`.
- **Forgetting `random_state=`** on a single sklearn estimator makes the whole pipeline non-deterministic.
- **Editing raw data files** destroys provenance. Raw is immutable; transformations write elsewhere.
- **Hard-coded paths** turn a portable pipeline into a personal one. Configs always.
- **Missing the Docker image** means another machine's library mix breaks your numerical results in ways that are hours to diagnose.
- **Skipping the data-validation gate** lets bad data train silently bad models.

## Output

A reproducible project tree (or PR adding the reproducibility layer to an existing one): `requirements.txt` or lock, `Dockerfile`, `configs/`, `src/`, `tests/`, `Makefile`, `README.md` with the exact reproduction commands. Final chat summary lists: pinned versions count, seed-set locations, CI status, and the single command to reproduce.
