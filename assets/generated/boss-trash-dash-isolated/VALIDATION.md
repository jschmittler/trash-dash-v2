# Trash Dash Isolated Sheet Validation

Status: **ARTWORK APPROVED**

Approval scope: the project owner approved the isolated sprite sheet in this task. Runtime promotion and gameplay integration remain separate release gates.

## Output

- Complete sheet: `boss-trash-dash-isolated.png`
- Layout metadata: `manifest.json`
- Review image with cell boundaries: `contact-sheet.png`
- Frame count: 96 approved animation and gameplay-support sprites
- Layout: explicit variable frame rectangles
- Transparent gutter: 8 source pixels on all four sides of every frame
- Source scale: 1
- AI generation: none
- Resizing, filtering, redrawing, retouching: none
- Runtime promotion: not performed

## Contract validation

- Character Identity: **PASS** — every visible character and effect pixel comes from approved source material.
- Unauthorized Design Change: **PASS** — no sprite was redrawn or reinterpreted.
- Animation Completeness: **PASS** — all approved states remain in locked pose order; emerge is 3 frames, retreat is 3, defeat is 7, and Toxic Ooze Spit is 5.
- Animation Continuity: **PASS** — scale, facing, logical pivot, and internal registration are preserved in manifest metadata.
- Sequence Meaning: **PASS** — the approved sludge emerge/retreat mechanism and inert refuse-heap defeat endpoint remain unchanged.
- Technical Sprite Compliance: **PASS** — RGBA hashes are recorded per frame; atlas composition preserves every visible source pixel and normalizes only invisible RGB beneath alpha 0.
- Frame Isolation and Spacing: **PASS** — every declared frame rectangle is disjoint and contains an 8-pixel transparent gutter on all four sides.

Validation command:

`python3 tools/verify/check_boss_trash_dash_isolated.py`
