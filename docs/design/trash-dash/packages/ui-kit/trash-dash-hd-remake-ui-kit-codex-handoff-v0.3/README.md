# Trash Dash HD Remake UI Kit - Codex Handoff

Version: 0.3.0

This package combines the approved Trash Dash UI visual direction, phased source sheets, component contracts, motion rules, crop guidance, validation tools, and a Codex import prompt.

The core visual language is **Reclaimed Playground**: a playful, physical interface assembled from cardboard, painted wood, paper, stickers, tape, bottle caps, hardware, warning signs, and hand-painted marks.

## Read in this order

1. `docs/APPROVAL_AND_AUTHORITY.md`
2. `docs/UI_KIT_BRIEF.md`
3. `docs/ASSET_CATALOG.md`
4. `docs/ASSET_EXTRACTION_AND_RUNTIME_USE.md`
5. `docs/COMPONENTS.md`
6. `docs/MOTION.md`
7. `docs/IMPLEMENTATION.md`
8. `tokens/ui.tokens.json`
9. `tokens/motion.tokens.json`
10. `ui-kit.manifest.json`
11. `manifests/asset-manifest.json`
12. `manifests/sprite-regions.json`
13. `CODEX_IMPORT_PROMPT.md`

## Package structure

```text
trash-dash-hd-remake-ui-kit-codex-handoff-v0.3/
  README.md
  CODEX_IMPORT_PROMPT.md
  AGENTS_UI_KIT_SNIPPET.md
  ui-kit.manifest.json
  docs/
  tokens/
  contracts/
  reference/
    concept-boards/
    motion/
  source-sheets/
  manifests/
  tools/
```

## Source of truth

Use this order when sources differ:

1. Written contracts, tokens, and approval rules
2. Overall concept board
3. Matching phase concept board
4. Matching source sheet
5. Implementation judgment that preserves the system

## Important asset status

The source sheets are approved source art, not final runtime atlases.

Codex must:

- stage the source files
- extract named regions
- clean alpha and fringes
- preserve aspect ratio
- separate dynamic text
- build scalable panels with 9-slice or layers
- define pivots and safe zones
- implement required motion
- validate in live gameplay

## Brand-name note

Some concept boards display the working label Trash Dash V2. The current game name is Trash Dash HD Remake. Do not use the V2 label as new runtime branding unless explicitly requested.

## Validation

Run:

```bash
python tools/validate_ui_package.py --package-root .
```

Optional staged extraction:

```bash
python tools/extract_ui_sources.py --package-root . --mode raw --output extracted/raw
```
