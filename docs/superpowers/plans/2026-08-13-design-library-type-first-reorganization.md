# Design Library Type-First Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the fragmented Trash Dash design tree with one discoverable, type-first canonical library while preserving every source byte, stable identity, approval claim, package record, and active reference.

**Architecture:** A declarative Python layout module defines every legacy-to-current mapping and feeds the migration inventory, central catalog, migration map, and validator. Canonical visual sources live under `docs/design/trash-dash/library/`, written canon under `manuals/`, and intact handoff packages under `packages/`; generated and runtime boundaries remain unchanged. Package internals retain historical paths, while all active repository consumers use the new canonical paths.

**Tech Stack:** Python 3 standard library, JSON/TSV manifests, Markdown, Git/Git LFS, existing shell and Godot verification tools.

## Global Constraints

- Preserve the sibling V1 repository unchanged.
- Preserve every non-metadata source byte; do not transform artwork during this migration.
- Preserve the current dirty worktree and never discard pre-existing edits.
- Treat `assets/generated/` as rebuildable candidates and `assets/runtime/` as the only promoted-runtime boundary.
- Keep archives noncanonical and complete package handoffs non-runtime-authoritative.
- Remove design-only `.import` and `.DS_Store` metadata only after recording it in the migration map.
- Do not normalize stable asset IDs or original source filenames for cosmetic consistency.
- Record any necessary collision rename as an alias in `library-catalog.json`.
- Run all Godot processes through the project-local log safety helpers in `tools/verify/`.
- Report the pre-existing macOS CA-certificate diagnostic separately if it still blocks the intentional runner probe.

---

### Task 1: Encode the approved layout and preflight inventory

**Files:**
- Create: `tools/library/library_layout.py`
- Create: `tools/library/snapshot_design_library.py`
- Create: `tests/library/test_library_layout.py`
- Create: `docs/design/trash-dash/manifests/LIBRARY_PRE_MIGRATION_INVENTORY.tsv`

**Interfaces:**
- Produces: `MappingRecord(old_path, new_path, stable_id, disposition, category, aliases)` records returned by `build_mapping(root: Path) -> list[MappingRecord]`.
- Produces: a deterministic TSV inventory with `path`, `size`, `sha256`, `git_state`, `category`, `destination`, and `disposition` columns.
- Consumes: the approved taxonomy in `docs/superpowers/specs/2026-08-13-design-library-type-first-reorganization.md`.

- [ ] **Step 1: Write failing mapping tests**

Cover representative and collision-sensitive paths explicitly:

```python
def test_role_specific_character_mapping():
    mapping = mapping_by_old_path(FIXTURE_ROOT)
    assert mapping["docs/design/trash-dash/reference/main-characters/sprites/trashy-regular-approved.png"].new_path == (
        "docs/design/trash-dash/library/characters/heroes/trashy/sprites/reference/"
        "trashy-regular-approved.png"
    )
    assert mapping["docs/design/trash-dash/reference/characters/level-03/sprites/boss-pizza-rat-king.png"].new_path == (
        "docs/design/trash-dash/library/characters/bosses/pizza-rat-king/sprites/reference/"
        "boss-pizza-rat-king.png"
    )
    assert mapping["docs/design/trash-dash/reference/characters/level-03/sprites/subway-roach.png"].new_path == (
        "docs/design/trash-dash/library/characters/enemies/level-03/sprites/reference/subway-roach.png"
    )


def test_foreground_sources_do_not_collapse():
    mapping = mapping_by_old_path(FIXTURE_ROOT)
    approved = mapping[
        "docs/design/trash-dash/reference/foreground-assets/level-01/foreground-gameplay-assets.png"
    ]
    imported = mapping[
        "docs/design/trash-dash/reference/levels/level-01/references/foreground-gameplay-assets.png"
    ]
    assert approved.new_path == (
        "docs/design/trash-dash/library/environments/foreground/level-01/foreground-gameplay-assets.png"
    )
    assert imported.new_path == (
        "docs/design/trash-dash/packages/imported-source/trashy/levels/level-01/"
        "references/foreground-gameplay-assets.png"
    )
    assert approved.new_path != imported.new_path
```

- [ ] **Step 2: Run the tests and confirm they fail**

Run: `python3 -m unittest discover -s tests/library -p 'test_*.py'`

Expected: failure because `tools.library.library_layout` does not exist.

- [ ] **Step 3: Implement the declarative mapping module**

Define immutable records and exact mapping rules. The table must cover:

```python
@dataclass(frozen=True)
class MappingRecord:
    old_path: str
    new_path: str | None
    stable_id: str | None
    disposition: Literal[
        "canonical-moved",
        "package-preserved",
        "archive",
        "generated-metadata-removed",
    ]
    category: str
    aliases: tuple[str, ...] = ()
```

Encode these source-to-destination families:

| Legacy source | Destination |
|---|---|
| `reference/main-characters/concepts/<hero>-*` | `library/characters/heroes/<hero>/concepts/` |
| `reference/main-characters/sprites/<hero>-*` | `library/characters/heroes/<hero>/sprites/reference/` |
| character package Phase 01 approved atlases | copy to `library/characters/heroes/<hero>/sprites/animation-source/` |
| `reference/characters/level-*/concepts/boss.png` | `library/characters/bosses/<level-boss>/concepts/` |
| other `reference/characters/level-*/concepts/` | `library/characters/enemies/level-*/concepts/` |
| `reference/characters/level-*/sprites/boss-*.png` | `library/characters/bosses/<boss-id-without-boss-prefix>/sprites/reference/` |
| other `reference/characters/level-*/sprites/` | `library/characters/enemies/level-*/sprites/reference/` |
| character package Phase 02/03 final atlases | copy to matching enemy `sprites/animation-source/` |
| character package Phase 04 final atlases | copy to matching boss `sprites/animation-source/` |
| `reference/environments/level-*` | `library/environments/backgrounds/level-*` |
| `reference/foreground-assets/level-*` | `library/environments/foreground/level-*` |
| `reference/level-layouts/dynamic-approved/level-*-*` | `library/environments/blueprints/level-*` |
| `reference/levels/level-*/blueprints` | `library/environments/blueprints/level-*` |
| `reference/levels/level-*/concepts` | `library/environments/concepts/level-*` |
| `reference/levels/level-*/props` | `library/environments/props/level-*` |
| `reference/levels/level-*/tilesheets` | `library/environments/tiles/level-*` |
| `reference/levels/level-*/specs` | `manuals/levels/level-*` |
| `reference/levels/level-*/generation` and `/references` | `packages/imported-source/trashy/levels/level-*/` |
| `reference/items/collectibles-*` | `library/gameplay/items/<concepts-or-sprites>/` |
| `reference/items/powerups-*` | `library/gameplay/powerups/<concepts-or-sprites>/reference/` |
| `reference/rewards/*` | `library/gameplay/rewards/<concepts-or-sprites>/` |
| `reference/ui-powerups/concepts/*` | `library/interface/concepts/powerup-splashes/` |
| `reference/ui-powerups/sprites/*` | `library/interface/source-sheets/powerup-splashes/` |

Map the mixed gameplay-tile files explicitly rather than guessing from their
parent folder:

```python
GAMEPLAY_TILE_DESTINATIONS = {
    "trash_dash_forest_level_blueprint.png": "environments/blueprints/level-01",
    "trash_dash_moonlit_neighborhood_blueprint.png": "environments/blueprints/level-02",
    "trash_dash_level_2_concept_board.png": "environments/concepts/level-02",
    "trash_dash_space_center_level_4.png": "environments/concepts/level-04",
    "trash_dash_orbital_junkyard_concepts.png": "environments/concepts/level-05",
    "trash_dash_stadium_nightfall_layout.png": "environments/blueprints/level-06",
    "trash_dash_suburban_night_sprite_atlas.png": "environments/tiles/level-02",
    "trash_dash_level_3_sprite_sheet.png": "environments/tiles/level-03",
    "trash_dash_level_4_sprite_sheet.png": "environments/tiles/level-04",
    "trash_dash_orbital_junkyard_sprite_sheet.png": "environments/tiles/level-05",
}
```

Use the boss map `01=trash-dash`, `02=brutus-bin-hound`,
`03=pizza-rat-king`, `04=project-opossum`, `05=galactogobbler`, and
`06=diamond-don`. Preserve `squirel.png` as a source filename and record
`squirrel` as its stable-ID alias.

- [ ] **Step 4: Implement the deterministic preflight snapshot**

`snapshot_design_library.py` must hash every file beneath the current design
tree, read tracked/untracked state through `git ls-files` and `git status
--porcelain=v1`, join it to `build_mapping()`, refuse any unaccounted path, and
write the sorted TSV atomically. Metadata files receive
`generated-metadata-removed`; no source file may have a null destination.

- [ ] **Step 5: Generate and inspect the preflight inventory**

Run:

```bash
python3 tools/library/snapshot_design_library.py \
  --output docs/design/trash-dash/manifests/LIBRARY_PRE_MIGRATION_INVENTORY.tsv
```

Expected: exit 0, deterministic row count, and no `unresolved` disposition.
Run the command twice and confirm the output hash is identical.

- [ ] **Step 6: Run the mapping tests**

Run: `python3 -m unittest discover -s tests/library -p 'test_*.py'`

Expected: PASS.

- [ ] **Step 7: Commit the mapping contract and snapshot**

```bash
git add tools/library/library_layout.py tools/library/snapshot_design_library.py \
  tests/library/test_library_layout.py \
  docs/design/trash-dash/manifests/LIBRARY_PRE_MIGRATION_INVENTORY.tsv
git commit -m "test: lock design library migration map"
```

---

### Task 2: Build the catalog and structure validator before moving content

**Files:**
- Create: `tools/verify/validate_design_library.py`
- Create: `tests/library/test_validate_design_library.py`
- Modify: `tools/verify/audit_canonical_assets.py`
- Modify: `tools/verify/test_shell_contracts.sh`

**Interfaces:**
- Consumes: `MappingRecord` and the preflight inventory from Task 1.
- Produces: `validate_design_library.py --root <path>` with deterministic diagnostics and exit 1 on any invariant violation.
- Produces: validation of `manifests/library-catalog.json` and `manifests/LIBRARY_MIGRATION_MAP.tsv` after migration.

- [ ] **Step 1: Write failing validator tests with temporary fixture trees**

Include focused cases for missing catalog paths, duplicate stable IDs,
uncataloged library files, package/runtime authority violations, unaccounted
legacy paths, design `.import` files, and active stale `reference/` links.

```python
def test_active_legacy_reference_fails(self):
    self.write("AGENTS.md", "Use docs/design/trash-dash/reference/characters")
    result = self.run_validator()
    self.assertNotEqual(result.returncode, 0)
    self.assertIn("active legacy path", result.stdout)


def test_historical_package_reference_is_allowed(self):
    self.write(
        "docs/design/trash-dash/packages/imported-source/README.md",
        "Original package root: reference/characters",
    )
    result = self.run_validator(minimal_valid_catalog=True)
    self.assertEqual(result.returncode, 0, result.stdout)
```

- [ ] **Step 2: Run the validator tests and confirm they fail**

Run: `python3 -m unittest tests.library.test_validate_design_library -v`

Expected: failure because the validator does not exist.

- [ ] **Step 3: Implement the validator**

The validator must:

- require schema `trash-dash-v2-library-catalog-v1`;
- hash-check each catalog record;
- reject duplicate IDs and duplicate canonical paths;
- ensure every non-README source file in `library/` is cataloged;
- reject canonical or runtime authority for `packages/` and archives;
- validate every migration-map old path against the preflight inventory;
- require each nonremoved migration-map destination to exist;
- reject `.import` and `.DS_Store` under `docs/design/trash-dash/`;
- scan active text consumers while excluding `.git/`, historical
  `docs/superpowers/`, package internals, and the migration map's old-path
  column;
- allow the approved design spec to describe the former path as history;
- report all failures in one run rather than stopping at the first error.

- [ ] **Step 4: Refactor the canonical audit to consume the new catalog**

Replace the partial `canonical-asset-manifest.json` path assumption with
`library-catalog.json`. Preserve image dimension, alpha, hash, duplicate-ID,
and visual-identity checks. Scope unregistered-file detection to the entire
canonical `library/` root.

- [ ] **Step 5: Add shell contract coverage**

Extend `tools/verify/test_shell_contracts.sh` with fixtures proving that the
new validator is included by local policy verification and propagates a
nonzero exit.

- [ ] **Step 6: Run focused tests**

```bash
python3 -m unittest discover -s tests/library -p 'test_*.py'
tools/verify/test_shell_contracts.sh
```

Expected: unit tests PASS; the repository-level validator itself may report
the expected pre-migration missing catalog/tree until Task 6.

- [ ] **Step 7: Commit the validator**

```bash
git add tools/verify/validate_design_library.py \
  tools/verify/audit_canonical_assets.py tools/verify/test_shell_contracts.sh \
  tests/library/test_validate_design_library.py
git commit -m "test: validate canonical design library structure"
```

---

### Task 3: Migrate canonical character and environment sources

**Files:**
- Create: `tools/library/reorganize_design_library.py`
- Modify: `tests/library/test_library_layout.py`
- Move: `docs/design/trash-dash/reference/main-characters/` into typed hero paths
- Move: `docs/design/trash-dash/reference/characters/` into typed boss/enemy paths
- Move: `docs/design/trash-dash/reference/environments/`, `foreground-assets/`, `gameplay-tiles/`, `level-layouts/`, and `levels/` into typed environment paths or preserved package paths
- Copy authoritative character package outputs into `library/characters/**/sprites/animation-source/`

**Interfaces:**
- Consumes: Task 1's exact mapping and preflight hashes.
- Produces: `reorganize_design_library.py --check` and `--apply`; `--apply` refuses overwrite, verifies source hashes, moves canonical sources, copies package-approved implementation sources, and never deletes package originals.

- [ ] **Step 1: Write failing dry-run and collision tests**

Tests must prove that `--check` reports planned operations without writing,
that non-identical destinations are rejected, and that copies from preserved
packages retain both source and destination.

- [ ] **Step 2: Implement safe apply semantics**

Use `Path.replace()` only after validating source and destination boundaries,
then immediately hash-check the destination. Git will detect tracked renames
from the byte-identical moves; untracked imported sources receive the same
boundary and hash checks. Use `shutil.copy2` only for the package-to-library
authoritative copies, whose package source receives the `package-preserved`
disposition and remains intact.

- [ ] **Step 3: Dry-run the character batch**

Run: `python3 tools/library/reorganize_design_library.py --check --batch characters`

Expected: all hero, boss, and enemy sources accounted for; no collision or
unresolved authority.

- [ ] **Step 4: Apply and verify the character batch**

Run: `python3 tools/library/reorganize_design_library.py --apply --batch characters`

Then compare every character source hash to the preflight inventory. Confirm
the animation-source library contains 4 playable-character, 26 common-enemy,
and 6 boss atlases while the complete 211-file character package still exists.

- [ ] **Step 5: Dry-run the environment batch**

Run: `python3 tools/library/reorganize_design_library.py --check --batch environments`

Expected: the six newer nonidentical foreground reference sheets route to the
preserved Trashy package area, while the six older approved foreground sheets
route to the canonical library.

- [ ] **Step 6: Apply and verify the environment batch**

Run: `python3 tools/library/reorganize_design_library.py --apply --batch environments`

Confirm all six levels have predictable `backgrounds`, `blueprints`,
`concepts`, `foreground`, `props`, and `tiles` locations represented by a
category README when no asset exists. Do not add placeholder images.

- [ ] **Step 7: Run focused integrity checks**

```bash
python3 -m unittest discover -s tests/library -p 'test_*.py'
python3 tools/library/reorganize_design_library.py --check --batch characters
python3 tools/library/reorganize_design_library.py --check --batch environments
```

Expected: PASS and zero pending source moves for both applied batches.

- [ ] **Step 8: Commit the canonical visual migration**

Stage only the migration tool, tests, and character/environment source moves.
Review `git diff --summary` and rename detection before committing.

```bash
git commit -m "assets: organize characters and environments by type"
```

---

### Task 4: Migrate gameplay, interface, branding, manuals, and packages

**Files:**
- Move: `docs/design/trash-dash/reference/items/`, `rewards/`, and `ui-powerups/` into `library/gameplay/` or `library/interface/`
- Move: `docs/design/trash-dash/docs/game/` into `manuals/`
- Move: `docs/design/trash-dash/character-animation/` into `packages/character-animation/`
- Move: `docs/design/trash-dash/ui-kit/` into `packages/ui-kit/`
- Move: `docs/design/trash-dash/powerups/` into `packages/powerups/`
- Move: `docs/design/trash-dash/multipart/` into `packages/multipart/`
- Move: `docs/design/trash-dash/docs/integration/` and `docs/prompts/` into `packages/imported-source/master-bundle/`
- Copy: approved UI and power-up sources from preserved packages into canonical library paths

**Interfaces:**
- Consumes: the safe migration engine from Task 3.
- Produces: one canonical copy of each approved gameplay/UI source plus complete preserved handoff packages.

- [ ] **Step 1: Extend tests for manual/package and package-copy rules**

Assert these exact manual families:

| Current content | Destination |
|---|---|
| `docs/game/APPROVED_ASSET_POLICY.md`, `DECISIONS.md` | `manuals/` |
| `APPROVED_MAIN_CHARACTERS.md`, `MAIN_CHARACTERS.md` | `manuals/characters/` |
| `docs/game/bosses/**` | `manuals/bosses/` |
| enemy-canon Markdown/YAML | `manuals/enemies/` |
| enemy-canon `reference-art/**` | `packages/imported-source/trashy/enemy-canon/reference-art/` |
| `ITEMS_POWERUPS_UI_REWARDS.md` | `manuals/gameplay/` |
| `LEVEL_LAYOUT_GUIDANCE.md`, `levels.md` | `manuals/levels/` |
| `foreground-assets.md` | `manuals/environments/` |

- [ ] **Step 2: Apply the gameplay batch**

Run: `python3 tools/library/reorganize_design_library.py --apply --batch gameplay`

Copy the approved Taco/Kite clean item sheet and two clean overlay sheets from
the preserved power-up package into `library/gameplay/powerups/sprites/animation-source/`.
Copy its approved branded boards into `library/gameplay/powerups/concepts/`.
Do not promote them to `assets/runtime/`.

- [ ] **Step 3: Apply the interface and branding batch**

Run: `python3 tools/library/reorganize_design_library.py --apply --batch interface`

Copy the UI kit's approved concept boards, four source sheets, UI tokens, and
motion references into the matching `library/interface/` branches. Do not copy
alternate embedded logos into `library/branding/`; add a README stating that
no standalone canonical logo or promotional asset is currently approved.

- [ ] **Step 4: Apply manuals and packages batches**

```bash
python3 tools/library/reorganize_design_library.py --apply --batch manuals
python3 tools/library/reorganize_design_library.py --apply --batch packages
```

Preserve package-local file names and internal relative structure. Update only
the package root location; do not rewrite package history at this stage.

- [ ] **Step 5: Verify package completeness and byte preservation**

Confirm the moved packages retain their preflight file counts: character
animation 211, UI kit 41, power-ups 18, and multipart 8. Hash every preserved
package file against the preflight inventory.

- [ ] **Step 6: Run focused tests**

Run: `python3 -m unittest discover -s tests/library -p 'test_*.py'`

Expected: PASS with no pending gameplay, interface, manuals, or package move.

- [ ] **Step 7: Commit the remaining library and package migration**

Review rename/copy summaries and stage only Task 4 paths.

```bash
git commit -m "assets: organize gameplay interface manuals and packages"
```

---

### Task 5: Generate the complete catalog and migration map

**Files:**
- Create: `docs/design/trash-dash/manifests/library-catalog.json`
- Create: `docs/design/trash-dash/manifests/LIBRARY_MIGRATION_MAP.tsv`
- Modify: `docs/design/trash-dash/manifests/MASTER_ASSET_CATEGORIES.json`
- Modify: `docs/design/trash-dash/manifests/canonical-asset-manifest.json`
- Modify: `tools/asset_pipeline/import_trashy_canonical_assets.py`
- Modify: `tools/library/reorganize_design_library.py`

**Interfaces:**
- Produces: catalog schema `trash-dash-v2-library-catalog-v1`.
- Produces: import behavior that targets `library/`, `manuals/`, and `packages/imported-source/trashy/` directly and refuses legacy-root recreation.

- [ ] **Step 1: Write failing deterministic-catalog tests**

Require sorted stable IDs, paths relative to repository root, exact SHA-256,
required authority fields, aliases for legacy paths, and byte-identical output
across repeated runs.

- [ ] **Step 2: Implement catalog and migration-map generation**

Each catalog record must contain fields equivalent to this generated record:

```python
record = {
    "id": "level-03.enemy.subway-roach.animation-source",
    "resourceType": "character-animation-source",
    "canonicalPath": canonical_path.relative_to(ROOT).as_posix(),
    "level": "03",
    "character": "subway-roach",
    "approvalStatus": "approved-source",
    "sourcePackage": "character-animation/phase-05-codex-integration",
    "sha256": sha256(canonical_path),
    "intendedUsage": "animation extraction source",
    "runtimeStatus": "not-runtime",
    "aliases": [],
}
```

Populate hashes from the files, never from stale manifests. Merge stable IDs
from existing manifests and package inventories; refuse collisions rather than
adding numeric suffixes.

- [ ] **Step 3: Convert the partial canonical import manifest**

Retain it as an import-specific provenance document, update all destination
paths, and add `supersededByCatalog` pointing to `library-catalog.json`. It
must no longer claim to be the complete canonical library index.

- [ ] **Step 4: Retarget the Trashy importer**

Replace `REFERENCE` with explicit `LIBRARY`, `MANUALS`, and
`TRASHY_PACKAGE` roots. Route imported visual canon through the same mapping
module used by the migration, route generation/support material into the
preserved package, and make a second import into an already migrated fixture a
no-op with identical catalog output.

- [ ] **Step 5: Generate and validate both manifests**

```bash
python3 tools/library/reorganize_design_library.py --write-manifests
python3 tools/verify/validate_design_library.py
python3 tools/verify/audit_canonical_assets.py
```

Expected: PASS with every library source cataloged and every preflight path
accounted for.

- [ ] **Step 6: Commit catalog authority changes**

```bash
git add docs/design/trash-dash/manifests tools/asset_pipeline/import_trashy_canonical_assets.py \
  tools/library/reorganize_design_library.py
git commit -m "assets: establish complete design library catalog"
```

---

### Task 6: Update active references and add the human library index

**Files:**
- Create: `docs/design/trash-dash/LIBRARY_INDEX.md`
- Create: `docs/design/trash-dash/.gdignore`
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `docs/design/trash-dash/README.md`
- Modify: `docs/design/trash-dash/MULTIPART_README.md`
- Modify: `.gitattributes`
- Modify: `.gitignore`
- Modify: `.skills/**` files containing active design paths
- Modify: `tools/asset_pipeline/build_boss_*.py`
- Modify: `tools/verify/check_boss_*.py`
- Modify: `tools/verify/check_character_animation_import.sh`
- Modify: `tools/verify/check_powerup_source_import.sh`
- Modify: active generated manifests, source audits, validation reports, and READMEs under `assets/generated/`
- Modify: active architecture/migration documentation that instructs current work

**Interfaces:**
- Consumes: final canonical paths and catalog from Task 5.
- Produces: one human entry point and zero active references to the former root or former package/manual locations.

- [ ] **Step 1: Write the library index**

The index must contain a concise authority diagram, a category table with
clickable relative links, level-specific location examples, manual/package
links, catalog/approval guidance, and a clear source → generated → runtime
flow. It must explicitly state that `packages/` preserves evidence and is not a
second canonical source root.

- [ ] **Step 2: Update project authority instructions**

Change `AGENTS.md` and the root/design READMEs to name `library/`, `manuals/`,
`packages/`, and `library-catalog.json`. Update the canonical UI and boss/enemy
manual instructions to their new locations. Keep archive restrictions intact.

- [ ] **Step 3: Update active code and generated-evidence consumers**

Use the migration map to replace exact path literals. Do not global-replace
bare `reference/`, because package-local references and prose uses of the word
"reference" are legitimate. Re-run `rg` after each consumer family.

- [ ] **Step 4: Add `.gdignore` and remove generated metadata**

Add `.gdignore` at `docs/design/trash-dash/`. Remove all 341 design-tree
`.import` sidecars and all 24 `.DS_Store` files only after confirming each has
`generated-metadata-removed` in the migration map. Do not touch `.import`
settings beneath `assets/runtime/`.

- [ ] **Step 5: Validate active-reference hygiene**

Run:

```bash
python3 tools/verify/validate_design_library.py
rg -n 'docs/design/trash-dash/reference/' \
  AGENTS.md README.md .skills tools assets/generated docs/architecture docs/migration
```

Expected: validator PASS and `rg` produces no active match. Historical specs,
plans, reports, and package evidence may retain migration-context matches.

- [ ] **Step 6: Commit discovery and reference updates**

Review pre-existing edits in `AGENTS.md`, `README.md`, `.gitignore`, and any
other dirty file before staging; preserve every unrelated line.

```bash
git commit -m "docs: publish discoverable design library index"
```

---

### Task 7: Integrate validation and produce final migration evidence

**Files:**
- Modify: `tools/verify/check_policy.sh`
- Modify: `tools/verify/verify_local.sh`
- Create: `docs/superpowers/reports/2026-08-13-design-library-reorganization.md`
- Modify: `docs/migration/V2_BUILD_PLAN.md`

**Interfaces:**
- Consumes: validator, catalog, migration map, and final file tree.
- Produces: clean-checkout-capable policy enforcement and a direct-evidence migration report.

- [ ] **Step 1: Add the library validator to local policy verification**

Invoke `python3 tools/verify/validate_design_library.py` and
`python3 tools/verify/audit_canonical_assets.py` before Godot import. Ensure a
validator failure stops `verify_local.sh` with the original exit code.

- [ ] **Step 2: Run non-Godot verification**

```bash
python3 -m unittest discover -s tests/library -p 'test_*.py'
python3 tools/verify/validate_design_library.py
python3 tools/verify/audit_canonical_assets.py
tools/verify/check_policy.sh
tools/verify/test_shell_contracts.sh
tools/verify/check_character_animation_import.sh
tools/verify/check_powerup_source_import.sh
```

Expected: PASS. If a package checker intentionally validates package-internal
historical paths, update only its package root, not its internal contract.

- [ ] **Step 3: Run the existing Godot test wrapper once**

Run: `tools/verify/run_tests.sh`

Expected: either PASS or the separately documented pre-existing macOS
`get_system_ca_certificates` diagnostic. Do not retry automatically after a
nonzero exit; inspect `.codex/godot-logs/` and record the exact command, exit,
engine log, and output log.

- [ ] **Step 4: Run full local verification only when its prerequisites pass**

Run: `tools/verify/verify_local.sh`

Expected: PASS through policy, import, tests, smoke, unsigned macOS export, and
bounded package process. If the existing CA diagnostic or dirty-checkout export
policy blocks the run, record `CANNOT VERIFY` for that step without weakening
the gate.

- [ ] **Step 5: Write the migration report**

Record:

- pre/post source counts by category;
- pre/post package counts;
- source hash preservation totals;
- exact `.import` and `.DS_Store` removal counts;
- catalog and migration-map row counts;
- all validator/test commands and results;
- every unresolved ambiguity, or an explicit `none`;
- confirmation that `assets/generated/` and `assets/runtime/` authority did
  not change;
- the pre-existing Godot diagnostic separately from migration defects.

- [ ] **Step 6: Update the roadmap**

Record the library organization/catalog validation as completed asset-pipeline
infrastructure without marking runtime asset promotion, vertical-slice proof,
or the V2 release gate complete.

- [ ] **Step 7: Review the full diff and commit final verification wiring**

```bash
git diff --check
git status --short
git diff --stat
git commit -m "chore: verify type-first design library migration"
```

- [ ] **Step 8: Final acceptance check**

Confirm every acceptance requirement in the approved design spec maps to
direct evidence in the final report. Report the migration as `INCOMPLETE` if
any source is unaccounted for, any active link is stale, any catalog invariant
fails, or any non-metadata hash is lost.
