# AI Feature Spec: [Feature Name]

**Status**: Draft | In Review | Approved | Deprecated  
**Author**: [Name]  
**Reviewers**: [Product Lead], [Tech Lead], [Safety], [Legal (if regulated)]  
**Created**: YYYY-MM-DD  
**Last updated**: YYYY-MM-DD  
**EU AI Act tier**: [Prohibited / High-risk / Limited / Minimal] (see `maximus-ai-safety-governance`)

---

## 1. Problem statement

_One paragraph. What user problem does this feature solve? What is the current state (no AI), and what does the AI version enable that wasn't possible before?_

## 2. User story

> As a [user type], I want [AI capability] so that [outcome].

**In scope**:
- [specific use case 1]
- [specific use case 2]

**Out of scope**:
- [explicitly excluded use case 1]
- [explicitly excluded use case 2]

---

## 3. User-visible behavior

### 3.1 Invocation
_How does the user trigger the AI feature? Button click, text field submit, background trigger, API call?_

### 3.2 Success state
_What does the user see when the model produces a good output?_

- **Format**: [free text / structured JSON / ranked list / classification label]
- **Length**: [max N words / tokens / items]
- **Tone**: [professional / conversational / technical]
- **Citations**: [required / optional / none]
- **Streaming**: [yes/no — if yes, what does the first token look like?]

### 3.3 Latency budget
- First-token latency (streaming): ≤ [N] ms
- Total response latency (P95): ≤ [N] ms
- Timeout behavior: [what happens after timeout?]

### 3.4 Failure / degraded state
_What does the user see when the model is unavailable, slow, or returning low-confidence output?_

---

## 4. Golden examples

_5–10 input→output pairs covering core use case, edge cases, and boundary conditions. These are used to calibrate evaluators and catch regressions._

| # | Input | Expected output | Notes |
|---|-------|-----------------|-------|
| 1 | [typical case] | [expected output] | Core use case |
| 2 | [short/minimal input] | [expected output] | Edge case |
| 3 | [long/complex input] | [expected output] | Scale test |
| 4 | [borderline case] | [expected output] | Tests boundary |
| 5 | [refusal case] | [refusal message] | Should refuse |
| 6 | | | |
| 7 | | | |

---

## 5. Refusal and failure modes

_Every input category that must be refused. Every row must have a trigger definition and a user-facing message._

| Category | Trigger definition | User-facing message | Logged? |
|----------|--------------------|---------------------|---------|
| Off-topic | Input is unrelated to [feature domain] | "I can help with [domain]. For other topics, try [alternative]." | Yes |
| Harmful content | Input requests [harmful category] | "I can't help with that." | Yes, with category |
| PII in input | Input contains detected PII | "Please don't include personal information like [type]. [Revised request suggestion]." | Yes, redacted |
| Ambiguous input | Input is too vague to answer reliably | "Could you tell me more about [missing context]?" | No |
| Out-of-scope language | Input is in an unsupported language | "I can only respond in [supported languages] right now." | Yes |
| Confidence below threshold | Model confidence score < [X] | "[disclaimer] Here's my best answer, though I'm not fully certain: ..." | Yes, with score |

---

## 6. Output specification

### 6.1 Output format
_If structured output: include the JSON schema here._

```json
{
  "type": "object",
  "required": ["answer", "confidence"],
  "properties": {
    "answer": {"type": "string", "maxLength": 500},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "citations": {"type": "array", "items": {"type": "string"}}
  }
}
```

### 6.2 Output constraints
- Maximum output length: [N tokens]
- Prohibited content in outputs: [list]
- Required disclaimers: [when and what]

---

## 7. Eval rubric

_Complete rubric in `examples/eval-rubric.md`. Summary thresholds for launch gates:_

| Metric | Stage 1 (internal) | Stage 2 (5%) | Stage 3 (full) |
|--------|-------------------|--------------|----------------|
| Task success rate | ≥ [N]% | ≥ [N]% | ≥ [N]% |
| Safety pass rate | ≥ 99% | ≥ 99.5% | ≥ 99.5% |
| Format compliance | ≥ [N]% | ≥ [N]% | ≥ [N]% |
| Latency P95 | ≤ [N]ms | ≤ [N]ms | ≤ [N]ms |
| User thumbs-up | — | ≥ [N]% | ≥ [N]% |

---

## 8. Rollout plan

| Stage | Traffic | Hold time | Promotion criteria | Approver |
|-------|---------|-----------|-------------------|----------|
| 0: Off | 0% | Until Stage 1 ready | Infra deployed, dashboard live | Tech lead |
| 1: Internal | Team only | ≥ 3 business days | All Stage 1 metrics met, 0 P1 incidents | Product + Tech lead |
| 2: 5% | 5% random | ≥ 7 days or 1,000 calls | All Stage 2 metrics met, 0 P1 incidents in 72h | Product lead |
| 3: 25% | 25% | ≥ 3 days | Metrics stable | Product lead |
| 4: 50% | 50% | ≥ 3 days | Metrics stable | Product lead |
| 5: Full | 100% | — | — | — |

**Automated rollback trigger**: [define the metric + threshold that triggers an alert and on-call page]

---

## 9. Kill switch

- **Feature flag name**: `[flag_name]`
- **Flag owner**: [name / on-call rotation]
- **Single-person authority**: Yes — no approval required for flag flip
- **Automated alert trigger**: [metric condition, e.g., safety flag rate > 1% in 30 min]
- **User-facing fallback**: "[Exact copy the user sees when the feature is disabled]"
- **Kill switch test date**: [must be tested during Stage 1]
- **Post-flip notification**: [list: product lead, safety team, engineering manager]

---

## 10. Success metrics

### Leading indicators (measured weekly)
- Task success rate: target [N]%, measurement method [human eval / automated judge]
- Safety pass rate: target ≥ 99.5%, measurement method [safety classifier]
- User thumbs-up rate: target [N]%, source [in-product feedback]
- Format compliance rate: target [N]%, source [automated schema check]

### Lagging indicators (measured monthly)
- Feature engagement rate: [% of eligible users who use the feature]
- D7 / D30 retention impact: [methodology — e.g., holdout cohort comparison]
- Support ticket rate for AI outputs: [target, normalized by feature usage]

### Anti-metrics (signals of harm)
- [User deletes AI output and rewrites manually: if > X% of uses, investigate]
- [User reports AI output as wrong: if > X% of uses, escalate]

---

## 11. Open questions

| # | Question | Owner | Target resolution date |
|---|----------|-------|----------------------|
| 1 | | | |
| 2 | | | |

---

## 12. Related artifacts

- Design: [link to design doc / Figma]
- Prompt: [link to prompt file in repo]
- Eval suite: [link to eval suite]
- Safety review: [link]
- Model card: [link]
