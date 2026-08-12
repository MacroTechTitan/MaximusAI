# Quality appraisal tools — which tool for which study design

Quality appraisal (Phase 5) is field- and design-specific. This reference maps the standard tools with sources.

## Clinical / health research

### Randomized Controlled Trials (RCTs)

**Cochrane Risk of Bias 2 (RoB 2)**

- The 2019 update, replacing RoB 1
- Assesses 5 domains: randomization process, deviations from intended interventions, missing outcome data, measurement of outcome, selection of reported result
- Judgment per domain: low risk / some concerns / high risk
- Overall risk: low / some concerns / high
- Source: [Cochrane RoB 2](https://www.riskofbias.info/welcome/rob-2-0-tool)
- Paper: Sterne JAC, et al. *RoB 2: a revised tool for assessing risk of bias in randomised trials.* BMJ. 2019;366:l4898. [DOI](https://doi.org/10.1136/bmj.l4898)

### Non-randomized studies (cohort, case-control, cross-sectional)

**Newcastle-Ottawa Scale (NOS)**

- Star system: 0–9 stars (higher = better quality)
- Assesses selection, comparability, outcome
- Different versions for cohort vs case-control
- Source: [Ottawa Hospital Research Institute NOS](https://www.ohri.ca/programs/clinical_epidemiology/oxford.asp)
- Note: NOS is widely used but has been criticized for inter-rater reliability; ROBINS-I (below) is often preferred for methodologically rigorous reviews

**ROBINS-I (Risk Of Bias In Non-randomized Studies — of Interventions)**

- Cochrane tool designed as observational-study analog of RoB 2
- 7 domains: confounding, selection, classification of interventions, deviations, missing data, measurement of outcomes, selection of reported result
- Judgment per domain and overall
- Source: [Cochrane ROBINS-I](https://methods.cochrane.org/methods-cochrane/robins-i-tool)
- Paper: Sterne JA, et al. *ROBINS-I: a tool for assessing risk of bias in non-randomised studies of interventions.* BMJ. 2016;355:i4919.

### Diagnostic accuracy studies

**QUADAS-2**

- Quality Assessment of Diagnostic Accuracy Studies, version 2
- 4 domains: patient selection, index test, reference standard, flow and timing
- Applicability + risk of bias judgments per domain
- Source: [QUADAS-2](https://www.bristol.ac.uk/population-health-sciences/projects/quadas/quadas-2/)

### Systematic reviews (reviewing reviews — "overview of reviews")

**AMSTAR 2**

- Assessing the Methodological Quality of Systematic Reviews
- 16-item checklist
- Overall confidence in review: high / moderate / low / critically low
- Source: [AMSTAR](https://amstar.ca/Amstar_Checklist.php)

### Qualitative research

**CASP (Critical Appraisal Skills Programme) Qualitative Checklist**

- 10 questions covering appropriateness of methodology, ethics, data analysis, findings
- Source: [CASP UK checklists](https://casp-uk.net/casp-tools-checklists/)

## ML / CS research (field-adapted appraisal)

No single canonical tool exists in ML equivalent to Cochrane RoB 2. This skill uses a **field-adapted appraisal** with the following dimensions:

### Reproducibility
- Code released with the paper? (link functional?)
- Datasets available? (public or gated?)
- Seeds specified? (or at minimum, seed range and variance reported)
- Compute requirements documented?
- Environment / dependencies specified?

### Evaluation rigor
- Train/test contamination checked? (especially critical for LLMs — 2024–2026)
- Held-out benchmarks used, not just cross-validation on the training set?
- Statistical tests on the reported differences? (p-values, confidence intervals, or bootstrap)
- Multiple runs with variance reported? (single-run results are unreliable)
- Baseline strength: are the baselines competitive or straw-men?

### Fair comparison
- Same compute budget?
- Same data?
- Same tokenization / preprocessing?
- Publication timing (methods evaluated on benchmarks that existed at their training cutoff, not benchmarks released after)

### Peer-review status
- Peer-reviewed conference / journal? (name the venue)
- Preprint only? (arXiv timestamp)
- Preprint later peer-reviewed? (note the update)

### Grading
Grade each ML paper on a **3-level scale**: strong / adequate / weak. Report per-paper in the extraction table.

## Public health / policy

**JBI (Joanna Briggs Institute) Critical Appraisal Checklists**

- Multiple tools by study type (case reports, case series, quasi-experimental, prevalence studies)
- Source: [JBI checklists](https://jbi.global/critical-appraisal-tools)

## Rule for the reviewer

- **Do not exclude papers based on quality alone.** Extract the finding, appraise the quality, and weight in the synthesis. A high-quality null finding and a low-quality positive finding both belong in the extraction table — GRADE will handle the weighting.
- **Do not appraise a study with the wrong tool.** RoB 2 is for RCTs. Applying it to a cross-sectional study produces meaningless results.
- **Do note when appraisal is field-adapted** — say so in the method section. Reviewers accept adapted appraisal for fields where canonical tools do not exist; they do not accept "we made up our own scale."

Last reviewed: **2026-07-31**.
