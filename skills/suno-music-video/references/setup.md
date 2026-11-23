# One-time setup

## Path A — ComfyUI + comfyui-mcp (recommended hub; Mac/Win/Linux)

1. **Install ComfyUI** (Desktop app from comfy.org, or portable/manual).
2. **Connect Claude Code** — add the MCP server:
   ```jsonc
   // ~/.claude/settings.json
   {
     "mcpServers": {
       "comfyui": {
         "command": "npx",
         "args": ["-y", "comfyui-mcp"],
         "env": { "CIVITAI_API_TOKEN": "" }   // optional, for CivitAI downloads
       }
     }
   }
   ```
3. **Install the plugin** (slash commands + 29 skills):
   ```
   /plugin marketplace add artokun/comfyui-mcp
   /plugin install comfy
   ```
4. Models auto-download from HuggingFace/CivitAI on first use. For this pipeline you'll want:
   - Image: Flux (or SDXL/Qwen-Image)
   - Video: **Wan 2.2** (5B for ≤8-12GB VRAM, 14B for 16-24GB), Wan 2.2 **S2V**
   - Identity: IP-Adapter / PuLID weights
5. Smoke test: `> Generate an image of a sunset over mountains` then `/comfy:debug` if anything fails.

## Path B — Draw Things + MCP (Mac Apple Silicon, easiest images)

1. Install **Draw Things** (Mac App Store, free).
2. In Draw Things: Settings → **API Server ON** (default `127.0.0.1:7860`).
3. Add an MCP bridge, e.g. `james-see/mcp-drawthings`:
   ```jsonc
   { "mcpServers": { "drawthings": { "command": "uvx", "args": ["mcp-drawthings"] } } }
   ```
   (Any Draw Things MCP works; they all hit the same HTTP API.)
4. Download models inside Draw Things: an image model (Flux/SDXL) + **Wan 2.2** for video.
5. 16GB+ unified memory recommended for video; M-series required.

## Shared utilities (both paths)

```bash
# ffmpeg — assembly;  whisper — lyric timestamps;  demucs — vocal stem for S2V
brew install ffmpeg            # (or apt/winget)
pip install openai-whisper demucs
```

## Sanity checklist before a render session
- [ ] Backend reachable (ComfyUI at :8188 or Draw Things API at :7860)
- [ ] Video model present (Wan 2.2 / S2V downloaded)
- [ ] Song file + lyrics + user photos collected in one project folder
- [ ] Free disk ≥ 20GB (models + clips)
