# Code snippets — no-asset 3D techniques

All examples assume `three` is loaded globally (ESM via CDN import map, or `THREE` global via classic script tag).

## Scene skeleton (always start here)
```js
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(60, innerWidth/innerHeight, 0.1, 1000);
camera.position.set(0, 5, 10);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);

scene.add(new THREE.HemisphereLight(0xffffff, 0x444444, 1.2));
const key = new THREE.DirectionalLight(0xffffff, 1.5);
key.position.set(5, 10, 5);
scene.add(key);

const controls = new THREE.OrbitControls(camera, renderer.domElement);

addEventListener('resize', () => {
  camera.aspect = innerWidth/innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
});

(function loop(){
  requestAnimationFrame(loop);
  controls.update();
  renderer.render(scene, camera);
})();
```

## Procedural terrain (noise-displaced plane, vertex-colored, no texture)
```js
function buildTerrain(size = 50, segments = 100) {
  const geo = new THREE.PlaneGeometry(size, size, segments, segments);
  geo.rotateX(-Math.PI / 2);
  const pos = geo.attributes.position;
  const colors = [];
  for (let i = 0; i < pos.count; i++) {
    const x = pos.getX(i), z = pos.getZ(i);
    const h = noise2D(x * 0.1, z * 0.1) * 4; // plug in any 2D noise fn
    pos.setY(i, h);
    const t = (h + 4) / 8; // 0..1
    const c = new THREE.Color().setHSL(0.3 - t * 0.2, 0.5, 0.3 + t * 0.3);
    colors.push(c.r, c.g, c.b);
  }
  geo.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
  geo.computeVertexNormals();
  return new THREE.Mesh(geo, new THREE.MeshStandardMaterial({ vertexColors: true }));
}
```

## Instancing (thousands of the same object, one draw call)
```js
function buildFlowerField(count = 5000, areaSize = 40) {
  const geo = new THREE.ConeGeometry(0.1, 0.4, 5);
  const mat = new THREE.MeshStandardMaterial({ color: 0xff6699 });
  const mesh = new THREE.InstancedMesh(geo, mat, count);
  const m = new THREE.Matrix4();
  for (let i = 0; i < count; i++) {
    const x = (Math.random() - 0.5) * areaSize;
    const z = (Math.random() - 0.5) * areaSize;
    m.compose(
      new THREE.Vector3(x, 0, z),
      new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(0,1,0), Math.random()*Math.PI*2),
      new THREE.Vector3(1,1,1).multiplyScalar(0.7 + Math.random()*0.6)
    );
    mesh.setMatrixAt(i, m);
  }
  return mesh;
}
```

## Stylized/painterly post-process shader (minimal fragment shader pass)
```glsl
// fragment shader sketch — apply via a full-screen quad or EffectComposer ShaderPass
uniform sampler2D tDiffuse;
varying vec2 vUv;
void main() {
  vec3 color = texture2D(tDiffuse, vUv).rgb;
  // posterize + edge-darken for an "oil painting" feel
  color = floor(color * 6.0) / 6.0;
  float edge = smoothstep(0.0, 0.1, length(fwidth(color)));
  gl_FragColor = vec4(mix(color, vec3(0.0), edge * 0.4), 1.0);
}
```

## Voxel world — greedy meshing (concept, not full implementation)
Never do `one Mesh per voxel`. Instead:
1. Store voxels in a 3D typed array (`Uint8Array` of type IDs).
2. For each of the 6 face directions, scan the grid and merge adjacent same-type, same-facing faces into the largest possible rectangle (classic 2D rectangle-merge per slice).
3. Emit one `BufferGeometry` with all merged quads — typically reduces a 32³ voxel world from ~100k+ individual faces to a few thousand.
4. Reference algorithm: "Greedy Meshing" (Mikola Lysenko's writeup) — same idea applies regardless of language.

## Simple AABB collision (skip a physics engine for most games)
```js
function aabbIntersect(a, b) { // a, b = {min: Vector3, max: Vector3}
  return (a.min.x <= b.max.x && a.max.x >= b.min.x) &&
         (a.min.y <= b.max.y && a.max.y >= b.min.y) &&
         (a.min.z <= b.max.z && a.max.z >= b.min.z);
}
```
Good enough for platformers/FPS pickups/arena bounds. Reach for Cannon-es/Rapier only when you need realistic rigid-body physics (stacking, ragdolls, constraints).

## Ink/fluid diffusion (Canvas2D, no WebGL needed)
```js
// one diffusion step over a Float32Array `ink[width*height]`
function diffuse(ink, width, height, rate = 0.1) {
  const next = new Float32Array(ink.length);
  for (let y = 1; y < height-1; y++) {
    for (let x = 1; x < width-1; x++) {
      const i = y*width+x;
      const avg = (ink[i-1]+ink[i+1]+ink[i-width]+ink[i+width]) / 4;
      next[i] = ink[i] + (avg - ink[i]) * rate;
    }
  }
  return next;
}
```
