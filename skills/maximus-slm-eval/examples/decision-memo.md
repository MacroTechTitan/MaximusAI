# Decision memo — <task> on <machine>

**Question.** <one sentence with the threshold, e.g. smallest model ≥ 90% of
baseline on extraction set, ≥ 20 tok/s tg at 16K on M3 Pro 36 GB>

**Pinned.** Runtime <ollama x.y.z>, context <16384 via Modelfile>, temperature
<0>, prompt <sha/filename>, test set <n cases, date>, grader <model or code-only>.

| Model | Quant | Pass rate | Failures by type | pp @ depth | tg @ depth | Peak mem |
|---|---|---|---|---|---|---|
| | | | | | | |

**Choice.** <model + quant>. **Runner-up.** <...> <within noise? say so>.

**Not tested.** <longer contexts, concurrency, tool calls, other languages...>

**Re-run when.** <runtime upgrade, new model release, prompt change>
