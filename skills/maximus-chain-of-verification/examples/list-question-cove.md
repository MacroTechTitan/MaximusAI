# Worked example — CoVe on a list-based answer

**Why this example:** List-based questions have the highest hallucination rate in every LLM benchmark. The original [CoVe paper](https://arxiv.org/abs/2309.11495) reported the biggest gains here (0.15 → 0.35 F1 on Wikidata list questions). This example walks through a realistic list task and shows the exact list-mode workflow.

## Input question

> List every US state whose capital city is also the state's largest city.

## Phase 1 — Baseline draft

> The US states whose capital is also the largest city are: Boston (Massachusetts), Denver (Colorado), Honolulu (Hawaii), Indianapolis (Indiana), Little Rock (Arkansas), Nashville (Tennessee), Oklahoma City (Oklahoma), Phoenix (Arizona), Providence (Rhode Island), Salt Lake City (Utah), and Atlanta (Georgia).

## Phase 2 — Verification questions

List-mode CoVe: one verification question per list item.

| # | List item | Question |
|---|---|---|
| 1 | Boston / MA | Is Boston the largest city in Massachusetts? Is it the capital? |
| 2 | Denver / CO | Is Denver the largest city in Colorado? Is it the capital? |
| 3 | Honolulu / HI | Is Honolulu the largest city in Hawaii? Is it the capital? |
| 4 | Indianapolis / IN | Is Indianapolis the largest city in Indiana? Is it the capital? |
| 5 | Little Rock / AR | Is Little Rock the largest city in Arkansas? Is it the capital? |
| 6 | Nashville / TN | Is Nashville the largest city in Tennessee? Is it the capital? |
| 7 | Oklahoma City / OK | Is Oklahoma City the largest city in Oklahoma? Is it the capital? |
| 8 | Phoenix / AZ | Is Phoenix the largest city in Arizona? Is it the capital? |
| 9 | Providence / RI | Is Providence the largest city in Rhode Island? Is it the capital? |
| 10 | Salt Lake City / UT | Is Salt Lake City the largest city in Utah? Is it the capital? |
| 11 | Atlanta / GA | Is Atlanta the largest city in Georgia? Is it the capital? |

Plus one open-ended completeness question:

| # | Question |
|---|---|
| 12 | Which US state capitals are also the largest city in their state? Return the complete list. |

Q12 is critical — it catches items the baseline **missed**, not just items it got wrong.

## Phase 3 — Independent answers (fresh context per question)

| # | Answer | Confidence |
|---|---|---|
| 1 | Boston is the largest city in MA and the capital. ✓ | high |
| 2 | Denver is the largest city in CO and the capital. ✓ | high |
| 3 | Honolulu is the largest city in HI and the capital. ✓ | high |
| 4 | Indianapolis is the largest city in IN and the capital. ✓ | high |
| 5 | Little Rock is the capital of AR but NOT the largest city — that is also Little Rock actually, but the metro largest is disputed. Baseline claim is correct on Little Rock alone. | high (with note) |
| 6 | Nashville is the largest city in TN (edged out Memphis in 2021) and the capital. ✓ | high |
| 7 | Oklahoma City is the largest city in OK and the capital. ✓ | high |
| 8 | Phoenix is the largest city in AZ and the capital. ✓ | high |
| 9 | Providence is the largest city in RI and the capital. ✓ | high |
| 10 | Salt Lake City is the capital of UT and the largest city. ✓ | high |
| 11 | **Atlanta is the capital of GA but is NOT the largest metro; the city of Atlanta itself is the largest city by population within GA state boundaries. ✓** | high |
| 12 | Complete list per US Census 2020: Boston MA, Denver CO, Honolulu HI, Indianapolis IN, Little Rock AR, Nashville TN, Oklahoma City OK, Phoenix AZ, Providence RI, Salt Lake City UT, Atlanta GA, Columbia SC, Des Moines IA, Boise ID, Jackson MS, Cheyenne WY, Charleston WV. | high (multiple census sources) |

## Phase 4 — Revised draft

Verification found:
- All 11 baseline items confirmed.
- 6 additional items missed by baseline: **Columbia SC, Des Moines IA, Boise ID, Jackson MS, Cheyenne WY, Charleston WV.**

**Revised list (alphabetical by state, per US Census 2020):**
Little Rock AR, Phoenix AZ, Denver CO, Atlanta GA, Honolulu HI, Des Moines IA, Boise ID, Indianapolis IN, Boston MA, Jackson MS, Oklahoma City OK, Providence RI, Columbia SC, Nashville TN, Salt Lake City UT, Charleston WV, Cheyenne WY.

## Change summary

- **Kept:** 11 items (all baseline items confirmed).
- **Added:** 6 items missed by baseline (Columbia SC, Des Moines IA, Boise ID, Jackson MS, Cheyenne WY, Charleston WV).
- **Removed:** 0.

## Why this pattern works

Baseline LLM answers to list questions systematically **under-list**. The model generates a plausible-length list from memory and stops. Q12 — the open-ended completeness pass — is what catches the missing items. Without Q12, you would confirm what the baseline said but never notice the six missing states.

**The rule for list-mode CoVe:** always include an open-ended completeness question, not just per-item verification.
