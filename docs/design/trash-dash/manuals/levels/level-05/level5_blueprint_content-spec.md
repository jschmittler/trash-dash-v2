# Content Spec — Level 5 Blueprint (A2)

**Status:** EXECUTED — Phase 2 complete (2026-08-13)  
**Deliverable:** Blueprint — Level 5 — Orbital Junkyard  
**Internal ID:** `level_5_orbital_junkyard`  
**Output path:** `docs/level-design/blueprints/level5_orbital_junkyard_full_layout.png`

---

## References pinned

### Blueprint layout
- `level-1-blueprint-80e4f6e6-8bd8-48e8-baa6-d49a69ff4c08.png`
- `level-2-blueprint-1fbef721-8bd3-4a95-a3cf-12b447947a66.png`
- `level-6-blueprint-f5b6567c-0b73-4f3d-8f22-30524257595b.png`
- `docs/level-design/blueprints/level4_secret_space_center_full_layout.png` (completed A1 reference)

### Level-specific sources
- `level-5-concept-96ac3909-a9fa-4b9b-b023-16754dca3cb3.png`
- `boss-4afb2232-bf79-414d-9d8f-222fed4a9712.png` (GalactoGobbler)
- `output/level5/level5_orbital_junkyard.png` + manifest

### Global gameplay sources
- `powerups-sprite-sheet-approved-2240eb5f-8659-4b9a-9e11-d0719b008146.png`

### Enemy canon
- `docs/enemy-canon/LEVEL_05.md`
- `docs/enemy-canon/reference-art/level-05/asteroid-armadillo.png`
- `docs/enemy-canon/reference-art/level-05/rocket-roach.png`
- `docs/enemy-canon/reference-art/level-05/satellite-hermit-crab.png`
- `docs/enemy-canon/reference-art/level-05/vacuum-jelly.png`

---

## Header

- **Subtitle (verbatim):** `- LEVEL 5 | FULL LAYOUT CONCEPT -`

---

## Zones (in order)

| # | Zone name | Tagline |
|---|-----------|---------|
| 1 | SALVAGE DECK | Junk-strewn metal route. |
| 2 | ASTEROID STEP-UP | Grounded rock and scrap platform. |
| 3 | CRANE DOCK | Cross the cantilever scrap deck. |
| 4 | COSMIC SLUDGE GAP | Clear the neon goo chasm. |
| 5 | DEBRIS FIELD | Pick through satellite wreckage. |
| 6 | CRYSTAL OUTCROP | Navigate meteor chunks and alien trash. |
| 7 | CARGO BAY | Pods, pallets, and barrels. |
| 8 | JUNK-WORLD FINALE | Boss Battle: GalactoGobbler |
| 9 | THE DUMPSTER | Keep space clean(ish) — goal reward. |

---

## Panorama — zone-by-zone layout

### Zone 1 — SALVAGE DECK
- Trashy start left on riveted metal deck with yellow-black hazard striping; purple nebula + planet in background (Orbital Structures).
- Props: `level5_salvage_signpost`; scattered tires/pipes; red skull flags.
- Enemies: 1× Satellite Hermit Crab patrol.
- Collectibles: trash token intro arc.

### Zone 2 — ASTEROID STEP-UP
- Purple asteroid rock mound + anchored scrap structure (concept Panel 2).
- Props: `level5_meteor_chunk`; hazard-striped container; `level5_low_g_scrap_barrel`.
- Enemies: 1× Asteroid Armadillo (curled roll position).
- Collectibles: tokens on lower/upper tiers.

### Zone 3 — CRANE DOCK
- Cantilever platform on industrial crane arm (concept Panel 3); nothing floats unsupported.
- Props: `level5_cargo_pallet`; crane hook visible.
- Power-up: **Taco Power-Up** on upper crane deck.
- Enemies: 1× Rocket Roach on platform.
- Verticality: step-up or ladder to crane deck.

### Zone 4 — COSMIC SLUDGE GAP
- Neon green cosmic sludge chasm between decks (concept Panel 4); skull hazard sign.
- Props: `level5_floating_junk_anchor` (chain from grounded base).
- Hazard: fall/death goo pit.
- Enemies: 1× Vacuum Jelly floating above gap.
- Path overlays: green shortcut under-deck bypass; blue challenge route high arc.

### Zone 5 — DEBRIS FIELD
- Satellite Graveyard — broken dishes, solar panels (boss spec location).
- Props: `level5_satellite_debris_pile`; `level5_broken_bot_husk`.
- Enemies: 1× Satellite Hermit Crab; 1× Rocket Roach.
- Collectibles: tokens hidden in debris pile angles.

### Zone 6 — CRYSTAL OUTCROP
- Nebula Asteroid Mine — purple crystals, dark asteroids (boss spec location).
- Props: `level5_cosmic_crystal_cluster`; `level5_alien_trash_mound`.
- Power-up: **Kite Power-Up** on blue challenge-route high ledge.
- Enemies: 1× Asteroid Armadillo on meteor slope; 1× Vacuum Jelly drifting.
- Path overlays: blue dashed high route with kite + bonus tokens.

### Zone 7 — CARGO BAY
- Abandoned Alien Station interior — purple conduit glow (boss spec location).
- Props: `level5_space_cargo_pod`; `level5_maintenance_crate`; `level5_oxygen_canister` collectible.
- Enemies: 1× Rocket Roach; 1× Vacuum Jelly; 1× Satellite Hermit Crab.
- Collectibles: `oxygen_canister` in alcove.

### Zone 8 — JUNK-WORLD FINALE (Boss Arena)
- Junk-World Finale horizon — towers of rusted scrap under orange-purple cosmic sky.
- Boss: **GalactoGobbler, Hoarder of Worlds** — spherical junk shell, purple alien core, glowing blue trash bin, mechanical legs, purple-lit platform.
- Health bar: `GALACTOGOBBLER`
- Arena: wide metal platform; low-gravity debris floating subtly.

### Zone 9 — THE DUMPSTER
- Green dumpster + flag GOAL; token cluster; `level5_cargo_pallet` set dressing.

---

## Standard enemies (from LEVEL_05.md)

| ID | Name | Placement | Zones |
|----|------|-----------|-------|
| L5-E01 | Asteroid Armadillo | Ground + ballistic low-gravity | 2, 6 |
| L5-E02 | Rocket Roach | Ground + rocket burst | 3, 5, 7 |
| L5-E03 | Satellite Hermit Crab | Ground | 1, 5, 7 |
| L5-E04 | Vacuum Jelly | Floating / aerial | 4, 6, 7 |

**Total:** 11 standard enemy icons. Zone 8 boss only.

---

## Boss

- **Name:** GalactoGobbler, Hoarder of Worlds
- **Arena:** Zone 8 — JUNK-WORLD FINALE
- **Health bar:** `GALACTOGOBBLER`
- **3 hits to defeat** (not illustrated)

---

## Footer — Boss callout (verbatim)

**Heading:** `LEVEL 5: GALACTOGOBBLER`

**Body:**
> Hoarder of Worlds — three-hit final boss. Uses suction, momentum, and low gravity. Final keeper of the glowing trash. Don't get inhaled!

---

## Legend

Row 1: TRASHY · ENEMIES (Armadillo, Hermit Crab, Rocket Roach, Vacuum Jelly) · TRASH TOKENS · TACO POWER-UP · KITE POWER-UP  
Row 2: SHORTCUT · CHALLENGE ROUTE · HAZARD (Cosmic sludge)

No breakables.

---

## Level assets (all 12 sprites placed)

`level5_space_cargo_pod`, `level5_salvage_signpost`, `level5_meteor_chunk`, `level5_satellite_debris_pile`, `level5_cosmic_crystal_cluster`, `level5_alien_trash_mound`, `level5_cargo_pallet`, `level5_floating_junk_anchor`, `level5_broken_bot_husk`, `level5_oxygen_canister`, `level5_low_g_scrap_barrel`, `level5_maintenance_crate`

---

## Approval

- [x] Follows Level 4 approved blueprint patterns
- [x] User directive: proceed with Level 5 deliverable
- [x] Blueprint generated
