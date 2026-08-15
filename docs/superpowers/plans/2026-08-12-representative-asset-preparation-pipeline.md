# Representative Asset-Preparation Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and prove a deterministic, manifest-first candidate generator for `trashy-regular`, `opossum-pilfer`, `mosquito`, `moth-dustwing`, `boss-trash-dash`, `taco`, and `kite`, stopping under `assets/generated/` for project-owner visual review.

**Architecture:** A dependency-light Python package validates canonical provenance and authored variable-frame manifests, copies exact source pixels through a pinned Pillow encoder, measures alpha/geometry independently, builds deterministic atlases and contact sheets twice in isolated staging directories, and atomically replaces only the selected generated candidate. A separate verifier decodes the finished outputs and recomputes hashes and measurements without trusting the generator report. Runtime promotion and Godot integration are separate future work.

**Tech Stack:** Python 3.11.3, Pillow 12.3.0, Python `unittest`, JSON, POSIX shell, Git LFS, existing Bash policy checks. Godot is not launched anywhere in this plan.

## Global Constraints

- Follow `AGENTS.md`, `.skills/rendering-asset-integrity`, `.skills/animation`, `.skills/visual-qa`, and `.skills/v2_release_gate` throughout execution.
- Approved source pixels and canonical source hashes are immutable; do not redraw, resize, recolor, synthesize, or derive replacements from concept sheets.
- Reject `archive/`, superseded files, sibling V1 paths, unsafe paths, and unapproved sources.
- Frame rectangles, order, pivots, timing, states, effects, and acknowledgements are authored decisions; automation may validate but may not guess them.
- Generated candidates live only at `assets/generated/<asset-id>/`. Nothing in this plan writes to or references `assets/runtime/`.
- Generate twice in clean staging directories and require byte-identical file sets before atomic candidate replacement.
- Preserve source RGB for every retained source pixel unless a manifest-authorized, source-specific Taco/Kite chroma operation applies.
- Never globally delete green pixels from the Taco/Kite sheet; legitimate green artwork and partial-alpha glow must survive.
- Use integer crop and packing coordinates, nearest-neighbor scaling only for enlarged review sheets, and one uniform runtime scale per gameplay form.
- Generated evidence supports review but cannot produce a V2 release-gate `PASS`; final phase status is `INCOMPLETE` until runtime promotion and gameplay validation occur.
- Do not launch Godot during this plan. If scope later changes to require Godot, first use the repository safety helpers and an explicit writable `.codex/godot-logs/<purpose>.log` as required by `AGENTS.md`.
- Preserve unrelated user changes. Stage and commit only the paths named by each task.

---

## File and interface map

| Path | Responsibility |
| --- | --- |
| `tools/asset-pipeline/requirements.lock` | Pin Pillow encoder/runtime provenance. |
| `tools/asset-pipeline/asset_pipeline/contract.py` | Parse and validate schema, semantics, paths, and canonical provenance. |
| `tools/asset-pipeline/asset_pipeline/image_ops.py` | Exact-pixel extraction, alpha/RGB measurement, pivot packing, and contact sheets. |
| `tools/asset-pipeline/asset_pipeline/build.py` | Build one candidate into a supplied staging directory. |
| `tools/asset-pipeline/asset_pipeline/verify.py` | Independently decode and verify an existing candidate. |
| `tools/asset-pipeline/asset_pipeline/transaction.py` | Double-build comparison and atomic destination replacement. |
| `tools/asset-pipeline/asset_pipeline/cli.py` | Stable `validate`, `build`, and `verify` command surface. |
| `tools/asset-pipeline/run_asset_pipeline.sh` | Resolve the repository-local Python environment and invoke the CLI fail-closed. |
| `tools/asset-pipeline/schema/asset-preparation-v1.schema.json` | Machine-readable manifest structure and closed-field vocabulary. |
| `tools/asset-pipeline/manifests/*.json` | Seven reviewed preparation manifests. |
| `tools/asset-pipeline/tests/` | Python unit, mutation, transaction, determinism, and CLI tests. |
| `assets/generated/<asset-id>/` | Candidate frames, atlas, measurements, contact sheets, and build report. |
| `tools/verify/check_asset_pipeline.sh` | Clean rebuild and independent verification for all seven representatives. |
| `tools/verify/check_policy.sh` | Repository allowlists and prohibition of runtime promotion/references. |
| `docs/architecture/ASSET_PIPELINE.md` | Operator commands, output meanings, review/promotion boundary. |
| `tools/visual-audit/evidence/asset-pipeline/` | Review record containing exact hashes, inspection status, and limitations. |

Core Python interfaces used across tasks:

```python
@dataclass(frozen=True)
class ValidatedManifest:
    asset_id: str
    source_path: Path
    source_sha256: str
    source_width: int
    source_height: int
    source_mode: str
    payload: dict[str, object]

def load_and_validate_manifest(
    repo_root: Path,
    manifest_path: Path,
    provenance_catalog: Mapping[str, CanonicalSource] | None = None,
) -> ValidatedManifest: ...
def build_candidate(repo_root: Path, manifest: ValidatedManifest, output_dir: Path) -> dict[str, object]: ...
def verify_candidate(repo_root: Path, manifest: ValidatedManifest, candidate_dir: Path) -> dict[str, object]: ...
def rebuild_and_publish(repo_root: Path, manifest_path: Path, generated_root: Path) -> Path: ...
```

All public failures raise `AssetPipelineError` with a stable code and message and cause CLI exit status `1`; argument/usage failures exit `64`; missing pinned dependencies exit `69`. No traceback is printed for an expected validation failure.

---

### Task 1: Establish the closed manifest and provenance contract

**Files:**
- Create: `tools/asset-pipeline/requirements.lock`
- Create: `tools/asset-pipeline/asset_pipeline/__init__.py`
- Create: `tools/asset-pipeline/asset_pipeline/errors.py`
- Create: `tools/asset-pipeline/asset_pipeline/contract.py`
- Create: `tools/asset-pipeline/schema/asset-preparation-v1.schema.json`
- Create: `tools/asset-pipeline/tests/__init__.py`
- Create: `tools/asset-pipeline/tests/fixtures/valid-minimal.json`
- Create: `tools/asset-pipeline/tests/test_contract.py`

**Interfaces:**
- Consumes: canonical character inventory and power-up manifest already under `docs/design/trash-dash/`.
- Produces: `AssetPipelineError(code: str, message: str)`, `CanonicalSource`, and `load_and_validate_manifest(repo_root, manifest_path, provenance_catalog=None) -> ValidatedManifest`. Production calls build the catalog from canonical repository manifests; tests may inject a temporary catalog without weakening path validation.

- [ ] **Step 1: Pin the image dependency and write the failing contract tests**

Set `requirements.lock` to exactly:

```text
Pillow==12.3.0
```

Write table-driven `unittest` cases proving that the loader rejects unknown root/frame fields; schema versions other than `1`; absolute, `..`, archive, superseded, sibling-V1, and symlink-escape paths; IDs outside the locked seven; canonical hash/dimension/path mismatches; bool-as-int coordinates; duplicate frame IDs; missing state membership; invalid status vocabulary; missing pivot/timing/geometry fields; unowned detached effects; and approvals on unhashed outputs. Include one minimal accepted manifest whose source is a generated temporary RGBA fixture and whose provenance adapter is injected for isolation.

- [ ] **Step 2: Run the focused tests and record RED**

Run:

```bash
PYTHONPATH=tools/asset-pipeline python3 -m unittest discover -s tools/asset-pipeline/tests -p 'test_contract.py' -v
```

Expected: FAIL because `asset_pipeline.contract` and the v1 schema do not exist. Record the exact command and failure in the task report before implementation.

- [ ] **Step 3: Implement the schema and semantic validator**

Define a closed JSON schema with these required root keys: `schema_version`, `asset_id`, `asset_class`, `source`, `render`, `animations`, `detached_assets`, `acknowledgements`, `outputs`, and `review`. Require `additionalProperties: false` at every defined object level. Represent rectangles as `{x,y,w,h}`, vectors as `{x,y}`, and geometry as `{id,kind,rect,active_frames}`.

In `contract.py`, validate JSON token types independently of Python truthiness, canonicalize paths with `Path.resolve(strict=True)`, require containment beneath the repository, and compare the five character assets against `CANONICAL_IMPORT_INVENTORY.json`. Compare Taco/Kite against the power-up manifest's exact file, dimensions, row split, x cuts, and package status. Require the locked ID set:

```python
REPRESENTATIVE_IDS = frozenset({
    "trashy-regular", "opossum-pilfer", "mosquito", "moth-dustwing",
    "boss-trash-dash", "taco", "kite",
})
```

Do not add implicit frame ordering, inferred defaults, or fallback source paths.

- [ ] **Step 4: Run contract tests and verify GREEN**

Run the focused command from Step 2. Expected: all contract cases pass and expected validation failures print no traceback.

- [ ] **Step 5: Commit the contract boundary**

```bash
git add tools/asset-pipeline/requirements.lock tools/asset-pipeline/asset_pipeline tools/asset-pipeline/schema tools/asset-pipeline/tests
git commit -m "feat: define asset preparation contracts"
```

---

### Task 2: Implement exact-pixel extraction and independent measurements

**Files:**
- Create: `tools/asset-pipeline/asset_pipeline/image_ops.py`
- Create: `tools/asset-pipeline/tests/test_image_ops.py`
- Create: `tools/asset-pipeline/tests/fixtures/make_fixtures.py`

**Interfaces:**
- Consumes: a `ValidatedManifest` and Pillow `Image.Image` source.
- Produces: `extract_frame`, `measure_rgba`, `pack_frames`, and `render_contact_sheet` pure functions.

- [ ] **Step 1: Generate deterministic test fixtures and write failing pixel tests**

Create fixtures programmatically in tests: hard-alpha body pixels, partial-alpha glow, transparent padding, legitimate green body pixels, removable chroma background, a detached particle, a boundary-touching silhouette, and two frames with different canvas sizes but the same grounded pivot. Tests must compare row-major raw RGBA bytes, visible bounds, nonzero/partial-alpha counts, raw-alpha SHA-256, retained-source-RGB SHA-256, and pivot-relative bounds.

- [ ] **Step 2: Run image tests and record RED**

```bash
PYTHONPATH=tools/asset-pipeline python3 -m unittest discover -s tools/asset-pipeline/tests -p 'test_image_ops.py' -v
```

Expected: FAIL because image operations do not exist.

- [ ] **Step 3: Implement exact-pixel operations**

Implement integer-only crops with no resizing. `measure_rgba()` must return texture size, visible bounds, opaque/nonzero/partial counts, per-edge alpha contact counts, raw-alpha SHA-256, and retained RGB SHA-256. `pack_frames()` must use manifest order, stable pivot alignment, deterministic row layout, fixed transparent padding, and no rotation. `render_contact_sheet()` must provide 1× native and 4× `Resampling.NEAREST` outputs with frame/state labels placed outside sprite cells.

The general extractor must prove every output pixel maps to either the exact source RGBA pixel or transparent padding. It must reject an unacknowledged alpha-positive crop edge and reject any nonuniform transform.

- [ ] **Step 4: Prove exactness and GREEN**

Run the focused image tests twice. Add a mutation test that changes one partial-alpha byte while preserving dimensions, visible bounds, and alpha-class counts; require the raw-alpha hash check to catch it.

- [ ] **Step 5: Commit image operations**

```bash
git add tools/asset-pipeline/asset_pipeline/image_ops.py tools/asset-pipeline/tests/test_image_ops.py tools/asset-pipeline/tests/fixtures/make_fixtures.py
git commit -m "feat: add deterministic sprite extraction"
```

---

### Task 3: Add the builder, independent verifier, and atomic transaction

**Files:**
- Create: `tools/asset-pipeline/asset_pipeline/build.py`
- Create: `tools/asset-pipeline/asset_pipeline/verify.py`
- Create: `tools/asset-pipeline/asset_pipeline/transaction.py`
- Create: `tools/asset-pipeline/tests/test_build.py`
- Create: `tools/asset-pipeline/tests/test_verify.py`
- Create: `tools/asset-pipeline/tests/test_transaction.py`

**Interfaces:**
- Consumes: Task 1 manifests and Task 2 image operations.
- Produces: the `build_candidate`, `verify_candidate`, and `rebuild_and_publish` interfaces from the file map.

- [ ] **Step 1: Write RED tests for the complete candidate file contract**

Require a candidate to contain `frames/*.png`, `atlas.png`, `measurements.json`, `provenance.json`, `contact-sheet-native.png`, `contact-sheet-4x.png`, and `validation-report.json`. Require sorted JSON keys, UTF-8 plus trailing newline, relative paths only, fixed PNG encoder settings, Python/Pillow/zlib provenance, source and manifest hashes, and a SHA-256 entry for every emitted file except the self-referential report itself.

Write independent-verifier mutations for changed PNG pixels, dimensions, alpha, metadata, missing/extra files, forged hashes, unsafe paths, and an atlas cell pointing at the wrong frame.

- [ ] **Step 2: Write RED tests for two-build and rollback behavior**

Inject seams after first build, after second build, before destination rename, and after old-destination backup. Prove nondeterministic bytes reject publication; an existing candidate remains byte-identical on every failure; temp/backup paths are collision-safe and removed; a successful replacement leaves exactly one final candidate; and the transaction refuses any generated root outside `assets/generated/` or any destination named `runtime`.

- [ ] **Step 3: Run the focused suite and record RED**

```bash
PYTHONPATH=tools/asset-pipeline python3 -m unittest discover -s tools/asset-pipeline/tests -p 'test_build.py' -v
PYTHONPATH=tools/asset-pipeline python3 -m unittest discover -s tools/asset-pipeline/tests -p 'test_verify.py' -v
PYTHONPATH=tools/asset-pipeline python3 -m unittest discover -s tools/asset-pipeline/tests -p 'test_transaction.py' -v
```

Expected: FAIL on missing builder/verifier/transaction modules.

- [ ] **Step 4: Implement build and verification as separate trust paths**

The builder may reuse Task 2 functions. The verifier must reopen PNG bytes and recompute dimensions, raw RGBA/alpha/RGB hashes, visible bounds, pivot-relative geometry, file inventory, and atlas-to-frame equality without accepting measured values merely because the builder wrote them. Compare the two staged directory trees by relative file set and SHA-256.

Publish with same-parent rename semantics: build staging siblings beneath `assets/generated/`, verify both, rename the current destination to a unique backup if present, rename the verified stage into place, then remove only the exact backup. Roll back on any post-backup failure.

- [ ] **Step 5: Run focused tests twice and verify GREEN**

Expected: all build, mutation, determinism, and transaction tests pass twice with no files outside test temporary directories.

- [ ] **Step 6: Commit the reliable build core**

```bash
git add tools/asset-pipeline/asset_pipeline tools/asset-pipeline/tests
git commit -m "feat: build and verify asset candidates atomically"
```

---

### Task 4: Add the fail-closed command surface and repository policy

**Files:**
- Create: `tools/asset-pipeline/asset_pipeline/cli.py`
- Create: `tools/asset-pipeline/run_asset_pipeline.sh`
- Create: `tools/asset-pipeline/tests/test_cli.py`
- Create: `tools/verify/check_asset_pipeline.sh`
- Modify: `tools/verify/check_policy.sh`
- Modify: `tools/verify/test_shell_contracts.sh`
- Modify: `.gitignore`
- Modify: `.gitattributes`

**Interfaces:**
- Consumes: Task 3 APIs.
- Produces: `validate MANIFEST`, `build MANIFEST`, `verify MANIFEST CANDIDATE`, and all-representative verification commands.

- [ ] **Step 1: Write failing CLI and shell-contract tests**

Test exact exit codes for bad usage (`64`), missing Python/Pillow or wrong Pillow version (`69`), validation/build/verification failure (`1`), and success (`0`). Test paths containing spaces. Test that missing `git`, `rg`, `jq`, `shasum`, or Python fail closed where required. Test that `check_asset_pipeline.sh` verifies but never promotes. Extend policy fixtures to reject tracked runtime files, generated temp/backup directories, source references from runtime code, and unallowlisted asset-pipeline scripts.

- [ ] **Step 2: Run CLI and shell tests and record RED**

```bash
PYTHONPATH=tools/asset-pipeline python3 -m unittest discover -s tools/asset-pipeline/tests -p 'test_cli.py' -v
bash tools/verify/test_shell_contracts.sh
```

Expected: new cases fail because the entry points and allowlists are absent.

- [ ] **Step 3: Implement command wrappers and policy updates**

Make the shell wrapper resolve its own repository root, set `PYTHONPATH` only to `tools/asset-pipeline`, require Python 3.11 and Pillow exactly 12.3.0, and use `exec python3 -m asset_pipeline.cli`. The CLI prints one stable success/failure summary and never a traceback for expected errors.

Ignore only generated transaction scratch names and Python caches, not `assets/generated/<asset-id>/`. Replace the blanket `tools/visual-audit/evidence/` ignore with `tools/visual-audit/evidence/*` plus an explicit negation for `tools/visual-audit/evidence/asset-pipeline/**`, so the reviewed pipeline record is committable while unrelated runtime evidence stays ignored. Add explicit LFS coverage for generated PNG candidates and contact sheets if the final fixture-sized trial shows they exceed normal Git suitability; otherwise document and test that generated PNGs are ordinary Git blobs. Do not blanket-LFS JSON.

- [ ] **Step 4: Run focused checks and verify GREEN**

Run the commands from Step 2 twice. Also run `bash -n` on every new shell file and `tools/verify/check_policy.sh`.

- [ ] **Step 5: Commit commands and guardrails**

```bash
git add .gitignore .gitattributes tools/asset-pipeline/asset_pipeline/cli.py tools/asset-pipeline/run_asset_pipeline.sh tools/asset-pipeline/tests/test_cli.py tools/verify/check_asset_pipeline.sh tools/verify/check_policy.sh tools/verify/test_shell_contracts.sh
git commit -m "feat: expose guarded asset pipeline commands"
```

---

### Task 5: Author and prove the five representative character manifests

**Files:**
- Create: `tools/asset-pipeline/manifests/trashy-regular.json`
- Create: `tools/asset-pipeline/manifests/opossum-pilfer.json`
- Create: `tools/asset-pipeline/manifests/mosquito.json`
- Create: `tools/asset-pipeline/manifests/moth-dustwing.json`
- Create: `tools/asset-pipeline/manifests/boss-trash-dash.json`
- Create: `tools/asset-pipeline/tests/test_representative_manifests.py`
- Create: `assets/generated/{trashy-regular,opossum-pilfer,mosquito,moth-dustwing,boss-trash-dash}/**`

**Interfaces:**
- Consumes: exact source identities from the canonical inventory and Tasks 1–4.
- Produces: five deterministic character candidate directories with status `candidate`.

- [ ] **Step 1: Inspect every approved atlas beside its branded reference at original detail**

For each asset, record source dimensions, visual groups, complete pose order, detached effects, visible bounds, grounded feet or flying body center, and all ambiguous regions. Use the canonical source paths and hashes:

| ID | Size | SHA-256 |
| --- | --- | --- |
| `trashy-regular` | 1024×1536 | `64d85e6b9b40b119e87cf7fa1725cd5be076104d1c6971c77b5810ff7ff6e9e6` |
| `opossum-pilfer` | 1536×1024 | `e97c21956ddf8d9ccea7d7f92930c088e6c7fc4df74ffba0822b33bd1f854310` |
| `mosquito` | 1536×1024 | `1ca3164b27faac424811be277c64a1534b9a1d9684805cd92dca5ad9c055392a` |
| `moth-dustwing` | 1536×1024 | `bb08951082e4d5d2df98b748bbf83bf85a8be04a7a7ac1f88356594df6222a98` |
| `boss-trash-dash` | 1536×1024 | `85f85f67a46c028dbf6a416cc90cf71c7be58dff95a73f9774439fee7d1ba96f` |

If frame order is ambiguous, a required effect cannot be isolated, or source/reference meaning conflicts, stop that asset and report it rather than guessing.

- [ ] **Step 2: Write the five manifests and failing golden expectations**

Author exact integer rectangles and ordered states from the visual audit. Use feet anchors for grounded actors and logical body-center anchors for flying actors. Give Moth Dustwing's detached dust/projectile effects independent IDs and timing. Give the boss explicit reveal, tell/action/recovery, vulnerability/phase, defeat, and exit groups only where corresponding art exists; do not invent missing states.

In `test_representative_manifests.py`, pin the reviewed rectangle list, frame order, pivots, raw-alpha hashes, visible bounds, nonzero/partial counts, and detached-asset ownership independently from generated reports.

- [ ] **Step 3: Run validation and record RED before generation**

```bash
for manifest in tools/asset-pipeline/manifests/{trashy-regular,opossum-pilfer,mosquito,moth-dustwing,boss-trash-dash}.json; do
  tools/asset-pipeline/run_asset_pipeline.sh validate "$manifest"
done
PYTHONPATH=tools/asset-pipeline python3 -m unittest discover -s tools/asset-pipeline/tests -p 'test_representative_manifests.py' -v
```

Expected: manifest validation passes, while golden candidate tests fail because generated outputs do not exist.

- [ ] **Step 4: Build all five candidates**

Run `build` once per manifest. Each command internally performs two clean builds, independent verification, and atomic publication. Do not batch over a failed asset; inspect its validation report and source evidence before deciding whether a manifest correction is justified.

- [ ] **Step 5: Run golden and independent verification GREEN**

Run the focused unit test, then `verify` for each candidate. Run a second full build and require Git status to remain byte-clean, proving deterministic regeneration.

- [ ] **Step 6: Inspect contact sheets without approving runtime promotion**

Open all ten character contact sheets at original detail. Compare against branded sources and inspect complete silhouettes, frame order, alpha/halos, detached effects, pivot registration, scale consistency, and crop boundaries. Record defects as `candidate` findings; keep review status `candidate` even if static inspection is clean.

- [ ] **Step 7: Commit character candidates**

```bash
git add tools/asset-pipeline/manifests tools/asset-pipeline/tests/test_representative_manifests.py assets/generated/trashy-regular assets/generated/opossum-pilfer assets/generated/mosquito assets/generated/moth-dustwing assets/generated/boss-trash-dash
git commit -m "assets: prepare representative character candidates"
```

---

### Task 6: Add source-specific Taco/Kite chroma preparation

**Files:**
- Create: `tools/asset-pipeline/asset_pipeline/chroma.py`
- Create: `tools/asset-pipeline/manifests/taco.json`
- Create: `tools/asset-pipeline/manifests/kite.json`
- Create: `tools/asset-pipeline/tests/test_chroma.py`
- Modify: `tools/asset-pipeline/tests/test_representative_manifests.py`
- Create: `assets/generated/{taco,kite}/**`

**Interfaces:**
- Consumes: the approved 2172×724 RGB Taco/Kite sheet, exact row split, and 12 x-cuts per row from the power-up manifest.
- Produces: a manifest-authorized chroma-to-alpha transform with independently pinned retained-color and alpha evidence.

- [ ] **Step 1: Write RED chroma safety tests**

Fixtures must distinguish connected exterior chroma, legitimate enclosed green body pixels, green antialiasing near body art, glow/particles, and unrelated colored pixels. Tests require background removal to start only from image/crop edges, retain manifest-seeded protected components, preserve all non-background RGB exactly, create partial alpha only under the declared matte rule, and reject a global green deletion implementation.

- [ ] **Step 2: Run chroma tests and record RED**

```bash
PYTHONPATH=tools/asset-pipeline python3 -m unittest discover -s tools/asset-pipeline/tests -p 'test_chroma.py' -v
```

Expected: FAIL because `asset_pipeline.chroma` does not exist.

- [ ] **Step 3: Implement the reviewed chroma transform**

Use the manifest's exact per-frame x cuts and row bounds. Classify only edge-connected background candidates within a declared color-distance threshold, protect reviewed legitimate-green seeds/components, calculate a deterministic one-pixel or manifest-declared matte transition, and retain original RGB values for every alpha-positive output pixel. Record threshold, connectivity, protected regions, removed count, partial count, and raw-alpha hash in measured metadata.

- [ ] **Step 4: Author Taco and Kite manifests**

Use source `docs/design/trash-dash/powerups/trash-dash-hd-powerups-v1/assets/powerups/taco-kite-powerups-clean-chroma.png`, dimensions 2172×724, Taco row `y=0..362`, Kite row `y=362..724`, and the exact x cuts and state labels from the approved package manifest. Explicitly author pivots for item/hover states, effect envelopes, timing, and reviewed protected-green regions. Do not process the separate pickup overlay sheets in this representative phase.

- [ ] **Step 5: Build, independently verify, and prove deterministic outputs**

Run focused tests, build each candidate, verify each candidate, rebuild again, and require byte-clean Git status. Pin raw alpha and retained-RGB hashes independently in `test_representative_manifests.py` so a chroma mutation that preserves counts/bounds still fails.

- [ ] **Step 6: Inspect four power-up contact sheets at original detail**

Compare Taco and Kite at native and 4× scale to the approved branded reference. Check legitimate green retention, glow falloff, rings, sparkles, wind trails, clean background removal, complete silhouettes, and stable item pivots. Keep both statuses `candidate` pending the combined owner gate.

- [ ] **Step 7: Commit power-up candidates**

```bash
git add tools/asset-pipeline/asset_pipeline/chroma.py tools/asset-pipeline/manifests/taco.json tools/asset-pipeline/manifests/kite.json tools/asset-pipeline/tests assets/generated/taco assets/generated/kite
git commit -m "assets: prepare taco and kite candidates"
```

---

### Task 7: Integrate the full verification and document operation

**Files:**
- Modify: `tools/verify/check_asset_pipeline.sh`
- Modify: `tools/verify/check_policy.sh`
- Modify: `tools/verify/test_shell_contracts.sh`
- Create: `docs/architecture/ASSET_PIPELINE.md`
- Create: `tools/visual-audit/evidence/asset-pipeline/2026-08-12-representative-candidates.md`

**Interfaces:**
- Consumes: all seven manifests and candidate directories.
- Produces: one clean-checkout verification command and an evidence-backed `INCOMPLETE` review record.

- [ ] **Step 1: Write failing integration assertions**

Require `check_asset_pipeline.sh` to enumerate exactly seven IDs, validate each manifest, rebuild each candidate in isolated staging, compare it with the committed candidate, independently verify every output, ensure no manifest has status `approved`, and prove `assets/runtime/` contains only its existing `.gitkeep`. Add shell tests for missing candidates, extra IDs, modified hashes, missing tools, nonzero child exits, and forbidden runtime files/references.

- [ ] **Step 2: Run the integration checks and record RED**

```bash
tools/verify/check_asset_pipeline.sh
bash tools/verify/test_shell_contracts.sh
```

Expected: the new aggregate/negative cases fail until the final enumerator and policy rules are complete.

- [ ] **Step 3: Complete the aggregate verifier and operator documentation**

Document environment setup, exact commands, candidate directory layout, deterministic rebuild behavior, failure recovery, manifest-authoring rules, visual-review procedure, approval vocabulary, and the explicit separation between generation, future runtime promotion, and Godot integration. State that this plan invokes no Godot process.

- [ ] **Step 4: Record the candidate visual audit**

List exact source, manifest, atlas, and contact-sheet hashes for all seven assets; record every native/4× image inspected; summarize frame/state coverage; record acknowledgements and defects; mark automated provenance/derivation checks individually; and set the overall V2 gate to `INCOMPLETE` because no runtime promotion, animation registration, uninterrupted gameplay traversal, or target-resolution runtime evidence exists.

- [ ] **Step 5: Run the complete non-Godot verification twice**

```bash
PYTHONPATH=tools/asset-pipeline python3 -m unittest discover -s tools/asset-pipeline/tests -p 'test_*.py' -v
tools/verify/check_asset_pipeline.sh
tools/verify/check_character_animation_import.sh
tools/verify/check_powerup_source_import.sh
bash tools/verify/test_shell_contracts.sh
tools/verify/check_policy.sh
git lfs fsck
git diff --check
```

Run the entire sequence twice. Expected: every command exits `0`; the second asset rebuild leaves no tracked diff; `assets/runtime/` remains unchanged; no Godot process is launched.

- [ ] **Step 6: Commit verification and documentation**

```bash
git add tools/verify/check_asset_pipeline.sh tools/verify/check_policy.sh tools/verify/test_shell_contracts.sh docs/architecture/ASSET_PIPELINE.md tools/visual-audit/evidence/asset-pipeline/2026-08-12-representative-candidates.md
git commit -m "docs: record representative asset candidate gate"
```

---

### Task 8: Project-owner contact-sheet review checkpoint

**Files:**
- Modify only after feedback: `tools/visual-audit/evidence/asset-pipeline/2026-08-12-representative-candidates.md`
- Modify only when a finding requires correction: the affected `tools/asset-pipeline/manifests/<asset-id>.json` and regenerated `assets/generated/<asset-id>/`

**Interfaces:**
- Consumes: fourteen contact sheets and the Task 7 audit.
- Produces: explicit per-asset `accepted candidate` or `rejected candidate` decisions; never runtime promotion.

- [ ] **Step 1: Present all seven native/4× comparisons to the project owner**

Group the review as player, grounded enemy, flying enemy, effect-heavy enemy, boss, and two power-ups. For each asset, show the source identity, ordered contact sheet, pivot/baseline guide, acknowledgements, and exact candidate hash.

- [ ] **Step 2: Record explicit decisions**

Do not interpret silence or general project approval as asset approval. Record `accepted candidate` only when the owner explicitly accepts that asset's static preparation. Record `rejected candidate` with the exact visual issue otherwise. The manifest remains `candidate`; schema-level `approved` is reserved for the later promotion workflow that records approval identity, time, and immutable hashes.

- [ ] **Step 3: Correct rejected manifests through a fresh RED/GREEN cycle**

For each rejected asset, add a golden test reproducing the defect, adjust only reviewed manifest metadata or source-specific processing, rebuild twice, independently verify, and show replacement contact sheets. Never edit source art to hide a pipeline defect.

- [ ] **Step 4: Re-run the complete Task 7 verification and commit the review record**

Expected: all automation passes; accepted/rejected decisions and limitations are durable; `assets/runtime/` is still unchanged; final status remains `INCOMPLETE` pending a separately designed promotion and gameplay-integration phase.

```bash
git add tools/visual-audit/evidence/asset-pipeline/2026-08-12-representative-candidates.md
git commit -m "docs: record representative candidate review"
```

---

## Final handoff

Report the exact commit range, Python/Pillow versions, seven source and candidate hashes, deterministic rebuild results, test counts, policy/LFS results, contact sheets inspected, owner decisions, acknowledged exceptions, and every unresolved condition. Use `INCOMPLETE`, not `PASS` or `production-ready`, because runtime promotion and gameplay verification are intentionally deferred.
