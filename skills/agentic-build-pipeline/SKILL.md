---
name: agentic-build-pipeline
description: Split a complex creative build (game, 3D scene, app, long video) into a planning pass and one or more parallel builder passes using the Agent tool, then a review/iterate pass — instead of one model trying to do everything in one shot. Use when the user wants to build something ambitious in one sitting, says "에이전트로 만들어줘", "서브에이전트로 나눠서", "설계하고 구현해줘", "체이닝해서 만들어줘", "에이전트 여러 개로 빌드", or references chaining a reasoning model with a fast execution model.
license: MIT
---

# Agentic Build Pipeline

The pattern behind "design model plans, build model executes, repeat" showcases (a reasoning agent chaining into a fast generation agent, ten agents each building one district of a city, a storyboard agent handing off to an animation agent). You don't need two different AI products to do this — Claude's own Agent tool, used in three distinct passes, gets the same structural benefit: **separate thinking from doing, and parallelize the doing.**

## When to use
- A build is big enough that one pass tends to produce something generic, broken, or inconsistent across parts (a multi-room scene, a multi-system game, a multi-section video, a multi-page app)
- The user explicitly wants a staged/chained/multi-agent workflow
- Variations: "10 agents built a city" (spatial partition), "storyboard → animation" (sequential handoff), "Opus plans → Fable builds" (reasoning/execution split)

## The three passes

### Pass 1 — Plan (one agent, foreground, high reasoning)
Do this yourself or spawn one `Agent` call with a reasoning-heavy prompt. Output a **tight, concrete spec** — not prose, a literal checklist the builder(s) can't misinterpret:
- A fixed **style key**: 3-5 adjectives + a concrete reference ("low-poly, pastel, Ghibli-lit, no textures") that every builder pass must repeat verbatim in its own prompt. This is the #1 failure mode without it: parallel builders drift to different styles.
- A **component/section list** with boundaries that don't overlap (rooms in a house, districts in a city, shots in a video, systems in a game: movement / combat / UI).
- **Shared constraints** every builder inherits: tech stack, performance budget, naming conventions, file layout.
- **Acceptance criteria** per component — what "done" looks like, checkable by the review pass.

Never skip straight to building without this artifact existing as text first. If the plan is vague, the parallel step amplifies the vagueness N times instead of catching it once.

### Pass 2 — Build (parallel Agent calls, one per component)
Spawn one `Agent` call per independent component from the plan, **in a single message** (true parallelism — see the Agent tool's own guidance on batching independent calls). Each prompt must include, verbatim:
1. The style key from Pass 1
2. That component's spec + acceptance criteria only — don't hand every builder the whole plan, that's how they start improvising on each other's territory
3. The shared constraints (stack, conventions)
4. Explicit file/namespace ownership so parallel outputs don't collide (e.g. "write only to `rooms/kitchen.js`, export `buildKitchen()`")

Use `isolation: "worktree"` when builders touch the same repo/files, so parallel edits can't stomp each other.

### Pass 3 — Integrate & review (one agent or yourself)
- Assemble the builder outputs (import/compose them into the whole).
- Check each acceptance criterion from the plan against the actual result — for visual work, this means actually looking (render/screenshot/open the artifact), not just reading code.
- **Only re-run the builder(s) that failed**, with a correction note added to their original prompt. Don't restart the whole pipeline over one broken component — that's the entire point of having split it.

## Failure modes this avoids (and still watch for)
| Symptom | Cause | Fix |
|---|---|---|
| Parts look like different projects glued together | No shared style key in Pass 1, or builders didn't repeat it verbatim | Put the style key in EVERY builder prompt, not just the plan doc |
| Builders overwrite each other's work | No explicit file/namespace ownership | Assign exclusive paths per builder, use worktree isolation for shared repos |
| One weak component drags down review | Treating review as pass/fail on the whole instead of per-component | Score each acceptance criterion independently; only redo the failing ones |
| Endless re-plan loops | Plan was vague enough that "done" is undefined | Pass 1 isn't finished until acceptance criteria are concrete/checkable, not vibes |

## Minimal 3-component example (sizing: keep it small — this is a pattern, not a mandate to always spawn 10 agents)
1. Plan pass: "Design a 3-room dollhouse scene: kitchen, bedroom, living room. Style key: low-poly, warm pastel, soft shadows, no textures. Each room: 4x4 units, shares a wall with the next. Acceptance: distinct furniture silhouettes readable from a 45° top-down camera."
2. Build pass (3 parallel `Agent` calls): one per room, each given only its room's spec + the style key + the shared wall coordinates.
3. Review pass: open the composed scene, check all three rooms render, share walls correctly, and read as the same style at a glance. Re-run only the room(s) that don't.
