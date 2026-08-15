# Galactogobbler Bossfix Validation

**VALIDATION: PASSED**

## Seven mandatory tests

- **TEST A — CHARACTER IDENTITY: PASS.** Every delivered visible RGBA pixel is copied from the accepted atlas at 1:1 scale; the canonical reference and accepted atlas hashes are locked and verified.
- **TEST B — UNAUTHORIZED DESIGN CHANGE: PASS.** Generation, replacement, redraw, resize, rotation, filtering, retouching, and runtime promotion counts are all zero.
- **TEST C — ANIMATION COMPLETENESS: PASS.** EMERGE, RETREAT, and DEFEAT have explicit approved-only starts, ordered progressions, endings, continuity statements, and pivot-aligned previews with matching frame counts.
- **TEST D — ANIMATION CONTINUITY: PASS.** Source order, 1:1 scale, stable declared pivots, complete per-state ordering, and approved transition endpoints are preserved; timing remains intentionally unset pending approval.
- **TEST E — SEQUENCE MEANING: PASS.** EMERGE resolves from canonical emblem-bag/reassembly art to active idle; RETREAT intentionally recalls into the reversible emblem-bag state; DEFEAT sheds the approved shell and ends on the living identifiable alien with cyan canister.
- **TEST F — TECHNICAL SPRITE COMPLIANCE: PASS.** All 494,403 accepted visible pixels and their RGBA values are assigned exactly once; there are no omissions, duplicates, generated pixels, or atlas/frame mismatches.
- **TEST G — FRAME ISOLATION AND SPACING: PASS.** All 224 variable rectangles have transparent inner extraction padding and eight transparent atlas-gutter pixels on every side; no delivered visible pixel touches a rectangle boundary or contaminates another cell.

## Commands and scope

- Build: `python3 tools/asset_pipeline/build_boss_galactogobbler_isolated.py`
- Verify: `python3 tools/verify/check_boss_galactogobbler_isolated.py`
- Canonical source: `docs/design/trash-dash/library/characters/bosses/galactogobbler/sprites/reference/boss-galactogobbler.png`
- Accepted extraction source: `docs/design/trash-dash/library/characters/bosses/galactogobbler/sprites/animation-source/boss-galactogobbler-transparent.png`
- Output: `assets/generated/boss-galactogobbler-isolated/`

## V2 release-gate status

`INCOMPLETE / NOT PROMOTED` by design. This package is generated review material only. No runtime registration, gameplay timing, collision, real-runtime traversal, target-resolution capture, or promotion was authorized or performed.

**ARTWORK APPROVED — RUNTIME PROMOTION NOT AUTHORIZED**
