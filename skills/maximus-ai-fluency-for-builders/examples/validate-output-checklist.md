# Example: Validate AI Output Checklist

A reusable checklist for validating AI-generated output without re-doing the work. Use this after any significant AI delegation.

---

## How to use this checklist

Run through the relevant sections for your output type. Mark each item ✓ (pass), ✗ (fail), or N/A.

A single ✗ in Section 1 (structural) means rerun. Two or more ✗ in Section 2 (factual) means the output is not trustworthy — rerun with more specific constraints.

---

## Section 1: Structural check (run first, ~1 min)

These checks don't require domain knowledge. Run them before reading the content.

- [ ] **Format matches spec**: Correct number of sections/items? Right output format (table, list, prose)? Correct length?
- [ ] **No hallucinated structure**: No extra columns, sections, or items that weren't requested?
- [ ] **Completeness**: All requested sections are present (no "TBD" or "[placeholder]" in the output)?
- [ ] **No self-references**: Output doesn't refer to itself as an AI or hedge with "As an AI, I..."?

**If any item fails**: The output is structurally wrong. Rerun with a more explicit format constraint before doing any factual checking.

---

## Section 2: Factual check — research output (~3–5 min)

Pick 3 specific factual claims at random (not the ones you already know are true — specifically the ones you don't know). Verify each against the primary source.

- [ ] **Claim 1**: [claim] → Source URL: [url] → Verified: yes / no
- [ ] **Claim 2**: [claim] → Source URL: [url] → Verified: yes / no
- [ ] **Claim 3**: [claim] → Source URL: [url] → Verified: yes / no

**If 0/3 wrong**: Output is trustworthy. Proceed.
**If 1/3 wrong**: Fix the error. Spot-check 2 more claims in the same topic area.
**If 2+/3 wrong**: Output is not trustworthy for this topic. Rerun with more constraints or a different approach.

**Citation check**:
- [ ] All cited URLs are real (open in a browser without 404)?
- [ ] All cited URLs support the specific claim they're cited for (not just tangentially related)?

---

## Section 3: Factual check — code output (~2–3 min)

- [ ] **Runs without errors**: Execute the code. Does it run? (If not, fix before anything else.)
- [ ] **Handles the primary case**: Does it produce the expected output for the main use case?
- [ ] **Edge case 1**: [your edge case] — does it handle it correctly?
- [ ] **Edge case 2**: [your edge case] — does it handle it correctly?
- [ ] **No invented APIs**: Check every non-trivial library call against the actual docs. Hallucinated methods are the most common AI coding failure.
- [ ] **No security issues**: For any code that handles user input, external data, or secrets: is it safe?

---

## Section 4: Copy / prose check (~2 min)

- [ ] **Read aloud**: Read the entire output aloud. Does it flow naturally? Does it sound like you (or your brand)?
- [ ] **No generic AI filler**: No "In conclusion", "It's worth noting", "Certainly!", "As mentioned above", or "As an AI language model."
- [ ] **Tone match**: Does the tone match the brief (formal/casual/technical/conversational)?
- [ ] **Core claim intact**: Is the main point still the main point, or did the model drift away from it?

---

## Section 5: Plan / spec output (~3 min)

- [ ] **All steps are actionable**: Each step has a clear deliverable. No vague steps like "Research options."
- [ ] **Dependencies are correct**: Steps that depend on earlier steps are ordered correctly.
- [ ] **Blockers are surfaced**: Unknown dependencies, waiting-on-others items, or risks are explicitly flagged.
- [ ] **Scope matches intent**: The plan solves the problem you actually have, not a related but different problem.

---

## Iteration decision framework

| Check result | Action |
|---|---|
| All structural checks pass, all sample facts correct | Accept. Note the prompt pattern for reuse. |
| Structural failure | Rerun with explicit format constraint. Don't iterate on content yet. |
| 1 factual error | Fix the specific error. Accept the rest. |
| 2+ factual errors | Rerun. The original request was under-specified. |
| Code doesn't run | Paste the error back and ask for a fix. One round. |
| Code runs but wrong behavior | Provide the specific failing case. Ask for a targeted fix. |
| Copy sounds wrong | Edit voice yourself. Don't re-prompt for voice — you'll spend more time prompting than editing. |

---

## Notes field (fill in after validation)

```
Output type: 
Date: 
Prompt pattern used: 
Validation result: 
Errors found: 
Time to validate: 
Prompt pattern worth saving? Y/N
```
