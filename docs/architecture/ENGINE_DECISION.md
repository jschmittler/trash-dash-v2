# Engine decision

Status: **accepted**

Decision owner: project owner

Accepted: 2026-08-11

## Decision

Trash Dash 2.0 will use the current stable Godot 4 release with typed GDScript.

Launch targets are:

- Windows through Steam;
- macOS through Steam;
- iOS through the Apple App Store;
- Android through Google Play.

Linux and web exports are not launch targets.

## Presentation and input

- Gameplay uses a fixed 960×540 logical viewport and fixed 16:9 field of view.
- Wider or taller physical displays use letterboxing and safe-area-aware UI rather than revealing additional gameplay space.
- Mobile gameplay is landscape-only and touch-first.
- Desktop keyboard controls are required and remappable.
- Controller support is recommended but is not a launch blocker.
- All devices feed one platform-neutral gameplay action layer.

## Runtime architecture

Godot owns the game loop, rendering, input, audio, scene lifecycle, and platform exports. Typed GDScript modules remain focused by responsibility. Application-wide autoloads are limited to save/settings, audio routing, scene transitions, and truly global state.

Levels use a hybrid authoring model:

- typed, validated Godot Resources define sections, supports, collision, encounters, checkpoints, routes, boss lifecycle, and asset references;
- Godot scenes provide visual composition and editor previews;
- stable IDs connect resource data to scene nodes;
- validation prevents invalid or incomplete levels from entering gameplay.

Approved design files remain immutable source references. Deterministic tools derive candidates under `assets/generated/`; only release-gated outputs enter `assets/runtime/`.

## Renderer and physics

The initial engine spike will use Godot's Compatibility renderer because the project is a pixel-art 2D game and broad mobile compatibility is more valuable than advanced 3D rendering features. The spike must verify the choice on representative iOS and Android hardware before it becomes a production constraint.

Gameplay uses purpose-built 2D platformer behavior with Godot collision primitives. Collision, hurtboxes, attacks, weak points, supports, and effect origins remain independent from transparent sprite bounds.

## Persistence and services

Launch saves are local, versioned, validated, and written atomically. Corrupt saves are retained for diagnosis before safe defaults are restored. Steam Cloud, iCloud, and Google Play synchronization are deferred behind a future storage adapter.

## Distribution constraints

- Windows and macOS packages target Steam.
- macOS distribution requires signing and notarization.
- iOS exporting and App Store submission require macOS, Xcode, signing identities, and provisioning.
- Android publishing uses signed Android App Bundles.
- Signing keys, certificates, provisioning profiles, and store credentials never enter the repository.

## Rejected approaches

- **Browser-first Phaser/custom Canvas:** rejected because Windows, macOS, iOS, and Android native builds are required while Linux and web are not.
- **Unity:** viable but rejected because its C# workflow and project/runtime weight are unnecessary for this 2D scope.
- **Separate native applications:** rejected because duplicated rendering, input, save, testing, and release systems would multiply cost and drift.

## Mandatory pre-production spike

Before creating production gameplay, build a disposable Godot spike outside production source that proves:

1. fixed-step gameplay behavior;
2. typed GDScript project structure;
3. fixed 960×540 rendering with crisp integer-friendly scaling, letterboxing, and safe-area UI;
4. keyboard and landscape touch action parity;
5. camera follow, transition, boss lock, and release states;
6. independent collision and debug overlays;
7. one derived sprite animation with stable anchors and aspect ratio;
8. one typed level resource connected to one composed scene;
9. local versioned save/load and corruption recovery;
10. audio pause, mute, loop, transition, and lifecycle behavior;
11. automated unit and gameplay checks;
12. screenshot capture at representative desktop and mobile resolutions;
13. unsigned development exports for Windows, macOS, iOS device, and Android device.

Record the results, remove the spike, and retain only accepted contracts and infrastructure decisions. Spike gameplay may not be promoted into production source.
