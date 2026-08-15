# Trash Dash 2.0 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven development or an equivalent task-by-task execution workflow. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a clean-room, data-driven Trash Dash 2.0 whose runtime and
assets pass deterministic, visual, and uninterrupted-gameplay release gates.

**Current delivery scope:** macOS desktop MVP through a meaningful working
prototype. Windows, Android, and iOS are deferred, nonblocking roadmap targets.
Linux and web are out of scope.

**Architecture:** Approved design files remain immutable inputs. Godot 4.7.1
Standard with typed GDScript consumes validated level, encounter, animation,
asset, and rendering contracts through adapters isolated from game logic.
Generated assets are promoted to runtime only after provenance, automated, and
visual gates.

**Tech Stack:** Godot 4.7.1 Standard; typed GDScript; Compatibility renderer
for the macOS MVP foundation; Git and Git LFS; GitHub Actions where signing
permits; repository tools for asset, level, and visual validation.

## Global constraints

- The sibling V1 repository is read-only and must remain unchanged.
- Do not copy V1 gameplay code, level files, spawn tables, runtime atlases,
  runtime art, or implementation debt.
- `docs/design/trash-dash/library/` is the approved design source of truth;
  archives are forbidden.
- The disposable source-sheet-derived Trashy idle is spike evidence only and
  must not enter main or production runtime.
- Use the project owner's incoming clean sprites/assets for production. Do not
  derive further production assets from concept sheets without an explicit,
  reviewed request or demonstrated necessity.
- The accepted foundation authorizes macOS infrastructure and prototype work,
  not canonical-level, asset, audio, multi-platform, or release completion.
- An item is complete only after `.skills/v2_release_gate/SKILL.md` returns
  `PASS` for that item.

---

### Task 1: Validate the engine and current target matrix

**Files:** `docs/architecture/ENGINE_DECISION.md` and the reviewed foundation
report; disposable implementation remains outside `main`.

- [x] Select Godot 4 with typed GDScript, fixed 960×540 presentation,
  platform-neutral actions, hybrid authoring, and local saves.
- [x] Build and review a disposable native-foundation spike without copying V1
  production code or promoting spike content.
- [x] Record measured display, input, camera, collision, animation, save,
  audio, test, export, and packaged macOS evidence.
- [x] Select Godot 4.7.1 Standard plus Compatibility renderer for the macOS MVP
  foundation and record the revised macOS-only scope.
- [x] Record that the overall SPIKE/V2 gate is `INCOMPLETE`; do not treat the
  original Windows/Android/iOS proof matrix as accepted.
- [x] Remove the validated disposable branch/worktree after the reviewed main
  documentation was committed and pushed.

### Task 2: Scaffold the macOS MVP runtime boundaries

**Files:** Create focused modules under `src/core`, `src/rendering`,
`src/world`, `src/actors`, `src/gameplay`, and `src/ui`, plus engine
configuration at repository root.

- [x] Establish the production Godot project from accepted contracts, without
  copying spike gameplay, generated fixtures, or evidence code.
- [x] Define the fixed-step clock, scene lifecycle, dependency boundaries,
  structured error handling, and development diagnostics. Dependency
  boundaries (`ServiceRegistry` + unavailable-service fallbacks), structured
  startup error handling (`StartupValidator`/`FoundationStatus`), and
  development diagnostics (`bootstrap_view`) were already implemented.
  `FixedStepClock` (`src/core/time/fixed_step_clock.gd`) defines a
  deterministic accumulator clock, pinned to an explicit
  `physics/common/physics_ticks_per_second=60` and validated by
  `StartupValidator`. `LiveSceneTransitionService`
  (`src/core/services/live_scene_transition_service.gd`) implements a real,
  container-scoped scene swap (`change_scene`/`current_scene`) validated
  against `ResourceLoader`; the `Unavailable*` DI fallback pattern is
  preserved unchanged. `save_settings_service.gd` remains an unimplemented
  stub, deferred to Task 5's persistence work.
- [x] Implement the fixed 960×540/16:9 macOS viewport and desktop-only UI
  policy with remappable physical-keyboard actions. The fixed viewport,
  letterboxing (`DisplayPolicy`), and desktop-only UI gating
  (`is_mobile_ui_enabled`) were already implemented. `InputRemapService`
  (`src/core/input/input_remap_service.gd`) now adds real single-key rebind
  capability with conflict rejection and reset-to-defaults, applied through
  the new `InputMapAdapter` seam; persistence of a chosen remap to disk is
  deferred to Task 5.
- [x] Add macOS boot/smoke tests and CI commands for import, format/lint, unit,
  gameplay, visual-contract, and unsigned development builds. Import,
  unsigned-build, and package-smoke stages already existed. `verify_local.sh`
  now runs a `gdformat --check`/`gdlint` stage (config in `.gdlintrc`) over
  every `src/`/`tests/` script, and `tests/visual/test_visual_contract.gd`
  adds an explicit visual-contract suite (content-rect and diagnostic
  typography invariants across every required target window size) alongside
  the existing unit/gameplay suites in the `Tests` stage.
- [x] Run all commands from a clean checkout and record exact tool versions.
  Documented in `docs/development/MACOS_FOUNDATION.md`; scripts enforce the
  exact accepted Godot build. `gdtoolkit==4.5.0` is now pinned and documented
  there too.

### Task 3: Implement schema-first content contracts

**Files:** Create schema/validator modules under `src/core` and tests under
`tests/unit` for the architecture contracts.

- [ ] Encode stable, versioned schemas for assets, animations, levels,
  encounters, rendering layers, collision, and save/settings data.
  `RenderingLayer` (`src/core/schema/rendering_layer.gd`), `RenderObjectRef`
  (`src/core/schema/render_object_ref.gd`), `CollisionGeometry`
  (`src/core/schema/collision_geometry.gd`), `AssetRef`
  (`src/core/schema/asset_ref.gd`), `AnimationManifest`
  (`src/core/schema/animation_manifest.gd`), `AnimationStateRef`
  (`src/core/schema/animation_state_ref.gd`), and `Encounter`
  (`src/core/schema/encounter.gd`) are implemented, each with an explicit
  `schema_version`. Level and save/settings schemas remain unimplemented.
- [ ] Add fixtures that fail for unapproved paths, archive paths, missing
  supports, nonuniform scale, unknown layers/states, boss contamination, and
  schema mismatches. Covered so far: unknown layers/states
  (`tests/unit/test_render_object_ref_validator.gd`,
  `tests/unit/test_animation_state_ref_validator.gd`), unapproved/archive
  paths (`tests/unit/test_asset_ref_validator.gd`), nonuniform scale
  (`tests/unit/test_animation_manifest_validator.gd`), missing/unknown
  supports and duplicate IDs (`tests/unit/test_encounter_validator.gd`), and
  schema mismatches across every schema implemented so far.
  Boss-contamination fixtures are deferred to the level slice, since only
  the level record owns boss arena lock bounds.
- [ ] Implement the minimum validators required to pass each failing fixture.
  `RenderObjectRefValidator`, `CollisionGeometryValidator`,
  `AssetRefValidator`, `AnimationManifestValidator`,
  `AnimationStateRefValidator`, and `EncounterValidator` are implemented.
  Level and save/settings validators remain unimplemented.
- [ ] Add human-readable error reports used by `tools/level-validation` and
  the release gate. Validators return `PackedStringArray` messages in the
  established `StartupValidator` style, but `tools/level-validation` wiring
  and release-gate aggregation do not exist yet.

### Task 4: Build the clean-asset promotion pipeline

**Files:** Create deterministic tools under `tools/asset-pipeline`, generated
manifests under `assets/generated`, runtime manifests under `assets/runtime`,
and tests under `tests/unit`.

- [x] Reorganize the design-source library by asset type, preserve complete
  handoff packages, publish deterministic catalog/migration manifests, and
  validate active references. This is source-library infrastructure only; it
  does not promote or approve any runtime asset.

- [ ] Receive and inventory the project owner's clean sprites/assets.
- [ ] Implement explicit crop/cell handling, alpha inspection,
  visible-bounds measurement, anchor metadata, nearest-neighbor processing,
  and contact-sheet output without reusing the disposable spike derivative.
- [ ] Fail builds on archive provenance, missing approvals, dirty atlas edges,
  frame bleed, distorted aspect ratio, nondeterministic output, or missing
  rebuild metadata.
- [ ] Promote only reviewed hashes into `assets/runtime` and validate their
  production use at the feature-level release gate.

### Task 5: Build and verify runtime primitives

**Files:** Implement isolated modules for input, camera, audio, persistence,
rendering, collision, and debug overlays in their designated `src` areas; add
unit/gameplay tests.

- [ ] Implement remappable macOS keyboard actions and lifecycle clearing.
- [ ] Implement camera follow, clamp, transition, arena lock, checkpoint
  restore, and defeat-gated release as explicit states.
- [ ] Implement audio buses, mute/pause ownership, loop points, transitions,
  cancellation, cleanup, and the play-after-parent ordering contract.
- [ ] Remove the isolated real-audio-test exit leak warning before claiming a
  clean automated gate.
- [ ] Implement versioned save/settings validation, defaults, migration,
  atomic writes, byte-exact corrupt-save retention, and storage failures.
- [ ] Implement semantic render layers, independent collision geometry,
  anchors, supports, and development bounds overlays.
- [ ] Verify primitives in a synthetic non-production harness; do not call it
  a level.

### Task 6: Prove one macOS vertical-slice content pipeline

**Files:** Create one non-production validation scene under tests/tools, not a
canonical level.

- [ ] Import one clean, owner-supplied character state set and one clean
  environment element through the production asset pipeline.
- [ ] Exercise input, camera, animation, collision, platform support,
  layering, audio, and target-resolution capture.
- [ ] Build a hash-identified universal arm64+x86_64 macOS package and have a
  human perform uninterrupted physical-keyboard traversal, including
  checkpoint/arena, pause/mute/resume, and save/relaunch behavior.
- [ ] Capture and inspect the final package at 1280×720, 1440×900,
  1280×800, and the agreed narrow-window policy.
- [ ] Run the full applicable V2 release gate. Remove the harness after
  documenting reusable infrastructure findings.

### Task 7: Author canonical levels in order

**Files:** Create validated level data under `src/levels` and focused
actors/gameplay modules only as demanded by the current level.

- [ ] Begin Level 1 only after Tasks 2–6 and their applicable per-feature gates
  permit it; no V1 level or spawn data may be copied.
- [ ] Gate Level 1 with complete human traversal, required states, target
  resolutions, surrounding regressions, and release evidence.
- [ ] Repeat one level at a time for Levels 2–6; do not stack the next level on
  a failing gate.
- [ ] Keep bosses exclusive to validated arenas and keep each level's
  encounter density section-specific.

### Task 8: Re-enter deferred platforms only after a meaningful prototype

- [ ] Windows: choose a supported GPU/driver environment, resolve the
  historical Compatibility GLES3 shader `FAIL`, then repeat renderer,
  physical-keyboard traversal, save, audio, and export proof.
- [ ] Android: attach an authorized device/emulator, validate Compatibility
  rendering and landscape touch lifecycle, configure the release Gradle/AAB
  pipeline, and repeat save/audio/runtime proof.
- [ ] iOS: perform user-led local Apple Team/signing setup without committing
  Team ID/certificates/profiles, then validate Compatibility rendering,
  landscape touch, safe areas, save/audio, and a physical-device run.
- [ ] Reassess the target matrix only from direct evidence. Deferred platforms
  remain nonblocking for the current macOS MVP but are not implicitly accepted.

### Task 9: Harden, deploy, and release

**Files:** Create deployment workflow, release documentation, and final audit
evidence only after target selection and valid remote configuration.

- [ ] Run clean-checkout builds, full campaign traversal, save migration,
  device/input, audio, performance, accessibility, and regression passes for
  the selected release target.
- [ ] Produce reproducible visual-audit evidence for every target resolution
  and orientation; build artifacts remain ephemeral unless an explicit
  release-retention policy says otherwise.
- [ ] Confirm Git LFS/runtime asset policy, repository size, licenses,
  provenance, and disaster-recovery procedure.
- [ ] Configure signing/notarization outside Git and verify the chosen package
  before enabling deployment from protected `main`.
- [ ] Release only when every applicable `v2_release_gate` item is `PASS`.
