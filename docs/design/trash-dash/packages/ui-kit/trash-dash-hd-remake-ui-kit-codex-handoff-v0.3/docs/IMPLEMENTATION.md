# Trash Dash V2 UI Implementation Rules

## 1. Build components, not screenshots

The concept board is a style reference. Do not recreate the board as one large texture or hard-code screen-sized images.

Each UI element should be constructed from reusable layers and components.

## 2. Asset construction

Recommended separation for a scalable component:

- base material layer
- edge/corner treatment
- fasteners or tape
- shadow
- optional decorative junk
- icon
- dynamic label/value
- focus/selection treatment

Use 9-slice scaling for rectangular panel shells where supported. If 9-slice is unavailable, use separate corners, edges, and center tiles.

Never stretch a decorative raster asset non-uniformly.

## 3. Character Select artwork

Character cards need a predictable artwork window.

Requirements:

- Trashy and Jimothy use the same artwork frame dimensions.
- Art uses contain-style scaling.
- Full silhouette stays visible.
- Feet, ears, hats, weapons, tails, tools, and backpacks must not be clipped.
- Character name is a dynamic label outside the art bounds.
- Selection overlay is independent from the character image.

## 4. Text

Prefer actual runtime text for labels, counts, scores, objectives, settings, and notifications.

Text should not be part of a decorative PNG unless the wording is permanent branded artwork such as a logo.

Support long values without compressing the whole component horizontally.

## 5. Layout

Target the live game's supported viewport system, with 1920x1080 as the design reference.

- anchor important controls to safe areas
- use logical layout containers
- allow extra breathing room around irregular silhouettes
- keep a minimum safe margin of 4 percent near screen edges
- do not position UI by screenshots alone

## 6. Input

All core actions need stable keyboard and controller focus order.

A component's decorative transform must not destroy its hit area or focus target.

When the game is paused, focus should enter the pause menu and return to the previous gameplay context on Resume.

Character Select should support left/right navigation and clear confirmation.

## 7. Audio hooks

Motion primitives should expose optional audio event hooks rather than playing sound internally.

Suggested semantic hooks:

- `ui.focus`
- `ui.press`
- `ui.panel_thud`
- `ui.sticker_peel`
- `ui.cap_clink`
- `ui.stamp`
- `ui.warning_rattle`
- `ui.reward`

This keeps animation reusable and lets audio evolve independently.

## 8. Animation architecture

Create a centralized UI motion helper or animation service that consumes names from `motion.tokens.json`.

Avoid one-off tween literals scattered through scene code.

Desired API shape, adapt to the project's engine:

```ts
motion.play(node, 'td.lift')
motion.play(node, 'td.press')
motion.sequence('levelClear', context)
motion.cancel(node)
motion.setReducedMotion(enabled)
```

The exact implementation can differ, but the named primitives and behavior contracts should stay stable.

## 9. State ownership

Use explicit state models for components instead of inferring state from current sprite scale or alpha.

Examples:

```ts
button.state = 'focused'
characterSelect.selectedCharacter = 'trashy'
levelClear.phase = 'ready'
pauseMenu.state = 'open'
```

Visuals derive from state. Game progression data should not depend on animation callbacks.

## 10. Asset naming

Suggested naming scheme:

```text
ui/material/cardboard_*.png
ui/material/wood_*.png
ui/decor/tape_*.png
ui/decor/sticker_*.png
ui/icon/*.png
ui/component/button_primary_*.png
ui/component/panel_*.png
ui/character-select/trashy_*.png
ui/character-select/jimothy_*.png
```

Use transparent PNG or the engine's preferred equivalent for irregular art.

## 11. Visual QA acceptance criteria

Do not consider a screen complete until it has been tested in actual gameplay rather than only on isolated fixture pages.

Acceptance criteria:

- no cropped character or UI art
- no squashed or stretched textures
- no unexpected transparency fringe
- no overlapping buttons
- no clipped shadows or animated overshoot
- labels stay readable at supported resolutions
- all focus states are visible
- all major animations can be interrupted safely
- result sequence can be skipped safely
- reduced motion works
- character selection clearly distinguishes Trashy and Jimothy

