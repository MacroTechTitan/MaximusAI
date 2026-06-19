# Reference: EU AI Act Risk Tiers

**Regulation**: EU 2024/1689 (the AI Act), entered into force 1 August 2024.

**Timeline**:
- 2 February 2025: Prohibited practices (Article 5) apply
- 2 August 2025: Governance and general-purpose AI (GPAI) provisions apply
- 2 August 2026: High-risk system obligations (Annex III) fully apply
- 2 August 2027: High-risk systems under Annex I (product safety legislation) apply

---

## Tier 1: Prohibited AI Practices (Article 5)

Systems in this tier are **banned in the EU**. Do not build these.

| Practice | Article 5 reference |
|----------|---------------------|
| Subliminal manipulation that distorts behavior in a way that causes harm | Art. 5(1)(a) |
| Exploitation of vulnerabilities (age, disability, social situation) to distort behavior | Art. 5(1)(b) |
| Social scoring by public authorities leading to detrimental treatment | Art. 5(1)(c) |
| Real-time remote biometric identification in publicly accessible spaces by law enforcement (with narrow exceptions) | Art. 5(1)(d) |
| Biometric categorization based on sensitive attributes (race, religion, political opinion, etc.) | Art. 5(1)(e) (added in final text) |
| Emotion recognition in the workplace and educational institutions | Art. 5(1)(f) |
| Building criminal offense prediction systems based solely on profiling | Art. 5(1)(g) |
| Facial recognition databases built by untargeted internet/CCTV scraping | Art. 5(1)(h) |

**Action**: If a proposed feature touches any of these categories, stop. Escalate to legal and product immediately.

---

## Tier 2: High-Risk AI Systems (Annex III)

Systems in this tier require **mandatory conformity assessment** before market deployment.

### Annex III Categories

**Category 1: Biometric systems** (except prohibited under Art. 5)
- Remote biometric identification for purposes other than law enforcement
- Biometric categorization not prohibited under Art. 5
- Emotion recognition systems (not in workplace/education — those are prohibited)

**Category 2: Critical infrastructure**
- Safety components of critical digital, transport, water, gas, heating, electricity infrastructure management

**Category 3: Education and vocational training**
- Determining access to or admission to educational/vocational training institutions
- Evaluating learning outcomes or assessing students
- Monitoring or proctoring during tests

**Category 4: Employment, workers management, self-employment**
- Recruitment, screening, or CV filtering
- Evaluating candidates during interviews / tests
- Decisions on promotion, termination, task allocation
- Monitoring performance and behavior

**Category 5: Essential private and public services**
- Credit scoring and creditworthiness assessment
- Life and health insurance risk assessment
- Emergency services dispatch prioritization
- Eligibility assessment for social benefits/services

**Category 6: Law enforcement**
- Individual risk assessment for criminal activity prediction
- Lie detector / emotion detection use by police
- Evaluation of evidence reliability in criminal investigations

**Category 7: Migration, asylum, border control**
- Risk assessment of irregular migration
- Examination of asylum applications
- Verification of travel documents

**Category 8: Administration of justice and democratic processes**
- AI for researching, interpreting, or applying the law in specific cases
- AI that influences elections

### High-Risk System Obligations (Chapter III, Section 2)

If a feature is high-risk:

| Obligation | Article |
|-----------|---------|
| Risk management system (ongoing, documented) | Art. 9 |
| Data governance for training data (quality, bias mitigation) | Art. 10 |
| Technical documentation (before market placement) | Art. 11 |
| Automatic logging of system operation (audit logs, retained per purpose) | Art. 12 |
| Transparency to deployers (instructions for use, limitations) | Art. 13 |
| Human oversight measures (ability for humans to override/stop) | Art. 14 |
| Accuracy, robustness, cybersecurity requirements | Art. 15 |
| Conformity assessment before deployment | Art. 43 |
| Registration in EU database (for most high-risk systems) | Art. 49 |
| Post-market monitoring plan | Art. 72 |

---

## Tier 3: Limited Risk — Transparency Obligations (Article 50)

Systems that interact with humans or generate synthetic content must disclose their AI nature.

| System type | Obligation |
|------------|------------|
| AI system interacting directly with humans (chatbots) | Inform the user they are interacting with AI (Art. 50(1)) |
| Emotion recognition or biometric categorization (limited risk context) | Inform those exposed (Art. 50(3)) |
| AI-generated audio, image, video, text content (deepfakes) | Mark content as AI-generated (Art. 50(2)) |
| GPAI generating text published for public information | Machine-readable marking of AI-generated content (Art. 50(4)) |

**Action**: Any chatbot or user-facing AI assistant needs a disclosure that it is AI. Implement this in the UI.

---

## Tier 4: Minimal Risk

Everything else. No mandatory legal obligations under the AI Act.

**Voluntary**: The EU encourages minimal-risk system operators to adhere to voluntary codes of conduct (Article 95).

---

## General-Purpose AI (GPAI) Models (Articles 51–56)

Applies to foundation models (LLMs, multimodal models) placed on the EU market.

- All GPAI models: technical documentation, copyright compliance, training data summary published.
- GPAI models with systemic risk (compute threshold: ≥ 10²⁵ FLOPs, updated by Commission): adversarial testing, incident reporting, cybersecurity, energy efficiency.

**Practical implication**: If you're using a GPAI API (OpenAI, Anthropic, Google, Mistral), the model provider handles GPAI compliance. You handle the downstream application's risk tier.

---

## Classification Decision Tree

```
Is the practice listed in Article 5?
  YES → Do not build. (Prohibited)
  NO ↓

Does the feature fall under Annex III categories 1–8?
  YES → High-risk. Conformity assessment required before deployment.
  NO ↓

Is the feature a chatbot, deepfake generator, or emotion recognizer?
  YES → Limited risk. Transparency disclosure required.
  NO ↓

Minimal risk. Voluntary codes of practice apply.
```

---

## Documentation required for each tier

| Tier | Required documentation |
|------|----------------------|
| Prohibited | N/A — do not build |
| High-risk | Technical documentation (Art. 11), Risk management records (Art. 9), Audit logs (Art. 12), Conformity assessment (Art. 43), EU DB registration (Art. 49) |
| Limited risk | Transparency disclosure mechanism in product |
| Minimal risk | Recommended: voluntary model card and usage policy |

---

## Sources

- [EU AI Act full text (EUR-Lex)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689)
- [EU AI Act Annex III (high-risk systems)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689#anx_III)
- [AI Act Article 5 (prohibited practices)](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32024R1689#art_5)
- [EU AI Office implementation resources](https://digital-strategy.ec.europa.eu/en/policies/european-approach-artificial-intelligence)
