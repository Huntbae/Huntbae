---
name: suno-music-video
description: Turn a SUNO (or any) song plus the user's photos into a music video using LOCAL AI — ComfyUI (via comfyui-mcp) or Draw Things on Mac. Use when the user wants to make a music video from a song, generate lyric-matched scenes, animate their photo to music (Wan 2.2 S2V lip-sync), or run text-to-image / image-to-image / text-to-video / image-to-video / video-to-video locally and assemble clips with ffmpeg.
license: MIT
---

# SUNO → Local AI Music Video

Direct a music video like a filmmaker: **Claude plans, local AI renders, ffmpeg assembles.**
Song (SUNO) + user photos → lyric/mood analysis → shot plan → keyframes → clips → final MV.

## Backends (pick what's installed — check first)
| Backend | OS | Connect | Strength |
|---|---|---|---|
| **ComfyUI + `comfyui-mcp`** (artokun) | Mac/Win/Linux | MCP server + Claude Code plugin (`/plugin marketplace add artokun/comfyui-mcp`) | Full pipeline: Flux/Qwen images, **Wan 2.2 i2v/S2V**, LTX video, model auto-download |
| **Draw Things + `mcp-drawthings`** | Mac (Apple Silicon) | Draw Things app → enable API Server (port 7860) → MCP server | Fastest native Mac images; Wan 2.2 video (5B=speed, 14B=quality) |

If neither is reachable, stop and walk the user through setup (see `references/setup.md`). Never pretend a generation happened.

## Inputs to collect
1. **Song file** (SUNO download, .mp3/.wav) and **lyrics** (SUNO page copy-paste).
2. **User photos** — the subject to feature. Confirm the photos are of the user or someone who consented.
3. **Look**: cinematic / anime / dreamy / retro etc., aspect ratio (16:9, 9:16 for Shorts/Reels), target length.

## Workflow (per `references/pipeline.md` for exact commands)

### 1 — Analyze the song (Claude, no GPU)
Parse lyrics into sections (intro/verse/chorus/bridge/outro), extract mood, imagery, story beats, tempo. If timing is unknown, get per-line timestamps with local Whisper (`whisper song.mp3 --output_format srt`).

### 2 — Shot plan (the creative core)
Fill `references/shot-plan.md`: one row per shot — section, time range, scene description, prompt, which user photo (if any), motion note, backend/model. Aim 3–6s per clip; chorus shots can repeat with variation. **Show the plan to the user for approval before rendering** — GPU time is expensive.

### 3 — Keyframes (t2i / i2i)
- Scenes without the user: text-to-image (Flux/Qwen/SDXL).
- Scenes with the user: image-to-image or IP-Adapter/PuLID identity transfer from their photo so the face stays consistent across shots. Keep seed/style params logged.

### 4 — Clips (the money step)
- **Hero shots (user singing/appearing):** **Wan 2.2 S2V** — one photo/keyframe + the song segment → audio-synchronized motion & lip-sync. Feed the *vocal-only* stem when possible (separate with demucs).
- **B-roll:** Wan 2.2 **i2v** from keyframes (or t2v for abstract shots). LTX for fast drafts.
- Render at 480–720p, 3–6s each. Verify each clip before the next (fail fast).

### 5 — Assemble (ffmpeg)
Concat clips in shot-plan order, mux the ORIGINAL SUNO track as the only audio, optional crossfades, export final .mp4. Exact commands in `references/pipeline.md`.

### 6 — Review loop
Play the result; re-render only the weak shots (their prompts/seeds are all in the shot plan — that's why we log them).

## Guardrails
- **VRAM/RAM reality:** Wan 2.2 needs ~8GB VRAM (5B) to 24GB (14B); Mac needs 16GB+ unified memory. On weak hardware: 480p, 5B, shorter clips — or offload rendering with the `colab-gpu-run` skill and keep only planning local.
- **Identity/likeness:** only animate photos of the user or people who consented. Refuse celebrity/third-party face swaps.
- **One clip at a time.** Verify before batching; a bad prompt burned across 12 shots wastes an evening.
- SUNO output ownership follows the user's SUNO plan — remind them before publishing (YouTube monetization needs a paid plan).
- Keep every prompt/seed/model in the shot plan file — reproducibility is the whole point.
