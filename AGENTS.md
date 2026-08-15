# Trash Dash 2.0 Project Instructions

## Clean-room boundary

Trash Dash 2.0 is a selective greenfield rebuild. The sibling V1 repository at `../trash-dash/` is read-only reference material. Never modify it and never copy its production source tree, level modules, spawn tables, runtime atlases, runtime art, or implementation code into this repository without an approved reuse-matrix change.

The canonical visual source is `docs/design/trash-dash/library/`, interpreted through `docs/design/trash-dash/manifests/library-catalog.json`. Written canon lives under `docs/design/trash-dash/manuals/`; complete handoff evidence lives under `docs/design/trash-dash/packages/` and is not a competing source of truth. Start at `docs/design/trash-dash/LIBRARY_INDEX.md`. Files under any `archive/` path are noncanonical and may not enter V2 runtime work.

## Canonical boss descriptions

Before any work involving a boss's visuals, animation, VFX, attacks, narrative, dialogue, marketing, or generative prompt, read `docs/design/trash-dash/manuals/bosses/README.md` and that boss's linked canon file in full. These descriptions are strict project canon. Do not silently reinterpret, omit, replace, or contradict a locked attribute. The approved library reference sheet remains the final authority for visible appearance; if prose and source art appear to conflict, stop and request a canon ruling rather than inventing a resolution.

## Canonical UI kit

Before modifying menu, HUD, notification, alert, pause, results, reward, or Character Select code or art, read `docs/design/trash-dash/library/interface/` and the preserved written UI contracts under `docs/design/trash-dash/packages/ui-kit/trash-dash-hd-remake-ui-kit-codex-handoff-v0.3/docs/`. Follow their authority order: written contracts/tokens/approval rules, overall concept board, matching phase concept board, matching phase source sheet, then implementation judgment. The approved visual language is **Reclaimed Playground**.

Source sheets are immutable extraction sources, not runtime atlases. Stage crops before cleanup; never stretch or squash raster UI art; construct scalable panels with 9-slice or layered pieces; keep dynamic values as runtime text; preserve full Trashy and Jimothy silhouettes; use the motion-token system with reduced-motion behavior; and validate UI changes in live gameplay. Do not import alternate source-sheet logos, characters, or off-style UI.

## Canonical Art and Level-Design Resources

Before selecting, creating, replacing, or implementing visual assets, read `docs/design/trash-dash/manifests/library-catalog.json` and the relevant level concept, blueprint, level specification, and enemy specification. Reuse registered canonical sources instead of creating competing duplicates. Concepts and blueprints are reference-only unless explicitly registered for runtime use; isolated props are authoritative appearances; composite foreground sheets are contact/reference sheets, not automatic spritesheets. Never overwrite approved canon without an explicit requested revision. Register newly approved sources, label derivatives with their source relationship, and run `python3 tools/verify/validate_design_library.py` plus `python3 tools/verify/audit_canonical_assets.py` after any asset import or visual replacement.

## Mandatory skill routing

Before substantial work, read this file, `.skills/README.md`, and every applicable skill. Declare the selected skill set before editing.

| Work | Required skills |
|---|---|
| Character creation | `sprite-art`, `rendering-asset-integrity`, `animation`, `visual-qa`, `v2_release_gate` |
| Sprite extraction and animation | `rendering-asset-integrity`, `animation`, `visual-qa`, `v2_release_gate` |
| Level creation | `environment-placement`, `overlap-prevention`, `visual-qa`, `v2_release_gate` |
| Enemy layout | `environment-placement`, `overlap-prevention`, `visual-qa`, `v2_release_gate` |
| Platform construction | `rendering-asset-integrity`, `environment-placement`, `overlap-prevention`, `visual-qa`, `v2_release_gate` |
| Prop placement | `rendering-asset-integrity`, `environment-placement`, `overlap-prevention`, `visual-qa`, `v2_release_gate` |
| Collision and grounding | `rendering-asset-integrity`, `environment-placement`, `overlap-prevention`, `visual-qa`, `v2_release_gate` |
| Scale and aspect ratio | `rendering-asset-integrity`, `visual-qa`, `v2_release_gate` |
| Z-order and layering | `environment-placement`, `rendering-asset-integrity`, `visual-qa`, `v2_release_gate` |
| Visual auditing | `visual-qa`, `v2_release_gate` plus every skill governing the changed content |
| Audio and music | `conductor`, `v2_release_gate` |
| Runtime readiness | `v2_release_gate` plus every applicable content skill |

## Foundation contracts

Runtime work must conform to:

- `docs/architecture/ENGINE_DECISION.md`
- `docs/architecture/RENDERING_LAYERS.md`
- `docs/architecture/LEVEL_CONTRACT.md`
- `docs/architecture/ANIMATION_CONTRACT.md`
- `docs/architecture/ENCOUNTER_CONTRACT.md`
- `docs/architecture/VISUAL_AUDIT_PROTOCOL.md`

Do not begin production gameplay or level implementation until the engine decision is accepted and its mandatory disposable native-platform spike has passed review. Source sheets are design references, not runtime atlases. Use independent collision geometry, preserve aspect ratios, and keep generated and runtime assets separate.

## Codex Godot execution safety

Godot 4.7.1 can crash when it cannot open its log file. Before every
Codex-initiated Godot process, locate the project root containing
`project.godot`, create `<project-root>/.codex/godot-logs/`, and verify that
directory is writable. Every invocation must explicitly include
`--log-file "<project-root>/.codex/godot-logs/<purpose>.log"`.

Never use `user://`, `~/Library/`, a nonexistent or unverified temporary
directory, or any path outside the writable project workspace for Godot
automation logs. Use `--headless` for imports, validation, script checks,
exports, and automated smoke tests unless visual QA explicitly requires an
interactive window. Never run concurrent automated import/editor processes
for the same project.

If Godot exits nonzero, do not automatically retry. Inspect the project-local
engine and output logs, report the full command and exit status, diagnose the
failure, and only then decide whether another launch is justified. Batch code
and filesystem changes before one validation pass rather than launching Godot
after every edit. Repository automation must use the shared safety helpers in
`tools/verify/godot_log_safety.sh` and `tools/verify/godot_diagnostics.sh`.

## Completion language

`v2_release_gate` is mandatory before calling any asset, animation, encounter, level, or audio integration complete. If required runtime or visual evidence cannot be produced, report `INCOMPLETE` or `CANNOT VERIFY`, never `PASS`.
