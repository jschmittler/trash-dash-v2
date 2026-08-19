# Level 2 parallax candidate evidence

## Scope and status

Fifteen candidate-only 1320×540 parallax plates were generated for the approved Level 2 **Suburban After Dark** reference progression: moonlit backyard, garbage night street, backyard obstacle course, drainage ditch and culvert, and suburban main street.

- **Asset-stage review:** PASS pending owner visual approval.
- **Runtime/traversal/renderer/release:** INCOMPLETE. No Level 2 scene or parallax renderer was added.

## Canonical-source provenance

The immutable visual references are the cataloged `approved-source` files in `docs/design/trash-dash/library/environments/backgrounds/level-02/`:

- `level-2-01-moonlit-backyard.png` — `c040f99b882db3931c133393711d3374f207e8174991cd9e66ec26a0b602bfb5`
- `level-2-02-garbage-night-street.png` — `3e0f803153ad7714bb1f6368885daac2686769ccead2d93908ede2f0a9199ec5`
- `level-2-03-backyard-obstacle-course.png` — `d35c6d9796b423bb53c45dab55dd22148f78bfee3968c046d6f74b46275ca7c5`
- `level-2-04-drainage-ditch-and-culvert.png` — `5b98903b39d8de949f40186976a99b49b4cee14ba428ee14b92d1aa45abfe63f`
- `level-2-05-suburban-main-street.png` — `b7559ed0da19f435bdbf6465b0094ceebf3e907972806dc03d08d50dd0f64597`

Each candidate stage has an opaque far vista plus middle and close isolated keyed scenic plates. Moving plates deliberately exclude route, collision, platform, player, enemy, pickup, and hazard semantics.

## Verification and visual QA

- `python3 -m unittest tests.asset_pipeline.test_level1_parallax tests.asset_pipeline.test_level2_parallax` — 6/6 pass.
- `python3 tools/verify/check_level2_parallax.py` — exact 15-asset inventory, PNG readability, 1320×540 dimensions, far-plane opacity, binary moving alpha, and no opaque hot-magenta matte.
- Static QA is generated under `assets/generated/level2-parallax/qa/`: composites, forced-wrap seams, forward/reverse sweeps, and transitions.
- The ignored inspection sheets at `tools/visual-audit/evidence/level2-parallax/` were reviewed for clean chroma removal, full silhouettes, foreground/middle/far separation, and no incidental characters or UI.

The broad design-library audit is not cited as a pass: existing uncataloged `.DS_Store` files outside this package remain a separate repository hygiene issue.
