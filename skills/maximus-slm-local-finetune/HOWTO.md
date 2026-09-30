# HOWTO — SLM Local Fine-Tune

Three recipes. Versions and VRAM numbers: `references/slm-local-finetune-2026-09.md`.
All code is **illustrative**. It follows the documented APIs, but pin versions
and check against current docs before running.

---

## 1. Unsloth (NVIDIA / AMD / Intel / Mac) → Ollama

```python
from unsloth import FastLanguageModel
model, tok = FastLanguageModel.from_pretrained("unsloth/Qwen3-8B", load_in_4bit=True,
                                               max_seq_length=4096)
model = FastLanguageModel.get_peft_model(model, r=16, lora_alpha=16)
# ... train with TRL SFTTrainer on your chat-formatted train split ...
model.save_pretrained_gguf("out", tok, quantization_method="q4_k_m")
```

Unsloth writes a Modelfile with the chat template used in training. Then:

```bash
ollama create my-tune -f out/Modelfile
ollama run my-tune
```

## 2. MLX-LM (Apple Silicon)

```bash
# data/ holds train.jsonl, valid.jsonl, test.jsonl in chat format:
# {"messages":[{"role":"user","content":"..."},{"role":"assistant","content":"..."}]}
mlx_lm.lora --model mlx-community/Mistral-7B-Instruct-v0.3-4bit --train --data data \
            --adapter-path adapters --iters 600
mlx_lm.lora --model mlx-community/Mistral-7B-Instruct-v0.3-4bit --adapter-path adapters \
            --data data --test
mlx_lm.fuse --model mistralai/Mistral-7B-Instruct-v0.3 --adapter-path adapters --export-gguf
# -> fused_model/ggml-model-f16.gguf  (Mistral/Mixtral/Llama-style only, fp16)
```

A quantized `--model` means QLoRA. For Qwen or Gemma, fuse without
`--export-gguf` and convert the safetensors with llama.cpp's converter.

## 3. Quantize, import, re-evaluate

```bash
llama-quantize fused_model/ggml-model-f16.gguf my-tune-Q4_K_M.gguf Q4_K_M
cat > Modelfile <<'MF'
FROM ./my-tune-Q4_K_M.gguf
PARAMETER num_ctx 8192
# TEMPLATE """...copy the base model's template from `ollama show <base> --modelfile`..."""
MF
ollama create my-tune -f Modelfile
```

Run the `maximus-slm-eval` suite against `ollama:chat:my-tune` and the base
model tag. Ship only if the quantized build still wins.
