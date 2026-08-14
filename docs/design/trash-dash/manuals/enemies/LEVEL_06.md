# Trash Dash HD Remake - Enemy Master Specification v1.5
## Secret Level 6: Abandoned Ballpark

**STATUS: APPROVED / LOCKED CANON**

Secret Level 6 uses baseball behavior as environmental adaptation. These animals are not merely wearing sports costumes and do not need to understand baseball as humans did. Stadium artifacts and spaces have shaped movement, territory, combat, and survival behavior.

## Secret Level 6 Enemy Ecology

| Enemy | Placement | Core archetype | Primary player pressure |
|---|---|---|---|
| Baserunning Beaver | Ground | Speedy slider / charge enemy | Low horizontal rushes and committed slides |
| Clobbering Cub | Ground | Heavy melee hitter | Large swing arcs, timing, miss-recovery windows |
| Sliding Seagull | Flying + ground skim | Dive-bomber | Vertical tracking, dive timing, low fly-by attacks |
| Windup Weasel | Ground | Ranged pitcher | Arcing projectiles, fastballs, distance control |

Core identities:

- Beaver slides.
- Cub swings.
- Seagull dives.
- Weasel pitches.

---

# SL6-E01: Baserunning Beaver

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated beaver  
**Placement:** Ground  
**Archetype:** Speedy slider / low charge enemy

The canonical sheet describes a Beaver mutant that loves to play ball, especially when it involves sliding headfirst into trouble. The defining combat behavior is **sliding**, not generic charging.

Canonical player read:

- Standing Beaver = manageable.
- Crouched Beaver = slide incoming.
- Sliding Beaver = clear the lane.

## 2. Placement and Movement Class

**Placement:** GROUND

Supports standing, walking, patrolling, running, charging, crouching, belly sliding, quick turning, slide recovery, tumbling. Slide requires a continuous ground surface and should remain visibly connected to dirt, concrete, grass, or other approved surface.

Preferred flow:

`Idle -> patrol -> detect -> run/charge -> crouch -> slide start -> full slide -> slide recovery`

Quick turn may follow overshoot/change of direction.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium-to-large standard enemy.

Key silhouette:

- Large rounded head
- Broad muzzle
- Large protruding front incisors
- Low muscular torso
- Four heavy limbs
- Large flat beaver tail
- Baseball cap
- Dirty jersey
- Forward-heavy stance

During full slide the body becomes dramatically lower/longer while head, cap, teeth, torso, and flat tail remain recognizable.

## 4. Immutable Visual Anatomy

### Visual Canon

- Exactly two primary eyes
- Large pale yellow/cream eye surfaces
- Dark pupils
- Heavy dark brows
- Two small rounded ears partially obscured by fur/headwear
- Broad rodent muzzle
- Dark nose
- Long whiskers
- Two very large front incisors
- Smaller teeth in aggressive expressions
- Four limbs
- Four clawed paws
- Long dark claws
- One extremely large flat beaver tail
- Dense shaggy brown fur
- Dark brown outer coat
- Lighter gray/tan chest/shoulder areas
- Scruffy raised back fur

### Tail

Broad, flat, dark brown/charcoal, crosshatched/scaled, large relative to body. Canonical detail: **BEAVER TAIL RUDDER**. It is important to turning and slide stability.

### Baseball Equipment

- Dark blue/teal cap
- Light-colored **B** marking
- Worn/dirty cap
- Torn/patched baseball jersey
- Pale gray/cream fabric
- Dark lettering/markings
- Purple/dark accent material around damaged areas
- Wrist bands on forearms
- Dark teal/blue worn bands
- Cleat-like/heavily clawed feet suitable for digging into dirt

Do not clean up the uniform.

## 5. Color, Material, and Surface Treatment

- Dark brown
- Warm brown
- Gray-brown
- Dirty cream
- Charcoal
- Dark blue/teal
- Muted purple
- Warm yellow eyes
- Dirty white baseball leather
- Red stitching

Fur is thick, shaggy, dirty, uneven, and matted. Jersey is torn, patched, stained, frayed, and ground into stadium dirt. Cap is worn/scratched/misshapen.

Canonical baseballs are scuffed, chewed, dirty white, brown-stained, red-stitched, never pristine.

## 6. Character Personality and Intent

Competitive, excitable, reckless, physical, proud of speed, easily baited, more interested in reaching a destination than avoiding obstacles.

It sees open horizontal stretches as running lanes. Once a slide begins, self-preservation becomes secondary. Core thought: **Get there first.**

## 7. Gunk Transformation and Backstory

Beavers colonized stadium structures long after human maintenance stopped. Wood, benches, signs, dugouts, sod, drainage, and equipment became nesting/building material.

The Gunk exaggerated environmental manipulation and altered speed/territorial behavior. Caps became protection, fabric became nesting/protection, straps became forelimb guards.

The long dirt paths rewarded dropping into a belly slide. The flat tail became a steering surface. Repeated Gunk adaptation reinforced the behavior until baselines became **highways** rather than relics of sport.

## 8. Movement and Navigation Behavior

### Idle / Stand

Breathing, whiskers, tail, cap, eyes, paw flex, tooth/mouth motion.

### Walk / Patrol

Heavy quadruped movement with body weight, claw contact, tail counterbalance, jersey/fur secondary motion.

### Run / Charge

Body lowers, front paws reach, rear legs drive, tail trails, dirt displaces.

### Anticipation / Crouch

Mandatory attack telegraph:

1. Drop chest.
2. Pull limbs in.
3. Lower head.
4. Align body horizontally.
5. Brace claws.
6. Adjust tail.
7. Focus travel direction.

### Quick Turn

Use paw planting, tail swing, dirt scrape, and body lean. No instant rotation around a fixed point.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Full Sliding Attack

Canonical **SLIDE ATTACK START** -> **FULL SLIDING ATTACK**.

Slide start uses a final rear-leg burst and lowered front body. Full slide travels rapidly on belly, with attack pressure concentrated around head, shoulders, front torso.

Dirt spray, pebbles, speed streaks, and scrapes reinforce motion.

Slide is highly committed. Tail may allow limited correction but never homing-style steering.

Environmental collision can create stronger impact and recovery.

### Baseball Props

Sheet includes hurled baseball and optional ball bag, but no canonical throwing animation exists in the character sequence. Therefore baseball throwing is **not** part of the locked primary moveset until dedicated approved animation exists.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Walk/charge in visibly before first slide so scale and normal silhouette read.

### Slide Recovery

Body slows, torso rises, paws regain contact, dirt settles, Beaver stands. Do not jump directly from flat slide to idle.

### Hit / React

Stars, startled expression, recoil, loss of balance, possible tumble.

### Stunned

Collapses low with stars and vulnerability.

### Recovery

Shake off, reposition limbs, raise head, return to stance.

### Defeat / Tumble-Out

Loss of control, body rotation, possible cap separation late in sequence, dirt/debris, final sprawled pose. Cap separation is defeat-specific, not permission to omit it during standard states.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Walk / Patrol
- Run / Charge
- Anticipation / Crouch
- Slide Attack Start
- Full Sliding Attack
- Slide Recovery
- Quick Turn
- Hit / React
- Stunned
- Recovery
- Defeat / Tumble-Out
- Effects
- Props

### Required expanded states

- Entry
- Idle
- Detect Player
- Patrol
- Run Start
- Run
- Charge Acceleration
- Crouch Telegraph
- Slide Launch
- Early Slide
- Full Slide
- Slide Impact
- Slide Deceleration
- Slide Recovery
- Quick Turn Anticipation
- Quick Turn
- Re-Engage
- Hit / Heavy Hit
- Stunned
- Recovery
- Defeat Tumble
- Cap Separation
- Final Dazed
- Retreat / Exit if applicable

## 12. Animation Construction and Modification Rules

Locked:

- Two-eye design
- Large incisors
- Flat tail
- Four-legged anatomy
- Fur palette
- Cap
- **B** marking
- Jersey
- Wrist bands
- Body proportions

Maintain planted paws, shoulder/hip motion, spine stability, tail counterbalance.

Do not squash the standing sprite into a slide. Pose torso, limbs, spine, head, and tail properly.

Tail may drag/sweep/lift/rotate/absorb impact but cannot shrink, become furry/cylindrical, or disappear.

Dirt/slide VFX remain separate where practical.

## 13. Collision and Gameplay Readability

Standard collider follows head/chest/torso/central limbs, not tail. Slide collider lowers/elongates with actual body, with attack volume concentrated around forward mass. Dirt spray is not damaging by default. Stunned collider follows lowered body.

Baseball props use independent collision only when gameplay-relevant.

## 14. Effects and Environmental Interaction

Canonical:

- Dirt sprays
- Infield dust
- Skidding streaks
- Spit-up pebbles
- Claw scrapes
- Slide impact bursts

Surface matters. Infield dirt can produce strong spray; concrete should not produce identical dirt effects.

## 15. Character Validation Checklist

Reject if:

- Limb count changes
- Incisors disappear
- Tail becomes small/cylindrical
- Cap marking changes
- Jersey becomes clean
- Slide uses sprite squashing
- Beaver hovers during slide
- Full slide turns sharply/homes
- Dirt hides silhouette
- Cap disappears during normal gameplay
- Baseball throwing is added without canonical animation
- Recovery jumps from slide directly to standing

---

# SL6-E02: Clobbering Cub

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated bear cub  
**Placement:** Ground  
**Archetype:** Heavy melee hitter

The Cub combines a stocky body, surprising speed, and an oversized weapon. It is not merely a slow tank. Missed attacks and heavy recovery create fair vulnerability windows.

## 2. Placement and Movement Class

**Placement:** GROUND

Primarily bipedal anthropomorphic bear. Supports stand, walk, patrol, run, charge, ready stance, swing anticipation, side swing, overhead swing, miss recoil, bat-drag recovery, stomp, taunt. No quadruped locomotion without separate design approval.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium-to-large heavy enemy.

Key silhouette:

- Large rounded helmet
- Rounded bear ears
- Broad bear head
- Heavy shoulders
- Thick torso
- Short powerful legs
- Oversized wooden bat
- Large paws
- Protective baseball equipment

The bat is nearly as important to silhouette as the Cub itself. Attack arcs must remain readable without hiding the body.

## 4. Immutable Visual Anatomy

### Cub

- Exactly two primary eyes
- Pale cream eye surfaces
- Dark pupils
- Heavy expressive brows
- Two rounded bear ears
- Broad bear muzzle
- Large black nose
- Cream/tan muzzle
- Visible white teeth
- Two arms
- Two legs
- Large paw-like hands
- Large feet
- Brown fur
- Dark brown outer coat
- Lighter brown/tan face/belly
- Thick stocky build
- No long tail

### Helmet

- Dark rusty red
- Heavy rounded shell
- Damaged, scratched, cracked
- Pale **C** marking
- Bear-ear accommodation
- Worn low
- Scuffed paint and chin strap

### Jersey / Protective Gear

- Torn dirty pale cream/gray jersey
- Stitched patches
- Protective torso padding
- Leather/metal gear
- Belts
- Arm bands/pads
- Leather straps
- Metal studs
- Sewn repairs

### Bat

- Oversized wood
- Thick
- Dirty
- Chipped/dented
- Tape repairs
- Metal reinforcement
- Barbed/studded nails/spikes

Canonical callout: **Barbed nails, tape, dented wood.** Never replace with a clean bat.

## 5. Color, Material, and Surface Treatment

- Dark brown
- Medium brown
- Dirty tan
- Dirty cream
- Rust red
- Dark gray
- Leather brown
- Dull steel

Fur is thick/scruffy/dirty/matted. Bat shows splinters, dents, tape, metal, embedded nails. Helmet paint is scraped/chipped/cracked/faded, never glossy sporting gear.

## 6. Character Personality and Intent

Loud, competitive, confident, easily excited, proud of strength, impatient, playful in a dangerous way. It enjoys swinging almost more than hitting.

Canonical celebratory stomp/taunt supports posing and showing off. Ego is a weakness; missed swings frustrate and expose it.

## 7. Gunk Transformation and Backstory

Bears found shelter/food in concession storage, garbage areas, maintenance rooms, and buried stadium waste. Gunk-exposed young bears became unusually adept with human objects.

One Cub dragged/chewed a damaged bat, then gained the coordination/strength to lift and swing it. The weapon was repeatedly repaired with tape, metal, nails, and scrap as impacts damaged it.

Protective equipment made the behavior survivable. The Cub never learned baseball. It learned one rule: **Swing hard.**

## 8. Movement and Navigation Behavior

### Idle / Stand

Heavy breathing, bat repositioning, helmet adjustment, eye tracking, shoulders, foot shift, annoyed huff. Bat weight affects posture.

### Walk / Patrol

Weapon load creates asymmetric lean and delayed follow-through.

### Run / Charge

Aggressive acceleration, foot dust, bat trails behind.

### Ready Stance

Clearly transitions locomotion into attack preparation.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Side Swing

Canonical **BACKSWING ANTICIPATION** -> **SIDE SWING ATTACK**.

Windup rotates torso, plants feet, draws bat back, keeps eyes on target. Active swing follows a wide horizontal arc. Follow-through continues shoulders, torso, arms, and bat beyond target point.

### Secondary Attack: Overhead Swing

Canonical **OVERHEAD SWING VARIATION**. Raises weapon, delivers vertical ground-impact attack with debris/wood effects.

### Missed Swing Recoil

Canonical vulnerability. Momentum carries body past target, feet adjust, balance breaks, weapon drags.

### Bat Drag Recovery

Heavy bat scrapes ground during reposition. This is a usable recovery window.

### Celebratory Stomp / Taunt

Can occur after successful hit or scripted moment. Do not overuse to the point of harming combat pacing.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Enter dragging/carrying bat. Scrape sound can precede visual arrival.

### Hit / React

Body recoil, bat displacement, impact effect, unstable posture. Bat remains physically connected to hands unless an explicit disarm exists.

### Stunned

Upright/dazed with stars and vulnerability.

### Recovery

Shake off, reset feet, regrip bat.

### Defeat / Topple

Heavy fall; bat lands beside/beneath; stars/daze may remain. Helmet and bat remain recognizable in final pose.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Walk / Patrol
- Run / Charge
- Ready Stance
- Backswing Anticipation
- Side Swing Attack
- Overhead Swing Variation
- Missed Swing Recoil
- Bat Drag Recovery
- Celebratory Stomp / Taunt
- Hit / React
- Stunned
- Recovery
- Defeat / Topple
- Props & Gear
- Effects & Impacts

### Required expanded states

- Entry
- Idle
- Bat Adjustment
- Patrol
- Detect Player
- Run Start / Charge
- Ready Stance
- Side-Swing Windup / Active / Follow-Through
- Overhead Windup / Active / Ground Impact / Follow-Through
- Missed Swing / Off-Balance Recoil
- Bat Drag / Recovery
- Successful-Hit Taunt / Stomp
- Hit / Heavy Hit
- Stunned / Recovery
- Defeat Topple / Final Dazed
- Exit if applicable

## 12. Animation Construction and Modification Rules

Locked:

- Bear head proportions
- Rounded ears
- Black nose
- Two-arm/two-leg anatomy
- Stocky body
- Helmet and **C** marking
- Jersey/gear
- Bat dimensions/damage details

Canonical note: **Bat is heavier than cub, use weight in arcs and follow-through.** This is a critical rule.

Backswing rotates shoulders/hips and braces feet. Follow-through continues body after contact point.

Bat nail/tape/metal/barrel details remain consistent. Do not rotate the entire flat sprite around center to simulate swing; pose shoulders, elbows, wrists, hips, knees, feet individually.

## 13. Collision and Gameplay Readability

Body collider follows head/torso/lower body. Bat attack collider follows actual weapon only during active frames. Idle bat is not constantly damaging.

Side swing uses broad horizontal attack region. Overhead is narrower horizontally with strong vertical/impact region. Attack collider deactivates during recovery so player can punish misses.

## 14. Effects and Environmental Interaction

Canonical:

- Bat swing arcs
- Wood impact bursts
- Dust stomps
- Claw scrapes
- Splinter chips

Stadium props include baseball, catcher mask, soda can, home plate, but these are environmental props, not anatomy.

## 15. Character Validation Checklist

Reject if:

- Long tail appears
- Helmet marking changes
- Bat becomes clean
- Bat scale changes between frames
- Weapon feels weightless
- Swing lacks anticipation/follow-through
- Whole-sprite rotation substitutes for posed swing
- Attack collider remains active during recovery
- Bat disappears on hit
- Cub becomes quadrupedal without approval
- Taunt constantly interrupts combat
- Helmet/jersey/pads regenerate inconsistently

---

# SL6-E03: Sliding Seagull

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated seagull  
**Placement:** Flying + temporary ground skim  
**Archetype:** Dive-bomber

Canonical profile:

- **ROLE: AERIAL ENEMY / DIVE ATTACKER**
- **THREAT: MEDIUM**
- **SPEED: FAST IN DIVE**
- **SIZE: MEDIUM**
- **WEAKNESS: WELL-TIMED HITS DURING DIVE OR RECOVERY**

## 2. Placement and Movement Class

### Primary

**FLYING**

Hover, patrol, flap, bank, target alignment, dive, pull-up.

### Secondary

**GROUND SKIM / TEMPORARY CONTACT** during end of dive. This does not turn it into a standard ground enemy.

### Tertiary

**PERCH / SHORT LANDING** on approved rails, ledges, stadium structures, narrow surfaces.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium aerial enemy.

Key silhouette:

- Large gray wings
- White-gray body
- Long orange beak
- Orange talons
- Blue baseball helmet
- Loose chin strap
- Tattered jersey material
- Tail feathers

Dive silhouette tucks wings, leads with head/beak, narrows body, aligns tail, and keeps helmet readable. Canonical callout: **TUCKS IN & ANGLES BEAK**.

## 4. Immutable Visual Anatomy

- Exactly two anatomical eyes
- Pale yellow/cream eye surfaces
- Dark pupils
- Two wings
- Two legs
- Two taloned feet
- Long orange/yellow beak
- No mammalian teeth
- White/gray body feathers
- Dark gray layered wing feathers
- Dark wing tips
- Tail feathers
- Feather tufts around neck/body

### Helmet

- Dark blue/teal
- Dirty/scratched/worn
- Pale **S** marking
- Loose chin strap

Canonical: **LOOSE CHIN STRAP FLAPS IN WIND**.

### Jersey

Tattered jersey fragment with red/maroon **15** marking. Number and garment language remain stable.

## 5. Color, Material, and Surface Treatment

- Dirty white
- Light gray
- Dark gray
- Charcoal
- Orange beak/talons
- Dark blue/teal helmet
- Brown leather strap
- Muted red/maroon jersey
- Pale yellow eyes

Feathers are layered, dirty, wind-worn, uneven, slightly ragged. Helmet is scuffed/matte. Jersey is torn/dirty/frayed.

## 6. Character Personality and Intent

Territorial, loud, arrogant, aggressive, opportunistic, confident in air, somewhat clumsy during recovery. Stadium airspace is territory. It enjoys the dive and ground skim almost like showing off.

## 7. Gunk Transformation and Backstory

Abandoned stadiums offered gulls food remnants, garbage, nesting ledges, open roofs, structural perches, and fields. Gunk amplified aggression and flight behavior.

Helmet fragments became protection and jersey fabric became nesting debris that stayed attached. The field rewarded steep diving followed by low fast skimming along smooth/worn surfaces before pull-up.

The creature does not understand baseball. It has learned: **Dive low. Stay fast. Pull up before the wall.**

## 8. Movement and Navigation Behavior

### Idle Hover

Small vertical motion, strong wing beats, loose strap response.

### Patrol Flight

Smooth horizontal/gently arcing travel. Less frantic than Mosquito.

### Flap Cycle

Use canonical wing-position anchors rather than regenerating arbitrary wing poses.

### Banking Turn

Body roll, asymmetric wing positions, head/tail corrections. Do not rotate unchanged flight sprite.

### Alert / Target-Lock

Notice, stabilize, track player, adjust orientation, communicate attack path.

### Dive Anticipation

Wings tuck, head lowers, beak aligns, body pitches.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Diving Attack

Alert/target-lock -> dive anticipation -> acceleration -> ground approach.

### Ground Skim / Slide

Canonical low horizontal continuation with dirt/debris/streaks. It is short-lived and should not become indefinite ground locomotion.

### Pull-Up Recovery

Spread wings, convert forward momentum into altitude. Recovery is a canonical vulnerability window.

### Perch

Land with actual talon contact, not a frozen flying sprite hovering above rail.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Enter from above or stadium perch; distant wing/call may precede.

### Hit / React

Feather displacement, unstable flight, body roll, helmet instability, stars/effects.

### Stunned

Collapse to ground/low unstable state with stars.

### Recovery

Shake off, spread wings, restore posture, relaunch.

### Defeat / Crash-Out

Loss of flight, chaotic rotation, ground collision, feathers/debris, helmet separation, final dazed crash. Helmet separation is defeat-specific.

## 11. Animation State Inventory

### Existing

- Idle Hover
- Patrol Flight
- Flap Cycle
- Banking Turn
- Alert / Target-Lock
- Dive Anticipation
- Diving Attack
- Ground Skim / Slide
- Pull-Up Recovery
- Perch / Short Landing
- Hit / React
- Stunned
- Recovery
- Defeat / Crash-Out
- FX & Effects

### Required expanded states

- Perched Entry / Flight Entry
- Idle Hover
- Patrol
- Flap Cycle
- Bank Left / Right
- Detect Player / Target Lock
- Dive Windup / Start / Acceleration / Full Dive
- Ground Approach / Ground Skim / Skim Impact
- Pull-Up Start / Pull-Up / Recovery Flight
- Perch Approach / Landing / Perch Idle / Relaunch
- Hit / Heavy Hit
- Stunned / Ground Recovery
- Defeat Fall / Crash / Helmet Separation / Final Dazed
- Exit

## 12. Animation Construction and Modification Rules

Locked:

- Two-wing anatomy
- Eye treatment
- Orange beak/talons
- Feather palette
- Helmet and **S**
- Chin strap
- Jersey and **15**

Use approved flap anchors. No extra/missing wings or changed wing roots.

Bank through body roll, wing asymmetry, head correction, tail correction, not whole-sprite rotation.

Chin strap trails/flutters/swings with wind/momentum while remaining attached.

Do not stretch bird for speed. Use pose, wing tuck, streaks, body angle, effect layers.

## 13. Collision and Gameplay Readability

Flight collider follows head/chest/torso, excluding full wings. Dive collider follows forward body/beak region. Ground-skim collider lowers with body. Ground debris is visual. Attack collider deactivates during intended recovery vulnerability.

## 14. Effects and Environmental Interaction

Canonical:

- Feather burst
- Whoosh trail
- Dive arc guide
- Trash scraps
- Wing-flap gust
- Ground dust/skid
- Impact puff
- Stars/daze

Keep feather effects modest enough to preserve silhouette. Surface type should affect ground skim VFX.

## 15. Character Validation Checklist

Reject if:

- Extra wings appear
- Helmet disappears during normal movement
- Chin strap disconnects
- Jersey number changes
- Seagull becomes permanently ground-based
- Ground skim becomes hovering
- Dive lacks target-lock telegraph
- Full dive makes impossible instant turns
- Pull-up has no recovery interval
- Banking uses whole-sprite rotation only
- Helmet detaches before defeat without cause
- Wings become unreadable inside speed effects

---

# SL6-E04: Windup Weasel

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated weasel  
**Placement:** Ground  
**Archetype:** Ranged pitcher

Canonical profile:

- Ranged enemy
- Throws baseballs in an arc
- Quick and nimble
- Carries extra balls
- Weak in close combat

The Weasel should encourage the player to close distance.

## 2. Placement and Movement Class

**Placement:** GROUND

Supports stand, walk, patrol, quick scamper, aim, windup, throw, follow-through, retrieve/pull next ball, recover. Prioritizes distance management. No default climbing/jumping without dedicated approved states.

## 3. Size, Scale, and Silhouette

**Relative class:** Small-to-medium ranged enemy.

Key silhouette:

- Long narrow weasel head
- Pointed muzzle
- Large ears
- Long curved tail
- Upright bipedal posture
- Baseball cap
- Tattered jersey
- Baseball in throwing hand
- Bag of extra baseballs

Tail is major counterbalance during throws.

## 4. Immutable Visual Anatomy

- Exactly two primary eyes
- Pale cream eye surfaces
- Dark pupils
- Heavy brows
- Two pointed/rounded ears
- Long narrow muzzle
- Dark nose
- White whiskers
- Sharp white teeth
- Two arms
- Two legs/feet
- Long flexible fur-covered tail
- Brown/gray fur
- Dark facial mask-like shading
- Pale muzzle/throat/chest
- Lean narrow body

### Tail

Long, flexible, expressive. Canonical animator note: **TAIL IS EXPRESSIVE - USE IT FOR BALANCE AND EMOTION.**

### Cap

Dark olive-green with pale **W**, worn/scuffed, short bill.

### Jersey

Dirty, torn, pale gray/cream, dark/red markings, frayed and loose.

### Baseball Bag

Brown leather/canvas-like worn pouch, open enough for multiple balls to remain readable, secured to body. Remains part of standard silhouette.

## 5. Color, Material, and Surface Treatment

- Dark brown
- Medium brown
- Gray
- Dirty cream
- Olive green
- Muted red
- Black
- Dirty white baseballs
- Red stitching

Fur is coarse/scruffy/dirty. Jersey is thin/torn/stained/weathered. Baseballs remain scuffed/worn rather than pristine.

## 6. Character Personality and Intent

Clever, cocky, precise, fast, nervous when approached, proud of pitching, highly expressive. Confidence collapses into frantic repositioning at close range.

Character summary: **brilliant pitcher, terrible brawler.**

## 7. Gunk Transformation and Backstory

Weasels naturally rely on speed, precision, direction changes, and timing. Baseballs throughout equipment rooms/dugouts/field became nesting objects/toys. Gunk strengthened forelimbs and coordination.

A thrown baseball revealed a major survival advantage: hit something before getting close. Balls became ammunition; bags became storage; uniforms became protection. Over generations, pitching became a refined predatory adaptation.

They never learned innings or strikes. They learned: **Arc means reach. Speed means impact. Another ball means another chance.**

## 8. Movement and Navigation Behavior

### Idle / Stand

Baseball handling, tail motion, ear twitch, eye tracking, bag adjustment, ball inspection, weight shifts. Usually appears ready with a ball.

### Walk / Patrol

Casual bipedal movement; bag responds; tail balances.

### Quick Scamper

Body drops lower, steps accelerate, tail stretches backward. Remains bipedal/nimble rather than becoming a quadruped.

### Aim / Target

Raise/position baseball and visually track target before full windup.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Arcing Pitch

Canonical **throws baseballs in an arc**.

Aim -> windup -> release -> follow-through -> pull next ball.

Windup rotates body, draws throwing arm back, prepares front leg/torso, uses tail counterbalance. Release converts ball into independent projectile; hand opens and no duplicate remains.

### Pull Next Ball

Next ball originates from bag/approved retrieval motion, reinforcing ammunition supply.

### Secondary Attack: Overhead Fast Throw

Faster, flatter trajectory, stronger streak, shorter reaction window. Telegraph must remain distinguishable from standard arcing pitch.

### Projectile Behaviors

Canonical projectile states support:

- Held baseball
- Spinning baseball
- Fastball streak
- Bouncing baseball
- Ricochet spark
- Cracked ball impact

Standard arc, bounce, ricochet, and cracked/broken states must remain physically readable.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Scamper into ranged position with a ball ready.

### Hit / React

Stars, ball displacement, recoil, tail reaction, loss of throwing posture. Strong hit can drop held ball as independent prop.

### Stunned

Temporarily unable to pitch.

### Recovery

Shake off, regain posture, check position, reach for next ball.

### Defeat / Spin-Out

Lose balance, spin, baseballs interact, tumble, collapse. Loose balls may scatter from bag and become separate props.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Walk / Patrol
- Quick Scamper
- Aim / Target
- Windup
- Throw Release
- Follow-Through
- Catch / Pull-Next-Ball
- Overhead Fast Throw Variation
- Hit / React
- Stunned
- Recovery
- Defeat / Spin-Out
- Projectiles & Effects
- Extra Props

### Required expanded states

- Entry
- Idle / Ball Check
- Patrol
- Detect Player
- Reposition / Quick Scamper
- Aim / Target Lock
- Standard Windup / Release / Follow-Through
- Pull Next Ball
- Fastball Telegraph / Overhead Windup / Release / Follow-Through
- Throw Recovery
- Hit / Heavy Hit / Ball Drop
- Stunned / Recovery
- Defeat Spin / Bag Spill / Final Dazed
- Retreat / Exit

### Projectile states

- Held
- Release
- Standard Flight
- Spin
- Fastball Flight
- Bounce
- Ricochet
- Crack
- Ground Impact
- Despawn / Settle

## 12. Animation Construction and Modification Rules

Locked:

- Head proportions
- Muzzle length
- Ear placement
- Two-arm/two-leg anatomy
- Long tail
- Fur palette
- **W** cap
- Jersey
- Baseball bag
- Baseball appearance

Tail must actively support balance/emotion: stabilize aim, oppose torso during windup, follow release, trail scamper, react strongly on hit.

Track one ball through `bag -> hand -> release -> flight -> impact`. No duplication.

Bag inventory may shift with movement but balls do not randomly appear outside it.

Canonical animator note: **BALLS FOLLOW A NATURAL ARC; ADD ANTICIPATION.** Avoid teleportation/frame jumps/arbitrary homing curves.

## 13. Collision and Gameplay Readability

Body collider follows head/torso/lower body; tail excluded. Baseballs use independent colliders; motion trails do not. Ricochet collision follows ball after direction change.

Canonical close-combat weakness should matter: ranged attacks should become difficult/unavailable at designated close distance rather than allowing effortless point-blank pitching.

## 14. Effects and Environmental Interaction

Canonical:

- Spinning ball
- Fastball streak
- Bounce arcs
- Ricochet sparks
- Cracked-ball impacts
- Debris puffs
- Loose baseballs
- Junk
- Ground debris
- Shadows

Surface can influence ball behavior: dirt reduces bounce, concrete creates harder ricochet, wood produces material-specific impact. These deepen gameplay without changing character design.

## 15. Character Validation Checklist

Reject if:

- Tail disappears/becomes rigid
- **W** cap changes
- Baseball bag disappears
- Weasel becomes strong in close combat
- Ball duplicates between hand/projectile
- Ball appears without leaving bag/hand
- Standard arc becomes unexplained homing
- Fastball and standard throw have identical telegraphs
- Throw lacks anticipation/follow-through
- Visual trajectory disagrees with projectile movement
- Bag contents randomize every frame
- Character becomes quadrupedal during scamper without approval

---

# Secret Level 6 Global Animation Production Contract

All approved Level 1-5 rules remain active.

## Baseball theme must emerge from behavior

- Beaver: sliding and lane movement.
- Cub: bat swings and heavy-hit timing.
- Seagull: dive + ground skim.
- Weasel: pitching/projectile control.

Caps and jerseys alone are not sufficient.

## Baseball gear is canonical

Persistent gear:

- Beaver: B cap, jersey, wrist bands.
- Cub: C helmet, jersey/armor, oversized bat.
- Seagull: S helmet, chin strap, #15 jersey fragment.
- Weasel: W cap, jersey, baseball bag.

Equipment separates only in approved hit/defeat/throw states.

## Letters and numbers remain stable

Manually validate **B, C, S, W, 15**. AI interpolation may not turn them into other glyphs.

## Surface material matters

- Dirt: dust, pebbles, trenches, skid spray.
- Grass: grass fragments, softer soil, reduced dust.
- Concrete: scrape effects, minimal soil, possible sparks with metal.
- Wood: material-specific impact/splinters.

Do not reuse one universal effect everywhere.

## Momentum and recovery

Committed attacks require recovery:

- Beaver slide
- Cub bat follow-through
- Seagull dive/pull-up
- Weasel throw/follow-through

Enemies may not instantly cancel attack states into new attacks.

## Telegraphs are mandatory

- Beaver crouch before slide.
- Cub backswing before hit.
- Seagull target-lock/dive anticipation.
- Weasel aim/windup before pitch.

Difficulty comes from timing, speed, combinations, and positioning, not invisible attacks.

## Sports props remain independent

Baseballs, bat, helmets, ball bags, and other equipment require explicit state ownership. Identical baseball visuals can have different gameplay roles, so projectile ownership must be tracked.

## Motion physics are distinct

- Cub bat: heavy angular momentum.
- Weasel baseball: ballistic projectile.
- Seagull: aerial momentum.
- Beaver: ground-friction slide.

Do not share one generic movement interpolation.

## Equipment weight affects animation

- Beaver tail/body dominate slide.
- Cub bat dominates attacks.
- Seagull helmet/strap respond to flight.
- Weasel ball bag affects balance/tail.

## Equipment removal requires cause

Missing gear without a state reason is a defect.

## Facing/mirroring

Blind mirroring is risky because letters/numbers can reverse. Preserve readable markings through dedicated orientation handling where needed.

## Cross-Roster Validation

- Beaver: read crouch, leave slide lane.
- Cub: bait swing, punish heavy recovery.
- Seagull: track lock, evade dive, exploit pull-up.
- Weasel: read pitch, navigate projectile, close distance.

If the roster becomes generic chase/contact enemies wearing baseball gear, the level has failed its concept.

## Secret Level 6 Gunk Mythology

The Abandoned Ballpark demonstrates long-term ecological adaptation. Gunk-altered behavior has persisted long enough for an abandoned human environment to shape an ecosystem.

A baseline becomes a high-speed animal path. A bat becomes a territorial weapon. A baseball becomes a projectile. A helmet becomes armor. A jersey becomes scavenged protection.

The creatures do not need to understand human baseball. They have developed new survival behavior around the artifacts that survived it.

This supports the larger story that substantial time has passed and the Gunk continued evolving while Trashy was gone.
