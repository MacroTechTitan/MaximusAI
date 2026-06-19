# HOWTO — maximus-ai-fluency-for-builders

Recipes for the most common AI-fluency tasks. Each recipe is a complete, runnable procedure.

---

## Recipe 1: How to delegate a research task to AI

**Goal**: Get a high-quality research output on a technical or domain topic without re-doing the work yourself.

**Steps**:
1. Define the research question precisely. "What are the best options?" is not a research question. "What are the three most actively maintained open-source vector databases as of 2025, and what are their performance tradeoffs at 10M vectors?" is.
2. Specify the output format: "Return a table with columns: name, license, index type, query latency at 10M vectors, and a one-sentence tradeoff note."
3. Add a source constraint: "Cite primary sources (official docs or benchmarks) for each latency figure. Include the URL."
4. Add a recency constraint if needed: "Focus on information from 2024 onward."
5. Run in Perplexity Computer (for multi-source synthesis) or Perplexity search (for single-fact lookups).
6. Validate: spot-check 3 claims against the cited URLs. Verify the URLs open and say what they're cited for.

**Verification**: All cited URLs are real, open, and support the claims made. The output table has no blank cells.

**Common pitfalls**:
- Asking for "everything about X" produces padding and unfocused output. Constrain the scope before you run it.
- Skipping the source constraint produces confident-sounding uncited claims. Always ask for URLs.
- Using Perplexity search for a multi-source synthesis question. Use Computer for those — search is for single-fact lookups.

---

## Recipe 2: How to validate AI output without redoing the work

**Goal**: Confirm AI output is accurate and complete without spending more time than the delegation saved.

**Steps**:
1. Use `examples/validate-output-checklist.md` as the base checklist.
2. **Structural check** (1 min): Does the output match the format you specified? Correct number of items, right columns, right length? If not, that's a specification failure — rerun with a clearer constraint.
3. **Sample check** (3–5 min): Pick 3 specific factual claims or code paths. Verify each against the primary source (cited URL, docs, or running the code). If 0/3 are wrong, proceed. If 1/3 is wrong, fix and check the others. If 2+/3 are wrong, the output is not trustworthy — rerun with more constraints.
4. **Edge-case check** (for code): Identify the 2 most likely edge cases. Does the output handle them? If not, note them and fix.
5. **Tone check** (for copy): Read aloud. Does it sound like you or your brand? If not, it's a second-author draft — edit.
6. Document any errors found for the iteration step.

**Verification**: You can stand behind the output. If a claim is challenged, you can point to the source.

**Common pitfalls**:
- Checking all claims (redoing the work). Check a sample — 3 claims is enough for most outputs.
- Only checking the things you already know. Specifically check the things you don't know, which are where errors are likely.
- Skipping the structural check. Wrong format often signals wrong content.

---

## Recipe 3: How to pick the right tool for a task

**Goal**: Route a task to the AI tool most likely to produce a good result efficiently.

**Steps**:
1. Classify the task using the delegation decision tree in `references/delegation-decision-tree.md`.
2. Apply the routing table:
   - Single-fact lookup, current information → **Perplexity search**
   - Multi-source research synthesis → **Perplexity Computer**
   - In-repo code edit with file context → **Cursor** (or Computer with `bash`/`edit` tools)
   - Long-document review (>50 pages) → **Computer** (large context window)
   - Iterative copy drafting → **Computer or Claude** (conversation memory)
   - Structured data extraction with schema → **Computer with schema prompt**
   - Image generation → **Computer media skill**
   - Scheduled/automated job → **Computer cron + programmatic tools**
3. If unsure between two tools: use the one with more context about the task. Computer with your codebase context beats a standalone chat for code. Perplexity search beats Computer for breaking news.
4. Run the task.
5. If the output is poor: check whether the failure was a tool mismatch before blaming the prompt.

**Verification**: The tool used is the one best suited to the task type. If you got a poor result, you can explain whether it was a tool choice, prompt, or inherent task difficulty issue.

**Common pitfalls**:
- Defaulting to chat for everything. Forms reduce errors for constrained tasks; code tools need repo context.
- Using a frontier model for simple classification or extraction. A smaller model (Haiku, GPT-4o mini) handles these at 10× lower cost.

---

## Recipe 4: How to compose a multi-step AI workflow

**Goal**: Break a complex task into AI-handled and human-handled steps, execute them in sequence, and get a shippable output.

**Steps**:
1. Decompose the task into steps. Example: "Write a technical blog post" → (a) research the topic, (b) outline, (c) draft, (d) edit for voice, (e) add examples.
2. Label each step: AI-primary, human-primary, or collaborative (AI drafts, human edits).
3. Run AI-primary steps first and validate output before passing it to the next step. Don't chain AI outputs without a validation gate.
4. For collaborative steps: give AI the human-authored input from the previous step as context. Anchor to what's already decided.
5. For human-primary steps: do the work. Don't force AI into a step where your judgment is the point.
6. At the end: review the full output as a whole. AI-composed multi-step outputs often have seams — transitions between sections, inconsistent terminology — that only show in the complete view.

**Verification**: The final output reads as a coherent whole, not as patched AI sections. The human-primary steps reflect genuine judgment, not AI-written content you agreed with.

**Common pitfalls**:
- Chaining AI outputs without validation gates. Error in step 2 compounds through steps 3, 4, 5.
- Using AI for judgment calls ("which approach is best?") where your knowledge of the business context is irreplaceable. AI can surface options; you pick.
- Not re-reading the whole at the end. Step-by-step quality doesn't guarantee overall coherence.

---

## Recipe 5: How to draft with AI as the second author

**Goal**: Produce copy or documentation with AI doing the bulk of the drafting and you providing structure and voice.

**Steps**:
1. Write the brief yourself: audience, goal, key points to hit, tone, length, and one example of the right voice.
2. Ask AI for a first draft with the explicit framing: "Draft, not final. Focus on structure and coverage — I'll adjust voice."
3. Read the draft once without editing. Mark: (a) anything factually wrong, (b) anything structurally wrong, (c) sections where the voice is off.
4. Fix factual errors yourself (don't ask AI — it may restate the error confidently).
5. Give AI one targeted instruction for structural issues: "The second section buries the main point. Rewrite it so the first sentence states the conclusion."
6. Edit for voice yourself. AI can match a style direction but not your exact voice. Voice editing is fast — do it yourself.
7. Read aloud before publishing.

**Verification**: If you read the output, you could defend every sentence. The voice sounds like you (or your brand), not like generic AI prose.

**Common pitfalls**:
- Asking AI to fix its own factual errors. Restate the correct fact and ask it to incorporate it, rather than asking it to "fix the error."
- Publishing without reading aloud. Sentences that look right on screen often read awkwardly aloud — especially lists and headers.
- Using AI as a ghostwriter for opinion pieces. AI can draft; the opinion has to be yours.
