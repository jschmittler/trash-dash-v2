# Pizza Rat King Bossfix Validation Report

Validation date: 2026-08-13  
Asset status: `ARTWORK APPROVED`  
Approval scope: Level 3 Pizza Rat King isolated artwork package; runtime promotion remains unauthorized  
Validated physical frame/support-sprite count: 74  
Approved visible pixels reconstructed exactly once: 538601  
Atlas: `assets/generated/boss-pizza-rat-king-isolated/boss-pizza-rat-king-isolated.png` (2048×857, RGBA)  
Atlas gutter: 8px transparent on all four sides of every declared cell

## Seven mandatory tests

### TEST A — CHARACTER IDENTITY: PASS

All 538601 approved visible RGBA pixels reconstruct the accepted transparent source exactly once at source scale 1. The source is tied to canonical-board SHA-256 `ee5c495e2f0e2cdcca6735ef472a0c3b47fe53ec23a58a0e96e6a7e7457f7255`; no identity-bearing artwork was redrawn or regenerated.

### TEST B — UNAUTHORIZED DESIGN CHANGE: PASS

`GENERATE NEW = 0`, `REPLACE UNAPPROVED = 0`, and all 74 physical operations are `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`. No scaling, filtering, rotation, retouching, redrawing, new damage, or new effects occurred.

### TEST C — ANIMATION COMPLETENESS: PASS

EMERGE has 5 ordered approved frame references, RETREAT has 5, and DEFEAT has 5. Every sequence has a declared start, intermediate progression, end, and continuity connection. The package contains 74 unique physical frames/support sprites and three pivot-aligned animated previews.

### TEST D — ANIMATION CONTINUITY: PASS

Approved pose order and right-facing orientation are unchanged. EMERGE decelerates from approved rush poses into idle; RETREAT accelerates from idle into approved exit motion; DEFEAT follows approved hit and crash/stunned poses to the face-down king. Source/output scale remains 1 and every physical frame has explicit pivot/ground metadata. Runtime duration is intentionally unset rather than invented.

### TEST E — SEQUENCE MEANING: PASS

- EMERGE: off-screen dust cue → approved right-facing entry rush → charge slowdown → active idle.
- RETREAT: active idle → approved charge acceleration → right-facing exit → off-screen dust cue, without defeat imagery.
- DEFEAT: hit reaction → crash/stunned collapse → face-down defeated king, still visibly the exact approved character. The rat/crown reveal remains separate approved post-defeat support art.

No new entrance mechanism, defeat damage, or character redesign was introduced.

### TEST F — TECHNICAL SPRITE COMPLIANCE: PASS

The output is a complete transparent RGBA sheet using manifest-defined variable rectangles. Every extracted PNG round-trips byte-for-byte through its atlas art rectangle, source/output scale is 1, every visible pixel matches its approved source coordinate, and the accepted source has zero omitted or duplicated visible pixels.

### TEST G — FRAME ISOLATION AND SPACING: PASS

Every extracted frame has transparent pixels between its visible bounds and extraction boundary. Every packed cell has an additional 8px transparent gutter on all four sides. Declared cells do not overlap. Reviewed ownership masks isolate previously touching/overlapping source envelopes, including the accepted fast-run bridge seam, and every detached component has integrated-frame or standalone ownership metadata.

## Reproducibility

```sh
python3 tools/asset_pipeline/build_boss_pizza_rat_king_isolated.py
python3 tools/verify/check_boss_pizza_rat_king_isolated.py
```

## V2 release-gate scope

This batch stops in `assets/generated/`. No runtime asset, engine registration, collision, encounter, or gameplay path changed. Running-game traversal and target-resolution runtime verification are therefore outside this approval-stage package and cannot support a runtime-readiness claim. Runtime promotion remains blocked pending explicit user approval and a later release-gated integration task.
