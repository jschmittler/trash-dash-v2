# Trash Dash HD Remake - Taco + Kite Power-Up Package

This is the approved production package for the Taco Power and Kite Power item art and their pickup overlay animations.

## Runtime assets

- `assets/powerups/taco-kite-powerups-clean-chroma.png` - clean Taco/Kite item sprite sheet, 11 states per row
- `assets/overlays/taco-power-overlay-clean-8frame.png` - clean 8-frame Taco pickup overlay
- `assets/overlays/kite-power-overlay-clean-8frame.png` - clean 8-frame Kite pickup overlay
- `manifest.json` - authoritative frame order, crop hints, dimensions, and implementation rules

## Reference assets

The files under `reference/` are the approved branded boards used to verify fidelity. They should not ship in the runtime build.

## Import into a repo

From the unzipped package:

```bash
./scripts/import_powerups.sh /path/to/trash-dash-hd-remake
```

The default destination is `public/assets/trash-dash/powerups` inside the target repo. Override it with `ASSET_ROOT`:

```bash
ASSET_ROOT=src/assets ./scripts/import_powerups.sh /path/to/trash-dash-hd-remake
```

Set `INCLUDE_REFERENCES=1` if you also want the branded reference art copied into the repo. Set `FORCE=1` to overwrite an existing import.

## Codex

After importing, give Codex `CODEX_IMPORT.md`. It tells Codex how to preserve the approved art, key the chroma safely, create persistent frame metadata, connect Taco/Kite pickup overlays, and validate the integration in live gameplay.
