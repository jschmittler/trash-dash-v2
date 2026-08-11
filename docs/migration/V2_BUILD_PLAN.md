# Trash Dash 2.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven development or an equivalent task-by-task execution workflow. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a clean-room, data-driven Trash Dash 2.0 whose runtime and assets pass deterministic, visual, and uninterrupted-gameplay release gates.

**Architecture:** Approved design files remain immutable inputs. A selected 2D runtime consumes validated level, encounter, animation, asset, and rendering contracts through adapters isolated from game logic. Generated assets are promoted to runtime only after provenance, automated, and visual gates.

**Tech Stack:** Runtime framework pending `docs/architecture/ENGINE_DECISION.md`; Git; GitHub Actions after remote creation; engine-appropriate TypeScript or native scripting; repository tools for asset, level, and visual validation.

## Global constraints

- The sibling V1 repository is read-only and must remain unchanged.
- Do not copy V1 gameplay code, level files, spawn tables, runtime atlases, runtime art, or implementation debt.
- `docs/design/trash-dash/reference/` is the approved design source of truth; archives are forbidden.
- Do not begin level production until shared runtime contracts and one disposable engine spike are accepted.
- An item is complete only after `.skills/v2_release_gate/SKILL.md` returns `PASS`.

---

### Task 1: Accept the engine and target matrix

**Files:** Modify `docs/architecture/ENGINE_DECISION.md`; create the engine-native package/project configuration only after acceptance.

- [ ] Answer all nine decision questions and record browser/device, resolution, orientation, accessibility, physics, editor, and deployment targets.
- [ ] Build a disposable spike proving the candidate acceptance test without copying V1 production code.
- [ ] Record measured bundle/startup, pixel scaling, input, camera, audio, test, and screenshot results.
- [ ] Select the engine, document rejected alternatives, delete the spike, and verify no spike gameplay entered `src/`.

### Task 2: Scaffold the runtime boundaries

**Files:** Create focused modules under `src/core`, `src/rendering`, `src/world`, `src/actors`, `src/gameplay`, `src/ui`, and engine configuration at repository root.

- [ ] Define fixed-step clock, scene lifecycle, dependency boundaries, error handling, and development diagnostics.
- [ ] Add engine boot and smoke tests that load an empty scene at each target viewport.
- [ ] Add CI commands for install, format/lint, unit, gameplay, visual-contract, and production build checks.
- [ ] Run all commands from a clean checkout and record exact versions in the lockfile.

### Task 3: Implement schema-first content contracts

**Files:** Create schema/validator modules under `src/core` and tests under `tests/unit` for the five architecture contracts.

- [ ] Encode stable, versioned schemas for assets, animations, levels, encounters, rendering layers, collision, and save/settings data.
- [ ] Add fixtures that fail for unapproved paths, archive paths, missing supports, nonuniform scale, unknown layers/states, boss contamination, and schema mismatches.
- [ ] Implement the minimum validators required to pass each failing fixture.
- [ ] Add human-readable error reports used by `tools/level-validation` and the release gate.

### Task 4: Build the asset promotion pipeline

**Files:** Create deterministic tools under `tools/asset-pipeline`, generated manifests under `assets/generated`, runtime manifests under `assets/runtime`, and tests under `tests/unit`.

- [ ] Inventory approved references through the canonical manifests without treating sheets as atlases.
- [ ] Implement explicit crop/cell extraction, alpha inspection, visible-bounds measurement, anchor metadata, nearest-neighbor processing, and contact-sheet output.
- [ ] Fail builds on archive provenance, missing approvals, dirty atlas edges, frame bleed, distorted aspect ratio, nondeterministic output, or missing rebuild metadata.
- [ ] Promote only reviewed hashes into `assets/runtime` and prove a clean rebuild reproduces them byte-for-byte where formats permit.

### Task 5: Build runtime primitives before levels

**Files:** Implement isolated modules for input, camera, audio, persistence, rendering, collision, and debug overlays in their designated `src` areas; add unit/gameplay tests.

- [ ] Implement remappable action input with keyboard/touch lifecycle clearing and target-device checks.
- [ ] Implement camera follow, clamp, transition, arena lock, checkpoint restore, and defeat-gated release as explicit states.
- [ ] Implement audio buses, mute/pause ownership, loop points, transitions, cancellation, and cleanup.
- [ ] Implement versioned save/settings with validation, defaults, migration, and storage-failure behavior.
- [ ] Implement semantic render layers, independent collision geometry, anchors, supports, and development bounds overlays.
- [ ] Verify primitives in a synthetic non-production harness; do not call it a level.

### Task 6: Prove one vertical-slice content pipeline

**Files:** Create one non-production validation scene under tests/tools, not a canonical level.

- [ ] Derive one approved character state set and one environment element through the asset pipeline.
- [ ] Exercise input, camera, animation, collision, platform support, layering, audio, and target-resolution capture.
- [ ] Run an uninterrupted harness traversal and the full V2 release gate.
- [ ] Remove the harness after documenting reusable infrastructure findings; retain tests and contracts only.

### Task 7: Author canonical levels in order

**Files:** Create validated level data under `src/levels` and focused actors/gameplay modules only as demanded by the current level.

- [ ] Build Level 1 from approved sources after Tasks 1–6 pass; no V1 level or spawn data may be copied.
- [ ] Gate Level 1 with complete traversal, required states, target resolutions, surrounding regressions, and release evidence.
- [ ] Repeat one level at a time for Levels 2–6; do not stack the next level on a failing gate.
- [ ] Keep bosses exclusive to validated arenas and keep each level's encounter density section-specific.

### Task 8: Harden, deploy, and release

**Files:** Create deployment workflow, release documentation, and final audit evidence only after target selection and valid GitHub remote configuration.

- [ ] Run clean-checkout builds, full campaign traversal, save migration, device/input, audio, performance, accessibility, and regression passes.
- [ ] Produce immutable visual-audit ledgers for every target resolution and orientation.
- [ ] Confirm Git LFS/runtime asset policy, repository size, licenses, provenance, and disaster-recovery procedure.
- [ ] Build and verify the chosen hosting artifact before enabling deployment from protected `main`.
- [ ] Release only when every applicable `v2_release_gate` item is `PASS`.
