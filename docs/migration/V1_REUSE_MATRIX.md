# Trash Dash V1 reuse matrix

Audit date: 2026-08-11

V1 path: `/Users/jamesschmittler/Documents/Portfolio/trash-dash`

V1 remote: `https://github.com/jschmittler/trash-dash-alley-acres.git`

Audit mode: read-only; no V1 files were copied during this audit.

## Executive decision

V2 is a clean-room implementation informed by V1 behavior and lessons, not a source migration. Approved design documents and their manifests are the only material approved for direct import. Reusable V1 ideas must be rewritten behind V2 contracts unless this matrix is explicitly amended after a module-level review.

## Matrix

| Area | V1 finding | Classification | V2 action |
|---|---|---|---|
| 1. Engine and framework | React 19.2.6 and Next 16.2.6 via Vinext/Vite; gameplay is a custom 960×540 HTML5 Canvas loop concentrated in `app/trash-dash-game.tsx`. | REWRITE FOR V2 | Keep browser delivery as a candidate, but do not copy the React/Canvas runtime. Select and scaffold the V2 engine only after `ENGINE_DECISION.md` questions are accepted. |
| 2. Build and package configuration | Node >=22.13, npm lockfile, Vinext/Vite, Cloudflare plugin, Tailwind/PostCSS, TypeScript, ESLint, plus a separate Vite GitHub Pages build. | REUSE WITH ADAPTATION | Reuse version-pinning, deterministic install, lint/test/build separation, and CI concepts. Create new package/build files after engine selection; do not copy V1 configuration wholesale. |
| 3. Input system | React-managed `Set<string>` keyboard state; keydown/up for arrows/A-D, Space, Shift, E, M and pause/fullscreen flows; pointer-capture touch buttons; lifecycle clearing through mobile-experience helpers. | REUSE WITH ADAPTATION | Preserve action semantics, held-input clearing, touch parity, and interruption handling as behavioral requirements. Rewrite through the selected engine's input abstraction and add real-device tests. |
| 4. Camera system | Smoothed horizontal follow with world clamping, checkpoint recovery, parallax consumers, boss transition easing, arena lock, and defeat-gated release. | REUSE WITH ADAPTATION | Preserve camera states and boss-arena rules as a contract. Rewrite as an isolated camera controller with deterministic tests and no dependency on the render component. |
| 5. Audio system | HTML Audio-based looping music, exploration/boss maps, mute/pause ownership, async replacement, crossfade, cancellation, and cleanup. Two M4A runtime loops cover current levels. | REUSE WITH ADAPTATION | Preserve ownership, cancellation, mute/pause, transition, and loop-test ideas. Rebuild with engine-native audio, approved formats, per-level manifests, and SFX buses. Investigate master provenance before reuse. |
| 6. Save and settings system | `localStorage` stores only high score and best time. Mute is component state; no versioned save schema or durable settings service was found. | REWRITE FOR V2 | Add a versioned save/settings boundary with migration, validation, defaults, storage-failure handling, and test coverage after engine selection. |
| 7. Deployment configuration | GitHub Actions builds and deploys `dist-pages` to GitHub Pages from `main`; OpenAI Sites metadata and Cloudflare/Vinext development bindings also exist. | REUSE WITH ADAPTATION | Retain build-before-deploy and artifact verification. Choose one V2 deployment path after engine/export decisions; do not carry duplicate hosting configuration by default. |
| 8. Test infrastructure | Node `--test` suite with many pure-module unit/contract tests, rendered HTML assertions, build checks, skill validation, and level/visual integrity checks. | REUSE WITH ADAPTATION | Preserve pure deterministic contracts and layered test categories. Rewrite tests against V2 modules; avoid source-text regex tests where behavior can be exercised. |
| 9. Screenshot and visual-audit tooling | Query-string fixture routes, debug overlays, a visual inventory, extensive stored screenshots/reports, and manual browser passes at desktop/mobile sizes. Some reports explicitly note fixture and input limitations. | REUSE WITH ADAPTATION | Preserve route/state reproducibility, overlays, target-resolution ledgers, and evidence reports. Require uninterrupted real gameplay through `v2_release_gate`; fixture screenshots alone cannot pass. |
| 10. `AGENTS.md` | Routes work through the project-local skill registry and mandates visual QA. | REUSE WITH ADAPTATION | V2 root guidance retains routing but adds clean-room boundaries, canonical design paths, architecture contracts, and the mandatory release gate. |
| 11. `.skills` structure | Seven canonical skills with one-level references and agent metadata: sprite art, rendering integrity, animation, placement, overlap, visual QA, conductor. | REUSE WITH ADAPTATION | Copy and update paths/contracts. Add `v2_release_gate`; do not duplicate canonical design documents in skills. |
| 12. Runtime asset pipeline | Python and Node scripts derive atlases/backgrounds/props from `concepts/`; runtime PNGs live in `public/assets/generated`; source, generated, contact-sheet, and runtime concerns are partially mixed. | REWRITE FOR V2 | Keep only pipeline principles: deterministic extraction, alpha checks, contact sheets, manifests, and tests. New tools live in `tools/asset-pipeline`; outputs separate `assets/generated` from `assets/runtime`. |
| 13. Level representation | Browser-independent declarative modules define zones, surfaces, flight bands, backgrounds, encounters, rewards, checkpoints, routes, boss data, and exits; validation exists but schemas are implicit JS objects. | REUSE WITH ADAPTATION | Preserve the data-driven shape and named supports. Re-express it through `LEVEL_CONTRACT.md` with schema validation; do not copy V1 level files or spawn tables. |
| 14. Enemy and boss architecture | Ordinary enemies share runtime records and kind-specific behavior modules. Bosses use separate animation/behavior helpers, explicit arena activation, camera lock, platform/weak-point validation, defeat, and release state. | REUSE WITH ADAPTATION | Preserve separation of definition, behavior, animation, and arena lifecycle as design patterns. Rewrite every implementation and author new V2 encounter data from approved references. |
| 15. Collision and rendering layers | Axis-aligned independent collision records coexist with visible bounds, placement footprints, anchors, supports, flight bands, and nine semantic render layers. Some legacy paths still couple dimensions inside the monolithic runtime. | REUSE WITH ADAPTATION | Adopt independent geometry and semantic layers through V2 contracts. Never derive collision from transparent sprite bounds or use z-order to hide intersections. |

## Cross-cutting classifications

### REUSE AS-IS

- Approved design package files imported from multipart parts 00–07, with internal structure and checksums preserved.
- Approval policy and manifest semantics under `docs/design/trash-dash/manifests/`.

### REUSE WITH ADAPTATION

- Behavioral contracts for input clearing, camera arena lifecycle, audio ownership, data-driven levels, semantic layers, deterministic validation, skill routing, and visual evidence.

### REWRITE FOR V2

- Runtime engine, render loop, gameplay component, persistence, asset-build tooling, runtime schemas, actors, collisions, and all gameplay implementations.

### RETIRE

- The monolithic `trash-dash-game.tsx` architecture.
- V1 level modules, spawn tables, runtime atlases, runtime art, query fixtures as acceptance substitutes, duplicated hosting stacks, and source-sheet-as-atlas practices.

### NEEDS INVESTIGATION

- Final V2 engine/runtime choice and export targets.
- Existing music master provenance and reuse rights.
- Exact V1 GitHub visibility after valid `gh` authentication is restored.
- Whether any small pure utility merits a later module-level audit; none is currently approved for copying.

## Audit evidence

Reviewed V1 `package.json`, Vite/Next/Pages configuration, deployment workflow, root agent guidance, `.skills`, core gameplay/runtime modules, level definitions, camera/boss helpers, music controller, visual contract/inventory, test inventory, asset scripts, and visual-audit reports. V1 remained untouched.
