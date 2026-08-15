# Level 3 Parallax Generation Record

Status: generated and statically validated; production-runtime verification is unavailable in this foundation checkout.

## Contract

- Camera: 960×540.
- Runtime plates: 1320×540 PNG.
- Stages: `restaurant-alley`, `rainy-downtown-avenue`, `rooftop-run`, `subway-maintenance-tunnels`, `construction-site-finale`.
- Layers/speeds: `far` 0.018, `middle` 0.055, `close` 0.13.
- Far plates are opaque RGB. Middle and close plates use binary hard alpha.
- Source masters, processed outputs, and runtime candidates are separate.

## Provenance

- Generator: built-in Codex `image_gen` tool (`gpt-image-2` path), 2026-08-13.
- Reference role: approved visual direction only, not edit targets.
- Approved references: `docs/design/trash-dash/library/environments/backgrounds/level-03/level-3-01-restaurant-alley.png` through `level-3-05-construction-site-finale.png`.
- Manifest approval and SHA-256 matches were verified before generation.
- Exact approved prompt set is preserved in the originating Codex task; prompt responsibilities and ownership are summarized in `prompts/plate-prompts.md`.

## Derivation

```sh
/Users/jamesschmittler/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  tools/asset_pipeline/process_level3_parallax.py

/Users/jamesschmittler/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  tools/asset_pipeline/validate_level3_parallax.py

/Users/jamesschmittler/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 \
  tools/asset_pipeline/render_level3_parallax_evidence.py
```

Processing uses a centered aspect-preserving crop followed by nearest-neighbor resize. Magenta-keyed moving plates are converted to strict alpha values 0/255 without feathering or soft mattes.

## Directories

- `source-masters/`: selected generator output before normalization/key removal.
- `processed/`: normalized reviewed candidates.
- `public/assets/backgrounds/`: runtime-named candidates.
- `tools/visual-audit/evidence/level3-parallax/`: background-only sweep/checkpoint evidence.

The repository currently has no Level 3 runtime record, gameplay renderer, `package.json`, canonical npm parallax validator, or Level 3 checkpoints. Therefore production build, production-renderer camera sweep, console inspection, and uninterrupted gameplay traversal remain `CANNOT VERIFY`.
