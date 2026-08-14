# Jimothy Powered - Approved Sprite Atlas

**Status:** Approved for Phase 01 main-character use.

**Canonical asset:** `atlases/jimothy-powered-approved.png`

**Dimensions:** `1254 x 1254` px, RGBA.

## What this atlas contains

Approved powered-up Jimothy atlas. Golden electrical energy is part of the approved visual language and must be preserved.

The atlas represents the approved clean character art for this state of the character. It replaces the earlier branded presentation sheet for runtime asset work.

## Codex rules

- Treat this approved atlas as visual truth.
- Do not substitute any earlier V1, V2, or V3 extraction output.
- Do not perform background removal, OCR, color-key transparency, or automatic content trimming.
- Do not stretch or squash the character art.
- Preserve detached effects, dust, stars, electrical arcs, kite/umbrella components, cords, and other pose-specific details.
- Preserve transparent pixels and alpha.
- Use a bottom-center pivot when creating runtime frame definitions unless the existing gameplay system requires a more specific pivot.
- If exact frame rectangles are created during integration, store those explicit rectangles in code or a runtime manifest. Do not rediscover them every launch.

## Gameplay animation vocabulary

The original design language includes: idle/stand, walk, run, jump start, midair/rise, fall, land, skid/stop, crouch, hurt/flinch, knockout/stunned, victory/celebrate, and glide/kite flight. Some approved atlases also contain action or support poses/effects. Use only poses that match the gameplay state being implemented.

## Acceptance criteria

A runtime implementation passes visual QA when the character matches this approved atlas, no part of the silhouette or effects is cropped, aspect ratio is unchanged, transparent regions remain transparent, and no presentation-sheet artifacts appear.
