# Trash Dash v2 Secret Level 6 parallax asset package

Asset-stage package for **The Abandoned Ballpark**. Runtime integration, gameplay traversal, renderer evidence, production-event verification, and promotion into runtime/public directories are intentionally deferred.

## Contract and outputs

- Internal camera: `960x540`; processed plate: `1320x540` PNG.
- Five manifest-derived stage IDs: `entryway`, `concessions`, `stadium-seats`, `outfield`, `infield-boss-arena`. No Level 6 runtime stage record was present.
- Speeds: far `0.018`, middle `0.055`, close `0.13`.
- `sources/` preserves 15 accepted independent masters and three explicitly named rejected generations.
- `processed/` contains exactly 15 asset-stage candidates.
- `qa/composites/` contains exactly five centered `960x540` three-plane previews.
- `validation-report.json` records output hashes, dimensions, alpha values, coverage, transparency, and chroma checks.
- `prompt-manifest.json` preserves the exact final accepted prompt set and output IDs.

The deterministic processor uses centered aspect-preserving nearest-neighbor framing only. Far plates are made fully opaque. Middle and close plates are keyed locally from `#FF00FF`, conservatively boundary-contracted and navy-despilled, then written with strict binary alpha. No plane was derived from another plane or from a flattened reference.

Rebuild from the repository root:

```sh
python3 tools/asset_pipeline/build_level6_parallax.py
```

## Canonical provenance

All five references are listed as approved by `docs/design/trash-dash/manifests/APPROVAL_STATUS.tsv` and `APPROVED_FILES.txt`. Their bytes match both `SHA256SUMS.txt` and `SHA256SUMS_MASTER.txt`. Files under `archive/superseded-level-06-environments/` were not used.

| Stage | Canonical reference | SHA-256 |
|---|---|---|
| entryway | `level-6-01-entryway.png` | `1ba3d10c748e401a1d0494424a1c0c0ff7e7c0ca06e35f870dbfa82af5be5022` |
| concessions | `level-6-02-concessions.png` | `efd411315086567d94a387278caf30cc452090ac60aecc7970c7222ce3257117` |
| stadium-seats | `level-6-03-stadium-seats.png` | `b20513d39309d29357a61ccb5bc4886a070a84377d5ce0a56a0437515d7d551a` |
| outfield | `level-6-04-outfield.png` | `62d657e5ae3f4288e9a96f03dcf192a3789d267c913a95ff71330ad1ee355b49` |
| infield-boss-arena | `level-6-05-infield-boss-arena.png` | `725ff6bce6357dbd0230c307275c681fd808c06ad5261bb3f14eae6357c67b2d` |

## Accepted built-in generation IDs

| Plate | Output ID |
|---|---|
| entryway far | `exec-e7a759c7-59e5-493e-9f0a-a2a38d6e0d30.png` |
| entryway middle | `exec-b9fbb688-8da9-42c5-9fb1-032ab11c4706.png` |
| entryway close | `exec-c9107cd5-2f1b-490d-8151-263bfa53a4d1.png` |
| concessions far | `exec-32edbcd1-758d-494c-acba-d6d530eb9bef.png` |
| concessions middle | `exec-2d520788-02e6-416e-a78a-20090fc0072f.png` |
| concessions close | `exec-e4c36701-c7e5-4a01-8835-849ac91373f3.png` |
| stadium-seats far | `exec-f9d59a3c-da52-449d-84e8-3a34adfc26a1.png` |
| stadium-seats middle | `exec-aa0c24c5-0f9a-49d1-a754-55a149c9ac8e.png` |
| stadium-seats close | `exec-bd2a03c7-c016-4cfa-8825-e1f11fafee2e.png` |
| outfield far | `exec-da3de461-357c-4ac3-b2dd-ef40358fb82c.png` |
| outfield middle | `exec-74ac2270-b446-4080-a5a0-dd9bb74eddd5.png` |
| outfield close | `exec-dc1d6b44-72aa-4fb1-8d48-49383d702ed8.png` |
| infield-boss-arena far | `exec-09fd658e-645d-4309-86fa-3de51c478798.png` |
| infield-boss-arena middle | `exec-813e2e58-f300-40b8-8f93-932234a20232.png` |
| infield-boss-arena close | `exec-8e7521ab-432e-4c22-a010-09328e0ddd53.png` |

## Landmark ownership

- Far owns opaque atmosphere, distant stadium massing, and broad remote depth only.
- Middle owns every complete contextual landmark: entry structures; concession groups; seating/press/aisle groups; ivy wall/bleacher/gate groups; and arena dugouts/scoreboard/equipment.
- Close owns only sparse disconnected edge fragments. It contains no complete landmark or continuous frame.
- Terrain, collision, platforms, actors, effects, hazards, interactive fixtures, traversal, boss supports, unlock behavior, and HUD remain runtime-owned.

## Rejection history

- `level6-stadium-seats-far-source-rejected-platform-slab.png`: rejected because a high-contrast foreground slab read as a collision-bearing platform. Replaced by an independent generation with only distant field depth in the lower region.
- `level6-infield-boss-arena-middle-source-rejected-center-obstruction.png`: rejected because groundskeeping equipment occupied the protected boss combat center.
- `level6-infield-boss-arena-middle-source-rejected-purple-matte-and-duplicate-scoreboard.png`: rejected because dark-magenta object colors produced a visible purple matte impression and its scoreboard duplicated the far landmark too literally.

## QA status

- Canonical provenance and checksum verification: `PASS`.
- Asset-stage static PNG validation: `PASS`.
- Asset-stage centered composite inspection: `PASS` after targeted regeneration and deterministic boundary despill.
- Runtime integration, renderer wrap/sweep behavior, smoothstep transitions, uninterrupted traversal, boss-arena gameplay, target-resolution runtime evidence, and production-event verification: `DEFERRED`.
- Overall V2 runtime release gate: `INCOMPLETE` until runtime evidence exists.

