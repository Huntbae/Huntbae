# google-colab-cli cheatsheet

Official CLI from the `googlecolab` org. Package: `google-colab-cli`. Command: `colab`. Linux/macOS only.

## Install & maintain
```bash
uv tool install google-colab-cli     # recommended
pip install google-colab-cli         # alternative
colab version
colab update --install
```

## Global options
- `--auth {adc|oauth2}` — auth strategy (default `adc`)
- `-c, --client-oauth-config PATH` — OAuth client config
- `--config PATH` — session metadata file (default `~/.config/colab-cli/sessions.json`)
- `--logtostderr` — debug logging
- `-s, --session NAME` — target session (omit when only one exists)

## Command map
### Session
| Command | Purpose |
|---|---|
| `colab new [-s NAME] [--gpu GPU] [--tpu TPU]` | allocate runtime |
| `colab sessions` | list sessions |
| `colab status [-s NAME]` | hardware/status |
| `colab restart-kernel [-s NAME]` | restart kernel |
| `colab stop [-s NAME]` | terminate (stops billing) |
| `colab url [-s NAME] [--open]` | browser connection |

### Execution
| Command | Purpose |
|---|---|
| `colab run [--gpu GPU] [--tpu TPU] [--keep] SCRIPT [ARGS...]` | fresh VM → run → auto-stop |
| `colab exec [-s NAME] [-f FILE] [--output-image PATH]` | run stdin / .py / .ipynb |
| `colab repl [-s NAME]` | interactive Python (needs local TTY) |
| `colab console [-s NAME]` | raw tmux TTY (needs local TTY) |

### Files
| Command | Purpose |
|---|---|
| `colab ls [-s NAME] [PATH]` | list remote |
| `colab upload [-s NAME] LOCAL REMOTE` | upload |
| `colab download [-s NAME] REMOTE LOCAL` | download |
| `colab rm [-s NAME] PATH` | delete remote |
| `colab edit [-s NAME] PATH` | edit remote with local editor |

### Automation / utility
| Command | Purpose |
|---|---|
| `colab auth [-s NAME]` | authenticate GCP services |
| `colab drivemount [-s NAME] [PATH]` | mount Google Drive |
| `colab install [-s NAME] [-r FILE \| PKG...]` | install deps via uv/pip |
| `colab log [-s NAME] [-n N] [-o FILE]` | view/export history (.ipynb/md/txt/jsonl) |
| `colab pay` | subscription management |

## Accelerators
- GPU: `T4`, `L4`, `G4`, `H100`, `A100`
- TPU: `v5e1`, `v6e1`
- Omit `--gpu/--tpu` for CPU.

## Recipes

### LoRA / fine-tune, keep only the checkpoint
```bash
colab new -s ft --gpu A100
colab install -s ft -r requirements.txt
colab exec -s ft -f finetune_lora.py
colab download -s ft out/adapter.safetensors ./adapter.safetensors
colab stop -s ft
```

### One-shot batch (e.g. FEM/CFD/eval), no leftover VM
```bash
colab run --gpu L4 run_batch.py --case engine_bracket
```

### Notebook run with Drive-backed data
```bash
colab new -s nb
colab drivemount -s nb
colab exec -s nb -f analysis.ipynb
colab log -s nb -o analysis_log.md
colab stop -s nb
```

### Shebang: make a script self-run on GPU
```python
#!/usr/bin/env -S colab run --gpu L4 --keep
# ./script.py  -> provisions an L4 and runs there
```

## Gotchas
- Windows unsupported → use WSL2/macOS/Linux.
- Always `stop` what you `new`/`--keep`.
- `repl`/`console` need a TTY; for automation use `exec -f` or piped stdin.
- GPU availability/billing follow the user's Colab plan — don't assume H100/A100 is free.
