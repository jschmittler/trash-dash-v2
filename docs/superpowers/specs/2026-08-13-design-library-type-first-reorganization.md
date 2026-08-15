# Trash Dash Design Library Type-First Reorganization

**Status:** Approved design, awaiting implementation plan

**Approved:** 2026-08-13

## Goal

Reorganize the Trash Dash 2.0 design library into one discoverable,
type-first canonical structure without losing files, provenance, approval
state, stable asset identity, package evidence, or active references.

## Authority model

`docs/design/trash-dash/library/` becomes the only canonical root for visual
and source assets. `docs/design/trash-dash/manuals/` becomes the only canonical
root for written game canon. `docs/design/trash-dash/packages/` preserves
complete imported handoffs, source packs, package-local manifests, QA reports,
and historical evidence; package contents are not automatically canonical or
runtime-authoritative.

`docs/design/trash-dash/manifests/` remains the machine-readable authority
layer. Rebuildable candidates stay under `assets/generated/`. Only promoted
runtime assets belong under `assets/runtime/`. Existing archive content remains
noncanonical and isolated.

Moves must preserve source bytes. Every former path must have a recorded
destination or a documented disposition. Similar-looking artwork must not be
deduplicated. Only byte-identical files with a clearly established canonical
owner may collapse to one library entry; complete package copies remain intact
for provenance.

## Canonical taxonomy

```text
docs/design/trash-dash/
├── library/
│   ├── characters/
│   │   ├── heroes/
│   │   │   ├── trashy/{concepts,sprites}
│   │   │   └── jimothy/{concepts,sprites}
│   │   ├── bosses/
│   │   │   └── <boss-id>/{concepts,sprites}
│   │   └── enemies/
│   │       └── level-01…level-06/{concepts,sprites}
│   ├── environments/
│   │   ├── backgrounds/level-01…level-06
│   │   ├── blueprints/level-01…level-06
│   │   ├── concepts/level-01…level-06
│   │   ├── foreground/level-01…level-06
│   │   ├── props/level-01…level-06
│   │   └── tiles/level-01…level-06
│   ├── gameplay/
│   │   ├── items/{concepts,sprites}
│   │   ├── powerups/{concepts,sprites}
│   │   ├── rewards/{concepts,sprites}
│   │   └── effects/{concepts,sprites}
│   ├── interface/
│   │   ├── concepts
│   │   ├── source-sheets
│   │   ├── tokens
│   │   └── motion
│   └── branding/
│       ├── concepts
│       ├── logos
│       └── promotional
├── manuals/
│   ├── characters
│   ├── bosses
│   ├── enemies
│   ├── levels
│   ├── gameplay
│   └── interface
├── packages/
│   ├── character-animation
│   ├── ui-kit
│   ├── powerups
│   ├── multipart
│   └── imported-source
└── manifests/
```

Level-specific content stays under its asset type using the stable directories
`level-01` through `level-06`. Each environment category uses the same level
layout even when a category is initially empty. Characters are grouped by role
first, then by identity or level.

The design tree receives a `.gdignore`. Design-only Godot `.import` sidecars
are removed and recorded as generated metadata in the migration map. Import
settings for promoted runtime assets remain with content under
`assets/runtime/`.

## Catalog and discovery

Create `docs/design/trash-dash/manifests/library-catalog.json` as the complete
index of every canonical library file. Each record contains:

- stable asset ID;
- resource type;
- canonical path;
- level or character association when applicable;
- approval state;
- source package;
- SHA-256 digest;
- intended use;
- runtime status;
- aliases for any recorded legacy or corrected name.

Package-local manifests remain intact inside `packages/` and continue to
describe their original package layout. The central catalog describes current
canonical paths and authority.

Create `docs/design/trash-dash/manifests/LIBRARY_MIGRATION_MAP.tsv`. It records
every old path, new path, stable ID, hash, and disposition. Allowed
dispositions are `canonical-moved`, `package-preserved`, `archive`, and
`generated-metadata-removed`.

Create `docs/design/trash-dash/LIBRARY_INDEX.md` as the human entry point. It
links every library category, manual, package, manifest, generated area, and
runtime area, and explains the source/generated/runtime authority boundaries.

Stable asset IDs and source filenames remain unchanged unless a filename is
actively misleading. A necessary correction is recorded as an alias rather
than silently changing identity.

## Reference migration

Update active repository instructions, contracts, READMEs, scripts,
validators, Godot resources, manifests, and Markdown links to the new paths.
Historical plans and reports retain factual statements about original package
layouts but receive valid current links or migration notes where needed.

A repository validator fails when it finds:

- an active reference to the former `docs/design/trash-dash/reference/` root;
- a canonical library file absent from the catalog;
- a catalog path that does not exist;
- duplicate canonical IDs or competing canonical claims;
- archive or package files marked runtime-authoritative;
- an old path missing from the migration map;
- a design-library `.import` sidecar.

## Migration process

Before moving files, capture the path, byte size, SHA-256, category, and Git
state of every source. Migrate in independently verifiable batches:

1. characters;
2. environments;
3. gameplay assets;
4. interface and branding;
5. manuals;
6. preserved packages;
7. manifests and repository references.

After each batch, verify that every source hash still exists, each catalog
destination exists, no active stale path remains for the migrated category,
and relevant package or canonical asset validation passes. A file with unclear
authority remains unmoved and is reported as unresolved; the migration must not
guess.

## Verification and acceptance

The completed migration must provide direct evidence that:

1. every pre-migration file has a destination or allowed disposition;
2. all source bytes are preserved except recorded generated `.import`
   metadata;
3. all canonical catalog paths and Markdown links resolve;
4. package-local manifests still validate against preserved packages;
5. canonical IDs and approval claims remain complete and unique;
6. `assets/generated/` and `assets/runtime/` boundaries are unchanged;
7. repository policy, asset audits, shell tests, and the Godot suite have been
   run with exact results recorded;
8. the final report lists counts before and after, hash preservation, removed
   metadata, unresolved ambiguity, and all verification outcomes.

The existing macOS Godot CA-certificate diagnostic is a pre-existing test
harness limitation. If it still prevents the intentional-failure probe from
completing, report it separately and do not attribute it to this migration.

## Non-goals

- Promoting assets into `assets/runtime/`.
- Changing artwork, animation, level content, or game canon.
- Reclassifying archive content as canonical.
- Rewriting package history to resemble the new canonical layout.
- Renaming stable IDs for cosmetic consistency.
