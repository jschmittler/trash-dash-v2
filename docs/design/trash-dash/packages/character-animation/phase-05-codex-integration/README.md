# Trash Dash Phase 05 Codex Integration Handoff

This is the canonical handoff for the approved character, common-enemy, and boss animation sources created in Phases 01 through 04.

## Scope

- 4 playable-character variants
- 26 common enemies across Levels 1 through 6
- 6 bosses across Levels 1 through 6
- 36 approved animation source atlases total

These source atlases preserve variable-width poses, projectiles, props, effects, transformations, and defeat states. They are not equal-grid runtime atlases.

## Start here

1. Read `CODEX_IMPORT_AND_INTEGRATION_PROMPT.md`.
2. Verify every archive against `qa/SHA256SUMS`.
3. Import the source package into `docs/design/trash-dash/` without overwriting unrelated project files.
4. Stop after the import audit and report the inventory before beginning extraction.
5. Complete extraction, runtime integration, and gameplay validation as separate gated stages.

## Important exclusions

Environment concept sheets, parallax layers, ground, platforms, foreground props, and collectibles are separate production tracks. Do not infer or generate them from this package, and do not fold them into character frame extraction.
