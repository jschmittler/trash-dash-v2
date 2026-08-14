# Codex Prompt: Import and Integrate Trash Dash Character Animation Sources

You are working in the Trash Dash game repository. The supplied Phase 05 package is the canonical approved source for playable characters, common enemies, and bosses.

## Non-negotiable visual contract

- Approved transparent atlases and their branded source references are visual truth.
- These are variable-canvas source atlases. Do not use equal grid slicing or force frames into 128 x 128, square, or uniform cells.
- Preserve the original aspect ratio, complete silhouette, weapons, tails, wings, projectiles, props, motion trails, impact effects, transformations, and defeat poses.
- Do not stretch, squash, crop, redraw, invent, or procedurally replace approved art.
- Keep characters and effects on true alpha. Remove no intentional character color while cleaning residue.
- Separate detached projectiles, props, and effects from character frames when they need independent timing or movement.
- Collision geometry is authored independently from transparent pixel bounds.

## Stage 0: Inspect before changing anything

1. Read the repository `AGENTS.md`, README, project rules, existing skills, asset conventions, animation systems, engine configuration, and test commands.
2. Inspect `git status` and preserve all unrelated user changes.
3. Identify the engine and renderer actually used by the project. Do not assume Godot, Phaser, Unity, or another framework from the package alone.
4. Locate existing character, enemy, boss, animation, collision, z-order, and visual-audit systems.
5. Report the proposed file destinations, code paths to change, validation commands, and any conflicts before implementation.

## Stage 1: Canonical source import

1. Verify the four archives against `qa/SHA256SUMS`.
2. Install the package documentation and approved source files beneath `docs/design/trash-dash/character-animation/` or the repository’s established equivalent.
3. Merge with existing documentation. Never overwrite unrelated design files or delete legacy assets during import.
4. Preserve the Phase 01 through 04 package identity and original manifests.
5. Build an import inventory using `ASSET_MAP.md` and report every missing, duplicate, or conflicting asset.
6. Stop after this audit. Do not begin runtime extraction until the inventory is complete and all 36 canonical atlas IDs resolve.

## Stage 2: Variable-frame extraction

For each atlas:

1. Inspect the approved branded reference and the cleaned transparent atlas side by side.
2. Identify animation groups and their exact source order. Do not infer frame order from filename sorting alone.
3. Extract each pose by connected visual bounds plus a deliberate transparent margin. Do not use equal-width slicing.
4. Give every frame its own rectangle, pivot, duration, visual offset, events, attachments, hitboxes, and hurtboxes using `FRAME_METADATA_SCHEMA.json` or an engine-native equivalent with the same information.
5. Use a consistent ground-contact pivot for grounded states. Use a stable body-center pivot for flight and hover states. Do not let frame dimensions move the character’s feet or body center between frames.
6. Keep attack anticipation, active, follow-through, recovery, hit, stun, defeat, and reveal states distinct.
7. Extract projectiles, detached weapons, hazards, summons, splashes, dust, sparks, rings, trails, and impact bursts as independent runtime assets when appropriate.
8. Preserve boss phase changes, armor or harness changes, enraged states, transformations, defeat sequences, and reveal forms as explicit state-machine states.
9. Generate contact sheets and transparent playback previews for every asset. Compare them visually to the approved source before integration.

## Stage 3: Runtime integration

1. Integrate one representative asset from each class first: playable character, grounded enemy, flying enemy, projectile enemy, and boss.
2. Validate the representatives in normal gameplay before scaling the extraction workflow to the full roster.
3. Maintain aspect ratio at every resolution and viewport. Never apply independent X and Y scaling.
4. Author collision separately from image bounds. Keep hurtboxes stable and gameplay-sized, and activate hitboxes only during committed attack frames.
5. Ground all grounded characters on their pivots. No floating, sinking, or vertical jitter.
6. Keep flying enemies stable around their body-center pivots. Do not force walk or run states onto flying characters.
7. Use explicit render layers and z-order. Characters, projectiles, foreground props, platforms, and effects must not accidentally pass behind or through unrelated geometry.
8. Keep gameplay objects outside platform interiors unless they are intentionally embedded. Prevent invisible collision and visual overlap.
9. Map animation events to gameplay timing, including projectile release, melee contact, landing impact, vulnerability windows, boss phase transitions, and defeat completion.
10. Do not remove old runtime assets until the replacement is proven in gameplay and references have been updated.

## Stage 4: Mandatory gameplay visual QA

Static fixtures and contract tests are not sufficient. Perform uninterrupted gameplay validation at every level and boss encounter.

Validate:

- character proportions and aspect ratio
- grounded contact and stable flight pivots
- readable idle, movement, anticipation, attack, recovery, hit, stun, defeat, and boss-transition motion
- correct frame order and no duplicate-standing motion in walk or run cycles
- no cropped weapons, tails, wings, projectiles, effects, or defeat poses
- no chroma residue, dark halos, white boxes, clipped sprays, or accumulated transparent GIF frames
- correct projectile release and impact timing
- stable collision and no invisible walls
- correct z-order with platforms and foreground elements
- no unintended overlaps or clustered props
- responsive behavior across supported viewport sizes
- complete boss phase changes, vulnerability windows, defeats, and reveals

Capture screenshots or short recordings from normal gameplay for every level and boss. Treat the observed playthrough as authoritative when it conflicts with static tests.

## Stage 5: Required deliverables

- canonical import inventory for all 36 atlases
- one metadata file per runtime character, enemy, and boss
- extracted frame or atlas assets using variable source rectangles
- animation state maps and event timing
- collision, pivot, scale, and z-order documentation
- automated alpha, bounds, metadata, and state-completeness tests
- per-level gameplay screenshots or recordings
- updated visual-audit document listing every issue found and fixed
- final report with remaining limitations clearly marked incomplete

## Stop conditions

Stop and report instead of guessing when:

- an atlas or reference is missing or corrupt
- source frame order is ambiguous
- a required state exists in the reference but cannot be isolated cleanly
- existing runtime conventions conflict with the metadata contract
- an implementation decision would alter gameplay balance or boss behavior
- environment or foreground assets are required but their separate production package has not yet been delivered

Do not claim completion while any required state, representative gameplay check, level playthrough, boss phase, visual defect, or deliverable remains unverified.

## Separate asset tracks

Environment concepts, parallax close, middle, and far layers, ground, platforms, foreground props, hazards, collectibles, UI, cutscenes, and dialog are outside this character integration package. Import those only from their own approved production handoffs.
