---
name: no-asset-3d-scene
description: Build a 3D scene, game, or visual effect from pure code — zero external 3D models, textures, or images — as a self-contained Three.js artifact. Use when the user wants a 3D scene, a browser game, a shader/visual effect, a procedural landscape, a voxel world, or any "no assets" / "from scratch" 3D build, or says things like "에셋 없이 3D 만들어줘", "순수 코드로 장면/게임 만들어줘", "셰이더 효과", "복셀/절차적 지형".
license: MIT
---

# No-Asset 3D Scene

Everything is generated: geometry is procedural, materials are shaders or solid colors, lighting is computed, not baked. No image downloads, no model files, no network calls at runtime. Ships as a single self-contained HTML Claude Artifact (Three.js via CDN) so it runs immediately with no install.

Inspired by a cluster of recent showcases (jeep models, FPS games, voxel engines, procedural flower fields, oil-painting shaders, ink-calligraphy simulations) that all share this one constraint: **build the look, don't import it.**

## When to use
- "3D [scene/game/effect] 만들어줘, 에셋 없이"
- "순수 코드로 [풍경/게임/오브젝트]"
- Shader effects, procedural terrain, voxel worlds, particle systems
- A browser game that should run from one HTML file

## Decision tree — pick the right technique first

| What they want | Technique |
|---|---|
| A specific object (vehicle, furniture, device) | Compose from primitives (Box/Cylinder/Sphere/Cone geometries), boolean-ish layering, no single mesh does everything |
| A landscape/terrain | Perlin/Simplex noise → displace a PlaneGeometry's vertices → vertex colors by height, no texture |
| Many of the same thing (flowers, cells, rocks) | `InstancedMesh` — one draw call for thousands of instances, vary via instance matrix |
| A painterly/stylized look | Fragment shader post-process pass (ShaderMaterial or a full-screen EffectComposer pass), not a texture |
| A voxel world | Greedy meshing — merge coplanar faces of adjacent same-type voxels into single quads; never render 1 mesh per cube (kills performance past a few thousand voxels) |
| A fluid/ink/smoke look | Canvas2D diffusion step (simple cellular blur pass) or a GPU shader with a feedback buffer |
| A game | Three.js + `PointerLockControls` (FPS) or `OrbitControls` (third-person/puzzle) + a physics lib (Cannon-es/Rapier) only if real collisions are needed — otherwise hand-rolled AABB checks are enough and lighter |

## Build order (do this every time, don't skip steps)
1. **Scene skeleton first**: camera, one light, a ground plane, orbit controls. Verify it renders before adding anything procedural — isolates "nothing shows up" bugs early.
2. **Geometry**: build the procedural shapes per the decision tree. Keep each generator a pure function (seed in, mesh/geometry out) so it's easy to iterate on parameters.
3. **Material/shader**: start with a flat `MeshStandardMaterial` to confirm geometry is right, THEN swap in the shader/stylization. Debugging geometry and shader at once is slow.
4. **Lighting**: one key light + ambient/hemisphere fill is enough for 90% of these. Don't reach for baked lightmaps — there's nothing to bake from.
5. **Interaction/animation last**: once the static scene looks right, add camera movement, game loop, or physics.

## Performance rules (these are what separates a working demo from a frozen tab)
- **Instance, don't duplicate.** Hundreds of individual `Mesh` objects = hundreds of draw calls = dead frame rate. `InstancedMesh` for anything repeated more than ~20 times.
- **Merge static geometry.** Non-moving scene parts: merge into one `BufferGeometry` via `BufferGeometryUtils.mergeGeometries` instead of many meshes.
- **Cap particle/voxel counts before you start**, don't discover the limit by freezing the tab. Rough budget for a smooth artifact: ≤ ~50k instanced objects, ≤ ~200k triangles total.
- **Shaders over textures for style** — a procedural noise-based fragment shader is both zero-asset AND usually cheaper than loading a texture that doesn't exist anyway.

## Artifact mechanics
- Load `three.js` from a CDN per the artifact rules (jsdelivr/unpkg/cdnjs) — never bundle it inline.
- Load `artifact-design` skill before writing, for the page shell (title, dark/light theming, phone-width layout) — the 3D canvas itself should fill its container and stay responsive to resize events (`window.addEventListener('resize', ...)`).
- `requestAnimationFrame` loop; stop it (don't leak) if the artifact page is reloaded/republished.

See `references/snippets.md` for ready-to-adapt code for the techniques above.
