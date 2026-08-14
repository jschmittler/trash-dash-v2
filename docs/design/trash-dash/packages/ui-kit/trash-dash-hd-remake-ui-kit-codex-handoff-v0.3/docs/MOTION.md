# Motion and Animation Contract

Motion is a first-class part of the Trash Dash UI Kit. Components must not invent arbitrary timing and easing during implementation.

Use `tokens/motion.tokens.json` as the shared source for primitives and defaults. Use `reference/motion/ui-motion-reference.png` as the visual sequencing guide.

## Motion personality

The interface should feel physical, handmade, energetic, and slightly mischievous.

Preferred verbs:

- lift
- press
- squash
- pop
- wiggle
- slide
- peel
- stamp
- slam
- shake
- swing
- flap
- count up
- reveal
- burst

## Energy levels

### Micro

Buttons, tabs, counters, focus, and selected-state feedback.

Target duration: 80 to 180 ms.

### Mid

Notifications, objective updates, alerts, unlocks, and pause transitions.

Target duration: 180 to 700 ms.

### Hero

Main-menu arrivals, boss alerts, level clear, new records, and rare rewards.

Target sequence: 700 to 1700 ms.

Hero sequences must be skippable or accelerable when repeated.

## Required sequence 1 - Button hover and press

Timeline guidance:

- 0.00 s: idle
- 0.10 s: hover or focus lifts 6 to 8 px and slightly brightens
- 0.18 s: press squashes vertically by about 20 to 25 percent, with a small downward movement
- 0.30 s: release stamps down, overshoots upward by 6 to 8 px, then settles

The logical action should fire at input or at a very short intentional press point. Do not wait for the decorative bounce to finish.

## Required sequence 2 - Notification pop-in and pop-out

Timeline guidance:

- 0.00 s: offscreen or hidden
- 0.20 s: scale from about 80 percent to about 110 percent, then settle to 100 percent
- 0.20 to 1.20 s: readable hold with an optional 2 to 3 px float
- 1.70 s: drift right or upward, scale toward 80 percent, and fade

Stacked notifications need queue and replacement rules so they never overlap unpredictably.

## Required sequence 3 - Pause-menu flap-open

Timeline guidance:

- 0.00 s: game state is paused and box is closed
- 0.18 s: flaps swing open approximately 90 degrees with easing
- 0.36 s: menu controls slide upward about 30 px into the box
- 0.60 s: controls settle top to bottom with one small bounce

Input focus should land on Resume as soon as controls are usable. The player should not wait for secondary decorative motion.

## Required sequence 4 - Level-clear reveal

Timeline guidance:

- 0.00 s: results panel starts below the viewport
- 0.25 s: panel slams upward with a slight overshoot
- 0.25 to 1.15 s: score and time count up with quick ticks
- 1.15 to 1.70 s: reward icons bounce in one by one from left to right
- final: new record or reward sticker stamps into place, Continue becomes available

Level completion data must be committed before animation starts. Skipping the sequence must set all visuals to the final state without repeating reward logic.

## Required sequence 5 - Character Select swap

Timeline guidance:

- 0.00 s: current character card is active
- 0.18 s: outgoing card slides about 30 px left with no more than 2 degrees rotation
- 0.36 s: incoming card slides in from the right
- 0.54 s: selected card lands at about 105 percent scale, then settles to 100 percent

Selection state must be committed separately from animation. Rapid left and right input should cancel or blend safely from the current visual state.

## Standard compositions

### Button focus

`td.lift` followed by optional `td.wiggle`

### Button press

`td.press`, perform action, then settle

### Toast

`td.pop`, readable hold, `td.peelOut`

### Warning

`td.slam`, `td.shake`, hold, then `td.swing` or exit

### Objective complete

Expand tracker, `td.stamp` status, brief hold, collapse

### Pause open

Freeze world, slide box in, `td.flapOpen`, reveal controls, focus Resume

### Character selected

`td.lift`, selected marker `td.stamp`, optional short character reaction

### Unlock

`td.cardReveal`, unwrap or peel, `td.stamp` New badge, optional `td.celebrationBurst`

### Level clear

`td.slam`, headline `td.stamp`, metrics populate, `td.countUp`, reward or record `td.stamp`, Continue ready

## Interruption rules

Animation must be state-driven, not fire-and-forget.

When input changes the target state during an animation:

- cancel or blend the old tween cleanly
- animate from the current visual transform
- never leave partial scale, rotation, alpha, or disabled input
- do not queue decorative focus animations faster than focus can move
- do not allow pause open and close animations to fight each other

## Reduced motion

Support the platform preference and an in-game setting where practical.

When reduced motion is enabled:

- remove shake, swing, wiggle, slam, large spatial movement, and particle bursts
- replace entrances with short opacity and minimal scale changes
- resolve hero sequences quickly to their final state
- preserve focus, pressed, selected, warning, and completion clarity
- keep audio behavior independent from motion preference

Reduced motion must never remove information.

## Audio hooks

Expose semantic hooks instead of hard-coding audio inside visual components:

- `ui.focus`
- `ui.press`
- `ui.panel_thud`
- `ui.sticker_peel`
- `ui.cap_clink`
- `ui.stamp`
- `ui.warning_rattle`
- `ui.reward`

## Motion QA

Test:

- 30 fps degradation
- 60 fps behavior
- rapid controller focus changes
- button mashing
- repeated pause and resume
- notification bursts
- skipping level-clear animation
- rapid Trashy and Jimothy switching
- viewport resize during motion
- reduced-motion mode
