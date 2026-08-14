# Approval and Authority Policy

## Included approved direction

This handoff includes the visual direction and source sheets accepted through the phased UI Kit work:

- overall UI Kit concept board
- Phase 1 buttons and tabs
- Phase 2 panels and containers
- Phase 3 HUD, notifications, and alerts
- corrected Phase 4 results, rewards, and Character Select
- motion and animation direction

The earlier Phase 4 pass that moved away from the reclaimed-cardboard source style is intentionally excluded.

## What approval means

Approval means the assets are accepted as source material and direction for implementation.

It does not mean every PNG is already a clean runtime sprite. Codex must still extract, normalize, separate dynamic text, define 9-slice margins, create pivots, and perform live visual QA.

## Authority levels

### Canonical visual direction

- `reference/concept-boards/00-overall-ui-kit.png`
- matching phase concept boards
- `docs/UI_KIT_BRIEF.md`

### Approved extraction sources

- `source-sheets/phase-01-buttons-tabs.png`
- `source-sheets/phase-02-panels-containers.png`
- `source-sheets/phase-03-hud-notifications-alerts.png`
- `source-sheets/phase-04-results-character-select.png`

### Behavioral authority

- `tokens/motion.tokens.json`
- `docs/MOTION.md`
- `ui-kit.manifest.json`

## Source-sheet limitations

Generated source sheets can contain presentation residue, example text, extra decoration, or exploratory elements.

Do not treat these as canonical:

- alternate title logos shown inside sheets
- accidental character redesigns
- sheet headers and section labels
- brown or vignette backgrounds
- presentation shadows that do not survive extraction
- demo values such as example scores or times
- optional mini-map or character portrait HUD without gameplay approval

## Character authority

Trashy and Jimothy must retain the approved appearances shown on the overall concept board and corrected Phase 4 source sheet.

The UI portraits are not replacements for gameplay sprite sheets.

## No silent substitution

If an asset cannot be extracted cleanly, report it. Do not silently replace it with generic UI, an off-style generated asset, or a new character interpretation.

A temporary implementation may use a clearly labeled placeholder while preserving the intended layout and motion contract.
