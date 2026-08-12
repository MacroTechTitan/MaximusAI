# HOWTO — maximus-investigative-research

Six recipes for the investigative patterns that come up most often.

---

## Recipe 1 — Investigate a private company

**Trigger:** "dig into [private company X]" / "what's going on with [pre-IPO startup Y]"

**Source stack:**
- Primary: state incorporation filings, USPTO patents, trademark filings, Companies House (UK), corporate blog, official press releases, LinkedIn (for headcount trends), Glassdoor (as a signal, not a fact source), job postings
- Secondary: reputable outlet coverage, named analyst reports, industry newsletters
- Adversarial: litigation records (PACER, state courts), former-employee reviews (as leads, not conclusions), competitor filings, short-thesis writeups (rare for private)

**Timeline anchors:**
- Founding date, funding rounds (Crunchbase / PitchBook / press releases), leadership changes, product launches, litigation dates, hiring inflection points

**Contradiction hunt questions:**
- Does the founding story match the state filing dates?
- Do headcount claims match LinkedIn / Glassdoor / job-posting volume?
- Do announced customers match public case studies or press coverage?

---

## Recipe 2 — Reconstruct an event or incident

**Trigger:** "what actually happened with [event]" / "walk me through the sequence"

**Source stack:**
- Primary: official incident reports, court records, regulatory filings (SEC 8-K, NTSB, OSHA, etc.), agency press releases, timestamped social media from the entity
- Secondary: contemporaneous reporting from multiple outlets, wire-service reports
- Adversarial: competitor filings if relevant, plaintiff / defendant filings if litigation exists

**Timeline construction:**
- Every event gets a specific date **and time** where available (many incidents turn on hours-level ordering)
- Contradicting dates from different sources → both entries with "conflict" flag
- Cross-check: does the entity's official statement match contemporaneous reporting?

**Contradiction hunt:**
- Does the official story match the timeline reconstructed from public records?
- Did the entity's statement change over time? (Compare press releases from t+0, t+1 week, t+1 month)
- Are there court filings that describe the event differently than the press release?

---

## Recipe 3 — Fact-check a viral claim

**Trigger:** "is this claim true" / "fact-check this story" / "was that stat real"

**Source stack:**
- Primary: the original source the claim traces back to (paper, filing, dataset, statement)
- Secondary: reputable outlet coverage
- Adversarial: fact-check outlets (Snopes, Politifact, Reuters Fact Check, AP Fact Check) — read for context but do not defer

**Method:**
1. **Trace back to origin.** Where did this claim first appear? A viral tweet? A study? A press release?
2. **Re-fetch the original.** Read the primary source in full. Does it actually say what the viral version claims?
3. **Compare:** does the viral version match the source's actual wording? Missing caveats? Cherry-picked numbers?
4. **Corroborate:** do independent sources support the same claim?
5. **Report** with the primary source, the viral version, and the delta between them.

**Common findings:** "Up to X" reported as "X exactly." Correlation reported as causation. Preprint reported as peer-reviewed. Anonymous claim laundered through a secondary outlet.

---

## Recipe 4 — Trace a claim back through citation chain

**Trigger:** "where did this stat come from" / "who first said X" / "trace the source"

**Method — the citation-chain walk:**
1. Take the claim as it appears in the user's source.
2. Note the citation attached to it.
3. Fetch the cited source. Does it actually state the claim, or does it cite yet another source?
4. If it cites another source, repeat.
5. Continue until you reach either (a) a primary source stating the claim originally, or (b) a dead end (broken link, retracted paper, unattributed statement).

**Common findings:**
- Claim traces back to a preprint that has since been contradicted
- Claim traces back to a press release, not a study
- Claim traces back to a source that says something materially different
- Claim has no traceable origin (fabricated or unsourced)

---

## Recipe 5 — Investigate a person's public track record

**Trigger:** "look into [named public figure]" / "background check [named person]"

**Not for:** private individuals, personal data, personal contact info, family members. Public figures only, on public-record activity only.

**Source stack:**
- Primary: SEC Form D / Form 3-4-5 (for execs at public co's), FEC filings (for political contributions), court records where they are a named party, published writings, official corporate bios, verified interviews
- Secondary: reputable-outlet profiles
- Adversarial: litigation where they are a defendant, critical coverage, industry-specific critical outlets

**Method:**
1. Establish the person's public identity: current role, prior roles, education, verified accounts
2. Timeline of public activity: roles, filings, statements, litigation
3. Contradiction hunt: do their public statements at different points contradict each other? Do their filings match their public claims?
4. Corroboration: are there independent sources confirming each claim in their bio?

**Never:** dig into private life, family, undisclosed addresses, financial data outside public filings, or use breached data.

---

## Recipe 6 — Investigate a supply chain, ownership chain, or corporate structure

**Trigger:** "who really owns [entity]" / "trace the ownership chain" / "map the supply chain for X"

**Source stack:**
- Primary: incorporation filings (state, Companies House, OpenCorporates), UBO / beneficial-ownership registries where public, trade filings (import/export records via Panjiva or public trade data), procurement records
- Secondary: investigative outlet coverage (ICIJ, OCCRP, ProPublica for structural investigations)
- Adversarial: sanctions lists (OFAC, EU consolidated), sanctions-adjacent enforcement actions

**Method:**
1. Start with the entity in question.
2. Pull incorporation filings — who are the officers, directors, registered agent?
3. Trace each officer / director back — are they officers of other entities?
4. Build the ownership graph.
5. Cross-check against sanctions lists and enforcement actions.
6. Report the graph with source per edge and flag any sanction hits.

---

## When to bypass this skill and use a sibling

- **Just want a topic summary** → `maximus-deep-research`
- **Just want to test a specific thesis** → `maximus-deep-research-pro`
- **Need a structured counterparty export** → `maximus-counterparty-discovery`
- **Need to find a person to reach out to** → `maximus-people-finder`
- **Need academic literature synthesis** → `maximus-literature-review`
