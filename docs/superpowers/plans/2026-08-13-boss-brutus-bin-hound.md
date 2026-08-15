# Brutus Bin Hound Isolation Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the complete approved Brutus Bin Hound source atlas into independently extractable, pixel-exact frames with explicit animation/effect ownership and validation evidence, without runtime promotion.

**Architecture:** Treat the approved canonical board and accepted transparent Phase 04 atlas as immutable inputs. A deterministic Pillow builder extracts manifest-declared source rectangles, preserves every visible RGBA pixel at scale 1, repacks variable-size cells with transparent gutters, writes individual frames and a boundary contact sheet, and a separate verifier rechecks provenance, state coverage, pixel hashes, gutters, overlap, anchors, and all seven bossfix gates.

**Tech Stack:** Python 3, Pillow, JSON, PNG RGBA, SHA-256.

## Global Constraints

- Follow `/Users/jamesschmittler/Desktop/bossfix.md` and the Level 2 boss canon in full.
- Preserve approved artwork exactly; no redraw, generation, resampling, retouching, filtering, rotation, crop of visible pixels, or reinterpretation.
- Use `PRESERVE EXACTLY - REPOSITION FOR ISOLATION` for approved frames requiring layout correction.
- Every declared extraction rectangle must have transparent gutters on all four sides and unambiguous effect ownership.
- Keep outputs under `assets/generated/`; do not promote to runtime assets.
- Final status remains `GENERATED - AWAITING USER APPROVAL`.

---

### Task 1: Audit and immutable specification

**Files:**
- Create: `assets/generated/boss-brutus-bin-hound-isolated/immutable-generation-specification.md`
- Create: `assets/generated/boss-brutus-bin-hound-isolated/source-audit.json`

**Interfaces:**
- Consumes: approved canonical board and accepted transparent Phase 04 atlas.
- Produces: a locked inventory of states, source rectangles, ownership, anchors, and sequence classifications consumed by the builder.

- [ ] **Step 1: Measure both source images**

Record dimensions, modes, SHA-256 values, alpha distribution, visible bounds, and component/boundary evidence.

- [ ] **Step 2: Inventory every logical frame and effect**

Assign each visible envelope to one state/frame, preserve source order, and classify EMERGE, RETREAT, and DEFEAT as complete, incomplete, or missing.

- [ ] **Step 3: Freeze the execution specification**

Write identity, animation, rendering, restriction, gutter, anchor, and ownership requirements before producing final assets.

### Task 2: Deterministic atlas builder

**Files:**
- Create: `tools/asset_pipeline/build_boss_brutus_bin_hound_isolated.py`
- Create: `assets/generated/boss-brutus-bin-hound-isolated/manifest.json`
- Create: `assets/generated/boss-brutus-bin-hound-isolated/frames/*.png`
- Create: `assets/generated/boss-brutus-bin-hound-isolated/boss-brutus-bin-hound-isolated.png`
- Create: `assets/generated/boss-brutus-bin-hound-isolated/contact-sheet.png`

**Interfaces:**
- Consumes: immutable source inventory from Task 1.
- Produces: `build()` outputs and a manifest with state order, source/cell/art rectangles, pivots, visible bounds, ownership, hashes, and rebuild command.

- [ ] **Step 1: Implement exact extraction**

Crop declared rectangles without resampling, retain the complete source rectangle in each individual frame, and verify visible pixels match their source coordinates.

- [ ] **Step 2: Implement variable-cell packing**

Pack frames in state/frame order with at least 8 transparent pixels on every side and no overlapping cell rectangles.

- [ ] **Step 3: Generate the contact sheet**

Composite the atlas over a neutral checkerboard and draw/labell every declared cell boundary without modifying the delivered transparent atlas.

- [ ] **Step 4: Write the manifest**

Record all required contract fields and mark every approved frame `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`; set generation and replacement counts to zero unless the frozen audit proves otherwise.

### Task 3: Independent verification and report

**Files:**
- Create: `tools/verify/check_boss_brutus_bin_hound_isolated.py`
- Create: `assets/generated/boss-brutus-bin-hound-isolated/validation-report.md`

**Interfaces:**
- Consumes: Task 2 manifest, atlas, individual frames, and immutable sources.
- Produces: exit-zero verification evidence and an explicit Test A–G report.

- [ ] **Step 1: Verify provenance and exact pixels**

Check source hashes, frame RGBA hashes, source-to-frame equality, scale 1, and zero generative/replacement operations.

- [ ] **Step 2: Verify geometry and isolation**

Check visible bounds, transparent outer boundaries, minimum gutters, atlas round-trip pixels, non-overlapping rectangles, and unambiguous detached-effect ownership.

- [ ] **Step 3: Verify sequence coverage**

Check immutable frame counts and ordered membership for EMERGE, RETREAT, and DEFEAT plus all preserved states/effects.

- [ ] **Step 4: Run the full verifier**

Run: `python3 tools/verify/check_boss_brutus_bin_hound_isolated.py`

Expected: exit 0 and explicit PASS output for bossfix Tests A–G.

- [ ] **Step 5: Inspect the final atlas and contact sheet**

Open both final images at original resolution and confirm that frame boundaries, gutters, labels, alpha, and source-scale artwork match the manifest.

- [ ] **Step 6: Record release-gate scope**

State that runtime promotion/traversal is intentionally not performed because this execution stops at generated-source approval; do not claim runtime readiness.
