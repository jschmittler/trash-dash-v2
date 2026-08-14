# Trash Dash v2 Level 5 parallax asset package

Asset-only package for Level 5, **Raccoon in Space**. Runtime integration and production-event verification are intentionally deferred.

## Contract and outputs

- Internal camera: `960x540`; runtime plate: `1320x540` PNG.
- Exactly five manifest-derived stage IDs: `low-earth-orbit`, `satellite-graveyard`, `nebula-asteroid-mine`, `abandoned-alien-station`, and `intergalactic-junk-world`. No newer Level 5 runtime record was present.
- Speeds: far `0.018`, middle `0.055`, close `0.13`.
- `sources/` preserves all 15 accepted independent source masters.
- `processed/` contains the 15 normalized runtime candidates.
- `qa/composites/` contains centered `960x540` three-plane asset-review checkpoints.
- `validation-report.json` records dimensions, hashes, alpha values, coverage, and chroma checks.

The processor uses centered aspect-preserving nearest-neighbor framing only. Far plates are made fully opaque. Middle and close sources are locally keyed from `#FF00FF`, conservatively despilled at the matte boundary, and converted to strict binary alpha. No plane was derived by cropping, masking, or separating another plane or the flattened concept reference.

## Rebuild and validation

```sh
/Users/jamesschmittler/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 tools/asset_pipeline/build_level5_parallax.py
```

Static validation requires exactly 15 files, `1320x540` dimensions, zero transparency in far plates, only alpha `0/255` in moving plates, zero visible chroma, and at least 75% transparency in close plates. Current close transparency is 91.3–93.0%.

## Canonical references

All references were approved by `APPROVAL_STATUS.tsv` and `APPROVED_FILES.txt`; their current hashes matched both checksum manifests before generation.

| Stage | Canonical reference SHA-256 |
|---|---|
| low-earth-orbit | `bdbbc6e36a789c4b004f522db368012ef91e85c6412c5d345f0174373542b4bc` |
| satellite-graveyard | `a6829c852db5d23341bea3b1b337be1c17b4afd7bfa4761f92dda69f5ff97d34` |
| nebula-asteroid-mine | `9856d07ac439507d7f6972101a67fc94b9359fdea0da848e5e8cf8228fe2ca98` |
| abandoned-alien-station | `6b44edba27c1401fedef0f5203ae75fa7cffda66bd64e1e7c605af94ec225e97` |
| intergalactic-junk-world | `b9f65ce38f786ece180aede33fbfa064b5eec56d4573929f5cf10abcc7198610` |

## Generation provenance

Generator: built-in Codex image generation. Each plate used one independent request and its corresponding canonical reference only as visual direction, never as an edit target.

| Plate | Generated output ID |
|---|---|
| low-earth-orbit far / middle / close | `exec-4c9a5943-6b99-4cb9-8f49-04c94081043e.png` / `exec-104a8c08-fac1-489d-b436-f80328cc869e.png` / `exec-bbcaa157-ba00-4201-9ae4-f6473fabd728.png` |
| satellite-graveyard far / middle / close | `exec-13231d4a-7e77-4fdb-9b7b-084f99978b8a.png` / `exec-bc4bf9ce-412c-4691-a255-b153e384a340.png` / `exec-0a316d70-3fc8-4f2d-9bef-485f02a462ee.png` |
| nebula-asteroid-mine far / middle / close | `exec-e2e7dc7b-9c2f-49b0-aba6-eb550fcf2291.png` / `exec-fc739cb9-729d-41c1-9ba8-82db49522e4a.png` / `exec-8ecd601e-4a61-480d-a3f3-ea98723c90f0.png` |
| abandoned-alien-station far / middle / close | `exec-423d9d44-6af1-477e-a1c5-8ee6ebdbace6.png` / `exec-72f8701f-540e-406a-8c7c-f0f627f6b3de.png` / `exec-209c1e62-a606-4c5e-80bd-40c8de9ea6b9.png` |
| intergalactic-junk-world far / middle / close | `exec-3cefd1d6-447e-45e6-aa48-3871c461d3a4.png` / `exec-a1783f33-ff12-4b37-9b93-cb699a608cc4.png` / `exec-0071556a-132a-4ec6-94ff-9b6f4834764a.png` |

## Prompt record and ownership

The exact 15 structured prompts are preserved in the Codex task transcript. Each shared header specified polished late-16-bit pixel art, hard clusters, dark contours, three-to-four-value shading, centered wide framing, quiet edge zones, the x≈346 reading corridor, and the full no-gameplay/no-soft-effects constraint set. Plane-specific prompts assigned every major landmark exactly as required by the user contract: far atmosphere/depth, complete contextual landmarks on middle, and sparse disconnected framing on close. The unique glowing trash-can monument appears only in the Stage 5 middle source.

## Review status

- Canonical provenance and checksum verification: `PASS`.
- Asset-stage static PNG validation: `PASS`.
- Asset-stage centered composite inspection: `PASS` after conservative fringe despill.
- Runtime integration, wrap/sweep behavior in the renderer, monotonic smoothstep transitions, gameplay traversal, and production-event verification: `DEFERRED` by task scope.
- Overall V2 runtime release gate: `INCOMPLETE` until those runtime checks exist.
