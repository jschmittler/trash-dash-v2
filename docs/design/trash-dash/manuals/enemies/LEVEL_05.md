# Trash Dash HD Remake - Enemy Master Specification v1.4
## Level 5: Raccoon in Space

**STATUS: APPROVED / LOCKED CANON**

Level 5 introduces low-gravity combat. Low gravity is a real gameplay and animation rule affecting arcs, recovery, debris, secondary motion, momentum, and placement. It is not a decorative effect.

## Level 5 Enemy Ecology

| Enemy | Placement | Core archetype | Primary player pressure |
|---|---|---|---|
| Asteroid Armadillo | Ground + ballistic low-gravity movement | Rolling ricochet enemy | Momentum prediction and redirection |
| Rocket Roach | Ground + rocket-assisted horizontal burst | Burst-movement enemy | Telegraph recognition and high-speed lane attacks |
| Satellite Hermit Crab | Ground | Shielded transmitter / patroller | Defensive timing and shell-lift vulnerability |
| Vacuum Jelly | Floating / aerial | Position-control flyer | Suction, forced movement, debris control |

Core identities:

- Asteroid Armadillo rolls and rebounds.
- Rocket Roach warns, blasts, fails, and tumbles.
- Satellite Hermit Crab shields, signals, and transmits.
- Vacuum Jelly pulls, collects, and pops.

---

# L5-E01: Asteroid Armadillo

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated armadillo with mineralized asteroid-like armor  
**Placement:** Ground with low-gravity ballistic movement  
**Archetype:** Low-gravity roller / ricochet enemy

Primary intent is to build momentum, curl into an armored sphere, travel through long low-gravity arcs, bounce/ricochet, and force trajectory prediction.

Canonical player read:

- Armadillo visible = readable and relatively slow.
- Asteroid ball = fast, armored, momentum-driven threat.
- Uncurled after disruption = vulnerable.

## 2. Placement and Movement Class

**Primary:** GROUND  
**Secondary:** BALLISTIC LOW-GRAVITY ROLLER

Supports rolling surfaces, launching from edges, long airborne arcs, bouncing, ricocheting, player redirection, soft landings, and re-entry into roll. It does not fly. Airborne states remain governed by gravity and momentum.

Canonical states include Idle / Stand, Walk / Shuffle, Anticipation / Curl-Up, Full Curled / Asteroid Ball, Low-Gravity Roll, Airborne Spin / Long Arc, Bounce / Ricochet, Stomped Redirect / Direction-Change, Uncurl / Vulnerable.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium-to-large.

Uncurled silhouette:

- Small pointed mammalian head
- Long narrow snout
- Large upright ears
- Short sturdy legs
- Extremely large armored shell
- Rounded back
- Low posture

Curled silhouette is an almost perfect asteroid-like sphere and must remain readable at speed and small gameplay scale.

Vulnerable silhouette exposes the smaller animal within the heavy shell structure.

## 4. Immutable Visual Anatomy

### Animal

- Exactly two anatomical eyes
- Large dark glossy eyes with bright highlights
- Two upright pointed ears
- Warm brown/orange inner ears
- Long tapered snout
- Small dark nose
- Four legs
- Four feet
- Small claws where visible
- Gray-brown organic surface/fur/skin
- Pale gray/tan face/underside
- Low armadillo-like proportions

Do not add horns, wings, extra limbs, or a large furry tail.

### Asteroid Shell

- Large spherical armor
- Gray-brown/dark metallic-rock coloration
- Multiple crater-like depressions
- Overlapping armor plates
- Angular shell segments
- Dark recessed holes
- Heavy edge plates
- Scratches/chips
- Pitted rocky texture
- Occasional metal-like panel qualities

It must not become a smooth ordinary armadillo shell.

### Orbiting Debris

Dust, pebbles, and tiny rock fragments may drift/orbit as VFX. They are not anatomy.

## 5. Color, Material, and Surface Treatment

- Dark brown
- Gray-brown
- Charcoal
- Gunmetal
- Warm tan
- Rust brown
- Black
- Dusty beige

Shell should visually sit between biological armor, stone, meteorite, and salvaged metallic plating. It is matte, pitted, chipped, heavy, and cratered. Exposed animal remains visibly softer/organic.

## 6. Character Personality and Intent

Cautious, defensive, slow to provoke, highly committed once rolling, somewhat confused by low gravity, and reliant on armor rather than predation.

Its first instinct is to curl up. Low gravity accidentally turns defense into dangerous locomotion. It may seem surprised by how far it continues rolling.

## 7. Gunk Transformation and Backstory

Armadillos were part of biological research involving protective structures, radiation, bone density, and altered gravity. Gunk contaminated both animal and mineral-rich experiment material.

The shell absorbed surrounding compounds, thickened, mineralized, and bonded to debris until it resembled a meteorite. The Gunk amplified the curl instinct, while low gravity turned a defensive ball into a projectile.

On Earth, curling meant safety. Here, curling means movement.

## 8. Movement and Navigation Behavior

### Idle / Stand

Canonical note: **Hovering dust orbits slowly.** Animal remains grounded while debris drifts. Use breathing, eye/ear/head adjustments, shell shift.

### Walk / Shuffle

Canonical **slow, heavy plodding steps**. Show foot planting, body compression, shell inertia, dust.

### Curl-Up

Stop, retract head/limbs, compress shell plates toward a sphere. Do not instant-switch.

### Full Curled / Asteroid Ball

Can briefly idle with low-gravity dust orbit.

### Low-Gravity Roll

Starts slowly and builds speed.

### Airborne Spin / Long Arc

Canonical **long graceful arc** with long ascent, extended apex, slow descent, persistent rotation.

### Bounce / Ricochet

Impact redirects trajectory based on surface collision. No teleporting between arcs.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Asteroid Roll

Telegraph:

1. Stop.
2. Lower body.
3. Retract head.
4. Pull legs inward.
5. Close shell.
6. Shift dust.
7. Stabilize ball briefly.

Rolling sphere becomes active moving hazard and builds momentum.

### Stomp Redirect

Canonical **STOMPED REDIRECT / DIRECTION-CHANGE**. A hit from above redirects roll.

Successful redirect:

1. Clear impact burst.
2. Trajectory changes.
3. Rolled state persists.
4. New direction remains predictable.

This may temporarily turn the enemy into a player-directed projectile. Do not automatically uncurl on redirect.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Shuffle in, roll in, or arrive through low-gravity arc. First introduction should preferably show walking form before ball form.

### Hit / React

Canonical **flinches, shakes shell**. Armored hits should feel less effective.

### Uncurl / Vulnerable

Canonical artwork shows the vulnerable animal emerging from opened shell. The sheet note says "exposed raccoon," but the approved artwork is authoritative for the actual creature identity and design. Do not redesign it into a raccoon because of that label.

Vulnerability should stop/reduce momentum, open shell plates, expose animal, lower defense, and create a clear damage opportunity.

### Stunned

Stars orbit head. Vulnerable.

### Recovery

Shake off and re-curl visibly.

### Defeat / Dazed Tumble

Shell cracks, unstable tumble, collapse, dazed finish. No gore.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Walk / Shuffle
- Anticipation / Curl-Up
- Full Curled / Asteroid Ball
- Low-Gravity Roll
- Airborne Spin / Long Arc
- Bounce / Ricochet
- Stomped Redirect / Direction-Change
- Uncurl / Vulnerable
- Hit / React
- Stunned
- Recovery
- Defeat / Dazed Tumble
- Props & Details
- Effects & Impacts

### Required expanded states

- Entry
- Idle
- Suspicious Look
- Shuffle Start / Loop
- Curl Anticipation / Transition
- Ball Idle
- Roll Start / Acceleration / Fast Roll
- Edge Launch
- Airborne Ascent / Apex / Descent
- Soft Landing
- Hard / Wall Ricochet
- Stomp Impact / Redirect Transition / Redirected Roll
- Uncurl
- Vulnerable Idle
- Hit
- Stunned
- Recovery Shake / Re-Curl
- Defeat Crack / Dazed Tumble / Final Dazed
- Exit

## 12. Animation Construction and Modification Rules

Locked:

- Head proportions
- Snout length
- Ear shape
- Eye design
- Four-legged anatomy
- Shell diameter
- Crater language
- Shell plating/palette
- Animal-to-shell scale

Curl transformation uses anatomical retraction and shell closure, not scaling the sprite inward.

Rolled state stays circular. No horizontal speed stretching.

Large crater/plate positions must remain trackable through rotation. Rotate the canonical shell texture/features rather than randomizing crater layout per frame.

Low-gravity airborne frames derive from known takeoff/landing anchors with consistent sphere size, rotation, arc, and debris lag.

## 13. Collision and Gameplay Readability

Uncurled collider follows head/body/main shell. Curled state becomes clean circular approximation. Rolling ball becomes damaging during active movement. Stomp redirect uses a dedicated top interaction region. Vulnerable damage region shifts toward exposed animal/open shell core.

Orbiting dust/pebbles are non-colliding unless explicitly physical.

## 14. Effects and Environmental Interaction

Canonical:

- Dust puff
- Speed trail
- Air arc trail
- Impact burst
- Stunned stars
- Debris burst
- Orbiting dust/pebbles
- Shell fragments

Low gravity means fragments rise farther, fall more slowly, and remain visible longer than equivalent earlier-level debris.

## 15. Character Validation Checklist

Reject if:

- Shell becomes smooth
- Crater layout randomizes
- Limb count changes
- Ear/snout proportions drift
- Curled state becomes oval from scaling
- Roll starts instantly at full speed
- Airborne movement resembles sustained flight
- Arcs use fast Earth-gravity fall
- Ricochet ignores impact direction
- Redirect lacks readable stomp impact
- Vulnerable state is not visually distinct
- Debris settles too quickly for Level 5 gravity
- Orbiting pebbles become anatomy

---

# L5-E02: Rocket Roach

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated cockroach with improvised propulsion hardware  
**Placement:** Ground + rocket-assisted horizontal burst  
**Archetype:** Burst-movement enemy

Approved design intent:

- **Harmless until rocket dash.**
- **Two clear warnings before burst.**
- **Straight-line fast burst.**
- **Rockets fail after use.**
- **Vulnerable when tumbling.**

These are core gameplay canon.

## 2. Placement and Movement Class

**Primary:** GROUND  
**Secondary:** ROCKET-ASSISTED BURST

Normal crawl/patrol is grounded. Horizontal rocket dash may become partially airborne in low gravity but is not sustained flight. Burst follows a committed straight trajectory. After rocket failure, ballistic momentum takes over.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium including equipment.

Key silhouette:

- Dark orange-brown cockroach body
- Long antennae
- Six legs
- Large visible circular eye
- Huge improvised rocket apparatus
- Cylindrical spray cans
- Rectangular orange machinery housing
- Hoses/wires
- Exhaust assembly

The rig is intentionally absurd and top-heavy.

## 4. Immutable Visual Anatomy

### Roach

- Six insect legs
- Two long antennae
- Two anatomical compound eyes, near-side eye dominant in profile
- Segmented body
- Hard brown/orange exoskeleton
- Dark head
- Wing-case/back-shell language beneath equipment
- Small articulated mouthpart region
- No fur
- No mammalian teeth
- No vertebrate limbs

The dominant visible eye is round, dark, glossy, with blue/cyan-gray ring details. Do not redesign it as a literal one-eyed cyclops.

### Spray-Can Rocket Pack

Canonical prop includes:

- Multiple cylindrical canisters
- Large orange rectangular central housing
- Dark mechanical frame
- Hoses
- Pipes
- Wiring
- Valves/connectors
- Exhaust hardware
- Dirty labels/markings
- Large painted **ZAP!** graphic language
- Rust/scorch wear

The pack is improvised, not sleek spacecraft technology.

## 5. Color, Material, and Surface Treatment

- Rust orange
- Burnt orange
- Dark brown
- Black
- Gunmetal
- Dirty gray
- Muted cyan/blue details
- Red warning lights
- Orange-yellow flame

Roach shell is hard, oily, segmented, dirty. Rocket pack is old painted metal, rusted steel, aerosol cans, rubber hoses, tubing, burned exhaust.

## 6. Character Personality and Intent

Nervous, unstable, opportunistic, hyperactive, mostly harmless before activation, terrified of its own propulsion, and unable to fully control the aftermath.

It should feel more like the passenger than the pilot. During warning states it increasingly realizes what is about to happen.

## 7. Gunk Transformation and Backstory

Roaches reached Level 5 through contaminated cargo/trash/maintenance systems. A population nested near discarded propulsion experiments and compressed-gas canisters. Gunk increased resilience to heat, propellant, electrical discharge, and impact.

One Roach became trapped in discarded spray cans/hoses/test hardware. Instead of dying, Gunk-bound material accumulated into a wearable propulsion rig. The system sputters, leaks, misfires, and barely works, but when pressure builds it creates enormous horizontal thrust.

The Roach has learned to brace, not steer.

## 8. Movement and Navigation Behavior

### Idle Drift - Harmless

Light low-gravity drift/small motion. Canonical harmless state should not create attack contact unless explicitly tuned otherwise.

### Crawl / Patrol

Slow insect scuttle; pack shifts slightly; antennae active.

### Sputter Warning 1

Red lights activate, small irregularities, Roach reacts.

### Sputter Warning 2

Stronger lights, sparks, flame pops, vibration, stronger Roach reaction.

### Ignition Start-Up

Rockets prime. Roach lowers/braces, exhaust begins.

### Rocket Burst / Sustained Blast

Rapid straight-line horizontal acceleration. No homing curve.

### Post-Burst Tumble

Rockets fail. Momentum continues and Roach tumbles slowly in low gravity.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Rocket Burst

Mandatory stages:

1. Warning One
2. Warning Two
3. Ignition
4. Initial Burst
5. Sustained Horizontal Blast
6. Failure
7. Vulnerability

The active threat is primarily body + main equipment mass. Exhaust is only damaging if explicitly designed.

Canonical **VULNERABLE CRASH / WOBBLE** is part of the attack cycle, not optional recovery flavor.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Crawl/lightly drift in so player sees rig before activation.

### Hit / React

Recoil, sparks, equipment shake, stars, ground displacement.

### Vulnerable Crash

Tumble, equipment impacts ground, stars, pack becomes inactive.

### Recovery

Stabilize. If another cycle is permitted, rig visibly recovers before warning sequence begins again.

### Defeat / Scorched Sputter-Out

Sparks, smoke, scorch marks, mechanical debris, collapsed Roach/equipment, burned ground. Canon notes support destroying it for extra scrap.

## 11. Animation State Inventory

### Existing

- Idle Drift / Harmless
- Crawl / Patrol
- Sputter Warning 1
- Sputter Warning 2
- Ignition Start-Up
- Rocket Burst Dash
- Sustained Horizontal Blast
- Post-Burst Tumble / Spin
- Vulnerable Crash / Wobble
- Hit / React
- Recovery
- Defeat / Scorched Sputter-Out
- Dust / Crash / Scorch / Debris FX

### Required expanded states

- Entry
- Idle Drift
- Ground Settle
- Patrol
- Detect Player
- Warning 1 / Reset
- Warning 2
- Ignition Prime
- Engine Shake
- Initial Burst
- Full-Speed Burst
- Follow-Through
- Engine Failure
- Airborne Tumble
- Ground Crash
- Vulnerable Wobble / Idle
- Hit / Heavy Hit
- Recovery
- Rocket Reset if reusable
- Defeat / Sputter-Out / Final Scorched
- Exit if applicable

## 12. Animation Construction and Modification Rules

Locked:

- Six-leg anatomy
- Antenna count
- Eye design
- Roach palette
- Rocket-pack silhouette
- Orange housing
- Canister structure/count language
- ZAP graphic language
- Hose routing
- Exhaust placement

All six legs remain accounted for beneath/around equipment.

Pack is rigid mechanical assembly that can shake/tilt/bounce/fail/break but not stretch/morph/randomize.

Warning progression is always `Warning 1 < Warning 2 < Ignition`. Strongest warning cannot occur after dash begins.

Do not stretch Roach for speed; use pose/flame/streaks/vibration/exhaust/dust.

## 13. Collision and Gameplay Readability

Patrol collider follows Roach body + central equipment, excluding antennae. Canonical harmless state can disable attack contact. Rocket Burst activates moving attack collider around body/pack. Flame trail/speed lines are not automatic collision. Vulnerable state keeps damage collider on crashed body/pack.

## 14. Effects and Environmental Interaction

Canonical:

- Drift trails
- Ignition bursts/flame
- Sparks
- Loose pipes
- Smoke
- Tumble stars
- Speed lines
- Ground dust/skid
- Impact bursts
- Scorch marks
- Mechanical debris

Low-gravity broken components remain airborne longer than Level 4 machine debris.

## 15. Character Validation Checklist

Reject if:

- Warning sequence becomes one cue
- Burst curves/homes toward player
- Roach becomes sustained flying enemy
- Equipment becomes clean/futuristic
- ZAP housing changes arbitrarily
- Canisters duplicate/disappear
- Antennae disappear
- Leg count drifts
- Dash uses sprite stretching
- Roach remains dangerous during canonical vulnerable tumble
- Full exhaust continues after failure
- Defeat lacks mechanical debris/scorch language
- Warning lights activate only after attack begins

---

# L5-E03: Satellite Hermit Crab

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated hermit crab using satellite hardware as a shell  
**Placement:** Ground  
**Archetype:** Shielded patroller / transmitter

The shell is armor + antenna + transmitter. This is mechanically different from the Level 3 Traffic-Cone Crab.

## 2. Placement and Movement Class

**Placement:** GROUND

Supports idle, patrol walk, defensive crouch, alert, shell lift, transmit, quick scuttle, hit, flipped/stunned, recovery. Satellite dish does not provide flight.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium-to-large.

Dominant silhouette:

- Broad concave dish
- Tall central antenna
- Receiver at dish center
- Low dark crab body
- Large orange/red claws
- Multiple orange legs
- Cyan tech lights

Defensive silhouette lowers dish over body. Vulnerable silhouette lifts dish and exposes body. Difference must read at gameplay scale.

## 4. Immutable Visual Anatomy

### Crab

- Exactly two primary stylized eyes integrated in dark central body/face region
- Two large front claws
- Multiple articulated walking legs
- Dark charcoal carapace/body
- Orange/rust-red claws and legs
- Hard segmented crustacean surfaces
- No fur/mammalian features

Preserve approved decapod-style limb plan even when legs are occluded.

### Satellite Dish Shell

- Broad concave circular/parabolic dish
- Dirty off-white/light gray surface
- Segment lines
- Scratches
- Missing paint
- Dark damaged patches
- Orange/yellow markings
- Dark metal rim
- Central receiver
- Long antenna mast
- Red/orange signal light at mast tip
- Mechanical mounting hardware

Small cyan/blue technology accents appear beneath dish.

## 5. Color, Material, and Surface Treatment

- Dirty white
- Light gray
- Gunmetal
- Charcoal
- Black
- Rust orange
- Dark red-orange
- Cyan/blue
- Small red signal lights

Dish is metallic, thin but sturdy, scratched, weathered, damaged, and old technical hardware. Crab remains organic beneath it.

## 6. Character Personality and Intent

Watchful, cautious, defensive, methodical, sensitive to nearby movement, proud of its huge shell, and more comfortable transmitting than fighting directly.

Emotional cycle: `secure -> suspicious -> signal -> expose -> transmit -> panic -> protect again`.

## 7. Gunk Transformation and Backstory

A mutated hermit crab encountered broken orbital communications hardware. Gunk strengthened limbs enough to carry the oversized dish and altered the fit between body and machine mount.

Contaminated surviving circuitry occasionally activated when the Crab shifted. The animal learned that dish down meant safety and dish up created a pulse that drove threats away.

It does not understand radio. It has converted old communications hardware into an extension of defensive instinct.

## 8. Movement and Navigation Behavior

### Idle / Stand

Canonical rule: **SHELL IS DOWN DURING NORMAL PATROLS.** Eye/claw/leg adjustments, antenna movement, small signal flicker.

### Patrol Walk

Coordinated multi-leg scuttle. Dish stays relatively stable with slight secondary bounce.

### Alert / Blink-Signal Telegraph

Three escalating canonical signal stages:

- Signal 1
- Signal 2
- Signal 3

Canonical rule: **THREE BLINKING LIGHTS TELEGRAPH ATTACK.**

### Defensive Crouch

Lower body/dish to increase protection.

### Shell Lift

Dish physically rises, exposing body. No instant sprite swap.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Radio Pulse / Transmit

Canonical **TRANSMIT / ATTACK PULSE** and **DISH LIFTS TO TRANSMIT**.

Sequence:

1. Three signal telegraphs.
2. Dish lifts.
3. Blue/cyan pulse emits from dish/receiver.
4. Crab is vulnerable during exposed state.
5. Dish lowers after transmission/recovery.

Exact gameplay shape may be horizontal, radial, or position-disrupting as encounter needs, but it must originate from satellite hardware.

Canonical note: **SHELL LIFTS TO TRANSMIT OR WHEN VULNERABLE.**

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Patrol naturally into scene. Dish should make it readable early.

### Hit / React

Stars, dish instability, body recoil, mechanical debris, collapse/shell displacement.

### Stunned / Flipped / Exposed

Dedicated vulnerable state with dish displaced and body temporarily unable to defend.

### Recovery

Rights itself and returns dish to protection.

### Defeat / Scurry-Away

Canonical **DEFEAT / SCURRY-AWAY IF NOT DESTROYED**.

Canonical note: **DESTROYED WHEN HIT WHILE SHELL IS LIFTED.**

Two outcomes:

- Non-destructive encounter resolution: Crab scurries away.
- Strong exposed hit: satellite shell can break, mechanical debris separates, exposed Crab can flee.

The Crab itself need not die for encounter completion.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Patrol Walk
- Alert / Blink-Signal Telegraph
- Defensive Crouch
- Shell-Lift / Vulnerable
- Transmit / Attack Pulse
- Quick Scuttle
- Hit / React
- Stunned / Flipped / Exposed
- Recovery
- Defeat / Scurry-Away
- Props & Effects

### Required expanded states

- Entry
- Idle
- Patrol
- Turn
- Alert Start
- Signal 1 / 2 / 3
- Defensive Crouch
- Shell-Lift Start
- Shell Raised
- Vulnerable Idle
- Transmission Charge / Pulse / Sustain / End
- Shell Lower
- Quick Scuttle
- Hit / Heavy Hit
- Flip / Exposed Stun
- Dish Damage / Dish Break
- Recovery
- Crab Escape
- Defeat
- Exit

## 12. Animation Construction and Modification Rules

Locked:

- Orange/rust Crab limbs
- Two primary claws
- Dark body
- Satellite-dish scale/shape
- Central receiver
- Antenna mast
- Red tip light
- Cyan accents
- Weathered markings

Maintain stable crustacean limb plan. Dish is a large rigid prop that can tilt/lift/lower/shake/break but cannot stretch/fold like cloth/change diameter/duplicate.

Radio-wave VFX are independent. Shell lift is actual mechanical rotation/raising, not scaling upward.

## 13. Collision and Gameplay Readability

Protected body remains beneath dish with armor logic. Do not treat every dish edge as biological hitbox. Radio pulse uses independent gameplay volume. Shell-lift exposes a clear damage region. Broken dish pieces lose original shield collider.

## 14. Effects and Environmental Interaction

Canonical:

- Broken satellite shell
- Blinking signal lights
- Radio pulse/transmit waves
- Dust puffs
- Metallic debris
- Stars
- Sparks

Low gravity gives broken hardware longer arcs/slower descent.

## 15. Character Validation Checklist

Reject if:

- Dish is raised during ordinary patrol without reason
- Three-stage telegraph is removed/reordered
- Dish changes diameter
- Central antenna/signal tip disappears
- Limb plan changes
- Radio pulse comes from claws rather than dish
- Shell lift fails to expose body
- Vulnerable state remains fully protected
- Dish duplicates during break
- Debris falls with heavy Earth gravity
- Crab becomes flying enemy
- Non-destructive canonical scurry-away is ignored without reason

---

# L5-E04: Vacuum Jelly

## 1. Identity and Gameplay Role

**Type:** Gunk-animated microgravity waste-capture organism  
**Placement:** Floating / aerial  
**Archetype:** Position-control flyer

Canonical behavior:

- **Pulses twice to warn players.**
- **Contracts & sucks debris inward.**
- **Pops when hit, releases trash, becomes vulnerable.**

## 2. Placement and Movement Class

**Placement:** FLOATING / AERIAL

No floor required. Movement comes from buoyancy-like body pulsing, low-gravity drift, contraction, and re-expansion. States include idle float, hover drift, gentle reposition, suction stabilization, vulnerable collapse, reinflate, harmless float-away.

It has no wings and should not fly like Mosquito/Bee/Dustwing.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium-to-large floating enemy. Canonical scale guide shows a substantial creature relative to player.

Silhouette:

- Large transparent rounded bell/dome
- Broad lower lip
- Two oversized black eyes
- Multiple dangling tentacle-like appendages
- Visible trash suspended inside
- Bulbous jellyfish-like form

Contracted state is smaller/lower/denser. Popped state collapses dramatically and exposes debris.

## 4. Immutable Visual Anatomy

- Exactly two primary eyes
- Large black oval eyes with white highlights
- Transparent blue/cyan bell
- Broad rounded dome
- Thick lower bell edge
- Multiple flexible tentacle-like appendages
- No feet/legs/wings/fur
- No defining teeth
- No rigid skeleton

Tentacle visibility varies through occlusion/perspective. Do not invent extra prominent tentacles randomly; use approved anchors.

### Internal Trash

Visible collected refuse may include wrappers, containers, metal scraps, packaging, equipment pieces, and misc garbage. Unlike fixed equipment, exact inventory can change through gameplay collection/release state. It must not change randomly frame to frame.

## 5. Color, Material, and Surface Treatment

- Pale cyan
- Blue-gray
- Aqua
- White highlights
- Black eyes
- Muted trash colors
- Rust/green/purple/orange/dirty gray internal debris

Bell is transparent, gelatinous, glossy, wet, soft, semi-fluid. It may slightly distort internal debris without hiding it. Tentacles are soft, flexible, partly translucent, slightly darker than bell.

## 6. Character Personality and Intent

Calm, curious, hungry for objects rather than food, unhurried, almost peaceful, and dangerously indifferent to what it collects.

It can look content when full of trash. Popped form becomes startled, deflated, embarrassed.

## 7. Gunk Transformation and Backstory

Vacuum Jelly began as experimental microgravity waste-control gel intended to capture floating screws, packaging, dust, tools, food debris, and broken fragments.

Gunk animated that collection behavior. Elastic membrane became bell, tendrils became tentacles, and programmed material attraction became instinct. The creature accumulated trash inside its body.

It learned that contraction created strong pressure changes. In low gravity, that pull affects far more than dust.

The result is a living waste-management system with no understanding of the difference between garbage and a person.

## 8. Movement and Navigation Behavior

### Idle Float

Slow bell expansion, tentacle lag, internal debris float, eye movement, body wobble.

### Hover Drift

Gradual reposition with long easing; no abrupt stops.

### Double-Pulse Telegraph

Exactly two clear warnings. Each uses bell expansion, cyan rings, tentacle movement, internal trash movement. Second must be at least as clear as first.

### Suction Inhale / Contraction

Body contracts, bell shrinks, internal trash compresses toward center, tentacles pull inward.

### Strong Pull

Jelly stabilizes while surrounding objects move toward it.

### Trash-Swirling Internal

Collected debris circulates inside transparent bell.

### Gentle Reposition

Drift to a new position after attack.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Strong Pull

Sequence:

1. Pulse One.
2. Pulse Two.
3. Inhale / body contraction.
4. Strong pull.
5. Optional trash collection.
6. Release/reposition.

Affected targets can include player, loose trash, small props, debris, and approved movable objects.

Increasing internal trash does not redesign outer body.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Slowly float in already carrying a small amount of debris.

### Popped Vulnerable

Canonical **POPPED VULNERABLE - COLLECTED TRASH EXPOSED**:

1. Bell destabilizes.
2. Volume drops.
3. Membrane collapses.
4. Collected debris exposes.
5. Jelly spreads lower.
6. Vulnerability opens.

### Release-Trash Burst

Collected material is expelled outward and must originate from interior. Do not generate unrelated debris from nowhere.

### Hit / React

Body deformation, eye reaction, stars, tentacle lag, internal trash shift.

### Recovery / Reinflate

Membrane gathers, bell rises, body expands, tentacles reform, transparent volume returns. No one-frame full restoration.

### Defeat / Harmless Float-Away

Canonical non-destructive defeat. Creature becomes smaller/deflated/harmless/low-energy and floats away.

## 11. Animation State Inventory

### Existing

- Idle Float
- Hover Drift
- Double-Pulse Telegraph
- Suction Inhale / Contraction
- Strong Pull Attack
- Trash-Swirling Internal
- Gentle Reposition / Float
- Popped Vulnerable
- Release-Trash Burst
- Hit / React
- Recovery / Reinflate
- Defeat / Harmless Float-Away
- Effects & Props

### Required expanded states

- Entry Float
- Idle Float
- Drift Start / Loop / Brake
- Detect Player
- Pulse One / Recovery / Pulse Two
- Inhale Begin
- Contraction
- Weak Pull / Strong Pull / Sustained Pull
- Trash Capture
- Internal Swirl
- Suction Release
- Reposition
- Hit / Heavy Hit
- Pop Anticipation / Pop
- Vulnerable Collapse / Idle
- Trash Release
- Recovery Gather / Reinflate / Full Recovery
- Defeat Deflate / Harmless Float / Exit

## 12. Animation Construction and Modification Rules

Locked:

- Two-eye design/position
- Bell proportions
- Pale cyan/blue body
- Transparency language
- Lower bell shape
- Tentacle design language
- Overall size class

Check alpha for white/dark fringe, opaque patches, missing highlights, background contamination.

Bell can deform but face/eye spacing/identity remain stable. Contraction is compression of the same organism, not a new small Jelly.

Tentacles use delayed secondary motion and do not independently regenerate each frame.

Track each trash prop through outside -> pulled -> captured -> inside -> released. The same prop cannot be simultaneously inside and outside.

## 13. Collision and Gameplay Readability

Inflated collider follows central bell/body; exclude extreme tentacle tips. Suction uses independent force volume, not VFX bounds. Captured trash generally ceases independent collision while contained. Popped collider shrinks vertically to collapsed mass. Defeated float-away disables damage/suction.

## 14. Effects and Environmental Interaction

Canonical:

- Suction rings
- Airy pull trails
- Orbiting trash particles
- Pulse glow
- Pop burst
- Goo splash/fragments
- Exposed trash
- Stars

Released debris travels farther, falls more slowly, rotates visibly, and remains airborne longer due low gravity. Suction feedback should progress from dust/tiny debris toward larger objects.

## 15. Character Validation Checklist

Reject if:

- Eye count changes
- Bell becomes opaque
- Tentacles become rigid
- Jelly uses wing-like flight
- Only one pulse occurs
- Suction begins before both pulses
- Internal trash changes randomly without collection/release
- Same trash appears inside/outside simultaneously
- Contraction changes face proportions
- Pop state stays same size as inflated form
- Recovery instantly restores full volume
- Defeat destroys Jelly instead of harmless float-away
- Released debris falls too quickly for low gravity

---

# Level 5 Global Animation Production Contract

All approved Level 1-4 rules remain active.

## Low gravity is gameplay

Low gravity affects jump/launch arcs, falls, bounces, debris, props, secondary motion, recovery, and collisions. Do not use Earth-gravity timing and add floating particles afterward.

## Low gravity does not mean everything floats

- Armadillo: ground + ballistic airborne movement.
- Rocket Roach: ground + powered horizontal burst.
- Satellite Hermit Crab: ground only.
- Vacuum Jelly: true floating enemy.

Do not make the first three hover simply because gravity is reduced.

## Momentum persists

Especially Armadillo roll/ricochet, Rocket Roach dash/failure, Vacuum Jelly drift, and loose debris. State transitions inherit appropriate velocity rather than instantly canceling it.

## Powered vs ballistic movement

- Armadillo after launch is primarily ballistic.
- Rocket Roach begins propulsion-driven, becomes ballistic on failure.
- Vacuum Jelly self-propels by body pulse/buoyancy-like control.

These motion languages must remain distinct.

## Debris physics

After force is applied, low-gravity objects have longer ascent, longer apex, slower descent, and slower final settling.

## Vulnerability states are core

- Armadillo: uncurled/stunned.
- Rocket Roach: post-burst tumble.
- Hermit Crab: shell lifted/flipped/exposed.
- Vacuum Jelly: popped/collapsed.

Each changes animation, behavior, defense, collision, and player opportunity.

## Telegraphs cannot be shortened away

Mandatory:

- Armadillo curl-up
- Rocket Roach Warning 1 + Warning 2 + Ignition
- Hermit Crab Signal 1 + Signal 2 + Signal 3
- Vacuum Jelly Pulse 1 + Pulse 2 + contraction

## Circular forms cannot be squashed

Asteroid ball, satellite dish, and Jelly bell maintain approved geometry. Enlarge frame canvas instead of non-uniform scaling.

## Low-gravity secondary motion

Pebbles, antennae, hoses, broken pipes, antenna mast, debris, tentacles, and internal trash require longer follow-through and slower settling.

## State-aware collision

Use different collider behavior for curled/exposed, patrol/dash/crashed, shield-down/shell-up, inflated/popped.

## Cross-Roster Validation

- Armadillo: predict trajectory and redirect.
- Rocket Roach: read warnings, leave lane, punish failure.
- Hermit Crab: wait for shield lift, attack exposure.
- Vacuum Jelly: read double pulse, escape pull, punish pop.

If all four become simple contact-damage enemies with different movement, Level 5 has lost its intended design.

## Level 5 Gunk Mythology

Gunk remains active beyond ordinary Earth environments. Reduced gravity changes the outcomes rather than weakening transformation. The Gunk adapts to context, pushing existing behavior, material, machinery, and physics into extreme new forms.
