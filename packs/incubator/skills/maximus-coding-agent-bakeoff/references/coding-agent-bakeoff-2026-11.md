# Coding agent bake-off — facts and sources (pulled 2026-11-18)

| Fact | Source |
|---|---|
| Runta FrontierHarness Eval v1.1: 27,280 trials, 22 harness configurations, five models, 62 terminal tasks, four repeated trials per configuration, fresh runtime per trial, time limits from 15 minutes to eight hours; reward-hacked trials scored as failures | https://groundtruth.day/news/runta-coding-agent-inference-cost-failed-trials.html |
| 64.5% of priced inference spend went to runs that did not pass (52.7 points failures, 11.8 points timeouts); among the five best-value pairings, 68-82% of failed runs ended with a final answer rather than the time limit | same |
| Caveats: specific terminal tasks, one model provider, binary scoring; the results do not establish which setup works best on a particular team's backlog, which needs to be measured on a representative workload; a low-cost system can look best on cost per success by solving easier tasks | same |
| 83B tokens; model choice explained 92.8% of cost variation, harness alone 2.3%, harness-model pairing 4.9%; no single harness gave the best value across every model; Codex CLI ranked first on cost per task with GLM-5.3 and 16th with Kimi-K3; 216 trials flagged for reward hacking, 163 involving online lookups | https://www.insightex.si/news/runta-benchmark-finds-the-best-coding-agent-harness-changes-with-each-model |
| Benchmark Factory (arXiv 2611.18890, Nov 13, 2026): builds benchmarks from a team's landed production code changes; runs models of known relative strength; label-free quality anchors are necessary but not sufficient; a deliberately trivial benchmark and five broken graders failed the anchors; on held-out configurations it separated GPT-5.5 from GPT-5.4 (65.8% vs 60.5%, p = 0.004) | https://arxiv.org/abs/2611.18890 |
| Scout run 2026-11-18: `examples/bakeoff_report.py` on a synthetic 320-run CSV reported pass rates with Wilson intervals, cost per pass, and spend share on failures; exit 2 when the expected-stronger config lost and when a null config passed 100%; flagged an always-passed task and a never-passed task | local run |

Volatile: leaderboards and prices change monthly. The method (own tasks, repeats, anchors, cost per pass) is the durable part.
