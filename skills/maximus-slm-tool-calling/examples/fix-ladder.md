# Worked example — fix ladder on a failing 8B agent

**Illustrative.** The shape of the table is the deliverable. The numbers show
how to report results, and are not measurements of any specific model.

Agent: a repo helper with 9 tools on a general 8B chat model through Ollama's
OpenAI-compatible endpoint. Regression set: 40 cases (28 single-call, 8 chains,
4 no-tool).

| Step applied | Parses | Right tool | Chains complete | Notes |
|---|---|---|---|---|
| Baseline | x% | x% | x% | calls often written as prose |
| Tool-trained model, template checked | ↑ | ↑ | – | `ollama show` lists `tools` |
| Schema on action block only | ~100% | ↑ | – | shape fixed; choice still wrong sometimes |
| 9 → 4 tools, enum args | – | ↑ | – | |
| One tool per step, results truncated to 4K chars | – | – | ↑ | biggest gain on chains |
| Validated single retry | – | ↑ | – | failures now logged, not looped |

Report the final row as absolute rates on your own set, plus the residual
failure rate you are shipping with.
