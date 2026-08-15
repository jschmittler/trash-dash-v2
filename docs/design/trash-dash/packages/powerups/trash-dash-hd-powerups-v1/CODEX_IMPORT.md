# Codex Import Brief - Taco + Kite Power-Ups

Integrate the supplied Trash Dash HD Remake Taco and Kite power-up package into the existing game architecture.

Start by reading `manifest.json`. Treat the supplied runtime images as approved source art. Do not redraw, regenerate, recolor, squash, stretch, or otherwise reinterpret the Taco or Kite designs.

## 1. Inspect before changing code

First locate the existing asset loader, sprite/animation system, power-up state logic, pickup handling, UI overlay layer, and any existing texture-atlas or chroma-key preprocessing. Reuse the current architecture wherever possible rather than building a parallel system.

## 2. Power-up item sheet

Use `assets/powerups/taco-kite-powerups-clean-chroma.png` as the authoritative production source. It contains Taco on row 0 and Kite on row 1, with 11 approved states each. Use the exact state names and `xCuts` in `manifest.json` to create deterministic frame rectangles. Do not assume all 11 cells have equal width.

The green background is intentional. Convert only the connected chroma background to alpha. Do not globally remove every green pixel because the Taco ingredients, Kite panels, and effect debris contain approved green artwork. Preserve fine sparkles, glow falloff, rings, wind trails, leaves, and activation particles. Avoid green halos, clipped particles, edge erosion, or hard matte contours.

After preprocessing, persist the final frame rectangles in the project's normal asset metadata/config format so runtime code never has to infer them visually again.

The 11 item states are not one continuous loop. Use the manifest groups as the semantic starting point: ambient states, pickup states, active-power state, optional accent states, and recovery state. Integrate them with the existing power-up behavior rather than blindly looping all 11 frames.

## 3. Pickup overlay animations

Import:

- `assets/overlays/taco-power-overlay-clean-8frame.png`
- `assets/overlays/kite-power-overlay-clean-8frame.png`

Each is an exact 4-column by 2-row grid with 8 sequential frames. The manifest defines the frame size and semantic order. Trigger Taco's overlay when Taco Power is collected and Kite's overlay when Kite Power is collected.

Render the overlay above the gameplay/world layer as a short, high-impact pickup moment, then dismiss it cleanly and restore normal gameplay presentation. Preserve aspect ratio and do not non-uniformly scale any frame.

## 4. Asset organization

Keep the clean production images and generated metadata in the runtime asset path used by the project. Keep `reference/` out of the production bundle. Reference art is for visual comparison only.

## 5. Validation

Add or update checks that confirm:

- 11 Taco item states are available
- 11 Kite item states are available
- 8 Taco overlay frames are available
- 8 Kite overlay frames are available
- every frame rectangle is non-zero and remains inside its source image
- the power-up sprites preserve aspect ratio
- chroma removal leaves no obvious green fringe or missing approved green details
- particle effects are not clipped
- Taco and Kite overlays trigger from normal uninterrupted gameplay, not only isolated test fixtures

Visually verify both pickups in live gameplay at the game's normal target aspect ratio and at least one narrower responsive size.

## 6. Completion report

When finished, report:

- every file added or changed
- the final runtime asset paths
- where frame metadata lives
- how chroma-to-alpha was performed
- the animation timing used for item states and pickup overlays
- the exact trigger points for Taco and Kite pickup overlays
- what visual verification was completed
- any remaining limitations or follow-up work
