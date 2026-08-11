# Engine decision

Status: **decision required before gameplay scaffold**

Decision owner: project owner

Recorded: 2026-08-11

## What is already decided

- V2 is an unrelated greenfield repository, not a fork or wholesale port.
- Approved design references remain engine-neutral source material.
- Runtime art is derived, validated, and separate from full-resolution references.
- Gameplay must support deterministic tests, independent collision geometry, semantic render layers, real-game visual audits, keyboard and touch input, responsive target resolutions, and web deployment unless targets change.
- No gameplay implementation starts until the runtime choice is accepted.

## Recommendation

Retain web delivery and use a dedicated 2D game framework rather than rebuilding V1's React-owned Canvas loop. A framework should own the game loop, input, camera, audio, texture/animation registration, and scene lifecycle; React, if used at all, should be limited to surrounding product UI. Phaser is the leading web candidate, while a thin custom Canvas runtime is acceptable only if minimizing dependencies outweighs the maintenance burden. Godot should be selected only if native desktop/mobile exports are a near-term requirement and web bundle/startup tradeoffs are acceptable.

## Decision questions

1. Are web browsers the only launch target for the first public release, or are native desktop/mobile builds required?
2. Must V2 embed inside a React site, or may the game own the page and expose a small integration boundary?
3. Is deterministic replay/recording a first-release requirement?
4. Which browsers and mobile devices define the minimum support matrix?
5. What are the authoritative logical resolution, supported aspect ratios, and orientation policy?
6. Is a tilemap editor workflow required, or will levels be validated data authored through repository tools?
7. Should physics remain purpose-built platformer collision, or is a general physics engine required?
8. Are accessibility remapping, controller support, and cloud saves first-release requirements?
9. Which hosting target replaces or consolidates the V1 GitHub Pages/OpenAI Sites/Cloudflare mix?

## Candidate acceptance test

Before committing to an engine, build a disposable spike outside production source that proves: fixed-step simulation; keyboard/touch action mapping; pixel-crisp scaling; aspect preservation; camera follow and boss lock; independent collision overlays; audio pause/mute/transition; one derived sprite animation; one data-defined surface and encounter; screenshot capture at target resolutions; headless unit tests; and a production web build. Delete the spike after recording results; do not promote spike gameplay into V2.
