# Reference: Labeling Discipline and Inter-Rater Agreement

## Why annotation quality matters

Label noise is more destructive than small dataset size. A model trained on 10,000 noisy examples with κ = 0.5 will learn inconsistent patterns that don't transfer. A model trained on 1,000 clean examples with κ = 0.85 will generalize better.

The quality of a labeled dataset is determined at annotation time, not cleaning time. Cleaning after the fact removes obvious errors but cannot fix systematic annotator disagreement baked into the labels.

---

## Inter-Rater Agreement (IRA) Metrics

### Cohen's Kappa (κ)

**Use for**: Binary or multi-class categorical labels, two annotators.

**Formula**:
```
κ = (P_observed - P_expected) / (1 - P_expected)

P_observed = (number of agreements) / (total examples)
P_expected = sum over each class: (fraction labeled class_i by annotator A) × (fraction labeled class_i by annotator B)
```

**Interpretation**:

| κ range | Agreement level | Action |
|---------|-----------------|--------|
| < 0.40 | Poor | Stop labeling. Rewrite guidelines entirely. |
| 0.40 – 0.59 | Moderate | Guidelines need clarification. Revise and re-pilot. |
| 0.60 – 0.69 | Substantial (minimum for scale) | Acceptable to proceed carefully with monitoring. |
| 0.70 – 0.79 | Substantial (target) | Proceed. Good guidelines. |
| 0.80 – 1.00 | Almost perfect | Excellent. Proceed. |

**Practical notes**:
- κ assumes that disagreements are random. If annotators have systematic biases (one annotator is always more lenient), κ will be misleadingly high.
- Always look at the confusion matrix alongside κ. κ = 0.72 with one category having 0.40 agreement signals a definition problem for that category.

**Python calculation**:
```python
from sklearn.metrics import cohen_kappa_score
kappa = cohen_kappa_score(annotator_a_labels, annotator_b_labels)
```

---

### Krippendorff's Alpha (α)

**Use for**: Ordinal scales (1–5 ratings), interval data, more than two annotators, or when some examples have missing labels.

Krippendorff's α is more general than Cohen's κ:
- Handles any number of annotators (not just two)
- Handles missing annotations (not all annotators label all examples)
- Handles ordinal, interval, and ratio scales (via the distance metric)

**Interpretation thresholds** (Krippendorff's own guidelines):
- α ≥ 0.80: High reliability. Data is suitable for drawing firm conclusions.
- 0.667 ≤ α < 0.80: Acceptable reliability for tentative conclusions. Increase annotator training.
- α < 0.667: Low reliability. Do not proceed; fix the annotation process.

**Python calculation**:
```python
# pip install krippendorff
import krippendorff
import numpy as np

# reliability_data: 2D array, shape (n_annotators, n_examples)
# Use np.nan for missing annotations
alpha = krippendorff.alpha(
    reliability_data=reliability_data,
    level_of_measurement="ordinal"  # or "nominal", "interval", "ratio"
)
```

---

### Fleiss's Kappa

**Use for**: Categorical labels with more than two annotators when each example is labeled by the same number of annotators.

Less common than Cohen's κ or Krippendorff's α but occasionally required by labeling platforms that report it.

**Python**:
```python
from statsmodels.stats.inter_rater import fleiss_kappa
# Requires a frequency table: rows=examples, cols=categories
kappa = fleiss_kappa(freq_table)
```

---

## Annotator monitoring over time

Inter-rater agreement degrades as annotators become fatigued, change their interpretation of guidelines, or encounter new example types not covered in the original pilot.

**Continuous monitoring approach**: Embed gold-set examples in every batch (10% of each batch). Track per-annotator κ against the gold set over time.

```
Annotator monitoring dashboard (tracked weekly):

Annotator | Week 1 κ | Week 2 κ | Week 3 κ | Trend | Action
---------|---------|---------|---------|-------|-------
A        | 0.82    | 0.81    | 0.79    | Stable | None
B        | 0.76    | 0.70    | 0.62    | Declining | Calibration session
C        | 0.88    | 0.87    | 0.86    | Stable | None
```

**Trigger actions**:
- Per-annotator κ drops below 0.65: schedule a calibration session within 24 hours.
- Per-annotator κ drops below 0.60: pause that annotator's queue pending review.
- Overall batch κ drops below 0.65: call a team-wide calibration session; review recent guideline changes.

---

## Gold set design

The gold set is the calibration anchor for the whole annotation project. Design it carefully.

**Size**: 100–200 examples minimum. Larger for tasks with many edge cases.

**Composition**:
- ~50% clear positive examples (high confidence, easy to label)
- ~50% clear negative examples (high confidence, easy to label)
- ~15–20% edge cases or hard cases (drawn from the categories that cause most disagreement in practice)
- ~5% adversarial examples (designed to test the exact failure modes in the guidelines)

**Labeling the gold set**:
- One domain expert labels each example. Not majority vote — expert authority.
- For controversial hard cases: discuss to consensus among 2–3 domain experts, document the reasoning.
- Freeze the gold set once it's used for calibration. Do not modify it to reflect annotator performance.

**Hiding gold-set examples**:
- Annotators should not know which examples are gold (to prevent gaming).
- Seed them randomly throughout each batch, identical in appearance to regular examples.

---

## Labeling platform comparison

| Platform | Best for | Notes |
|----------|----------|-------|
| **Label Studio** | Open-source, on-premise, custom interfaces | Free. Strong for NLP/NER/CV. Requires DevOps setup. |
| **Argilla** | LLM output evaluation, RLHF preference data | Best open-source tool for LLM annotation. Integrates with HuggingFace. |
| **Scale AI** | High-volume, managed annotation workforce | Expensive but high quality. Good SLAs. |
| **Labelbox** | Enterprise ML teams, audit trails | Good compliance features. Mid-market price. |
| **Amazon Mechanical Turk** | Low-cost, high-volume, simple tasks | Quality varies significantly. Requires careful quality filtering (gold set seeding essential). |
| **Prolific** | Research-grade annotation, specialized populations | Better quality than MTurk for complex tasks. Research community standard. |

---

## Dataset card annotation quality section

The dataset card should document:

```markdown
## Annotation Process

- **Annotator pool**: [N annotators, describe expertise level]
- **Labeling tool**: [Label Studio / Scale AI / etc.]
- **Initial pilot size**: [N examples]
- **Pilot inter-rater agreement (Cohen's κ)**: [X.XX]
- **Pilot inter-rater agreement (Krippendorff's α)**: [X.XX] (if ordinal)
- **Calibration sessions held**: [N]
- **Final guidelines version**: [v1.N]
- **Ongoing gold-set monitoring frequency**: [Weekly / per-batch]
- **Average per-annotator κ at completion**: [X.XX]
- **Adjudication rate**: [X%] of examples required adjudication
- **Adjudication method**: [Majority vote / Expert review / Consensus session]
```
