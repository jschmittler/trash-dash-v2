# Brutus Bin Hound — Immutable Generation Specification

Status: frozen for `EXECUTE: boss-brutus-bin-hound` on 2026-08-13  
Delivery state: `ARTWORK APPROVED` by the project owner on 2026-08-13  
Runtime promotion: forbidden for this batch

## Authority and identity

- Contract: `/Users/jamesschmittler/Desktop/bossfix.md` (875 lines, reread in full before execution).
- Canonical visual authority: `docs/design/trash-dash/reference/characters/level-02/sprites/boss-brutus-bin-hound.png`, SHA-256 `ddf2eb77ad8f16aa164a934b08ea6b64c0679c24bf9c3a92a4fa444813c25c1c`, 1254×1254 RGB.
- Accepted transparent source atlas: `docs/design/trash-dash/character-animation/phase-05-codex-integration/phase-04-bosses/final/boss-brutus-bin-hound-transparent.png`, SHA-256 `2fb68f090e668dc662dbf5d92a08f15699a0f4afc8f5d864da82d27927da1cf1c`, 1536×1024 RGBA.
- The accepted transparent atlas is byte-identical to `/Users/jamesschmittler/Desktop/boss-brutus-bin-hound-transparent.png`.
- Locked identity: oversized stocky tan-orange English bulldog; enormous square wrinkled head; folded rose ears; narrow dark eyes; black nose; cream muzzle/chest/toes; drooping jowls; underbite; red-orange studded collar; inverted scratched ribbed dark blue-gray galvanized wheeled-bin armor; two black spiral-hub wheels on top; four short legs; right-facing side profile; approved materials, palette, expressions, and effects language.

## Audit classification

- EMERGE: `EXISTS - COMPLETE`, 4 approved frames. Closed shell → partial reveal → fuller reveal → active right-facing state.
- RETREAT: `EXISTS - COMPLETE`, 5 approved frames. Active state → progressive intentional withdrawal/exit → departing/dust end state.
- DEFEAT: `EXISTS - COMPLETE`, 5 approved frames. Collapse → dizzy reaction → splash-down transition → soaked state → pacified kiddie-pool end state.
- Missing required frames: none.
- Approved but unapproved/invalid artwork: none.
- Cross-frame layout defects: present in the accepted atlas because several variable-width bodies and detached particles occupy overlapping rectangular envelopes or have insufficient extraction gutters. The artwork itself remains approved.

## Immutable operation decision

- Every delivered frame/sprite operation is `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`.
- `GENERATE NEW`: 0.
- `REPLACE UNAPPROVED`: 0.
- AI generation, redraw, retouch, cleanup, filtering, rotation, scaling, resampling, and visible-pixel alteration are forbidden.
- Connected alpha components are assigned exactly once to a manifest-declared logical frame/effect. This ownership-mask extraction resolves overlapping rectangular envelopes without changing any visible source RGBA pixel.
- Every source visible-alpha pixel must appear in exactly one extracted output. No source visible-alpha pixel may be omitted or duplicated.

## Rendering and geometry

- Perspective, lighting, shading, texture, style, palette, facing, pose order, sprite scale, and artwork dimensions remain exactly as accepted.
- Source pixel scale and output pixel scale are 1:1.
- Output canvas uses true RGBA transparency and manifest-defined variable rectangles; it is not a fixed-cell runtime atlas.
- Each extracted frame contains its full assigned visible envelope plus two transparent pixels inside the frame image where source bounds permit.
- Each packed frame image receives an additional eight-pixel fully transparent atlas gutter on all four sides.
- Character pivots use the bottom-center of the largest assigned body component, retaining the accepted source ground contact after relocation. Effect/reference pivots use a declared bottom-center, logical-center, or emitter origin appropriate to ownership.
- Individual frame order follows the accepted atlas row order and the canonical board's named state order.
- Runtime FPS/durations are not invented in this source-only batch. Timing is recorded as ordered source-board progression with runtime duration `null` and status `not-promoted`.

## Effect ownership

- Bark lines, dust, speed streaks, stun stars, water droplets, dirt, and other detached components spatially associated with one actor frame remain integrated with and owned by that frame.
- Hydrants, sprinkler sprays, water splashes, impact-star strip, dust/puff sprites, drip strip, rolling-can projectiles, trash details, and close-up heads are separately declared support/effect sprites with independent rectangles and anchors.
- The DEFEAT splash-down frame is an approved effect-only transition owned by the DEFEAT sequence.

## Restrictions

- No approved source pose, expression, anatomy, silhouette, material, equipment, effect, or sequence assignment may change.
- No visible pixels may touch an extracted-frame boundary, packed cell boundary, or neighboring cell.
- No output may enter `assets/runtime/` or be registered in the game.
- The batch remains unapproved until the project owner explicitly approves it.
