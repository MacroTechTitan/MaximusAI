# HOWTO — Ollama Ops

Five recipes. Defaults and flags: `references/ollama-ops-2026-09.md`.

---

## 1. Baseline the box

```bash
ollama --version
ollama ps                     # NAME  SIZE  PROCESSOR  CONTEXT  UNTIL
ollama show qwen3:8b          # parameters, capabilities
ollama show qwen3:8b --modelfile > base.Modelfile
```

Save the output. You will diff against it.

## 2. A project Modelfile

```
# models/research-8b.Modelfile
FROM qwen3:8b
PARAMETER num_ctx 32768
PARAMETER temperature 0.2
PARAMETER stop "<|im_end|>"
SYSTEM You answer only from supplied context and cite the passage you used.
```

```bash
ollama create research-8b -f models/research-8b.Modelfile
ollama run research-8b "ping"
ollama ps    # CONTEXT column should read 32768
```

## 3. Server env (Linux, systemd)

```bash
sudo systemctl edit ollama
```

```
[Service]
Environment="OLLAMA_CONTEXT_LENGTH=32768"
Environment="OLLAMA_FLASH_ATTENTION=1"
Environment="OLLAMA_KV_CACHE_TYPE=q8_0"
Environment="OLLAMA_NUM_PARALLEL=2"
Environment="OLLAMA_KEEP_ALIVE=30m"
```

```bash
sudo systemctl daemon-reload && sudo systemctl restart ollama
```

macOS app: `launchctl setenv OLLAMA_CONTEXT_LENGTH 32768`, then restart Ollama.
Windows: set user environment variables, quit Ollama from the tray, and
relaunch.

Memory check before the restart: `weights + (KV per slot × NUM_PARALLEL) +
~1 GB` must fit under VRAM. Use the formula in `maximus-slm-local-stack`.

## 4. Import a GGUF

```bash
llama-quantize model-f16.gguf model-Q4_K_M.gguf Q4_K_M   # Ollama won't do this
printf 'FROM ./model-Q4_K_M.gguf\nPARAMETER num_ctx 16384\n' > Modelfile
ollama create mymodel -f Modelfile
ollama show mymodel --template   # compare to the model card's chat template
```

If the template is wrong, add a `TEMPLATE` block copied from the base model's
`ollama show --modelfile`.

## 5. Structured output that validates

```python
from ollama import chat
from pydantic import BaseModel

class Finding(BaseModel):
    claim: str
    source_passage: str
    confidence: float

r = chat(model="research-8b",
         messages=[{"role": "user", "content": "Extract the main claim as JSON: ..."}],
         format=Finding.model_json_schema(),
         options={"temperature": 0})
finding = Finding.model_validate_json(r.message.content)
```

Illustrative. It follows the documented `format` usage, but has not been run
against your model.
