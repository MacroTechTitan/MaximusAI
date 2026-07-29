# MXFP4 / MXFP8 quantization — reference

## What Moonshot AI shipped

Per the [K3 README §4](https://github.com/MoonshotAI/Kimi-K3):

> "Kimi K3 applies quantization-aware training from the SFT stage onward, using MXFP4 weights with MXFP8 activations for broad hardware compatibility."

Key facts:
- **MXFP4 weights** — Microscaling FP4 format, ~4 bits per weight with a shared 8-bit block exponent.
- **MXFP8 activations** — Microscaling FP8 activations for compute.
- **Quantization-aware training (QAT)** — quantization is baked into training from the SFT stage. This is different from post-training quantization (PTQ), which quantizes an already-trained model and typically loses more quality.

## Why this matters for self-hosting

1. **VRAM footprint is closer to a 4-bit model than a 16-bit one.** A naive bf16 estimate for 2.8T parameters would be ~5.6 TB of weights; MXFP4 with block-scaled exponents is much less. Actual per-engine footprint depends on how the engine packs and pages the weights — consult the engine recipe.
2. **MXFP8 activations require hardware support.** Not every GPU generation has efficient MXFP8 compute. Check your target hardware.
3. **QAT means "quantized" is native, not degraded.** Do not benchmark K3 in a de-quantized bf16 form and expect the same accuracy as MXFP4 native — QAT models can behave differently outside their training precision.
4. **Do not re-quantize.** Applying additional PTQ on top of a QAT MXFP4 model usually loses quality without a clear win.

## Hardware compatibility notes

- Moonshot AI's stated intent is "broad hardware compatibility" through the microscaling formats. Interpret this cautiously — check your specific GPU's MXFP4/MXFP8 support before committing.
- H20 GPUs appear in the K3 report footnotes for benchmark reruns.
- Blackwell (B100 / B200) has native FP4 compute; Hopper (H100 / H200) supports FP8 broadly with software paths for FP4.
- Older architectures (A100 and earlier) may require software emulation for MXFP4/MXFP8 and lose most of the efficiency benefit.

## What this file must never do

- Never quote a specific VRAM number for K3 without pointing at the engine recipe that produced it.
- Never claim MXFP4 makes K3 "half the size" of a bf16 model without noting that MXFP4 also stores block-scale exponents and requires runtime unpacking.
- Never recommend re-quantizing a QAT model to a different format without evidence.

## Where to get real numbers

- Your chosen engine's K3 recipe (vLLM, SGLang, TokenSpeed) will name the tested VRAM footprint on tested hardware.
- The [K3 tech report PDF](https://github.com/MoonshotAI/Kimi-K3/blob/main/k3_tech_report.pdf) may include more detail than the README.

Last reviewed: **2026-07-28**.
