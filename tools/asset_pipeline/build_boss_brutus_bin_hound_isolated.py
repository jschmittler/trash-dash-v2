#!/usr/bin/env python3
"""Losslessly isolate and repack every approved Brutus Bin Hound sprite.

The accepted Phase 04 atlas contains variable-width artwork whose rectangular
envelopes sometimes overlap.  This builder assigns every connected visible
alpha component to exactly one reviewed logical frame, copies those pixels at
1:1 scale, and packs independent manifest-defined rectangles with safe gutters.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/generated/boss-brutus-bin-hound-isolated"
FRAMES_OUT = OUTPUT / "frames"
SOURCE = (
    ROOT
    / "docs/design/trash-dash/character-animation/phase-05-codex-integration/phase-04-bosses/final/boss-brutus-bin-hound-transparent.png"
)
CANON = ROOT / "docs/design/trash-dash/reference/characters/level-02/sprites/boss-brutus-bin-hound.png"
DESKTOP_COPY = Path("/Users/jamesschmittler/Desktop/boss-brutus-bin-hound-transparent.png")
ATLAS_OUT = OUTPUT / "boss-brutus-bin-hound-isolated.png"
CONTACT_OUT = OUTPUT / "contact-sheet.png"
MANIFEST_OUT = OUTPUT / "manifest.json"
BATCH_OUT = OUTPUT / "batch-manifest.json"
AUDIT_OUT = OUTPUT / "source-audit.json"

SOURCE_SIZE = (1536, 1024)
SOURCE_PAD = 2
GUTTER = 8
MAX_ATLAS_WIDTH = 2048


def frames(prefix: str, count: int) -> list[str]:
    return [f"{prefix}-{index:02d}" for index in range(count)]


# Selection regions are reviewed ownership zones, not crop rectangles.  A
# connected component is assigned by its bounding-box center, then copied in
# full even if its envelope crosses a zone edge.  This preserves overlapping
# variable-width frames without contaminating either extraction.
ZONE_GROUPS = [
    ("reference-large", (0, 0, 300, 232), ["reference-large-00"]),
    ("idle", (300, 0, 1536, 114), frames("idle", 9)),
    ("bark-telegraph", (300, 114, 1536, 232), frames("bark-telegraph", 7)),
    ("walk-run", (0, 232, 1536, 329), frames("walk-run", 10)),
    ("roar", (0, 329, 515, 438), frames("roar", 4)),
    ("hit-reaction", (515, 329, 875, 438), frames("hit-reaction", 3)),
    ("crash-stunned", (875, 329, 1536, 438), frames("crash-stunned", 4)),
    ("recovery", (0, 438, 450, 536), frames("recovery", 4)),
    ("enraged", (450, 438, 1536, 536), frames("enraged", 6)),
    ("emerge", (0, 536, 510, 638), frames("emerge", 4)),
    ("turn-around", (510, 536, 910, 638), frames("turn-around", 4)),
    ("retreat", (910, 536, 1536, 638), frames("retreat", 5)),
    ("defeat", (0, 638, 900, 793), frames("defeat", 5)),
    ("idle-variants", (900, 638, 1225, 793), frames("idle-variant", 2)),
    ("dig", (1225, 638, 1435, 793), ["dig-00"]),
    ("reference-child", (1435, 638, 1536, 793), ["reference-child-00"]),
    ("rolling-can", (0, 793, 390, 899), frames("rolling-can", 4)),
    ("sprinkler-hydrant", (390, 793, 720, 899), frames("sprinkler-hydrant", 5)),
    ("water-splash", (720, 793, 990, 899), frames("water-splash", 3)),
    ("water-droplets", (990, 793, 1068, 899), ["water-droplets-00"]),
    ("impact-stars", (1068, 793, 1536, 899), ["impact-stars-00"]),
    ("dust-speed-puffs", (0, 899, 640, 1024), frames("dust-speed-puff", 9)),
    ("drip-strip", (640, 899, 900, 1024), ["drip-strip-00"]),
    ("misc-trash", (900, 899, 1170, 1024), frames("misc-trash", 6)),
    ("close-up-heads", (1170, 899, 1536, 1024), frames("close-up-head", 3)),
]


X_SPLITS = {
    "idle": [300, 438, 560, 690, 820, 956, 1084, 1209, 1330, 1536],
    "bark-telegraph": [300, 448, 640, 830, 1015, 1148, 1305, 1536],
    "walk-run": [0, 144, 275, 414, 544, 686, 848, 993, 1136, 1302, 1536],
    "roar": [0, 138, 258, 376, 515],
    "hit-reaction": [515, 618, 731, 875],
    "crash-stunned": [875, 1000, 1128, 1262, 1536],
    "recovery": [0, 130, 232, 330, 450],
    "enraged": [450, 629, 779, 907, 1072, 1253, 1536],
    "emerge": [0, 115, 235, 365, 510],
    "turn-around": [510, 625, 748, 827, 910],
    "retreat": [910, 1022, 1111, 1215, 1305, 1536],
    "defeat": [0, 180, 335, 520, 710, 900],
    "idle-variants": [900, 1060, 1225],
    "rolling-can": [0, 98, 175, 270, 390],
    "sprinkler-hydrant": [390, 451, 506, 552, 612, 720],
    "water-splash": [720, 803, 882, 990],
    "dust-speed-puffs": [0, 92, 163, 244, 345, 393, 447, 491, 550, 640],
    "misc-trash": [900, 960, 1005, 1043, 1075, 1112, 1170],
    "close-up-heads": [1170, 1294, 1410, 1536],
}


STATE_META = {
    "reference-large": (False, "reference-only"),
    "idle": (True, "ambient loop"),
    "bark-telegraph": (False, "warning tell to bark release"),
    "walk-run": (True, "ordered locomotion progression"),
    "roar": (False, "intimidation bark progression"),
    "hit-reaction": (False, "light to heavy reaction poses"),
    "crash-stunned": (False, "impact to dazed hold"),
    "recovery": (False, "stunned recovery to active"),
    "enraged": (True, "faster aggressive locomotion"),
    "emerge": (False, "closed shell to active state"),
    "turn-around": (False, "ordered facing transition"),
    "retreat": (False, "active state to intentional exit"),
    "defeat": (False, "collapse to pacified pool state"),
    "idle-variants": (True, "approved ambient variants"),
    "dig": (True, "approved dirt-kick action"),
    "reference-child": (False, "scale-reference-only"),
    "rolling-can": (False, "ordered projectile/damage progression"),
    "sprinkler-hydrant": (False, "ordered standalone hazard variants"),
    "water-splash": (False, "ordered standalone splash progression"),
    "water-droplets": (False, "standalone effect strip"),
    "impact-stars": (False, "standalone effect strip"),
    "dust-speed-puffs": (False, "standalone effect variants"),
    "drip-strip": (False, "standalone effect strip"),
    "misc-trash": (False, "standalone gameplay detail sprites"),
    "close-up-heads": (False, "reference-only expression sprites"),
}


ACTOR_STATES = {
    "idle",
    "bark-telegraph",
    "walk-run",
    "roar",
    "hit-reaction",
    "crash-stunned",
    "recovery",
    "enraged",
    "emerge",
    "turn-around",
    "retreat",
    "defeat",
    "idle-variants",
    "dig",
}


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def raw_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()


def visible_pixel_sha(image: Image.Image) -> str:
    digest = hashlib.sha256()
    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            if pixel[3]:
                digest.update(x.to_bytes(2, "big"))
                digest.update(y.to_bytes(2, "big"))
                digest.update(bytes(pixel))
    return digest.hexdigest()


def connected_components(image: Image.Image) -> list[dict]:
    width, height = image.size
    rgba = image.tobytes()
    visible = bytearray(1 if rgba[index + 3] else 0 for index in range(0, len(rgba), 4))
    visited = bytearray(width * height)
    components: list[dict] = []
    for start, is_visible in enumerate(visible):
        if not is_visible or visited[start]:
            continue
        stack = [start]
        visited[start] = 1
        pixels: list[int] = []
        min_x, min_y, max_x, max_y = width, height, 0, 0
        while stack:
            point = stack.pop()
            pixels.append(point)
            y, x = divmod(point, width)
            min_x, min_y = min(min_x, x), min(min_y, y)
            max_x, max_y = max(max_x, x), max(max_y, y)
            for neighbor_y in range(max(0, y - 1), min(height - 1, y + 1) + 1):
                row = neighbor_y * width
                for neighbor_x in range(max(0, x - 1), min(width - 1, x + 1) + 1):
                    neighbor = row + neighbor_x
                    if visible[neighbor] and not visited[neighbor]:
                        visited[neighbor] = 1
                        stack.append(neighbor)
        components.append(
            {
                "pixels": pixels,
                "bbox": (min_x, min_y, max_x + 1, max_y + 1),
                "center": ((min_x + max_x + 1) / 2, (min_y + max_y + 1) / 2),
            }
        )
    return components


def build_zones() -> tuple[list[dict], list[dict]]:
    zones: list[dict] = []
    states: list[dict] = []
    for state_id, region, frame_ids in ZONE_GROUPS:
        x0, y0, x1, y1 = region
        splits = X_SPLITS.get(state_id, [x0, x1])
        if len(splits) != len(frame_ids) + 1:
            raise RuntimeError(f"zone split count does not match frame count: {state_id}")
        for index, frame_id in enumerate(frame_ids):
            zones.append(
                {
                    "id": frame_id,
                    "state": state_id,
                    "stateFrameIndex": index,
                    "selectionRegion": [splits[index], y0, splits[index + 1], y1],
                }
            )
        loop, progression = STATE_META[state_id]
        states.append(
            {
                "id": state_id,
                "orderedFrames": frame_ids,
                "frameCount": len(frame_ids),
                "loop": loop,
                "progression": progression,
                "timing": {
                    "basis": "approved-source-order",
                    "durationMs": None,
                    "status": "not-promoted; runtime timing intentionally not invented",
                },
            }
        )
    return zones, states


def assign_components(components: list[dict], zones: list[dict]) -> dict[str, list[dict]]:
    assignments = {zone["id"]: [] for zone in zones}
    for component in components:
        center_x, center_y = component["center"]
        matches = []
        for zone in zones:
            left, top, right, bottom = zone["selectionRegion"]
            if left <= center_x < right and top <= center_y < bottom:
                matches.append(zone)
        if len(matches) != 1:
            raise RuntimeError(
                f"component at {component['bbox']} has {len(matches)} ownership matches"
            )
        assignments[matches[0]["id"]].append(component)
    empty = [frame_id for frame_id, owned in assignments.items() if not owned]
    if empty:
        raise RuntimeError(f"logical frames without visible components: {empty}")
    return assignments


def frame_anchor(state_id: str, components: list[dict], source_rect: tuple[int, int, int, int]) -> tuple[str, list[int]]:
    left, top, _right, _bottom = source_rect
    if state_id in ACTOR_STATES:
        largest = max(components, key=lambda component: len(component["pixels"]))
        x0, _y0, x1, y1 = largest["bbox"]
        return "body-ground-contact", [round((x0 + x1 - 1) / 2) - left, y1 - 1 - top]
    if state_id.startswith("reference") or state_id == "close-up-heads":
        union = union_bbox(components)
        return "reference-bottom-center", [round((union[0] + union[2] - 1) / 2) - left, union[3] - 1 - top]
    union = union_bbox(components)
    return "effect-bottom-center", [round((union[0] + union[2] - 1) / 2) - left, union[3] - 1 - top]


def union_bbox(components: list[dict]) -> tuple[int, int, int, int]:
    return (
        min(component["bbox"][0] for component in components),
        min(component["bbox"][1] for component in components),
        max(component["bbox"][2] for component in components),
        max(component["bbox"][3] for component in components),
    )


def pack_frames(frame_images: list[tuple[str, Image.Image]]) -> tuple[list[dict], tuple[int, int]]:
    placements: list[dict] = []
    x = 0
    y = 0
    row_height = 0
    for frame_id, image in frame_images:
        cell_width = image.width + GUTTER * 2
        cell_height = image.height + GUTTER * 2
        if x and x + cell_width > MAX_ATLAS_WIDTH:
            x = 0
            y += row_height
            row_height = 0
        placements.append(
            {
                "id": frame_id,
                "cellRect": [x, y, cell_width, cell_height],
                "artRect": [x + GUTTER, y + GUTTER, image.width, image.height],
            }
        )
        x += cell_width
        row_height = max(row_height, cell_height)
    return placements, (MAX_ATLAS_WIDTH, y + row_height)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    FRAMES_OUT.mkdir(parents=True, exist_ok=True)

    if not SOURCE.exists() or not CANON.exists() or not DESKTOP_COPY.exists():
        raise RuntimeError("required approved source input is missing")
    if file_sha(SOURCE) != file_sha(DESKTOP_COPY):
        raise RuntimeError("Desktop source and accepted Phase 04 atlas are not byte-identical")
    source = Image.open(SOURCE).convert("RGBA")
    canonical = Image.open(CANON)
    if source.size != SOURCE_SIZE or canonical.size != (1254, 1254):
        raise RuntimeError("approved source dimensions changed")
    if source.getchannel("A").getextrema() != (0, 255):
        raise RuntimeError("accepted source must contain both transparent and opaque pixels")
    alpha_bytes = source.getchannel("A").tobytes()
    alpha_values = set(alpha_bytes)
    if alpha_values != {0, 255}:
        raise RuntimeError("accepted source contains unexpected partial alpha")

    zones, states = build_zones()
    components = connected_components(source)
    assignments = assign_components(components, zones)
    frame_order = [frame_id for state in states for frame_id in state["orderedFrames"]]

    source_visible_count = sum(1 for alpha in alpha_bytes if alpha)
    assigned_visible_count = sum(
        len(component["pixels"])
        for frame_id in frame_order
        for component in assignments[frame_id]
    )
    if source_visible_count != assigned_visible_count:
        raise RuntimeError("visible source coverage is not exactly one-to-one")

    audit = {
        "boss": "Brutus Bin Hound",
        "canonId": "boss.level-02.brutus-bin-hound",
        "canonicalBoard": {
            "path": str(CANON.relative_to(ROOT)),
            "sha256": file_sha(CANON),
            "size": list(canonical.size),
            "mode": canonical.mode,
        },
        "acceptedTransparentAtlas": {
            "path": str(SOURCE.relative_to(ROOT)),
            "sha256": file_sha(SOURCE),
            "desktopCopySha256": file_sha(DESKTOP_COPY),
            "size": list(source.size),
            "mode": "RGBA",
            "visibleBounds": list(source.getchannel("A").getbbox()),
            "visiblePixelCount": source_visible_count,
            "opaquePixelCount": source_visible_count,
            "transparentPixelCount": source.width * source.height - source_visible_count,
            "partialAlphaPixelCount": 0,
            "connectedComponentCount": len(components),
        },
        "sequenceAudit": {
            "emerge": {"classification": "EXISTS - COMPLETE", "frameCount": 4},
            "retreat": {"classification": "EXISTS - COMPLETE", "frameCount": 5},
            "defeat": {"classification": "EXISTS - COMPLETE", "frameCount": 5},
        },
        "defects": {
            "crossFrameRectangularEnvelopeOverlap": True,
            "neighboringFrameBleedRisk": True,
            "visiblePixelsTouchingAcceptedAtlasBoundary": False,
            "ambiguousDetachedEffectOwnershipBeforeManifest": True,
            "insufficientTransparentGutters": True,
            "missingRequiredSequenceFrames": False,
        },
        "resolution": "ownership-mask extraction plus variable-cell repack; no artwork generation",
    }
    AUDIT_OUT.write_text(json.dumps(audit, indent=2) + "\n")

    # Contract stage: write the complete immutable batch inventory before any
    # individual frame or final atlas is produced.
    batch_manifest = {
        "boss": "Brutus Bin Hound",
        "execution": "EXECUTE: boss-brutus-bin-hound",
        "status": "immutable-pre-generation-manifest",
        "originalSheetDimensions": list(source.size),
        "outputFormat": "PNG RGBA, source scale 1, manifest-defined variable rectangles",
        "requiredGutterPixels": GUTTER,
        "operationCounts": {
            "PRESERVE EXACTLY": 0,
            "PRESERVE EXACTLY - REPOSITION FOR ISOLATION": len(frame_order),
            "GENERATE NEW": 0,
            "REPLACE UNAPPROVED": 0,
        },
        "sequences": states,
        "sourceRegions": [
            {
                "frame": zone["id"],
                "state": zone["state"],
                "stateFrameIndex": zone["stateFrameIndex"],
                "classification": "PRESERVE EXACTLY - REPOSITION FOR ISOLATION",
                "sourceOwnershipSelectionRegion": zone["selectionRegion"],
                "ownership": "all complete connected-alpha components whose bounding-box center is inside this reviewed region",
                "anchor": "preserve source-space body ground contact or declared effect/reference origin",
                "timing": "approved source order; runtime duration intentionally unset",
            }
            for zone in zones
        ],
    }
    BATCH_OUT.write_text(json.dumps(batch_manifest, indent=2) + "\n")

    for stale in FRAMES_OUT.glob("*.png"):
        stale.unlink()

    source_bytes = source.tobytes()
    zone_by_id = {zone["id"]: zone for zone in zones}
    images: dict[str, Image.Image] = {}
    records: dict[str, dict] = {}
    for frame_id in frame_order:
        owned = assignments[frame_id]
        visible_box = union_bbox(owned)
        source_rect = (
            max(0, visible_box[0] - SOURCE_PAD),
            max(0, visible_box[1] - SOURCE_PAD),
            min(source.width, visible_box[2] + SOURCE_PAD),
            min(source.height, visible_box[3] + SOURCE_PAD),
        )
        frame = Image.new(
            "RGBA",
            (source_rect[2] - source_rect[0], source_rect[3] - source_rect[1]),
            (0, 0, 0, 0),
        )
        frame_pixels = frame.load()
        for component in owned:
            for point in component["pixels"]:
                source_y, source_x = divmod(point, source.width)
                offset = point * 4
                pixel = tuple(source_bytes[offset : offset + 4])
                frame_pixels[source_x - source_rect[0], source_y - source_rect[1]] = pixel
        if frame.getchannel("A").getbbox() is None:
            raise RuntimeError(f"empty extracted frame: {frame_id}")
        bbox = frame.getchannel("A").getbbox()
        if bbox[0] == 0 or bbox[1] == 0 or bbox[2] == frame.width or bbox[3] == frame.height:
            raise RuntimeError(f"visible pixel touches extracted frame boundary: {frame_id}")
        destination = FRAMES_OUT / f"{frame_id}.png"
        frame.save(destination, format="PNG", compress_level=9, optimize=False)
        images[frame_id] = frame
        state_id = zone_by_id[frame_id]["state"]
        anchor_type, pivot = frame_anchor(state_id, owned, source_rect)
        records[frame_id] = {
            "state": state_id,
            "stateFrameIndex": zone_by_id[frame_id]["stateFrameIndex"],
            "classification": "PRESERVE EXACTLY - REPOSITION FOR ISOLATION",
            "sourceOwnershipSelectionRegion": zone_by_id[frame_id]["selectionRegion"],
            "sourceRect": [source_rect[0], source_rect[1], frame.width, frame.height],
            "sourceVisibleBounds": list(visible_box),
            "componentCount": len(owned),
            "frameFile": str(destination.relative_to(OUTPUT)),
            "frameSize": list(frame.size),
            "visibleBoundsInFrame": list(bbox),
            "pivotType": anchor_type,
            "pivotInFrame": pivot,
            "effectOwnership": (
                "integrated-with-emitter-frame"
                if state_id in ACTOR_STATES
                else "standalone-effect-or-reference-sprite"
            ),
            "timing": {
                "stateFrameIndex": zone_by_id[frame_id]["stateFrameIndex"],
                "durationMs": None,
                "status": "approved source order; runtime timing not promoted",
            },
            "frameRgbaSha256": raw_sha(frame),
            "visiblePixelSha256": visible_pixel_sha(frame),
            "visiblePixelCount": sum(len(component["pixels"]) for component in owned),
        }

    ordered_images = [(frame_id, images[frame_id]) for frame_id in frame_order]
    placements, atlas_size = pack_frames(ordered_images)
    atlas = Image.new("RGBA", atlas_size, (0, 0, 0, 0))
    for placement in placements:
        frame_id = placement["id"]
        art_x, art_y, _width, _height = placement["artRect"]
        # Direct paste preserves visible RGBA bytes. Transparent source RGB was
        # intentionally normalized during ownership-mask extraction.
        atlas.paste(images[frame_id], (art_x, art_y))
        records[frame_id]["cellRect"] = placement["cellRect"]
        records[frame_id]["artRect"] = placement["artRect"]
        records[frame_id]["pivotInCell"] = [
            GUTTER + records[frame_id]["pivotInFrame"][0],
            GUTTER + records[frame_id]["pivotInFrame"][1],
        ]
    atlas.save(ATLAS_OUT, format="PNG", compress_level=9, optimize=False)

    contact = Image.new("RGBA", atlas.size, (42, 45, 48, 255))
    checker = ImageDraw.Draw(contact)
    tile = 16
    for y in range(0, contact.height, tile):
        for x in range(0, contact.width, tile):
            if (x // tile + y // tile) % 2:
                checker.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(56, 60, 64, 255))
    contact.alpha_composite(atlas)
    draw = ImageDraw.Draw(contact)
    font = ImageFont.load_default()
    for index, placement in enumerate(placements):
        x, y, width, height = placement["cellRect"]
        draw.rectangle((x, y, x + width - 1, y + height - 1), outline=(255, 202, 40, 255))
        label = f"{index:03d} {placement['id']}"
        draw.text((x + 1, y), label, fill=(255, 255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0, 255))
    contact.save(CONTACT_OUT, format="PNG", compress_level=9, optimize=False)

    manifest = {
        "assetName": "boss-brutus-bin-hound-isolated",
        "canonId": "boss.level-02.brutus-bin-hound",
        "status": "artwork-approved",
        "approval": {
            "approvedBy": "project-owner",
            "approvedOn": "2026-08-13",
            "scope": "Level 2 Brutus Bin Hound isolated artwork package",
            "runtimePromotionAuthorized": False,
        },
        "canonicalFacing": "right",
        "approvedSource": str(SOURCE.relative_to(ROOT)),
        "approvedSourceSha256": file_sha(SOURCE),
        "canonicalVisualAuthority": str(CANON.relative_to(ROOT)),
        "canonicalVisualSha256": file_sha(CANON),
        "sheet": {
            "file": str(ATLAS_OUT.relative_to(ROOT)),
            "size": list(atlas.size),
            "mode": "RGBA",
            "background": "transparent",
            "layout": "manifest-defined-variable-rectangles",
            "gutterPixels": GUTTER,
            "readingOrder": "state order then ordered frame index",
        },
        "sourcePixelScale": 1,
        "outputPixelScale": 1,
        "states": states,
        "frames": records,
        "operationCounts": batch_manifest["operationCounts"],
        "coverage": {
            "sourceVisiblePixelCount": source_visible_count,
            "extractedVisiblePixelCount": sum(record["visiblePixelCount"] for record in records.values()),
            "visiblePixelsOmitted": 0,
            "visiblePixelsDuplicated": 0,
        },
        "provenance": {
            "method": "reviewed connected-alpha ownership masks plus lossless source-scale relocation",
            "aiGenerationUsed": False,
            "resizingUsed": False,
            "redrawingUsed": False,
            "filteringUsed": False,
            "rotationUsed": False,
            "runtimePromotionUsed": False,
            "rebuildCommand": "python3 tools/asset_pipeline/build_boss_brutus_bin_hound_isolated.py",
            "verifyCommand": "python3 tools/verify/check_boss_brutus_bin_hound_isolated.py",
        },
    }
    MANIFEST_OUT.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {len(records)} isolated approved frames/sprites")
    print(f"atlas: {ATLAS_OUT} ({atlas.width}x{atlas.height})")
    print(f"manifest: {MANIFEST_OUT}")


if __name__ == "__main__":
    main()
