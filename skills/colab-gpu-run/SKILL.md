---
name: colab-gpu-run
description: Offload a GPU/TPU job to Google Colab from the terminal using the official `google-colab-cli`. Use when the user wants to train a model, run LoRA fine-tuning, execute a heavy FEM/CFD or compute script, or run any Python/.ipynb on a cloud A100/H100/L4/T4/TPU without a local GPU — provision a VM, run a local script, retrieve outputs, and shut the VM down to stop billing.
license: MIT
---

# Colab GPU Run

Run heavy jobs on Colab cloud GPUs/TPUs straight from the shell via `colab` (package `google-colab-cli`, by the official `googlecolab` org). Pattern: **provision → install deps → run local script → download outputs → stop**.

The headline win is the *ephemeral* `colab run`: VM is created, runs the script, and self-terminates — so an idle GPU never quietly bills you.

## When to use
- "Train / fine-tune this on a GPU", "run LoRA on an A100", "I have no local GPU"
- "Run this heavy script / notebook in the cloud and get the results"
- "Offload this FEM/CFD/batch job"

## Preconditions (check first)
- **OS:** Linux or macOS only. On Windows, use WSL2 — native Windows is unsupported.
- **Installed?** Check `colab version`. If missing: `uv tool install google-colab-cli` (or `pip install google-colab-cli`).
- **Auth:** first run opens a browser OAuth once; `adc` (default) or `oauth2`. GPU tiers (H100/A100) depend on the user's Colab subscription/quota — surface this, don't assume availability.

## Decision: `run` vs. persistent session
- **One-shot job (preferred)** — a single script, no iteration → `colab run`. Auto-creates and auto-stops the VM. Cheapest, simplest.
- **Iterative work** — install deps once, run many times, inspect files between runs → named session (`colab new -s ...` → `exec`/`download` → `stop`). Remember the explicit `stop`.

## Workflow A — one-shot (default)
```bash
colab run --gpu A100 train.py --epochs 3            # provision → run → auto-stop
colab run --gpu L4 --keep infer.py                  # --keep leaves VM up for inspection
```
`run` reads the local script and forwards trailing args; no manual upload. After `--keep`, remember to `colab stop`.

## Workflow B — persistent session
```bash
colab new -s job --gpu A100            # or --tpu v5e1 ; omit for CPU
colab auth -s job                      # only if the job needs GCP/Drive
colab install -s job -r requirements.txt   # or: colab install -s job torch transformers
colab drivemount -s job                # optional: large data/outputs via Drive
colab exec -s job -f train.py          # runs local .py or .ipynb (content sent automatically)
colab download -s job checkpoints/model.bin ./model.bin
colab log -s job -o run.md             # export history (.ipynb/md/txt/jsonl)
colab stop -s job                      # ALWAYS stop to end billing
```

## Rules of thumb
- **Always stop.** Every `new` (and every `run --keep`) must be matched by a `stop`. If you create a VM, you are responsible for tearing it down.
- **Automation-safe execution:** use `exec` with `-f FILE` or piped stdin. Avoid `repl`/`console` (need a local TTY) in non-interactive flows.
- **Move data efficiently:** small files ride along with `exec`; big datasets/outputs go through `drivemount` or explicit `upload`/`download`, not inline.
- **`-s` is optional when exactly one session exists.**
- Pick the smallest GPU that fits (T4/L4 for inference & light training; A100/H100 for large training). State the choice and why.
- Don't invent quota/pricing. If provisioning fails on availability, report it and suggest a smaller tier or retry.

See `references/cheatsheet.md` for the full command map and ready-to-adapt recipes.
