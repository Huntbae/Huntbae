#!/usr/bin/env -S colab run --gpu A100 --keep
"""LoRA fine-tuning template for hermes-local (or any HF causal LM).

Designed to be launched by the `colab-gpu-run` skill:

    colab new -s ft --gpu A100
    colab install -s ft -r requirements.txt
    colab exec -s ft -f finetune_lora.py
    colab download -s ft out/adapter ./adapter
    colab stop -s ft

Or one-shot (the shebang above also makes `./finetune_lora.py` self-provision):

    colab run --gpu A100 finetune_lora.py --epochs 3 --data data/train.jsonl

Data format: JSONL, one object per line with a "text" field (already formatted
prompt+response). Swap `format_example` to match your hermes-local chat template.

Deps: transformers, peft, datasets, accelerate, torch (+ bitsandbytes for 4-bit).
This is a TEMPLATE — adjust BASE_MODEL, the dataset path, and the target modules.
"""
from __future__ import annotations

import argparse
import json
import os
import sys


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="LoRA fine-tune a causal LM")
    p.add_argument("--model", default=os.environ.get("BASE_MODEL", "NousResearch/Hermes-3-Llama-3.1-8B"),
                   help="HF model id or local path")
    p.add_argument("--data", default="data/train.jsonl", help="JSONL with a 'text' field")
    p.add_argument("--out", default="out/adapter", help="where to save the LoRA adapter")
    p.add_argument("--epochs", type=float, default=3.0)
    p.add_argument("--lr", type=float, default=2e-4)
    p.add_argument("--batch-size", type=int, default=1)
    p.add_argument("--grad-accum", type=int, default=8)
    p.add_argument("--max-len", type=int, default=1024)
    p.add_argument("--rank", type=int, default=16, help="LoRA rank r")
    p.add_argument("--alpha", type=int, default=32, help="LoRA alpha")
    p.add_argument("--4bit", dest="use_4bit", action="store_true", help="QLoRA 4-bit base")
    return p.parse_args(argv)


def format_example(row: dict) -> str:
    """Adapt this to your hermes-local chat/template format."""
    if "text" in row:
        return row["text"]
    if "prompt" in row and "response" in row:
        return f"<|user|>\n{row['prompt']}\n<|assistant|>\n{row['response']}"
    raise KeyError("each row needs 'text' or ('prompt' and 'response')")


def main(argv=None) -> int:
    args = parse_args(argv)

    try:
        import torch
        from datasets import load_dataset
        from peft import LoraConfig, get_peft_model
        from transformers import (AutoModelForCausalLM, AutoTokenizer,
                                   DataCollatorForLanguageModeling, Trainer,
                                   TrainingArguments)
    except ImportError as e:
        print(f"[setup] missing dependency: {e}. Install with:\n"
              "  colab install -s ft torch transformers peft datasets accelerate bitsandbytes",
              file=sys.stderr)
        return 2

    if not torch.cuda.is_available():
        print("[warn] no CUDA device visible — are you running on a --gpu VM?", file=sys.stderr)
    else:
        print(f"[gpu] {torch.cuda.get_device_name(0)}  "
              f"({torch.cuda.get_device_properties(0).total_memory // 1024**3} GB)")

    if not os.path.exists(args.data):
        print(f"[error] dataset not found: {args.data}", file=sys.stderr)
        return 1

    tok = AutoTokenizer.from_pretrained(args.model, use_fast=True)
    if tok.pad_token is None:
        tok.pad_token = tok.eos_token

    quant = None
    if args.use_4bit:
        from transformers import BitsAndBytesConfig
        quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                   bnb_4bit_compute_dtype=torch.bfloat16)

    model = AutoModelForCausalLM.from_pretrained(
        args.model, quantization_config=quant,
        torch_dtype=torch.bfloat16, device_map="auto")
    model = get_peft_model(model, LoraConfig(
        r=args.rank, lora_alpha=args.alpha, lora_dropout=0.05, bias="none",
        task_type="CAUSAL_LM",
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]))
    model.print_trainable_parameters()

    ds = load_dataset("json", data_files=args.data, split="train")

    def tokenize(row):
        out = tok(format_example(row), truncation=True, max_length=args.max_len)
        return out

    ds = ds.map(tokenize, remove_columns=ds.column_names)

    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir=args.out, num_train_epochs=args.epochs,
            per_device_train_batch_size=args.batch_size,
            gradient_accumulation_steps=args.grad_accum,
            learning_rate=args.lr, bf16=True, logging_steps=10,
            save_strategy="epoch", report_to="none"),
        train_dataset=ds,
        data_collator=DataCollatorForLanguageModeling(tok, mlm=False),
    )
    trainer.train()

    os.makedirs(args.out, exist_ok=True)
    model.save_pretrained(args.out)
    tok.save_pretrained(args.out)
    with open(os.path.join(args.out, "train_meta.json"), "w") as f:
        json.dump(vars(args), f, indent=2)
    print(f"[done] adapter saved to {args.out} — download it, then `colab stop`.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
