# Decision models — facts and sources (pulled 2026-10-14)

| Fact | Source |
|---|---|
| Ollama added decision models via `/v1/systemone`, based on TypeSafe's Jev API, available as of Ollama 0.35 (blog dated Sep 29, 2026) | https://ollama.com/blog/ollama-now-supports-jev-style-decision-models |
| Ollama models: Nimble (9B, Bespoke Labs), Tev1 (4B and 0.8B, Together AI, experimental); Clef and Clef Flash judge images and need v0.35.1+ | https://ollama.com/blog/ollama-now-supports-jev-style-decision-models , https://docs.ollama.com/capabilities/decision |
| Question types: `choice` (2–26 named options), `noul` (probability of true), `score` (2–10 ordered levels; probability-weighted average of zero-based indices) | https://docs.ollama.com/capabilities/decision |
| "A higher [confidence] value does not guarantee the answer is correct" | https://docs.ollama.com/capabilities/decision |
| Ollama limits: one JSON response, no streaming/tools; 64 KiB without images, 32 MiB with images; input never truncated; up to 64 questions per request; errors 400/404/413/500; local only, not on Ollama Cloud | https://docs.ollama.com/api/systemone |
| `ollama run <model> --ask ... --choice ... --level ...` CLI for decisions | https://docs.ollama.com/capabilities/decision |
| llama.cpp server supports `/v1/systemone` (PR #29818, blog Oct 2, 2026); one forward pass; existing clients only need a new base URL | https://huggingface.co/blog/ggml-org/decision-models-in-llamacpp |
| llama.cpp models: Julia-1 144M, Laya 421M, Kev-4B, lev 4B, OpenJev 27B (CC BY-NC 4.0, images), Clef 27B; median 3–43 ms per question on one RTX PRO 6000 | https://huggingface.co/blog/ggml-org/decision-models-in-llamacpp |
| Tips: describe options (Julia-1 misrouted "charged twice" with bare labels); pick confidence cutoff per model (same vague ticket 0.25 on Julia-1 vs 0.80 on Kev-4B); batch questions | https://huggingface.co/blog/ggml-org/decision-models-in-llamacpp |
| vLLM Semantic Router Decision 3.0: Apache-2.0 decision models from 0.8B to 27B, text/image/video; served behind the System One API | https://huggingface.co/vllm-sr/d3 , https://vllm-sr.ai/blog/tags/decision/ |

Volatile: model list, sizes, limits, version floors. Recheck before relying on them.
