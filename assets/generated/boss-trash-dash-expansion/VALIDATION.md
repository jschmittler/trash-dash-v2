# Trash Dash Canon Repair Validation

Status: **GENERATED - AWAITING USER APPROVAL**

## Canon and source authority

- Canon ID: `boss.level-01.trash-dash`
- Canonical Boss Bible: `docs/design/trash-dash/docs/game/bosses/README.md`
- Boss canon: `docs/design/trash-dash/docs/game/bosses/TRASH_DASH.md`
- Visible authority: `docs/design/trash-dash/reference/characters/level-01/sprites/boss-trash-dash.png`
- Preserved approved atlas: `/Users/jamesschmittler/Desktop/boss-trash-dash-transparent.png`

## Output

- Complete generated candidate: `boss-trash-dash-expanded.png`
- Original region: 1536×1024 RGBA, preserved exactly
- Expanded canvas: 1536×1280 RGBA
- Added source cells: thirteen native 128×128 cells
- Resizing: none
- Independent recentering: none
- AI generation: none
- Runtime promotion: not performed

## Canonical sequences

| Sequence | Canonical frames | Timing | Result |
|---|---:|---:|---|
| EMERGE | 3, approved order | 8 FPS one-shot | PASS |
| RETREAT | 3, approved order | 8 FPS one-shot | PASS |
| DEFEAT / MELTDOWN | 7, approved order | 10 FPS one-shot/hold | PASS |

The defeat sequence ends in the canon-locked small inert refuse heap, scattered scraps, and leaking chartreuse slime. No intact-collapse reinterpretation is used.

## Bossfix contract tests

- Character Identity: **PASS** — all added visible RGB derives directly from the approved visual-authority sheet.
- Unauthorized Design Change: **PASS** — no anatomy, silhouette, material, palette, facial, outline, residue, or VFX traits were redrawn or invented.
- Animation Completeness: **PASS** — canonical 3/3/7 sequences are complete and in approved order.
- Animation Continuity: **PASS** — source scale is 1, source-lane registration is preserved, facing remains right, and ground alignment derives from the canonical board baseline.
- Sequence Meaning: **PASS** — emerge rises from sludge, retreat withdraws into sludge, and defeat visibly deflates/melts into the canonical refuse heap.
- Technical Sprite Compliance: **PASS** — complete source region is byte-identical; cells use binary transparency, native 128×128 dimensions, safe margins, and no labels, panel matte, divider lines, or neighboring-frame bleed.

## V2 release-gate scope

Static source, canon, atlas, alpha, frame, geometry, ordering, manifest, and contact-sheet validation are complete. Runtime integration, state reachability, both-facing playback, arena-release events, uninterrupted gameplay traversal, and target-resolution screenshots were not performed. V2 release-gate status therefore remains **INCOMPLETE** until those separate integration checks occur.
