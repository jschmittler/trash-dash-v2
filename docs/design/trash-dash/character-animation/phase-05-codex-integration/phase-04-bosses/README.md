# Trash Dash Phase 04 Boss Animation Source Atlases

Phase 04 contains the six boss animation source atlases for Levels 1 through 6.

## Boss roster

- Level 1: Trash Dash
- Level 2: Brutus the Bin-Hound
- Level 3: His Greasiness, the Pizza Rat King
- Level 4: Project O.P.O.S.S.U.M.
- Level 5: Galactogobbler, Hoarder of Worlds
- Level 6: The Diamond Don

## Production contract

- These are variable-canvas animation source atlases, not fixed-cell runtime sheets.
- Do not force boss poses into square or equal-sized cells.
- Preserve oversized attacks, transformations, projectiles, props, summoned objects, arena hazards, damage phases, defeat sequences, and reveal forms.
- All final PNG files use true transparency.
- Runtime extraction should define independent bounds and anchors for each pose, projectile, prop, or effect.
- Validate scale, grounding, collision geometry, z-order, transitions, and uninterrupted boss gameplay after integration.

## Package structure

- `final/`: six cleaned transparent boss atlases
- `qa/`: paired and combined contact sheets plus visual-review records
- `source/`: approved branded boss references used as visual truth
- `run-manifest.json`: scope, method, output contract, and acceptance state

Intermediate chroma-key atlases are excluded because they are production artifacts rather than implementation assets.
