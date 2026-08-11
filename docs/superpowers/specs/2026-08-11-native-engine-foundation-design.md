# Trash Dash 2.0 Native Engine Foundation Design

## Purpose

Define the engine, platform, runtime, content, persistence, validation, and release foundations for Trash Dash 2.0 before any gameplay or Level 1 implementation begins.

## Scope

This design covers the Godot foundation and its disposable acceptance spike. It does not authorize production gameplay, canonical level construction, final store submission, cloud saves, or controller certification.

## Platform matrix

| Platform | Distribution | Required launch input | Launch status |
|---|---|---|---|
| Windows | Steam | Remappable keyboard | Required |
| macOS | Steam | Remappable keyboard | Required |
| iOS | Apple App Store | Landscape touch | Required |
| Android | Google Play | Landscape touch | Required |
| Desktop controllers | Steam platforms | Controller | Recommended, not release-blocking |
| Mobile controllers | iOS/Android | Controller | Optional |
| Linux | None | None | Out of scope |
| Web | None | None | Out of scope |

## Engine choice

Use the current stable Godot 4 release with typed GDScript. Godot owns the game loop, scenes, input, audio, rendering, collision integration, resource loading, and native exports. The initial spike uses the Compatibility renderer and must validate it on representative mobile devices before production adoption.

This choice replaces the former browser-first recommendation. It avoids V1's React-owned Canvas runtime and supports one native codebase across all four required launch platforms.

## Display contract

Gameplay has a fixed 960×540 logical viewport and fixed 16:9 field of view. Physical displays scale that viewport without exposing extra world space. Letterboxing absorbs aspect-ratio differences. UI respects platform safe areas and remains inside a tested action-safe region.

Pixel art uses nearest-neighbor sampling, stable anchors, and uniform scale. The runtime must not stretch fixed-aspect assets or derive collision from transparent image bounds. The spike must verify crisp rendering at representative desktop, phone, and tablet resolutions.

Mobile gameplay is landscape-only. Orientation changes outside landscape pause presentation and display a controlled rotate-device prompt without advancing gameplay.

## Project boundaries

The intended Godot structure is:

```text
project.godot
autoload/
scenes/
  boot/
  menus/
  gameplay/
  actors/
  levels/
  ui/
scripts/
  core/
  rendering/
  world/
  actors/
  gameplay/
  ui/
data/
  assets/
  animations/
  encounters/
  levels/
assets/
  generated/
  runtime/
tests/
  unit/
  gameplay/
  visual/
tools/
  asset-pipeline/
  level-validation/
  visual-audit/
```

Autoloads are restricted to application state, save/settings, audio routing, and scene transitions. Level scenes and actors receive dependencies through explicit properties, typed resources, groups, and signals rather than reaching into unrelated global state.

## Content model

The hybrid authoring model separates gameplay truth from visual composition:

- typed Godot Resources define assets, animations, level sections, supports, collision, encounters, checkpoints, routes, boss lifecycle, and transitions;
- Godot scenes arrange approved visual elements and provide editor previews;
- stable IDs connect resources to scene nodes;
- validation rejects missing IDs, unknown supports, archive paths, unapproved assets, invalid layers, incomplete animation states, and illegal encounter composition before gameplay begins.

Approved references under `docs/design/trash-dash/reference/` are immutable inputs, not runtime atlases. Deterministic pipeline outputs begin in `assets/generated/`. Promotion to `assets/runtime/` requires provenance, contract validation, automated checks, and the V2 release gate.

## Runtime flow

The boot scene loads settings, validates the local save, configures input and audio, then enters the main menu. Starting a level loads its typed resource and composed scene, resolves stable IDs, validates the complete level contract, and only then instantiates actors and encounters.

The camera is an explicit state machine with normal follow, transition, boss approach, arena lock, defeat release, and checkpoint recovery states. Gameplay systems consume platform-neutral actions rather than physical keys or touch controls.

Invalid development content fails early with actionable validation errors. A release build shows a controlled error screen, records diagnostic context, and returns safely instead of entering a partially constructed level.

## Input

Desktop requires remappable keyboard actions. Mobile provides safe-area-aware landscape touch controls. Both map into the same actions and produce equivalent press, hold, release, interruption, and lifecycle clearing behavior.

Controller mappings may be implemented during foundation work when they do not delay required targets. Missing or incomplete controller support cannot block the first release, but controller code must use the same action layer.

## Persistence

Launch persistence is local-only. Save data includes an explicit schema version, validated fields, safe defaults, and migrations between supported versions. Writes are atomic. If validation fails, preserve the corrupt file for diagnosis and recover with defaults rather than crashing or silently overwriting the only evidence.

Future Steam Cloud, iCloud, and Google Play synchronization will implement a storage adapter outside the save schema. Cloud services must not become prerequisites for local play.

## Testing and release evidence

Testing is layered:

- unit tests cover resource validators, save migrations, camera states, animation states, collision rules, and deterministic encounter decisions;
- gameplay tests cover action parity, movement primitives, checkpoints, boss lifecycle, and win/lose transitions in synthetic harnesses;
- visual-contract tests measure aspect ratio, atlas frames, anchors, collision independence, grounding, semantic layers, letterboxing, and safe areas;
- export smoke tests launch unsigned development builds on Windows, macOS, iOS devices, and Android devices;
- final content acceptance requires uninterrupted gameplay on representative hardware at target resolutions.

Fixture scenes and static screenshots are diagnostic evidence, not release-gate proof. Signing keys, certificates, provisioning profiles, keystores, and store credentials remain outside Git.

## Disposable spike

The first implementation plan produces a disposable engine spike, not production gameplay. It must prove every acceptance item in `docs/architecture/ENGINE_DECISION.md`, record results, and then be removed. Accepted contracts, build scripts, tests, or configuration may be retained only after explicit review; spike gameplay and content may not enter production source.

## Success criteria

The foundation design is successful when the spike demonstrates one coherent Godot/GDScript workflow across all required platforms, the fixed display/input/content contracts behave consistently, platform export prerequisites are documented, automated checks are repeatable, and no V1 gameplay code or legacy runtime asset enters V2.

## Official export references

- [Godot export overview](https://docs.godotengine.org/en/stable/tutorials/export/exporting_projects.html)
- [Godot iOS export requirements](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_ios.html)
- [Godot Android export requirements](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html)
- [Godot macOS export and notarization](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_macos.html)
