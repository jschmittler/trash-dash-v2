# Trash Dash HD Remake - Enemy Master Specification Contract

**Status:** APPROVED / LOCKED CANON FRAMEWORK  
**Applies to:** Level 1 through Secret Level 6 and all future enemies unless James explicitly revises the contract.

## Purpose

This contract is the permanent design-control framework for every Trash Dash HD Remake enemy. It exists so implementation, animation, level placement, balancing, collision, effects, and future iteration remain aligned to approved concept art and the overall Gunk story.

Approved concept art and sprite sheets are the visual source of truth. This written canon explains, constrains, and extends those designs. It does not grant permission to redesign them.

## Required 15-section structure

Every enemy specification uses this exact order:

1. Identity and Gameplay Role
2. Placement and Movement Class
3. Size, Scale, and Silhouette
4. Immutable Visual Anatomy
5. Color, Material, and Surface Treatment
6. Character Personality and Intent
7. Gunk Transformation and Backstory
8. Movement and Navigation Behavior
9. Attacks, Telegraphs, and Combat Behavior
10. Entry, Exit, Hit, and Defeat Behavior
11. Animation State Inventory
12. Animation Construction and Modification Rules
13. Collision and Gameplay Readability
14. Effects and Environmental Interaction
15. Character Validation Checklist

Do not change this structure for future enemies unless James explicitly approves a contract revision.

## Visual Canon vs Behavior / Lore Specification

### Visual Canon

Visual Canon is directly established by approved concept artwork and sprite sheets. It includes anatomy, silhouette, equipment, colors, markings, materials, proportions, and other visible identity characteristics.

Visual Canon is immutable during ordinary implementation work.

### Behavior / Lore Specification

Behavior / Lore Specification includes approved gameplay behavior, personality, attacks, movement, telegraphs, vulnerability windows, environmental interaction, animation behavior, and Gunk history built around the visual design.

Behavior / Lore may be tuned only when the requested change does not erase the enemy's canonical identity or approved player decision.

## Source hierarchy

When making an enemy-related decision, use this order of authority:

1. Explicit new instruction from James.
2. Approved Enemy Master Specification.
3. Approved canonical concept art / sprite sheet.
4. Existing implementation that is already canon-compliant.
5. Derived runtime assets and tests.
6. Historical or legacy implementation.

Existing code or sprites do not override canon simply because they already exist.

If written canon and approved concept art appear to conflict, flag the conflict. Do not silently invent a redesign.

## Immutable generation rule

> Never use a text description as the sole source for generating a new animation frame when approved visual references exist.

Every new frame must be derived from one or more approved visual anchor frames.

Required workflow:

`approved sheet -> isolate canonical anchor frames -> define pose change -> create intermediate/new pose -> restore canonical anatomy and surface details -> add effects separately -> compare against anchors -> animation playback test -> gameplay-scale validation`

The correct framing for any AI-assisted art task is:

> Preserve the exact approved character design. This is animation expansion, not character generation or character redesign. Resolve ambiguity in favor of the supplied canonical reference artwork.

## No character drift

Do not solve animation or implementation problems by silently:

- changing anatomy
- changing eye count
- changing limb count
- changing wing count
- changing feet or paw structure
- changing fur, feather, scale, shell, or skin patterns
- changing approved colors
- changing markings, letters, or numbers
- removing canonical equipment
- adding unapproved equipment or weapons
- changing prop scale or construction
- changing silhouette
- non-uniformly stretching sprites
- replacing a canonical container or shell with a generic substitute
- randomly regenerating surface details between frames

A redesign requires an explicit canon-revision request.

## Animation rules

### Anchor frames

Use approved frames immediately before and after a new intermediate frame whenever possible.

### Stable anatomy

Occlusion does not remove anatomy. Hidden limbs, wings, tails, and appendages remain present even if not visible in one frame.

### Stable markings

Track large fur patches, feather markings, scale patterns, stripes, dents, rivets, lettering, jersey numbers, helmet markings, and other identifying details across frames.

### Secondary motion

Use appropriate follow-through for tails, ears, wings, antennae, clothing, straps, backpacks, cargo, lanterns, loose equipment, hoses, debris, and other secondary masses.

### Aspect ratio

Never horizontally or vertically squash a canonical sprite to fit an animation box. Scale uniformly. Enlarge frame bounds when necessary.

### Effects

Keep VFX separate from the base character wherever technically practical. Motion blur, dust, slime, gas, electricity, web, venom, speed streaks, glow, debris, and impact effects should not require permanent repainting of the character.

## Placement rules

Before placing an enemy, confirm its canonical placement and movement class.

Possible classifications include:

- Ground
- Ground / low-profile
- Flying
- Floating
- Wall-clinging / surface-clinging
- Ground with ballistic airborne movement
- Machine-bound environmental operator
- Concealed / environmental disguise
- Armored / exposed state

Do not place a ground enemy in a position that requires unapproved flight or wall movement. Do not treat a temporary jump, pounce, dive, bounce, or launch as evidence that the enemy is a sustained flying enemy.

Enemy placement must support the intended attack path, telegraph, recovery, vulnerability, and player decision.

## Core gameplay identity rule

Every enemy has a canonical player-pressure pattern. Tuning may change numerical parameters, but it may not casually remove:

- mandatory telegraphs
- vulnerability windows
- placement class
- core attack type
- intended recovery
- state-dependent protection
- primary combat decision

Difficulty should come from timing, spacing, combinations, speed within fair bounds, encounter composition, and environment, not from deleting readability.

## Collision rules

Never derive collision solely from PNG transparency bounds.

Author state-appropriate collision intentionally.

Decorative extremities and VFX are not automatically physical collision. Examples include:

- wing tips
- tails
- antennae
- whiskers
- transparent glow
- speed streaks
- dust
- liquid trails
- weapon arcs
- web trails
- warning rings

Attack colliders should activate only in approved active frames.

When an enemy changes state substantially, such as curled vs exposed, shielded vs vulnerable, flying vs ground skim, inflated vs popped, or machine-bound vs ejected, use state-appropriate collision.

## Props and equipment

Canonical props must have explicit states such as:

- equipped
- held
- stored
- attached
- airborne
- on ground
- destroyed
- hidden by perspective
- released

A single prop may not exist in contradictory states simultaneously.

When a prop separates from a character, it should become an independent asset or gameplay object where appropriate.

## Facing and mirroring

Do not blindly mirror asymmetric art if it causes:

- letters to reverse
- jersey numbers to reverse
- equipment to switch sides incorrectly
- unique markings to move incorrectly

If runtime mirroring is used, document how readable markings and asymmetric equipment are preserved.

## Transparent-material rules

Transparent glass, gel, wings, and machine structures require alpha validation.

Check for:

- white matte
- dark matte
- colored fringe
- source background contamination
- clipped highlights
- missing interior lines
- opaque patches
- excessive transparency that destroys readability

## Environmental interaction

Effects must reflect the actual material and level context.

Examples:

- dirt should create dust, pebbles, and trenches
- grass should create softer soil and grass fragments
- concrete should create scrape effects with little soil
- metal can create sparks
- low gravity requires longer debris arcs and slower settling
- wall-clinging requires true surface contact

Do not use one generic impact or movement effect for every environment.

## Vulnerability states

Canonical vulnerability states are gameplay states, not decorative reactions.

They require:

- an entry condition
- a readable animation
- altered behavior or defense
- appropriate collision
- a usable player opportunity
- an explicit recovery transition

## Canon revision protocol

If James explicitly requests a change that conflicts with locked canon:

1. Identify the current canonical rule.
2. Treat the request as a potential canon revision, not an implementation exception.
3. Confirm the intended new behavior/design if ambiguity remains.
4. Update the relevant level specification.
5. Increment the Enemy Master Specification version.
6. Add the change to `CHANGELOG.md`.
7. Update `README.md`, `ASSET_MANIFEST.md`, and reference art if affected.
8. Then update implementation.

Never revise canon because a shortcut would be easier to implement.

## Validation contract

All visual and animation work must be reviewed:

1. At source resolution.
2. Frame by frame.
3. At intended playback speed.
4. At actual gameplay scale.
5. Against the intended level background.
6. With collision visualization where applicable.
7. During state transitions.
8. During interaction with props and environment.
9. During uninterrupted gameplay.

Static sprite-sheet review alone is insufficient.

## Final global canon rule

The concept art defines what the enemies are.

The Enemy Master Specification defines how those approved characters move, behave, attack, react, fail, recover, occupy the world, and connect to the Gunk story.

Implementation adapts to canon first. Canon does not silently adapt to implementation.
