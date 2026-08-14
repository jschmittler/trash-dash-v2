# Design Library Reorganization Report

**Date:** 2026-08-13
**Scope:** Trash Dash V2 design sources, written canon, handoff packages, manifests, and active repository references.

## Outcome

The design library now uses a type-first structure rooted at
`docs/design/trash-dash/library/`. Written canon is under `manuals/`, complete
handoff bundles are under `packages/`, and machine-readable discovery data is
under `manifests/`. This migration changes source-library organization only;
it does not promote assets into the Godot runtime or change runtime approval.

## Accounting

- Pre-migration inventory: 835 files.
- Canonical catalog: 253 assets.
- Migration map: all 835 pre-migration paths accounted for.
- Removed generated metadata: 365 `.import` and `.DS_Store` files. These are
  recorded in the migration map and are regenerable or recoverable from Git.
- Preserved non-metadata handoff files:
  - Character animation: 117.
  - UI kit: 31.
  - Power-ups: 12.
  - Multipart source: 8.
- Six newer Trashy-import foreground boards that differed from approved
  foreground boards were retained in the imported-source package instead of
  replacing approved canonical assets.
- Three byte-identical power-up board copies were not duplicated in the
  canonical library; their established canonical files and package originals
  remain available.

## Discovery and safeguards

- `LIBRARY_INDEX.md` provides a human entry point.
- `library-catalog.json` provides stable asset IDs, paths, categories, hashes,
  and aliases.
- `LIBRARY_MIGRATION_MAP.tsv` resolves every old path to its destination or
  documented metadata-removal disposition.
- Library validators check schema, hashes, catalog completeness, migration
  accounting, forbidden metadata, active path references, and Markdown links.
- The canonical asset audit, repository policy check, character animation
  source check, and power-up source check now operate on the new structure.

## Verification evidence

- Library unit tests: 9 passed.
- Design library validator: passed.
- Canonical asset audit: passed (253 registered files; 251 visual identities).
- Repository policy check: passed.
- Shell contract suite: passed with 0 failures.
- Character animation source check: passed (36/36 canonical atlases).
- Power-up source check: passed (3 working sources; 3 references).

The migration validator confirms preserved hashes for visual sources and
handoff-package files. Documentation files are allowed to change because their
paths and descriptions were intentionally updated.

## Boundary and outstanding environment issue

The canonical runtime and generated-asset boundaries are unchanged. The
repository's Godot wrapper still encounters the previously observed macOS
system CA-certificate diagnostic during its intentional failure probe. This is
an environment/harness issue outside the source-library rewrite and must not be
interpreted as asset promotion or V2 release-gate completion.
