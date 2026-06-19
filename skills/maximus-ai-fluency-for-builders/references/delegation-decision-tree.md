# Reference: Delegation Decision Tree

A structured decision framework for determining whether to delegate a task to AI, and if so, to which tool.

---

## Step 1: Should you delegate this at all?

Answer the three qualifying questions:

1. **Can AI do this at acceptable quality?**
   - AI is strong at: research synthesis, structured writing, code generation, summarization, extraction, classification, translation, analysis.
   - AI is weak at: tasks requiring real-time data it doesn't have, tasks requiring your specific business judgment, tasks where the output can't be verified, creative tasks where your voice is the point.

2. **Can I validate the output in under 20% of the time saved?**
   - If validating takes longer than doing the task yourself, delegation isn't worth it.
   - Code: run the tests (fast). Research: spot-check 3 claims (fast). Copy: read aloud (fast). Complex business decisions: hard to validate (slow).

3. **Is the task well enough specified to delegate?**
   - Can you write the Context / Goal / Constraints / Verification hook in under 5 minutes?
   - If you can't specify it in 5 minutes, it's probably not specified enough for AI to do it well either.

**If all three: yes** → proceed to Step 2.
**If any: no** → do the task yourself, or do only a sub-task with AI.

---

## Step 2: Which tool?

```
Is this a single-fact lookup or a current-events question?
  └── YES → Perplexity search (fast, well-sourced for current info)
  └── NO ↓

Is this a multi-source research synthesis or a multi-step analysis?
  └── YES → Perplexity Computer (deep research mode or agentic)
  └── NO ↓

Is this a code edit inside an existing codebase?
  └── YES → Cursor (repo context) or Computer with bash/edit tools
  └── NO ↓

Is this a long document review (>20 pages)?
  └── YES → Computer (large context window)
  └── NO ↓

Is this iterative copy or creative writing where you'll go back and forth?
  └── YES → Computer or Claude (conversation memory, good instruction-following)
  └── NO ↓

Is this structured data extraction (JSON schema, table fill)?
  └── YES → Computer with a schema prompt (or API call with structured output mode)
  └── NO ↓

Is this an image?
  └── YES → Computer media skill
  └── NO ↓

Default: Perplexity Computer
```

---

## Step 3: Which prompt pattern?

| Task type | Prompt pattern | Key elements |
|---|---|---|
| Research | "Find N sources on [topic]. For each: [columns]. Cite URLs." | N constraint, column spec, URL requirement |
| Planning | "Produce a numbered plan for [goal]. Each step: what/why/verify. Flag blockers." | Numbered steps, verify field, blocker field |
| Drafting | "Write a [format] for [audience] achieving [goal]. Tone: [adj]. Max [N] words. Exclude: [X]." | Audience, goal, tone, length, exclusion |
| Code | "Implement [function]. Signature: [sig]. Test case: [test]. Error seen: [error]." | Exact signature, failing test, error message |
| Code review | "Review this diff for: correctness, edge cases, security, style vs [conventions]. Output: numbered findings with severity." | Review axes, output format, conventions ref |
| Summarization | "Summarize [document] in [N] sentences for [audience]. Include: [key points]. Omit: [irrelevant sections]." | Length, audience, include/omit |
| Extraction | "Extract [fields] from the following [document type]. Output as JSON with schema: [schema]. Return null for missing fields." | Schema, null handling |

---

## Step 4: How many rounds of iteration?

| Situation | Appropriate rounds |
|---|---|
| Well-specified request, output mostly right | 1 targeted revision |
| Partially specified request | 1 revision to fix structural issues, 1 for content |
| Output is wrong in a consistent way (all outputs too long, all missing a key element) | Rewrite the brief, not the output. 0 additional rounds on the bad output. |
| Output is right but voice is off | Edit voice yourself. 0 more rounds. |
| 3rd round of iteration on the same output | STOP. Rewrite the brief from scratch. |

---

## Quick-reference: Task triage matrix

| Task | AI-appropriate? | Best tool | Validation method |
|---|---|---|---|
| Competitor research | Yes | Computer | Spot-check 3 claims vs sources |
| Writing a Slack message | Usually no | — | — |
| Debugging a known error | Sometimes | Computer + bash | Run the fix |
| Refactoring 500 lines | Yes, with care | Cursor / Computer | Run tests |
| Deciding product strategy | No | — | — |
| Drafting an email | Yes | Computer or Claude | Read aloud |
| Extracting data from a PDF | Yes | Computer | Check 3 rows |
| Market sizing | Yes (as a starting point) | Computer | Check methodology, not just numbers |
| Writing a performance review | Partial (AI for structure, you for content) | Computer | Your judgment |
| Generating test cases | Yes | Computer + bash | Run the tests |
