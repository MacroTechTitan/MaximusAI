"""
LoRA Fine-Tuning Script
========================
Fine-tunes a causal language model using LoRA (Low-Rank Adaptation) with the
Hugging Face PEFT + TRL stack.

Supports:
- Instruction tuning (SFT) on OpenAI Chat format JSONL
- QLoRA variant (4-bit quantized base model) for lower VRAM

Requirements:
    pip install transformers peft trl datasets accelerate bitsandbytes

Data format (train.jsonl and val.jsonl):
    Each line is one training example in OpenAI Chat format:
    {"messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of France?"},
        {"role": "assistant", "content": "The capital of France is Paris."}
    ]}

Usage:
    python lora-finetune.py --model meta-llama/Llama-3.1-8B-Instruct \
        --train data/train.jsonl --val data/val.jsonl \
        --output ./output --epochs 3 --qlora

Note: Requires a Hugging Face token with access to gated models like Llama.
      Set: export HF_TOKEN=your_token_here
"""

import argparse
import json
import logging
import os
from pathlib import Path
from typing import Optional

import torch
from datasets import Dataset

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_chat_jsonl(path: str) -> Dataset:
    """
    Load a JSONL file in OpenAI Chat format into a Hugging Face Dataset.
    Each line: {"messages": [{"role": ..., "content": ...}, ...]}
    """
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON on line {i+1} of {path}: {e}") from e

            if "messages" not in record:
                raise ValueError(
                    f"Line {i+1} in {path} missing 'messages' key. "
                    "Expected OpenAI Chat format: {\"messages\": [...]}"
                )
            records.append(record)

    logger.info("Loaded %d examples from %s", len(records), path)
    return Dataset.from_list(records)


# ---------------------------------------------------------------------------
# Model and tokenizer loading
# ---------------------------------------------------------------------------

def load_model_and_tokenizer(
    model_name: str,
    use_qlora: bool = False,
    torch_dtype=None,
):
    """
    Load the base model and tokenizer.

    Args:
        model_name: HuggingFace model ID or local path.
        use_qlora: If True, load in 4-bit NF4 quantization for QLoRA.
        torch_dtype: Override default dtype. None = auto-select.
    """
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

    logger.info("Loading tokenizer: %s", model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

    # Most chat models need a pad token; use eos_token if not set
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
        logger.info("Set pad_token = eos_token")

    if use_qlora:
        logger.info("Loading model in 4-bit NF4 quantization (QLoRA mode)")
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,  # Saves ~0.4 bits/param additional
        )
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=quantization_config,
            device_map="auto",
            trust_remote_code=True,
        )
    else:
        dtype = torch_dtype if torch_dtype else (torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float16)
        logger.info("Loading model in %s", dtype)
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=dtype,
            device_map="auto",
            trust_remote_code=True,
        )

    logger.info(
        "Model loaded. Parameters: %dM",
        sum(p.numel() for p in model.parameters()) // 1_000_000
    )
    return model, tokenizer


# ---------------------------------------------------------------------------
# LoRA configuration
# ---------------------------------------------------------------------------

def get_lora_config(
    rank: int = 16,
    alpha: int = 32,
    dropout: float = 0.05,
    target_modules: Optional[list[str]] = None,
    use_qlora: bool = False,
):
    """
    Build a LoRA configuration.

    Args:
        rank: LoRA rank (r). Higher rank = more parameters = better capacity.
              Default 16 is a good starting point for most tasks.
        alpha: LoRA alpha (scaling factor). Typically 2× rank.
        dropout: Dropout applied to LoRA layers. 0.05–0.1 for regularization.
        target_modules: Attention projection layers to apply LoRA to.
                       None = PEFT auto-detects based on model architecture.
        use_qlora: If True, prepare for QLoRA (adds gradient checkpointing preparation).
    """
    from peft import LoraConfig, TaskType

    if target_modules is None:
        # These work for Llama, Mistral, Phi, Gemma architectures.
        # For other architectures, inspect model.named_modules() to find attention layers.
        target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]

    config = LoraConfig(
        r=rank,
        lora_alpha=alpha,
        lora_dropout=dropout,
        target_modules=target_modules,
        task_type=TaskType.CAUSAL_LM,
        bias="none",  # Don't train bias parameters
    )

    logger.info(
        "LoRA config: rank=%d, alpha=%d, dropout=%.2f, target_modules=%s",
        rank, alpha, dropout, target_modules
    )
    return config


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train(
    model_name: str,
    train_path: str,
    val_path: str,
    output_dir: str,
    num_epochs: int = 3,
    batch_size: int = 2,
    gradient_accumulation_steps: int = 8,
    learning_rate: float = 2e-4,
    warmup_ratio: float = 0.03,
    lora_rank: int = 16,
    lora_alpha: int = 32,
    use_qlora: bool = False,
    max_seq_length: int = 2048,
):
    """
    Run LoRA/QLoRA fine-tuning using TRL's SFTTrainer.
    """
    from peft import get_peft_model, prepare_model_for_kbit_training
    from trl import SFTTrainer, SFTConfig

    # Load model and tokenizer
    model, tokenizer = load_model_and_tokenizer(model_name, use_qlora=use_qlora)

    # For QLoRA: prepare model for training (enables gradient checkpointing, casts layer norms)
    if use_qlora:
        model = prepare_model_for_kbit_training(model)

    # Apply LoRA
    lora_config = get_lora_config(rank=lora_rank, alpha=lora_alpha, use_qlora=use_qlora)
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # Load datasets
    train_dataset = load_chat_jsonl(train_path)
    eval_dataset = load_chat_jsonl(val_path)

    # Training configuration
    training_args = SFTConfig(
        output_dir=output_dir,
        num_train_epochs=num_epochs,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        gradient_accumulation_steps=gradient_accumulation_steps,
        learning_rate=learning_rate,
        warmup_ratio=warmup_ratio,
        lr_scheduler_type="cosine",
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        eval_strategy="steps",
        eval_steps=100,
        save_strategy="steps",
        save_steps=100,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss",
        greater_is_better=False,
        logging_steps=10,
        report_to=["tensorboard"],
        max_seq_length=max_seq_length,
        dataset_text_field=None,  # Use messages format
        remove_unused_columns=False,
    )

    trainer = SFTTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        processing_class=tokenizer,
    )

    logger.info("Starting training...")
    trainer.train()

    # Save the LoRA adapter (not the full model — much smaller)
    adapter_path = Path(output_dir) / "lora-adapter"
    trainer.model.save_pretrained(adapter_path)
    tokenizer.save_pretrained(adapter_path)
    logger.info("LoRA adapter saved to %s", adapter_path)

    return trainer


# ---------------------------------------------------------------------------
# Optional: merge LoRA adapter into base model for simplified serving
# ---------------------------------------------------------------------------

def merge_adapter(base_model_name: str, adapter_path: str, merged_output_path: str):
    """
    Merge the LoRA adapter weights into the base model for deployment.
    The merged model can be served without PEFT as a standard model.

    Trade-off: merged model is the full model size on disk. Adapter-only is smaller
    but requires PEFT at serving time.
    """
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    logger.info("Loading base model for merge: %s", base_model_name)
    base_model = AutoModelForCausalLM.from_pretrained(
        base_model_name, torch_dtype=torch.float16, device_map="cpu"
    )
    tokenizer = AutoTokenizer.from_pretrained(adapter_path)

    logger.info("Loading and merging LoRA adapter: %s", adapter_path)
    peft_model = PeftModel.from_pretrained(base_model, adapter_path)
    merged_model = peft_model.merge_and_unload()

    logger.info("Saving merged model to %s", merged_output_path)
    merged_model.save_pretrained(merged_output_path)
    tokenizer.save_pretrained(merged_output_path)
    logger.info("Merge complete.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LoRA/QLoRA fine-tuning with TRL SFTTrainer")
    parser.add_argument("--model", required=True, help="HuggingFace model ID or local path")
    parser.add_argument("--train", required=True, help="Path to train.jsonl (OpenAI Chat format)")
    parser.add_argument("--val", required=True, help="Path to val.jsonl (OpenAI Chat format)")
    parser.add_argument("--output", required=True, help="Output directory for checkpoints and adapter")
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--batch-size", type=int, default=2)
    parser.add_argument("--grad-accum", type=int, default=8)
    parser.add_argument("--lr", type=float, default=2e-4)
    parser.add_argument("--lora-rank", type=int, default=16)
    parser.add_argument("--lora-alpha", type=int, default=32)
    parser.add_argument("--qlora", action="store_true", help="Use QLoRA (4-bit quantization)")
    parser.add_argument("--max-seq-len", type=int, default=2048)
    parser.add_argument("--merge", action="store_true",
                        help="After training, merge adapter into base model")

    args = parser.parse_args()

    os.makedirs(args.output, exist_ok=True)

    trainer = train(
        model_name=args.model,
        train_path=args.train,
        val_path=args.val,
        output_dir=args.output,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        gradient_accumulation_steps=args.grad_accum,
        learning_rate=args.lr,
        lora_rank=args.lora_rank,
        lora_alpha=args.lora_alpha,
        use_qlora=args.qlora,
        max_seq_length=args.max_seq_len,
    )

    if args.merge:
        merged_path = Path(args.output) / "merged-model"
        adapter_path = Path(args.output) / "lora-adapter"
        merge_adapter(
            base_model_name=args.model,
            adapter_path=str(adapter_path),
            merged_output_path=str(merged_path),
        )
        print(f"\nMerged model saved to: {merged_path}")

    print(f"\nTraining complete. LoRA adapter at: {Path(args.output) / 'lora-adapter'}")
    print("Next step: evaluate with maximus-eval-and-test before promoting to production.")
