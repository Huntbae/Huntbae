# Shot plan — <SONG TITLE>

- **Song:** <file> · <length> · <BPM/tempo feel>
- **Mood/story (from lyrics):** <2–3 lines>
- **Global look:** <e.g. "cinematic, teal-orange, 35mm film grain"> ← appended to EVERY prompt
- **Aspect:** <16:9 | 9:16> · **Target:** <pilot 40s | full song>
- **Backend/models:** <ComfyUI: Flux + Wan2.2-14B + S2V | Draw Things: ...>
- **Hero reference photo:** photos/<file>

| # | Section | Time | Scene (what we see) | Prompt (final, with style suffix) | Source | Type | Motion note | Seed | Status |
|---|---------|------|--------------------|-----------------------------------|--------|------|-------------|------|--------|
| 001 | Intro | 0:00–0:05 | | | t2i | i2v | slow dolly-in | | ☐ |
| 002 | Verse 1 | 0:05–0:10 | | | photos/best.jpg | **S2V** (hero, lip-sync) | | | ☐ |
| 003 | Verse 1 | 0:10–0:15 | | | t2i | i2v | | | ☐ |
| … | | | | | | | | | |

Type legend: **S2V** = photo+audio sync (hero) · i2v = keyframe→video (b-roll) · t2v = abstract, no keyframe · v2v = restyle existing clip

Rules: every render logs its prompt+seed here · user approves plan before step 4 · re-renders change ONLY the target row.
