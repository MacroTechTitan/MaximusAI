# HOWTO — maximus-chain-of-verification

Six recipes for the CoVe patterns that come up most.

---

## Recipe 1 — Verify a research report before publishing

**Trigger:** "run CoVe on this report" / "fact-check this before I send"

**Steps:**
1. Load the draft into the agent's context.
2. Phase 2 — extract every verifiable claim, generate 1–3 independent questions per claim.
3. Phase 3 — spawn one sub-agent per question (or clear context between answers). Each sub-agent gets **only the question**, not the draft. Sub-agent uses search / fetch / connectors to answer.
4. Phase 4 — merge answers back. Revise the draft. Produce the ledger.

**Typical outcome:** 15–25% of numeric claims come back "revised" (close-but-wrong figures corrected), 5–10% come back "removed" (unsupported), the rest confirm.

---

## Recipe 2 — Verify a list-based answer

**Trigger:** "list the top 10 X" / "who are the largest Y" / "name all Z"

**Why this recipe matters:** List answers historically hallucinate at the highest rate. The [Dhuliawala et al. paper](https://arxiv.org/abs/2309.11495) reports biggest gains on list-based questions.

**Steps:**
1. Generate the list in the draft.
2. For each list item, generate one verification question — "is X actually a member of the set?"
3. Answer each in isolation with a fresh search.
4. Revise: drop unverified items, add any items the verification pass surfaced that were missing.

**Typical outcome:** Original lists often lose 20–40% of items and gain 10–20% new ones.

---

## Recipe 3 — Verify inline citations in a synthesis

**Trigger:** "check that these citations actually support the claims"

**The bug this catches:** Citation drift. The draft cites Paper A for a claim actually stated by Paper B. Common in `maximus-deep-research` and `maximus-literature-review` outputs.

**Steps:**
1. For each `[source](url)` in the draft, generate the question: "Does the source at [url] actually state [claim]?"
2. Fetch each URL freshly (do not rely on the draft's summary).
3. Match the claim against the source's actual content.
4. Revise: correct citations, remove unsupported claims, add missing citations where a claim is stated but not attributed.

---

## Recipe 4 — Verify a numeric claim in isolation

**Trigger:** "verify this number" / "is this figure right?"

**Steps:**
1. Extract the number and its full attribution ("K3 scored 42.0 on SWE-Marathon per the K3 tech report").
2. Generate a single verification question: "What score did K3 achieve on SWE-Marathon according to the K3 tech report?"
3. Answer in isolation, source-first.
4. Compare. Revise if different.

**Fast recipe** — use when the rest of the draft is already trusted and you just want one number checked.

---

## Recipe 5 — Verify a competitive-intel brief before external delivery

**Trigger:** post-run on `maximus-deep-research` or `maximus-counterparty-discovery` output

**Why this is mandatory:** External-delivery briefs get quoted back. A single hallucinated financial figure or org-chart claim damages credibility.

**Steps:**
1. Extract every load-bearing claim: revenue figures, funding rounds, headcount, exec names, market share, product features.
2. Independent verification per claim. Prefer primary sources (SEC filings, official announcements, LinkedIn for headcount).
3. Any claim below "high" confidence → soften or cut. External briefs get "high" or nothing.
4. Ship with the ledger attached as an appendix so the recipient sees the discipline.

---

## Recipe 6 — Verify a clinical or legal claim

**Trigger:** healthcare or legal domain, any claim that could inform a decision

**Steps:**
1. Extract each factual claim.
2. Verification questions must resolve to a primary source: peer-reviewed publication, case law, regulatory filing, official guideline. Blog summaries do not count.
3. Answer in isolation. If no primary source can be found, the claim is "cannot confirm."
4. Revise: unsupported claims are cut, not softened. Clinical and legal deliverables have zero tolerance for "reportedly."

**See `references/high-stakes-domains.md` for domain-specific verification-source rules.**

---

## When to bypass this skill

- Draft is entirely opinion, framing, or subjective judgment → nothing to verify
- One-sentence factual lookup → just re-search directly
- Already ran CoVe this session → do not re-run unless new claims appeared
- Casual conversation → CoVe is expensive; do not spend the tokens
