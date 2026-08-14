# Brutus Bin Hound Bossfix Validation Report

Validation date: 2026-08-13  
Asset status: `ARTWORK APPROVED`  
Approval scope: Level 2 Brutus Bin Hound isolated artwork package; runtime promotion remains unauthorized  
Validated frame/support-sprite count: 103  
Approved visible pixels reconstructed exactly once: 512248  
Atlas: `assets/generated/boss-brutus-bin-hound-isolated/boss-brutus-bin-hound-isolated.png` (2048×893, RGBA)  
Atlas gutter: 8px transparent on all four sides of every declared cell

## Seven mandatory tests

### TEST A — CHARACTER IDENTITY: PASS

All 512248 approved visible RGBA pixels reconstruct the accepted transparent source exactly once at source scale 1. The accepted source is tied to canonical board SHA-256 `ddf2eb77ad8f16aa164a934b08ea6b64c0679c24bf9c3a92a4fa444813c25c1c`; no identity-bearing artwork was redrawn or generated.

### TEST B — UNAUTHORIZED DESIGN CHANGE: PASS

`GENERATE NEW = 0`, `REPLACE UNAPPROVED = 0`, and all 103 operations are `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`. No scaling, filtering, rotation, retouching, redrawing, or visible-pixel changes occurred.

### TEST C — ANIMATION COMPLETENESS: PASS

EMERGE contains 4 ordered frames, RETREAT contains 5 ordered frames, and DEFEAT contains 5 ordered frames. The complete accepted atlas inventory contains 103 unique ordered logical frames/support sprites with no duplicate frame IDs.

### TEST D — ANIMATION CONTINUITY: PASS

Approved pose order and canonical right-facing orientation are unchanged. Character pivots retain each source-space largest-body ground contact through explicit `pivotInFrame` and `pivotInCell` metadata; output scale remains 1. Runtime duration is intentionally unset rather than invented.

### TEST E — SEQUENCE MEANING: PASS

- EMERGE: closed shell → partial reveal → fuller reveal → active state.
- RETREAT: active state → progressive intentional withdrawal → departure/dust end state, without defeat damage.
- DEFEAT: collapse → dizzy reaction → splash-down → soaked state → pacified kiddie-pool end state.

These meanings match the approved canonical board and accepted atlas; no new entrance, exit, or defeat mechanism was introduced.

### TEST F — TECHNICAL SPRITE COMPLIANCE: PASS

The output is a complete transparent RGBA sheet using manifest-defined variable rectangles. Every extracted PNG round-trips byte-for-byte through its atlas art rectangle, source/output scale is 1, every visible pixel matches its approved source coordinate, and the accepted source has zero omitted or duplicated visible pixels.

### TEST G — FRAME ISOLATION AND SPACING: PASS

Every extracted frame has transparent pixels between its visible bounds and extraction boundary. Every packed cell has an additional 8px transparent gutter on all four sides. Declared cells do not overlap. Connected-component ownership masks separate approved frames whose rectangular source envelopes overlapped, and every detached component has integrated-frame or standalone ownership metadata.

## Reproducibility

```sh
python3 tools/asset_pipeline/build_boss_brutus_bin_hound_isolated.py
python3 tools/verify/check_boss_brutus_bin_hound_isolated.py
```

## V2 release-gate scope

This batch intentionally stops in `assets/generated/`. No runtime asset, engine registration, collision, encounter, or gameplay path was changed. Running-game traversal and target-resolution runtime verification are therefore not applicable to this approval-stage source package and cannot be used to claim runtime readiness. Runtime promotion remains blocked pending explicit user approval and a later release-gated integration task.
