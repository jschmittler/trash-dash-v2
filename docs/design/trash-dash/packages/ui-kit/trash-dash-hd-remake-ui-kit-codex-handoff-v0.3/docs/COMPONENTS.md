# Trash Dash V2 UI Component Contracts

## Shared component rules

Every interactive component must support mouse, keyboard, and controller input where the runtime supports those modes. Touch support should use the same visual state model when applicable.

Do not bake dynamic text into decorative PNGs. Build the visual shell from scalable layers, then render labels and values independently.

Raster artwork must preserve its native aspect ratio. Never solve layout constraints by changing width and height independently.

Use a stable hit target even if the decorative shape is irregular. The visible object can wobble or rotate without moving the logical interaction region enough to make input unreliable.

### Shared interaction states

- Default: available but idle.
- Hover: pointer-only enhancement.
- Focus: strong controller and keyboard state, never color-only.
- Pressed: immediate physical compression.
- Selected: persistent state with outline, badge, arrow, sticker, check, or positional emphasis.
- Disabled: visually flattened and clearly unavailable.
- Locked: communicates unavailable status and preserves a reason affordance if the game provides one.

## 1. Main Menu Hero Panel

**ID:** `td.menu.hero`

### Anatomy
- Trash Dash title or logo zone
- physical backing surface
- primary navigation stack
- decorative junk layers
- optional character reaction zone
- low-priority legal/version region

### Behavior
- Play is the dominant action.
- Level Select and Settings use lower visual weight.
- Ambient motion may occur after an idle delay, but it must stop or defer as soon as the player interacts.
- Decorative layers may parallax slightly, but the menu labels must remain crisp and stationary enough to read.

### Motion
- Whole panel may enter with `td.slideIn`.
- Focused controls use the standard button motion.
- Ambient junk can use a low-amplitude variation of `td.wiggle` no more than occasionally.

## 2. Primary Button

**ID:** `td.button.primary`

### Anatomy
- scalable physical shell
- label
- optional icon
- focus outline
- shadow layer
- optional decorative fastener

### Behavior
- Hover or focus: `td.lift`, optionally followed by a subtle `td.wiggle`.
- Press: `td.press` immediately on input down.
- Release: spring back to focused or default state.
- Never delay the actual action until the decorative rebound completes.

## 3. Secondary Button

**ID:** `td.button.secondary`

Use the same interaction grammar as Primary with less visual weight and little or no wiggle.

## 4. Tab Navigation

**ID:** `td.navigation.tabs`

### Anatomy
- parent rail or attached surface
- tab label
- optional icon
- selected treatment
- content relation indicator

### Behavior
- Selected tab physically comes forward or overlaps the parent surface.
- Tab content can use `td.pageShift`.
- Do not animate the entire screen for every tab change.

## 5. Small Notification

**ID:** `td.notification.toast`

### Variants
- Pickup: sticker or icon-backed pop.
- Information: paper scrap.
- Milestone: stamped card.
- Currency: bottle-cap treatment.

### Behavior
- One idea per notification.
- Keep copy short.
- New toasts can queue, stack, or coalesce depending on frequency.
- Identical rapid pickup notifications should aggregate rather than spam the player.

### Motion
- Enter with `td.pop` or a light `td.slideIn`.
- Exit with `td.peelOut`.
- Frequent toast sequences should remain under the frequent-feedback duration budget.

## 6. Warning Alert

**ID:** `td.alert.warning`

### Behavior
Use only for time-sensitive or high-priority information.

### Motion sequence
1. `td.slam`
2. brief `td.shake`
3. readable hold
4. optional `td.swing` settle or fast exit

Do not repeatedly shake the full camera for routine UI warnings. The UI element itself should carry most of the impact.

## 7. Objective Tracker

**ID:** `td.hud.objectives`

### Anatomy
- Objectives heading
- objective rows
- status mark
- optional progress value

### Behavior
- Resting state stays compact.
- Update expands briefly, then settles.
- Completion uses `td.stamp` and a custom check or scribble.
- Do not rely on a green check alone. Completed text treatment should also change.

## 8. Pause Menu, Junk Box

**ID:** `td.menu.pause`

### Anatomy
- junk-box shell
- lid/flap layers
- navigation stack
- optional decorative objects

### Behavior
- Freeze gameplay before the opening sequence.
- Resume is first and most prominent.
- Exit Level uses destructive styling and should not sit on the same rapid confirm path as Resume.
- Interactive controls become usable as soon as they reach their readable resting positions.

### Motion sequence
1. freeze gameplay
2. box enters
3. flaps use `td.flapOpen`
4. controls settle
5. focus goes to Resume

Close in reverse, but Resume should not wait for every decorative object to finish settling.

## 9. Unlock Reward Card

**ID:** `td.reward.unlock`

### Anatomy
- hero item art
- NEW badge
- item name
- reward category
- optional support copy
- dismiss/continue action

### Motion
Common rewards use `td.cardReveal` and `td.stamp`.
Rare rewards may add `td.celebrationBurst`.
Do not make every unlock equally theatrical.

## 10. Level Clear Results Panel

**ID:** `td.results.levelClear`

### Anatomy
- celebration headline
- score
- time
- collectibles
- objectives
- rank or completion quality
- unlocks
- Continue action

### Default sequence
1. level victory pose or gameplay beat
2. results board enters using `td.slam`
3. headline uses `td.stamp`
4. collectible slots populate
5. score uses `td.countUp`
6. bonus or record sticker uses `td.stamp`
7. Continue becomes fully emphasized

The player may skip after the initial impact. Skip must immediately populate the final numbers and states without breaking progression logic.

## 11. Character Select

**ID:** `td.character.select`

### Required characters
- Trashy
- Jimothy

### Anatomy
- Choose Your Character heading
- Trashy card
- Jimothy card
- character artwork
- character name
- selected marker
- player marker when relevant
- confirmation action or direct-confirm behavior

### Selection treatment
The selected card must use several signals together:
- heavier outline
- lifted card position
- selected badge or check
- arrow or pointer
- stronger material/color treatment

Do not use color as the only differentiator.

### Motion
- Focus uses `td.lift`.
- A tiny `td.wiggle` can reinforce personality.
- Confirm uses `td.stamp` on the selected badge and a short character reaction if character animation assets are available.
- Character reaction must not hold up level loading.

### Character art rule
Trashy and Jimothy art must fit inside a defined artwork safe zone with `object-fit: contain` behavior or equivalent. Never crop body parts to fill the card.

