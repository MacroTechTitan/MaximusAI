# CoVe in high-stakes domains — clinical, legal, financial

CoVe is the same 4-phase workflow everywhere. What changes in high-stakes domains is **what counts as a valid verification source** and **what happens when verification fails**.

## Clinical

**Valid verification sources (in priority order):**
1. Peer-reviewed publications (PubMed, journal websites)
2. FDA / EMA / equivalent regulatory guidance
3. Clinical practice guidelines from major medical societies (AHA, ACC, NCCN, etc.)
4. Cochrane systematic reviews
5. WHO or national health authority publications

**Not valid:**
- Wikipedia
- Blog summaries of research
- Manufacturer marketing materials
- News articles summarizing studies (the study itself is valid; the article is not)
- LLM training-knowledge-only ("I know that…")

**Verification-failure policy:** unsupported clinical claims are **cut**, not softened. No "reportedly effective" or "appears to reduce." Either verified against a valid source or removed.

## Legal

**Valid verification sources:**
1. Primary sources — statutes, regulations, case law from official databases (PACER, Westlaw citation confirmed, state court sites)
2. Bar-authored practice guides (state bar publications)
3. Peer-reviewed law review articles (secondary but often necessary for interpretive claims)
4. Court-issued opinions with docket numbers

**Not valid:**
- Blog posts summarizing law
- LLM training knowledge (case law changes; training knowledge is stale by definition)
- Marketing sites for law firms

**Verification-failure policy:** unsupported legal claims are cut. Softening a legal claim ("may be enforceable") without a source is itself a professional-responsibility risk in some jurisdictions.

## Financial

**Valid verification sources:**
1. SEC filings (EDGAR)
2. Audited annual reports
3. Company IR pages for stated figures
4. Major-outlet financial reporting (Bloomberg, Reuters, WSJ, FT) for market-color claims
5. Regulatory databases (FINRA BrokerCheck, IAPD)

**Not valid:**
- Analyst estimates presented as facts
- Company forward-looking statements presented as guidance without the "guidance" caveat
- Social media / X posts
- LLM training knowledge for anything more recent than the model's cutoff

**Verification-failure policy:** unsupported financial claims are cut or clearly labeled as estimate/opinion. Never present an unverified figure as a fact — the recipient may act on it.

## Journalistic

**Valid verification sources:**
- Primary: original documents, on-the-record interviews, official announcements
- Multiple independent secondary sources for the same claim
- Reputable outlets (per your outlet's own source standards)

**Verification-failure policy:** single-sourced claims flagged clearly. Anonymous-sourced claims require higher independent corroboration.

## Competitive intelligence (external-delivery briefs)

**Valid verification sources:**
- Public financial filings (SEC, Companies House, equivalents)
- Official product announcements
- LinkedIn for personnel changes (with the caveat that LinkedIn is user-updated and can lag)
- Analyst reports where cited by outlet, not aggregated

**Verification-failure policy:** external CI briefs get "high confidence only." Cut everything else or move it to an "unverified signals" appendix that is clearly labeled.

---

## The universal rule for high-stakes domains

**"Cannot confirm" is a first-class outcome.** The model's training knowledge, however plausible, does not count as verification. Independent-source verification is the whole point of CoVe. If no valid source exists, the claim does not survive the pass.

**"Softening" is dangerous.** Rewriting "X causes Y" to "X may cause Y" without a source does not make the claim safer — it makes it less accountable. In clinical and legal contexts, this is a specific known anti-pattern.

Last reviewed: **2026-07-31**.
