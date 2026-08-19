# Level 1 Parallax Assets Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a reviewable, parallax-ready three-plane candidate package for each of Level 1's five canonical environments without treating the result as gameplay/runtime integration.

**Architecture:** The canonical Level 1 environment-background PNGs remain immutable visual-direction sources. Fifteen independently authored plates—one opaque far plate plus magenta-keyed middle and close plates per stage—live under `assets/generated/level1-parallax/`; a deterministic Pillow processor produces 1320×540 candidate PNGs, static validation checks their integrity, and contact-sheet/seam evidence makes human review repeatable. No level scene, renderer, collision data, or runtime promotion record is created by this work.

**Tech Stack:** Built-in Codex image generation, Pillow/Python 3, JSON manifests, existing V2 asset validators, source PNG inspection.

## Global Constraints

- Use only the five approved canonical files in `docs/design/trash-dash/library/environments/backgrounds/level-01/`; do not modify them or import V1 runtime art.
- Follow `sprite-art`, `rendering-asset-integrity`, `environment-placement`, `overlap-prevention`, `visual-qa`, and `v2_release_gate`.
- Camera contract is 960×540; candidate plates are 1320×540 PNGs; parallax speed metadata is far `0.018`, middle `0.055`, close `0.13`.
- Far is fully opaque RGB. Middle and close use binary alpha after processing; their source masters use #FF00FF only as external key background.
- Each recognizable landmark belongs to exactly one plane. Do not add floor, platform, collision surface, playable route, player/enemy, text, UI, watermark, or border to any plate.
- Preserve aspect ratio with nearest-neighbor resizing only; no blur, antialiasing, stretching, per-plane opacity simulation, or source-art overwrite.
- Outputs remain generated candidates. Overall Level 1 integration and V2 release status stay `INCOMPLETE` until a renderer, traversal, and target-resolution runtime evidence exist.

---

### Task 1: Lock the Level 1 plate contract and deterministic processor

**Files:**
- Create: `assets/generated/level1-parallax/README.md`
- Create: `assets/generated/level1-parallax/prompts/plate-prompts.md`
- Create: `tools/asset_pipeline/process_level1_parallax.py`
- Create: `tools/verify/check_level1_parallax.py`
- Create: `tests/asset_pipeline/test_level1_parallax.py`

**Interfaces:**
- Consumes: five canonical background paths, named stage IDs, and source masters at `assets/generated/level1-parallax/sources/level1-<stage>-<layer>-source.png`.
- Produces: normalized candidates at `assets/generated/level1-parallax/processed/level1-<stage>-<layer>.png`, static report `assets/generated/level1-parallax/validation-report.json`, and review evidence under `assets/generated/level1-parallax/qa/`.

- [ ] **Step 1: Add failing processor/validator tests**

Create test fixtures with a 5:2 input image containing an opaque far scene, a magenta-background moving plate with an enclosed violet detail, and an intentionally malformed plate. Assert `process_level1_parallax.py` exposes and uses these functions:

```python
def crop_far_to_runtime(image: Image.Image) -> Image.Image: ...
def fit_moving_plate(image: Image.Image) -> Image.Image: ...
def remove_boundary_connected_magenta(image: Image.Image) -> Image.Image: ...
```

Assert output is exactly `(1320, 540)`, nearest-neighbor, has no partial alpha, keeps an enclosed violet detail, removes only edge-connected magenta, keeps far alpha at 255, and makes moving-plate alpha contain both 0 and 255.

- [ ] **Step 2: Run the new focused test to verify RED**

Run:

```sh
python3 -m unittest tests.asset_pipeline.test_level1_parallax
```

Expected: FAIL because the processor module and the three functions do not yet exist.

- [ ] **Step 3: Implement the locked inventory and processor**

In `process_level1_parallax.py`, declare exactly this ordered inventory:

```python
STAGES = (
    "deep-woodland",
    "creek-and-ruined-mill",
    "forest-edge-highway",
    "industrial-city-fringe",
    "urban-park-transition",
)
LAYERS = ("far", "middle", "close")
TARGET = (1320, 540)
```

Make `crop_far_to_runtime` use a centered aspect-preserving crop followed by `Image.Resampling.NEAREST`. Make `fit_moving_plate` use a centered aspect-preserving fit on an opaque #FF00FF 1320×540 canvas. Make `remove_boundary_connected_magenta` flood only from the canvas boundary and write exact `(0, 0, 0, 0)` for removed pixels and exact alpha 255 otherwise. Write a JSON report with source path, source size, output size, and alpha counts per plate. Generate 960×540 composites, forced-wrap seam views, forward/reverse sweeps, and four five-frame scene-transition sheets.

- [ ] **Step 4: Implement the validator and provenance template**

Make `check_level1_parallax.py` reject a missing/extra candidate set, non-PNG file, non-1320×540 dimensions, partial alpha, transparent far pixel, opaque-only or transparent-only moving plate, and opaque hot-magenta (`red > 220`, `blue > 180`, `green < 80`). In `README.md`, list all canonical inputs, their catalog IDs and SHA-256 values, candidate status, output ownership, exact rebuild/check commands, and explicit nonclaims. In `plate-prompts.md`, reserve fifteen exact prompts with one source reference, plane ownership, forbidden geometry, and alpha/key requirements per plate.

- [ ] **Step 5: Run focused tests and static syntax checks**

Run:

```sh
python3 -m unittest tests.asset_pipeline.test_level1_parallax
python3 -m py_compile tools/asset_pipeline/process_level1_parallax.py tools/verify/check_level1_parallax.py
```

Expected: PASS.

- [ ] **Step 6: Commit the processor contract**

```sh
git add docs/superpowers/plans/2026-08-19-level1-parallax-assets.md \
  assets/generated/level1-parallax/README.md \
  assets/generated/level1-parallax/prompts/plate-prompts.md \
  tools/asset_pipeline/process_level1_parallax.py \
  tools/verify/check_level1_parallax.py \
  tests/asset_pipeline/test_level1_parallax.py
git commit -m "feat: add level 1 parallax pipeline contract"
```

### Task 2: Author and process the fifteen Level 1 plates

**Files:**
- Create: `assets/generated/level1-parallax/sources/level1-<stage>-<layer>-source.png` (15 files)
- Create: `assets/generated/level1-parallax/processed/level1-<stage>-<layer>.png` (15 files)
- Create: `assets/generated/level1-parallax/qa/composites/*.png` (5 files)
- Create: `assets/generated/level1-parallax/qa/seams/*.png` (15 files)
- Create: `assets/generated/level1-parallax/qa/sweeps/*.png` (5 files)
- Create: `assets/generated/level1-parallax/qa/transitions/*.png` (4 files)
- Create: `assets/generated/level1-parallax/validation-report.json`

**Interfaces:**
- Consumes: Task 1 processor and prompt record, canonical inputs, and the exact stage/layer inventory.
- Produces: all reviewable candidate assets and machine-readable measurements for Task 3.

- [ ] **Step 1: Verify canonical input provenance before generation**

Run:

```sh
python3 tools/verify/validate_design_library.py
python3 tools/verify/audit_canonical_assets.py
```

Expected: PASS. Record the five catalog SHA-256 values in the README before submitting any generation request.

- [ ] **Step 2: Generate far plates independently**

For each stage, issue one built-in image-generation request using its matching canonical background solely as a visual-direction reference. Far plates must be a side-view, polished late-16-bit woodland/urban-edge distant vista with quiet matching left/right edge material, no characters or gameplay structures, and no alpha/key background. Exact ownership:

```text
deep-woodland: forest silhouettes, fog, canopy
creek-and-ruined-mill: misty pines, distant light rays, mill silhouette only
forest-edge-highway: distant treeline, far highway line, first skyline glimpse
industrial-city-fringe: warehouse/rail-yard silhouette and hazy city glow
urban-park-transition: distant park trees, brick-building silhouette, moonlit transition
```

- [ ] **Step 3: Generate middle plates independently**

For every stage, generate on a solid #FF00FF backdrop. Use only the following separated middle-depth objects; leave at least 35% clear key background and no object touching a canvas edge:

```text
deep-woodland: trunks, shrubs, mist ribbons
creek-and-ruined-mill: waterwheel shell, ruined bridge fragments, tree roots
forest-edge-highway: guardrail runs, fence posts, culvert mouths
industrial-city-fringe: rail cars, warehouse façade fragments, shipping containers
urban-park-transition: mature trees, park fencing, distant brick façades
```

- [ ] **Step 4: Generate close plates independently**

For every stage, generate on a solid #FF00FF backdrop. Use only 4–7 disconnected edge-weighted non-playable dressing fragments, leave the center and bottom travel corridor clear, use no continuous floor/ledge/platform, and leave at least 60% clear key background:

```text
deep-woodland: broken signpost, crate, camp-junk fragments
creek-and-ruined-mill: mossy stump, concrete block, tire-pile fragments
forest-edge-highway: fallen log fragment, stone chunk, roadside litter
industrial-city-fringe: pallet edge, drain-channel fragment, container corner
urban-park-transition: hedge/bench fragment, trash bin, small fence corner
```

- [ ] **Step 5: Inspect each source master before accepting it**

Use native-size plus 400% visual inspection. Reject a source master if it contains characters, text, a watermark, a full-width ground/floor/route, key-color contamination inside retained art, a cropped silhouette, duplicated focal landmark across planes, or a landmark that belongs to a different plane. Preserve rejected attempts only with a `-rejected` suffix and state the rejection reason in `README.md`.

- [ ] **Step 6: Build and validate candidates**

Run:

```sh
python3 tools/asset_pipeline/process_level1_parallax.py
python3 tools/verify/check_level1_parallax.py
```

Expected: 15 named candidates; all far plates opaque; all moving plates binary alpha with meaningful transparent and opaque pixels; no hot-magenta output.

- [ ] **Step 7: Commit the candidate package**

```sh
git add assets/generated/level1-parallax
git commit -m "feat: generate level 1 parallax candidates"
```

### Task 3: Audit the package and record the bounded result

**Files:**
- Create: `tools/visual-audit/evidence/level1-parallax/README.md`
- Create: `tools/visual-audit/evidence/level1-parallax/level1-<stage>-review.png` (5 files)
- Modify: `assets/generated/level1-parallax/README.md`
- Modify: `docs/architecture/VISUAL_AUDIT_PROTOCOL.md`

**Interfaces:**
- Consumes: Task 2 candidate plates, QA composites/seams/sweeps/transitions, report, and static validator.
- Produces: explicit asset-stage visual evidence and an `INCOMPLETE` V2 gate statement.

- [ ] **Step 1: Add failing audit assertion for the complete inventory**

Extend `tests/asset_pipeline/test_level1_parallax.py` to open all fifteen processed images and assert: alpha/size contract, 960×540 composite for each stage, forced-wrap seam for each layer, forward/reverse sweep for every stage, transition sheet for each adjacent pair, and no missing named plate.

- [ ] **Step 2: Run the focused test to verify evidence requirements fail when a required artifact is removed**

Run:

```sh
python3 -m unittest tests.asset_pipeline.test_level1_parallax
```

Expected: FAIL after temporarily moving only the test fixture's required seam/evidence path; restore it immediately after proving the assertion.

- [ ] **Step 3: Assemble one review contact sheet per stage**

Create each `level1-<stage>-review.png` as a labeled 3×1 strip—far on black, middle and close on a neutral checkerboard—with a 960×540 composite below. Use only image labels in the audit artifact, never in game plates. Inspect at native resolution and 400% zoom for alpha fringes, clipped silhouettes, visible magenta, duplicate landmarks, parallax-plane ownership violations, seam discontinuities, empty sky bands, unreadable clutter, and distorted aspect ratio.

- [ ] **Step 4: Run the deterministic matrix and record results**

Run:

```sh
python3 tools/verify/validate_design_library.py
python3 tools/verify/audit_canonical_assets.py
python3 -m unittest tests.asset_pipeline.test_level1_parallax
python3 tools/verify/check_level1_parallax.py
git diff --check
```

Expected: all commands pass. Record command, revision, source hashes, generated output inventory, measurements, inspection observations, and rejected source masters in the evidence README.

- [ ] **Step 5: Apply the V2 release gate honestly**

Record `PASS` only for static asset integrity and manual asset-stage visual review. Record `INCOMPLETE` for renderer integration, uninterrupted Level 1 traversal, target-resolution gameplay captures, collision/placement verification, and overall V2 release because this plan creates assets only.

- [ ] **Step 6: Commit audited evidence**

```sh
git add assets/generated/level1-parallax \
  tools/visual-audit/evidence/level1-parallax \
  docs/architecture/VISUAL_AUDIT_PROTOCOL.md \
  tests/asset_pipeline/test_level1_parallax.py
git commit -m "docs: audit level 1 parallax candidates"
```

## Self-Review

- Spec coverage: the plan covers all five Level 1 canonical beats, exact three-plane ownership, source provenance, generated-vs-runtime separation, deterministic framing/alpha rules, static testing, seam/transition inspection, and the V2 release-gate nonclaim.
- Placeholder scan: no task delegates unspecified implementation; the processor functions, inventory, output folders, commands, prompt ownership, and acceptance/rejection conditions are named explicitly.
- Interface consistency: Tasks 2 and 3 consume exactly the Task 1 source naming convention, stage IDs, output dimensions, processor functions, validator, and QA directories.

## Execution Handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-19-level1-parallax-assets.md`.

1. **Subagent-Driven** — dispatch a fresh worker per task with review gates.
2. **Inline Execution** — execute it here, beginning with the provenance and processor contract.
