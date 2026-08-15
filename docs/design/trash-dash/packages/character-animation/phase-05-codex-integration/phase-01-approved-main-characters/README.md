# Trash Dash - Phase 01 Approved Main Characters

This package is the **canonical Phase 01 main-character art set** for Trash Dash. It contains the four character atlases that were visually reviewed and approved. Earlier extraction-based Phase 01 packages are rejected and superseded by this package.

## Approved character atlases

- `atlases/jimothy-powered-approved.png`
- `atlases/jimothy-regular-approved.png`
- `atlases/trashy-powered-approved.png`
- `atlases/trashy-regular-approved.png`

Each atlas has a matching Markdown guide in `docs/`. `manifest.json` is the machine-readable package index.

## Critical integration rule

**Do not run another cleanup pass on these images.** The approved atlases are already the source of truth. Codex should not perform OCR, background removal, automatic silhouette trimming, or recreate the art from the old branded sheets.

## Runtime slicing

The approved atlases are clean visual assets, but this package intentionally does **not** invent frame rectangles from the old branded sheets. During integration, define explicit frame rectangles once, visually verify them against these approved atlases, and persist those rectangles in the game's asset manifest or animation definitions. That is safer than making Codex visually rediscover the sprites at runtime.

## Character state vocabulary

The main-character animation vocabulary includes idle/stand, walk, run, jump start, midair/rise, fall, land, skid/stop, crouch, hurt/flinch, knockout/stunned, victory/celebrate, and glide/kite flight. The approved atlases may also include additional action/support poses.

## Superseded packages

Do not use Phase 01 V1, V2, or V3 extraction packages. They contained clipping or extraction artifacts and are retained only as historical attempts.

## Next step

After this package is accepted into the project, create the Codex integration prompt that imports these four atlases, defines explicit frame rectangles/pivots, replaces legacy runtime art, and performs visual QA in gameplay.
