# Labeling Guidelines Template

**Dataset**: [Dataset name and version]  
**Task**: [Classification / Ranking / Extraction / Generation quality rating]  
**Labels**: [List all label values]  
**Version**: 1.0  
**Author**: [Name]  
**Last updated**: YYYY-MM-DD

---

## Purpose of this document

This document defines what each label means, how to apply it consistently, and how to resolve ambiguous cases. Every annotator must read this document and complete the calibration exercise (Section 6) before labeling.

If you encounter a case not covered here, **do not guess**. Mark it as `[NEEDS ADJUDICATION]` and move on. Guessing creates label noise.

---

## 1. Task description

**What you are labeling**: [Clear 2–3 sentence description of what the annotator sees and what they are asked to judge]

**Example input**: [Paste a representative example of what the annotator will see]

**Why this matters**: [Brief explanation of how these labels will be used — training a classifier, building an eval set, etc. Annotators who understand the purpose make better judgments.]

---

## 2. Label definitions

### Label: `POSITIVE` / `1`

**Definition**: [Precise, unambiguous definition. Avoid subjective terms without operationalizing them.]

**Key criteria** (ALL must be true):
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

**Positive examples** (should be labeled POSITIVE):

| Example | Why it qualifies |
|---------|-----------------|
| [Example 1] | [Explanation] |
| [Example 2] | [Explanation] |
| [Example 3] | [Explanation] |

---

### Label: `NEGATIVE` / `0`

**Definition**: [Precise definition]

**Key criteria** (ANY sufficient to label NEGATIVE):
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Negative examples** (should be labeled NEGATIVE):

| Example | Why it doesn't qualify |
|---------|----------------------|
| [Example 1] | [Explanation] |
| [Example 2] | [Explanation] |

---

### Label: `BORDERLINE` / `2` (if applicable)

Use this label only when the example genuinely cannot be classified as POSITIVE or NEGATIVE. This is not a "I'm unsure" label — it is a label for examples that are genuinely ambiguous by design.

**Definition**: [When is something truly borderline? Be specific.]

**Borderline examples**:

| Example | Why it's borderline | Lean toward |
|---------|--------------------|-----------  |
| [Example 1] | [Explanation] | POSITIVE |
| [Example 2] | [Explanation] | NEGATIVE |

---

## 3. Hard cases and decision rules

These are cases that come up frequently and cause disagreement. The rule here is the canonical answer.

### Hard case 1: [Description]
**Rule**: [Specific rule to apply]  
**Example**: [Example of this case]  
**Label**: [POSITIVE / NEGATIVE / BORDERLINE]

### Hard case 2: [Description]
**Rule**: [Specific rule to apply]  
**Example**: [Example of this case]  
**Label**: [POSITIVE / NEGATIVE / BORDERLINE]

### Hard case 3: [Description]
**Rule**: [Specific rule to apply]  
**Label**: [POSITIVE / NEGATIVE / BORDERLINE]

---

## 4. What NOT to label based on

These are common sources of annotator error. Do not let these factors influence your label:

- **Your personal opinion about the topic**: The label is about [X], not about whether you agree with [Y].
- **Length of the example**: A short example can be POSITIVE; a long one can be NEGATIVE.
- **Spelling and grammar**: Unless grammar is part of the quality definition, don't penalize grammatical errors.
- **How you think the model "should" respond**: Label what is, not what you wish the model had done.

---

## 5. Annotation interface

[Screenshot or description of the labeling tool — Label Studio, Labelbox, Argilla, etc.]

**How to label**:
1. [Step 1]
2. [Step 2]
3. If you mark an example `[NEEDS ADJUDICATION]`, add a comment explaining why.

**Time budget**: Target [N] examples per hour. Do not rush — quality matters more than speed.

---

## 6. Calibration exercise (required before labeling)

Before you start your labeling queue, complete this calibration exercise. It consists of 20 examples from the gold set. Your answers will be compared to the gold-set answers to measure your initial agreement.

You will not be told the correct answers during the exercise — only after you submit. If your agreement is below κ = 0.70, you will have a brief calibration session with the task lead before proceeding.

**Access the calibration exercise**: [Link to calibration queue in labeling tool]

---

## 7. Quality monitoring

Your annotations are continuously monitored against gold-set examples embedded in your queue (10% of your queue is gold examples). This is how we detect annotator drift.

If your per-batch agreement drops below κ = 0.65:
- You will be flagged for review.
- A task lead will reach out within 24 hours.
- Your flagged annotations will be re-queued for adjudication.

This is not punitive — annotation drift happens, especially on edge cases. The monitoring exists to catch it early.

---

## 8. How to ask questions

- For quick questions: [Slack channel / chat link]
- For hard cases: mark as `[NEEDS ADJUDICATION]` with a comment; do not post examples in Slack (data confidentiality)
- For guideline ambiguities: raise in the weekly annotator sync ([day, time])

---

## 9. Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | YYYY-MM-DD | Initial version |
| 1.1 | YYYY-MM-DD | Added hard case 3; clarified BORDERLINE definition |

---

## 10. Inter-rater agreement targets

| Metric | Target | Action if below target |
|--------|--------|----------------------|
| Cohen's κ (pilot, all annotators) | ≥ 0.70 | Revise guidelines; re-pilot |
| Per-annotator κ (ongoing) | ≥ 0.65 | Calibration session |
| Adjudication rate | ≤ 15% of examples | If > 15%, guidelines need revision |
