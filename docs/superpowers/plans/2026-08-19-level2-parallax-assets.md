# Level 2 parallax candidate plan

## Goal

Produce reviewable candidate-only three-plane background packages for the five approved Level 2 scenes, preserving the canonical night-suburb direction and keeping background art separate from gameplay geometry.

## Scope

- Create five far, five middle, and five close source masters under `assets/generated/level2-parallax/sources/`.
- Normalize to deterministic 1320×540 processed plates with static integrity checks and review evidence.
- Do not add a Level 2 runtime renderer, scene, collision, route, traversal, or release claim.

## Verification

1. Focused primitive tests pass.
2. The candidate verifier proves exact 15-plate inventory, dimensions, alpha contract, and absence of hot-magenta matte.
3. Composite, forced-wrap seam, sweep, transition, and contact-sheet review evidence is inspected before requesting owner approval.
