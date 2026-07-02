# Music video pipeline — exact commands

Project layout (create per song):
```
mv-project/
  song.mp3          # SUNO download
  lyrics.txt        # SUNO page copy
  photos/           # user photos
  keyframes/        # step 3 output
  clips/            # step 4 output  (001.mp4, 002.mp4 … shot-plan order)
  shot-plan.md      # from references/shot-plan.md
  final/
```

## Step 1 — timing & stems
```bash
# Per-line lyric timestamps (scene boundaries)
whisper song.mp3 --model small --output_format srt --output_dir .

# Vocal-only stem for Wan S2V lip-sync (optional but better)
demucs --two-stems=vocals song.mp3      # -> separated/htdemucs/song/vocals.wav
```
Map SRT timestamps onto lyric sections → fill the time column of the shot plan.

## Step 2 — shot plan
Fill `shot-plan.md`. Rules of thumb:
- 3–6s per shot; a 3-min song ≈ 35–50 shots, BUT start with a 30–45s excerpt (8–12 shots) as a pilot.
- Chorus = strongest visuals, can reuse a hero shot with variations (same seed, prompt deltas).
- Alternate hero (user) shots and b-roll to hide identity drift.
- Get user approval before rendering.

## Step 3 — keyframes
Via comfyui-mcp conversation or `/comfy:gen`; log every prompt/seed back into the shot plan.
- b-roll: t2i with the shot prompt + a global style suffix (same suffix on every shot = coherent look).
- hero: i2i from `photos/best.jpg` (denoise 0.35–0.55 keeps the face) or IP-Adapter/PuLID for scene changes with the same face.
- Draw Things path: same, through the Draw Things MCP (t2i/i2i).

## Step 4 — clips
- **Hero + music sync:** Wan 2.2 **S2V** — inputs: keyframe (or raw photo), audio segment for that shot's time range, and the shot prompt. Cut segments first:
  ```bash
  ffmpeg -i separated/htdemucs/song/vocals.wav -ss 00:00:12 -t 5 -c copy seg_003.wav
  ```
- **B-roll:** Wan 2.2 **i2v** from the keyframe with a motion prompt ("slow dolly-in, hair moving in wind"). LTX for quick drafts, Wan for finals.
- 480p (448×768 / 768×448) on ≤16GB; 720p on 24GB+. 81 frames @16fps ≈ 5s.
- Name outputs by shot number: `clips/003.mp4`.
- No local GPU headroom? render clips remotely with the **colab-gpu-run** skill and download them back.

## Step 5 — assemble
```bash
cd mv-project
# 5a. normalize clips (same fps/size/pixfmt) — avoids concat glitches
for f in clips/*.mp4; do
  ffmpeg -y -i "$f" -r 24 -vf "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2" \
    -c:v libx264 -crf 18 -an "norm_$(basename $f)"
done
# 5b. concat list in shot order
ls norm_*.mp4 | sed "s/^/file '/;s/$/'/" > list.txt
# 5c. concat + mux the ORIGINAL full song as the only audio
ffmpeg -y -f concat -safe 0 -i list.txt -i song.mp3 \
  -map 0:v -map 1:a -c:v libx264 -crf 18 -c:a aac -b:a 192k -shortest final/mv.mp4
```
Optional crossfade between two clips (repeat pairwise or use xfade filtergraph):
```bash
ffmpeg -i a.mp4 -i b.mp4 -filter_complex \
  "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=4.5" ab.mp4
```
Vertical (Shorts/Reels): swap scale/pad to `720:1280`.

## Step 6 — review
Total video length must cover the song (`-shortest` trims). Rewatch; for weak shots, re-render ONLY those clip numbers using the logged prompt/seed with deltas, re-run 5b–5c.

## Failure quick-map
| Symptom | Fix |
|---|---|
| OOM during video | 5B model, 480p, fewer frames; close other apps; or colab-gpu-run |
| Face drifts between shots | i2i lower denoise; IP-Adapter/PuLID; reuse one hero keyframe |
| Lip-sync off | feed vocal stem (not full mix) to S2V; align segment start to SRT |
| Concat stutters/glitches | you skipped 5a normalization |
| Style inconsistent | one global style suffix + same checkpoint/LoRA for all keyframes |
