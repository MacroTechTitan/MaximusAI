# Worked example — CoVe on a competitive-intel memo

**Scenario:** An analyst has produced a one-page memo on Kimi K3. It is about to ship to a partner as a factual brief. Run CoVe before delivery.

## Input draft (baseline)

> Kimi K3 was released by Moonshot AI in July 2026 as an open-weight Mixture-of-Experts model with 2.8T total parameters and 104B active parameters per token. It supports a 1M-token context window and uses native MXFP4 quantization for weights with MXFP8 activations. Kimi K3 scored 42.0 on SWE-Marathon and 87% on GPQA-Diamond, matching Claude Fable 5 on both benchmarks. The model is available under the Kimi K3 License, which is Apache 2.0 compatible.

## Phase 2 — Verification questions

| # | Claim | Question |
|---|---|---|
| 1 | Kimi K3 was released by Moonshot AI in July 2026 | Who released Kimi K3 and when? |
| 2 | 2.8T total parameters, 104B active | What are the parameter counts (total and active) for Kimi K3? |
| 3 | 1M-token context window | What is the maximum context window of Kimi K3? |
| 4 | Native MXFP4 weights + MXFP8 activations | What quantization does Kimi K3 use natively for weights and activations? |
| 5 | 42.0 on SWE-Marathon | What score did Kimi K3 achieve on SWE-Marathon? |
| 6 | 87% on GPQA-Diamond | What score did Kimi K3 achieve on GPQA-Diamond? |
| 7 | Matches Claude Fable 5 on both benchmarks | What did Claude Fable 5 score on SWE-Marathon and GPQA-Diamond? |
| 8 | Kimi K3 License is Apache 2.0 compatible | What is the Kimi K3 License and is it Apache 2.0 compatible? |

## Phase 3 — Independent answers (each fetched fresh, draft not visible)

| # | Verified answer | Source | Confidence |
|---|---|---|---|
| 1 | Moonshot AI released K3 in July 2026 | https://github.com/MoonshotAI/Kimi-K3 (fetched fresh) | high |
| 2 | 2.8T total, 104B active per token | K3 tech report README | high |
| 3 | 1M-token context window | K3 tech report README | high |
| 4 | MXFP4 weights, MXFP8 activations, quantization-aware trained | K3 tech report README | high |
| 5 | 42.0 on SWE-Marathon | K3 tech report README | high |
| 6 | 88.4% on GPQA-Diamond (not 87%) | K3 tech report benchmarks table | high |
| 7 | Claude Fable 5 scored 44.8 on SWE-Marathon, 89.1% on GPQA-Diamond | Anthropic Claude Fable 5 release page | high |
| 8 | Kimi K3 License is source-available, NOT Apache 2.0 compatible | LICENSE file in K3 repo | high |

## Phase 4 — Revised draft

> Kimi K3 was released by Moonshot AI in July 2026 as an open-weight Mixture-of-Experts model with 2.8T total parameters and 104B active parameters per token ([K3 tech report](https://github.com/MoonshotAI/Kimi-K3)). It supports a 1M-token context window and uses MXFP4 weights with MXFP8 activations, quantization-aware trained ([K3 tech report](https://github.com/MoonshotAI/Kimi-K3)). Kimi K3 scored 42.0 on SWE-Marathon and 88.4% on GPQA-Diamond ([K3 tech report benchmarks](https://github.com/MoonshotAI/Kimi-K3)). Claude Fable 5 scored 44.8 and 89.1% respectively ([Anthropic release](https://www.anthropic.com/)), so K3 is close but does not match on either benchmark. K3 ships under the Kimi K3 License, which is source-available but **not** Apache 2.0 compatible — commercial use requires reviewing the license terms.

## Change summary

- **Kept:** 5 claims (release date, params, context, MXFP4, SWE score).
- **Revised:** 2 claims.
  - GPQA-Diamond: 87% → 88.4%. Original was rounded incorrectly.
  - "Matching Claude Fable 5": untrue. Revised to show actual gap (K3 42.0 vs CF5 44.8, K3 88.4% vs CF5 89.1%).
- **Removed / corrected:** 1 claim.
  - "Apache 2.0 compatible" was false. K3 License is source-available with commercial-use terms. This is material for a partner brief — cannot ship the wrong license claim.

## Cannot confirm

None in this pass. All claims resolved to primary sources on the K3 repo or the Anthropic release page.

## Why this matters

The baseline draft would have shipped with two errors that a partner could easily verify (GPQA score and license claim), which would have damaged credibility on the *first* fact-check. CoVe caught both in one pass at ~2x token cost — cheap insurance for external delivery.
