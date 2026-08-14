# Trash Dash HD Remake - Enemy Master Specification v1.1
## Level 2

**STATUS: APPROVED / LOCKED CANON**

The approved Level 2 character sheets remain the visual source of truth. Written canon extends those designs but never redesigns them.

## Level 2 Enemy Ecology

| Enemy | Placement | Core archetype | Primary player pressure |
|---|---|---|---|
| Dog | Ground | Reactive chaser / close-range aggressor | Pursuit, pressure, Gunk expulsion |
| Dustwing | Flying | Aerial controller / lantern attacker | Vertical pressure and unusual attack arcs |
| Skunk | Ground | Area-control enemy | Persistent hazardous space |
| Squirel | Ground | Ranged projectile defender | Distance pressure and projectile timing |
| Bee | Flying | Venom dash attacker | High-speed aerial commitment |

Core identities:

- Dog pursues.
- Dustwing manipulates aerial space.
- Skunk contaminates space.
- Squirel attacks from range.
- Bee commits to high-speed aerial attacks.

The standard Level 2 Dog is not Brutus. Keep Brutus separate if implemented elsewhere as a boss.

---

# L2-E01: Dog

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated domestic canine  
**Archetype:** Reactive chaser / close-range aggressor  
**Primary intent:** Detect the player, pursue aggressively, force movement, and punish hesitation.

The Dog should feel more physical than most standard enemies. Once aggravated, it commits to the chase. The intended player reaction is: **That thing is coming after me.**

## 2. Placement and Movement Class

**Placement:** GROUND

Four-legged ground enemy requiring a walkable surface. Standard navigation supports standing, alert standing, walking, trotting, running, charging, lunging, skidding, and recovering. It does not fly or wall-climb during normal gameplay.

Small jumps may be authored later for navigation, but they are not inferred from the current sheet and are not part of the base moveset.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium-to-large standard enemy.

Key silhouette:

- Large canine head
- Forward-projecting muzzle
- Upright triangular ears
- Stocky torso
- Four strong legs
- Large bushy upward-curving tail
- Scrap-covered back
- Low forward-leaning run posture

Idle is taller and square. Run is stretched, low, and horizontal. Preserve this silhouette change.

## 4. Immutable Visual Anatomy

### Visual Canon

- Exactly two eyes
- Large expressive white-to-cream eye surfaces
- Dark pupils
- Heavy dark brows
- Two upright triangular ears
- Pink/dark reddish inner ears
- One black canine nose
- Long canine muzzle
- Dark lips
- Multiple sharp white teeth
- Red/pink mouth interior
- Four legs
- Four paws
- Visible claws where pose allows
- One large bushy tail
- Thick dirty canine fur
- Warm tawny/orange-brown coat with darker mottling
- Dark markings on head/body
- Lighter muzzle/underside areas

Canonical scavenged gear includes:

- Green neck cloth/collar element
- Round blue hanging tag/medallion
- Brown/red straps
- Dented gray/silver scrap metal across the back
- Leaves/plant debris
- Miscellaneous refuse caught in the back rig

Do not simplify the Dog into a clean ordinary household animal.

## 5. Color, Material, and Surface Treatment

Primary palette:

- Tawny brown
- Rust brown
- Dark brown
- Black
- Warm cream
- Muted green
- Dirty red-brown
- Dull gray metal
- Blue tag accent
- Sickly yellow-green Gunk

Fur is coarse, clumped, dirty, uneven, and wild. Scrap is dented, scratched, tarnished, dirty, and improvised. Gunk is viscous, yellow-green, translucent in thin areas and opaque in thick areas. It never resembles clean water.

## 6. Character Personality and Intent

The Dog is territorial, suspicious, reactive, determined, impulsive, protective, and easily provoked. The Gunk distorted, rather than erased, familiar instincts such as territory, threats, possession, familiar smells, and protection.

It believes contaminated areas are territory that must be defended. Idle should feel watchful, not mindless. Detection should visibly progress from suspicion to aggression.

## 7. Gunk Transformation and Backstory

The blue tag supports the idea that this was once an ordinary neighborhood animal with a home. It investigated contaminated garbage, food, runoff, water, and refuse exactly as a dog would: sniffing, licking, eating, and drinking.

Repeated exposure made it tougher and more aggressive. The digestive system began producing/retaining contaminated fluid. Fur became matted from constant movement through refuse. Straps, leaves, and metal accumulated across the body into accidental armor.

The tragedy is that a recognizable old instinct remains. The Dog still thinks it is protecting something, but no longer understands what deserves protection.

## 8. Movement and Navigation Behavior

### Idle / Stand

Tense breathing, ear movement, tail motion, weight shift, eye tracking, lip/head movement. Never relaxed/friendly.

### Walk

Deliberate four-legged gait with forward lean. Maintain believable footfall order and planted feet.

### Run

Compress body downward and extend horizontally. Emphasize front-leg reach, rear-leg drive, spine compression, tail follow-through, ear lag, scrap-rig bounce, and dirt displacement.

Preferred chain:

`Idle -> Detect -> Alert -> Growl -> Accelerate -> Run -> Attack -> Recover -> Resume pursuit`

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Gunk Retch

The Dog violently expels green contaminated fluid from its mouth.

**Telegraph:** brace, dip/pull head back, open jaw, show residue, compress chest/abdomen.  
**Active:** lunge forward while Gunk leaves mouth.  
**Recovery:** mouth closes gradually and residual droplets may remain.

The attack should feel unpleasant and uncontrolled rather than magical.

### Secondary Threat: Chase Bite / Body Lunge

At close range, perform a shorter contact lunge/bite based on approved aggressive head/run poses. Do not build elaborate combo attacks unless separately designed.

Core loop remains:

`see player -> chase -> close distance -> attack`

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Rapidly enter from outside camera or behind environmental cover. Optional growl/bark can signal arrival.

### Exit

Turn and accelerate into established run cycle behind scenery or beyond arena.

### Hit

Canonical reaction includes wide eyes, stars, sudden loss of composure, compression, and temporary collapse.

### Defeat

Heavy stagger, leg instability, body compression, short dazed pause, then retreat/removal. Do not portray realistic animal injury.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Walk
- Run
- Attack
- Hit / React
- Effects

### Required expanded states

- Spawn / Entry
- Suspicious
- Detect Player
- Alert
- Growl / Attack Telegraph
- Acceleration
- Run
- Short Stop
- Skid
- Turn
- Gunk Retch Windup
- Gunk Retch Active
- Gunk Retch Recovery
- Bite / Contact Lunge
- Hit
- Heavy Hit
- Dazed
- Defeat
- Retreat
- Exit

## 12. Animation Construction and Modification Rules

Quadruped anatomy is high-risk for drift.

Locked features:

- Head proportions
- Muzzle length
- Ear shape
- Number of legs
- Tail construction
- Fur palette
- Blue tag
- Green neck detail
- Scrap-back arrangement
- Teeth style
- Body proportions

For intermediate frames:

1. Start from approved keyframes immediately before/after desired frame.
2. Identify weight-bearing paws.
3. Keep support paws grounded.
4. Move torso relative to planted limbs.
5. Advance airborne paws along believable arcs.
6. Maintain shoulders/hips.
7. Add spine compression.
8. Add head follow-through.
9. Add ears/tail secondary motion.
10. Add scrap movement last.

Tail follows momentum and must not behave rigidly. Back equipment lags slightly, metal remains rigid, straps flex, leaves flutter. Gunk should be a separate effect layer where practical.

## 13. Collision and Gameplay Readability

Core collider approximates chest, torso, head, main leg mass. Bushy tail and extreme ear tips remain outside primary collision.

Attack colliders:

- Bite/lunge: forward head/mouth volume
- Gunk retch: independent projectile/stream/hazard volume

Visual droplets outside gameplay volume are not automatically damaging.

## 14. Effects and Environmental Interaction

Canonical effects:

- Green Gunk stream
- Gunk splash
- Dust clouds
- Dirt
- Ground debris
- Impact burst
- Paw prints

Running should visibly disturb loose material. Paw prints may briefly appear on suitable surfaces.

## 15. Character Validation Checklist

Reject if:

- Leg count changes
- Paws visibly slide during planted phases
- Blue tag disappears
- Green neck treatment disappears
- Back scrap changes arbitrarily
- Fur becomes clean/smooth
- Tail size changes dramatically
- Muzzle shortens
- Teeth style changes
- Gunk becomes clear/blue
- Run loses low horizontal silhouette
- Effects are permanently merged into body art

---

# L2-E02: Moth / Dustwing

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated moth  
**Canonical identity:** Dustwing  
**Placement:** Flying  
**Archetype:** Aerial controller / lantern attacker

Dustwing is mysterious compared with the Bee. It behaves like an eerie contaminated moth carrying its own unnatural light source rather than a direct aerial weapon.

## 2. Placement and Movement Class

**Placement:** FLYING

Does not require ground contact. Primary states include hover, flutter, slow aerial travel, fast travel, dash, vertical repositioning, lantern attack, hit drift, and recovery. Ground contact is exceptional/scripted.

## 3. Size, Scale, and Silhouette

**Relative class:** Small-to-medium aerial enemy.

Silhouette:

- Four visible wing surfaces
- Two large upper wings
- Two smaller lower wings
- Compact furry purple body
- Large black head
- Two huge glowing yellow eyes
- Two feathery antennae
- Pale fluffy neck collar
- Hanging illuminated lantern

The lantern is essential. Dustwing without the lantern is not the approved character.

## 4. Immutable Visual Anatomy

- Exactly two primary eyes
- Large oval yellow glowing eye surfaces
- Dark charcoal/black head
- Two feathery plume-like antennae
- Four visible wings: two larger forewings, two smaller rear wings
- Purple wing edges
- Pale tan/cream central wing fields
- Irregular purple markings and pale highlights
- Purple furry body
- Cream/white fuzzy collar around neck/thorax
- Six insect legs as anatomical basis, several obscured in poses
- No defining visible teeth

### Lantern

- Warm brass/brown construction
- Rounded glowing chamber
- Yellow-green luminous interior
- Dark contamination symbol in illuminated center
- Green-yellow aura
- Small hanging support/connection

The lantern is equipment, not anatomy.

## 5. Color, Material, and Surface Treatment

Primary palette:

- Deep violet
- Purple
- Lavender
- Cream
- Warm beige
- Charcoal
- Black
- Brass brown
- Acidic yellow-green

Wings are soft, powdery, worn, slightly translucent at thin edges, and never glossy dragonfly-like surfaces. Body remains furry. Lantern glow is sickly yellow-green, not ordinary warm candlelight.

## 6. Character Personality and Intent

Dustwing is curious, mesmerized, erratic, dreamlike, territorial around light, easily distracted, and dangerous without appearing openly furious.

Dustwing floats and wanders. During aggression, the lantern becomes the focal point and the creature's movement organizes around it.

## 7. Gunk Transformation and Backstory

Dustwing's transformation began with light. A contaminated discarded outdoor lantern/garden light attracted an ordinary moth. Repeated exposure coated wings in contaminated residue and altered natural phototaxis until the moth became obsessed with possessing the light.

The lantern now travels with the creature. Gunk also altered powdery wing scales, so each flutter sheds traces of luminous contamination.

The name Dustwing reflects the contaminated dust/light it leaves behind.

## 8. Movement and Navigation Behavior

### Idle / Hover

Wing cycle, body rise/fall, lantern swing, antenna response, active glow. Lantern motion should lag body movement.

### Slow Fly / Flutter

Irregular motion with vertical changes, small acceleration changes, gentle bobbing, and slight pauses. Avoid perfect straight lines.

### Fast Fly / Dash

Low horizontal profile, wings trail back, yellow-green light/motion effects stretch behind. Lantern follows momentum rather than hanging perfectly vertical.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Gunk Lantern Swing

Dustwing actively manipulates/swings the lantern. This is not a generic projectile attack.

**Windup:** stabilize hover, pull lantern close/back, angle toward player, intensify glow.  
**Active:** swing/throw lantern outward through a broad glowing arc.  
**Recovery:** lantern swings back beneath body and Dustwing absorbs momentum.

A passive wing-dust effect may be visual only. Do not silently turn it into a damaging hazard without gameplay approval.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Atmospheric entry: small yellow-green glow appears, lantern enters, Dustwing follows, wings spread, hover stabilizes.

### Exit

Angle upward/diagonally and flutter out, lantern trailing.

### Hit

Stars, disturbed wing posture, body displacement, lantern instability. Lantern swings violently but does not disappear.

### Defeat

Unstable hover, lantern swing, wing desynchronization, wobbling/spiraling retreat. Preserve whimsical tone.

## 11. Animation State Inventory

### Existing

- Idle / Hover
- Slow Fly / Flutter
- Fast Fly / Dash
- Attack
- Hit / React
- Effects

### Required expanded states

- Spawn Glow
- Entry
- Hover
- Curious Look
- Detect Player
- Reposition
- Flutter
- Fast Flight
- Dash Brake
- Lantern Windup
- Lantern Swing
- Lantern Follow-Through
- Lantern Recovery
- Turn
- Hit
- Dazed Hover
- Defeat
- Exit

## 12. Animation Construction and Modification Rules

Locked features:

- Two-eye design
- Eye color
- Four-wing silhouette
- Wing markings
- Purple body
- Cream neck collar
- Feathery antennae
- Lantern design
- Lantern glow color

Wing count/patterns must remain stable. Wing blur is allowed in fast motion but anatomy stays identifiable.

Treat lantern as a hanging secondary object affected by gravity, acceleration, deceleration, turning, and attack momentum.

For attack intermediates, track body center separately from lantern and plot the lantern swing arc before adding VFX.

## 13. Collision and Gameplay Readability

Core collider follows head/thorax/body, not full wing span. Lantern may receive temporary attack volume during active swing. Glow trail is not automatically damaging across its full visual bounds.

## 14. Effects and Environmental Interaction

Canonical effects:

- Lantern glow
- Yellow-green circular light
- Glowing particles
- Wing material
- Green contamination
- Gunk puddle
- Gunk impact into foliage/ground

Where technically practical, lantern can subtly illuminate nearby surfaces in stylized form.

## 15. Character Validation Checklist

Reject if:

- Lantern disappears or changes shape arbitrarily
- Eye glow changes color
- Extra eyes appear
- Wing count changes
- Wing markings regenerate randomly
- Cream collar disappears
- Antennae disappear
- Wings become glass-like
- Purple coloration is lost
- Fast flight becomes unrecognizable smear
- Lantern motion ignores body acceleration

---

# L2-E03: Skunk

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated skunk  
**Placement:** Ground  
**Archetype:** Area-control enemy

Primary intent is to create hazardous zones that temporarily change where the player can safely stand/move. The Skunk should not rely primarily on chasing.

## 2. Placement and Movement Class

**Placement:** GROUND

Quadrupedal states include idle, walk, run, brace, aim, spray, recover, retreat. The large tail is a major silhouette feature, not an independent locomotion system.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium.

Silhouette:

- Low stocky body
- Large arched tail
- Broad white stripe
- Small pointed face
- Improvised harness
- Portable metal canister/nozzle

Attack posture raises the tail and increases vertical silhouette.

## 4. Immutable Visual Anatomy

- Exactly two eyes
- Cream eye surfaces/dark pupils
- Two ears
- Dark nose
- Four legs
- Four paws
- Thick black/charcoal fur
- One very large bushy tail
- Broad white stripe across head/back/tail region
- Pale white facial/head accents
- Dirty textured coat

Canonical equipment:

- Purple/brown scavenged harness/vest
- Straps
- Patches
- Small skull-themed marking/emblem
- Improvised metal cylindrical canister/nozzle

The canister is canonical and may separate during strong reaction/defeat states.

## 5. Color, Material, and Surface Treatment

Primary palette:

- Black
- Charcoal
- Cream/off-white
- Dirty purple
- Brown
- Rust
- Gray metal
- Sickly olive-green gas

Fur remains dense, dirty, uneven, coarse-soft. Gas is yellow-green/olive, semi-transparent, dense in center, diffuse at edges. It should not look like fire smoke.

## 6. Character Personality and Intent

Defensive rather than predatory. Irritable, paranoid, easily threatened, smug when controlling space, and uninterested in prolonged pursuit.

Attitude: **You came too close. Now this entire area is your problem.**

## 7. Gunk Transformation and Backstory

Repeated contaminated scavenging altered the scent glands first. Natural spray became a lingering concentrated cloud. The Gunk transformed smell into something almost physical.

A cylindrical piece of refuse became a crude way to direct/concentrate the spray. The Skunk learned, through instinct or Gunk-enhanced problem solving, to use the metal opening as a stink cannon.

It believes everything should simply stay farther away.

## 8. Movement and Navigation Behavior

### Idle

Breathing, tail motion, eye tracking, gas wisps, equipment movement, weight shifts. Faint rear haze can remain visual characterization.

### Walk

Short-legged gait. Tail has significant inertia.

### Run

Body compresses/leans forward; tail stretches back; dust may appear. It should not run as aggressively as Dog. Repositioning exists to set up another spray.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Stink Spray

Canonical **ATTACK - STINK SPRAY**.

Telegraph:

1. Stop.
2. Raise tail.
3. Brace body.
4. Reposition canister.
5. Aim opening.
6. Increase small gas leakage.

Active cloud expands rapidly then lingers.

Gameplay function is temporary area denial. Possible tuned effects may include damage, slow, obscured visibility, forced displacement, or temporary unsafe region. Exact numbers are implementation tuning.

Small passive rear wisps are visual unless explicitly promoted into hazards.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Emerge from behind trash/cover. Small green cloud may precede body.

### Exit

Run/retreat into cover with tail trailing.

### Hit

Wide eyes, stars, compression, loss of composure. Canister may shift/detach on sufficiently strong reaction.

### Defeat

Heavy hit, canister falls/rolls, Skunk briefly collapses/dazes, then retreats/removes.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Walk
- Run
- Attack - Stink Spray
- Hit / React
- Effects

### Required expanded states

- Spawn / Entry
- Suspicious
- Detect Player
- Tail Raise
- Spray Windup
- Canister Aim
- Stink Spray Active
- Stink Spray Sustain
- Spray Recovery
- Hazard Maintenance
- Reposition
- Turn
- Hit
- Dazed
- Canister Drop
- Defeat
- Retreat
- Exit

## 12. Animation Construction and Modification Rules

Locked:

- White stripe pattern
- Tail proportions
- Eye design
- Harness
- Skull marking
- Metal canister
- Fur palette
- Body proportions

Tail is a large secondary mass and must retain volume. White stripe path remains logically continuous through body/tail motion.

Canister is rigid metal. It may rotate, bounce, drop, and roll, but may not stretch, melt, or change opening diameter/container identity.

Render gas separately.

## 13. Collision and Gameplay Readability

Body collider follows head, torso, main leg area. Do not include full raised tail.

Stink uses dedicated hazard volume. Visual cloud may exceed damage volume, but danger boundaries should remain understandable. Persistent cloud lifetime should be conveyed through opacity/motion.

## 14. Effects and Environmental Interaction

Canonical:

- Small gas clouds
- Large gas clouds
- Directed spray
- Swirling gas
- Bubble-like gas clusters
- Dust
- Leaves
- Trash
- Detached canister

Gas moves independently after release; do not keep it rigidly parented to the Skunk.

## 15. Character Validation Checklist

Reject if:

- Stripe changes randomly
- Tail becomes too small
- Canister disappears or becomes flexible
- Gas turns into ordinary white smoke
- Skunk becomes primarily a chase enemy
- Foot planting fails
- Harness changes significantly
- Green wisps are painted as fur
- Gas remains rigidly attached after firing

---

# L2-E04: Squirel

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated squirrel  
**Canonical project spelling:** Squirel  
**Placement:** Ground  
**Archetype:** Ranged projectile defender

Primary intent is to maintain distance and pressure the player with thrown acorns.

## 2. Placement and Movement Class

**Placement:** GROUND

Can inhabit ground paths, platforms, and raised ledges. Standard navigation: stand, walk, run, reposition, throw, recover. Do not automatically add wall/tree climbing without dedicated animation/gameplay approval.

## 3. Size, Scale, and Silhouette

**Relative class:** Small-to-medium.

Silhouette dominated by:

- Huge orange tail
- Small upright body
- Metal helmet
- Leafy helmet top
- Shoulder armor
- Acorn during attack preparation

Tail makes the character feel much larger than its torso.

## 4. Immutable Visual Anatomy

- Exactly two primary eyes
- Large cream/white eye surfaces
- Dark pupils
- Small dark nose
- Two ears anatomically, partially obscured by headgear in some poses
- Two arms
- Two legs
- Two feet
- One enormous bushy tail
- Orange/rust-red fur
- Cream belly
- Cream lower facial/muzzle region
- Small claws/hands in approved style

Canonical armor/clothing:

- Dented metal bucket/can-like helmet
- Leaf/twig vegetation protruding from top
- Green neck scarf/cloth
- Small metal shoulder armor
- Brown utility/armor details

Canonical projectile: brown acorn.

## 5. Color, Material, and Surface Treatment

- Burnt orange
- Rust red
- Warm brown
- Cream
- Muted green
- Dull gray/silver
- Dark brown

Acorn remains natural brown. Do not recolor every projectile green merely because the enemy is Gunk-mutated.

## 6. Character Personality and Intent

Overconfident, defensive, fussy, energetic, serious about a very silly job, and proud of improvised armor. The tiny pseudo-knight quality is intentional.

In Squirel's mind, an acorn is artillery.

## 7. Gunk Transformation and Backstory

Contaminated soil/roots altered buried acorn caches. Repeated exposure transformed normal food storage into territorial stockpiling. Acorns became possessions, then ammunition.

The Gunk increased strength enough to throw acorns with absurd force. Discarded metal became helmet/shoulder armor, foliage remained caught in equipment, and the Squirel became a tiny defender of a contaminated kingdom.

## 8. Movement and Navigation Behavior

### Idle / Stand

Tail movement, helmet bounce, eye scanning, acorn inspection, weight shifts, hand movement.

### Walk

Short steps with tail counterbalance.

### Run

Body lowers, tail extends backward, helmet/leaf details trail, dust appears.

### Ranged Repositioning

Preferred loop:

`Detect -> establish distance -> throw -> evaluate distance -> reposition -> throw again`

Do not endlessly backpedal while firing. Movement and throwing remain readable phases.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Nut Throw

Canonical **ATTACK - NUT THROW**.

Telegraph:

1. Produce/grip acorn.
2. Raise acorn.
3. Draw throwing arm back.
4. Rotate body slightly.
5. Track target with eyes.

At release, hand opens and acorn becomes separate projectile. White motion trail begins. Follow-through completes.

Projectile travels forward, may spin, stays brown, and creates dirt/leaf impact. Trajectory can be tuned but must remain readable.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Emerge quickly from leaves, shrubbery, debris, or level edge. Do not require tree climbing without dedicated assets.

### Exit

Lower body and rapidly run into foliage/off-screen.

### Hit

Stars, wide eyes, shock, compression, loss of throwing posture. Prepared acorn may drop.

### Defeat

Hit, helmet rings/wobbles, acorn drops, Squirel crouches dazed, then retreats. Helmet remains canonical.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Walk
- Run
- Attack - Nut Throw
- Hit / React
- Projectile & Effects

### Required expanded states

- Entry
- Detect Player
- Aim
- Acquire Acorn
- Throw Windup
- Throw Release
- Throw Follow-Through
- Throw Recovery
- Reposition
- Turn
- Skid
- Hit
- Projectile Interrupt / Drop
- Dazed
- Defeat
- Retreat
- Exit

### Projectile states

- Held Acorn
- Release
- Flight
- Spin
- Impact
- Break / Debris
- Despawn

## 12. Animation Construction and Modification Rules

Locked:

- Orange fur
- Cream belly
- Tail size
- Helmet
- Leaf detail
- Green scarf
- Shoulder armor
- Eye design
- Acorn design

Tail is major secondary motion: gentle in idle, counterbalance in walk, trails in run, counter-rotates during throw. Keep volume stable.

Helmet is rigid and may bounce/tilt/vibrate but may not stretch/change identity or lose leaf detail.

The acorn exists in one place at a time. Never leave it simultaneously in hand and in flight after release.

## 13. Collision and Gameplay Readability

Core collider follows head, torso, lower body. Tail remains outside primary collision. Acorn has independent collider. Motion trail and impact VFX do not automatically expand hit radius.

## 14. Effects and Environmental Interaction

Canonical:

- Static acorn
- Spinning acorn
- Projectile streak
- Curved streak
- Dirt impact
- Leaves
- Acorn fragments
- Ground debris
- Dust

Effects should reinforce outdoor/suburban physicality rather than magic.

## 15. Character Validation Checklist

Reject if:

- Tail becomes small
- Helmet/leaf/scarf/shoulder armor disappears
- Helmet changes design
- Acorn becomes slime
- Extra limbs appear
- Duplicate acorns appear in a throw frame
- Hand/release position does not align
- Projectile trail disconnects from ball
- Character begins climbing without approved state

---

# L2-E05: Bee

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated bee  
**Placement:** Flying  
**Archetype:** Venom dash flyer

The Bee patrols aerial lanes and commits to high-speed forward attacks. It is more direct and organized than Dustwing or Mosquito.

## 2. Placement and Movement Class

**Placement:** FLYING

States include hover, slow flight, patrol, fast flight, alignment, dash, venom attack, brake, reposition. It does not require terrain and remains aerial during normal combat.

## 3. Size, Scale, and Silhouette

**Relative class:** Small-to-medium flying enemy.

Key silhouette:

- Compact round insect body
- Black and golden-orange banding/fur
- Two large pale visible wings
- Oversized eyes
- Riveted metal head armor
- Forward-facing metal nozzle/proboscis
- Multiple tucked insect legs

Dense and armored compared with Dustwing.

## 4. Immutable Visual Anatomy

- Exactly two oversized primary eyes
- Cream/white eye surfaces
- Dark pupils
- Heavy angry brows
- Golden-orange/yellow face
- Dark charcoal/black body
- Warm orange/golden fuzzy banding
- Six insect legs as anatomical basis, some occluded
- Two large visible pale wings in approved silhouette
- Visible wing veins
- Dark body hairs/fuzzy texture
- Paired antennae integrated around head/helmet region
- No defining visible teeth

Canonical metal equipment:

- Dark gray metal head armor
- Rivets/studs
- Rust/orange wear
- Protruding rods/antenna elements
- Forward metal nozzle/proboscis assembly

Bright green Gunk drips from the front nozzle.

Do **not** add a major rear stinger simply because the creature is a bee. The front contaminated nozzle is the approved weapon silhouette.

## 5. Color, Material, and Surface Treatment

- Charcoal
- Black
- Golden yellow
- Burnt orange
- Cream
- Pale beige wings
- Dirty silver
- Rust
- Bright chartreuse Gunk

Wings are pale, slightly translucent, veined, and warm-toned. Body remains fuzzy/uneven. Armor is riveted, scratched, tarnished, industrial, and dirty.

## 6. Character Personality and Intent

Aggressive, focused, militaristic, territorial, fast, short-tempered, and unwilling to disengage once committed. Personality comes from eyes, brow, head angle, alignment, and sudden acceleration.

The Mosquito is irritating. The Bee is angry.

## 7. Gunk Transformation and Backstory

Contaminated flowers, pollen, nectar, water, and plant surfaces exposed the Bee repeatedly. Defensive hive instincts intensified into aggressive patrol behavior. Body became denser and fur coarser. Mouthparts/venom changed.

A discarded metal fitting became incorporated around the front of the face through Gunk-mediated fusion, forming a crude nozzle. Contaminated fluid accumulates behind it and leaks constantly.

The Bee turns its entire body into a delivery mechanism for Gunk during attack.

## 8. Movement and Navigation Behavior

### Idle / Hover

Small vertical bob, wing cycling, nozzle drip, antenna motion, minor leg movement, focused eyes.

### Slow Fly

Controlled, lane-oriented patrol. More stable than Dustwing.

### Fast Fly / Dash

Body narrows horizontally, wings smear backward, green contamination trails. Build momentum visibly.

Preferred flow:

`Hover -> Detect -> Align -> Windup -> Dash -> Brake -> Reposition`

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Venom Dash

Unified signature attack combining body acceleration with forward Gunk emission.

#### Alignment

Turn toward player trajectory.

#### Windup

Pull slightly backward, intensify wings, build circular speed effect, accumulate green fluid at nozzle.

#### Attack

Launch forward at high speed while green venom/Gunk projects from front nozzle. Threat includes both body path and forward contaminated stream.

#### Follow-Through

Travel beyond target line rather than stopping instantly.

#### Brake

Flare wings, reduce speed, return to hover.

Idle drips may be visual only. Do not automatically turn them into projectiles.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Green speed streak appears; Bee races into frame, slightly overshoots patrol point, brakes, and enters hover.

### Exit

Align to off-screen route and dash out.

### Hit

Stars, shocked eyes, body displacement, interrupted attack focus. Green residue may shake loose.

### Defeat

Hit, unstable wings, spin/roll, green droplets, fall or uncontrolled acceleration out of play. Avoid realistic insect death.

## 11. Animation State Inventory

### Existing

- Idle / Hover
- Slow Fly
- Fast Fly / Dash
- Attack
- Hit / React
- Effects

### Required expanded states

- Entry Dash
- Entry Brake
- Hover
- Patrol
- Detect Player
- Align
- Attack Windup
- Spin / Charge
- Venom Dash
- Dash Follow-Through
- Brake
- Recovery
- Turn
- Hit
- Dazed Flight
- Defeat
- Exit Dash

## 12. Animation Construction and Modification Rules

Locked:

- Two-eye design
- Golden/black palette
- Visible wing arrangement/shape
- Metal helmet
- Rivet language
- Front nozzle
- Green venom color
- Body proportions

Wing blur is allowed but roots remain consistent and permanent extra wings cannot appear.

Nozzle is rigid, front-mounted, stable in diameter/attachment, and never becomes rear stinger or different weapon.

Dash interpolation:

1. Start from approved hover/attack anchors.
2. Pitch body forward progressively.
3. Compress silhouette slightly through pose, not scale distortion.
4. Sweep wings back.
5. Increase motion blur.
6. Preserve eye direction.
7. Keep nozzle aimed forward.
8. Begin Gunk trail.
9. Enter full attack pose.
10. Reverse during braking.

## 13. Collision and Gameplay Readability

Core collider follows head, thorax, abdomen, not full wings. Venom Dash uses separate active volumes for Bee body and forward Gunk/venom. Speed streaks are visual only.

## 14. Effects and Environmental Interaction

Canonical:

- Green droplets
- Green splashes
- Venom/Gunk streak
- Wing blur
- White circular motion effect
- Ground impact
- Leaves
- Dirt
- Large green splash/explosion

A missed dash can produce a strong designated terrain impact.

## 15. Character Validation Checklist

Reject if:

- Front nozzle disappears/moves rearward
- Large new rear stinger appears
- Golden/black banding is lost
- Eye proportions change
- Extra permanent wings appear
- Green venom changes color
- Helmet becomes smooth/clean
- Dash is made by sprite stretching
- Wings remain static across speed change
- Attack stops communicating forward commitment
- Motion effects become permanently baked into idle art

---

# Level 2 Global Animation Production Contract

All Level 1 production rules remain active.

Additional Level 2 requirements:

1. Approved sheets remain untouched source material.
2. New files are derivatives/extensions, never overwrites.
3. Every new frame uses at least one canonical anchor.
4. Keep character, equipment, projectile, foreground VFX, background VFX, ground effects, and shadows separate where practical.
5. Never squash sprites to fit frame bounds.
6. Ground enemies use stable ground-relative roots; flying enemies use stable body-center roots.
7. PNG bounds are not collision bounds.
8. Preserve secondary motion: Dog ears/tail/scrap, Dustwing lantern/antennae/wings, Skunk tail/canister, Squirel tail/helmet vegetation, Bee wings/antennae/venom.
9. Preserve surface continuity: fur patches, stripe paths, wing markings, metal dents, rivets, clothing, leaves, tags, symbols, equipment placement.
10. Do not blindly mirror asymmetric art.
11. Validate transparency edges for red/yellow/white/dark fringe, cropped particles, ears, tails, wings, and other fine features.
12. Gameplay-scale validation is mandatory in uninterrupted gameplay.

## Level 2 Cross-Roster Validation

- Dog must communicate pursuit and physical aggression.
- Dustwing must communicate fluttering aerial control and lantern-based behavior.
- Skunk must communicate persistent space contamination.
- Squirel must communicate ranged projectile pressure.
- Bee must communicate fast directional aerial assault.

If two enemies begin producing the same player behavior despite different artwork, implementation has drifted from canon.
