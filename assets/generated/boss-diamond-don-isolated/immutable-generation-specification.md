# Diamond Don Immutable Generation Specification

Execution: `EXECUTE: boss-diamond-don`  
Contract: `docs/design/trash-dash/manuals/bosses/BOSSFIX.md`, reread in full immediately before execution
Specification status: immutable for this execution batch

## Identity

- Boss: The Diamond Don (`boss.level-06-secret.diamond-don`).
- Canonical visual authority: `docs/design/trash-dash/library/characters/bosses/diamond-don/sprites/reference/boss-diamond-don.png`.
- Accepted extraction source: `docs/design/trash-dash/library/characters/bosses/diamond-don/sprites/animation-source/boss-diamond-don-transparent.png`.
- Locked: towering upright heavyweight charcoal/deep-gray raccoon; black mask; lighter muzzle and cheeks; pale yellow-green reflective eyes; broad black nose; enormous ringed tail; low black fedora/trilby; dirty off-white/gray pinstriped baseball shirt; distressed ambiguous `06`; charcoal armor; layered belts, brown straps, gold buckles/chains; armored gloves; dark trousers; black boots; battered reinforced spiked dark-brown wooden bat; huge forearms, round belly, short powerful legs, wide plantigrade stance; smug controlled theatrical kingpin affect.
- Locked effects: dirty gray-brown shockwaves/rubble, black arcs, pale baseball streaks, yellow stars, smoky violet curse with acid-green accents, skull motifs, subtle green gauntlet indicators, approved baseballs/coins/chains/padlock/dust/mines/minions/hat/bat/detached props/defeat effects.

## Animation

- EMERGE: 9 approved-only references; detached curse symbol -> skull motif -> curse smoke/body materialization -> command settle -> active idle.
- RETREAT: 9 approved-only references; active idle -> intentional command -> curse dematerialization -> detached inactive/exit symbol. No hit, fall, prone, or exhaustion art is used.
- DEFEAT: 9 approved-only references; hit/stagger -> collapse -> prone hold -> rubble settling -> exhausted softened seated post-defeat boss.
- All three classify `EXISTS - COMPLETE`; generation and replacement counts are zero.
- Runtime timing is `UNSET / NOT PROMOTED`; 150 ms GIF cadence is review-only and not gameplay metadata.

## Rendering

- Preserve perspective, scale, lighting, shading, texture, palette, alpha, body/prop relationships, and source order exactly.
- Source/output pixel scale is 1:1. No resize, resampling, rotation, redraw, retouch, cleanup, filtering, or style conversion.
- Output is transparent RGBA with manifest-defined variable rectangles, two pixels of transparent frame padding, and eight transparent atlas-gutter pixels on every side.
- Actor pivots use the largest owned connected component's bottom center; standalone effects/props use the complete visible envelope's bottom center.
- Reviewed rectangular ownership partitions resolve crowded source rows and the right-edge contact while assigning every visible source RGBA pixel exactly once.

## Restrictions and generation scope

- Every physical item is `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`.
- `GENERATE NEW = 0`; `REPLACE UNAPPROVED = 0`.
- Do not add ordinary proportions, a slender body/small tail, clean white suit, crown, cigar, firearm, gold bat, replacement sleeve number, blue/red replacement magic, mascot affect, weapons, anatomy, markings, costume, or damage.
- Do not promote, register, or copy any output into `assets/runtime/`.
