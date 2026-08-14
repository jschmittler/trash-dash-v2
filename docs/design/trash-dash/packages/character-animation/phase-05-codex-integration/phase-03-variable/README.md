# Trash Dash Phase 03 Enemy Sprite Atlases

Phase 03 contains the 16 common-enemy animation source atlases for Levels 3 through 6.

## Production contract

- These are variable-canvas animation source atlases, not fixed-cell runtime sheets.
- Do not force poses into 128 x 128 or other square cells.
- Preserve each pose's natural width and height, including weapons, tails, wings, projectiles, motion trails, impact effects, and defeat poses.
- Every final PNG uses true transparency.
- The approved source sheets remain the visual reference for character identity and animation intent.
- Runtime extraction must use per-pose bounds and explicit anchor metadata rather than equal grid slicing.

## Roster

### Level 3

- Alley Cat Burglar
- Sewer Rat Courier
- Subway Roach
- Traffic-Cone Crab

### Level 4

- Beaker Slime
- Clipboard Hamster
- Mop-Bot 3000
- Phase Gecko

### Level 5

- Asteroid Armadillo
- Rocket Roach
- Satellite Hermit Crab
- Vacuum Jelly

### Level 6

- Baserunning Beaver
- Clobbering Cub
- Sliding Seagull
- Windup Weasel

## Package structure

- `final/`: cleaned transparent animation source atlases for implementation
- `qa/`: per-level contact sheets, combined review board, technical audit, and visual-review records
- `source-pack/`: approved branded reference sheets used as visual truth
- `run-manifest.json`: phase scope, method, output contract, and acceptance state

The intermediate chroma atlases are intentionally excluded from the handoff package. They remain production intermediates rather than implementation assets.

## Implementation guidance

Before importing into the game, define a rectangle and anchor for every pose or effect. Keep a consistent ground or body anchor across related states. Flying enemies should use a stable body-center anchor. Projectiles and detached effects should be extracted as separate assets. Validate playback in normal gameplay, including scale, grounding, collision geometry, z-order, and uninterrupted animation transitions.
