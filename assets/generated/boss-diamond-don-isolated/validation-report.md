# Diamond Don Bossfix Validation

**VALIDATION: PASSED**

## Seven mandatory tests

- **TEST A — CHARACTER IDENTITY: PASS.** Every delivered visible RGBA pixel is copied from the accepted atlas at 1:1 scale; canonical and accepted-source hashes are locked and verified.
- **TEST B — UNAUTHORIZED DESIGN CHANGE: PASS.** Generation, replacement, redraw, resize, retouch, rotation, filtering, and runtime promotion counts are zero.
- **TEST C — ANIMATION COMPLETENESS: PASS.** EMERGE, RETREAT, and DEFEAT each have explicit approved-only starts, ordered progressions, endings, continuity statements, and pivot-aligned previews with matching frame counts.
- **TEST D — ANIMATION CONTINUITY: PASS.** Approved source order, scale, ground-contact pivot strategy, effect-envelope pivots, and transition endpoints are preserved; runtime timing remains intentionally unset.
- **TEST E — SEQUENCE MEANING: PASS.** EMERGE materializes through canonical curse imagery into idle; RETREAT intentionally reverses that vocabulary without defeat art; DEFEAT uses approved hit/fall/exhausted art and ends with the exact identifiable softened seated Don.
- **TEST F — TECHNICAL SPRITE COMPLIANCE: PASS.** All 590,058 accepted visible pixels and RGBA values are assigned exactly once; there are no omissions, duplicates, generated pixels, replacements, or atlas/frame mismatches.
- **TEST G — FRAME ISOLATION AND SPACING: PASS.** All 78 variable rectangles have two transparent frame-padding pixels plus eight transparent atlas-gutter pixels on every side; no delivered visible pixel touches a boundary or contaminates another cell.

## Commands and scope

- Build: `python3 tools/asset_pipeline/build_boss_diamond_don_isolated.py`
- Verify: `python3 tools/verify/check_boss_diamond_don_isolated.py`
- Canonical source: `docs/design/trash-dash/library/characters/bosses/diamond-don/sprites/reference/boss-diamond-don.png`
- Accepted extraction source: `docs/design/trash-dash/library/characters/bosses/diamond-don/sprites/animation-source/boss-diamond-don-transparent.png`
- Output: `assets/generated/boss-diamond-don-isolated/`

## V2 release-gate status

`INCOMPLETE / NOT PROMOTED` by design. The requested artifact is generated review material only. No runtime registration, gameplay timing, collision, uninterrupted traversal, target-resolution runtime capture, or promotion was authorized or performed.

**ARTWORK APPROVED — RUNTIME PROMOTION NOT AUTHORIZED**
