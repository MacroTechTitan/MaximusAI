# Worked trace — Fast tier vs over-firing brain

Brain right-sizes effort. Running Deep on a chat wastes the user's time and feels like an interrogation. Below is the contrast.

---

## The request

User: **"What's the difference between LoRA and QLoRA, in one paragraph?"**

This is a definitional question. Stakes are low. No memory dependency. No code, no deploy, no money. Right tier: **Fast**.

---

## What Fast looks like

> [Pass 1 — Frame, one sentence] User wants a one-paragraph contrast between LoRA and QLoRA. Fast tier.
>
> [Pass 2 — Recall] Skip. No project context needed.
>
> [Pass 3 — Select] No skill needed; this is well-known stable knowledge. (If unsure, would verify against the original LoRA and QLoRA papers.)
>
> [Pass 4 — Execute] Compose the paragraph.
>
> [Pass 5 — Critique, one breath] Names match papers; technique distinction (4-bit quantized base + LoRA adapters) is correct; one paragraph as requested. Ship.

**Response to user:**

> LoRA (Low-Rank Adaptation) freezes the base model and trains small rank-decomposed matrices alongside the original weights, cutting trainable parameters by 10,000× while preserving full-precision base weights. QLoRA goes further: it quantizes the frozen base model to 4-bit (using NormalFloat4 + double quantization) and trains LoRA adapters on top, dropping memory enough to fine-tune a 65B model on a single 48GB GPU. LoRA gives you efficient adaptation; QLoRA gives you efficient adaptation on consumer hardware.

That's it. Three sentences. No skill loaded. No tool call. No ceremony.

---

## What over-firing looks like (anti-pattern)

> Let me think carefully about this. I'll restate the goal: you want to understand the difference between LoRA and QLoRA. Let me first search memory for prior context on this topic… [memory_search] … No prior context found. I'll now load the `maximus-fine-tuning` skill to ensure I cover this thoroughly… [skill load] … I'll plan my response in three sections: 1) LoRA, 2) QLoRA, 3) the comparison…

This is process theater. The user asked for one paragraph. They got a meeting.

**Rule:** Fast tier is the default for chat-style questions. If you find brain announcing the loop on a definitional question, the tier is wrong. Drop to Fast.

---

## When Fast is wrong

Same request, but stakes are now real:

> "What's the difference between LoRA and QLoRA — I'm picking one for the customer support model we ship Monday."

That **is** stakes. Brain promotes to **Standard** (maybe Deep):

- Frame restates the *real* question: "Which technique should we use for the production support model, given LoRA vs QLoRA tradeoffs?"
- Recall checks memory for the model, hardware, and budget constraints.
- Select loads `maximus-fine-tuning` and `maximus-llm-model-selection`.
- Execute produces a contrast plus a recommendation tied to the actual hardware/budget.
- Critique verifies the recommendation against real constraints.

Same domain, different stakes, different tier. The discipline is right-sizing.

---

## The signal

When the user asks a quick question, give a quick answer. When the user signals stakes — explicitly or through the nature of the task — promote the tier. Brain's value is in matching depth to the work, not in being uniformly deep.
