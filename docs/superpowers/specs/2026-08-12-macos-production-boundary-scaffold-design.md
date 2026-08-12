# macOS Production Boundary Scaffold Design

Status: **approved design, pending implementation plan**

Approved by: project owner

Approved: 2026-08-12

## Purpose

Create the first production Godot project for Trash Dash 2.0 as a macOS-only,
contract-first shell. The scaffold establishes enforceable runtime boundaries,
repeatable local verification, and an unsigned development export without
starting gameplay, level authoring, or production asset integration.

This is production infrastructure, not a playable vertical slice. It may
support later prototype work, but it must not copy the disposable spike or V1
implementation.

## Accepted foundation

The scaffold consumes the reviewed decisions in:

- `docs/architecture/ENGINE_DECISION.md`;
- `docs/superpowers/reports/2026-08-11-godot-native-foundation-spike.md`;
- `docs/migration/V2_BUILD_PLAN.md`.

The accepted foundation is:

- Godot 4.7.1 Standard;
- typed GDScript;
- Compatibility renderer for the macOS MVP;
- fixed 960×540 logical gameplay viewport and fixed 16:9 field of view;
- centered letterboxing on other desktop window shapes;
- nearest-neighbor texture filtering;
- remappable physical-keyboard actions through a platform-neutral input layer;
- unsigned universal arm64+x86_64 macOS development export;
- local verification before CI;
- Windows, Android, and iOS deferred until the macOS prototype is meaningful;
- Linux and web excluded;
- no credentials, Team IDs, certificates, profiles, passwords, or signing
  material in Git.

## Scope

The scaffold includes:

1. a production `project.godot` at the repository root;
2. one diagnostic bootstrap scene and its typed presentation/controller code;
3. immutable build identity and startup-status data;
4. focused display, input-map, startup-validation, and service-registry
   boundaries;
5. narrow save/settings, audio, scene-transition, and runtime-state service
   contracts with explicit unavailable behavior;
6. a dependency-free headless GDScript test runner;
7. boot, project-contract, display, input-map, scene-boundary, and
   service-contract tests;
8. local verification scripts for import, tests, policy checks, editor smoke,
   and unsigned macOS export verification;
9. one secret-safe macOS Universal 2 development export preset;
10. concise developer documentation for running the scaffold locally.

The scaffold excludes:

- player or enemy actors;
- movement, combat, encounters, checkpoints, bosses, or other gameplay;
- canonical or synthetic levels;
- production save/audio/camera implementations;
- autoloads whose only purpose is anticipated future work;
- main menu/product navigation;
- runtime sprites, animation atlases, environment art, music, or SFX;
- further extraction from concept/reference sheets;
- the project owner's pending clean sprite/asset import;
- Windows, Android, iOS, Linux, or web export presets;
- Steam, App Store, or Google Play SDKs and store workflows;
- signing, notarization, CI, cloud saves, analytics, or networking.

## Architecture

Use a contract-first vertical shell. The bootstrap path is real and fully
tested, while unfinished systems expose small contracts rather than fake
implementations.

### Production project

The repository root is the Godot project root. `project.godot` owns only
production settings:

- application name and semantic scaffold version;
- `res://scenes/bootstrap/bootstrap.tscn` as the main scene;
- 960×540 viewport;
- `canvas_items` stretch mode with `keep` aspect;
- Compatibility rendering on desktop and mobile renderer fields where Godot
  requires a coherent import configuration, without adding mobile presets;
- nearest-neighbor filtering;
- six platform-neutral input actions: `move_left`, `move_right`, `jump`,
  `dash`, `action`, and `pause`;
- required keyboard defaults: A/Left, D/Right, Space, Shift, E, Escape.

No production autoload is added in this slice. The bootstrap scene owns the
initial registry so tests and future scenes can replace services without
global state.

### Bootstrap scene

`scenes/bootstrap/bootstrap.tscn` is the only startup scene. Its hierarchy is
small and screen-space:

```text
Bootstrap (Control)
└── SafeMargin (MarginContainer)
    └── StatusColumn (VBoxContainer)
        ├── ProjectTitle (Label)
        ├── FoundationStatus (Label)
        ├── BuildIdentity (Label)
        ├── RuntimePolicy (Label)
        └── ContentStatus (Label)
```

The scene contains no gameplay world, camera, sprite, texture, or hidden
prototype content. Containers and anchors own layout; script code supplies
data, not pixel positions.

The diagnostic shell presents neutral text:

- `Trash Dash 2.0`;
- `macOS prototype foundation`;
- the semantic version and source build identity;
- `960×540 / Compatibility`;
- `prototype content not loaded`.

The shell is not a main menu and has no interactive buttons.

### Bootstrap controller and status model

`BootstrapController` performs only startup orchestration:

1. receive or construct the service registry;
2. invoke the startup validator;
3. construct an immutable `FoundationStatus` model;
4. give that model to the diagnostic view;
5. end in `FOUNDATION_READY` or `FOUNDATION_ERROR`.

The view never reads project settings, OS state, autoloads, or service
implementations directly. The controller never formats labels or manipulates
layout beyond providing the status model.

`FoundationStatus` contains:

- state enum;
- project name;
- semantic version;
- build identity;
- logical viewport;
- renderer name;
- content status;
- ordered validation messages.

Build identity defaults to a deterministic development value and may be
overridden by an environment/export setting later. It must never contain an
absolute local path.

### Startup validation

The startup validator is a pure typed unit. It receives a settings adapter and
returns ordered validation results. It verifies:

- viewport width and height are exactly 960 and 540;
- stretch mode is `canvas_items`;
- stretch aspect is `keep`;
- renderer is `gl_compatibility`;
- default texture filtering is nearest-neighbor compatible;
- all six required actions exist;
- the service registry contains every required contract;
- prototype content is intentionally unavailable.

Validation failures are data, not crashes. The bootstrap scene renders an
error state and the headless contract test exits nonzero.

### Display policy

`DisplayPolicy` is a pure typed helper. It owns:

- logical size `Vector2i(960, 540)`;
- largest centered integer 16:9 content rectangle calculation;
- desktop/mobile presentation policy queries.

The production scaffold targets macOS only. Desktop policy never enables
touch controls or portrait pausing. Mobile policy remains an interface-level
future concern and receives no scene, preset, or runtime implementation here.

### Input-map boundary

The scaffold configures actions but does not implement actor input or
movement. `InputMapContract` validates action existence and required default
keyboard mappings without polling gameplay state.

The required defaults are:

| Action | Defaults |
|---|---|
| `move_left` | A, Left Arrow |
| `move_right` | D, Right Arrow |
| `jump` | Space |
| `dash` | Shift |
| `action` | E |
| `pause` | Escape |

Remapping UI and persistent bindings are deferred. Consumers added later must
read action names rather than raw key codes.

### Service registry and contracts

`ServiceRegistry` is a small typed object owned by the bootstrap scene. It
contains four explicit contracts:

- save/settings;
- audio;
- scene transition;
- runtime state.

The contracts describe only operations required to preserve architectural
boundaries. Each initial implementation is an `Unavailable*Service` that:

- is deterministic and side-effect free;
- returns `ERR_UNAVAILABLE` or a typed unavailable result;
- exposes a stable service identifier;
- never writes a save, creates an audio player, changes scenes, or mutates
  runtime state;
- emits no success signal for unavailable work.

These objects are not autoloads. Production implementations replace them only
when a planned feature needs the behavior and has failing tests.

## Runtime flow

```text
Godot main scene
  → BootstrapController
    → ServiceRegistry with unavailable service implementations
    → StartupValidator
      → ProjectSettings adapter
      → InputMapContract
    → FoundationStatus
      → Bootstrap diagnostic view
```

A healthy scaffold ends in `FOUNDATION_READY` even though prototype content
and operational services are unavailable. Readiness means the production
boundaries and settings are valid; it does not mean gameplay exists.

## Error handling

- Expected unimplemented operations return explicit unavailable results.
- Invalid project configuration produces ordered startup validation messages.
- Missing required scene nodes fail scene parsing or a focused scene-contract
  test; optional-node lookup is not used to hide structural errors.
- Local verification scripts stop at the first failing stage and propagate its
  exit code.
- Export output directories must be explicit, outside source, empty, and never
  deleted recursively by verification scripts.
- Tests use isolated temporary output and clean only paths they created.
- Diagnostics and reports never include secrets or absolute user paths.

No global exception-swallowing, silent fallback, or placeholder success is
permitted.

## Test architecture

Use the dependency-free GDScript runner pattern proven during the disposable
spike, reimplemented from the written contract rather than copied from the
deleted spike branch.

The runner:

- extends `SceneTree`;
- loads an explicit ordered list of test scripts;
- invokes methods prefixed `test_`;
- collects typed assertion failures;
- prints deterministic failure messages;
- exits 1 when any assertion fails and 0 otherwise;
- gives native scene/audio/resource teardown enough frames before exit;
- must produce warning-free output.

Initial suites cover:

1. project settings and renderer contract;
2. exact viewport/content-rectangle behavior at 1280×720, 1440×900,
   1280×800, and 390×844;
3. exact input actions/default key mappings;
4. build identity and foundation status model;
5. startup validator success and ordered failure behavior;
6. service registry completeness and unavailable-service semantics;
7. bootstrap scene load, required node paths, diagnostic text, and clean free;
8. macOS export preset scope and secret-safe fields;
9. static clean-room policy checks.

The test runner itself has focused tests for assertion collection and nonzero
failure exit behavior.

## Local verification

CI is intentionally deferred until local commands are stable. `tools/verify/`
provides focused scripts and one aggregate entry point. The required sequence
is:

1. verify Godot is exactly the accepted 4.7.1 stable Standard build;
2. scan repository policies and forbidden paths;
3. run headless project import;
4. run the dependency-free test suite;
5. run a headless editor boot smoke;
6. export an unsigned macOS Universal 2 development ZIP to a fresh temporary
   output directory;
7. verify ZIP integrity;
8. verify the executable contains arm64 and x86_64 slices;
9. launch the package for a bounded smoke check and confirm no process remains.

The aggregate command must fail nonzero if any stage fails. It must not upload,
sign, notarize, commit, or delete broad directories.

## Export configuration

`export_presets.cfg` contains exactly one preset named `macOS`:

- Universal 2 architecture;
- ZIP packaging;
- embedded PCK when supported by the preset;
- signing disabled through valid Godot 4.7.1 enum settings;
- notarization disabled;
- no Team ID, certificate, identity, entitlement secret, password, or local
  absolute path;
- no Windows, Android, iOS, Linux, or web preset.

The development package is ephemeral and must be produced from a recorded,
clean source revision with its size, SHA-256, ZIP integrity, and executable
architectures reported. Byte-for-byte reproducibility is not claimed because
Godot and ZIP metadata may include build-time values. The package is not a
retained release artifact or proof of store readiness.

## Static clean-room policy

Verification fails when production configuration or source includes:

- a path under the sibling V1 repository;
- an `archive/` source;
- the deleted spike project or its generated fixture;
- a concept/reference-sheet path under production runtime configuration;
- deferred-platform export presets;
- credentials or signing material;
- absolute `/Users/`, `/home/`, or Windows drive paths;
- tracked `.godot/`, `.import/`, generated UID-cache data such as
  `.godot/uid_cache.bin`, temporary, build, or export output; source `.uid`
  sidecars required by Godot are not classified as cache by this rule;
- gameplay, actor, level, runtime asset, audio track, or concept-derived asset
  introduced by this scaffold.

The owner's future clean assets remain outside this specification.

## File responsibility map

The implementation plan will assign exact filenames, but the intended
production boundaries are:

```text
project.godot                     Production Godot settings and input map
export_presets.cfg                One secret-safe macOS development preset
scenes/bootstrap/                 Diagnostic startup scene only
src/core/bootstrap/               Controller, status model, startup validation
src/core/build/                   Immutable build identity
src/core/display/                 Pure viewport/presentation policy
src/core/input/                   Input-map contract validation
src/core/services/                Registry, contracts, unavailable services
src/ui/bootstrap/                 Diagnostic view adapter
tests/support/                     Assertions, base case, dependency-free runner
tests/unit/                        Pure contract tests
tests/gameplay/                    Bootstrap scene/runtime smoke only
tools/verify/                      Local policy, test, smoke, and export scripts
docs/development/                 Local scaffold commands and boundaries
```

Empty placeholder directories outside this slice remain untouched.

## Acceptance criteria

The scaffold is accepted when all of the following are true:

1. a clean checkout imports and boots with Godot 4.7.1 Standard;
2. the diagnostic scene reaches `FOUNDATION_READY` and displays the required
   neutral status without gameplay or assets;
3. all GDScript is typed and each file has one focused responsibility;
4. fixed 960×540, 16:9 keep-aspect, Compatibility, and nearest-filter settings
   pass automated contract tests;
5. the six exact action mappings pass tests;
6. every unavailable service returns explicit unavailable behavior without
   side effects;
7. the dependency-free test runner and complete initial suite exit 0 with no
   parse, resource, leak, or warning output;
8. repository policy checks find no clean-room, archive, concept-runtime,
   credential, absolute-path, deferred-platform, cache, or build-product
   violation;
9. a fresh unsigned macOS ZIP exports successfully and is verified as a
   universal arm64+x86_64 package;
10. a bounded package boot exits cleanly with no lingering process;
11. only scaffold infrastructure files are committed;
12. V1 remains unchanged;
13. visual completion is reported `INCOMPLETE` until the final diagnostic shell
    is directly inspected at the required macOS window sizes.

Passing this scaffold permits implementation of the next planned macOS MVP
infrastructure task. It does not permit a production level, asset, audio, or
release `PASS` claim.

## Deferred work

- GitHub Actions and protected-branch CI;
- production save, audio, scene-transition, runtime-state, camera, collision,
  and rendering services;
- clean asset import and promotion;
- gameplay and vertical-slice scenes;
- main menu and product UI;
- human packaged keyboard traversal;
- signing/notarization and Apple account hookup;
- Windows, Android, and iOS platform re-entry;
- controller support, cloud saves, analytics, networking, and store SDKs.
