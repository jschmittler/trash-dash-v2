# Asset Extraction and Runtime Use

## Important status

The source sheets are approved art sources, not production-ready atlases.

Before runtime use, every extracted asset needs:

- clean alpha
- removal of sheet background and presentation residue
- transparent padding
- edge-fringe cleanup
- consistent pixel density
- preserved aspect ratio
- explicit anchor and pivot
- state mapping
- visual QA over light and dark gameplay scenes

## Extraction workflow

1. Copy source sheets into a staging area outside production runtime folders.
2. Read `manifests/sprite-regions.json`.
3. Run `tools/extract_ui_sources.py` in raw mode first.
4. Inspect each crop and adjust regions if needed.
5. Run assisted background removal only on crops that need it.
6. Clean alpha manually where the automated result is uncertain.
7. Add 8 to 16 px transparent padding around irregular art.
8. Export runtime-ready PNG or the engine's preferred lossless format.
9. Create engine metadata for pivots, 9-slice margins, state names, and scale.
10. Validate every result in live UI, not only on a neutral asset viewer.

## Suggested extraction commands

Raw crops:

```bash
python tools/extract_ui_sources.py --package-root . --mode raw --output extracted/raw
```

Assisted GrabCut extraction:

```bash
python tools/extract_ui_sources.py --package-root . --mode grabcut --output extracted/cleaned
```

Single sheet:

```bash
python tools/extract_ui_sources.py \
  --package-root . \
  --sheet phase-01-buttons-tabs \
  --mode grabcut \
  --output extracted/phase-01
```

The assisted mode is a starting point. It must not be treated as final without visual review.

## Runtime asset categories

Recommended destination structure:

```text
assets/ui/
  materials/
  decor/
  icons/
  controls/
  tabs/
  panels/
  hud/
  notifications/
  alerts/
  results/
  rewards/
  character-select/
```

Recommended names:

```text
button-primary-default.png
button-primary-focus.png
button-primary-pressed.png
panel-cardboard-9slice.png
panel-notebook.png
notification-bottle-cap.png
alert-boss-incoming.png
character-card-trashy-selected.png
character-card-jimothy-selected.png
```

## Dynamic text

Do not ship changing text baked into sprites.

Rebuild these as runtime text or data:

- button labels
- scores
- counts
- times
- objective copy
- progress values
- settings labels
- character names if localization or renaming is possible
- level-specific result values

It is acceptable to keep permanent art lettering when it is intentionally fixed, such as a stylized Trashed It headline or New Record stamp.

## Scalable controls and panels

Use 9-slice, tiled edges, or separate layers for scalable rectangular UI.

A scalable panel should usually separate:

- center material
- top, bottom, left, and right edges
- four corners
- fasteners
- tape or stickers
- shadow
- content layer
- focus or selected overlay

Never non-uniformly stretch a full raster panel.

## Shadows

Some source assets include baked shadows. Decide per component whether to:

- preserve the baked shadow as part of the art, or
- remove it and use a shared runtime shadow

Do not stack both and create an oversized muddy halo.

## Focus and hit targets

Decorative movement must not move the logical input target.

- Keep the hit box stable.
- Animate the visual child.
- Preserve safe spacing for overshoot and shadow.
- Do not clip focus rings or selected badges.

## Character artwork

The character cards contain UI illustrations of Trashy and Jimothy.

- They are not gameplay animation sprites.
- Use contain-style scaling.
- Preserve full silhouette and aspect ratio.
- Do not crop tools, backpacks, tails, hats, ears, feet, or hands.
- Keep selected treatment on a separate layer.

## Alpha QA

Check each asset on:

- white
- black
- saturated green
- saturated magenta
- actual level background

Reject assets with:

- brown sheet residue
- bright fringe
- dark halo
- clipped shadow
- missing tape or fasteners
- unintended rectangular background
- isolated floating pixels

## Runtime QA

Do not call the import complete until:

- all manifest paths exist
- all included source files match hashes
- extracted crops can be opened
- no runtime sprite is stretched
- dynamic text is separate
- focus states are visible
- motion sequences use the token system
- reduced motion is implemented
- Character Select works for both Trashy and Jimothy
