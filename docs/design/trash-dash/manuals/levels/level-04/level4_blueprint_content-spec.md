# Content Spec — Level 4 Blueprint (A1)

**Status:** EXECUTED — Phase 2 complete (2026-08-13)  
**Deliverable:** Blueprint — Level 4 — Secret Space Center  
**Internal ID:** `level_4_secret_space_center`  
**Output path (on approval):** `docs/level-design/blueprints/level4_secret_space_center_full_layout.png`

---

## References pinned

### Blueprint layout (match exactly)
- `level-1-blueprint-80e4f6e6-8bd8-48e8-baa6-d49a69ff4c08.png`
- `level-2-blueprint-1fbef721-8bd3-4a95-a3cf-12b447947a66.png`
- `level-6-blueprint-f5b6567c-0b73-4f3d-8f22-30524257595b.png`

### Level-specific sources
- `level-4-concept-31753bc4-a652-4e76-884b-3e39ae6f96f1.png`
- `boss-94199dac-3731-48fa-8c9d-5c84b276c466.png` (Project O.P.O.S.S.U.M.)
- `output/level4/level4_secret_space_center.png` + manifest

### Global gameplay sources
- `powerups-sprite-sheet-approved-2240eb5f-8659-4b9a-9e11-d0719b008146.png` (Taco + Kite — one of each per level)

### Enemy canon (authoritative)
- `docs/enemy-canon/ENEMY_MASTER_CONTRACT.md`
- `docs/enemy-canon/LEVEL_04.md`
- `docs/enemy-canon/reference-art/level-04/beaker-slime.png`
- `docs/enemy-canon/reference-art/level-04/clipboard-hamster.png`
- `docs/enemy-canon/reference-art/level-04/mop-bot-3000.png`
- `docs/enemy-canon/reference-art/level-04/phase-gecko.png`

---

## Header

- **Logo:** Rustic wooden plank sign, `TRASH DASH`, green vine accents (per blueprint refs).
- **Subtitle (verbatim):** `- LEVEL 4 | FULL LAYOUT CONCEPT -`

---

## Environment & art direction

- **Setting:** Secret underground space center at night — industrial concrete/steel, mossy playable surfaces, hazard yellow-black striping, glowing green containment energy.
- **Sky/backdrop:** Starry purple night sky visible through windows/open hangar bays; distant rocket on launchpad, satellite dishes, facility domes (per Level 4 concept).
- **Lighting:** Cool blue facility lighting + green glow from stasis tubes, reactor core, and containment fluid; red boss-arena alarm accents in Zone 8.
- **Terrain:** Moss-topped metal/concrete platforms with visible structural support — nothing floats unsupported (per Level 4 concept design notes).
- **Props interaction rule:** Standable/blocking/non-interactive only — **nothing in the level is smashable or breakable.**
- **Do not use:** Props, enemies, or biomes from other levels.

---

## Zones (in order)

| # | Zone name | Tagline |
|---|-----------|---------|
| 1 | HIDDEN SERVICE ENTRANCE | Sneak past the sealed vault doors. |
| 2 | LAB CORRIDOR | Learn the mossy steel floors. |
| 3 | REACTOR APPROACH | Step up the braced platform. |
| 4 | EXPERIMENTAL LABS | Thread the stasis tube gallery. |
| 5 | CONTAINMENT WING | Navigate hazmat crates and barriers. |
| 6 | REACTOR PIT TRENCH | Clear the containment fluid gap. |
| 7 | ROBOTICS CHAMBER | Dodge overhead arms and carts. |
| 8 | ROCKET HANGAR | Boss Battle: Project O.P.O.S.S.U.M. |
| 9 | THE DUMPSTER | Into the bin — goal reward. |

---

## Panorama — zone-by-zone layout

### Zone 1 — HIDDEN SERVICE ENTRANCE
- **Start position:** Trashy at far left on mossy metal grating.
- **Set dressing:** Heavy circular vault/service door (boss spec “Hidden Service Entrance”); purple/red indicator lights; `KEEP OUT` hazard markings.
- **Props:** `level4_warning_barrier` flanking the entry path; `level4_cable_bundle` ground clutter.
- **Collectibles:** 3–4 trash tokens in a gentle arc introducing movement.
- **Enemies:** 1× **Beaker Slime** (blue state) — flat ground patrol, first enemy intro.
- **Verticality:** Flat intro lane.

### Zone 2 — LAB CORRIDOR
- *Maps to Level 4 concept Panel 1 — Main Ground Lane / Lab Corridor.*
- **Set dressing:** Door labeled `LAB 04` with green keypad; window into lab with glowing green stasis tubes; distant rocket silhouette.
- **Props:** `level4_floor_terminal` (ACCESS GRANTED screen); `level4_hazard_storage_crate` (standable top, blocking body); `level4_utility_barrel` beside corridor wall.
- **Collectibles:** Trash tokens along the corridor floor and one elevated arc over the hazard crate.
- **Enemies:** 1× **Beaker Slime** (yellow state) on floor; 1× **Mop-Bot 3000** corridor patrol with visible suction cone VFX hint.
- **Terrain:** Flat mossy steel/concrete lane with yellow-black edge striping.

### Zone 3 — REACTOR APPROACH
- *Maps to Level 4 concept Panel 2 — Raised Platform / Step-Up.*
- **Set dressing:** Tall braced concrete/steel support block with X-bracing; metal ladder on right face.
- **Props:** `level4_floor_terminal` on platform top; `level4_maintenance_trolley` at base (standable top shelf).
- **Power-up:** **Taco Power-Up** floating above upper platform with golden collectible highlight ring (approved power-up sheet, state 5).
- **Collectibles:** Tokens on lower lane + upper platform reward cluster.
- **Enemies:** 1× **Beaker Slime** (red state) on upper platform — teaches horizontal leap telegraph before pit.
- **Verticality:** Required step-up jump or ladder climb to continue.

### Zone 4 — EXPERIMENTAL LABS
- *Maps to boss spec “Experimental Labs” location.*
- **Set dressing:** Row of glowing green stasis/containment tubes with silhouettes; computer consoles; purple-lit lab walls.
- **Props:** `level4_containment_pod` (×2, standable tops); `level4_sample_canister` as placed collectible prop; `level4_lab_bin` (standable rim).
- **Collectibles:** Trash tokens threading between pods; 1 `sample_canister` collectible (glowing green glass cylinder).
- **Enemies:** 1× **Beaker Slime** (blue state) between pods; 1× **Clipboard Hamster** in wheel rig beside console — visibly powering stasis-tube machinery (operator encounter).
- **Terrain:** Multi-tier lab floor with one raised pod walkway.

### Zone 5 — CONTAINMENT WING
- **Set dressing:** `RESTRICTED AREA` / radiation signage; industrial pipes; caution striping.
- **Props:** `level4_warning_barrier` (×2); `level4_hazard_storage_crate` (×2, standable/blocking); `level4_utility_barrel` stack (blocking).
- **Collectibles:** Tokens placed after barrier gaps requiring timed movement.
- **Enemies:** 1× **Clipboard Hamster** operating barrier/warning-light system; 1× **Mop-Bot 3000** patrolling behind barriers.
- **System read:** Hamster powers active hazard lights/barriers until disrupted (per L4-E02 canon).

### Zone 6 — REACTOR PIT TRENCH
- *Maps to Level 4 concept Panel 4 — Reactor Pit / Containment Fluid Trench.*
- **Hazard:** Wide gap between platforms filled with glowing green containment fluid with electric arcs — **fall/death hazard**.
- **Set dressing:** Yellow sign reading `DANGER REACTOR PIT` with radiation symbol; massive glowing green reactor core in distant background.
- **Props:** `level4_vent_box` (standable tops) on landing platforms at each side; `level4_cable_bundle` near edges.
- **Power-up:** **Kite Power-Up** on the blue challenge-route high path with wind-ring collectible highlight (approved power-up sheet, state 5).
- **Collectibles:** High-route token cluster above the pit (blue challenge route reward).
- **Enemies:** 1× **Phase Gecko** wall-clinging on vertical pit wall near far landing — semi-camouflaged, tongue-strike ambush position (not on pit floor).
- **Path overlays:**
  - **Green dashed shortcut:** Upper catwalk bypass via stacked `level4_vent_box` platforms, skipping lower landing gecko line-of-sight.
  - **Blue dashed challenge route:** High arc over reactor pit — kite power-up + bonus tokens.

### Zone 7 — ROBOTICS CHAMBER
- *Maps to Level 4 concept Panel 3 — Service Catwalk / Lab Module + boss spec “Robotics Chambers”.*
- **Set dressing:** Overhead industrial robot/claw arms; door labeled `ACCESS 7A`; large circular ventilation fan in close background.
- **Props:** Elevated catwalk with visible support struts below; `level4_rolling_tool_cart` (×2, blocking); `level4_maintenance_trolley` (standable top); metal ladder/stairs to catwalk.
- **Collectibles:** Trash tokens along catwalk; 1 `level4_energy_cell` collectible on side alcove.
- **Enemies:** 1× **Mop-Bot 3000** on lower floor (pursuit lane); 1× **Phase Gecko** on catwalk wall segment; 1× **Clipboard Hamster** at control panel operating overhead claw arm.
- **Verticality:** Catwalk is secondary platform tier (player can pass under or over).

### Zone 8 — ROCKET HANGAR (Boss Arena)
- *Maps to boss spec “Rocket Hangar Systems” + central boss illustration.*
- **Set dressing:** Circular industrial platform with `KEEP OUT` skull markings and blue recessed lights; red-and-white rocket visible in background between blast doors; alarm lighting.
- **Boss:** **Project O.P.O.S.S.U.M.** (Escaped Prototype Boss) — cybernetic opossum with glass dome power core, red siren, sparking tail plug, plate reading `O.P.O.S.S.U.M. UNIT 09-X`.
- **Health bar:** Yes — red bar above boss labeled `PROJECT O.P.O.S.S.U.M.`
- **Arena features (visual only, no phase diagram):** Wall socket for tail plug; `CAUTION` doorway suggesting hazard triggers; vertical metal wall segment suggesting wall-climb attack.
- **Enemies:** Boss only — no standard enemies.
- **Terrain:** Flat circular arena platform, wide enough for boss scale (~2× Trashy height).

### Zone 9 — THE DUMPSTER (Goal)
- **Set dressing:** Rocket hangar exit lane narrowing to goal staging.
- **Goal object:** Green industrial dumpster with recycling symbol and small green flag — matching Levels 1/2/6 goal pattern.
- **Props:** `level4_lab_bin` beside dumpster as set dressing; scattered token reward cluster near goal.

---

## Player character

- **Trashy** at Zone 1 start — yellow bandana, backpack (consistent with Level 2/6 blueprints).

---

## Standard enemies

> **Canon source:** `docs/enemy-canon/LEVEL_04.md` — Level 4 should feel systemic, not like four ordinary chase enemies.

### Roster

| ID | Name | Placement class | Archetype | Reference art |
|----|------|-----------------|-----------|---------------|
| L4-E01 | Beaker Slime | Ground / bouncing | Transforming mobility — color predicts bounce (blue=low/quick, yellow=high/slow, red=long leap) | `reference-art/level-04/beaker-slime.png` |
| L4-E02 | Clipboard Hamster | Machine-bound / exposed ground | Environmental operator — powers hazards until wheel stomped | `reference-art/level-04/clipboard-hamster.png` |
| L4-E03 | Mop-Bot 3000 | Ground / mobile machine | Suction hazard / pursuer — directional pull + pursuit | `reference-art/level-04/mop-bot-3000.png` |
| L4-E04 | Phase Gecko | Ground + wall-clinging | Camouflaged ambusher — tongue strikes from walls | `reference-art/level-04/phase-gecko.png` |

### Placement map (9 standard enemies, Zones 1–7)

| Zone | Enemy | Count | Placement notes |
|------|-------|-------|-----------------|
| 1 | Beaker Slime | 1 | Blue state; flat entry grating |
| 2 | Beaker Slime | 1 | Yellow state; corridor floor |
| 2 | Mop-Bot 3000 | 1 | Corridor patrol; suction cone readable |
| 3 | Beaker Slime | 1 | Red state; upper platform only |
| 4 | Beaker Slime | 1 | Blue state; pod walkway |
| 4 | Clipboard Hamster | 1 | Wheel rig at console; powers stasis machinery |
| 5 | Clipboard Hamster | 1 | Powers warning barriers/lights |
| 5 | Mop-Bot 3000 | 1 | Behind barriers |
| 6 | Phase Gecko | 1 | Wall-cling on pit wall; far side only |
| 7 | Mop-Bot 3000 | 1 | Lower floor pursuit lane |
| 7 | Phase Gecko | 1 | Catwalk wall segment |
| 7 | Clipboard Hamster | 1 | Operating overhead claw arm panel |

**Totals:** 4× Beaker Slime · 3× Clipboard Hamster · 2× Mop-Bot 3000 · 2× Phase Gecko  
**Zone 8:** Boss only.

### Placement rules (from canon)
- Beaker Slime: ballistic bouncing only — always resolves to a surface; show color state visually.
- Clipboard Hamster: machine-bound when operating; show connected system (barriers, claws, stasis tubes).
- Mop-Bot 3000: ground mobile only; suction direction readable in illustration.
- Phase Gecko: wall-cling positions on vertical surfaces only — not floating; semi-camouflaged against lab walls.

---

## Boss

| Field | Value |
|-------|-------|
| **Name** | Project O.P.O.S.S.U.M. |
| **Subtitle** | Escaped Prototype Boss |
| **Arena zone** | 8 — ROCKET HANGAR |
| **Health bar** | Yes — `PROJECT O.P.O.S.S.U.M.` |
| **Defeat condition** | 3 hits to defeat *(from boss spec — not illustrated in blueprint)* |
| **Key visual traits** | Opossum face; metal harness; glass dome with blue liquid; red siren; mechanical tail with two-prong electrical plug; sparks |

---

## Goal

- **Label:** Zone 9 — THE DUMPSTER
- **Object:** Green industrial dumpster with recycling symbol + green flag.
- **Tagline:** Into the bin — goal reward.

---

## Collectibles, power-ups & interactives

| Item | Visual | Placement |
|------|--------|-----------|
| **Trash Tokens** | Yellow glowing trash-bag icons (standard) | Arcs and lines throughout all zones; densest before boss and at goal |
| **Taco Power-Up** | Approved taco sheet — idle/bob with golden highlight ring | Zone 3 — upper platform of Reactor Approach |
| **Kite Power-Up** | Approved kite sheet — idle/bob with blue wind ring | Zone 6 — blue challenge route over Reactor Pit |
| **Sample Canister** | `level4_sample_canister` | Zone 4 — Experimental Labs |
| **Energy Cell** | `level4_energy_cell` | Zone 7 — Robotics Chamber alcove |

**Global rule:** Exactly **1 Taco** and **1 Kite** per level.

---

## Legend bar (bottom-left)

*Level 2 extended pattern — no breakable entry.*

### Row 1 — Characters, collectibles & power-ups

| Icon | Label | Description |
|------|-------|-------------|
| Trashy raccoon head | TRASHY (FAST & AGILE) | Player character |
| Composite enemy icon strip | ENEMIES (VARIES) | Beaker Slime · Clipboard Hamster · Mop-Bot 3000 · Phase Gecko |
| Yellow glowing trash bag | COLLECTIBLES (TRASH TOKENS) | Collect to score! |
| Golden taco | TACO POWER-UP (SUPER POWER ITEM) | Ultra powered! |
| Color diamond kite | KITE POWER-UP (FLYING ABILITY) | Soar over hazards! |

### Row 2 — Path & hazard

| Icon | Label | Description |
|------|-------|-------------|
| Green ladder | SHORTCUT (ALTERNATE ROUTE) | Risk vs. reward. |
| Gold trophy/token | CHALLENGE ROUTE (HIGH RISK / HIGH REWARD) | Harder path, more tokens. |
| Radiation symbol | HAZARD (FALL / DANGER) | Reactor pit — avoid the fluid. |

---

## Path overlays (confirmed)

| Type | Color | Usage |
|------|-------|-------|
| Main path | White dashed arrows (zone strip only) | Intended route through all 9 zones |
| Shortcut | Green dashed line | Zone 6 — upper vent-box catwalk bypass |
| Challenge route | Blue dashed line | Zone 6 — high arc over reactor pit (kite + bonus tokens) |

---

## Footer — Boss callout card (Level 2 / Brutus pattern)

- **Type:** Boss callout (parchment card, bottom-right)
- **Portrait:** Project O.P.O.S.S.U.M. head/bust — cybernetic opossum with dome core and red siren
- **Heading (verbatim):** `LEVEL 4: PROJECT O.P.O.S.S.U.M.`
- **Body copy (verbatim):**

> Escaped prototype on the loose. Overcharges machinery, climbs walls, and triggers room hazards. Three hits shuts it down — if you survive the short circuit!

---

## Level assets used (all from `output/level4/`)

| Sprite ID | Zones | Interaction |
|-----------|-------|-------------|
| `level4_warning_barrier` | 1, 5 | blocking |
| `level4_cable_bundle` | 1, 6 | blocking |
| `level4_floor_terminal` | 2, 3 | non_interactive |
| `level4_hazard_storage_crate` | 2, 5 | standable + blocking |
| `level4_utility_barrel` | 2, 5 | blocking |
| `level4_maintenance_trolley` | 3, 7 | standable + blocking |
| `level4_containment_pod` | 4 | standable |
| `level4_sample_canister` | 4 | collectible |
| `level4_lab_bin` | 4, 9 | standable + blocking |
| `level4_vent_box` | 6 | standable |
| `level4_rolling_tool_cart` | 7 | blocking |
| `level4_energy_cell` | 7 | collectible |

All 12 Level 4 manifest sprites placed at least once. None depicted as breakable/smashable.

---

## Resolved decisions

| Item | Decision |
|------|----------|
| Breakables | None — standable/blocking/non-interactive only |
| Shortcuts | Green shortcut + blue challenge route in Zone 6 |
| Power-ups | 1 Taco (Zone 3) + 1 Kite (Zone 6) |
| Footer | Boss callout card (L2 / Brutus style) |
| Zone 8 name | ROCKET HANGAR |
| Standard enemies | Full Level 4 roster from `docs/enemy-canon/LEVEL_04.md` |

---

## Approval checklist

- [x] Zone names + taglines defined
- [x] Standard enemy roster + per-zone placement defined
- [x] Power-ups, shortcuts, footer confirmed
- [x] User approves boss callout copy verbatim
- [x] User approves enemy placement map
- [x] Ready for Phase 2 execution
- [x] Blueprint generated: `docs/level-design/blueprints/level4_secret_space_center_full_layout.png`
