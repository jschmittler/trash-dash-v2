# Engine decision

Status: **accepted for the macOS MVP foundation**

Decision owner: project owner

Accepted: 2026-08-11

Revised and user-approved: 2026-08-12

## Decision

Trash Dash 2.0 will use Godot 4.7.1 Standard with typed GDScript. The current
MVP target is macOS desktop only until the project has a meaningful working
prototype. Windows, Android, and iOS remain intended roadmap targets, but their
proof and release work are deferred and do not block the macOS MVP.

Linux and web are not targets.

This approval is deliberately narrow. It accepts the engine foundation for
macOS runtime scaffolding, production infrastructure, and prototype gameplay.
It does not approve a canonical level, production asset, complete platform
matrix, store package, or release.

## Presentation and input

- Gameplay uses a fixed 960×540 logical viewport and fixed 16:9 field of view.
- Wider or taller physical displays use centered letterboxing rather than
  revealing additional gameplay space.
- macOS requires remappable physical-keyboard controls through one
  platform-neutral gameplay action layer.
- Mobile remains landscape-only and touch-first when Android and iOS re-enter
  scope; touch controls and the rotate-device gate must remain hidden on
  desktop.
- Controller support is recommended but is not an MVP blocker.

## Runtime architecture

Godot owns the game loop, rendering, input, audio, scene lifecycle, and native
exports. Typed GDScript modules remain focused by responsibility.
Application-wide autoloads are limited to save/settings, audio routing, scene
transitions, and truly global state.

Levels use a hybrid authoring model:

- typed, validated Godot Resources define sections, supports, collision,
  encounters, checkpoints, routes, boss lifecycle, and asset references;
- Godot scenes provide visual composition and editor previews;
- stable IDs connect resource data to scene nodes;
- validation prevents invalid or incomplete levels from entering gameplay.

Approved design files remain immutable source references. Deterministic tools
derive candidates under `assets/generated/`; only release-gated outputs enter
`assets/runtime/`.

## Renderer and physics

Godot's Compatibility renderer is accepted for the macOS MVP foundation only.
The reviewed macOS package used OpenGL 4.1 through Metal on Apple M2 and
preserved the fixed FOV, letterboxing, and desktop UI policy at all assessed
window sizes.

Cross-platform renderer acceptance remains pending. A historical run in a
Parallels Windows 11 VM reached Compatibility OpenGL 3.3 but repeatedly failed
GLES3 vertex-shader compilation. That result is `FAIL`, is nonblocking for the
macOS MVP, and must be resolved on an appropriate Windows GPU/driver
environment before Windows re-enters scope. Android and physical-device iOS
renderer results are `CANNOT VERIFY` and deferred.

Gameplay uses purpose-built 2D platformer behavior with Godot collision
primitives. Collision, hurtboxes, attacks, weak points, supports, and effect
origins remain independent from transparent sprite bounds.

## Persistence and services

MVP saves are local, versioned, validated, and written atomically. Corrupt
saves are retained for diagnosis before safe defaults are restored. Steam
Cloud, iCloud, and Google Play synchronization are deferred behind a future
storage adapter.

## Assets

The source-sheet-derived Trashy idle used during the disposable spike is test
evidence only. It must not enter main, `assets/runtime/`, or production. The
project owner is preparing clean sprites/assets for the next phase; those
assets must be imported, validated, and promoted through the normal pipeline.
Do not derive further production assets from concept sheets unless the owner
explicitly requests it or it becomes necessary and is reviewed first.

## Distribution constraints

- The macOS MVP package is a universal arm64+x86_64 desktop build.
- macOS store distribution eventually requires signing and notarization.
- The project owner has an Apple Developer account but has deferred Team ID,
  certificate, and provisioning-profile hookup. None may enter Git.
- Future Windows packaging targets Steam.
- Future iOS export/submission requires local Xcode signing and physical-device
  proof; future Android publishing requires a signed Android App Bundle and
  device proof.
- Signing keys, certificates, provisioning profiles, Team IDs, keystores,
  passwords, and store credentials never enter the repository.

## Rejected approaches

- **Browser-first Phaser/custom Canvas:** rejected because the longer-term
  roadmap still calls for native desktop and mobile builds.
- **Unity:** viable but rejected because its C# workflow and project/runtime
  weight are unnecessary for this 2D scope.
- **Separate native applications:** rejected because duplicated rendering,
  input, save, testing, and release systems would multiply cost and drift.

## Disposable spike outcome

The mandatory disposable spike was completed outside `main` and reviewed. Its
macOS MVP foundation is acceptable, but the SPIKE/V2 release gate is
`INCOMPLETE`, not `PASS`, because:

1. no uninterrupted human traversal of the packaged build or physical-keyboard
   feel assessment was performed;
2. the otherwise green full suite retains an isolated real-audio-test exit
   warning for leaked `AudioStreamWAV`/`AudioStreamPlaybackWAV` instances and
   orphan `Master`;
3. clean production sprites/assets have not yet been imported or validated.

The spike proved enough to begin macOS MVP infrastructure and prototype work.
Each production feature still requires its applicable contracts and V2
release gate. No level, asset, audio integration, platform, or release is
complete merely because the foundation was accepted.

No spike implementation or generated spike asset may enter `main`. After this
reviewed record is safely committed and pushed, the temporary spike
branch/worktree is removed; reproducible build and export evidence remains
ephemeral rather than a retained release artifact.
