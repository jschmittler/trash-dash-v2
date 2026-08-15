# Project O.P.O.S.S.U.M. Bossfix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the accepted Project O.P.O.S.S.U.M. transparent source atlas into a complete lossless, manifest-defined isolated sheet with individual frames, composed EMERGE/RETREAT/DEFEAT previews, and reproducible seven-test validation evidence, without runtime promotion.

**Architecture:** A deterministic Pillow builder will assign each nontransparent source pixel to exactly one reviewed logical frame or support sprite, crop each ownership mask with transparent extraction padding, pack the unchanged pixels into disjoint variable rectangles with eight-pixel atlas gutters, and emit manifests plus review artifacts. A separate verifier will reconstruct approved-source coverage, validate hashes, geometry, sequence metadata, and every bossfix gate, then write the validation report.

**Tech Stack:** Python 3, Pillow, JSON, PNG/GIF, SHA-256, repository-local asset pipeline and verification scripts.

## Global Constraints

- The project-local `docs/design/trash-dash/docs/game/bosses/BOSSFIX.md` must be reread in full immediately before the execution build; it was copied byte-identically from the restored Desktop contract.
- The approved visual board and accepted transparent atlas are immutable inputs; the repository atlas must be byte-identical to `/Users/jamesschmittler/Desktop/boss-project-opossum-transparent.png`.
- Existing visible RGBA pixels remain at 1:1 scale with no generation, redraw, resampling, filtering, rotation, retouching, or reinterpretation.
- Use `PRESERVE EXACTLY - REPOSITION FOR ISOLATION` for all approved physical frames and support sprites that require new extraction layout.
- Every visible source pixel must be assigned exactly once, with no omissions or duplication.
- Every extracted frame and packed rectangle must have fully transparent gutters on all four sides.
- EMERGE, RETREAT, and DEFEAT must be assembled only from approved poses, phase/effect states, de-armored states, and reveal/defeat art.
- Runtime timing remains explicitly unset where canon does not define it.
- Outputs remain under `assets/generated/`; do not promote or register runtime assets.
- Final status is `GENERATED - AWAITING USER APPROVAL` even when all seven asset-package tests pass.

---

### Task 1: Deterministic Project O.P.O.S.S.U.M. atlas builder

**Files:**
- Create: `tools/asset_pipeline/build_boss_project_opossum_isolated.py`
- Create: `assets/generated/boss-project-opossum-isolated/immutable-generation-specification.md` (generated)
- Create: `assets/generated/boss-project-opossum-isolated/batch-manifest.json` (generated before assembly)
- Create: `assets/generated/boss-project-opossum-isolated/source-audit.json` (generated)
- Create: `assets/generated/boss-project-opossum-isolated/manifest.json` (generated)
- Create: `assets/generated/boss-project-opossum-isolated/boss-project-opossum-isolated.png` (generated)
- Create: `assets/generated/boss-project-opossum-isolated/contact-sheet.png` (generated)
- Create: `assets/generated/boss-project-opossum-isolated/frames/*.png` (generated)
- Create: `assets/generated/boss-project-opossum-isolated/previews/{emerge,retreat,defeat}.gif` (generated)

**Interfaces:**
- Consumes: accepted 1536×1024 RGBA atlas, canonical 1448×1086 visual board, desktop duplicate, reviewed ownership zones, and the locked canon documents.
- Produces: `manifest.json` containing ordered states, required sequences, explicit source/cell/art rectangles, pivots, visible bounds, timing status, effect ownership, hashes, and one-to-one source-pixel coverage.

- [ ] **Step 1: Audit source alpha geometry and define reviewed logical ownership zones**

Run diagnostic scripts against the accepted atlas to enumerate connected-alpha components, row/column occupancy, merged neighbors, detached effects, and candidate state boundaries. Record every physical frame and support/effect sprite in approved reading order.

- [ ] **Step 2: Encode immutable source and sequence contracts**

Define fixed source sizes and hashes, lossless pixel-assignment rules, state metadata, actor/effect pivot rules, and approved-frame-only EMERGE/RETREAT/DEFEAT sequences. Set `GENERATE NEW = 0` and `REPLACE UNAPPROVED = 0` unless the completed source audit disproves frame coverage.

- [ ] **Step 3: Write batch inventory before frame assembly**

The builder must emit `immutable-generation-specification.md` and `batch-manifest.json` before writing frame PNGs or the updated sheet. Every source region uses `PRESERVE EXACTLY - REPOSITION FOR ISOLATION` and declares intended ownership.

- [ ] **Step 4: Extract and pack every approved pixel losslessly**

Assign each visible source pixel to exactly one frame mask, crop with transparent source padding, save individual RGBA frames, pack disjoint variable cells with eight-pixel transparent atlas gutters, and preserve source-coordinate registration metadata.

- [ ] **Step 5: Render review artifacts**

Create a boundary-labeled contact sheet and pivot-aligned EMERGE, RETREAT, and DEFEAT GIF previews using only manifest-referenced approved frames.

- [ ] **Step 6: Execute the builder**

Run: `python3 tools/asset_pipeline/build_boss_project_opossum_isolated.py`

Expected: successful creation of the complete generated package; console output reports exact one-to-one visible-pixel assignment and the packed atlas dimensions.

### Task 2: Independent seven-gate verifier

**Files:**
- Create: `tools/verify/check_boss_project_opossum_isolated.py`
- Create: `assets/generated/boss-project-opossum-isolated/validation-report.md` (generated)

**Interfaces:**
- Consumes: Task 1 manifests, accepted source/canon inputs, individual frames, updated atlas, contact sheet, and three previews.
- Produces: deterministic exit status, seven-test console evidence, and a validation report explicitly scoped to generated artwork rather than runtime readiness.

- [ ] **Step 1: Validate immutable provenance and delivery inventory**

Check required files, source/canon SHA-256 values, desktop byte identity, PNG modes/dimensions, state order, sequence classifications, preview existence, and operation counts.

- [ ] **Step 2: Prove exact visible-pixel preservation**

For every frame, map nontransparent pixels back through its declared source rectangle, compare exact RGBA bytes, reject duplicate ownership, and require total covered pixels to equal the accepted source visible-pixel count.

- [ ] **Step 3: Prove extraction and atlas isolation**

Require transparent margins around every frame-visible bound, verify eight transparent packed-gutter pixels on all sides, reject intersecting cell rectangles, and byte-compare every atlas art rectangle to its individual frame PNG.

- [ ] **Step 4: Verify sequence semantics and metadata**

Require unique, known, ordered approved frame references for EMERGE, RETREAT, and DEFEAT; verify pivots remain inside frames and relocated pivots preserve their local coordinates; require unambiguous effect ownership and explicitly unset runtime timing.

- [ ] **Step 5: Run complete verification**

Run: `python3 tools/verify/check_boss_project_opossum_isolated.py`

Expected: all seven bossfix tests print `PASS` for the reviewed 145-frame/support inventory, followed by `VALIDATION: PASSED` and `GENERATED - AWAITING USER APPROVAL`.

### Task 3: Visual inspection and handoff

**Files:**
- Inspect: `assets/generated/boss-project-opossum-isolated/contact-sheet.png`
- Inspect: `assets/generated/boss-project-opossum-isolated/previews/emerge.gif`
- Inspect: `assets/generated/boss-project-opossum-isolated/previews/retreat.gif`
- Inspect: `assets/generated/boss-project-opossum-isolated/previews/defeat.gif`
- Inspect: `assets/generated/boss-project-opossum-isolated/validation-report.md`

**Interfaces:**
- Consumes: final deterministic outputs after the last rebuild and verification run.
- Produces: user-facing generated-package handoff with no runtime-readiness claim.

- [ ] **Step 1: Inspect native-size and magnified frame boundaries**

Open the contact sheet at original resolution and inspect representative actor frames, wide gravity effects, cyan phase duplicates, debris/smoke support sprites, de-armored reveal states, and every cell boundary for bleed or contact.

- [ ] **Step 2: Inspect pivot-aligned required sequences**

Open all three previews and confirm canonical facing, stable scale, usable ground/pivot registration, unambiguous entrance/withdrawal/defeat meaning, and the approved recognizable final animal state.

- [ ] **Step 3: Record release-gate scope**

Confirm outputs exist only in `assets/generated/`. Record runtime traversal, target-resolution gameplay evidence, collision, encounter, and runtime animation registration as intentionally not applicable until explicit approval authorizes a later integration task.

- [ ] **Step 4: Deliver the approval-stage result**

Report the atlas/frame counts, exact visible-pixel coverage, reproducibility commands, seven-test result, inspection limits, and final status exactly as `GENERATED - AWAITING USER APPROVAL`.
