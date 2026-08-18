# Trash Dash Design Library

This is the entry point for approved Trash Dash design sources and written
canon. Use the catalog to confirm approval and provenance before deriving or
integrating an asset.

## Authority flow

```text
library/ (approved source) -> assets/generated/ (candidate derivative)
                           -> assets/runtime/   (reviewed promotion only)

manuals/  written game canon
packages/ preserved handoffs and provenance; not a second canonical library
manifests/library-catalog.json  machine-readable canonical index
```

## Visual library

| Type | Location | Contents |
|---|---|---|
| Heroes | [`library/characters/heroes/`](library/characters/heroes/) | Trashy and Jimothy concepts, visual references, and approved animation sources |
| Bosses | [`library/characters/bosses/`](library/characters/bosses/) | One identity folder per boss |
| Enemies | [`library/characters/enemies/`](library/characters/enemies/) | Level-scoped concepts, references, and animation sources |
| Backgrounds | [`library/environments/backgrounds/`](library/environments/backgrounds/) | Five environment panels per level |
| Blueprints | [`library/environments/blueprints/`](library/environments/blueprints/) | Directional level layouts grouped by level |
| Environment concepts | [`library/environments/concepts/`](library/environments/concepts/) | Approved level look and interactive-environment references |
| Foreground references | [`library/environments/foreground/`](library/environments/foreground/) | Approved composition and foreground boards |
| Props | [`library/environments/props/`](library/environments/props/) | Isolated level-specific props |
| Tiles | [`library/environments/tiles/`](library/environments/tiles/) | Approved tilesheets and gameplay sheets |
| Items | [`library/gameplay/items/`](library/gameplay/items/) | Collectible concepts and source sheets |
| Power-ups | [`library/gameplay/powerups/`](library/gameplay/powerups/) | Taco/Kite references and approved preparation sources |
| Rewards | [`library/gameplay/rewards/`](library/gameplay/rewards/) | End-of-level reward art |
| Interface | [`library/interface/`](library/interface/) | UI concepts, extraction sheets, motion references, and tokens |
| Branding | [`library/branding/`](library/branding/) | Standalone approved brand assets; currently no approved logo or promotional source |

Character `sprites/reference/` folders preserve visual identity sheets.
`sprites/animation-source/` folders contain cleaned, approved extraction
sources. Neither is a fixed-cell runtime atlas unless its manifest says so.

## Written canon

- [`manuals/ANIMATION_MINIMUM_CHECKLIST.md`](manuals/ANIMATION_MINIMUM_CHECKLIST.md) — shared animation production baseline.
- [`manuals/characters/`](manuals/characters/) — playable-character canon.
- [`manuals/bosses/`](manuals/bosses/) — boss identity and behavior canon.
- [`manuals/enemies/`](manuals/enemies/) — enemy index, contracts, and level rosters.
- [`manuals/levels/`](manuals/levels/) — level guidance and imported content specifications.
- [`manuals/gameplay/`](manuals/gameplay/) — items, power-ups, UI rewards, and related rules.
- [`manuals/environments/`](manuals/environments/) — foreground and environment guidance.

## Preserved packages

Complete handoffs live in [`packages/`](packages/). Package-local manifests and
historical relative paths remain evidence of what was delivered. A file in a
package is canonical only when `manifests/library-catalog.json` points to its
approved library counterpart.

## Manifests and validation

- [`manifests/library-catalog.json`](manifests/library-catalog.json) — complete canonical asset catalog.
- [`manifests/LIBRARY_MIGRATION_MAP.tsv`](manifests/LIBRARY_MIGRATION_MAP.tsv) — old-to-new path accounting.
- [`manifests/LIBRARY_PRE_MIGRATION_INVENTORY.tsv`](manifests/LIBRARY_PRE_MIGRATION_INVENTORY.tsv) — immutable hash baseline.
- `python3 tools/verify/validate_design_library.py` — layout and reference validation.
- `python3 tools/verify/audit_canonical_assets.py` — asset hash, metadata, ID, and duplicate audit.

Archives and files marked superseded remain noncanonical. Never promote a
design source directly into gameplay without the applicable asset preparation
and release gates.
