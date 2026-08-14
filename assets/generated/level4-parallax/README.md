# Trash Dash v2 Level 4 parallax asset package

Asset-only package for Level 4, **Secret Space Center**. Runtime integration is intentionally deferred.

## Contract

- Internal camera: `960x540`.
- Runtime plates: `1320x540` PNG.
- Plane speeds: far `0.018`, middle `0.055`, close `0.13`.
- Far plates are fully opaque.
- Middle and close sources use `#FF00FF`; reviewed outputs use strict binary alpha.
- Normalization uses centered aspect-preserving crop for far plates and centered aspect-preserving fit for moving plates, always with nearest-neighbor sampling.
- Stage identifiers are manifest-derived because no Level 4 runtime stage record existed at production time.

## Directories

- `sources/`: accepted generated source masters plus explicitly named rejected attempts.
- `processed/`: reviewed normalized runtime candidates.
- `qa/composites/`: centered `960x540` three-plane checkpoints.
- `qa/seams/`: forced-wrap evidence for every stage and layer.
- `qa/transitions/`: five-frame monotonic smoothstep contact sheets.
- `qa/sweeps/`: background-only forward/reverse sampling evidence.
- `../../../public/assets/backgrounds/`: promoted reviewed asset-only candidates.

## Rebuild

```sh
/Users/jamesschmittler/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 tools/asset_pipeline/process_level4_parallax.py
```

The processor performs only centered aspect-preserving framing, nearest-neighbor resizing, local chroma removal, binary-alpha conversion, and discrete terminal-column seam matching. It does not stretch, blur, antialias, or derive one plane from another.

## Canonical references

All five references were approved by `docs/design/trash-dash/manifests/APPROVAL_STATUS.tsv` and `APPROVED_FILES.txt`. Current file hashes matched `SHA256SUMS.txt` and `SHA256SUMS_MASTER.txt` before generation.

| Stage | Canonical reference SHA-256 |
|---|---|
| hidden-service-entrance | `5134992bc6e733b2e87d9ae13ca58e2dabac2eb565d22160fc4dc4cd7214b4cf` |
| experimental-laboratory | `d679ab35db6b85053d8eda600aa5b9da8bbc17461c3113137bd860d487743eb4` |
| robotics-assembly-chamber | `d9274dda9225e49ca85aa0096ffc4d73c5308e4148e96e946c7212aa074f0439` |
| zero-gravity-research-chamber | `6a6ae27c1010bb84b806303181d265e1a8aba5db2423dc5314e2cceb40f6c68c` |
| rocket-hangar-finale | `e3c5e997e59a1ffa9f083cd1a3276922168825fa6b5e9c4864a4896d5d98c3b6` |

## Generation provenance

Generator: built-in Codex image generation, one independent request per plate. Canonical references were supplied only as visual-direction references, never edit targets.

Final accepted generation output IDs:

| Plate | Generated output ID |
|---|---|
| hidden-service-entrance far | `exec-e05c7dd0-a90e-42ed-b408-18d5beb3be1e.png` |
| hidden-service-entrance middle | `exec-2a0eb86b-bd59-4d29-8d62-95a3665d02ac.png` |
| hidden-service-entrance close | `exec-45116c9d-b938-4c83-a3a8-4dcc9c8e8b90.png` |
| experimental-laboratory far | `exec-ab19d0b7-3a46-4936-8766-57c176804111.png` |
| experimental-laboratory middle | `exec-022db677-8704-4caf-b79c-6b50e4519af5.png` |
| experimental-laboratory close | `exec-50f6e841-6471-4ec3-9521-6c234530d747.png` |
| robotics-assembly-chamber far | `exec-b693ac62-030e-4f06-902a-5d541b99e6db.png` |
| robotics-assembly-chamber middle | `exec-e832dfef-85f5-4a6f-82a5-3c1d65e3531a.png` |
| robotics-assembly-chamber close | `exec-9c5bf164-3c2c-4762-b3cb-c736c596f333.png` |
| zero-gravity-research-chamber far | `exec-3fede09f-4d10-4fbc-a189-6ac9ddd0aa40.png` |
| zero-gravity-research-chamber middle | `exec-8891b85f-1f06-4cc2-99c6-fc71c61083c2.png` |
| zero-gravity-research-chamber close | `exec-da2b7b08-f612-42eb-89bc-87af78fe3896.png` |
| rocket-hangar-finale far | `exec-3f319087-ff37-4e03-addd-63b1c07f526f.png` |
| rocket-hangar-finale middle | `exec-2985e41e-8fd4-4306-8712-29b3c022149d.png` |
| rocket-hangar-finale close | `exec-39d66072-12f7-4c17-a876-1e76441a23ca.png` |

Rejected generations remain in `sources/` with `-rejected` in their names. Rejection causes included platform-like framing, traversal architecture, humanoid-looking robot parts, ignored chroma instructions, landmark duplication risk, and insufficiently sparse close framing.

## Exact prompt record

The complete user-approved fifteen-prompt set is preserved verbatim in the Codex task transcript. Final accepted retries used the same approved plane ownership and negative constraints with these exact corrective additions:

- Far retries: `BACK WALL SHELL ONLY`; no floor, ledge, walkway, platform, catwalk, ladder, or runtime-owned structure; quiet matching material at both horizontal edges.
- Sparse close retries: only six tiny disconnected edge fragments; no bottom-edge object, continuous frame, ladder, housing, or central obstruction; at least 90% uniform `#FF00FF`.
- Robotics middle retry: four separated machine cutouts—one compact press, one short inactive uneven-top conveyor, one compact suspended tool gantry, and one bin of loose hands/gears/panels; no ramps or humanoid torsos, heads, or legs.
- Zero-gravity middle retry: one gyroscopic ring, one horseshoe magnetic assembly, three sealed box modules, and five tiny debris shards; no environmental wall, fan, platform, rail, or second circular object.
- Rocket middle retry: exactly one full-height rocket, one compact recessed service tower, two short disconnected maintenance arms, one closed elevator housing, and compact fueling pipes; no connected walkway or scaffolding.

The transcript remains the exact authority for the shared headers, plate-specific requests, reference roles, speeds, keying behavior, alpha intent, negative constraints, and risk notes approved before generation.

## Review status

- Asset-stage static validation: PASS.
- Asset-stage composite, seam, sweep, and transition review: PASS.
- Runtime integration, uninterrupted gameplay traversal, renderer inspection, production event verification: DEFERRED by task scope.
- Overall V2 runtime release gate: INCOMPLETE until integration and runtime evidence exist.
