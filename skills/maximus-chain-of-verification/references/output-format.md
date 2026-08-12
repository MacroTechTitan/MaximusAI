# Output format — verification-questions.json and verification-answers.json

The runner script (`scripts/run_cove.py`) uses these JSON shapes so the pipeline is reproducible. Agents can produce the same shape manually.

## verification-questions.json

Produced at the end of Phase 2. One entry per verifiable claim.

```json
{
  "draft_id": "draft-2026-07-31-001",
  "generated_at": "2026-07-31T21:04:00Z",
  "claims": [
    {
      "claim_id": "c1",
      "claim_text": "K3 scored 42.0 on SWE-Marathon per the K3 tech report.",
      "questions": [
        {
          "q_id": "c1-q1",
          "text": "What score did Kimi K3 achieve on SWE-Marathon according to the K3 tech report?"
        }
      ]
    },
    {
      "claim_id": "c2",
      "claim_text": "Anthropic released Claude Fable 5 in June 2026.",
      "questions": [
        {
          "q_id": "c2-q1",
          "text": "When did Anthropic release Claude Fable 5?"
        },
        {
          "q_id": "c2-q2",
          "text": "What is the release month and year of Claude Fable 5?"
        }
      ]
    }
  ]
}
```

Rules:
- Every `claim_text` copies the draft verbatim (so the ledger later can quote it exactly).
- Every question is answerable **without the draft in context**. If a question refers to "the study mentioned above," rewrite it.
- 1–3 questions per claim. More is diminishing returns.

## verification-answers.json

Produced at the end of Phase 3. One entry per question. Each question is answered in an **independent context** (fresh sub-agent or cleared history).

```json
{
  "draft_id": "draft-2026-07-31-001",
  "answered_at": "2026-07-31T21:07:00Z",
  "answers": [
    {
      "q_id": "c1-q1",
      "claim_id": "c1",
      "answer_text": "According to the Kimi K3 tech report README, Kimi K3 scored 42.0 on SWE-Marathon.",
      "sources": [
        {
          "url": "https://github.com/MoonshotAI/Kimi-K3",
          "fetched_at": "2026-07-31T21:06:12Z",
          "matches_claim": true
        }
      ],
      "confidence": "high"
    },
    {
      "q_id": "c2-q1",
      "claim_id": "c2",
      "answer_text": "Cannot confirm with an independent source.",
      "sources": [],
      "confidence": "cannot_confirm"
    }
  ]
}
```

Rules:
- Every answer includes at least one source URL that was **re-fetched during Phase 3**. The draft's own cited sources do not count until re-verified.
- `confidence` is one of: `high`, `medium`, `low`, `cannot_confirm`. Mapping to the final ledger:
  - `high` → kept (or revised if the answer differs from the claim)
  - `medium` → revised with a caveat OR kept with confidence: medium
  - `low` → softened or cut
  - `cannot_confirm` → surfaced in the "Cannot confirm" section; user decides
- `matches_claim` records whether the fetched source actually says what the claim asserts.

## Final revised draft output

The revised draft is Markdown. Every material change from the original is recorded in the ledger. Silent rewrites are forbidden — even a comma-level change to a numeric value must show up.

## Why the JSON shapes matter

- **Reproducibility.** The pipeline can be re-run against the same draft and produce the same questions, then re-verified later against fresh sources.
- **Auditability.** Regulators, editors, and internal reviewers can see exactly what was checked and how.
- **Composability.** Downstream skills (report generation, publishing, compliance filing) can key off `confidence` and `sources`.

Last reviewed: **2026-07-31**.
