# Galactogobbler Isolation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Losslessly rebuild the accepted Galactogobbler atlas as independently extractable variable rectangles and compose approved-only EMERGE, RETREAT, and DEFEAT sequences.

**Architecture:** A deterministic Pillow builder partitions every visible source pixel into one reviewed ownership rectangle, crops each owned envelope at source scale, packs the frames with transparent gutters, writes manifests and pivot-aligned previews, and records preservation hashes. A separate verifier reconstructs the source-to-output mapping and enforces every Bossfix test that can be proven for this generated-only package.

**Tech Stack:** Python 3, Pillow, JSON, PNG RGBA, GIF previews.

## Global Constraints

- Accepted atlas SHA-256: `3a030409a4ee38c38ece7137f4a5f6484b629b12ec9dcc9760e8ecd18015f15a`.
- Canonical board SHA-256: `9c1896aa4b61bed52586e4b1df3dbeca002e3edb09da536ab17945332284ace4`.
- Preserve every approved RGBA visible pixel exactly once at 1:1 scale.
- Use `PRESERVE EXACTLY - REPOSITION FOR ISOLATION` for every physical output; generate and replace zero artwork frames.
- Every variable cell has at least 8 fully transparent gutter pixels on all sides.
- Runtime timing remains unset and nothing is promoted into `assets/runtime/`.

---

### Task 1: Deterministic atlas builder

**Files:**
- Create: `tools/asset_pipeline/build_boss_galactogobbler_isolated.py`
- Create at build time: `assets/generated/boss-galactogobbler-isolated/**`

**Interfaces:**
- Consumes: the accepted transparent atlas, canonical board, and reviewed rectangular ownership zones.
- Produces: `manifest.json`, `source-audit.json`, `batch-manifest.json`, immutable specification, isolated PNG frames, complete atlas, contact sheet, and three GIF previews.

- [ ] **Step 1: Encode immutable source hashes, state rows, ownership rectangles, pivots, and approved-only sequence order.**
- [ ] **Step 2: Assert every visible source pixel belongs to exactly one nonempty ownership zone.**
- [ ] **Step 3: Copy owned RGBA pixels without redraw, resize, rotation, filtering, or retouching.**
- [ ] **Step 4: Pack variable rectangles with transparent gutters and write all metadata/evidence artifacts.**
- [ ] **Step 5: Run `python3 tools/asset_pipeline/build_boss_galactogobbler_isolated.py`; expect exact one-to-one coverage and zero generated frames.**

### Task 2: Independent verification

**Files:**
- Create: `tools/verify/check_boss_galactogobbler_isolated.py`
- Verify: `assets/generated/boss-galactogobbler-isolated/**`

**Interfaces:**
- Consumes: accepted source atlas plus generated manifest and image artifacts.
- Produces: a nonzero exit on any source mismatch, omitted/duplicated pixel, boundary contact, gutter contamination, atlas mismatch, sequence defect, provenance violation, or runtime promotion.

- [ ] **Step 1: Verify immutable hashes, source dimensions, binary alpha, output inventory, and operation counts.**
- [ ] **Step 2: Reconstruct each ownership rectangle and compare every isolated frame RGBA value to the accepted source.**
- [ ] **Step 3: Prove exact source coverage, disjoint ownership, transparent boundaries/gutters, and atlas/frame identity.**
- [ ] **Step 4: Validate ordered EMERGE, RETREAT, and DEFEAT metadata and identifiable defeat ending.**
- [ ] **Step 5: Run `python3 tools/verify/check_boss_galactogobbler_isolated.py`; expect all seven Bossfix tests to pass.**

### Task 3: Visual QA and handoff

**Files:**
- Inspect: `assets/generated/boss-galactogobbler-isolated/contact-sheet.png`
- Inspect: `assets/generated/boss-galactogobbler-isolated/previews/{emerge,retreat,defeat}.gif`
- Update at build time: `assets/generated/boss-galactogobbler-isolated/validation-report.md`

**Interfaces:**
- Consumes: final build output after Task 2.
- Produces: boundary-labeled and pivot-aligned review evidence with explicit generated-only release status.

- [ ] **Step 1: Inspect the complete contact sheet at native and magnified scale for clipping, contamination, and ambiguous ownership.**
- [ ] **Step 2: Inspect all three pivot-aligned previews for meaning, continuity, stable scale, and final identity.**
- [ ] **Step 3: Re-run the builder and verifier to prove reproducibility.**
- [ ] **Step 4: Record Bossfix `VALIDATION: PASSED`, V2 runtime gate `INCOMPLETE / NOT PROMOTED`, and `GENERATED - AWAITING USER APPROVAL`.**

