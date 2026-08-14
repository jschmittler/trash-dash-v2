# Pizza Rat King Immutable Generation Specification

Execution: `EXECUTE: boss-pizza-rat-king`  
Contract: `/Users/jamesschmittler/Desktop/bossfix.md`, reread in full immediately before execution  
Specification status: immutable for this execution batch

## Identity

- Boss: His Greasiness, the Pizza Rat King (`boss.level-03.pizza-rat-king`).
- Canonical visual authority: `docs/design/trash-dash/reference/characters/level-03/sprites/boss-pizza-rat-king.png`.
- Accepted transparent atlas: `docs/design/trash-dash/character-animation/phase-05-codex-integration/phase-04-bosses/final/boss-pizza-rat-king-transparent.png`.
- Locked: enormous obese low sewer-rat silhouette; greasy dark brown-gray/olive-black fur; dirty pale belly; pink segmented tail and paws; large pale-yellow eyes; irregular teeth; bent-fork crown; ragged red-brown mantle; huge dirty silver pizza cutter; canonical pizza, grease, dust, debris, wheel, speed-streak, impact-star, rat-reveal, and crown-detail effects.

## Animation

- EMERGE: 5 approved frame references; off-screen dust cue -> fast right-facing entry -> charge deceleration -> active idle.
- RETREAT: 5 approved frame references; active idle -> charge anticipation -> fast right-facing exit -> off-screen dust cue. It contains no defeated, injured, or unconscious pose.
- DEFEAT: 5 approved frame references; hit reaction -> crash/stunned collapse -> face-down defeated king. The approved rat/crown reveal remains a separate post-defeat state.
- Pose order inside every approved physical state remains unchanged. Required sequences reference isolated approved rectangles and do not duplicate their pixels in the sheet.
- Timing remains `UNSET / NOT PROMOTED`; runtime cadence is not invented before user approval.

## Rendering

- Three-quarter side profile, canonical facing screen-right.
- Source and output scale: exactly 1:1; no resize, rotation, redraw, retouch, filter, or resampling.
- Preserve approved light, shading, texture, palette, alpha, dimensions, internal registration, and ground contact.
- Output: transparent RGBA PNG, manifest-defined variable rectangles, 8 transparent atlas-gutter pixels on every side in addition to transparent extraction padding.
- Actor pivot: largest connected body component ground contact. Standalone effect pivot: visible-envelope bottom center.
- Detached components are assigned to one reviewed body/effect rectangle. The accepted fast-run bridge at source bbox `[950,353,1345,451]` is separated at reviewed source x=1160; every visible RGBA source pixel remains assigned exactly once.

## Restrictions and generation scope

- `GENERATE NEW = 0`; `REPLACE UNAPPROVED = 0`.
- Every physical sprite/support operation is `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`.
- No image generation is used because the approved atlas already supplies every pose/effect needed to compose EMERGE, RETREAT, and DEFEAT.
- No character features, props, damage, effects, palette, anatomy, style, or gameplay scale may change.
- No runtime promotion, runtime registration, collision, encounter, or gameplay edit is authorized.
