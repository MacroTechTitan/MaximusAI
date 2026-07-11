# Reference — Confidence Ledger Spec

The confidence ledger is the deliverable's backbone. Every claim above a passing mention gets a row. This spec defines the fields, the tier-assignment rules, and reusable templates.

## Fields

| Field | Description |
|---|---|
| `claim` | One sentence, falsifiable, no hedging language folded into the sentence itself (hedging belongs in the confidence tier, not the wording). |
| `evidence_urls` | One or more URLs actually fetched this session. Never a URL recalled from memory without a fresh fetch. |
| `evidence_summary` | One or two lines: what the source(s) actually say, in their terms, not the conclusion you drew from them. |
| `inference_type` | One of: direct citation, triangulation, deduction, elimination, base-rate reasoning, expert consensus, negative evidence, analogical reasoning. See `references/inference-patterns.md`. |
| `confidence_tier` | high / medium / low. See tier criteria below. |
| `counter_evidence` | What the adversarial pass found against this claim, or the explicit string "none found after adversarial pass" — never leave this blank; blank means the adversarial pass wasn't run. |
| `gaps` | Anything about this claim that remains unresolved: unknown-public or unknown-could-probe-with-X. |
| `last_verified` | Date (or session timestamp) the evidence was fetched. Claims reused from a prior session's memory get re-verified or explicitly marked as carried forward without re-verification. |

## Tier-assignment rules

Assign tiers by evidence structure, not by how confident the claim *sounds*. A fluent sentence is not evidence of a high tier.

### High
- 2+ independent sources agree, **or** one primary source (filing, direct data, first-party documentation) plus a survived adversarial pass, **and**
- No unresolved counter-evidence — anything found in the adversarial pass was either explained, subsumed into the claim's own scope (e.g., "high under condition A"), or shown not to actually contradict the claim.

### Medium
- At least one credible source plus a plausible inference chain (triangulation, deduction, or base-rate reasoning shown explicitly), **or**
- Counter-evidence exists but is not decisive — it narrows the claim's scope rather than breaking it (e.g., "works well for stable-prefix workloads, less so for variable ones" rather than "does not work").

### Low
- A single source with no corroboration, **or**
- A thin inference chain (one weak analogy, one unverified proxy), **or**
- Unresolved counter-evidence that could not be run down further within the research session — the contradiction is real and unaddressed, not just unexplored.

**Never assign high confidence to a claim that rests solely on:** a single vendor-authored source, an LLM-memory recollection not verified this session, or analogical reasoning alone.

**A tier can — and should — drop mid-research.** If step 5 (adversarial verification) surfaces a real contradiction, drop the tier and record the counter-evidence. Do not keep the original tier and bury the contradiction in a footnote.

## Markdown table template

```markdown
| claim | evidence | confidence tier | counter-evidence | inference type |
|---|---|---|---|---|
| [claim] | [URL(s) + one-line summary] | high / medium / low | [finding, or "none found after adversarial pass"] | [type] |
```

## Extended markdown template (with gaps and verification date)

```markdown
### Claim: [claim text]
- **Evidence:** [summary] — [source name](URL)
- **Inference type:** [type]
- **Confidence tier:** [high / medium / low]
- **Counter-evidence:** [finding or "none found after adversarial pass"]
- **Gaps:** [unknown-public / unknown-could-probe-with-X / none]
- **Last verified:** [date]
```

## CSV template

```csv
claim,evidence_urls,evidence_summary,inference_type,confidence_tier,counter_evidence,gaps,last_verified
"Company Z ARR is approximately $25M-$35M","https://example.com/source1;https://example.com/source2","Headcount ~180 per LinkedIn; sector benchmark $150K-$300K rev/employee","triangulation","medium","none found in adversarial pass","unknown-public: exact disclosed ARR not available","2026-07-10"
```

Use the CSV form when the ledger has enough rows (roughly 8+) that a spreadsheet view is more useful than reading a long markdown table — save it as a workspace file alongside the narrative trace.

## Rules for maintaining the ledger through the iterative depth loop

- A claim's row is updated, not duplicated, when a later loop finds new evidence. Keep the row's history implicit in `last_verified` moving forward, not by stacking rows.
- If a claim is dropped entirely because it turned out not to matter to the final conclusion, remove its row — a ledger padded with irrelevant claims is as unhelpful as one missing important ones.
- If the loop revises the hypothesis itself (see `SKILL.md` step 5-to-1 revision path), the ledger's claims should be re-read against the *revised* hypothesis before the final synthesis — a claim can be true and irrelevant to the new framing.
