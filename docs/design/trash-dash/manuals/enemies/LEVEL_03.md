# Trash Dash HD Remake - Enemy Master Specification v1.2
## Level 3

**STATUS: APPROVED / LOCKED CANON**

Level 3 shifts enemy ecology toward dense urban trash, alleyways, sewer infrastructure, discarded food, grease, newspapers, cardboard, and street debris. Standard sustained-flight enemies are absent. Threats focus on ambush, ground momentum, projectiles, grease/hazardous refuse, armor states, and environmental interactions.

## Level 3 Enemy Ecology

| Enemy | Placement | Core archetype | Primary player pressure |
|---|---|---|---|
| Alley Cat Burglar | Ground | Pounce predator / ambusher | Sudden horizontal leaps and overshoot danger |
| Sewer Rat Courier | Ground | Mobile charger / hazard dropper | Chase pressure, shoulder checks, slippery food hazards |
| Subway Roach | Ground / concealed | Ambush sprinter | Surprise emergence and rapid lane attacks |
| Traffic-Cone Crab | Ground / armored | Shell defender / projectile attacker | Armor-state changes and launched cone hazards |
| His Greasiness, the Pizza Rat King | Ground boss | Heavy charger / ranged boss | Arena control, charge timing, projectiles, enraged phase |

Core identities:

- The Cat hunts.
- The Courier delivers chaos.
- The Roach ambushes.
- The Crab weaponizes its protection.
- The Pizza Rat King dominates the arena.

---

# L3-E01: Alley Cat Burglar

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated alley cat  
**Placement:** Ground  
**Archetype:** Pounce predator / ambusher

The Cat watches, prowls, waits, then commits. Its rhythm is `observe -> stalk -> accelerate -> leap -> land/crash -> recover`. Feline confidence should remain strong until an attack goes badly.

## 2. Placement and Movement Class

**Placement:** GROUND

Requires walkable terrain. Supports standing, crouching, prowling, running, leaping, pouncing, sliding, landing, and recovery. It leaves the ground during pounce but is not a flying enemy. Jumps follow ballistic arcs rather than hover.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium.

Key silhouette:

- Compact feline torso
- Arched back
- Four legs
- Large pointed ears
- Curled upright tail
- Broad scruffy head
- Long whiskers
- Fish skeleton prominent around mouth/front

Idle is compact/arched. Pounce is long and nearly horizontal. Preserve compression-to-extension.

## 4. Immutable Visual Anatomy

- Exactly two eyes
- Large yellow-to-cream eyes
- Dark pupils and heavy dark eyelid/brow shapes
- Two triangular ears with pink-red inner ears
- Four legs and four paws
- Small claws where pose permits
- One long curled tail
- Long white whiskers
- Scruffy charcoal-to-black fur with dark brown accents
- Pale tan/cream muzzle/lower face
- Small dark nose
- Sharp white teeth in aggressive expressions

### Fish Skeleton

Persistent standard prop:

- Skull/head
- Eye socket
- Spine
- Ribs
- Tail bones
- Dirty off-white/gray bone

The fish skeleton contributes strongly to the silhouette and should not disappear randomly.

Small torn purple/magenta fabric or contaminated scrap around the shoulder/back must remain consistent.

## 5. Color, Material, and Surface Treatment

- Charcoal
- Black
- Dark brown
- Dirty cream
- Warm yellow
- Pink-red ear interiors
- Muted purple accents
- Dirty gray-white bone

Fur is scruffy, tufted, uneven, dirty, and matted. Fish bone is dry, hard, stained, and never bright white.

## 6. Character Personality and Intent

Opportunistic, suspicious, possessive, sneaky, self-confident, food-obsessed, and easily embarrassed by failure. The fish skeleton is stolen treasure. The Cat assumes everything edible already belongs to it.

## 7. Gunk Transformation and Backstory

The Cat survived by stealing food from alleys, restaurants, dumpsters, apartments, and abandoned containers. It ingested contaminated grease, drank dirty water, slept in contaminated cardboard, and groomed residue from its fur.

Gunk amplified hunting and possessiveness rather than producing a radically new anatomy. Food became treasure, trash became territory, and moving creatures became competition. The fish skeleton is a trophy it refuses to surrender even when no food remains.

## 8. Movement and Navigation Behavior

### Idle / Stand

Breathing, eye scanning, ear twitches, tail movement, whisker movement, fish-skeleton adjustment, suspicious crouch/rise.

### Walk / Prowl

Low body, independent shoulder/hip motion, quiet steps, tail counterbalance.

### Run / Leap

Compress spine before launch; extend through airborne phase.

Recommended chain:

`Idle -> detect -> crouch -> prowl -> run -> leap/pounce -> landing -> recovery`

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Pounce

Telegraph:

1. Drop chest.
2. Compress rear legs.
3. Adjust tail.
4. Narrow eyes.
5. Prepare front paws.
6. Brief hold.

Launch extends the body horizontally. Active region follows front paws, head, and forward torso.

### Overshoot Mechanic

Canonical **OVERSHOOT / CRASH INTO BOX CAGE** is a real vulnerability state. If the player evades under correct environmental conditions, the Cat can continue into a cardboard box, causing the box to close/collapse around it and create a comic vulnerability window.

The overshoot must feel like a consequence of confidence and momentum.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Emerge from cardboard/shadow/trash or drop from a low ledge into a grounded landing. Do not materialize directly into idle.

### Exit

Sprint into alley opening, garbage, or off-screen.

### Hit

Wide eyes, stars, vertical recoil, body shake, loss of aggressive expression.

### Defeat

Heavy hit, stagger, scramble, dazed crouch, retreat. Box-mechanic resolution may use pounce -> overshoot -> box impact -> box closes -> shaking/peeking/escape.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Walk / Prowl
- Run / Leap
- Pounce Attack
- Landing / Recovery
- Hit / React
- Overshoot / Crash Into Box Cage
- Props
- Effects

### Required expanded states

- Spawn / Entry
- Detect Player
- Suspicious Look
- Crouch
- Prowl
- Pounce Windup
- Pounce Launch
- Pounce Airborne
- Pounce Hit
- Miss / Overshoot
- Landing
- Landing Slide
- Recovery
- Box Collision
- Box Entrapment
- Box Struggle
- Turn
- Hit
- Dazed
- Defeat
- Retreat
- Exit

## 12. Animation Construction and Modification Rules

Locked:

- Eye color/proportion
- Ear shape
- Fur palette
- Tail length/curl
- Whisker treatment
- Fish skeleton design/scale
- Scruffy silhouette
- Purple accent details

Use quadruped foot-planting rules. Tail responds to momentum.

Fish skeleton continuity must be tracked. Do not change rib count dramatically, reverse orientation randomly, resize, duplicate, disappear, or clip deeply into head.

Cardboard box remains an independent prop. Prefer separate Cat, box, debris, and impact layers.

## 13. Collision and Gameplay Readability

Core collider follows head, chest, torso, central leg mass. Tail/whiskers excluded. Fish skeleton normally decorative.

Pounce attack volume follows head/front paws/forward torso. Trapped Cat may use smaller visible-body hitbox.

## 14. Effects and Environmental Interaction

Canonical effects:

- Dust clouds
- Speed streaks
- Dirt splash
- Stars
- Impact bursts
- Cardboard debris
- Mud/oily splats
- Ground particles

Fast movement should disturb alley garbage. Box crash debris must not obscure trapped state.

## 15. Character Validation Checklist

Reject if:

- Tail disappears/loses curl
- Fish skeleton disappears or duplicates without reason
- Eye color changes
- Fur becomes smooth
- Leg count changes
- Paws slide
- Pounce resembles hovering
- Box permanently fuses into Cat art
- Purple details regenerate randomly
- Silhouette stops reading as scruffy alley cat

---

# L3-E02: Sewer Rat Courier

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated sewer rat  
**Placement:** Ground  
**Archetype:** Mobile charger / hazard dropper

Its identity is **delivery under pressure**. It behaves as though perpetually late.

## 2. Placement and Movement Class

**Placement:** GROUND

Supports stand, sneak, walk, sprint, chase, charge, shoulder check, skid, recovery. The pizza load should influence momentum and balance.

## 3. Size, Scale, and Silhouette

**Relative class:** Small-to-medium.

Recognizable through:

- Pointed rat head
- Large pink ears
- Long thin tail
- Black delivery cap
- Large stack of pizza boxes strapped across back
- Forward-hunched posture

Cargo makes the silhouette wider/taller than the underlying rat.

## 4. Immutable Visual Anatomy

- Exactly two eyes
- Yellow/cream eye surfaces
- Dark pupils
- Two large rounded ears with pink interiors
- Long pointed muzzle
- Pink nose
- Whiskers
- Two arms
- Two legs/feet
- One long pink hairless tail
- Gray-to-dark brown fur
- Pale muzzle/belly accents

Equipment:

- Black/dark delivery cap
- Small orange/red cap emblem
- Dark utility clothing/harness
- Brown straps
- Large pizza-box load

Boxes are brown cardboard, dirty, grease-stained, red/orange branded, stacked and strapped.

## 5. Color, Material, and Surface Treatment

- Dark gray
- Brown
- Black
- Pink
- Dirty cream
- Brown cardboard
- Muted red
- Orange
- Dark green/brown clothing accents

Boxes remain greasy, slightly crushed, worn at edges, dirty, structurally readable. Pizza uses orange/brown crust, yellow-orange cheese, red circular toppings, dark grease.

## 6. Character Personality and Intent

Nervous, hurried, defensive, overworked, easily startled, and focused on delivery rather than the player. Frequently glances backward at cargo. Internal logic: **Move. I have somewhere to be.**

## 7. Gunk Transformation and Backstory

Gunk entered the sewer and mixed with grease, discarded pizza, restaurant waste, and food scraps. Rats became faster/stronger and increasingly organized around food acquisition.

The Courier's scavenging instinct became delivery behavior. Old boxes became cargo, uniforms became equipment, routes became territory. Couriers form part of the food network around the Pizza Rat King's domain, whether or not the King truly controls them.

## 8. Movement and Navigation Behavior

### Stand / Idle / Glance Back

Breathing, ears, tail, cap adjustment, cargo check, backward glance, load-bearing weight shifts.

### Walk / Sneak

Forward lean, light box bounce/lag.

### Sprint / Chase

Lower body, increased leg turnover, tail trail, aggressive cargo bounce, dust.

Courier should feel top-heavy. Sudden stops visibly affect boxes.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Shoulder Check

Canonical **ATTACK / SHOULDER CHECK (CHARGE)**.

Telegraph: notice obstruction, lower head, turn shoulder forward, compress body, shift load backward, accelerate.

Active attack uses shoulder/torso with significant horizontal commitment. Impact may produce spark/burst, debris, recoil, short stagger.

### Secondary Mechanic: Pizza Slice Drop

Canonical **PIZZA SLICE DROP**. Slice falls behind the Courier, lands, and may create grease/slippery hazard.

Important distinction:

- Courier pizza is dropped/lost.
- Pizza Rat King pizza is deliberately thrown.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Run in already carrying pizza stack. A backward glance can establish concern immediately.

### Exit

Accelerate out while stabilizing/protecting boxes.

### Hit

Stars, backward recoil, cargo disruption, tumble, collapse, dazed floor state. Load reacts independently.

### Recovery

Return to feet and reestablish posture.

### Defeat

Heavy hit, tumble, boxes shift/open, slice/debris may fall, Courier remains stunned or flees.

## 11. Animation State Inventory

### Existing

- Stand / Idle / Glance Back
- Walk / Sneak
- Sprint / Chase
- Attack / Shoulder Check
- Pizza Slice Drop
- Hit / React
- Recovery
- Pizza Box States
- Pizza Slice Items
- Grease / Slippery Effects
- Debris / Crumbs

### Required expanded states

- Entry
- Detect Player
- Glance Back
- Cargo Check
- Acceleration
- Sprint
- Shoulder Windup
- Shoulder Charge
- Impact
- Charge Recovery
- Pizza Slip / Drop
- Pizza Landing
- Turn
- Skid
- Hit
- Tumble
- Dazed
- Recovery
- Defeat
- Retreat
- Exit

## 12. Animation Construction and Modification Rules

Locked:

- Cap/emblem
- Eye design
- Ear proportions
- Tail
- Fur palette
- Clothing/harness
- Pizza-box assembly/branding language

Boxes are rigid cardboard connected by straps. They may bounce, tilt, compress slightly, or shift under impact but may not stretch/melt/change count randomly or float independently in normal movement.

Dropped pizza becomes independent and cannot remain duplicated inside/open box and on ground. Tail remains hairless.

## 13. Collision and Gameplay Readability

Core collider follows head, torso, main lower body. Tail excluded. Pizza-box volume may extend beyond body collider.

Shoulder Check uses temporary forward shoulder/head attack volume. Pizza/grease use independent hazard definitions.

## 14. Effects and Environmental Interaction

Canonical:

- Dust
- Grease
- Dark oily puddles
- Pizza
- Crumbs
- Food debris
- Metal scraps
- Small urban debris
- Box damage

Pizza hitting ground should visibly produce grease readable against dark sewer surfaces.

## 15. Character Validation Checklist

Reject if:

- Pizza boxes disappear or box count changes accidentally
- Cap disappears
- Tail becomes furry
- Cargo ignores movement
- Pizza duplicates during drop
- Grease appears before pizza reaches surface
- Shoulder charge loses forward weight
- Rat becomes upright/humanlike
- Equipment branding changes between frames

---

# L3-E03: Subway Roach

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated cockroach  
**Placement:** Ground / concealed ambusher  
**Archetype:** Ambush sprinter

Before activation, the player sees trash. Then the trash moves.

## 2. Placement and Movement Class

**Primary:** GROUND  
**Secondary:** CONCEALED / ENVIRONMENTAL DISGUISE

Begins beneath newspaper. Supports hidden idle, newspaper movement, reveal, scuttle, sprint, dash, skid, hit, flip, recovery. Visible wing covers do not create a flight mechanic.

## 3. Size, Scale, and Silhouette

**Relative class:** Small.

Hidden state is a flatter/larger newspaper mound. Revealed state is low oval insect body with long antennae, six legs, overlapping dark wing covers, bright eyes, and orange-brown limb details.

The transformation from newspaper mound to Roach must be immediately legible.

## 4. Immutable Visual Anatomy

- Six insect legs
- Two long antennae
- Exactly two large stylized primary eyes
- Cream/yellow eye surfaces
- Dark pupils
- Low dark head
- Dark brown/black thorax
- Dark overlapping wing cases
- Orange-brown leg joints/underside
- Segmented insect anatomy
- Hard glossy shell mixed with grime

Do not add mammalian expressions, teeth, clothing, or accessories.

### Newspaper Cover

- Crumpled newspaper
- Gray/off-white
- Black printed text/graphic blocks
- Dirty
- Torn
- Irregular folds
- Large enough to fully obscure Roach

It is a prop, not biological armor.

## 5. Color, Material, and Surface Treatment

- Black
- Deep brown
- Rust brown
- Orange-brown
- Dirty cream
- Gray/off-white paper

Shell is hard, oily, slightly reflective, dirty. Newspaper is matte, soft, wrinkled, torn.

## 6. Character Personality and Intent

Skittish, hyper-reactive, sneaky, opportunistic, surprisingly bold once exposed, and unpredictable at rest. It hides instinctively rather than tactically. Disturbance produces explosive motion.

## 7. Gunk Transformation and Backstory

Roaches survived early Gunk contamination in greasy subway infrastructure. Gunk made an already effective survival strategy more extreme: tougher shell, greater speed, increased vibration sensitivity, and extraordinary stillness under debris.

Discarded newspaper became natural camouflage/shelter. They remain motionless until movement/footsteps trigger an explosive escape response, frequently through the thing that disturbed them.

## 8. Movement and Navigation Behavior

### Hidden Under Newspaper / Idle

Mostly inert. Small paper twitch/lift, antenna tip, brief eye visibility, tiny dust movement are acceptable warning cues.

### Reveal / Burst Out

Antennae, eyes, body, then paper scraps and full Roach.

### Scuttle Walk

Fast coordinated six-leg gait. Never slide a rigid sprite.

### Dash / Sprint

Body lower, antennae trail, dust/speed streaks increase.

### Skid / Stop

Legs brace, dirt kicks, body compresses, speed visibly decelerates.

## 9. Attacks, Telegraphs, and Combat Behavior

No separate weapon is canonical.

### Primary Threat: Ambush Dash

Telegraph is environmental:

1. Newspaper flickers.
2. Antennae appear.
3. Eyes become visible.
4. Paper rises.
5. Roach bursts out.

During designated dash frames, body collision can become damaging. The Roach commits to a horizontal lane and skids afterward.

Do not invent venom spit, bite combos, or ranged projectiles without separate approval.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Preferred hidden newspaper is already in environment when camera arrives.

### Exit

Sprint off-screen, scuttle under debris, or re-hide beneath approved cover.

### Hit

Surprise indicator, backward flip, upside-down landing, stars, leg motion, dazed flattened state.

### Recovery

Rock/roll until upright. This canonical recovery must remain readable.

### Defeat

Hit -> flip -> upside-down struggle -> slowing movement -> collapse/removal, or non-lethal retreat consistent with global tone.

## 11. Animation State Inventory

### Existing

- Hidden Under Newspaper / Idle
- Reveal / Burst Out
- Scuttle Walk
- Dash / Sprint
- Skid / Stop
- Hit / React
- Recovery
- Props & Effects

### Required expanded states

- Hidden Idle
- Hidden Warning
- Newspaper Flicker
- Antenna Reveal
- Eye Reveal
- Burst
- Scuttle
- Detect
- Dash Windup
- Dash
- Dash Follow-Through
- Skid
- Turn
- Hit
- Flip
- Upside-Down Dazed
- Righting Attempt
- Recovery
- Defeat
- Retreat
- Exit / Rehide

## 12. Animation Construction and Modification Rules

Locked:

- Six-leg anatomy
- Two antennae
- Eye design
- Wing-case shape
- Dark shell palette
- Orange-brown legs
- Low silhouette
- Newspaper visual language

All six legs must remain accounted for. Contact feet remain stable; segments cannot merge randomly. Antennae keep consistent head attachment/length and respond to speed/impact.

Treat newspaper as separate prop sequence. Do not deform the Roach to match paper folds.

## 13. Collision and Gameplay Readability

Normal collider follows head, thorax, abdomen. Antennae/extreme leg tips excluded. Dash collider follows main body. Hidden newspaper state is not automatically damaging.

## 14. Effects and Environmental Interaction

Canonical:

- Newspaper scraps
- Dash streaks
- Dust puffs
- Dirt kicks
- Impact bursts
- Stars
- Warning symbols
- Paper motion

Avoid oversized effects that make the small Roach seem physically enormous.

## 15. Character Validation Checklist

Reject if:

- Leg count changes
- Antennae disappear
- Wing covers become functional flying wings
- Newspaper permanently fuses to body
- Hidden state exposes too much of Roach
- Scuttle becomes sprite sliding
- Dash has no readable warning
- Eye proportions drift
- Shell becomes brightly colored
- Recovery omits upside-down behavior

---

# L3-E04: Traffic-Cone Crab

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated urban crab / hermit-style scavenger  
**Placement:** Ground / armored  
**Archetype:** Armored defender / shell projectile attacker

The intended read evolves from **that's a traffic cone** to **there is something underneath it** to **the cone itself is the weapon**.

## 2. Placement and Movement Class

**Placement:** GROUND  
**State classification:** ARMORED / EXPOSED

Supports cone-covered idle, scuttle, fast scuttle, shell retreat, fully concealed cone, cone slide/spin launch, exposed scuttle, hit, recovery. No flight.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium equipped; small-to-medium exposed.

Equipped silhouette is dominated by tall orange traffic cone and broad base, with claws/legs/eyes beneath. Exposed silhouette is much lower/wider with dark rounded body, orange-red legs, two claws, large eyes.

## 4. Immutable Visual Anatomy

### Crab

- Exactly two large stylized eyes
- Cream/yellow eye surfaces
- Dark pupils
- Dark charcoal/black central body
- Orange-red limbs
- Two prominent claws
- Multiple articulated walking legs
- Low crustacean body
- Hard shell/carapace texture

Do not simplify the crab to four legs based on occlusion in a single frame. Preserve a consistent crab-like multi-limbed construction.

### Traffic Cone

- Orange body
- Broad square/rounded base
- Pale reflective horizontal stripe
- Dirt
- Scratches
- Scuffs
- Dents
- Blackened wear
- Hollow interior

Cone is removable equipment, not biologically fused shell.

## 5. Color, Material, and Surface Treatment

- Traffic orange
- Rust orange
- Dark orange-red
- Dirty white/cream stripe
- Charcoal
- Black
- Brown dirt

Crab carapace is hard, dirty, slightly oily. Cone is battered flexible road plastic, not metal.

## 6. Character Personality and Intent

Defensive, nervous, opportunistic, resourceful, irritable when exposed, and much more confident while inside the cone.

Inside cone: bold/protected/confrontational.  
Exposed: anxious/fast/defensive/survival-focused.

## 7. Gunk Transformation and Backstory

The Crab reached city infrastructure through drainage, runoff, sewer, or contaminated waterways. Gunk strengthened it enough to carry an oversized discarded traffic cone as a shelter.

By retracting and using body rotation/kicks, it discovered the protective object could slide, spin, and launch. The Gunk made its survival instinct inventive: the home became a projectile.

## 8. Movement and Navigation Behavior

### Stand / Idle

Eyes/claws/legs adjust; cone may wobble slightly.

### Scuttle Walk

Cone travels with Crab and does not float. Leg contact remains believable.

### Fast Scuttle / Run

Greater leg speed, dust/debris, slight cone tilt.

### Cone Retreat / Shell-Up

Crab visibly retracts claws, eyes, legs, and body until the cone appears almost ordinary.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Cone Slide / Spin Launch

Preparation:

1. Crab retracts.
2. Cone settles.
3. Internal motion begins.
4. Cone tips/rotates.
5. Sparks/dirt indicate stored momentum.

Launch converts cone into an independent attack object that slides/rolls/spins through a physical trajectory.

After launch, Crab is exposed and vulnerable. It can scuttle/reposition/defend while trying to survive until recovery.

The attack deliberately sacrifices protection for offense.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Static traffic cone already in scene; then twitch -> eyes -> claws -> legs -> movement.

### Exit

Retract and remain apparently abandoned, scuttle off-screen equipped, or roll away inside cone.

### Hit

Canonical exposed hit uses stars, eye widening, compression, claw motion, possible roll.

### Recovery

Exposed Crab regains footing. If cone recovery is implemented, retrieval/re-entry must be authored. Never teleport cone back.

### Defeat

Hit, backward roll/collapse, claws drop, dazed pause, retreat/removal. Equipped damage can force shell separation before defeat.

## 11. Animation State Inventory

### Existing

- Stand / Idle
- Scuttle Walk
- Fast Scuttle / Run
- Cone Retreat / Shell-Up
- Cone Slide / Spin Launch
- Exposed Crab Scuttle
- Hit / React
- Recovery
- Props & Effects

### Required expanded states

- Static Cone / Entry
- Eye Reveal
- Limb Reveal
- Equipped Idle
- Scuttle
- Fast Scuttle
- Shell-Up Windup
- Fully Hidden
- Cone Tip
- Cone Spin
- Cone Launch
- Cone Projectile
- Exposed Reveal
- Exposed Scuttle
- Exposed Defensive Claw
- Hit
- Dazed
- Cone Reclaim if implemented
- Re-shell
- Defeat
- Retreat
- Exit

## 12. Animation Construction and Modification Rules

Locked:

- Orange-red limb palette
- Dark body
- Eye design
- Two primary claws
- Multi-legged crab anatomy
- Cone shape/stripe/wear language
- Relative scale of cone and crab

During separation, cone must become independent. Never show an exposed Crab still wearing a full cone while another identical full cone is also flying.

Shell-up is articulation/occlusion, not scaling the Crab smaller. Cone rotation preserves geometry and uses separate motion blur rather than horizontal squashing.

## 13. Collision and Gameplay Readability

Equipped collision follows cone base/central Crab body. Small limbs may extend beyond core collider. Launched cone receives independent collision. Exposed Crab collider becomes much smaller, reinforcing vulnerability.

## 14. Effects and Environmental Interaction

Canonical:

- Sparks
- Scraping
- Dust
- Skid lines
- Dirt
- Ground debris
- Trash
- Newspaper
- Oil/sludge
- Cone motion streaks

Sliding cone should have distinct scraping language on hard ground.

## 15. Character Validation Checklist

Reject if:

- Cone color/stripe changes arbitrarily
- Cone becomes metal
- Cone stretches during launch
- Crab permanently fuses to cone
- Cone duplicates accidentally
- Two primary claws disappear
- Walking limbs regenerate inconsistently
- Exposed state has same gameplay size/protection as equipped state
- Cone teleports back
- Cone attack lacks momentum
- Static cone doesn't visually match equipped cone

---

# L3-B01: His Greasiness, the Pizza Rat King

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated sewer rat boss  
**Placement:** Ground boss  
**Archetype:** Heavy charger / projectile boss / arena controller

The Pizza Rat King is ridiculous and genuinely threatening. Comedy comes from pizza, grease, garbage, and kitchen junk. Danger comes from mass, speed, momentum, and ego.

## 2. Placement and Movement Class

**Placement:** GROUND BOSS

Supports heavy stand, heavy walk, charge startup, pan-assisted charge, fast charge, enraged charge, crash, stun, recovery. Bound to arena surfaces. Do not infer jumping or flight.

## 3. Size, Scale, and Silhouette

**Relative class:** Boss scale, substantially larger than standard Level 3 rats.

Boss silhouette:

- Huge rounded rat body
- Large head
- Crown
- Long pink tail
- Red-orange ragged mantle/back mass
- Large round metal pan
- Broad belly
- Forward teeth
- Hunched charge silhouette

Canonical defeat reveals a dramatically smaller gray rat. Boss and revealed rat are not equal-scale variants.

## 4. Immutable Visual Anatomy

### Boss Form

- Exactly two primary eyes
- Yellow/cream eye surfaces
- Dark pupils
- Two rounded ears
- Long pointed muzzle
- Pink nose
- Long whiskers
- Large mouth
- Multiple sharp white teeth
- Two arms
- Two legs/feet
- One long pink hairless tail
- Massive gray-brown body
- Dirty pale belly
- Dark/brown fur patches
- Red-orange ragged material/heavily matted contaminated covering across back

### Crown

- Dull gold/brass band
- Improvised utensil-like upright prongs
- Fork/spoon shapes
- Screws
- Bolts
- Rivets
- Scrap-metal details

It must never become a polished conventional royal crown.

### Pan

- Large round metal body
- Central dents/details
- Dirty gray surface
- Brown/rust wear
- Long handle

Signature combat prop.

### Pizza

- Golden crust
- Yellow-orange cheese
- Red circular toppings
- Grease

### Revealed Rat

Canonical small gray rat includes two ears, two eyes, gray body, pale underside, pink nose/tail. Crown separates during reveal.

## 5. Color, Material, and Surface Treatment

Primary boss palette:

- Dark gray
- Brown
- Dirty cream
- Pink
- Grease yellow
- Orange
- Deep red-orange
- Dull brass
- Dirty silver

Fur is greasy, matted, clumped, dirty, heavy. Level 3 grease may be brown/yellow-brown/orange/dark oily black because Gunk has mixed with food/oil/sewage. This does not redefine global Gunk color everywhere.

## 6. Character Personality and Intent

Arrogant, gluttonous, loud, territorial, entitled, easily enraged, and convinced of royalty. He believes pizza, grease, rats, and sewer territory are his domain.

Trashy's presence is treated as disrespect rather than simple prey behavior.

## 7. Gunk Transformation and Backstory

An ordinary sewer rat followed food through restaurant drains, grease traps, discarded pizza, subway trash, and dumpster leaks. Gunk mixed with enormous concentrations of grease/food.

Repeated consumption caused appetite and body size to reinforce each other. Other rats followed because food appeared around him; he interpreted this as loyalty. Pan became weapon. Bent utensils became crown. Greasy refuse became court.

The Gunk amplified hunger **and ego**.

Sewer Rat Couriers participate in the same food network and the King believes they serve him.

### Defeat Truth

The enormous form is unstable, inflated/sustained by years of Gunk-saturated grease/food. Defeat collapses that contamination and reveals the much smaller gray rat beneath it. The humiliation is exposure, not realistic death.

## 8. Movement and Navigation Behavior

### Idle / Stand

Heavy breathing, belly movement, crown wobble, pan adjustment, tail motion, mouth/gesture, falling grease/debris.

### Walk / Heavy Movement

Each step has body compression, belly inertia, crown lag, pan motion, dust/ground response.

### Charge Start-Up

Lower body, reposition pan, extend tail, tilt crown, compress rear body, drive feet.

### Pan Charge / Fast Run

Dramatically horizontal body with pan leading/supporting charge. Dust/debris trail. Despite mass, acceleration becomes frighteningly fast.

## 9. Attacks, Telegraphs, and Combat Behavior

### Attack 1: Pan Charge

Long readable windup. King braces behind pan, crosses large arena distance at speed.

If he hits approved obstacle or misses correctly, canonical **CHARGE CRASH / STUNNED** triggers. Momentum carries him forward, ground debris erupts, he falls, stars appear, and a vulnerability window opens.

### Attack 2: Pizza Slice Throw

Produce/raise slice, draw arm back, target, throw. Pizza follows readable arc and may leave small grease traces.

### Enraged Faster Charge

Canonical escalation. Enrage can alter charge speed, windup duration, recovery time, animation intensity, expression, and effects. It does **not** redesign the boss.

Recommended boss rhythm:

- Phase 1: heavy movement + standard pan charge + pizza throw
- Vulnerability: crash/stun windows
- Phase 2: faster charges + shorter intervals + more aggressive projectile use

Health thresholds remain implementation tuning, not visual canon.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Dedicated intro: heavy off-screen impacts, pizza/grease debris, crown appears, King enters with pan, stops, threat gesture. Do not spawn already charging.

### Hit

Impact burst, recoil, crown instability, wide expression, stars, loss of composure. Boss retains weight.

### Crash / Stun

Separate from ordinary hit. It is self-caused vulnerability through momentum and should be a much larger physical event.

### Defeat / Reveal

Canonical sequence:

1. Giant boss collapses.
2. Crown destabilizes.
3. Contaminated outer form slumps.
4. Interior/rear mass opens/falls away.
5. Small gray rat emerges.
6. Crown falls separately.
7. Small rat stands exposed.
8. Small rat retreats or remains humiliated per encounter staging.

This reveal is canon.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Walk / Heavy Movement
- Charge Start-Up
- Pan Charge / Fast Run
- Charge Crash / Stunned
- Pizza Slice Throw Attack
- Enraged Faster Charge
- Hit / React
- Defeat / Reveal
- Props & Effects
- Crown Details

### Required expanded states

**Boss Introduction:** Off-Screen Approach, Arena Entry, Crown Settle, Threat Display  
**Movement:** Idle, Heavy Walk, Turn, Pan Adjustment  
**Charge:** Telegraph, Start-Up, Standard Charge, Follow-Through, Crash, Crash Slide, Stunned, Stun Recovery  
**Pizza:** Acquire, Windup, Release, Follow-Through, Recovery  
**Phase Transition:** Enrage Trigger, Enrage Roar, Faster Charge Windup, Enraged Charge, Enraged Recovery  
**Damage:** Light Hit, Heavy Hit, Crown Wobble  
**Defeat:** Defeat Trigger, Collapse, Outer-Mass Failure, Crown Fall, Small Rat Reveal, Small Rat Recovery, Retreat/Exit

## 12. Animation Construction and Modification Rules

Locked boss features:

- Massive proportions
- Eye design
- Rat facial structure
- Tail
- Crown and utensil construction
- Pan
- Red-orange back treatment
- Fur palette
- Belly proportions
- Teeth

Weight is mandatory: anticipation, inertia, follow-through, secondary movement, ground response.

Crown is rigid but loosely seated. It may bounce/tilt/rotate/fall but may not stretch/melt/change into conventional crown or randomize utensil structure.

Pan is rigid independent prop in King's grasp. Do not stretch it during charge.

Pizza exists in hand before release and independently afterward, never duplicated.

The revealed small rat is a distinct approved canonical form, **not a scaled-down giant King**. Use approved revealed-rat frames directly.

## 13. Collision and Gameplay Readability

Standard boss collider follows head, belly, torso, central lower body; exclude full crown/tail.

Pan Charge collider includes forward pan/leading mass. Pizza uses independent projectile collider. Stunned state has clearly defined central damage region. After reveal, replace giant collision with small-rat scale.

## 14. Effects and Environmental Interaction

Canonical:

- Pan rotation
- Dust
- Dirt
- Pizza
- Grease
- Crumbs
- Ground impacts
- Stars
- Debris
- Speed streaks
- Grease smears
- Crown components

Boss charges should disturb more arena material than any standard Level 3 enemy. Crashes should have the strongest ground impact language in the level.

## 15. Character Validation Checklist

Reject if:

- Crown becomes polished/conventional
- Utensil/scrap crown language disappears
- Pan changes design/scale
- Tail disappears
- Boss moves without weight
- Charge uses sprite stretching
- Pizza duplicates
- Enraged phase redesigns character
- Defeat omits small-rat reveal
- Revealed rat is scaled-down giant boss
- Giant collision remains after reveal
- Giant/small forms overlap without canonical transition
- Grease/food/garbage material language disappears
- Boss no longer reads substantially larger than standard rats

---

# Level 3 Global Animation Production Contract

All approved Level 1 and Level 2 rules remain active.

## Character, prop, and effect separation

Prefer separate control for:

- Cat, fish skeleton, cardboard box, cardboard debris, impacts
- Courier, pizza-box stack, pizza slice, grease, loose debris
- Roach, newspaper, newspaper scraps, dust
- Crab, traffic cone, cone motion effects, sparks
- Pizza Rat King, boss body, pan, crown, pizza, grease, defeat debris, revealed rat

## Prop continuity

Track every canonical prop as equipped, held, stored, airborne, on ground, destroyed, or occluded. Props cannot exist in contradictory states.

## Momentum

Level 3 committed movement uses:

`anticipation -> acceleration -> active motion -> follow-through -> braking/impact -> recovery`

Especially Cat pounce, Courier shoulder check, Roach dash, cone launch, and Rat King charge.

## Environmental failure creates vulnerability

Canonical failed attacks create player opportunities:

- Cat overshoots into cardboard
- Rat King crashes/stuns
- Crab loses cone protection
- Courier tumbles/loses cargo
- Roach flips on back

These are gameplay states, not decorative animations.

## Grounding

All standard Level 3 enemies are ground-based. Validate floating feet, floor height, ground shadow, contact, and effect placement.

## No speed stretching

Use pose, compression, direction, blur, streaks, dust, and secondary motion. Never non-uniformly stretch a character.

## Stable roots and occlusion

Root follows actual body/ground contact, not props or VFX. Occlusion does not change anatomy.

## Interactive props

Cardboard, pizza, grease, newspapers, cones, pans, and crowns should be trackable where gameplay relevant rather than flattened into decorative pixels.

## Gameplay-scale validation

Review source, animation, actual game scale, Level 3 background, collision, transitions, prop interaction, and uninterrupted play.

## Cross-Roster Validation

- Cat: predatory anticipation + committed pounce.
- Courier: urgent delivery + shoulder pressure + dropped food hazard.
- Roach: concealment + explosive speed.
- Crab: armor management + shell-as-weapon.
- Pizza Rat King: boss-scale weight + reckless momentum + food projectiles + escalating rage.

No standard enemy should feel like a weaker reskin of the boss.
