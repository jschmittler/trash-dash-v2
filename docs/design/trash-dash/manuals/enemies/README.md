# Trash Dash HD Remake - Enemy Canon

**Status:** APPROVED / LOCKED CANON  
**Current canon version:** v1.5  
**Coverage:** Level 1 through Secret Level 6

This directory is the authoritative repository-native reference for all approved Trash Dash HD Remake enemies.

Before creating, editing, animating, placing, balancing, implementing, reviewing, or debugging an enemy, read:

1. `ENEMY_MASTER_CONTRACT.md`
2. The relevant `LEVEL_XX.md` file
3. The matching entry in `ASSET_MANIFEST.md`
4. The canonical concept art in `reference-art/`

Existing runtime implementation does not override approved canon.

## Roster index

| Level | Canonical enemy | Placement class | Gameplay archetype | Detailed spec |
|---|---|---|---|---|
| 1 | Mosquito | Flying | Airborne harasser / dash striker | [LEVEL_01.md](LEVEL_01.md#l1-e01-mosquito) |
| 1 | Pilfer the Opossum | Ground | Pursuer / scavenger | [LEVEL_01.md](LEVEL_01.md#l1-e02-pilfer-the-opossum) |
| 1 | Pigeon | Ground | Charger / bruiser | [LEVEL_01.md](LEVEL_01.md#l1-e03-pigeon) |
| 1 | Snake | Ground / low-profile | Ambusher / ranged controller | [LEVEL_01.md](LEVEL_01.md#l1-e04-snake) |
| 1 | Spider | Ground + web-based entry | Controller / trapper | [LEVEL_01.md](LEVEL_01.md#l1-e05-spider) |
| 2 | Dog | Ground | Reactive chaser / close-range aggressor | [LEVEL_02.md](LEVEL_02.md#l2-e01-dog) |
| 2 | Dustwing | Flying | Aerial controller / lantern attacker | [LEVEL_02.md](LEVEL_02.md#l2-e02-moth--dustwing) |
| 2 | Skunk | Ground | Area-control enemy | [LEVEL_02.md](LEVEL_02.md#l2-e03-skunk) |
| 2 | Squirel | Ground | Ranged projectile defender | [LEVEL_02.md](LEVEL_02.md#l2-e04-squirel) |
| 2 | Bee | Flying | Venom dash attacker | [LEVEL_02.md](LEVEL_02.md#l2-e05-bee) |
| 3 | Alley Cat Burglar | Ground | Pounce predator / ambusher | [LEVEL_03.md](LEVEL_03.md#l3-e01-alley-cat-burglar) |
| 3 | Sewer Rat Courier | Ground | Mobile charger / hazard dropper | [LEVEL_03.md](LEVEL_03.md#l3-e02-sewer-rat-courier) |
| 3 | Subway Roach | Ground / concealed | Ambush sprinter | [LEVEL_03.md](LEVEL_03.md#l3-e03-subway-roach) |
| 3 | Traffic-Cone Crab | Ground / armored | Shell defender / projectile attacker | [LEVEL_03.md](LEVEL_03.md#l3-e04-traffic-cone-crab) |
| 3 | His Greasiness, the Pizza Rat King | Ground boss | Heavy charger / ranged boss | [LEVEL_03.md](LEVEL_03.md#l3-b01-his-greasiness-the-pizza-rat-king) |
| 4 | Beaker Slime | Ground / bouncing | Transforming mobility enemy | [LEVEL_04.md](LEVEL_04.md#l4-e01-beaker-slime) |
| 4 | Clipboard Hamster | Machine-bound / exposed ground | Environmental operator | [LEVEL_04.md](LEVEL_04.md#l4-e02-clipboard-hamster) |
| 4 | Mop-Bot 3000 | Ground / mobile machine | Suction hazard / pursuer | [LEVEL_04.md](LEVEL_04.md#l4-e03-mop-bot-3000) |
| 4 | Phase Gecko | Ground + wall-clinging | Camouflaged ambusher | [LEVEL_04.md](LEVEL_04.md#l4-e04-phase-gecko) |
| 5 | Asteroid Armadillo | Ground + ballistic low-gravity movement | Rolling ricochet enemy | [LEVEL_05.md](LEVEL_05.md#l5-e01-asteroid-armadillo) |
| 5 | Rocket Roach | Ground + rocket-assisted horizontal burst | Burst-movement enemy | [LEVEL_05.md](LEVEL_05.md#l5-e02-rocket-roach) |
| 5 | Satellite Hermit Crab | Ground | Shielded transmitter / patroller | [LEVEL_05.md](LEVEL_05.md#l5-e03-satellite-hermit-crab) |
| 5 | Vacuum Jelly | Floating / aerial | Position-control flyer | [LEVEL_05.md](LEVEL_05.md#l5-e04-vacuum-jelly) |
| Secret 6 | Baserunning Beaver | Ground | Speedy slider / charge enemy | [LEVEL_06.md](LEVEL_06.md#sl6-e01-baserunning-beaver) |
| Secret 6 | Clobbering Cub | Ground | Heavy melee hitter | [LEVEL_06.md](LEVEL_06.md#sl6-e02-clobbering-cub) |
| Secret 6 | Sliding Seagull | Flying + ground skim | Dive-bomber | [LEVEL_06.md](LEVEL_06.md#sl6-e03-sliding-seagull) |
| Secret 6 | Windup Weasel | Ground | Ranged pitcher | [LEVEL_06.md](LEVEL_06.md#sl6-e04-windup-weasel) |

## Canon versions

- v1.0 - Level 1 approved
- v1.1 - Level 2 approved
- v1.2 - Level 3 approved
- v1.3 - Level 4 approved
- v1.4 - Level 5 approved
- v1.5 - Secret Level 6: Abandoned Ballpark approved

## Important identity notes

- The standard Level 2 Dog is not automatically Brutus. If Brutus exists elsewhere as a boss, keep the identities separate unless a later approved canon update says otherwise.
- Dustwing is the canonical identity for the Level 2 moth.
- `Squirel` is the canonical project spelling currently used in this canon package.
- Only enemies explicitly approved in these files are part of this enemy-canon import. Do not invent missing bosses or silently merge unrelated characters into these entries.

## Canon vs implementation

When implementation differs from this documentation, classify the difference before changing anything:

- `IMPLEMENTATION BUG`
- `MISSING IMPLEMENTATION`
- `CANON-COMPLIANT VARIATION`
- `POSSIBLE CANON CONFLICT`

Do not modify locked canon merely to justify the current implementation.
