# HOWTO — Maximus Deep Research

Six recipes. Each names the mode, the tools, and the shape of the output. Adapt query counts to the actual complexity of the question — these are starting points, not quotas.

## (a) Synthesize a topic from 15+ sources

**Mode:** Synthesis. **When:** a question too broad or contested for one source to answer honestly.

1. Frame the question into 3-5 sub-questions. Write them down before searching — this is the fan-out plan.
2. For each sub-question, run 2-3 `search_web` queries, short and keyword-based, in parallel (up to 3 queries per `search_web` call, multiple calls if needed). Aim for enough breadth that you have 15-20 candidate URLs before you start reading deeply.
3. Skim results, pick the strongest 2-3 per sub-question (favor primary/secondary sources — see `references/source-quality-tiers.md`), and `fetch_url` each with a targeted `prompt` asking for the specific fact, figure, or argument you need — not "summarize this page."
4. Dedup: group fetched facts by claim. If 6 of your 15 sources say the same thing, that's one well-supported claim, not six citations to sprinkle everywhere — pick the best 1-2 sources to cite, note the consensus.
5. Cross-verify: identify the 2-3 claims the final answer actually depends on. Confirm each against at least two independent sources, at least one primary/secondary. Flag anything that only tertiary sources support.
6. Write the synthesis: lead with the answer, structure by sub-question or by argument (not by source), cite inline as you go.
7. Save the trace (queries, source list, key claims) to a workspace file if the research is substantial enough that someone might need to audit it later.

See `examples/synthesis-trace.md` for a fully worked version of this recipe.

## (b) Competitive teardown of 5-10 vendors

**Mode:** Competitive Intel. **When:** "compare vendors", "competitive intel", "who should we buy from".

1. Fix the entity list and the dimensions up front: typically pricing, core features, target segment/positioning, differentiator/moat, and known weaknesses or complaints.
2. Per vendor, fan out: pricing page, product/docs pages, and at least one independent source (review site, analyst mention, user forum) for the "weakness" dimension — vendors don't self-report their weaknesses.
3. If the vendor count × dimension count is large (6+ vendors × 5+ fields), delegate the raw pull to `wide-search`: write one self-contained brief listing every vendor and every field, call `run_subagent` with `subagent_type="research"`, `preload_skills=["wide-search"]`, per that skill's instructions. Use its returned table as your evidence base.
4. Normalize the pulled data into one comparison table. Mark any cell that couldn't be verified as `n.a.` rather than guessing or reusing a competitor's marketing claim about another vendor.
5. Synthesize a short narrative on top of the table: where the market is converging, where vendors genuinely differentiate, and (if asked) a recommendation with the reasoning shown.
6. Cite every pricing figure and feature claim inline — pricing pages change; the citation lets the reader check currency.

See `examples/competitive-intel-trace.md` for a fully worked version (AI code review tools, 6 vendors).

## (c) Market sizing from primary sources

**Mode:** Synthesis, applied to a numeric question. **When:** "how big is market X", "what's the TAM for Y".

1. Identify what "size" means for this market — revenue, unit volume, user count, transaction value — and over what period. Ambiguity here compounds into a wrong number later.
2. Search for primary numeric sources first: government statistics agencies, industry association reports, public company filings (10-Ks disclose segment revenue that can anchor a market estimate), and paid analyst reports if summaries are publicly available.
3. Expect no single source to give a clean, current, exactly-scoped number. Collect 3-5 estimates, note their methodology, scope, and date — a "2021, North America only" figure is not the same claim as a "2026, global" one.
4. Cross-verify by triangulation: if a bottom-up estimate (units × price) and a top-down estimate (analyst TAM figure) land in the same order of magnitude, that's real corroboration. If they diverge by 5-10x, say so and explain the likely scope difference rather than picking one.
5. Present the estimate as a range with the reasoning and sources shown, not a single decimal-precision number that implies false confidence.

## (d) Technical or scientific deep dive

**Mode:** Synthesis, weighted toward primary literature. **When:** "how does X actually work", "what's the current state of the art in Y".

1. Run `search_vertical` with `vertical="academic"` alongside `search_web` — papers and preprints are the primary sources here; blog explainers are useful for framing but not for the technical claims themselves.
2. Prefer recent review papers or survey papers as an entry point — they map the landscape faster than reading primary papers cold, then follow their citations for the specific claims you need.
3. Fetch abstracts and relevant sections with `fetch_url` and a targeted prompt; don't rely on search snippets for technical accuracy.
4. Cross-verify any quantitative result (benchmark numbers, performance claims) against the original paper or a reproduction, not a secondary summary that may have transcribed it wrong.
5. Note where the field disagrees or where results haven't been replicated — a deep dive that only presents consensus is missing the most useful part for a technical reader.

## (e) Building a data table from many sources — delegate to wide-search

**When:** the research question is fundamentally "N entities, M fields each" — screeners, comparison tables, structured datasets.

Don't hand-roll this fan-out yourself. Load the built-in `wide-search` skill and follow it directly:

1. Write one self-contained brief: the full entity list inline, every field with definitions/units, the required output shape (columns, row order).
2. Call `run_subagent` once with `subagent_type="research"`, `task_name="wide_search_research"`, `preload_skills=["wide-search"]`, and the brief as `objective`.
3. Treat the returned table as a source-linked evidence base — every cell should carry the URL it came from, and unverified cells should read `n.a.`.
4. From there, this skill's job resumes: synthesize the table into the narrative, comparison, or recommendation the user actually asked for.

## (f) Turning research into an article — handoff to maximus-write-article

**When:** research is done, cited, and the next step is a publishable piece.

1. Finish the research to the point where every claim that will appear in the article has a citation and any unresolved disagreements are documented.
2. Do not start drafting prose here — hand off to `maximus-write-article` with the synthesized, cited findings as its input material, not a re-research task.
3. Carry the citation list across the handoff intact. The writing skill should be citing the same sources this skill verified, not re-deriving them from memory.
