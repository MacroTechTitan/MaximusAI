# Review bottleneck — facts and sources (pulled 2026-11-25)

| Fact | Source |
|---|---|
| Chen and Stratton, "Artificial Intelligence in the Firm: Bottlenecks in Software Production", Harvard job market paper, version of Nov 19, 2026 (first Jan 7, 2026); 655 firms, 720,542 workers, 445 million work events, Jan 2021-Aug 2026; not peer reviewed, and figures have moved between versions | https://fion.ac/jellyfish.pdf |
| Agent adoption at 12 months: PRs opened +35.7% (baseline 4.83 per worker-month), PRs merged +26.0%, lines added +44.0% (marginally insignificant), Jira issues resolved +13.7% (marginally insignificant), engineering employment -2.6% (not significant); about 62.7% of the additional PRs were merged vs 86.1% at baseline | same |
| Review: submission to merge +1.99 days (+56.1%, baseline 3.56 days); wait to first human review comment +1.67 days (+59.9%, baseline 2.78); active review +2.33 days (+58.5%, baseline 3.98); review comments per PR +38.6%; "Code review becomes the bottleneck" | same |
| By July 2026, 79.1% of firms had used AI in code review; AI generated 23.3% of review comments; 10.8% of PRs got at least one AI comment; 82.8% of actual reviews were in a codebase the reviewer had previously committed to; no significant change in PR size; an interviewee described senior-approval rules added for AI-generated code after outages | same |
| Demirer, Musolff, Yang, "Writing Code vs. Shipping Code", NBER Working Paper 35275 (May 2026, revised Sep 2026): 500,000+ GitHub developers; cumulative commit effects of 30%, 180%, 240% for autocomplete, interactive agents, autonomous agents; the 240% falls to 80% for projects and 30% for releases | https://www.nber.org/papers/w35275 |
| Scout run 2026-11-25: `examples/review_queue_report.py` on a synthetic 120-PR file and on 53 PRs from MacroTechTitan/MaximusAI ran without error and printed the per-segment table | local run |
