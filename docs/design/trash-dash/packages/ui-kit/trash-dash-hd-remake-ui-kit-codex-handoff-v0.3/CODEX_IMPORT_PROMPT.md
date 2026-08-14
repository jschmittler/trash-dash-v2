# Codex Prompt - Import and Consume the Trash Dash HD Remake UI Kit

I am attaching the folder `trash-dash-hd-remake-ui-kit-codex-handoff-v0.3`.

Install it into the Trash Dash repository as the canonical UI design and source-art package, then prepare the approved assets for runtime use without losing the original source material.

## 1. Inspect before changing anything

Inspect:

- repository root and git status
- root `AGENTS.md`
- existing `.skills/` or equivalent skills
- current UI architecture
- asset-loading conventions
- input and focus system
- animation or tween utilities
- current menu, HUD, notification, pause, results, and Character Select implementations
- current runtime asset directories

Do not delete, overwrite, or flatten existing assets blindly.

## 2. Install the package

Prefer this canonical location:

```text
docs/design/trash-dash/ui-kit/
```

If the repository already has a clearly established Trash Dash design-source root, install the package there instead and report the final path.

Preserve the package structure.

Copy source sheets and concept boards as immutable references. Do not optimize or rewrite the only copies.

## 3. Read in order

Read these files before importing runtime assets:

1. `docs/APPROVAL_AND_AUTHORITY.md`
2. `docs/UI_KIT_BRIEF.md`
3. `docs/ASSET_CATALOG.md`
4. `docs/ASSET_EXTRACTION_AND_RUNTIME_USE.md`
5. `docs/COMPONENTS.md`
6. `docs/MOTION.md`
7. `docs/IMPLEMENTATION.md`
8. `tokens/ui.tokens.json`
9. `tokens/motion.tokens.json`
10. `ui-kit.manifest.json`
11. `manifests/asset-manifest.json`
12. `manifests/sprite-regions.json`
13. `reference/concept-boards/00-overall-ui-kit.png`
14. the matching phase concept boards and source sheets
15. `reference/motion/ui-motion-reference.png`

The overall brief and concept boards define the visual language. Source sheets are extraction sources, not full-screen textures.

## 4. Visual-language contract

The interface is **Reclaimed Playground**.

It should feel built from the Trash Dash world using:

- corrugated cardboard
- painted reclaimed wood
- torn paper
- stickers
- duct tape and masking tape
- screws, nails, and paper clips
- bottle caps
- battered signs
- hand-painted lettering and marks

The UI may be visually playful and imperfect, but it must be functionally clear and consistent.

Do not introduce generic glass panels, corporate app cards, glossy mobile-game chrome, sci-fi surfaces, unrelated comic branding, or smooth gradient panels that ignore the source material.

Some concept boards show the working label Trash Dash V2. The current game name is Trash Dash HD Remake. Do not replace current branding with V2 or with alternate logos found inside exploratory sheets.

## 5. Asset authority

Use this order when sources disagree:

1. written contracts, tokens, and approval rules
2. overall UI Kit concept board
3. matching phase concept board
4. matching phase source sheet
5. implementation judgment that preserves the system

The earlier off-style Phase 4 sheet is not included and must not be recreated.

## 6. Stage and validate source assets

Before extracting:

- run `python tools/validate_ui_package.py --package-root <installed-path>`
- verify all hashes and dimensions
- report missing or corrupt files
- create a staging directory outside production runtime assets
- preserve originals unchanged

Use `manifests/sprite-regions.json` as crop guidance.

Start with raw crops:

```bash
python tools/extract_ui_sources.py \
  --package-root <installed-path> \
  --mode raw \
  --output <staging-path>/raw
```

Assisted alpha extraction may be used after raw crops are inspected:

```bash
python tools/extract_ui_sources.py \
  --package-root <installed-path> \
  --mode grabcut \
  --output <staging-path>/cleaned
```

Automated background removal is not authoritative. Visually inspect and clean every asset.

## 7. Convert sources into reusable runtime components

Do not implement the source sheets as single images.

For each extracted component:

- remove presentation background and residue
- clean alpha fringe
- add transparent padding
- preserve aspect ratio
- define pivot and safe bounds
- identify baked shadow versus runtime shadow
- separate changeable text and values
- define component states
- document source-sheet region
- map to the matching UI Kit component ID

Build scalable panels using 9-slice or layered corners, edges, centers, fasteners, tape, and shadows.

Never stretch or squash a raster UI asset.

## 8. Phase-specific usage

### Phase 1 - Buttons and tabs

Create reusable Primary Button, Secondary Button, Neutral Button, Icon Button, Tab, Locked, and Disabled components.

Keep logical hit targets stable while visual children lift, squash, or bounce.

### Phase 2 - Panels and containers

Create reusable cardboard, wood, notebook-paper, sticker-card, and junk-box container components.

Use blank centers for dynamic content. Animate pause-box flaps and menu contents as separate layers where practical.

### Phase 3 - HUD, notifications, and alerts

Prioritize the canonical HUD, toast, objective, warning, status, and impact assets described in `docs/ASSET_CATALOG.md`.

Do not implement the optional mini-map, compass, or character portrait HUD unless the current game design requires them.

Do not adopt alternate source-sheet branding or characters.

### Phase 4 - Results, rewards, and Character Select

Create reusable Level Clear, New Record, Unlock, Character Select Board, Trashy Card, Jimothy Card, P1 Badge, Selected Badge, and Pointer assets.

Trashy and Jimothy are equal playable choices. Preserve full silhouettes and proportions. These portraits are UI art, not gameplay animation sprites.

## 9. Dynamic content rules

Use runtime text and data for:

- button labels
- scores
- counts
- times
- objective copy
- settings labels
- character names when practical
- result values

Do not bake demo values such as 12,450, 18,920, or x18 into reusable runtime components.

Permanent branded art such as a fixed Trashed It headline or New Record stamp may remain raster art if it is intentionally non-localized.

## 10. Motion is required

Implement or adapt a centralized UI motion service that consumes `tokens/motion.tokens.json`.

Required sequences:

- button hover, press, release, and settle
- notification pop-in, readable hold, and drift-out
- pause-menu flap-open and close
- objective completion stamp
- warning slam and shake
- unlock reveal
- skippable Level Clear sequence
- Trashy and Jimothy selection swap and confirmation
- reduced-motion alternatives
- safe cancellation and interruption

Do not scatter unexplained duration and easing literals through screen code.

Critical game state must not depend on decorative animation callbacks.

## 11. Input and accessibility

- Support mouse, keyboard, controller, and touch where the game supports them.
- Focus and selected state must use more than color.
- Maintain stable hit targets during decorative transforms.
- Return focus correctly after Pause and modal screens.
- Implement reduced motion.
- Keep labels readable over actual gameplay backgrounds.
- Make repeated hero sequences skippable or accelerable.

## 12. Update repository guidance

Merge `AGENTS_UI_KIT_SNIPPET.md` into the appropriate root or project `AGENTS.md`.

Update UI, animation, asset-extraction, and visual-audit skills so they consult this package before modifying interface code or art. Reference the canonical paths rather than duplicating the full documents.

## 13. Runtime implementation order

1. token and motion adapter
2. button, icon-button, and tab primitives
3. material and scalable panel primitives
4. Main Menu and Character Select
5. Pause Menu
6. Level Clear and New Record
7. Unlock card
8. HUD counters and objective tracker
9. notifications and warnings
10. reduced-motion and full input pass
11. live-game visual QA

## 14. Required visual QA

Test in the actual game at supported resolutions.

Verify:

- no cropped art
- no squashed or stretched textures
- no brown sheet residue
- no alpha fringe
- no clipped shadows or overshoot
- no overlapping controls
- no unreadable dynamic text
- stable controller focus
- correct Trashy and Jimothy selection
- safe pause and resume repetition
- safe Level Clear skip
- safe animation interruption
- reduced motion

## 15. Final report

Return:

1. exact canonical install path
2. files copied or merged
3. validation and hash results
4. source sheets staged
5. assets extracted and their runtime paths
6. assets that still need manual alpha cleanup
7. reusable components created or updated
8. motion primitives and sequences implemented
9. screens updated
10. AGENTS and skills changes
11. live-game screenshots for Main Menu, Character Select, Pause, HUD notification, and Level Clear
12. remaining gaps against `ui-kit.manifest.json`
13. git diff summary

Do not call the UI Kit fully implemented while required components are static, missing motion, represented only by source sheets, or untested in live gameplay.
