# Character Animation Canonical Import Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Import and audit the Phase 05 canonical character-animation handoff while stopping before frame extraction or runtime integration.

**Architecture:** Preserve each original Phase 01–04 package root beneath a new namespaced design-source directory. Keep branded references and cleaned transparent atlases distinct, record every canonical ID in one machine-readable inventory, and validate provenance and file integrity with a repository shell check.

**Tech Stack:** Git LFS, Bash, SHA-256, JSON, PNG source assets, Godot 4.7.1 project conventions (no Godot process required for this import audit).

## Global Constraints

- Approved transparent atlases and branded source references are visual truth.
- Do not use equal-grid slicing or force frames into uniform cells.
- Do not alter, redraw, crop, rescale, or regenerate approved art.
- Preserve Phase 01 through 04 identities and original manifests.
- Never overwrite existing design sources or delete legacy assets.
- All imported PNGs must be tracked through Git LFS.
- Stop after all 36 canonical atlas IDs resolve; do not begin extraction or runtime integration.
- Any later Godot invocation must use a verified project-local `.codex/godot-logs/<purpose>.log` and the shared safety helpers.

---

### Task 1: Import the canonical phase packages

**Files:**
- Create: `docs/design/trash-dash/character-animation/phase-05-codex-integration/**`
- Modify: `.gitattributes`

**Interfaces:**
- Consumes: the verified Phase 05 delivery archive and its four checksum-pinned inner archives.
- Produces: immutable design-source phase directories whose original relative manifest paths still resolve.

- [x] **Step 1: Verify the four delivery archives**

```bash
LC_ALL=C LANG=C shasum -a 256 -c phase-05-codex-integration/qa/SHA256SUMS
```

Expected: four `OK` results.

- [x] **Step 2: Copy top-level handoff documents and extracted Phase 01–04 roots**

Copy only into `docs/design/trash-dash/character-animation/phase-05-codex-integration/`. Preserve every original filename, image byte, and manifest byte; normalize only repository-disallowed Markdown trailing whitespace. Do not copy over `docs/design/trash-dash/reference/`.

- [x] **Step 3: Extend LFS coverage**

Add this exact rule to `.gitattributes`:

```gitattributes
docs/design/trash-dash/character-animation/**/*.png filter=lfs diff=lfs merge=lfs -text
```

- [x] **Step 4: Confirm source-reference duplication is benign**

Compare every Phase 02–04 branded source PNG to its existing file under `docs/design/trash-dash/reference/characters/`. Expected: every duplicate is byte-identical; any mismatch is a stop condition.

### Task 2: Add the canonical 36-atlas inventory and validator

**Files:**
- Create: `docs/design/trash-dash/character-animation/phase-05-codex-integration/CANONICAL_IMPORT_INVENTORY.json`
- Create: `docs/design/trash-dash/character-animation/phase-05-codex-integration/IMPORT_AUDIT.md`
- Create: `tools/verify/check_character_animation_import.sh`
- Modify: `tools/verify/check_policy.sh`

**Interfaces:**
- Consumes: `ASSET_MAP.md`, original phase manifests, branded reference paths, and cleaned transparent atlas files.
- Produces: exactly 36 unique canonical IDs with class, level, source reference, approved atlas, SHA-256, dimensions, and source filename aliases.

- [x] **Step 1: Write the inventory**

Each record must include:

```json
{
  "asset_id": "squirrel",
  "asset_class": "common_enemy",
  "level": 2,
  "movement_profile": "grounded_projectile",
  "approved_atlas": "phase-02/final/squirrel-transparent.png",
  "approved_atlas_sha256": "<64 lowercase hex characters>",
  "source_reference": "docs/design/trash-dash/reference/characters/level-02/sprites/squirel.png",
  "source_filename_alias": "squirel.png"
}
```

Use `null` for player levels and classify enemies according to their authored grounded, flying, or projectile role. Bosses use `boss`.

- [x] **Step 2: Write a fail-closed validator**

The shell validator must reject missing tools, missing files, duplicate IDs, any count other than 36, invalid JSON, bad SHA-256 values, mismatched hashes, missing alpha-capable PNGs, absent LFS attributes, unresolved source references, and any source duplicate whose bytes differ from the existing repository reference.

- [x] **Step 3: Run the import audit**

```bash
tools/verify/check_character_animation_import.sh
```

Expected: `Character animation import: PASS (36/36 canonical atlases)`.

- [x] **Step 4: Inspect scope and stop**

```bash
git status --short
git diff --check
git lfs status
```

Confirm there are no files under `assets/generated/` or `assets/runtime/`, no runtime GDScript/scene changes, and no Godot process was launched. Record all duplicates, naming aliases, and remaining Stage 2–5 work as incomplete.
