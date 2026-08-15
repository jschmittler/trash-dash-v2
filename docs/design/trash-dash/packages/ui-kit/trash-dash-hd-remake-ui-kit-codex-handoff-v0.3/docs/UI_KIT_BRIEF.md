# Trash Dash HD Remake UI Kit Brief

## Purpose

This package defines the visual, behavioral, and motion language for the Trash Dash interface. It replaces generic or stylistically plain game UI with a system that feels built from the same world as the characters and levels.

The core direction is **Reclaimed Playground**. The interface looks assembled from objects Trashy and Jimothy might find, reuse, paint, tape together, and carry through the game.

Some approved source boards still show the working label **Trash Dash V2**. The current game name is **Trash Dash HD Remake**. Treat the V2 text as historical concept-board labeling, not a request to replace current title branding.

## Experience premise

The UI should feel handcrafted out of the game world, not placed on top of it.

A pause menu is a junk box that opens. A button is a painted cardboard or wood object. A notification is a sticker, paper note, bottle cap, or warning sign. A level-clear screen is a physical reward board that slams into place and fills with stamps, counts, and collectible pieces.

The visual personality can be playful and imperfect. The interaction model must remain clear, fast, and consistent.

## Design pillars

### 1. Built from the world

Use corrugated cardboard, painted wood, torn notebook paper, stickers, duct tape, masking tape, screws, nails, bottle caps, scrap metal, battered signs, paper clips, and hand-painted marks.

Avoid generic app cards, glass panels, featureless rounded rectangles, polished sci-fi surfaces, and default engine UI.

### 2. Physical depth

Components should feel layered and tangible. Use irregular silhouettes, visible edges, small overlaps, fasteners, taped corners, offset shadows, and occasional curled paper or bent sign details.

Depth should communicate hierarchy:

1. World and gameplay
2. UI surfaces and containers
3. Interactive controls
4. Notifications and feedback
5. Celebration and modal moments

### 3. Playful visually, predictable functionally

Decorative asymmetry is encouraged. Interaction inconsistency is not.

Players should always understand:

- what is focused
- what is selected
- what is disabled or locked
- what action is primary
- how to go back
- when input is accepted

Focus and selection must use more than color alone. Use position, outline, scale, check badges, arrows, stamps, or card lift.

### 4. Controlled imperfection

Edges can be hand-cut, paint can be worn, screws can be slightly uneven, and tape can be crooked. The system should still feel intentionally art-directed.

Do not randomize every component independently. Reuse a controlled set of materials, edge treatments, shadows, fasteners, and motion primitives.

### 5. Motion communicates state

Motion is part of the UI contract. It is not optional polish.

Preferred motion verbs are:

- lift
- press
- squash
- pop
- stamp
- bounce
- slide
- peel
- slam
- shake
- swing
- flap
- count up
- reveal
- burst

Frequent interactions stay quick. Hero moments can be more theatrical, but repeated sequences must be skippable or accelerable.

### 6. Reward has ceremony

Positive moments should feel satisfying. Level clear, new records, unlocks, secrets, checkpoints, and collectible milestones deserve distinct physical and animated feedback.

Do not use one generic toast for every event.

## Shape language

- chunky silhouettes
- hand-cut rounded corners
- slight asymmetry
- layered boards and scraps
- thick readable outlines
- visible corrugation, paint wear, and material seams
- front-facing 2D presentation for reusable UI art

Avoid excessive perspective. A small amount of physical depth is welcome, but components must remain easy to align, scale, and read.

## Material hierarchy

### Primary materials

- corrugated cardboard
- painted reclaimed wood

### Secondary materials

- torn paper
- notebook paper
- stickers
- tin or metal signs
- bottle caps

### Fasteners and accents

- masking tape
- duct tape
- screws
- nails
- paper clips
- small arrows, crowns, skulls, stars, and hand-drawn marks

## Color behavior

The palette is grounded in cardboard brown, aged cream, charcoal, weathered blue, muted green, worn yellow, rusty red, and teal.

Functional accents:

- Yellow: primary action, attention, objective
- Green: selected, success, continue, checkpoint
- Blue: information, utilities, settings, counters
- Red: danger, damage, destructive action, boss warning
- Purple: secret, rare, unusual reward
- Pink: celebratory stamp, pointer, new record accent

Color should reinforce meaning, not carry it alone.

## Typography

Use three roles:

1. Display: bold, chunky, hand-painted character for titles and hero moments
2. UI label: playful but highly readable for buttons, tabs, and headings
3. Support text: clean, readable text for settings, objectives, and descriptions

Dynamic labels, scores, counts, objectives, times, and settings should be rendered as runtime text. Do not bake changeable text into final production textures.

Permanent branded lettering or intentionally fixed art, such as a hand-painted Level Clear headline, may be raster art when appropriate.

## Character Select

Trashy and Jimothy are equal playable choices.

- Show both at once when the viewport permits.
- Preserve full silhouettes and original proportions.
- Do not crop ears, tails, tools, backpacks, feet, or props.
- Use contain-style scaling inside a shared card window.
- Separate character art, name label, focus treatment, selected badge, and confirmation animation.
- Selection must remain clear for keyboard, controller, mouse, and touch.

The character illustrations in this package are UI portraits and cards. They are not replacements for gameplay animation sprites.

## Animation energy levels

### Micro

Buttons, tabs, focus, pressed states, counters.

Typical duration: 80 to 180 ms.

### Mid

Toasts, objective updates, warnings, pause transitions, unlock cards.

Typical duration: 180 to 700 ms.

### Hero

Main menu arrival, boss warning, level clear, rare unlock, new record.

Typical sequence: 700 to 1700 ms.

## Accessibility and usability

- Support reduced motion.
- Never remove information when reducing motion.
- Keep hit targets stable even when art lifts or squashes.
- Maintain readable contrast over live gameplay.
- Keep focus visible at all times.
- Avoid text inside irregular art when it may overflow or localize.
- Do not use color as the only state indicator.
- Make repeated celebration sequences skippable.

## Visual anti-patterns

Do not introduce:

- generic mobile-game chrome
- glossy plastic UI
- sci-fi holograms
- glassmorphism
- clean corporate cards
- smooth blue gradient panels that ignore the reclaimed material language
- unrelated comic-book branding
- new mascots or character redesigns from generated sheet decoration
- perfectly uniform geometry everywhere
- raster stretching or squashing
- title logos copied from exploratory source sheets

## Authority order

When sources disagree, use this order:

1. Written contracts, tokens, and approval rules
2. `reference/concept-boards/00-overall-ui-kit.png`
3. The matching phase concept board
4. The matching phase source sheet
5. Implementation judgment that preserves the system

Concept boards define the visual language. Source sheets provide extraction candidates. Neither should be implemented as a single full-screen screenshot.
