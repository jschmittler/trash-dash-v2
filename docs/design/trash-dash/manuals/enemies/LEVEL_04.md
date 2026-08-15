# Trash Dash HD Remake - Enemy Master Specification v1.3
## Level 4: Secret Space Center

**STATUS: APPROVED / LOCKED CANON**

Level 4 shifts the Gunk story into laboratories, machinery, power systems, experimental chemicals, maintenance equipment, and adaptive technology. The Gunk is now interacting with chemistry and machines as well as animals.

## Level 4 Enemy Ecology

| Enemy | Placement | Core archetype | Primary player pressure |
|---|---|---|---|
| Beaker Slime | Ground / bouncing | Transforming mobility enemy | Bounce prediction and color-state recognition |
| Clipboard Hamster | Machine-bound / exposed ground | Environmental operator | Powers hazards until disrupted |
| Mop-Bot 3000 | Ground / mobile machine | Suction hazard / pursuer | Pull force, debris movement, pursuit |
| Phase Gecko | Ground + wall-clinging | Camouflaged ambusher | Hidden threats, tongue strikes, wall attacks |

Core identities:

- Beaker Slime transforms.
- Clipboard Hamster operates.
- Mop-Bot pulls.
- Phase Gecko hides and strikes.

---

# L4-E01: Beaker Slime

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated experimental chemical organism  
**Placement:** Ground / bouncing  
**Archetype:** Bouncing transformer enemy

Each color is gameplay information:

- **BLUE = LOW & QUICK BOUNCE**
- **YELLOW = HIGH & SLOW BOUNCE**
- **RED = LONG HORIZONTAL LEAP**

Color is not decorative. It predicts locomotion.

## 2. Placement and Movement Class

**Primary:** GROUND  
**Movement:** BALLISTIC / BOUNCING

The Beaker Slime does not walk. It uses small hops, low bounces, high bounces, long horizontal leaps, landings, compression, rebound, and chemical transformation. Airborne movement always resolves toward a surface under gravity.

Blue: low trajectory, fast cadence, short airtime.  
Yellow: tall trajectory, slower cadence, long airtime.  
Red: long horizontal displacement with strong forward momentum.

## 3. Size, Scale, and Silhouette

**Relative class:** Small-to-medium.

Outer silhouette is defined by the transparent laboratory flask:

- Wide lower chamber
- Narrow neck
- Open circular top
- Thick glass rim
- Curved shoulders
- Flat lower contact area

Living slime fills much of the lower chamber. The vessel may tilt/compress visually during movement but remains recognizable.

## 4. Immutable Visual Anatomy

### Slime

- Exactly two large primary eyes
- Glossy black eye surfaces with white highlights
- Small expressive mouth
- Rounded amorphous body
- Rounded pseudopod/lobe shapes
- No bones
- No defining teeth
- No fur/claws/conventional feet

Extremities are temporary deformations of one gelatinous mass.

### Vessel

- Clear glass
- Thick upper rim
- Cylindrical neck
- Curved shoulders
- Wide lower chamber
- Strong dark glass outlines
- Pale blue/gray highlights
- Chemical residue/splash marks

The vessel is a canonical part of the character.

### Color states

**Blue:** cobalt/bright laboratory blue, darker internal blobs, blue residue.  
**Yellow:** golden yellow/amber, bright highlights, yellow residue.  
**Red:** saturated red/orange-red, darker internal mass, red residue.

Face, proportions, and anatomy remain the same between colors.

## 5. Color, Material, and Surface Treatment

Glass is transparent, reflective, thick, hard, fragile, and laboratory-made. Slime is glossy, wet, gelatinous, semi-fluid, dense enough to hold shape, and capable of splashing/reforming. Small bubbles/blobs/droplets may be suspended.

Chemical glow may match blue, yellow, or red state and should support readability without overwhelming the character.

## 6. Character Personality and Intent

Curious, energetic, unstable, playful, chemically reactive, slightly confused, and dangerous because it cannot remain still.

Blue can feel quick/twitchy. Yellow buoyant/excited. Red focused/committed. These emotional differences stay secondary to gameplay readability.

## 7. Gunk Transformation and Backstory

Secret Space Center scientists studied experimental fuels, polymers, gels, biological material, and energy-reactive compounds. Gunk contamination did not simply ruin one sample. It organized it.

Chemical reactions became preferences. Viscosity became movement. Chemical state became mood. Eyes and a mouth formed. Researchers attempted to contain it in laboratory glassware, effectively giving it a shell.

Different compounds produced different movement states. Blue stabilized rapid low rebounds, yellow created buoyant high movement, red produced explosive horizontal momentum.

This is a major mythology step: **the Gunk did not merely mutate life. It made something alive.**

## 8. Movement and Navigation Behavior

### Idle / Stand

Slime wobble, eye movement, bubbles, pseudopods, slight vessel vibration, droplets sliding inside glass.

### Bounce Loop / Neutral

`compression -> launch -> airborne rise -> apex -> descent -> impact -> internal compression -> rebound`

Glass defines external trajectory; slime lags/deforms inside due inertia.

### Anticipation

Slime compresses, vessel settles, mass shifts down, eyes focus, active-state cue intensifies.

### Blue

Low, fast, rhythmic.

### Yellow

Greater compression, slower taller arc, possible slight flask tilt.

### Red

Forward pitch with strong speed streaks and long horizontal commitment.

## 9. Attacks, Telegraphs, and Combat Behavior

Movement is the attack system. Do not add unrelated biting/shooting/melee.

### Blue State: Quick Bounce Pressure

Frequent low bounces across short distances.

### Yellow State: High Bounce / Drop

High arc and stronger vertical landing impact.

### Red State: Long Horizontal Leap

Long committed horizontal traversal with clear destination direction.

### Chemical Color Change

Must be visually transitioned through current color -> glow -> chemical transition -> stabilized new color. Never instant-switch without readable cue.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Can ride laboratory machinery/conveyor, bounce in, or sit inert before activation. Approved props include a conveyor/power assembly.

### Exit

Bounce out using current movement state.

### Hit

Glass vibration, slime recoil, eye reaction, wobble, impact marks.

### Stunned / Splash Out

Canonical sequence: stun -> collapse -> tip flask -> spill slime -> ground splash -> shards/debris -> disrupted vulnerable state.

### Recovery

If intact recovery is used after breakage, visibly explain it: slime gathers, chemical glow, shards/glass reform, stable beaker returns. Do not pop instantly to intact flask. If encounter uses broken state as defeat, only use recovery where explicitly supported.

## 11. Animation State Inventory

### Existing

- Idle / Stand
- Bounce Loop / Neutral
- Anticipation Before Bounce
- Blue Bounce State
- Yellow Bounce State
- Red Bounce State
- Landing / Impact
- Chemical Color Change
- Hit / React
- Stunned / Splash Out
- Recovery
- Props
- Effects

### Required expanded states

- Spawn / Activation
- Neutral Idle
- Bounce Compression
- Bounce Launch
- Airborne Rise
- Apex
- Descent
- Landing
- Blue Anticipation / Quick Bounce
- Yellow Anticipation / High Bounce / Heavy Landing
- Red Anticipation / Horizontal Leap / Skid
- Blue-to-Yellow
- Yellow-to-Red
- Red-to-Blue
- Hit
- Heavy Hit
- Stunned
- Flask Tip
- Splash Out
- Broken Vessel
- Slime Gather
- Recovery
- Exit

## 12. Animation Construction and Modification Rules

Locked:

- Two-eye design/proportions
- Facial placement
- Flask silhouette/transparency
- Color-state definitions
- Blue/Yellow/Red gameplay relationship
- Relative slime-to-vessel proportions

Glass neck width, rim, shoulder curve, bottom width, and thickness language remain stable.

Internal slime follows delayed fluid-like motion: lag opposite acceleration, compress down on landing, shift toward lower side on tilt. Do not simply rotate an unchanged slime sprite with flask.

Color transformations may change hue/glow/particles, never face/anatomy/vessel/scale.

## 13. Collision and Gameplay Readability

Primary collider follows physical glass vessel while contained. Airborne damage follows vessel body. Landing can use brief separate impact volume. Splash-out collision follows exposed slime, not previous upright flask dimensions. Shard VFX are not damaging unless explicitly designed.

## 14. Effects and Environmental Interaction

Canonical:

- Bounce dust
- Small impact ring
- Large impact ring
- Blue splash
- Yellow splash
- Red splash
- Chemical glow
- Shard spray
- Goo trail

Effect color must match active state unless mid-transition.

## 15. Character Validation Checklist

Reject if:

- Eye count/face changes
- Flask proportions drift
- Glass becomes opaque
- Blue loses low/quick identity
- Yellow loses high/slow identity
- Red loses long-horizontal identity
- Color transition is unreadable
- Slime moves rigidly inside glass
- Flask stretches to imply motion
- Bounce hovers
- Broken recovery teleports to intact form
- VFX color disagrees with active state

---

# L4-E02: Clipboard Hamster

## 1. Identity and Gameplay Role

**Type:** Gunk-altered laboratory hamster  
**Placement:** Machine-bound environmental operator / exposed ground  
**Archetype:** Environmental operator

The Hamster is a systems enemy. Its danger comes from what it powers rather than direct combat.

## 2. Placement and Movement Class

### Primary

**MACHINE-BOUND / STATIONARY ENVIRONMENTAL OPERATOR**

While in wheel, the Hamster remains tied to a fixed machinery station. The wheel rotates but the full station should not travel unless a separate mobile design is approved.

### Secondary

**GROUND / EXPOSED**

After ejection, the Hamster can scurry, flee, recover, and react on the ground.

## 3. Size, Scale, and Silhouette

Hamster is very small. Complete machine assembly is much larger.

Hamster silhouette:

- Compact round rodent body
- Large rounded head
- Tiny paws
- Rounded ears
- Clipboard
- Headset while operating

Machine silhouette:

- Giant transparent circular exercise wheel
- Dark segmented rim
- Industrial base
- Power module
- Hazard stripes
- Cables/control hardware

## 4. Immutable Visual Anatomy

### Hamster

- Exactly two large black eyes with bright highlights
- Two rounded ears with pink interiors
- Small pink nose
- White/cream muzzle
- Fine whiskers
- Brown/tan fur
- Cream/white belly
- Pale forepaws
- Two arms
- Two legs
- Tiny pinkish paws/feet
- Compact rounded body
- No long rat-like tail

### Clipboard

Brown board, pale paper, dark checklist markings, upper clip.

Canonical rule: **HAMSTER ALWAYS CLUTCHES CLIPBOARD WHEN IN WHEEL.**

### Headset

Dark ear-mounted operator hardware with headband/cable/mic language.

### Wheel

Large, circular, transparent, reinforced with segmented dark metal rings.

Canonical note: **WHEEL IS TRANSPARENT - USE INNER RING LINES FOR READABILITY.**

### Base

Heavy dark metal, hazard striping, blue tech glow, power box, cables, red status light, brackets, floor mount.

## 5. Color, Material, and Surface Treatment

Hamster: medium brown, warm tan, cream, white, pink, black eyes.

Machine: graphite, steel gray, dirty silver, black, hazard yellow, muted orange, cyan/blue tech glow, red warning accent.

Canonical power-up rule: **POWER-UP STATE GLOWS BLUE TO MATCH SPACE LAB TECH.** Do not replace with default green Gunk glow.

## 6. Character Personality and Intent

Extremely serious, industrious, distracted, bureaucratic, proud of responsibility, anxious when interrupted, and more employee than warrior.

It appears to believe it has procedures, checklists, quotas, and important work. Disruption reads as **You are ruining the experiment**, not aggression for aggression's sake.

## 7. Gunk Transformation and Backstory

Laboratory hamsters were used for research and equipment testing. A wheel rig converted movement into electrical power. Gunk increased metabolism, focus, and the compulsion to run while also allowing the animal to associate running with machine operation.

The progression became: running makes lights turn on -> running makes machines work -> running is its job.

Research notes became clipboard, communication hardware became headset, wheel became workstation. It continues powering experiments long after humans are gone because the clipboard says the work must continue.

## 8. Movement and Navigation Behavior

### Stand / Idle

Inside wheel: posture adjustment, clipboard check, instrument look, small wheel motion, ear/whisker motion.

### Slow Roll

Walk/light jog in wheel. Wheel rotates beneath body; station stays fixed.

### Fast Run

Faster paw turnover, body lean, fur motion, clipboard stabilization, machine vibration.

The Hamster must continue holding clipboard while running.

### Operator / Power-Up

Running creates blue energy flowing through cables/machinery.

### Exposed

Low body, fast scurry/flee. Clipboard may separate during ejection. Ground behavior must feel distinct from operator state.

## 9. Attacks, Telegraphs, and Combat Behavior

Primary mechanic: **Power Machinery**.

Connected systems may include moving machinery, electrical hazards, doors, lasers, platforms, lab mechanisms, or enemy-support equipment. Exact system varies by encounter; operator relationship remains `power source -> player disrupts -> machine loses power`.

### Warning / Alert

Hamster looks up, exclamation cue appears, running changes, operator becomes visibly alarmed.

### Vulnerability: Stomped Wheel Eject

Canonical **STOMPED WHEEL EJECT SEQUENCE**:

1. Wheel receives impact.
2. Transparent wheel vibrates/deforms visually.
3. Hamster loses footing.
4. Clipboard separates.
5. Hamster is ejected.
6. Debris/sparks appear.
7. Hamster becomes exposed.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Generally already installed in environment. Player may hear wheel/machine before seeing it.

### Exit

Machine-bound Hamster does not voluntarily exit. Exposed Hamster may flee.

### Hit / React

Exposed sequence: stars, recoil, clipboard displacement, collapse, daze.

### Recovery

Exposed Hamster regains footing and flees. Do not automatically return it to wheel unless a dedicated reentry mechanic is approved.

### Disabled Machine Aftermath

Power loss, smoke, sparks, mechanical damage, impact/explosion language, visibly inactive machinery. Disabled machine must look materially different from active machine.

## 11. Animation State Inventory

### Existing

- Stand / Idle
- Slow Roll
- Fast Run
- Operator / Power-Up
- Warning / Alert
- Stomped Wheel Eject Sequence
- Exposed Hamster / Scurry / Flee
- Hit / React
- Recovery
- Disabled Machine Aftermath
- Props
- Effects

### Required expanded states

Machine-bound: Inactive Operator, Idle, Clipboard Check, Slow Run, Fast Run, Power-Up Transition, Powered Loop, Warning, Alert, Panic Run.  
Ejection: Wheel Impact, Wheel Vibration, Loss of Footing, Clipboard Release, Ejection, Airborne Hamster, Ground Impact.  
Exposed: Dazed, Scurry, Flee, Turn, Hit, Heavy Hit, Recovery, Escape.  
Machine: Power Active, Power Interruption, Short Circuit, Disabled, Smoke Loop, Final Aftermath.

## 12. Animation Construction and Modification Rules

Locked Hamster: eye design, fur pattern, pink nose, rounded ears, compact proportions, clipboard, headset/operator identity.

Clipboard remains in grasp during normal wheel operation. It may separate during ejection but cannot disappear/duplicate/randomly resize.

Wheel remains transparent. Use rim, inner ring lines, highlights, reflections for readability. Never fill opaque gray.

Track foot contact, body center, wheel rotation, clipboard angle, headset position so Hamster appears to drive the wheel rather than slide inside it.

Blue electrical effects remain separate where practical.

## 13. Collision and Gameplay Readability

Machine/wheel uses encounter interaction collider. Hamster can remain protected while inside. Wheel has dedicated stomp/vulnerability interaction zone.

After ejection, collider shrinks to Hamster body. Clipboard normally non-damaging. Connected hazards use their own independent colliders.

## 14. Effects and Environmental Interaction

Canonical:

- Dust puff
- Speed lines
- Energy arc
- Sparks
- Warning alert
- Blue electrical arcs
- Debris
- Smoke
- Machine impacts

Approved note: **USE DUST, SPARKS & DEBRIS FOR IMPACT CLARITY.**

## 15. Character Validation Checklist

Reject if:

- Long rat tail appears
- Clipboard disappears during normal wheel use
- Clipboard duplicates during ejection
- Wheel becomes opaque
- Inner ring structure disappears
- Power glow changes away from cyan/blue
- Entire station moves without explicit design intent
- Hamster slides instead of runs inside wheel
- Exposed Hamster remains machine-sized
- Disabled machine looks active
- Hamster teleports back into wheel
- Headset changes/disappears randomly while operating

---

# L4-E03: Mop-Bot 3000

## 1. Identity and Gameplay Role

**Type:** Gunk-corrupted autonomous cleaning machine  
**Placement:** Ground / mobile machine  
**Archetype:** Mobile suction hazard / pursuer

Mop-Bot patrols, identifies targets as debris, pursues, and uses strong suction to drag creatures/objects inward. It is entirely mechanical.

## 2. Placement and Movement Class

**Placement:** GROUND / MOBILE MACHINE

Supports idle patrol, slow roll, fast pursuit, reverse, pivot, skid, suction stationary/adjusted positioning, short-circuit stumble. No flight, jumps, or wall climbing unless separately approved.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium-to-large standard hazard.

Low/wide silhouette:

- Circular robotic-cleaner chassis
- Thick dark bumper
- Low cylindrical body
- Lower brushes
- Upright yellow wet-floor sign
- Red/orange warning beacon
- Tanks/canisters
- Pipes/hoses
- Cyan/blue front panel
- Industrial detail

Warning sign is the most important vertical identifier.

## 4. Immutable Visual Anatomy

As a machine it has no biological eyes, mouth, fur, limbs, or anatomy.

Canonical machine features:

- Circular chassis
- Dark metal exterior
- Segmented bumper
- Cyan/blue front display/sensor
- Lower cleaning brushes
- Rolling hardware
- Rear/side fluid canisters
- Tubes/cables/pipes
- Mechanical brackets
- Grime/damage

### Wet Floor Sign

Yellow/orange folding sign, dark warning graphics, dirty/scratched, securely mounted. Must not disappear during fast movement.

### Beacon

Red/orange transparent housing, mechanically mounted, increasingly active in warnings.

Do not anthropomorphize Mop-Bot with cartoon eyes, mouth, teeth, or eyebrows.

## 5. Color, Material, and Surface Treatment

- Charcoal
- Gunmetal
- Steel gray
- Black
- Rust
- Hazard yellow
- Orange
- Cyan/blue
- Red warning light

Chassis is scratched, dented, dirty, industrial, heavily used.

Water/cleaning fluid uses pale blue/cyan/white highlights. Not every liquid in the game is green Gunk.

## 6. Character Personality and Intent

Tireless, literal, cheerfully procedural, oblivious, aggressively committed to cleanliness. Musical-note idle cue supports a light cleaning jingle.

The transition from cheerful patrol to aggressive pursuit is part of the humor. It does not hate Trashy. It has classified Trashy as **DEBRIS**.

## 7. Gunk Transformation and Backstory

Originally autonomous facility maintenance: detect debris/spills, clean floors, collect waste, return to maintenance.

When Gunk reached the facility, Mop-Bot tried to clean it. Gunk entered brushes, intake, tanks, tubing, filters, and electronics. Sensor classification broke. The definition of debris expanded from paper/tools to lab samples, animals, and eventually anything moving on the floor.

The cleaning routine survived. Judgment did not. Mop-Bot cheerfully attempts to vacuum the world.

## 8. Movement and Navigation Behavior

### Idle / Patrol

Internal vibration, beacon motion, brushes, small cleaning movement, occasional jingle, cyan front light.

### Slow Roll

Methodical movement with faint water trail near cleaning components.

### Fast Pursuit

Acceleration, increased debris movement, beacon intensity, faster brushes, more pronounced water trail.

### Reverse / Pivot Skid

Circular chassis supports reverse/tight pivot/partial spin/skid. Use dust and warning rings to communicate direction change.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Strong Suction Burst

Canonical multi-stage system.

#### Suction Warning / Build-Up

**BEACON ACCELERATES**.

1. Stabilize.
2. Beacon accelerates.
3. Red warning rings appear.
4. Intake sound increases.
5. Brushes/intake spin up.
6. Loose particles start moving inward.

#### Strong Suction Burst

Cyan/white suction stream forms. Targets may include player, enemies, cans, small debris, lightweight props. This applies real pull force, not just visual wind.

#### Intake / Pull State

Canonical **DRAGS ENEMIES & DEBRIS**. Objects accelerate toward intake, slide/tumble, and generate dirt movement.

### Secondary Threat

Fast-pursuit chassis contact may create damage/displacement but remains secondary to suction identity.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Can enter already patrolling: jingle -> water trail -> beacon -> full robot.

### Exit

Roll out along navigation path.

### Hit / React

Stars, chassis tilt, sign displacement, movement interruption, mechanical recoil.

### Short Circuit / Stumble

Stronger damage state with sparks, blue discharge, smoke, unstable chassis, temporary loss of control.

### Recovery

Stabilize, reduce electricity, level chassis, reset beacon, resume behavior.

### Defeat

Movement stops, beacon flickers out, brushes slow, smoke increases, power down. No giant explosion unless separately designed.

## 11. Animation State Inventory

### Existing

- Idle / Patrol
- Slow Roll / Patrol
- Fast Pursuit Roll
- Suction Warning / Build-Up
- Strong Suction Burst
- Reverse / Pivot Skid
- Intake / Pull State
- Hit / React
- Short Circuit / Stumble
- Recovery
- Props
- Effects

### Required expanded states

- Spawn / Patrol Entry
- Idle Cleaning
- Patrol Roll
- Detect Target
- Pursuit Acceleration
- Fast Pursuit
- Pursuit Brake
- Pivot Left / Right
- Reverse
- Suction Windup
- Beacon Acceleration
- Warning Ring Build
- Weak Intake
- Strong Suction Burst
- Sustained Pull
- Suction Release
- Intake Recovery
- Hit
- Heavy Hit
- Short Circuit
- Stumble
- Disabled Pause
- Recovery
- Defeat / Power Down
- Exit

## 12. Animation Construction and Modification Rules

Locked:

- Circular chassis
- Low profile
- Yellow warning sign
- Red beacon
- Cyan front display
- Brush placement language
- Pipes/tanks
- Dark industrial palette

No facial anthropomorphism.

Warning sign is rigid and may vibrate/tilt slightly but cannot bend like cloth, stretch, or disappear.

Do not non-uniformly stretch chassis for speed. Use motion blur, brush rotation, debris, water trails, speed lines.

Suction effects remain separate and originate from consistent approved intake location.

## 13. Collision and Gameplay Readability

Primary collider follows circular chassis, excluding full sign height, beacon glow, brush extremities, pipes, water spray.

Suction uses dedicated directional pull volume extending beyond body. Fast pursuit contact uses main chassis collider. Pulled debris retains independent collision where appropriate.

## 14. Effects and Environmental Interaction

Canonical:

- Water trail
- Skid dust
- Suction stream
- Suction pull particles
- Red warning rings
- Blue sparks
- Hit stars
- Smoke puffs

Mop-Bot should strongly affect loose paper, trash, cans, dust, and lab debris.

## 15. Character Validation Checklist

Reject if:

- Cartoon face appears
- Warning sign/beacon disappears
- Cyan front light changes arbitrarily
- Chassis becomes non-circular
- Robot stretches for speed
- Suction origin moves randomly
- Warning rings occur after suction begins
- Pulled debris ignores suction direction
- Sign is included as full body collision
- Short circuit looks identical to normal hit
- Mop-Bot flies/jumps without approved redesign

---

# L4-E04: Phase Gecko

## 1. Identity and Gameplay Role

**Type:** Gunk-mutated gecko affected by experimental phase/camouflage technology  
**Placement:** Ground + wall-clinging  
**Archetype:** Camouflaged ambush predator

Canonical sheet establishes:

- **CLINGS TO WALLS**
- **CAMOUFLAGES BY MATCHING PANEL**
- **AMBUSHES PLAYERS WITH TONGUE STRIKE**

All three are core identity rules.

## 2. Placement and Movement Class

**Primary:** SURFACE-CLINGING

Supported surfaces include ground, vertical walls, and approved wall panels. Ceiling traversal is not automatically inferred without dedicated poses/navigation.

States include wall-cling idle, ground crawl, creep, camouflaged wall, reveal, tongue attack, stuck tongue, vulnerable reaction, recovery.

## 3. Size, Scale, and Silhouette

**Relative class:** Medium.

Low horizontal silhouette:

- Oversized rounded head
- Two huge yellow eyes
- Broad low body
- Four limbs
- Wide adhesive toes
- Long curled tail
- Dark pebbled/warty skin
- Long red tongue

Wall pose must appear tightly adhered to surface.

## 4. Immutable Visual Anatomy

- Exactly two primary eyes
- Large yellow/gold eye surfaces
- Black vertical slit pupils
- Thick dark eyelid surrounds
- Broad rounded head
- Small nostrils
- Wide mouth
- Small white teeth in open-mouth expressions
- Long pink/red tongue
- Four limbs
- Broad adhesive feet
- Multiple rounded toe pads
- One long curled tail
- Dark slate-blue/gray skin
- Raised bumps/nodules across head/back/tail
- Lighter blue-gray reflective spots
- Low rounded body

No horns, spikes, fur, or armor.

### Camouflage

Copies surrounding panel texture. Canonical camouflage idle keeps **eyes visible** as player detection cue.

## 5. Color, Material, and Surface Treatment

Normal palette:

- Slate gray
- Blue-black
- Charcoal
- Dark blue
- Blue-gray highlights
- Golden yellow eyes
- Black pupils
- Pink-red tongue
- White teeth

Skin is pebbled, thick, slightly moist, rubbery, uneven, nodular. Do not smooth into generic lizard.

Camouflage imitates actual wall panel, seams, industrial plating, cables, and local color. Slight digital/phase instability differentiates it from architecture.

## 6. Character Personality and Intent

Patient, watchful, predatory, curious, extremely still, suddenly aggressive, and slightly confused by its own tongue when attacks fail. Confidence comes from believing it cannot be seen.

The stuck-tongue failure is a comic weakness.

## 7. Gunk Transformation and Backstory

The facility studied adaptive surface materials for spacecraft coatings, habitat concealment, thermal regulation, and camouflage. Geckos were used in adhesion studies.

Gunk contaminated both programs. Adaptive material properties were carried into Gecko biology. Skin began copying panels, adhesive feet strengthened, and the already-extensible tongue became longer/heavier/more adhesive.

The Gecko became perfectly adapted to abandoned architecture: it hides by becoming the wall, then attacks before the player realizes the wall has eyes.

## 8. Movement and Navigation Behavior

### Wall-Cling Idle

Extremely subtle eye movement, breathing, toe adjustment, tongue flick, tail tension. Gravity influences body mass without visible sliding.

### Crawl / Creep

Low coordinated four-limb crawl. Adhesive toes visibly contact/release.

### Camouflage Idle

Body progressively matches panel. Eyes remain readable. Do not instant-disappear.

### Flicker / Reveal

Use purple pixels, blue/cyan fragments, digital shimmer, surface breakup, then normal body. It is unstable experimental camouflage, not magic.

## 9. Attacks, Telegraphs, and Combat Behavior

### Primary Attack: Tongue Strike

Telegraph:

1. Reveal/partially reveal.
2. Lower body.
3. Focus eyes.
4. Open mouth.
5. Show tongue.
6. Pull head slightly back.

Tongue launches rapidly, remains attached to mouth, follows clear line, retains red/pink color, and ends in enlarged adhesive tip.

### Tongue Extended Stuck State

Canonical failure mechanic. Tongue may adhere to approved wall fixtures, panels, pipes, or hard anchors. Once stuck, tongue remains taut, Gecko strains backward, movement is restricted, and vulnerability opens.

Do not instantly cancel stuck state.

## 10. Entry, Exit, Hit, and Defeat Behavior

### Entry

Preferred: already camouflaged on wall. Eyes/subtle shimmer reveal presence.

### Exit

Crawl off-screen, move to adjacent wall, or re-enter camouflage. No teleport between panels.

### Hit

Stars, tongue displacement, compression, eye reaction, collapse, phase/purple breakup in later frames.

### Recovery

Restore posture, retract tongue, resume low movement.

### Defeat

Heavy hit -> phase instability -> increasing purple/cyan artifacts -> loss of camouflage cohesion -> collapse or phased disappearance. Avoid realistic injury.

## 11. Animation State Inventory

### Existing

- Wall-Cling Idle Variations
- Crawl / Creep
- Camouflage Idle / Eyes Visible
- Flicker / Reveal Sequence
- Tongue Strike
- Tongue Extended Stuck State
- Vulnerable / Stuck Reaction
- Hit / React
- Recovery
- Props & Debris
- Effects
- Decor / Drips

### Required expanded states

Surface: Wall Attach, Wall Idle, Wall Crawl, Ground Crawl, Turn, Surface Transition.  
Camouflage: Camo Begin, Partial Camo, Camo Idle, Eye Tracking, Camo Shimmer, Reveal Flicker, Full Reveal.  
Attack: Detect Player, Tongue Telegraph, Launch, Mid-Extension, Full Extension, Impact, Retract, Miss, Stuck.  
Vulnerability: Initial Stuck Reaction, Pull/Strain, Exhausted Stuck, Tongue Release, Recovery.  
Damage: Hit, Heavy Hit, Phase Instability, Dazed, Defeat, Retreat/Re-camouflage, Exit.

## 12. Animation Construction and Modification Rules

Locked:

- Two large yellow eyes
- Vertical pupils
- Four limbs
- Adhesive toe pads
- Tail length/curl
- Dark pebbled skin
- Surface nodules
- Red/pink tongue
- Broad head proportions

Wall contact integrity is mandatory. At least a believable subset of feet remains planted while others move. No floating toes, sliding body, detached limbs.

Tail provides balance, may curl/uncurl/lag/press toward wall, but cannot duplicate/change length/detach.

Camouflage must derive from the **actual intended panel appearance**, not generic metal. Preserve underlying anatomy.

Tongue is one continuous structure from mouth -> shaft -> adhesive tip. Never duplicate or detach it while also leaving a tongue in the mouth.

## 13. Collision and Gameplay Readability

Core collider follows head, torso, central limb mass; exclude full tail/toes/inactive tongue.

Wall-state collider orientation follows surface. Do not retain ground-oriented collider while wall-clinging.

Tongue has independent temporary attack collider. Once stuck to scenery, attack collision may deactivate while vulnerability begins.

## 14. Effects and Environmental Interaction

Canonical:

- Purple digital pixels
- Purple phase burst
- Cyan/blue electrical shimmer
- Smoke
- Speed streaks
- Impact burst
- Wall panels
- Pipes
- Tech debris
- Facility drips/sludge

Camouflage/reveal effects should loop cleanly where required and only on intentionally supported surfaces.

## 15. Character Validation Checklist

Reject if:

- Eye count changes
- Eyes disappear completely during canonical camo idle
- Pupils stop being vertical
- Limb count changes
- Tail duplicates
- Skin becomes smooth
- Body floats off wall
- Feet slide during cling
- Camouflage uses unrelated generic texture
- Reveal has no flicker
- Tongue duplicates/detaches/emerges from wrong location
- Stuck state instantly cancels
- Purple/cyan phase language disappears
- Wall collider remains ground-oriented

---

# Level 4 Global Animation Production Contract

All approved Level 1-3 rules remain active.

## Transformation types

- Beaker Slime: chemical creation/transformation.
- Clipboard Hamster: biological/behavioral transformation.
- Mop-Bot 3000: mechanical corruption.
- Phase Gecko: biological + technological transformation.

Do not force all four into a single green-monster language.

## Transforming identity

Beaker color changes, design does not. Phase Gecko surface appearance changes, anatomy does not.

## Transparent assets

Beaker glass and Hamster wheel require explicit alpha validation for halos, matte, clipped highlights, missing interior lines, background contamination, and excessive transparency.

## Machinery is not anatomy

Hamster != wheel != power station. Phase Gecko panel is environment. Beaker glass remains distinct from slime. Mop-Bot VFX are not robot anatomy.

## Environmental systems

Document explicit source -> state -> affected object -> gameplay result relationships for Hamster-powered systems, Mop-Bot debris, Gecko camouflage panels, and any externally controlled Beaker state.

## Surface orientation

Phase Gecko wall behavior requires dedicated contact/collision validation. A rotated ground cycle is insufficient if it breaks anatomy/contact.

## Color is gameplay information

Beaker blue/yellow/red need non-color supporting motion cues as accessibility reinforcement:

- Blue: fast compression/low arc
- Yellow: strong upward anticipation/tall arc
- Red: forward lean/horizontal streaks

## Vulnerability states

- Beaker: splash-out/stunned
- Hamster: ejected
- Mop-Bot: short-circuit/stumble
- Gecko: tongue stuck

Each needs entry condition, animation, behavior/collision change, duration, and recovery.

## Material-specific VFX

Chemical slime is wet/viscous. Electricity is sharp/branching. Suction is directional/particle-driven. Phase tech is digital/fragmented. Do not reuse one generic effect language.

## Cross-Roster Validation

- Beaker: read color, predict bounce.
- Hamster: disrupt operator, shut system down.
- Mop-Bot: avoid/resist directional pull.
- Gecko: watch environment and punish failed tongue strike.

Level 4 should feel systemic, not like four ordinary chase enemies.
