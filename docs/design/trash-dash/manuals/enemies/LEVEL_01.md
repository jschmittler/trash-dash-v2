# Trash Dash HD Remake - Enemy Master Specification v1.0
## Level 1

**STATUS: APPROVED / LOCKED CANON**

The approved Level 1 sprite sheets are the visual source of truth. Written specification extends those designs without redesigning them.

## Level 1 Enemy Ecology

| Enemy | Placement | Core archetype | Primary player pressure |
|---|---|---|---|
| Mosquito | Flying | Airborne harasser / dash striker | Vertical positioning and quick reaction |
| Pilfer the Opossum | Ground | Pursuer / scavenger | Chase pressure and close combat |
| Pigeon | Ground | Charger / bruiser | Momentum and lane denial |
| Snake | Ground / low-profile | Ambusher / ranged controller | Low attacks and toxic projectiles |
| Spider | Ground + web-based entry | Controller / trapper | Space control and layered attacks |

The roster must not collapse into five skins of the same enemy. Their silhouettes, vertical placement, attack ranges, locomotion, and timing profiles are intentionally different.

---

# L1-E01: Mosquito

## 1. Identity and Gameplay Role

**Type:** Mutated mosquito  
**Archetype:** Airborne harasser / dash striker  
**Combat intent:** Interrupt movement, pressure jumping, and force the player to monitor airspace.

The Mosquito should feel persistent, twitchy, invasive, and more confident than its physical size warrants. It is dangerous because of mobility, not raw power.

## 2. Placement and Movement Class

**Placement:** FLYING

Normal states include hover, slow aerial patrol, fast aerial pursuit, dash, attack hover, and repositioning. It does not require a ground surface and should not become a walking insect during normal combat. Ground contact is reserved for impacts, defeat, or scripted moments.

## 3. Size, Scale, and Silhouette

**Relative class:** Small-to-medium enemy.

Recognition is driven by:

- Large pale wings
- Compact dark insect body
- Oversized angry eyes
- Extremely long red proboscis

The proboscis is essential. Removing or significantly shortening it changes the character identity. Preserve the approved in-game scale rather than normalizing it against unrelated sheets.

## 4. Immutable Visual Anatomy

### Visual Canon

- Exactly two large primary eyes
- Off-white/cream eye surfaces with dark pupils
- Heavy angry brow shapes
- One pair of primary insect wings
- Pale translucent wings with visible vein structure
- Six insect legs as the anatomical basis, with several trailing/occluded in poses
- Dark charcoal-to-black bristly abdomen
- Brown/rust thorax and head region
- Long dark-crimson/red proboscis
- Wet/drooping character at the end of the proboscis
- Small battered metal helmet/armored cap
- Rivets/studs and aged metal detailing
- No mammalian fur
- No defining visible teeth

Motion-smear wing shapes must not be interpreted as additional permanent wings.

## 5. Color, Material, and Surface Treatment

- Body: coarse, dirty, nearly black insect texture
- Thorax: rusty brown organic shell/fuzz
- Wings: translucent dirty cream, gray, beige
- Helmet: aged bronze/brown metal with dark oxidation
- Proboscis: dark crimson/red
- Eyes: warm off-white with strong dark outlines

Nothing should become clean or glossy. This creature belongs in a contaminated garbage environment.

## 6. Character Personality and Intent

The Mosquito is irritable, obsessive, impatient, opportunistic, and aggressively curious. Even idle animation should suggest it is barely restraining itself from attacking. Head direction can lead body movement slightly, and eyes should strongly track the player during aggression.

## 7. Gunk Transformation and Backstory

Before exposure, it was an ordinary mosquito living around stagnant water, garbage containers, puddles, and discarded vessels. Gunk contaminated the same standing water used by mosquito populations.

The Gunk amplified its most basic survival instinct: **feed**.

Movement, heat, sound, and living creatures became impossible to ignore. Its proboscis elongated, its body became heavier and more armored, and contaminated metallic refuse became lodged around its head like crude armor.

The Mosquito does not protect the Gunk because it understands it. It attacks because the Gunk transformed hunger into obsession.

## 8. Movement and Navigation Behavior

### Idle / Hover

Small positional drift with active wing motion.

### Slow Fly

Controlled patrol flight.

### Fast Fly / Dash

Body pitches forward, wings intensify, and trailing effects increase.

Preferred sequence:

`hover -> notice -> lean -> accelerate -> attack/reposition -> recover into hover`

Avoid instantaneous direction reversal. Even a tiny creature needs anticipation and braking.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Proboscis Strike

The Mosquito aligns with the target, pulls slightly backward, then thrusts forward.

**Telegraph:** wing cadence changes, eyes lock, head pulls back.  
**Damage moment:** proboscis reaches maximum extension.

### Secondary Behavior: Dash Strike

At greater distance, combine fast forward movement with the strike. Use the existing FAST FLY language instead of inventing a new pose family.

Red liquid effects from the sheet may support hit feedback, feeding, or impact effects.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Fast off-screen arrival. Streak in, slightly overshoot, brake, and settle into hover.

### Exit

Pitch forward and accelerate out using FAST FLY poses.

### Hit

Use the canonical HIT / REACT language: widened eyes, stars, loss of control.

### Defeat

Extend hit into uncontrolled spin/fall or off-screen trajectory. Do not create a realistic dead insect. Preserve exaggerated cartoon language.

## 11. Animation State Inventory

### Existing

- Idle / Hover
- Slow Fly
- Fast Fly / Dash
- Attack
- Hit / React
- Effects

### Add / support

- Spawn / Entry
- Player Detected
- Attack Anticipation
- Dash Brake
- Turn / Direction Change
- Recovery
- Defeat
- Retreat / Exit

## 12. Animation Construction and Modification Rules

Never redraw the Mosquito from text alone. Begin from an approved frame.

Preserve:

- eye size
- helmet construction
- proboscis attachment point
- wing attachment point
- thorax-to-abdomen ratio
- body texture
- wing coloration
- leg count
- head shape

Create motion through posing, wing angle, effects, and body orientation. Fast motion may use wing blur, speed trails, dust, and controlled smear, but the core body must remain identifiable. Effects should be separate layers where practical.

## 13. Collision and Gameplay Readability

Core body collider should primarily represent head, thorax, and central abdomen. Do not include full translucent wing span. Proboscis gains an attack collider only during active attack frames. Motion blur and liquid effects are not physical collision.

## 14. Effects and Environmental Interaction

Canonical effect language includes:

- Wing effects
- Speed clouds
- Red droplets
- Red splash
- Circular motion effect
- Dirt/debris

Keep effects painterly, dirty, and exaggerated.

## 15. Character Validation Checklist

Reject a frame if:

- Extra permanent wings appear
- Helmet changes design
- Eyes shrink significantly
- Red proboscis disappears
- Character becomes clean or brightly colored
- It stands or walks during normal gameplay
- Body becomes smooth instead of bristly
- Silhouette no longer matches approved art

---

# L1-E02: Pilfer the Opossum

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated opossum scavenger  
**Canonical identity:** Pilfer  
**Archetype:** Ground pursuer / thief / melee aggressor

Pilfer is a small-time garbage criminal who has taken scavenging too seriously. He is quick, sneaky, greedy, and frantic rather than lumbering.

## 2. Placement and Movement Class

**Placement:** GROUND

Requires a ground/platform surface. Standard movement includes standing, walking, running, crouched pursuit, lunging, and scrambling. He does not fly or use wall climbing as a standard Level 1 behavior.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium enemy.

The backpack creates much of his apparent mass. Key silhouette elements:

- Long pointed face
- Black beanie
- Huge rounded garbage sack
- Hunched upper body
- Long curling pink tail

The bag should make him read as back-heavy even during running.

## 4. Immutable Visual Anatomy

- Two eyes
- Pale face
- Strong dark eye markings
- Long pointed snout
- Pink/red nose
- Two large pink ears
- Two arms
- Two legs/feet
- Clawed hands
- Clawed feet
- One long hairless pink tail
- Gray/dark body fur
- Black knit cap
- Purple outer garment/hoodie
- Dark lower clothing
- Large brown garbage sack/backpack
- Visible junk and collected objects attached to or embedded in the bag
- Sharp teeth visible during aggressive expressions

Do not simplify the sack into a generic backpack.

## 5. Color, Material, and Surface Treatment

- Pale gray/cream face
- Dark charcoal markings
- Pink ears, nose, tail
- Black cap
- Muted purple clothing
- Brown/olive garbage sack
- Dirty metal and garbage accents

Everything remains worn, patched, dirty, and mismatched.

## 6. Character Personality and Intent

Pilfer is greedy before he is evil. His defining thought is **Mine.** He views food, trash, useful debris, and potentially Trashy's possessions as things that should belong to him.

Motion should communicate sneaking, scheming, territorial greed, panic when hit, and sudden aggression.

## 7. Gunk Transformation and Backstory

Pilfer encountered Gunk through normal scavenging. Trace contamination accumulated on packaging, cans, rotten scraps, and discarded objects.

Finding became collecting. Collecting became hoarding. Hoarding became stealing.

Pilfer began dragging increasingly absurd quantities of refuse until the garbage sack became part of his identity. The Gunk sharpened his intelligence just enough to recognize value, possession, and theft, but not enough to understand that most of his treasure is garbage.

## 8. Movement and Navigation Behavior

### Idle / Stand

Restless and hunched.

### Walk

Cautious scavenger movement.

### Run

Low sprint with dust and strong backpack inertia.

The sack should lag slightly behind direction changes. The tail is major secondary motion.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Claw Swipe

Forward claw attack.

### Secondary Attack: Scramble Lunge

Lower body and aggressively close distance before striking.

Telegraph through posture:

1. Stop.
2. Lower center of gravity.
3. Fix eyes on player.
4. Pull arm back.
5. Lunge.

Do not invent unrelated weapons.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Crawl or emerge from behind trash, dumpster, crate, bush, or level edge. Pause, notice player, then enter locomotion.

### Exit

Run away with sack bouncing violently.

### Hit

Maintain comic stars and startled facial reaction.

### Defeat

Backpack momentum carries him backward/off balance. A small junk piece may fall free before he scrambles away or is removed. Do not destroy the backpack as a normal hit reaction.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Walk
- Run
- Attack
- Hit / React
- Effects

### Add / support

- Enter
- Notice Player
- Suspicious Look
- Attack Windup
- Attack Recovery
- Turn
- Skid / Stop
- Defeat
- Retreat
- Exit

## 12. Animation Construction and Modification Rules

Head, hat, clothing, tail, and sack are locked design elements.

Do not:

- Change the beanie
- Remove clothing
- Recolor the purple garment
- Turn the bag into a rigid backpack
- Shorten the snout
- Add unrelated tools/weapons
- Make the tail furry
- Change the pink tail coloration

The bag should deform slightly from weight rather than behave as a rigid sphere. Clothing and bag motion follow the body with secondary overlap.

## 13. Collision and Gameplay Readability

Core collider follows torso, head, and main leg area. Tail is normally excluded. Backpack may visually extend beyond collider unless gameplay explicitly supports hitting it. Claws use temporary attack hitboxes.

## 14. Effects and Environmental Interaction

Canonical effects include:

- Dust
- Speed streaks
- Loose garbage
- Cans
- Leaves
- Dirt
- Ground scrapes

Pilfer should frequently disturb the environment.

## 15. Character Validation Checklist

Reject if:

- Pink tail disappears
- Beanie changes
- Sack becomes small
- Purple garment changes substantially
- Body becomes upright/humanlike
- Snout becomes short
- Sack stops functioning as a major silhouette feature

---

# L1-E03: Pigeon

## 1. Identity and Gameplay Role

**Type:** Gunk-altered urban pigeon  
**Archetype:** Ground charger / bruiser

Despite being a bird, this is primarily a ground enemy.

## 2. Placement and Movement Class

**Placement:** GROUND

The Pigeon may flap, hop, or briefly become airborne during attacks/transitions, but standard combat requires terrain. It must not occupy the Mosquito's sustained-flight role.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium.

Compact upright idle becomes extremely low and horizontal during running. Key identifiers:

- Pigeon body
- Large expressive eye
- Battered metal container/helmet
- Gray layered wings
- Iridescent neck

## 4. Immutable Visual Anatomy

- Two anatomical eyes, near eye dominant in profile
- Two wings
- Two orange/red feet
- Layered tail feathers
- Dark blue/charcoal head
- Gray body
- Pale gray belly
- Layered gray wing feathers
- Iridescent teal/green/purple neck
- Orange beak
- Large expressive cream eye area
- Battered metal pail/can-like helmet
- Bent dirty protrusion/handle at helmet crown
- No teeth

Do not add avian teeth.

## 5. Color, Material, and Surface Treatment

- Charcoal
- Slate gray
- Light gray
- Teal
- Green
- Purple
- Orange feet and beak
- Helmet: aged silver/gray metal with grime and brown weathering

## 6. Character Personality and Intent

The Pigeon thinks it owns the sidewalk. It is irritable, territorial, stubborn, easily offended, and strangely fearless. Unlike Pilfer, it does not scheme. It gets angry and commits.

## 7. Gunk Transformation and Backstory

The Pigeon ate discarded crumbs, grease, fries, bread, and garbage carrying Gunk traces. Contamination made it heavier, stronger, and much more territorial.

A discarded metal container became entangled with it and was eventually adopted as armor, almost as a badge of rank. Altered feathers became too dense for normal sustained flight, though the wings still support violent hops, lunges, braking, and attack motion.

This is why the bird functions as a ground combatant.

## 8. Movement and Navigation Behavior

### Idle / Stand

Compact and upright.

### Walk

Grounded bird movement.

### Run

Critical state: body drops almost horizontal while head leads. Preserve the silhouette transformation.

## 9. Attacks, Telegraphs, and Combat Behavior

Canonical attack language supports:

### Charge

Low, fast ground acceleration.

### Peck / Head Strike

Direct beak/helmet attack.

### Wing-Assisted Slam

Wings extend to add force and exaggeration.

Telegraph charge through a crouch/tension phase before launch.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Short flutter-hop from perch or off-screen. Land before normal ground combat.

### Exit

Run away or perform several frantic wing beats to leave. This does not change standard classification to flying.

### Hit

Use approved stars and shocked expression.

### Defeat

Strong impact can loosen or spin helmet temporarily, but helmet is canonical and should not disappear permanently except through explicitly authored defeat motion.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Walk
- Run
- Attack
- Hit / React
- Effects

### Add / support

- Flutter Entry
- Land
- Notice
- Charge Anticipation
- Charge
- Brake
- Turn
- Attack Recovery
- Defeat
- Exit

## 12. Animation Construction and Modification Rules

Maintain:

- Helmet shape and position
- Eye proportions
- Iridescent neck
- Gray feather structure
- Orange feet
- Compact pigeon body

Wing extension frames must remain the same bird anatomy. Helmet may bounce/rotate slightly but still appear attached.

## 13. Collision and Gameplay Readability

Normal collider follows head, torso, and lower body. Wing tips and tail feather extremities generally remain outside core collision. Charge uses a forward attack volume.

## 14. Effects and Environmental Interaction

Canonical effects:

- Loose feathers
- Feather swirls
- Dust
- Speed streaks
- Trash
- Ground impacts
- Helmet impacts

Charges should leave visible environmental chaos.

## 15. Character Validation Checklist

Reject if:

- Helmet disappears without narrative reason
- Neck loses teal/purple iridescence
- Pigeon becomes a sustained flying enemy
- Feet/beak lose warm orange palette
- Run loses low forward posture
- Extra wings appear

---

# L1-E04: Snake

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated snake  
**Archetype:** Low-profile ambusher / ranged controller

The Snake introduces threat at the bottom of the play space and combines low traversal with contaminated projectile pressure.

## 2. Placement and Movement Class

**Placement:** GROUND / LOW-PROFILE

No feet, no legs, no jumping locomotion. Normal movement remains in contact with or extremely close to the ground.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium footprint, low height.

Idle uses a taller coiled silhouette. Movement uses a long horizontal silhouette. Both forms are intentionally distinct.

## 4. Immutable Visual Anatomy

- No limbs
- No feet
- Long muscular body
- Olive/brown-green dorsal coloration
- Dark organic blotches
- Pale tan/cream underside
- Large expressive cartoon eyes
- Red forked tongue
- Wide jaw during attack
- Sharp white fangs in aggressive poses
- Thick battered metal collar around neck
- Dirt/grime surface treatment

Do not replace the approved expressive eyes with realistic tiny snake eyes.

## 5. Color, Material, and Surface Treatment

Dominant colors:

- Olive
- Mud brown
- Dark moss green
- Tan
- Cream
- Red mouth/tongue
- Dirty steel collar

Gunk-related attacks use sickly green fluid.

## 6. Character Personality and Intent

The Snake is patient, suspicious, calculating, irritable, predatory, and territorial. It watches, waits, then commits suddenly.

## 7. Gunk Transformation and Backstory

The Snake repeatedly crawled through contaminated runoff near cans, damp soil, drainage areas, and refuse. Gunk penetrated its scales and altered venom glands/digestive systems until its natural venom became closer to concentrated Gunk.

The neck collar began as refuse trapped around the animal. Instead of dying or escaping, the transformed Snake grew around it. The metal ring remains permanently embedded as a reminder of contamination.

The Snake effectively carries Gunk inside itself.

## 8. Movement and Navigation Behavior

Canonical:

- Idle / Coil
- Slither
- Fast Slither / Dash

Movement should be driven by a continuous body wave. Never slide the entire rigid sprite across the ground.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Gunk Spit

Rise, open jaw, expel green contaminated fluid.

### Secondary Attack: Bite

Close-range forward strike using fangs.

### Mobility Attack: Dash

FAST SLITHER may reposition or create contact pressure.

The head is the key telegraph. A raised head means danger is imminent.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Emerge from trash, pipe, tall vegetation, behind objects, or discarded containers. Slither outward and rise into Idle / Coil.

### Exit

Lower profile and disappear beneath/behind cover.

### Hit

Use canonical star effects and dazed posture.

### Defeat

Recoil, collapse into a loose coil, then retreat or remove. Avoid gore.

## 11. Animation State Inventory

### Existing

- Idle / Coil
- Slither
- Fast Slither / Dash
- Attack
- Hit / React
- Effects

### Add / support

- Emerge
- Notice
- Raise / Threaten
- Spit Windup
- Bite Windup
- Bite
- Recover
- Turn
- Retreat
- Defeat
- Exit

## 12. Animation Construction and Modification Rules

Maintain scale pattern continuity. Blotches cannot randomly change. Cream underside must remain logically connected through bends. Collar is rigid around a flexible neck and must not stretch.

Do not change:

- Head size
- Fang placement
- Eye proportions
- Tongue color
- Scale palette
- Collar design

The body should move around a consistent implied spine.

## 13. Collision and Gameplay Readability

Core collider follows head and central body mass rather than every tail curve. Bite uses temporary head/jaw attack volume. Gunk spit becomes an independent projectile collider.

## 14. Effects and Environmental Interaction

Canonical language includes:

- Forked tongue
- Green Gunk
- Dust
- Crushed cans
- Dirt
- Leaves
- Impact effects

Fast slither should disturb substantially more material than standard slither.

## 15. Character Validation Checklist

Reject if:

- Legs appear
- Collar changes
- Green attack becomes ordinary water
- Scale markings randomly regenerate
- Cream underside disappears
- Head proportions drift
- Movement looks like rigid sprite sliding

---

# L1-E05: Spider

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated garbage spider  
**Archetype:** Ground controller / trapper / multi-attack enemy

The Spider is one of the most mechanically complex standard Level 1 enemies. Canonical attack vocabulary explicitly includes **WEB, LUNGE, VENOM BITE**.

## 2. Placement and Movement Class

**Primary placement:** GROUND  
**Secondary traversal/entry:** WEB-SUSPENDED / OTHER

The Spider may descend or retreat via webbing but performs primary combat navigation on ground/platform surfaces. It is not a Mosquito-style flying enemy.

## 3. Size, Scale, and Silhouette

**Relative class:** Large standard enemy.

Silhouette is defined by:

- Eight radiating legs
- Large rounded contaminated rear reservoir
- Low dark head
- Huge eyes
- Purple-black coloration

It occupies more visual ground space than other normal Level 1 enemies.

## 4. Immutable Visual Anatomy

- Exactly eight legs
- Two oversized primary cartoon eyes
- Do not add realistic clusters of secondary spider eyes
- Dark purple/black head
- Purple segmented legs
- Large cream/yellow eye surfaces
- Large dirty green rear body/reservoir
- Grime, patch, and trash details
- Short metal container-like opening/object at top of rear mass
- White crossed marking/patch detail
- Large mouth with visible pointed teeth/fangs during attack
- Dark mouth interior
- Purple contaminated web/venom effects

The unusual rear structure is canonical. Do not reinterpret it as an ordinary spider abdomen. It is a fused Gunk-and-garbage structure.

## 5. Color, Material, and Surface Treatment

Primary palette:

- Very dark purple
- Black
- Violet
- Dirty green
- Olive
- Cream/yellow eyes
- Brown grime
- Rusted metal
- Pale lavender Gunk/web

The contrast between purple legs and green rear body is essential.

## 6. Character Personality and Intent

The Spider is possessive, patient, predatory, slightly unhinged, and confident inside its territory. It manipulates space rather than chasing merely because the player exists.

## 7. Gunk Transformation and Backstory

The Spider built its nest inside Gunk-saturated refuse. Webbing repeatedly absorbed contamination until boundaries between web, Gunk, trash, and animal blurred.

Its rear body swelled around contaminated refuse into a reservoir. Normal silk became sticky elastic Gunk filament. Venom mutated alongside it.

The Spider instinctively incorporates garbage into nest and body as building material.

Important distinction:

**Pilfer collects. Spider constructs.**

## 8. Movement and Navigation Behavior

Canonical:

- Idle / Stand
- Walk
- Run

Movement must account for eight legs. Scientific arachnid gait is not required, but alternating contact rhythm must feel coherent. Avoid random leg flicker. The heavy rear reservoir should show secondary weight and inertia.

## 9. Attacks, Telegraphs, and Combat Behavior

### Attack 1: Web

Ranged space-control attack. Webbing can create projectile, sticky surface, temporary obstacle, or slowing zone depending on implementation.

The approved artwork determines the emission point. Do not relocate it to a biologically "correct" position if that changes the character design.

### Attack 2: Lunge

Lower body, load legs, launch horizontally.

### Attack 3: Venom Bite

Close-range committed mouth/fang attack.

Intended relationship:

`web restricts movement -> lunge closes distance -> bite punishes proximity`

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Preferred special entry: web strand appears from above; Spider descends, lands, compresses, and settles into Idle / Stand.

### Exit

Scuttle off-screen or attach web upward and retract vertically.

### Hit

Use canonical dazed stars and compressed body language.

### Defeat

Legs buckle, heavy rear structure tips the creature, then it retreats or is pulled upward. Preserve cartoon tone.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Walk
- Run
- Attack
- Hit / React
- Effects

### Expand into

- Web Entry
- Land
- Notice
- Web Windup
- Web Fire
- Web Recovery
- Lunge Anticipation
- Lunge
- Lunge Landing
- Venom Bite Anticipation
- Venom Bite
- Bite Recovery
- Turn
- Hit
- Defeat
- Web Exit

## 12. Animation Construction and Modification Rules

Leg continuity is the highest priority.

Across frames:

- All eight legs remain accounted for
- Legs do not randomly appear/disappear
- Joint segmentation remains recognizable
- Contacting legs remain planted during support phase
- Moving legs arc between contacts

Rear reservoir can bounce/lag but construction must remain stable. Do not regenerate trash markings independently every frame.

For additional frames:

1. Preserve anchor-frame anatomy.
2. Pose limbs.
3. Preserve rear reservoir.
4. Preserve eyes/face.
5. Add secondary body motion.
6. Add web/venom separately.
7. Validate leg count and silhouette against neighbors.

## 13. Collision and Gameplay Readability

Core collider follows head/body and central abdomen/reservoir. Extreme leg tips remain outside normal body collision.

Independent attack volumes:

- Web projectile/zone
- Lunge body attack
- Bite mouth attack

## 14. Effects and Environmental Interaction

Canonical effects:

- Lavender web/Gunk
- Sticky splashes
- Dust
- Dirt impacts
- Loose garbage
- Cans
- Hanging drips

Web should look sticky and contaminated, not pristine white silk.

## 15. Character Validation Checklist

Reject if:

- Anything other than eight legs appears
- Realistic secondary eye clusters are added
- Green rear structure becomes an ordinary abdomen
- Purple coloration disappears
- Garbage/reservoir construction changes between frames
- Web changes visual language
- Ground movement becomes sliding rather than articulated walking
- New pose redesigns head or face

---

# Level 1 Global Animation Production Rules

1. Approved concept sheets are immutable source material. Never overwrite them.
2. Animation expansion is not character generation.
3. New frames require canonical visual anchors.
4. Preserve exact character anatomy, equipment, proportions, markings, palette, and material treatment.
5. Never use non-uniform sprite scaling to solve layout or speed.
6. Keep VFX separate where practical.
7. Stable pivots/roots must be maintained across each animation family.
8. Transparent image bounds are not collision bounds.
9. Visual canon takes priority over legacy implementation.
10. Validate every animation at gameplay scale in uninterrupted play.

The original approved sheets function as visual source code.
