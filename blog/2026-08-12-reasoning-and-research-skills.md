# Three skills that make Maximus research like a person

*2026-08-12 · Macro Tech Titan*

Maximus already had two research skills — [`maximus-deep-research`](../skills/maximus-deep-research) for multi-source synthesis and [`maximus-deep-research-pro`](../skills/maximus-deep-research-pro) for hypothesis-first inference with adversarial verification. Good coverage for two shapes. Missing the other three that a working analyst, journalist, or graduate researcher actually reaches for.

Today three new skills close that gap. **42 skills total** — up from 39.

## What's new

**[`maximus-chain-of-verification`](../skills/maximus-chain-of-verification)** — the reasoning-quality skill that wraps everything else.

Factored Chain-of-Verification, [as published by Dhuliawala et al. in 2023](https://arxiv.org/abs/2309.11495). Draft → generate independent verification questions → answer each in a fresh context without the draft visible → revise. The paper reports 40–60% hallucination reduction; the 2026 clinical and legal deployments pair it with RAG grounding and hit 1–2% error rates.

The critical rule the skill enforces: **independent verification means independent context**. Naive fact-check prompts collapse into "does the draft agree with itself?" — which the model always says yes to. This skill spawns fresh sub-agents per verification question so the draft cannot leak in.

Outputs a claim-by-claim confidence ledger with kept / revised / removed counts and an explicit "Cannot confirm" section. Runs on top of any research skill or on standalone drafts. Lives in the AI Engineering pillar.

**[`maximus-investigative-research`](../skills/maximus-investigative-research)** — research the way a working reporter or intelligence analyst does it.

The mental model is a reporter with a notebook, not a search engine with a summarizer. Six phases: lead intake → source mapping (primary / secondary / adversarial) → timeline construction → contradiction hunt → corroboration pass → report with confidence tags.

Where the aggregation skill would average two sources into a smoothed synthesis, this skill picks a spine — the strongest available primary source — and traces claims back to it. Contradictions between sources are surfaced as evidence, not smoothed away. Single-sourced claims are flagged, not laundered.

Ships with worked examples for private-company investigation and public-record event reconstruction, plus references on source-tier classification, contradiction patterns, and ethical limits (public-record only; no paywall bypass; no private-individual investigation for personal purposes). Writing/Research/People pillar.

**[`maximus-literature-review`](../skills/maximus-literature-review)** — systematic literature review with PRISMA-style discipline.

Seven phases: scope + PICO/PECO → search protocol → two-pass screening → extraction table → quality appraisal → synthesis with GRADE grading → PRISMA-style flow report. Ships with worked examples for a clinical RCT review and an ML methods review (the field-adaptation using TMBM instead of PICO), plus references on PRISMA 2020, GRADE grading, quality-appraisal tools (RoB 2, Newcastle-Ottawa, ROBINS-I, QUADAS-2, AMSTAR 2, CASP), and 2026 database-coverage notes including the LLM benchmark-contamination issue.

Grades confidence per finding, not per paper — a discipline that separates real synthesis from vote-counting. Also lives in Writing/Research/People pillar.

## Why these three, and why together

Every AI-native builder has by now shipped or debugged a research feature that hallucinated a citation, mis-quoted a source, or smoothed over a contradiction. Not because the model was bad — because the workflow shape was wrong.

The three shapes that go missing most often:

- **Verification as a distinct step** (not a "please be accurate" system-prompt line). CoVe makes it a first-class phase with independent context.
- **Investigative discipline** — the reporter's habit of source-tiering, timeline reconstruction, and refusing to smooth contradictions. Missing from every LLM tool that treats sources as interchangeable.
- **Systematic evidence-synthesis discipline** — the researcher's habit of PRISMA flow, pre-defined criteria, quality appraisal, GRADE grading. Missing from every LLM tool that treats "found 20 papers" as the same as "reviewed 20 papers."

Individually each shape is a specific research trade. Together they cover the modes that neither aggregation nor hypothesis-testing does.

## The stack, and how the pieces fit

The mental model:

- **`maximus-deep-research`** — aggregation. When the question is "what's the state of X?"
- **`maximus-deep-research-pro`** — hypothesis-first inference. When the question is "is thesis Y true, and what would falsify it?"
- **`maximus-investigative-research`** — narrative reconstruction. When the question is "what actually happened / who is really behind this?"
- **`maximus-literature-review`** — academic synthesis. When the question is "what does the peer-reviewed evidence say?"
- **`maximus-chain-of-verification`** — verification layer. Run before any of the above deliverables leaves the room.

CoVe is composable — it wraps any of the other four. Investigative and lit-review are complementary — you'd use investigative to reconstruct a real-world event and lit-review to synthesize the academic response to it.

## Design principles the skills share

Every one of the three ships with the same discipline:

- **Method visible alongside findings.** A reviewer or reader can see what was searched, what was excluded, what could not be confirmed. The workflow shape is the evidence.
- **Grade every claim.** High / medium / low or GRADE-scale confidence per finding, not per paper. Ungraded findings mislead.
- **Name what is not known.** Every output has an explicit gap section — "what we do not know," "cannot confirm," "what the literature does not answer." Gaps are findings.
- **Never invent a source.** Every citation is a URL that was actually re-fetched during the current workflow.
- **Never smooth a contradiction.** Contradictions between sources are surfaced as evidence, not averaged away.

The workhorse voice, applied to research.

## Where they live

- [`skills/maximus-chain-of-verification/`](../skills/maximus-chain-of-verification) — SKILL, README, HOWTO (6 recipes), two examples (single-report and list-question), three references, and a reference runner script that enforces context isolation.
- [`skills/maximus-investigative-research/`](../skills/maximus-investigative-research) — SKILL, README, HOWTO (6 recipes), two examples (entity investigation and event reconstruction), three references (source tiers, contradiction patterns, ethics and limits).
- [`skills/maximus-literature-review/`](../skills/maximus-literature-review) — SKILL, README, HOWTO (6 recipes), two examples (clinical RCT and ML methods), three references (PRISMA + GRADE, quality-appraisal tools, database coverage).

## Reach for them

Load `maximus-chain-of-verification` before any high-stakes factual deliverable leaves the room.

Load `maximus-investigative-research` when the request has investigative shape — leads, entities, events, sequences.

Load `maximus-literature-review` when the request is for an academic synthesis with defensible method.

Details live in the [README](../README.md).

— The workhorse works. Read before you edit. Verify before you send.
