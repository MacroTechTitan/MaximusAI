# Example — long-context recommendation

**User prompt (verbatim):**
> "I have a due-diligence pipeline that needs to read a full data room — roughly 800K tokens of PDFs and financial docs — and produce a memo. One-shot ideal. Which model?"

## Step 1 — Decision inputs

- **Task shape:** long-context single-pass extraction + synthesis
- **Context length:** ~800K tokens confirmed (asked user; not extrapolated)
- **Deployment:** hosted API OK
- **License:** no constraint
- **Cost sensitivity:** cost-aware but not cost-dominated (single-batch runs, not high-volume)

## Step 2 — Benchmark fit

At 800K tokens, the window itself is the discriminator. From `references/k3-benchmarks.md` and the K3 report §2:

- K3 context length: **1,048,576 tokens** — native.
- BrowseComp (agentic long-context browsing): K3 91.2 with context compaction at 300K, 90.4 with the full 1M and no compaction ([Kimi K3 report](https://github.com/MoonshotAI/Kimi-K3)).
- OmniDocBench (document-heavy vision + text): K3 91.1 — best in the reported set.
- ResearchRubrics (long-form research synthesis): K3 76.2 vs. GPT-5.6 Sol 73.8 vs. CF5 not reported.

Claude Fable 5 and GPT-5.6 Sol do not publish comparable native-1M benchmarks in the K3 report table. If they have larger windows in a subsequent release, this recommendation should be refreshed.

## Step 3 — Constraints

- **Retrieval alternative:** could the pipeline chunk to 300K + retrieval? If yes, cost drops and the recommendation may flip. Ask.
- **Preserved-thinking:** single-turn workload — preserved-thinking overhead does not apply here (see `references/preserved-thinking-cost.md`).
- **License:** no constraint per the user, so K3 License terms are OK.

## Step 4 — Recommendation

## Recommendation
Kimi K3 with the full 1M-token context, single-turn, `reasoning_effort=max`.

## Why this one
- K3's native 1M window is the only frontier model in the K3 report that fits 800K in one shot without compaction ([Kimi K3 report §2](https://github.com/MoonshotAI/Kimi-K3)).
- OmniDocBench 91.1 (best in reported set) — supports PDF-heavy input.
- BrowseComp 90.4 at full 1M no-management confirms the model actually uses the window rather than degrading.
- ResearchRubrics 76.2 supports the synthesis half of the task.

## Why not the runner-up
- GPT-5.6 Sol has strong reasoning benchmarks but no comparable published 1M-context number in the K3 report; you would be extrapolating past documented behavior.
- Claude Fable 5 lands strong on many benches but does not publish a comparable 1M single-shot number in the K3 report. If Anthropic ships that data, revisit.

## Watch-outs
- Cost per run at 800K input is material. Get a price quote from platform.kimi.ai before committing to volume.
- If chunking + retrieval is acceptable, most frontier models can do the job for less. Ask whether one-shot is truly required.
- License: K3 is source-available under the Kimi K3 License; if this pipeline is ever wrapped as a hosted product for third parties, get legal review.

## Ask-back
Is one-shot truly required, or would 300K chunks + retrieval + a final synthesis pass work? If chunking is OK, the recommendation may flip to a cheaper model.

---

## Notes on how this trace was built

- The 800K figure came from the user, not from assumption. If the user had said "a lot of documents," step 1 would have blocked on getting an actual token count.
- The recommendation named the specific benchmark (native 1M window + BrowseComp at 1M no-management) rather than "K3 has a long context."
- The ask-back invites the user to relax the hardest constraint (one-shot). Often the answer is "actually chunking is fine," which changes the recommendation.
- Preserved-thinking cost was explicitly noted as *not applicable* — the skill should call out when a known caveat does not apply, so the recommendation is complete.
