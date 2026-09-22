# Local RAG components — pulled 2026-09-22

**This file expires.** Every claim carries a source URL and a pull date. If
today is more than roughly two months past 2026-09-22, re-verify before
quoting, and rename the file when you refresh it. Nothing here comes from model
memory.

---

## 1. Local embeddings are no longer a compromise

As of April 2026, three open embedding models matched or beat OpenAI's
`text-embedding-3-large` on retrieval accuracy in one practitioner's RAG
benchmarks, at $0 per million tokens, leaking no documents to a third party, and
running on a ~$300 GPU ([Local AI Master](https://localaimaster.com/blog/local-vs-openai-embeddings),
pulled 2026-09-22). Single-practitioner benchmarks are directional, not
authoritative — reproduce on your own corpus before committing.

## 2. Embedding model picks

From [d-central](https://d-central.tech/local-embedding-models/) (pulled
2026-09-22):

| Model | Params | VRAM | License | Notes |
|---|---|---|---|---|
| `nomic-embed-text` | 137M | ~0.3 GB | MIT | Easiest start, pulls from Ollama |
| `Qwen3-Embedding-0.6B` | 0.6B | ~1.5 GB | Apache-2.0 | **Best quality per VRAM**, 70.7 MTEB-eng-v2, Ollama-native |
| `Qwen3-Embedding-8B` | 8B | high | Apache-2.0 | Scale up only with GPU to spare |
| `bge-m3` | 568M | moderate | MIT | Multilingual + dense/sparse/ColBERT in one model |

Apple Silicon specifics from [Contra Collective](https://contracollective.com/blog/local-embeddings-apple-silicon-nomic-bge-qwen3-m5-max-2026)
(pulled 2026-09-22): `nomic-embed-text-v2` (137M, MIT, 8192-token context),
`bge-m3` (568M, MIT, 8192-token context, hybrid retrieval),
`Qwen3-Embedding-8B` (8B, Apache-2.0).

For 8 GB laptops, [Local AI Zone](https://local-ai-zone.github.io/guides/best-ai-embedding-models-ultimate-ranking-2026.html)
(pulled 2026-09-22) recommends BGE-M3 or Nomic Embed v2, both supporting hybrid
retrieval.

**Non-negotiable:** the embedding model is part of your index. Changing it
invalidates every stored vector. Pin the version and record it beside the index.

## 3. Two-model memory budget

A generator plus an embedder must be resident together. Worked figure from
[CraftRigs](https://craftrigs.com/articles/63-hardware-for-local-rag-system/)
(pulled 2026-09-22): Llama 3.1 8B at Q4 (~5 GB) plus `nomic-embed-text`
(~0.7 GB) needs **6 GB minimum**, fitting an 8 GB card. A 14B generator at
~8.9 GB plus an embedder pushes past 12 GB.

Add the KV cache at your real context length on top — see
`maximus-slm-local-stack/references/slm-landscape-2026-09.md` section 3.

## 4. Grounding reduces small-model error

Retrieval supplies supporting passages at inference time, improving factuality
and interpretability, at the cost of retrieval-accuracy dependence and added
latency ([SciTePress, optimizing knowledge placement in small language
models](https://www.scitepress.org/Papers/2026/144557/144557.pdf), pulled
2026-09-22).

Hallucination rate is not purely a function of parameter count: Intel documents
a 7B model posting a low hallucination rate on Vectara's HHEM leaderboard
([Intel](https://www.intel.com/content/www/us/en/developer/articles/technical/do-smaller-models-hallucinate-more.html),
pulled 2026-09-22 — note this article dates to 2024, so treat it as evidence
that size is not destiny, not as a current ranking).

Detection and mitigation methods inside RAG frameworks (LettuceDetect, RAG-HAT,
prompting techniques) have documented efficacy and documented limits — see
[this OpenReview paper on low-resource hallucination mitigation](https://openreview.net/pdf/8a86dbf69cccf07d757370a0b1bb6adcbb9ed32c.pdf)
(pulled 2026-09-22) before assuming any single guardrail is sufficient.

## 5. Prior art to study before building

[Local Deep Research](https://github.com/LearningCircuit/local-deep-research) —
open-source, runs fully local or against cloud LLMs, 10+ search sources
(arXiv, PubMed, web, private documents), encrypted storage, reporting ~95%
accuracy on SimpleQA ([review](https://andrew.ooo/posts/local-deep-research-self-hosted-ai-research-review/),
[listing](https://www.everydev.ai/tools/local-deep-research), both pulled
2026-09-22). SimpleQA is a narrow short-answer benchmark; a high score there
does not transfer to open-ended synthesis. Read it for architecture, not as a
capability promise.

## 6. Full local stacks

Single-GPU laptops can now serve very long contexts without a cloud API: one
2026-09-08 walkthrough reports a 262,000-token context window served locally
after Qwen3.8-27B shipped under Apache 2.0 on August 14, alongside major Ollama
and vLLM releases ([Tech Insider](https://tech-insider.org/run-llm-locally-ollama-vllm-rag-2026/),
pulled 2026-09-22). Verify the model name and license directly with the vendor
before relying on this; long-context claims also say nothing about *quality* at
that length.

## 7. What to re-check on refresh

1. Whether the embedding leaderboard order changed (MTEB moves constantly).
2. Whether the recommended embedders still ship in Ollama.
3. Whether reranker options improved at small VRAM.
4. Current hallucination-detection tooling inside RAG frameworks.
5. Whether Local Deep Research or a successor changed architecture.
