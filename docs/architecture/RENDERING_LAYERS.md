# Rendering layers

V2 uses centralized semantic layers. Numeric engine depths are assigned in one adapter only; gameplay data names layers symbolically.

| Back-to-front order | Layer | Owns |
|---:|---|---|
| 1 | `FAR_BACKGROUND` | Opaque distant sky and far parallax plane |
| 2 | `BACKGROUND_SCENERY` | Whole background landmarks and middle parallax plane |
| 3 | `REAR_ENVIRONMENT` | Scenery behind traversal and actors |
| 4 | `TERRAIN` | Ground, platforms, structural collision silhouettes |
| 5 | `GROUND_DECOR` | Grounded nonblocking props and decals |
| 6 | `GAMEPLAY` | Player, enemies, bosses, pickups, interactive fixtures |
| 7 | `GAMEPLAY_EFFECTS` | Projectiles, attacks, particles, readable gameplay effects |
| 8 | `FOREGROUND` | Intentional framing that never hides required traversal information |
| 9 | `HUD` | Screen-space HUD, menus, announcements, and debug overlays when enabled |

Rules: z-order cannot conceal impossible geometry; every object has one owning layer; landmarks may not be split across parallax planes; collision is independent of rendering; foreground occlusion must preserve threats, landing targets, pickups, and UI; debug layers are development-only.
