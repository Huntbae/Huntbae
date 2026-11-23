# colab-gpu-run examples

Ready-to-adapt scripts the `colab-gpu-run` skill knows how to launch. Drop them
into the target repo, adjust the marked points, and run via `colab`.

| Script | For | What it does | Run |
|---|---|---|---|
| `finetune_lora.py` | **hermes-local** | LoRA / QLoRA fine-tune of a HF causal LM, saves the adapter | `colab run --gpu A100 finetune_lora.py --data data/train.jsonl --epochs 3` |
| `run_batch.py` | **autodesign-llm** | Batch design validation; analytic dry-run by default, real FEM/CFD via `SOLVER_CMD` injection; writes JSON+Markdown report | `colab run --gpu L4 run_batch.py --cases cases.json` |

Both carry a `#!/usr/bin/env -S colab run ...` shebang, so once `google-colab-cli`
is installed and `chmod +x`'d they self-provision a VM: `./finetune_lora.py`.

## Notes
- `run_batch.py` runs with **no GPU and no solver** out of the box (built-in demo
  cases) — safe to test locally first: `python run_batch.py`.
- `finetune_lora.py` needs `transformers peft datasets accelerate torch`
  (+`bitsandbytes` for `--4bit`). Install on the VM with
  `colab install -s ft -r requirements.txt`.
- Adaptation points are commented: `format_example()` (chat template),
  `BASE_MODEL`, LoRA `target_modules`, and `solver_check()` (your real solver).
- Always `colab stop` when done — see the skill's guardrails.
