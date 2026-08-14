# Trash Dash Boss Animation Expansion - Strict Execution Contract

## PURPOSE

Update the existing Trash Dash boss sprite assets so every required boss includes complete animation sequences for:

* **EMERGE**
* **RETREAT**
* **DEFEAT**

These sequences are additive animation work only.

**THE BOSS CHARACTERS ARE LOCKED.**

This task does not authorize redesigning, improving, modernizing, reinterpreting, restyling, simplifying, embellishing, correcting, or otherwise changing any boss character.

The goal is:

> **Same exact boss. Same exact design. New poses and frames only.**

---

# 1. SOURCE-OF-TRUTH HIERARCHY

Every execution must follow this authority order:

1. **This Trash Dash Boss Animation Expansion - Strict Execution Contract (`bossfix.md`)**
2. **Approved original boss artwork and sprite references**
3. **Explicitly approved animation requirements from this conversation**
4. **The current execution command**
5. Everything else

Higher-ranked sources always override lower-ranked sources.

Previous generated images, failed attempts, assistant summaries, conversational shorthand, assumptions, memory, or inferred preferences are **NOT sources of truth**.

If any instruction conflicts with this Contract, this Contract wins.

If a conflict cannot be resolved without violating a higher-ranked source, stop execution and report:

**EXECUTION BLOCKED - SOURCE CONFLICT**

Do not improvise a solution.

---

# 2. IMMUTABLE CHARACTER LOCK

Every boss is a locked character.

The following characteristics must remain unchanged unless an approved source image already depicts a pose-dependent variation:

* Overall character design
* Character identity
* Body shape
* Body proportions
* Head shape
* Face
* Eyes
* Mouth
* Teeth
* Nose
* Ears
* Limbs
* Hands
* Feet
* Tail
* Fur, skin, shell, scales, metal, fabric, trash, or other body materials
* Colors
* Color placement
* Patterns
* Markings
* Clothing
* Armor
* Accessories
* Props permanently associated with the character
* Surface textures
* Rendering style
* Line treatment
* Shading treatment
* Detail level
* Silhouette language
* Visual age
* Visual personality
* Species
* Mechanical construction
* Relative scale
* Any character-specific identifying feature

Do **not** add:

* New costume elements
* New armor
* New accessories
* New facial features
* New markings
* New colors
* New damage
* Scars
* Cracks
* Dirt
* Blood
* Debris
* Weapons
* Effects
* Glows
* Energy
* Smoke
* Motion trails

unless those elements already exist in the approved boss design or are explicitly authorized.

Animation does not grant permission to redesign the character.

---

# 3. PERMITTED CHANGES

The only changes permitted for the new animation frames are changes necessary to create motion.

These can include:

* Limb position
* Head position
* Body position
* Body rotation
* Character translation
* Character orientation
* Expression changes that are consistent with the existing character
* Pose-dependent perspective
* Pose-dependent foreshortening
* Natural overlap of body parts
* Existing articulated mechanical movement
* Existing squash or stretch only when consistent with the established animation language
* Visibility changes required when a character enters or exits the scene

These changes must always preserve the underlying character design.

---

# 4. REQUIRED ANIMATION SEQUENCES

Every boss must be audited for the following three sequences.

## EMERGE

The sequence must clearly communicate the boss entering, revealing itself, appearing from its established location, or transitioning from its hidden/pre-fight state into its active boss state.

The animation should progress logically from the boss's established starting condition to its normal active state.

The final EMERGE frame must connect naturally to an existing idle, ready, attack, movement, or other established active-state animation.

Do not invent a new entrance mechanism if the level, existing sprite set, boss design, or source artwork already implies one.

---

## RETREAT

The sequence must clearly communicate the boss intentionally withdrawing, hiding, backing away, escaping, submerging, leaving the active area, or otherwise transitioning out of its current active state.

RETREAT is **not DEFEAT**.

The character should remain capable of returning afterward unless the existing game behavior specifies otherwise.

The first RETREAT frame must connect naturally to an existing active animation.

The final frame must establish the appropriate hidden, exited, or inactive state.

Do not make the boss appear injured, destroyed, unconscious, or dead during RETREAT unless existing approved behavior specifically requires it.

---

## DEFEAT

The sequence must clearly communicate that the boss has lost the encounter.

The animation should transition naturally from the boss's active state through an unmistakable defeat reaction and into its established post-defeat state.

Possible motion may include reaction, staggering, loss of balance, collapse, shutdown, recoil, falling, slumping, or another character-appropriate defeat action.

However:

**Defeat does not authorize character damage or redesign.**

Do not add:

* Wounds
* Broken body parts
* New cracks
* Detached pieces
* Damage markings
* New facial anatomy
* New destruction effects

unless they already exist in approved source material.

The boss at the end of DEFEAT must still visibly be the exact approved character.

---

# 5. FRAME COUNT AND ANIMATION LANGUAGE

Do not arbitrarily invent animation specifications.

First inspect the boss's existing sprite system.

Determine:

* Existing frame dimensions
* Existing frame count conventions
* Animation cadence
* Pose spacing
* Motion exaggeration
* Camera perspective
* Character scale
* Ground plane
* Character anchor point
* Sprite-sheet organization
* Padding
* Transparency requirements
* Existing start/end animation states

New sequences must conform to those conventions.

If the existing assets provide enough information to determine the appropriate structure, use them.

If an essential animation specification genuinely cannot be derived from the approved assets or this Contract, do **not** silently invent it.

Remain in Conversation Mode and identify the unresolved requirement.

---

# 6. EXISTING SEQUENCES MUST BE PRESERVED

Before creating anything, audit the supplied boss assets.

For each boss determine whether EMERGE, RETREAT, and DEFEAT already exist.

If an approved sequence already exists and satisfies the contract:

**PRESERVE IT.**

Do not regenerate it merely for consistency.

If a sequence exists but is incomplete, identify exactly what is missing.

If a sequence does not exist, create it.

Do not modify unrelated animations.

Existing approved animations are locked unless I explicitly request changes to them.

---

# 6A. FULL SPRITE-SHEET REGENERATION AND ASSEMBLY

Every execution must deliver a complete boss sprite sheet containing both:

* All existing approved sprites
* Only the new sprites required to complete the approved work

Recreating the full sheet means assembling a complete updated sheet. It does **not** authorize redrawing, regenerating, retouching, or otherwise altering existing approved sprites.

Every existing approved sprite must be transferred from the approved source sheet into the updated sheet exactly as supplied.

For existing approved sprites, do **not** change:

* Pixel content
* Pose
* Character design
* Color values
* Alpha values or transparency
* Dimensions
* Scale
* Cropping
* Padding within the frame
* Anchor position
* Ground alignment
* Edge treatment
* Rendering or shading
* Frame order
* Animation assignment

Do not pass the full source sheet, an approved sequence, or any approved sprite through a generative redraw, image-to-image transformation, resampling step, enhancement filter, cleanup pass, or style-matching process.

Generation is permitted only for:

* A sequence classified as `MISSING`
* The specifically missing frames of a sequence classified as `EXISTS - INCOMPLETE`
* A frame explicitly classified as invalid and not approved

When a sequence is incomplete, preserve every approved frame in that sequence and add or replace only the frames identified in the immutable generation specification and batch manifest.

The original sheet layout, cell dimensions, frame spacing, and ordering must remain unchanged wherever the source sheet has usable empty cells or reserved positions. If the sheet must expand to contain new frames, preserve the original sheet region exactly and add only the minimum required rows, columns, or clearly defined sequence region. Do not rearrange approved sprites merely to make the layout more uniform.

Before generation, the batch manifest must distinguish:

* `PRESERVE EXACTLY` — existing approved sprites copied unchanged
* `GENERATE NEW` — missing sprites to be added
* `REPLACE UNAPPROVED` — invalid, explicitly unapproved sprites that may be replaced

After assembly, validate every `PRESERVE EXACTLY` cell against the approved source. Its pixel and alpha data must match exactly. Any mismatch is a validation failure.

The complete updated sprite sheet is the required deliverable. Separate generated frames may also be provided for review, but they do not replace the complete-sheet deliverable.

---

# 6B. FRAME ISOLATION, SPACING, AND EFFECT ENVELOPES

Every sprite frame must be spatially isolated from every neighboring frame.

For this rule, a frame includes its complete visible envelope:

* The boss body
* Every limb and pose extreme
* Shadows or ground-contact marks that belong to the frame
* Authorized sludge, spray, projectile, particle, droplet, debris, impact, or motion effect
* Every intentional detached pixel or detached visual component assigned to that frame

The complete visible envelope of one frame must never overlap, touch, enter, or contaminate the source rectangle, extraction area, or transparent gutter of another frame. Adjacent frame artwork may not share pixels or visually merge into one continuous image.

An effect that travels through gameplay space must still be contained entirely inside its own declared frame rectangle. If the combined boss-and-effect envelope cannot fit safely, use one of the following without shrinking the boss:

1. A larger uniform cell for that animation family
2. An explicit larger frame rectangle declared in the manifest
3. A separate effect-only sprite or atlas region with its own declared anchor, timing, and ownership

Never solve a spacing problem by reducing sprite scale, squeezing the artwork, cropping visible pixels, shortening an approved effect, changing the pose, or allowing cross-frame bleed.

Preserve the original pose order. Existing approved sprite pixels must remain byte-for-byte unchanged. However, when an approved sprite's complete visible envelope is not isolated, the sprite and all visual components belonging to that frame may be moved together as one unchanged unit or placed in an expanded sheet region solely to create safe separation. This narrow layout correction does not authorize redrawing, resampling, scaling, rotating, retouching, splitting apart an integrated frame, changing its internal padding, or changing its logical anchor and ground contact.

The sheet may expand as much as necessary to provide safe transparent spacing. Uniform appearance is not the objective; reliable extraction is. Each declared frame rectangle must contain its complete visible envelope plus a fully transparent gutter on every side. The gutter must be large enough that no visible pixel touches a frame boundary and neighboring cells can be extracted independently with no foreign pixels.

During the pre-generation audit, classify any frame with cross-frame overlap, neighboring-frame bleed, boundary contact, or ambiguous effect ownership as invalid for assembly until its layout is corrected. If its artwork is otherwise approved, classify it as `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`, not `REPLACE UNAPPROVED`.

This rule applies to all animation rows and effect families, including attack sequences. It is not limited to the frame or row that first revealed the problem.

---

# 7. CONVERSATION MODE VS EXECUTION MODE

There are two completely separate operating modes.

## MODE A - CONVERSATION

Conversation Mode is the default.

In Conversation Mode you may:

* Discuss requirements
* Inspect references
* Audit existing assets
* Identify missing animation sequences
* Recommend frame structures
* Explain technical constraints
* Propose changes
* Ask or answer questions
* Build an execution plan
* Refine requirements

You may **NOT generate or modify final assets** in Conversation Mode.

Discussion does not alter this Contract.

Suggestions do not alter this Contract.

Assistant statements do not alter this Contract.

Generated examples do not alter this Contract.

My feedback does not alter this Contract unless I explicitly approve a change.

Nothing said conversationally should gradually replace or weaken the original requirements.

---

# 8. CHANGING THE REQUIREMENTS

A change becomes authoritative only when I explicitly state something equivalent to:

**AMEND CONTRACT:**

or

**APPROVE SPEC CHANGE:**

Ordinary discussion is not a contract amendment.

If I say:

* "Maybe..."
* "What if..."
* "Could we..."
* "I wonder if..."
* "Try something like..."
* "What do you think about..."

treat it as discussion, not authorization.

---

# 9. EXECUTION TRIGGER

Do not begin generation simply because enough information appears to be available.

Execution begins only when I issue a direct command using:

**EXECUTE: [boss or batch]**

Examples:

`EXECUTE: PROJECT O.P.O.S.S.U.M.`

`EXECUTE: Level 6 boss`

`EXECUTE: All approved bosses missing DEFEAT animations`

Anything else remains Conversation Mode.

---

# 10. MANDATORY EXECUTION WORKFLOW

Every EXECUTE command must use this exact process:

**RELOAD THIS CONTRACT → COMPILE IMMUTABLE GENERATION SPECIFICATION → BATCH MANIFEST → GENERATE → ASSEMBLE FULL SHEET → VALIDATE → DELIVER OR REJECT → RESET**

No stage may be skipped.

---

# 11. STEP 1 - RELOAD THIS CONTRACT

Immediately before **every execution batch**, actively reopen and reread the complete current copy of `bossfix.md`.

Do not use:

* Memory
* A summary
* A prior compiled specification
* A previous batch's prompt
* Previous assistant reasoning
* Previous generated results

as a substitute.

This Contract must be reread from the actual source document.

If this Contract cannot be accessed at execution time, stop.

Report:

**EXECUTION BLOCKED - CONTRACT NOT ACCESSIBLE**

Never recreate the contract from memory.

---

# 12. STEP 2 - RELOAD APPROVED BOSS REFERENCES

After reading this Contract, reopen the approved source artwork for the boss being generated.

Treat those files as the visual identity reference.

Do not use a previous failed generation as a character reference.

Do not allow cumulative generations to slowly redefine the character.

Every new animation sequence must derive from the approved source boss.

---

# 13. STEP 3 - COMPILE A FRESH IMMUTABLE GENERATION SPECIFICATION

For the current batch, create a new internal generation specification from:

* The freshly reread current copy of this Contract
* The freshly inspected approved boss references
* The approved animation requirements
* The current EXECUTE command

The specification must explicitly define:

### Identity

* Boss name
* Approved reference assets
* Locked design characteristics

### Animation

* Sequence being generated
* Existing start state
* Required motion progression
* Required end state
* Frame count
* Frame ordering
* Pose continuity

### Rendering

* Perspective
* Scale
* Lighting
* Shading
* Texture
* Style
* Transparency
* Canvas requirements
* Sprite dimensions
* Character anchor
* Ground alignment
* Complete visible bounds and motion/effect envelope
* Required transparent gutter on every side
* Frame-isolation strategy for detached or emitted effects

### Restrictions

* Features that cannot change
* Elements that cannot be added
* Existing animations that cannot be modified

This specification becomes immutable for that execution.

Do not rewrite it during generation to accommodate a bad result.

If generation fails, correct the result against the specification.

Do not correct the specification against the result.

---

# 14. STEP 4 - CREATE THE BATCH MANIFEST

Before generation, create a manifest listing exactly what will be produced.

For every sequence include:

* Boss
* Sequence name
* Existing or missing
* Number of frames
* Start state
* Intermediate motion
* End state
* Required continuity connection
* Output format

For the full-sheet assembly also include:

* Every source region marked `PRESERVE EXACTLY`
* Every new frame location marked `GENERATE NEW`
* Every explicitly unapproved frame location marked `REPLACE UNAPPROVED`
* Every approved frame requiring layout-only isolation marked `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`
* Original sheet dimensions
* Updated sheet dimensions
* Cell dimensions or explicit frame rectangles and placement coordinates
* Complete visible bounds for every frame
* Required transparent gutters on all four sides
* Ownership, anchor, and timing for every detached or effect-only sprite

Only items in the manifest may be generated.

No bonus assets.

No alternate designs.

No experimental variations.

No unrequested poses.

---

# 15. STEP 5 - GENERATE

Generate only the assets defined by the compiled specification and manifest.

Do not generate existing approved sprites. Generate only items marked `GENERATE NEW` or `REPLACE UNAPPROVED`, then assemble them with the unchanged `PRESERVE EXACTLY` source regions into the complete updated sprite sheet.

The visual target is:

> **The approved boss performing a new action, not a new interpretation of the boss.**

When choosing between more visually interesting motion and stronger design preservation, choose design preservation.

When choosing between dramatic posing and animation continuity, choose animation continuity.

When choosing between artistic improvisation and the approved reference, choose the approved reference.

---

# 16. STEP 6 - VALIDATE BEFORE DELIVERY

Generation is not completion.

Every generated sequence must be inspected against both:

1. The immutable generation specification
2. The approved original boss reference

Do not send assets to me before validation.

Validate every sequence against the following tests.

## TEST A - CHARACTER IDENTITY

Confirm:

* Same boss
* Same proportions
* Same anatomy
* Same face
* Same features
* Same colors
* Same markings
* Same materials
* Same clothing
* Same accessories
* Same visual style
* Same detail language

**PASS / FAIL**

---

## TEST B - UNAUTHORIZED DESIGN CHANGE

Check for:

* Added details
* Removed details
* Changed proportions
* Changed colors
* Changed shapes
* New props
* New damage
* New effects
* New anatomy
* Costume changes
* Style drift

There must be no unauthorized design changes.

**PASS / FAIL**

---

## TEST C - ANIMATION COMPLETENESS

Confirm that the sequence includes:

* Clear starting state
* Readable motion progression
* Sufficient intermediate poses
* Clear ending state
* No unexplained jumps
* No accidental duplicate frames
* Correct sequence order

**PASS / FAIL**

---

## TEST D - ANIMATION CONTINUITY

Inspect the sequence as motion, not as isolated illustrations.

Confirm:

* Limbs move logically
* Body mass moves logically
* Facing direction remains intentional
* Scale remains stable
* Ground contact remains consistent
* Anchor point remains usable
* Perspective remains stable
* Motion reads clearly frame-to-frame
* Start and end poses connect to adjacent game states

**PASS / FAIL**

---

## TEST E - SEQUENCE MEANING

For EMERGE:

Does the boss unmistakably transition from its pre-fight/hidden state into its active state?

For RETREAT:

Does the boss unmistakably withdraw without appearing defeated?

For DEFEAT:

Does the boss unmistakably lose the encounter without becoming a redesigned or damaged character?

**PASS / FAIL**

---

## TEST F - TECHNICAL SPRITE COMPLIANCE

Confirm all technical requirements in this Contract, including any applicable:

* Image dimensions
* Transparency
* Cropping
* Padding
* Sprite scale
* Alignment
* Frame spacing
* Background restrictions
* Edge quality
* Output organization
* Naming requirements
* Exact pixel-and-alpha preservation of every `PRESERVE EXACTLY` cell
* Exact pixel-and-alpha preservation of every `PRESERVE EXACTLY - REPOSITION FOR ISOLATION` frame
* Correct placement of every `GENERATE NEW` or `REPLACE UNAPPROVED` cell
* Complete updated sprite-sheet assembly

**PASS / FAIL**

---

## TEST G - FRAME ISOLATION AND SPACING

Inspect the complete updated sheet and every declared extraction rectangle at 100% and magnified pixel view.

Confirm:

* Every frame's complete visible envelope is inside its own declared rectangle
* No visible pixel touches a frame boundary
* Every frame has a fully transparent gutter on all four sides
* No boss body, projectile, spray, sludge, particle, impact, shadow, detached component, or motion effect overlaps or enters a neighboring frame rectangle or gutter
* No two adjacent sprites visually merge into a continuous image
* Every frame can be extracted independently without including pixels from another frame
* Detached effects have unambiguous frame ownership or are stored as separately declared effect sprites
* Repositioned approved frames preserve their original pixel and alpha data exactly
* Pose order, approved artwork dimensions, internal registration, logical anchor, ground contact, facing direction, and gameplay scale remain unchanged; only the containing cell or explicit source rectangle may grow

Any cross-frame overlap, boundary contact, neighboring-frame bleed, ambiguous ownership, or contaminated extraction is an automatic failure.

**PASS / FAIL**

---

# 17. FAILED VALIDATION

A failed validation result must never be presented as finished work.

If any test fails:

1. Identify the exact failed frame or sequence.
2. Compare it against the immutable specification.
3. Regenerate or correct only the failed asset.
4. Repeat the complete validation.
5. Deliver only after every required test passes.

Do not lower the standard because repeated attempts fail.

Do not modify the boss design to make animation generation easier.

Do not silently accept "close enough."

If the requested output cannot be produced without violating the contract, report:

**VALIDATION FAILED - NO COMPLIANT ASSET PRODUCED**

and explain which requirement prevented delivery.

---

# 18. DELIVERY GATE

A batch may be delivered only when:

**Character Identity = PASS**
**Unauthorized Design Change = PASS**
**Animation Completeness = PASS**
**Animation Continuity = PASS**
**Sequence Meaning = PASS**
**Technical Sprite Compliance = PASS**
**Frame Isolation and Spacing = PASS**

All seven are mandatory.

Before presenting the result, state:

**VALIDATION: PASSED**

If validation has not passed, do not label the asset complete or approved.

---

# 19. APPROVAL

Successful generation does not automatically make an asset approved.

Only I can approve final artwork.

Until I explicitly say that a boss or sequence is approved, treat it as:

**GENERATED - AWAITING USER APPROVAL**

Do not use an unapproved generation as a new canonical character reference.

---

# 20. RESET AFTER EVERY EXECUTION

After an execution batch is delivered:

Discard the compiled generation specification and batch manifest.

Do not reuse them for the next boss.

Do not assume the next execution is "the same as last time."

Do not say "using the same rules as before" instead of rebuilding the specification.

For the next EXECUTE command, begin again with:

**RELOAD THIS CONTRACT → COMPILE IMMUTABLE GENERATION SPECIFICATION → BATCH MANIFEST → GENERATE → ASSEMBLE FULL SHEET → VALIDATE → DELIVER OR REJECT → RESET**

This Contract must be reread again from the current `bossfix.md` file.

The approved boss references must be reopened again.

A fresh specification must be compiled again.

---

# 21. ANTI-DRIFT RULE

The longer this conversation becomes, the **more important** the original sources become, not less.

Conversation history must never gradually replace the source files.

At execution time, authority comes from the freshly loaded contract and approved source artwork.

Not from conversational momentum.

Not from prior generations.

Not from remembered instructions.

Not from what seems aesthetically preferable.

---

# 22. INITIAL ACTION AFTER RECEIVING THIS CONTRACT

Do **not** generate anything immediately.

Enter **CONVERSATION MODE**.

First:

1. Confirm that the current `bossfix.md` Contract is available.
2. Identify the approved boss source assets available to you.
3. Audit each boss for existing EMERGE, RETREAT, and DEFEAT sequences.
4. Classify each sequence as:

   * `EXISTS - COMPLETE`
   * `EXISTS - INCOMPLETE`
   * `MISSING`
5. Identify any genuinely unresolved requirements that prevent execution.
6. Present the proposed animation work without generating it.

Then wait for an explicit:

**EXECUTE: [boss or batch]**

before creating or modifying any asset.
