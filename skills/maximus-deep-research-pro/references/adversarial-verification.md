# Reference — Adversarial Verification Protocol

The single step most likely to be skipped under time pressure, and the single step whose omission most reliably produces a confidently wrong deliverable. This reference makes the protocol concrete enough that skipping it requires a deliberate choice, not a drift.

## The core rule

For every claim that will enter the confidence ledger above "low," run at least one search query specifically engineered to surface evidence *against* the claim — not a neutral rephrase, not a second search for more of the same confirming evidence. The query's job is to try to break the claim. If it can't, the claim earns its tier. If it can, the tier drops and the finding gets recorded, not argued away.

## Why a confirming rephrase doesn't count

Searching "prompt caching cost savings" and then "prompt caching cost reduction benefits" is one search wearing two outfits — both retrieve the same confirming content, because both are phrased from the confirming frame. The adversarial query has to invert the frame: "prompt caching limitations," "prompt caching doesn't work," "prompt caching worst case." Different frame, different index results, different chance of actually surfacing disconfirmation if it exists.

## Falsifiability query patterns

Use these as templates. Swap in the specific claim's subject and predicate.

| Claim shape | Confirming query (insufficient alone) | Adversarial query (required) |
|---|---|---|
| "[X] achieves [metric]" | "[X] [metric] results" | "[X] [metric] limitations" / "[X] [metric] failure" / "[X] doesn't achieve [metric]" |
| "[Company] hit [financial milestone]" | "[Company] [milestone] announcement" | "[Company] layoffs" / "[Company] revenue miss" / "[Company] skeptic OR critic" |
| "[Event Y] caused [Outcome Z]" | "[Event Y] [Outcome Z] connection" | "[Outcome Z] alternative explanation" / "[Outcome Z] analysts attribute to" |
| "[Person] has [claimed credential/track record]" | "[Person] [credential] background" | "[Person] controversy" / "[Person] lawsuit" / "[Person] previous venture failure" |
| "[Approach] works at scale" | "[Approach] scalability benchmark" | "[Approach] doesn't scale" / "[Approach] production issues" / "[Approach] postmortem" |
| "[Consensus claim] is broadly accepted" | "[Claim] expert support" | "[Claim] dissent" / "[Claim] criticized" / "[Claim] disputed" |

## Protocol steps

1. **Identify the claim's failure condition before searching.** Ask: "what would have to be true for this claim to be false or overstated?" Write that condition down — it's the target of the adversarial query, not an afterthought.
2. **Write the adversarial query from the failure condition, not from the claim.** If the claim is "X saves 90% cost," the failure condition is "hit rate is much lower than assumed in typical production traffic" — the query targets that condition directly.
3. **Run the query and actually read what comes back**, not just scan for confirmation that nothing came up. A quiet result set is itself a data point (see negative evidence in `references/inference-patterns.md`), but only if the query was genuinely capable of surfacing a contradiction had one existed.
4. **Classify the result:**
   - **Clear contradiction found** — go to "On a genuine contradiction" below.
   - **Partial/conditional contradiction** — the claim holds under some conditions and not others. Narrow the claim's scope rather than keeping it as originally stated (see the caching example in `examples/hypothesis-falsification-trace.md`).
   - **No contradiction found, and the query was well-targeted** — the claim earns its tier; record "none found after adversarial pass" in the ledger.
   - **No contradiction found, but the query was weak or the topic is under-covered online** — do not treat this as confirmation. Flag it as a gap (unknown-public or unknown-could-probe-with-X) rather than silently upgrading confidence.

## On a genuine contradiction: revise, don't defend

This is the discipline that separates this skill from motivated reasoning wearing a research process as a costume.

**Do:**
- Update the claim's confidence tier downward immediately.
- Record the counter-evidence in the ledger's `counter_evidence` field, with its source.
- Revise the claim's scope if the contradiction is conditional (works under A, not under B) rather than total.
- If the contradiction is severe enough to undermine the whole hypothesis, loop back to Step 1 (Frame Hypothesis) with a revised, more accurate framing — this is a normal and expected outcome of the loop, not a sign the research failed.

**Do not:**
- Search for a fourth source to "outvote" the contradiction without first checking whether the contradicting source is actually more credible or more directly on-point than the confirming ones.
- Bury the counter-evidence in a footnote while keeping the headline claim and tier unchanged.
- Rationalize the contradiction away with an unverified explanation ("that report is probably outdated") unless you actually verify the recency/relevance claim you're using to dismiss it.
- Treat "I found one contradicting source" as automatically decisive either — weigh it the same way you'd weigh any source: tier, independence, recency, relevance. A single low-tier contradicting blog post doesn't automatically override two primary sources; it does automatically mean the claim is no longer "no counter-evidence found."

## When adversarial verification is most likely to be skipped (and why that's costly)

- **Time pressure near the end of a research session** — the first-pass answer feels done. This is exactly when skipping the pass is most tempting and most dangerous, because the deliverable is about to ship on an unstress-tested conclusion.
- **When the first-pass evidence came from multiple sources** — the researcher (human or agent) mistakes source *count* for source *independence* and *stress-testedness*. Multiple sources repeating one original claim is still one claim.
- **When the claim is emotionally or narratively satisfying** — a clean, decisive-sounding conclusion is more pleasant to write than a hedged, conditional one. That pleasantness is not evidence of correctness; if anything, treat a suspiciously clean conclusion as a signal to look harder for the adversarial case.

## Minimum bar

No claim enters the final deliverable at "medium" or "high" confidence without at least one adversarial query having been run and its result recorded in the ledger. If time or budget runs out before every claim gets its adversarial pass, the unrun claims get capped at "low" and the gap is stated explicitly — the cap is not a punishment, it's an honest reflection of what was actually checked.
