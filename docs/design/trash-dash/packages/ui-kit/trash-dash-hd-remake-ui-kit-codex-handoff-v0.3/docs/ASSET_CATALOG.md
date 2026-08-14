# Asset Catalog and Intended Use

## Asset authority

The package has two visual layers:

- **Concept boards** are the visual reference and composition authority.
- **Source sheets** are extraction and production sources.

The source sheets are not ready-to-use runtime atlases. They contain presentation spacing, uneven alpha, shadows, and in some cases example text or exploratory decoration. Extract and normalize them before use.

## Overall concept board

### `reference/concept-boards/00-overall-ui-kit.png`

Defines the complete system in one view:

- main menu hero panel
- primary and secondary buttons
- tab navigation
- pickup notification
- warning alert
- objective tracker
- junk-box pause menu
- unlock reward card
- level-clear panel
- Trashy and Jimothy character select
- core material language

Use it to judge whether a runtime screen feels like one coherent Trash Dash interface.

## Phase 1 - Buttons and tabs

### Reference

`reference/concept-boards/01-buttons-tabs.png`

### Source sheet

`source-sheets/phase-01-buttons-tabs.png`

### Included assets

- Primary Play button: default, focus, pressed
- Secondary Back button: default, focus, pressed
- Neutral Level Select button
- Neutral Settings button
- Gear icon button
- Back arrow icon button
- Map tab: selected and unselected
- Collection tab: selected and unselected
- Stats tab: selected and unselected
- Locked state bar
- Disabled state bar

### Intended use

Use these as surface and state references for shared button and tab components. Keep button labels dynamic whenever practical. The focus version can be implemented as a separate sprite or reproduced through a shared outline, lift, shadow, and light treatment.

Do not create a different control silhouette for every screen. Reuse the component system.

## Phase 2 - Panels and containers

### Reference

`reference/concept-boards/02-panels-containers.png`

### Source sheet

`source-sheets/phase-02-panels-containers.png`

### Included assets

- Main menu hero backing panel without menu controls
- Generic cardboard content panel
- Blank layered wooden signboard
- Torn notebook-paper panel
- Sticker-style reward card panel
- Open junk-box pause container
- Closed junk-box container
- Cardboard, tape, sticker, bottle-cap, and wood material samples
- Reusable loose tape pieces

### Intended use

Use panels as layered construction sources. Build scalable versions with 9-slice or separate corner, edge, and center pieces. Preserve irregular silhouettes and fasteners while keeping the content area flexible.

Treat the open and closed junk-box images as key visual states for a layered pause-menu animation. Do not simply crossfade between full screenshots if the engine can animate flaps and content independently.

## Phase 3 - HUD, notifications, and alerts

### Reference

`reference/concept-boards/03-hud-notifications-alerts.png`

### Source sheet

`source-sheets/phase-03-hud-notifications-alerts.png`

### Core assets

- health display variants
- bottle-cap, key, and collectible counters
- timer panels
- resource icons
- number glyph reference
- direction arrows
- Bottle Cap +1 toast
- Key Found toast
- Checkpoint Reached toast
- Secret Found toast
- objective tracker and objective states
- Boss Incoming warning
- Low Health warning
- Run warning
- Danger Ahead warning
- status badges
- impact and notification FX
- notification and alert animation-reference strips

### Optional exploratory assets

- mini-map and compass
- character portrait HUD treatments

The optional exploratory assets should only be implemented if the current game design calls for them.

### Intended use

Extract the core HUD shells, icons, and fixed illustrations. Render changing scores, times, counts, objective copy, and progress as runtime content.

The Phase 3 source sheet explores more UI types than the original compact concept board. Do not let its extra logo, character portrait, or presentation decoration override the canonical visual system or character designs.

## Phase 4 - Results, rewards, and Character Select

### Reference

`reference/concept-boards/04-results-character-select.png`

### Source sheet

`source-sheets/phase-04-results-character-select.png`

### Included assets

- Level Clear results panel
- New Record results variant
- New Hat Unlocked reward card
- Character Select board
- Trashy card: unselected and selected
- Jimothy card: unselected and selected
- P1 badge
- Selected check badge
- Pink pointer arrow

### Intended use

Results panels should be decomposed into a shell, headline treatment, metric slots, icons, record badge, and action button. Scores and counts must stay dynamic.

Character cards should be decomposed into card shell, portrait art, name plate, focus treatment, selected treatment, and check badge. Preserve character proportions exactly.

## Motion reference

### `reference/motion/ui-motion-reference.png`

Summarizes the required animation sequences for:

- button hover and press
- toast entrance, hold, and exit
- pause-menu flap-open
- level-clear reveal
- Trashy and Jimothy selection swap

Use the written motion contract and tokens for exact behavior. The board is a visual sequencing reference.

## Region manifest

`manifests/sprite-regions.json` provides generous source crop coordinates for every named region.

These regions are starting points only. They are not runtime anchors, hitboxes, final sprite bounds, or 9-slice guides.
