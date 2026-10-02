# Local fine-tuning facts — pulled 2026-09-30

**This file expires.** Unsloth and MLX-LM change monthly. Re-verify after
about two months.

## Unsloth ([requirements](https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements))

- Training works on NVIDIA, AMD, Intel GPUs and Mac. NVIDIA minimum CUDA
  capability 7.0; "GTX 1070, 1080 works, but is slow." On OOM, set batch size
  to 1-3 first.
- VRAM by model size ("QLoRA uses 4-bit, LoRA uses 16-bit"; may need more
  depending on model):

| Params | QLoRA (4-bit) | LoRA (16-bit) |
|---|---|---|
| 3B | 3.5 GB | 8 GB |
| 7B | 5 GB | 19 GB |
| 8B | 6 GB | 22 GB |
| 14B | 8.5 GB | 33 GB |
| 27B | 22 GB | 64 GB |
| 32B | 26 GB | 76 GB |
| 70B | 41 GB | 164 GB |

- Export to Ollama: Unsloth "automatically create[s] a `Modelfile`" including
  the chat template used for fine-tuning. An "incorrect chat template" is "the
  most common cause" of broken output
  ([Saving to Ollama](https://unsloth.ai/docs/basics/inference-and-deployment/saving-to-ollama)).

## MLX-LM ([LORA.md](https://github.com/ml-explore/mlx-lm/blob/main/mlx_lm/LORA.md))

- `mlx_lm.lora --train --data <dir>` expects `train.jsonl` (plus `valid.jsonl`;
  `test.jsonl` for `--test`). If `--model` is quantized, training uses QLoRA.
  Adapters go to `--adapter-path`.
- JSONL formats: `chat`, `tools`, `completions`, `text`. `--mask-prompt` is
  supported for `chat` and `completion`.
- `mlx_lm.fuse` merges adapters. `--export-gguf` writes
  `fused_model/ggml-model-f16.gguf`, but "GGUF support is limited to Mistral,
  Mixtral, and Llama style models in fp16 precision."

## Ollama import ([Importing a model](https://docs.ollama.com/import))

- "Ollama does not quantize GGUF models during import." Use llama.cpp
  `llama-quantize` first.
