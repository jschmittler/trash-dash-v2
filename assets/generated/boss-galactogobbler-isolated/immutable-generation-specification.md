# Galactogobbler Immutable Generation Specification

Execution: `EXECUTE: boss-galactogobbler`  
Contract: `docs/design/trash-dash/docs/game/bosses/BOSSFIX.md`, reread in full immediately before execution  
Specification status: immutable for this execution batch

## Identity

- Boss: Galactogobbler, Hoarder of Worlds (`boss.level-05.galactogobbler`).
- Canonical visual authority: `docs/design/trash-dash/reference/characters/level-05/sprites/boss-galactogobbler.png`.
- Accepted transparent atlas: `docs/design/trash-dash/character-animation/phase-05-codex-integration/phase-04-bosses/final/boss-galactogobbler-transparent.png`.
- Locked: small lavender-to-deep-violet alien; bulbous hairless head; two enormous glossy black-purple oval eyes; tiny nostrils; wide subordinate-to-maw mouth; compact limbs and rounded fingers; cyan luminous cylindrical canister; nearly spherical asteroid/electronics/cosmic-garbage shell; circular aperture; orbiting scraps; curious, hungry, frightened, uncertain, intelligent affect.
- Locked effects: violet/lavender/magenta-white/cyan/deep near-black gravity, portals, orbit paths, rubble, meteors with limited orange-yellow heat, black tied emblem bags, canister light, smoke, wire, machinery, and reassembly effects already present in the accepted atlas.

## Animation

- EMERGE: 17 approved references; dispersed emblem-bag state -> bag/body reveal -> approved rubble and shell reassembly -> active idle.
- RETREAT: 17 approved references; active idle -> intentional shell recall -> alien/canister -> emblem-bag inactive/exit state. It is reversible and does not end in a defeat hold.
- DEFEAT: 20 approved references; hit -> mass shedding -> exposed core -> shell burst/rubble -> living alien beside cyan canister.
- Every sequence uses references to isolated approved physical sprites; no pixels are duplicated in the atlas.
- Timing is `UNSET / NOT PROMOTED`; runtime cadence and event frames are intentionally not invented before approval.

## Rendering

- Preserve the accepted perspective, source scale, lighting, shading, texture, palette, alpha, and ground/contact relationships exactly.
- Source and output pixel scale are 1:1. No resize, rotation, redraw, retouch, filtering, cleanup, or resampling is permitted.
- Output is transparent RGBA with manifest-defined variable rectangles and 8 transparent atlas-gutter pixels on every side, in addition to 2 transparent extraction-padding pixels.
- Actor/object pivots use the largest owned connected component's bottom center. Effect/rubble pivots use the complete visible envelope's bottom center.
- Crowded source rows are resolved by reviewed rectangular ownership partitions. Those partitions are layout-only isolation seams; every original visible RGBA pixel is retained exactly once.

## Restrictions and generation scope

- `GENERATE NEW = 0`; `REPLACE UNAPPROVED = 0`.
- Every physical output is `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`.
- Do not add a giant eyeball, tentacles, spacesuit, clean sphere, rock-only shell, missing alien/core, demon characterization, cockpit, green poison, conventional fire magic, primary blue lightning, weapons, anatomy, markings, damage, or costume elements.
- Do not permanently explain the emblem-bag function.
- Do not promote, register, or copy any output into `assets/runtime/`.
