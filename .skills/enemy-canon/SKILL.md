---
name: enemy-canon
description: Use whenever creating, modifying, debugging, reviewing, animating, placing, balancing, or implementing Trash Dash enemies, enemy encounters, enemy props, enemy VFX, enemy collision, or enemy behavior. Enforces the approved Enemy Master Specification and concept-art canon.
---

# Enemy Canon Workflow

## 1. Identify the affected enemy

Determine:

- level
- canonical enemy name
- requested change
- files likely involved

If multiple enemies are affected, repeat this workflow for every enemy.

## 2. Load canon before editing

Read:

1. `docs/design/trash-dash/manuals/enemies/README.md`
2. The relevant `LEVEL_XX.md` file in that same directory (e.g. `LEVEL_01.md`)
3. Relevant rules in `docs/design/trash-dash/manuals/enemies/ENEMY_MASTER_CONTRACT.md`
4. The enemy's entry in `docs/design/trash-dash/manuals/enemies/ASSET_MANIFEST.md`
5. Canonical reference art in `docs/design/trash-dash/packages/imported-source/trashy/enemy-canon/reference-art/`

Do this before modifying code, configuration, levels, or assets.

## 3. Inspect existing implementation

Locate all relevant:

- enemy definitions/configuration
- AI behavior
- movement logic
- animation state machine
- sprite/source assets
- runtime exports
- collision
- VFX
- props/equipment
- level placements
- encounter configuration
- tests
- visual QA tooling

Do not assume existing implementation is canonical.

## 4. Compare implementation to canon

Check at minimum:

- silhouette
- anatomy
- palette
- markings
- equipment
- placement class
- movement
- attack
- telegraph
- vulnerability
- animation states
- collision
- VFX
- environmental interaction
- Gunk/story intent when relevant

Classify differences as:

- `IMPLEMENTATION BUG`
- `MISSING IMPLEMENTATION`
- `CANON-COMPLIANT VARIATION`
- `POSSIBLE CANON CONFLICT`

Never silently resolve `POSSIBLE CANON CONFLICT` by rewriting canon.

## 5. Plan the change

Prefer the smallest coherent implementation that satisfies both the user's request and approved canon.

### Animation work

- Start from approved anchor frames.
- Preserve aspect ratio.
- Preserve anatomy.
- Preserve equipment.
- Preserve surface markings.
- Preserve approved colors/materials.
- Preserve stable roots and pivots.
- Keep VFX separate where practical.
- Validate frame continuity.
- Never solve motion by non-uniform sprite stretching.

### Placement work

- Confirm placement/movement class.
- Confirm required ground, wall, air, perch, or machine context.
- Confirm sufficient attack path.
- Confirm telegraph visibility.
- Confirm recovery/vulnerability space.
- Avoid unwanted overlap.
- Avoid invalid z-ordering.
- Avoid placing enemies within geometry that contradicts canonical grounding.
- Ensure the placement supports the enemy's intended player decision.

### Balancing work

Preserve:

- mandatory telegraphs
- vulnerability windows
- attack identity
- placement class
- recovery behavior
- state-dependent defense

Prefer tuning:

- timing within fair bounds
- spacing
- encounter combinations
- cooldowns
- numerical speed/damage/health
- environment

rather than deleting canonical readability.

## 6. Implement

Do not modify locked canon documentation unless the user explicitly requests a canon revision.

If implementation conflicts with canon, fix implementation by default.

## 7. Validate

Run relevant automated tests.

Run the canon integrity check when the task could have touched canon files or reference art:

```bash
python3 tools/verify/audit_canonical_assets.py
```

For visual/animation work also validate:

- source resolution
- frame sequence
- gameplay scale
- actual background
- state transitions
- grounding
- clipping
- transparency edges
- aspect ratio
- prop continuity
- letters/numbers/markings
- collision visualization
- uninterrupted gameplay

For placement validate:

- no invalid platform/geometry overlap
- no unwanted prop overlap
- correct ground/wall/flying/floating classification
- sufficient attack path
- sufficient recovery path
- no unfair off-camera attack without intended telegraph
- accessible vulnerability state

## 8. Report canon compliance

At completion include:

### Canon consulted

List the enemy specification and reference art used.

### Changes made

Briefly describe implementation.

### Canon checks passed

List important rules confirmed.

### Remaining deviations

List any known deviations.

If none, state:

`No known enemy-canon deviations remain.`

# Canon revision protocol

If the user explicitly requests a visual, behavioral, story, or gameplay change that conflicts with approved canon:

1. Identify the current canonical rule.
2. Treat the request as a canon revision.
3. Clarify only if the intended revision is genuinely ambiguous.
4. Update the relevant specification after intent is clear.
5. Increment the Enemy Master Specification version.
6. Add an entry to `docs/design/trash-dash/manuals/enemies/CHANGELOG.md`.
7. Update `docs/design/trash-dash/manuals/enemies/README.md`, `ASSET_MANIFEST.md`, and reference art where affected.
8. Then update implementation.

Never create a canon revision merely because implementation would be easier another way.
