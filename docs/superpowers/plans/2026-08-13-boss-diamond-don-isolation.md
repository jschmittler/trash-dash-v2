# Diamond Don Isolation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a generated-only, lossless Diamond Don isolation package with variable rectangles, complete approved-only EMERGE/RETREAT/DEFEAT previews, and reproducible seven-test verification.

**Architecture:** A deterministic Pillow builder partitions every opaque accepted-atlas pixel through reviewed, disjoint ownership regions, reconstructs each frame at 1:1 RGBA with transparent padding, packs variable cells with eight-pixel gutters, and emits manifests/evidence before the physical sheet. A separate verifier reconstructs ownership independently and rejects changed hashes, omitted or duplicated pixels, contaminated gutters, incomplete sequences, or runtime promotion.

**Tech Stack:** Python 3, Pillow, JSON, SHA-256, PNG RGBA, GIF previews.

## Global Constraints

- Canonical source SHA-256: `f6132b478842f9cf6a5d54b32072e3ac1027aad3b1835350b40be680b483f5ac`.
- Accepted atlas SHA-256: `7376000f332ef2ee4d58602b0843018c908ccbb0cd014fefb8e38d3704252bb8`.
- Every accepted visible pixel and RGBA value is assigned exactly once at source scale 1.
- Every physical item is `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`; `GENERATE NEW` and `REPLACE UNAPPROVED` remain zero.
- No redraw, resize, resampling, rotation, retouch, filtering, cleanup, or runtime promotion.
- Outputs remain under `assets/generated/boss-diamond-don-isolated/` and end at `GENERATED - AWAITING USER APPROVAL`.
- Runtime timing remains unset because promotion and gameplay integration are outside scope.

---

### Task 1: Deterministic atlas builder

**Files:**
- Create: `tools/asset_pipeline/build_boss_diamond_don_isolated.py`
- Create during execution: `assets/generated/boss-diamond-don-isolated/**`

**Interfaces:**
- Consumes: canonical and accepted PNG paths plus the attached byte-identical desktop copy.
- Produces: `manifest.json`, `batch-manifest.json`, `source-audit.json`, immutable specification, isolated frames/support effects, transparent atlas, contact sheet, previews, validation placeholder, and approval-status handoff.

- [ ] **Step 1: Declare reviewed ownership regions**

  Encode disjoint source bands and center splits for the hero illustration, idle/taunt/walk/run, attacks, command/curse/minions, hit/damage, defeat/recovery, props, dust, shockwaves, skull motifs, baseball trails, stars, mines, coins, chains, bat, and detached hat effects.

- [ ] **Step 2: Enforce exact source coverage**

  Assign only pixels with alpha 255; fail on multiply owned, unowned, or empty regions. Preserve each source RGBA tuple verbatim in a padded output frame.

- [ ] **Step 3: Emit pre-assembly evidence before frame files**

  Write the immutable generation specification, source audit, and pre-assembly batch manifest before saving frames or the atlas.

- [ ] **Step 4: Assemble review artifacts**

  Pack explicit variable cells with eight transparent gutter pixels on every side, label every boundary, and render pivot-aligned EMERGE/RETREAT/DEFEAT GIFs from approved frames only.

- [ ] **Step 5: Run the builder**

  Run: `python3 tools/asset_pipeline/build_boss_diamond_don_isolated.py`

  Expected: source hashes match, zero generated/replaced pixels, and exact one-to-one visible-pixel coverage is reported.

### Task 2: Independent verification

**Files:**
- Create: `tools/verify/check_boss_diamond_don_isolated.py`
- Update during verification: `assets/generated/boss-diamond-don-isolated/validation-report.md`

**Interfaces:**
- Consumes: all Task 1 artifacts and source PNGs.
- Produces: a nonzero exit on any contract defect and a seven-test PASS report only when every deterministic assertion succeeds.

- [ ] **Step 1: Verify provenance and immutable operations**

  Assert source hashes/dimensions/binary alpha, generated/replaced/redrawn/resized/filtered/rotated/promoted counts of zero, and generated-awaiting-approval status.

- [ ] **Step 2: Independently reconstruct every frame**

  Reapply each manifest ownership rectangle to the accepted source, compare exact RGBA bytes and hashes, and require all source-visible pixels to be owned once with no omission or duplication.

- [ ] **Step 3: Verify rectangles, pivots, gutters, and previews**

  Assert frame-visible bounds stay inside transparent padding, every atlas gutter is empty, atlas crops match frame bytes, pivots are in bounds, and preview counts/endpoints match required sequences.

- [ ] **Step 4: Verify generated-only scope**

  Reject any Diamond Don file under `assets/runtime/` and write explicit V2 status `INCOMPLETE / NOT PROMOTED` without weakening Bossfix tests A-G.

- [ ] **Step 5: Run independent verification**

  Run: `python3 tools/verify/check_boss_diamond_don_isolated.py`

  Expected: `VALIDATION: PASSED`, Bossfix A-G PASS, and V2 gate `INCOMPLETE / NOT PROMOTED`.

### Task 3: Visual evidence and final audit

**Files:**
- Inspect: `assets/generated/boss-diamond-don-isolated/contact-sheet.png`
- Inspect: `assets/generated/boss-diamond-don-isolated/previews/emerge.gif`
- Inspect: `assets/generated/boss-diamond-don-isolated/previews/retreat.gif`
- Inspect: `assets/generated/boss-diamond-don-isolated/previews/defeat.gif`

**Interfaces:**
- Consumes: final Task 1 artifacts after Task 2 passes.
- Produces: evidence-backed delivery with no completion or runtime-readiness claim.

- [ ] **Step 1: Inspect the boundary-labeled contact sheet**

  Check normal size and magnified crops for clipped tails, bat, baseballs, rubble, shockwaves, curse smoke, skull motifs, coins, chain, stars, dust, minions, mines, hat, detached props, neighboring bleed, and visible boundary contact.

- [ ] **Step 2: Inspect all three pivot-aligned previews**

  Confirm EMERGE resolves curse materialization into active idle, RETREAT reverses that vocabulary without defeat, and DEFEAT ends on the approved identifiable softened seated Diamond Don with hat, clothing, tail, accessories, and nearby bat/baseball material intact.

- [ ] **Step 3: Re-run verification after final inspection**

  Run: `python3 tools/verify/check_boss_diamond_don_isolated.py`

  Expected: unchanged `VALIDATION: PASSED` and exact coverage counts.

- [ ] **Step 4: Deliver review status**

  Report `VALIDATION: PASSED` followed by `GENERATED - AWAITING USER APPROVAL`, explicitly noting that runtime promotion and the full V2 runtime release gate were not authorized.
