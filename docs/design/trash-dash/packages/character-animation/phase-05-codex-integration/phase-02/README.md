# Trash Dash Phase 02 Enemy Animation Source Sheets

This package contains the ten approved standard enemies for Levels 1 and 2, rebuilt as clean transparent animation source sheets.

## Level 1

- Mosquito
- Opossum Pilfer
- Pigeon
- Snake
- Spider

## Level 2

- Bee
- Dog
- Moth Dustwing
- Skunk
- Squirrel

## Output contract

Each `final/*-transparent.png` file is a 1536 x 1024 RGBA source sheet. Presentation labels and dark backgrounds were removed. Approved pose order, attack sequences, projectiles, props, hit reactions, defeat poses, motion extremes, and character-specific effects were retained.

These are reference-complete animation source sheets, not fixed-cell runtime atlases. Runtime cell size, anchors, hitboxes, frame durations, loop behavior, release/contact timing, and direction flipping should be defined during game integration.

## QA

- All ten files have real alpha transparency.
- All ten canvases have fully transparent outer edges, so no sprite or effect is clipped by the canvas boundary.
- Level 1, Level 2, and combined contact sheets are included in `qa/` for visual review.
- The approved source sheets remain in `source-pack/` and the chroma intermediates remain in `generated/` for provenance and targeted regeneration.
