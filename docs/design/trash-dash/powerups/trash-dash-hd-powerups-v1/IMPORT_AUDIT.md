# Taco and Kite Power-Up Source Import Audit

Status: **SOURCE IMPORTED / RUNTIME INCOMPLETE**

The supplied `import_powerups.sh` is byte-identical to the script inside the ZIP, but it targets a generic web repository (`public/assets`) and was not executed against this Godot project. Its intent was adapted to the repository's canonical design-source conventions.

## Provenance

- Supplied ZIP SHA-256: `6763e4d6af56218fb9a84cf4982faba06d809ca8cf1588ba987d85ad8f7b5354`
- Package: `trash-dash-hd-powerups`
- Version: `1.0.0`
- Manifest status: `approved`
- All four checksums in `checksums.sha256` pass.

## Imported sources

| Source | Dimensions | Alpha | Contract |
| --- | ---: | --- | --- |
| `assets/powerups/taco-kite-powerups-clean-chroma.png` | 2172×724 | No (RGB chroma) | 11 variable-width Taco states and 11 variable-width Kite states using manifest `xCuts` |
| `assets/overlays/taco-power-overlay-clean-8frame.png` | 1536×1024 | Yes (RGBA) | Exact 4×2 grid, 384×512 per frame, sequential 8-frame overlay |
| `assets/overlays/kite-power-overlay-clean-8frame.png` | 1536×1024 | Yes (RGBA) | Exact 4×2 grid, 384×512 per frame, sequential 8-frame overlay |

The three branded boards under `reference/` were inspected at original detail against the supplied working sources. They preserve the intended Taco/Kite identity, state order, rings, particles, debris, wind trails, glow, and overlay transitions. They use new package filenames and do not overwrite the repository's earlier approved concept/sprite boards.

## Import boundary

- The package is retained unchanged beneath `docs/design/trash-dash/powerups/trash-dash-hd-powerups-v1/` except for this audit record.
- All six PNGs are design sources tracked through Git LFS.
- Nothing was copied to `assets/generated/` or `assets/runtime/`.
- No Godot scene, GDScript, power-up logic, pickup trigger, or overlay layer was changed.
- No Godot process was required or launched.

The item sheet is intentionally not runtime-ready: connected-background chroma removal must preserve legitimate green art and all soft effects. The two overlays also require per-frame alpha/bounds review, timing authoring, trigger integration, and live gameplay verification before promotion.

## Validation

```bash
tools/verify/check_powerup_source_import.sh
```

Expected:

```text
Power-up source import: PASS (3 working sources, 3 references)
```

Runtime preparation and gameplay integration remain **INCOMPLETE**.
