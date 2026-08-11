# Trash Dash 2.0 Project Instructions

## Clean-room boundary

Trash Dash 2.0 is a selective greenfield rebuild. The sibling V1 repository at `../trash-dash/` is read-only reference material. Never modify it and never copy its production source tree, level modules, spawn tables, runtime atlases, runtime art, or implementation code into this repository without an approved reuse-matrix change.

The canonical design source is `docs/design/trash-dash/reference/`, interpreted through the approval files in `docs/design/trash-dash/manifests/`. Files under any `archive/` path are noncanonical and may not enter V2 runtime work.

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

## Completion language

`v2_release_gate` is mandatory before calling any asset, animation, encounter, level, or audio integration complete. If required runtime or visual evidence cannot be produced, report `INCOMPLETE` or `CANNOT VERIFY`, never `PASS`.
