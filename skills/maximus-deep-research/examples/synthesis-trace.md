# Worked Example — Synthesis Mode

**Research question:** "What's actually driving the recent wave of stablecoin regulation in the US and EU, and how do the two approaches differ?"

This trace shows the fan-out plan, source collection, dedup, cross-verification, and final synthesis. It is illustrative of the *process* — treat any figures below as representative of the method, not as a substitute for running the searches fresh at the time of use.

## 1. Frame

One-sentence goal: explain what triggered US and EU stablecoin regulation and how the two regimes differ in structure.

Sub-questions:
1. What specific events triggered regulatory attention (US)?
2. What is the substance of the US approach (legislation, agencies involved)?
3. What is the substance of the EU approach (MiCA or successor framework)?
4. Where do the two regimes materially diverge (reserve requirements, issuer eligibility, enforcement)?

Done = a short synthesized answer, each claim cited, disagreements between sources flagged rather than smoothed over.

## 2. Fan-out plan (parallel queries)

Batch 1 (`search_web`, 3 queries in parallel):
- "US stablecoin regulation 2026 legislation"
- "stablecoin collapse triggered regulation"
- "GENIUS Act stablecoin"

Batch 2 (`search_web`, 3 queries in parallel):
- "EU MiCA stablecoin rules"
- "EU stablecoin reserve requirements"
- "MiCA e-money token issuer"

Batch 3 (`search_web`, 2 queries, comparative/recency):
- "US vs EU stablecoin regulation differences"
- "stablecoin regulation 2026"

This is fan-out-before-narrowing: eight short queries across three batches before reading anything deeply, rather than one query followed immediately by a single source.

## 3. Candidate sources collected (12 after initial triage)

| # | Source | Tier | Role |
|---|---|---|---|
| 1 | US Treasury / agency statement on stablecoin oversight | Primary | Regulatory intent, US |
| 2 | Full text or official summary of US stablecoin legislation | Primary | US legal substance |
| 3 | Federal Reserve public remarks on payment stablecoins | Primary | US rationale |
| 4 | Official EU MiCA regulation text (EUR-Lex) | Primary | EU legal substance |
| 5 | European Banking Authority guidance on e-money tokens | Primary | EU enforcement detail |
| 6 | Reuters/Bloomberg coverage of US legislation passage | Secondary | US timeline, context |
| 7 | Financial Times coverage of MiCA implementation | Secondary | EU timeline, context |
| 8 | Major press coverage of a stablecoin de-peg event | Secondary | Trigger event |
| 9 | Analyst report (e.g., law firm client alert) comparing US/EU regimes | Secondary | Comparative framing |
| 10 | Industry association commentary on compliance burden | Secondary | Industry reaction |
| 11 | Aggregator blog summarizing "stablecoin rules explained" | Tertiary | Framing/leads only |
| 12 | Crypto news site quoting an unnamed "industry source" | Tertiary | Discarded as unsupported |

## 4. Dedup

Sources 6, 7, and 10 substantially repeat the same three facts (legislation name, effective date, reserve requirement threshold) already stated more authoritatively in sources 1-5. Collapsed: cite the primary source for the fact itself, cite secondary press only for context/reaction the primary source doesn't cover (market response, industry sentiment).

Source 11 (tertiary aggregator) added no fact not already found in a primary or secondary source — dropped from citation list, used only to confirm nothing was missed.

Source 12 discarded per anti-pattern: unnamed source, no independent corroboration, tertiary tier. Not used to support any claim.

## 5. Cross-verify (the claims the answer leans on)

- **Claim:** "The US framework requires 1:1 reserve backing in cash or short-term Treasuries." Verified against the primary legislative text (source 2) and confirmed by an independent secondary summary (source 9) — two independent sources, one primary. Cross-verified.
- **Claim:** "MiCA caps large e-money tokens' transaction volume in certain circumstances." Verified against EBA guidance (source 5) and EUR-Lex text (source 4) — both primary, consistent. Cross-verified.
- **Claim:** "A specific de-peg event was the proximate trigger for accelerated US legislative action." Sources disagree on how much weight to give this versus longer-running regulatory concern predating the event — noted as a disagreement rather than resolved artificially.

## 6. Synthesize (illustrative excerpt)

"US and EU stablecoin regimes both converge on requiring high-quality liquid reserves, but diverge sharply on issuer eligibility: the US framework permits both bank and qualified nonbank issuers under federal or state oversight, while the EU's MiCA framework routes issuance primarily through licensed e-money or credit institutions and imposes volume-based restrictions on 'significant' tokens that the US framework does not mirror. Commentators are split on how much a single de-peg event accelerated US legislative timing versus longer-standing regulatory intent — the primary sources do not resolve this, so it's presented here as an open question rather than settled fact."

Every sentence in the actual deliverable would carry an inline citation to the specific fetched source (e.g., the EUR-Lex text, the legislation text, the named press outlet) — omitted here only because this file is illustrating method, not reporting live findings.

## 7. What this trace demonstrates

- Fan-out happened in batches of parallel, short, single-angle queries — not one compound query.
- 12 sources were collected before any claim was finalized; only 6-7 survived dedup as citation-worthy.
- Two claims were explicitly cross-verified against independent, higher-tier sources before being stated as fact.
- One disagreement between sources was preserved as a disagreement rather than resolved by picking whichever source sounded more confident.
