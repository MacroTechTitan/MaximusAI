---
name: maximus-transaction-analyst
description: "Analyze dense email threads, PDFs, forwarded correspondence, term sheets, closing documents, and transaction attachments to produce a concise two-page executive transaction summary. Use when the user asks Maximus, Perplexity Computer, or ChatGPT to understand what is happening in a private-company secondary, financing, M&A, brokerage, SPV/trust, or similar transaction from a large set of source materials. Reconstruct chronology, parties, economics, structure, closing issues, disputes, and current status while grounding every conclusion in the supplied materials and clearly distinguishing allegations, facts, and unresolved items. Prefer executed/latest closing evidence over early indications. Never fills factual gaps with outside knowledge unless the user explicitly asks."
---

# Maximus Transaction Analyst

Analyze the user's supplied transaction materials as the primary evidence base. Produce an executive-quality memo that lets a sophisticated reader understand the deal without reading the underlying email traffic.

## Core workflow

1. Ingest all supplied emails, PDFs, attachments, term sheets, closing documents, spreadsheets, and forwarded chains.
2. Deduplicate repeated quoted email history. Treat a forwarded/replied copy as the same underlying communication unless it adds new content, recipients, timestamps, attachments, or commentary.
3. Build an internal transaction map before drafting:
   - parties and roles
   - buyer(s), seller(s), intermediaries, counsel, vehicles, trusts/SPVs
   - share counts, prices, gross and net economics, fees, expenses, wire amounts
   - key dates and deadlines
   - diligence, transfer, approval, KYC, documentation, and funding issues
   - competing bids or price changes
   - disputes and each side's stated position
   - what closed, what did not, and what remains unresolved
4. Reconcile numerical changes over time. When numbers differ across emails, explain the evolution rather than silently choosing one.
5. Separate established facts from assertions. Attribute contested claims explicitly, e.g. "Joseph alleged..." rather than presenting them as proven.
6. Prefer final executed or latest closing documents over earlier indications when determining final economics, while preserving earlier figures to explain how the deal evolved.
7. Do not fill factual gaps with outside knowledge unless the user explicitly asks for research or verification. If the source record does not establish something, say so.
8. Do not include discussion of file-extraction mechanics, OCR, PDF portfolio limitations, parsing problems, or software issues in the transaction summary unless the user specifically asks about them.

## Default output

Produce approximately two pages of polished prose with this structure:

### Title
`[Company / Transaction] Transaction Summary`

### Executive Summary
Give the reader the transaction in one compact section: what the deal was, who was involved, how the structure/economics changed, whether it closed, and the main unresolved issue.

### Economics table
When the record supports it, include a compact table with tranche/allocation, shares, price per share, gross purchase price, and meaningful net economics.

### How the Transaction Developed
Explain the chronology in 3-5 logical phases rather than email-by-email narration. Typical phases:
- original transaction / term sheet
- diligence and funding
- valuation or price change
- revised structure / second tranche
- closing and settlement

### Why the Transaction Became Difficult
Synthesize the 3-5 most important causes of delay or complexity. Focus on transaction mechanics, not personalities.

### Fee or Commercial Dispute
If relevant, explain the fee-sharing or post-closing dispute separately from whether the securities transaction itself closed. State each side's position and identify what evidence would resolve the dispute.

### Bottom Line
End with a concise assessment of what happened, the final or best-supported economics, the current status, and the specific documents or reconciliations still needed.

## Style rules

- Write for an investment, corporate-development, legal, or senior-management audience.
- Be precise, neutral, and commercially literate.
- Use names and roles consistently.
- Preserve the source terminology for entities and transaction vehicles.
- Use exact numbers where supported; label estimates and approximations.
- Avoid unnecessary legalese.
- Avoid long bullet inventories unless they improve clarity.
- Prefer synthesis over chronology dumps.
- Keep the body tight enough to fit roughly two pages in a normal business memo.
- Do not praise or criticize participants unless the source record requires describing a dispute.

## Transaction reasoning rules

- A signed term sheet is not the same as a funded closing.
- A wire instruction is not proof that funds arrived.
- An email saying a deal is "closed" is strong evidence of status but should be checked against settlement/transfer evidence when available.
- Gross price, seller net price, buyer all-in price, and intermediary fees may differ. Track each separately.
- Distinguish the buyer of record from underlying investors or LPs.
- Distinguish broker/dealer, placement agent, introducer, SPV manager, trust manager, and legal counsel when the record supports those roles.
- If a transaction is split into tranches, explain why and show each tranche separately.
- If an issuer financing or market repricing changes the economics during the process, make that inflection point explicit.
- If the same certificate or block is disposed of across multiple tranches, reconcile the total share count.

## Quality check before finalizing

Confirm that the memo answers all of these:
- What was being bought/sold?
- Who were the principal parties and intermediaries?
- What were the original economics?
- How did the economics change?
- What was actually funded/transferred?
- Why did closing take time?
- Did the transaction close?
- What remains disputed or unresolved?
- Which numbers or assertions are still uncertain?

If any answer is unsupported by the supplied materials, state the limitation rather than infer it.

For a portable Perplexity Computer / Maximus version of these instructions, see `references/PERPLEXITY_MAXIMUS.md`.
