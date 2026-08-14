# Phase 05 Canonical Import Audit

Status: **REFERENCE COMPLETE / RUNTIME INCOMPLETE**

This audit records the Stage 1 import of the approved Phase 05 character-animation handoff. It does not authorize frame extraction, runtime registration, collision geometry, state-machine timing, or replacement of existing runtime art.

## Delivery verification

- Supplied outer ZIP SHA-256: `161a3d06235d1042ddc3a28d1d4b08c5ef97f98907f5461b60e757d4546cb3cd`
- Phase 01 archive: `67ea2033d864a1792a3f959e64a54757797ff35143525b6d251d4b289501429c` — verified
- Phase 02 archive: `ffd9a6e1f86a678b9a230630589864af3709fc123c509feb741ed701a531f885` — verified
- Phase 03 archive: `54811c23a4a3f20290523005dc0afa15eae65552e72f41da2de8071228887033` — verified
- Phase 04 archive: `1fc488cfa6563289bdb955fc9db8d653a2a0d447d817e0380099ad40bbd0c343` — verified

The original archives were verified before extraction. Their unpacked contents, phase roots, original manifests, documentation, source references, approved transparent atlases, and QA records are retained here. The opaque ZIP containers were not duplicated into Git; `qa/SHA256SUMS` remains the immutable delivery receipt.

## Inventory result

| Class | Expected | Resolved | Missing | Conflicting |
| --- | ---: | ---: | ---: | ---: |
| Playable character variants | 4 | 4 | 0 | 0 |
| Common enemies | 26 | 26 | 0 | 0 |
| Bosses | 6 | 6 | 0 | 0 |
| **Total** | **36** | **36** | **0** | **0** |

Every approved atlas is an 8-bit RGBA PNG with the exact dimensions and SHA-256 recorded in `CANONICAL_IMPORT_INVENTORY.json`. The inventory contains 36 unique canonical IDs and 36 unique approved-atlas paths.

## Duplicate and naming audit

- Phases 02–04 contain 38 branded-source PNG instances representing 32 unique enemy and boss references. All 38 are byte-identical to their existing canonical files under `docs/design/trash-dash/reference/characters/`.
- The four playable-character branded references were already present under `docs/design/trash-dash/reference/main-characters/sprites/`. Phase 01 supplies separate approved transparent atlases; these were namespaced and did not overwrite the branded files with matching names.
- Canonical runtime ID `squirrel` intentionally maps to the retained source filename `squirel.png` and approved atlas `squirrel-transparent.png`.
- No missing, corrupt, or byte-conflicting source reference was found.

## Repository integration

- Imported sources live only beneath `docs/design/trash-dash/character-animation/phase-05-codex-integration/`.
- New PNGs are covered by the dedicated Git LFS rule in `.gitattributes`.
- Existing design sources and legacy assets were not modified or deleted.
- No file was added to `assets/generated/` or `assets/runtime/`.
- No scene, GDScript runtime, collision, animation, z-order, or gameplay code was changed.
- No Godot process was needed or launched for this source-only audit.

Validation command:

```bash
tools/verify/check_character_animation_import.sh
```

Expected result:

```text
Character animation import: PASS (36/36 canonical atlases)
```

## Required next gate

Stage 2 remains **INCOMPLETE**. Before any atlas can enter runtime use, each approved transparent atlas must be inspected beside its branded source; variable frame order and bounds must be authored explicitly; detached projectiles/effects must be separated where required; per-frame pivots, durations, offsets, events, attachments, hitboxes, and hurtboxes must be recorded; and native/zoomed contact sheets and playback previews must be reviewed. Ambiguous frame order or inseparable required states are stop conditions.
