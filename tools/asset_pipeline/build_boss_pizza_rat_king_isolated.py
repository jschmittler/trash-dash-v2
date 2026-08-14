#!/usr/bin/env python3
"""Losslessly isolate and repack the approved Pizza Rat King atlas.

The accepted Phase 04 atlas is a variable-canvas source whose logical sprite
envelopes lack reliable rectangular extraction gutters. This builder assigns
every visible source pixel exactly once, preserves RGBA values at source scale,
and creates manifest-defined variable rectangles plus composed EMERGE, RETREAT,
and DEFEAT sequence metadata from approved frames only.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/generated/boss-pizza-rat-king-isolated"
FRAMES_OUT = OUTPUT / "frames"
PREVIEWS_OUT = OUTPUT / "previews"
SOURCE = (
    ROOT
    / "docs/design/trash-dash/character-animation/phase-05-codex-integration/phase-04-bosses/final/boss-pizza-rat-king-transparent.png"
)
CANON = ROOT / "docs/design/trash-dash/reference/characters/level-03/sprites/boss-pizza-rat-king.png"
DESKTOP_COPY = Path("/Users/jamesschmittler/Desktop/boss-pizza-rat-king-transparent.png")
ATLAS_OUT = OUTPUT / "boss-pizza-rat-king-isolated.png"
CONTACT_OUT = OUTPUT / "contact-sheet.png"
MANIFEST_OUT = OUTPUT / "manifest.json"
BATCH_OUT = OUTPUT / "batch-manifest.json"
AUDIT_OUT = OUTPUT / "source-audit.json"
SPEC_OUT = OUTPUT / "immutable-generation-specification.md"

SOURCE_SIZE = (1717, 916)
CANON_SIZE = (1448, 1086)
SOURCE_PAD = 2
GUTTER = 8
MAX_ATLAS_WIDTH = 2048
MERGED_FAST_RUN_BBOX = (950, 353, 1345, 451)
MERGED_FAST_RUN_SEAM_X = 1160


def names(prefix: str, count: int) -> list[str]:
    return [f"{prefix}-{index:02d}" for index in range(count)]


# Rectangles are reviewed ownership zones, not crop rectangles. Normally a
# complete connected-alpha component is owned by the zone containing its
# bounding-box center. One accepted fast-run component visibly bridges two
# neighboring poses; that component alone is split at the reviewed transparent
# valley x=1160 so both bodies become independently extractable.
ZONE_GROUPS = [
    ("idle", (0, 0, 1717, 159), [0, 290, 500, 700, 900, 1110, 1317, 1717], names("idle", 7)),
    ("walk-heavy-movement", (0, 159, 1717, 286), [0, 245, 480, 735, 990, 1220, 1430, 1717], names("walk-heavy-movement", 7)),
    ("charge-startup", (0, 286, 950, 397), [0, 235, 430, 620, 950], names("charge-startup", 4)),
    ("pan-charge-fast-run", (0, 397, 950, 490), [0, 230, 480, 690, 950], names("pan-charge-fast-run", 4)),
    ("pan-charge-fast-run", (950, 286, 1717, 480), [950, 1160, 1350, 1717], names("pan-charge-fast-run", 7)[4:]),
    ("pizza-slice-throw", (0, 490, 950, 600), [0, 260, 450, 620, 710, 820, 950], names("pizza-slice-throw", 6)),
    ("charge-crash-stunned", (950, 480, 1717, 600), [950, 1155, 1360, 1717], names("charge-crash-stunned", 3)),
    ("enraged-faster-charge", (0, 600, 1717, 700), [0, 245, 460, 690, 950, 1278, 1717], names("enraged-faster-charge", 6)),
    ("hit-react", (0, 700, 1260, 825), [0, 210, 375, 570, 800, 1030, 1260], names("hit-react", 6)),
    ("defeat-reveal", (1260, 700, 1717, 830), [1260, 1380, 1490, 1717], names("defeat-reveal", 3)),
    ("rolling-cutter", (0, 825, 360, 880), [0, 75, 135, 212, 290, 360], names("rolling-cutter", 5)),
    ("dust-impact-effects", (360, 825, 1050, 880), [360, 520, 660, 820, 1050], names("dust-impact-effect", 4)),
    ("crown-details-upper", (1050, 825, 1717, 880), [1050, 1220, 1360, 1717], names("crown-detail-upper", 3)),
    ("pizza-props", (0, 880, 375, 916), [0, 130, 200, 260, 325, 375], names("pizza-prop", 5)),
    ("ground-effects", (375, 880, 1050, 916), [375, 435, 490, 555, 630, 710, 855, 1050], names("ground-effect", 7)),
    ("crown-details-lower", (1360, 880, 1717, 916), [1360, 1717], ["crown-detail-lower-00"]),
]


STATE_META = {
    "idle": (True, "approved heavy breathing/stand loop"),
    "walk-heavy-movement": (True, "approved ordered heavy locomotion"),
    "charge-startup": (False, "approved low-body charge anticipation"),
    "pan-charge-fast-run": (True, "approved ordered fast cutter charge"),
    "pizza-slice-throw": (False, "three emitter poses followed by three approved projectile poses"),
    "charge-crash-stunned": (False, "approved crash-to-stunned hold"),
    "enraged-faster-charge": (True, "approved faster charge progression"),
    "hit-react": (False, "approved ordered impact and recovery poses"),
    "defeat-reveal": (False, "approved post-collapse rat/crown reveal"),
    "rolling-cutter": (False, "standalone approved cutter rotations"),
    "dust-impact-effects": (False, "standalone approved dust/debris/impact envelopes"),
    "crown-details-upper": (False, "standalone approved crown reference sprites"),
    "pizza-props": (False, "standalone approved pizza variants"),
    "ground-effects": (False, "standalone approved ground-travel effects"),
    "crown-details-lower": (False, "standalone approved crown detail strip"),
}


ACTOR_STATES = {
    "idle",
    "walk-heavy-movement",
    "charge-startup",
    "pan-charge-fast-run",
    "pizza-slice-throw",
    "charge-crash-stunned",
    "enraged-faster-charge",
    "hit-react",
}


REQUIRED_SEQUENCES = {
    "emerge": {
        "classification": "EXISTS - COMPLETE",
        "orderedFrames": [
            "dust-impact-effect-00",
            "pan-charge-fast-run-06",
            "charge-startup-03",
            "charge-startup-00",
            "idle-00",
        ],
        "startState": "approved off-screen dust/entry cue",
        "intermediateMotion": "approved right-facing rush decelerates through charge startup poses",
        "endState": "idle-00 active boss state",
        "continuity": "dust cue to canonical right-facing movement to active idle",
        "loop": False,
    },
    "retreat": {
        "classification": "EXISTS - COMPLETE",
        "orderedFrames": [
            "idle-00",
            "charge-startup-00",
            "pan-charge-fast-run-00",
            "pan-charge-fast-run-06",
            "dust-impact-effect-00",
        ],
        "startState": "idle-00 active boss state",
        "intermediateMotion": "approved charge anticipation accelerates into intentional right-facing exit",
        "endState": "approved off-screen dust/exit cue",
        "continuity": "active idle to canonical charge vocabulary; no defeat pose",
        "loop": False,
    },
    "defeat": {
        "classification": "EXISTS - COMPLETE",
        "orderedFrames": [
            "hit-react-00",
            "hit-react-03",
            "charge-crash-stunned-00",
            "charge-crash-stunned-01",
            "charge-crash-stunned-02",
        ],
        "startState": "approved hit reaction",
        "intermediateMotion": "approved recoil and crash progression",
        "endState": "approved face-down defeated king, still visibly the exact boss",
        "continuity": "hit to crash/stunned collapse; the separate approved rat/crown reveal remains post-defeat support art",
        "loop": False,
    },
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
    image = image.convert("RGBA")
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
    state_frames: dict[str, list[str]] = {}
    state_order: list[str] = []
    for state_id, region, splits, frame_ids in ZONE_GROUPS:
        x0, y0, x1, y1 = region
        if splits[0] != x0 or splits[-1] != x1 or len(splits) != len(frame_ids) + 1:
            raise RuntimeError(f"invalid reviewed ownership geometry: {state_id}")
        if state_id not in state_frames:
            state_frames[state_id] = []
            state_order.append(state_id)
        offset = len(state_frames[state_id])
        for index, frame_id in enumerate(frame_ids):
            zones.append(
                {
                    "id": frame_id,
                    "state": state_id,
                    "stateFrameIndex": offset + index,
                    "selectionRegion": [splits[index], y0, splits[index + 1], y1],
                }
            )
            state_frames[state_id].append(frame_id)
    states = []
    for state_id in state_order:
        loop, progression = STATE_META[state_id]
        frame_ids = state_frames[state_id]
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
                    "status": "not promoted; runtime timing intentionally not invented",
                },
            }
        )
    return zones, states


def assign_pixels(components: list[dict], zones: list[dict], width: int) -> dict[str, list[int]]:
    assignments = {zone["id"]: [] for zone in zones}
    for component in components:
        if component["bbox"] == MERGED_FAST_RUN_BBOX:
            for point in component["pixels"]:
                _y, x = divmod(point, width)
                target = "pan-charge-fast-run-04" if x < MERGED_FAST_RUN_SEAM_X else "pan-charge-fast-run-05"
                assignments[target].append(point)
            continue
        center_x, center_y = component["center"]
        matches = []
        for zone in zones:
            left, top, right, bottom = zone["selectionRegion"]
            if left <= center_x < right and top <= center_y < bottom:
                matches.append(zone)
        if len(matches) != 1:
            raise RuntimeError(f"component at {component['bbox']} has {len(matches)} ownership matches")
        assignments[matches[0]["id"]].extend(component["pixels"])
    empty = [frame_id for frame_id, pixels in assignments.items() if not pixels]
    if empty:
        raise RuntimeError(f"logical frames without visible pixels: {empty}")
    return assignments


def pixels_bbox(pixels: list[int], width: int) -> tuple[int, int, int, int]:
    xs = []
    ys = []
    for point in pixels:
        y, x = divmod(point, width)
        xs.append(x)
        ys.append(y)
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def largest_component_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    components = connected_components(image)
    return max(components, key=lambda item: len(item["pixels"]))["bbox"]


def frame_anchor(state_id: str, frame: Image.Image) -> tuple[str, list[int]]:
    bbox = frame.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("cannot anchor empty frame")
    if state_id in ACTOR_STATES:
        body = largest_component_bbox(frame)
        return "body-ground-contact", [round((body[0] + body[2] - 1) / 2), body[3] - 1]
    return "effect-bottom-center", [round((bbox[0] + bbox[2] - 1) / 2), bbox[3] - 1]


def pack_frames(frame_images: list[tuple[str, Image.Image]]) -> tuple[list[dict], tuple[int, int]]:
    placements = []
    x = y = row_height = 0
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


def render_preview(name: str, frame_ids: list[str], images: dict[str, Image.Image], records: dict[str, dict]) -> None:
    left = max(records[frame_id]["pivotInFrame"][0] for frame_id in frame_ids) + 24
    right = max(images[frame_id].width - records[frame_id]["pivotInFrame"][0] for frame_id in frame_ids) + 24
    top = max(records[frame_id]["pivotInFrame"][1] for frame_id in frame_ids) + 24
    bottom = max(images[frame_id].height - records[frame_id]["pivotInFrame"][1] for frame_id in frame_ids) + 24
    canvas_size = (left + right, top + bottom)
    rendered = []
    for frame_id in frame_ids:
        canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
        pivot_x, pivot_y = records[frame_id]["pivotInFrame"]
        canvas.alpha_composite(images[frame_id], (left - pivot_x, top - pivot_y))
        rendered.append(canvas)
    rendered[0].save(
        PREVIEWS_OUT / f"{name}.gif",
        save_all=True,
        append_images=rendered[1:],
        duration=140,
        loop=0,
        disposal=2,
        transparency=0,
    )


def immutable_specification() -> str:
    return """# Pizza Rat King Immutable Generation Specification

Execution: `EXECUTE: boss-pizza-rat-king`  
Contract: `/Users/jamesschmittler/Desktop/bossfix.md`, reread in full immediately before execution  
Specification status: immutable for this execution batch

## Identity

- Boss: His Greasiness, the Pizza Rat King (`boss.level-03.pizza-rat-king`).
- Canonical visual authority: `docs/design/trash-dash/reference/characters/level-03/sprites/boss-pizza-rat-king.png`.
- Accepted transparent atlas: `docs/design/trash-dash/character-animation/phase-05-codex-integration/phase-04-bosses/final/boss-pizza-rat-king-transparent.png`.
- Locked: enormous obese low sewer-rat silhouette; greasy dark brown-gray/olive-black fur; dirty pale belly; pink segmented tail and paws; large pale-yellow eyes; irregular teeth; bent-fork crown; ragged red-brown mantle; huge dirty silver pizza cutter; canonical pizza, grease, dust, debris, wheel, speed-streak, impact-star, rat-reveal, and crown-detail effects.

## Animation

- EMERGE: 5 approved frame references; off-screen dust cue -> fast right-facing entry -> charge deceleration -> active idle.
- RETREAT: 5 approved frame references; active idle -> charge anticipation -> fast right-facing exit -> off-screen dust cue. It contains no defeated, injured, or unconscious pose.
- DEFEAT: 5 approved frame references; hit reaction -> crash/stunned collapse -> face-down defeated king. The approved rat/crown reveal remains a separate post-defeat state.
- Pose order inside every approved physical state remains unchanged. Required sequences reference isolated approved rectangles and do not duplicate their pixels in the sheet.
- Timing remains `UNSET / NOT PROMOTED`; runtime cadence is not invented before user approval.

## Rendering

- Three-quarter side profile, canonical facing screen-right.
- Source and output scale: exactly 1:1; no resize, rotation, redraw, retouch, filter, or resampling.
- Preserve approved light, shading, texture, palette, alpha, dimensions, internal registration, and ground contact.
- Output: transparent RGBA PNG, manifest-defined variable rectangles, 8 transparent atlas-gutter pixels on every side in addition to transparent extraction padding.
- Actor pivot: largest connected body component ground contact. Standalone effect pivot: visible-envelope bottom center.
- Detached components are assigned to one reviewed body/effect rectangle. The accepted fast-run bridge at source bbox `[950,353,1345,451]` is separated at reviewed source x=1160; every visible RGBA source pixel remains assigned exactly once.

## Restrictions and generation scope

- `GENERATE NEW = 0`; `REPLACE UNAPPROVED = 0`.
- Every physical sprite/support operation is `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`.
- No image generation is used because the approved atlas already supplies every pose/effect needed to compose EMERGE, RETREAT, and DEFEAT.
- No character features, props, damage, effects, palette, anatomy, style, or gameplay scale may change.
- No runtime promotion, runtime registration, collision, encounter, or gameplay edit is authorized.
"""


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    FRAMES_OUT.mkdir(parents=True, exist_ok=True)
    PREVIEWS_OUT.mkdir(parents=True, exist_ok=True)

    # Contract stages: the immutable specification and complete batch inventory
    # are written before any frame or final atlas is assembled.
    SPEC_OUT.write_text(immutable_specification())

    if not SOURCE.exists() or not CANON.exists() or not DESKTOP_COPY.exists():
        raise RuntimeError("required approved source input is missing")
    if file_sha(SOURCE) != file_sha(DESKTOP_COPY):
        raise RuntimeError("Desktop source and accepted Phase 04 atlas are not byte-identical")
    source = Image.open(SOURCE).convert("RGBA")
    canonical = Image.open(CANON)
    if source.size != SOURCE_SIZE or canonical.size != CANON_SIZE:
        raise RuntimeError("approved source dimensions changed")
    if set(source.getchannel("A").tobytes()) != {0, 255}:
        raise RuntimeError("accepted source must contain hard transparent and opaque alpha only")

    zones, states = build_zones()
    components = connected_components(source)
    assignments = assign_pixels(components, zones, source.width)
    frame_order = [frame_id for state in states for frame_id in state["orderedFrames"]]
    source_visible_count = sum(1 for alpha in source.getchannel("A").tobytes() if alpha)
    assigned_visible_count = sum(len(assignments[frame_id]) for frame_id in frame_order)
    if source_visible_count != assigned_visible_count:
        raise RuntimeError("visible source coverage is not exactly one-to-one")
    all_assigned = [point for frame_id in frame_order for point in assignments[frame_id]]
    if len(all_assigned) != len(set(all_assigned)):
        raise RuntimeError("a visible source pixel was assigned more than once")

    audit = {
        "boss": "His Greasiness, the Pizza Rat King",
        "canonId": "boss.level-03.pizza-rat-king",
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
        "sequenceAudit": REQUIRED_SEQUENCES,
        "defects": {
            "missingOrIncompleteAnimations": False,
            "crossFrameRectangularEnvelopeOverlap": True,
            "neighboringFrameBleedRisk": True,
            "visiblePixelsTouchingAcceptedAtlasBoundary": False,
            "ambiguousDetachedEffectOwnershipBeforeManifest": True,
            "insufficientTransparentGutters": True,
            "missingEmergeFrames": False,
            "missingRetreatFrames": False,
            "missingDefeatFrames": False,
        },
        "resolution": "approved-frame sequence composition plus reviewed ownership-mask extraction and variable-cell repack; no artwork generation",
    }
    AUDIT_OUT.write_text(json.dumps(audit, indent=2) + "\n")

    batch_manifest = {
        "boss": "His Greasiness, the Pizza Rat King",
        "execution": "EXECUTE: boss-pizza-rat-king",
        "status": "immutable-pre-assembly-manifest",
        "originalSheetDimensions": list(source.size),
        "updatedSheetDimensions": "computed deterministically from explicit frame rectangles before atlas write",
        "outputFormat": "PNG RGBA, source scale 1, manifest-defined variable rectangles",
        "requiredGutterPixels": GUTTER,
        "operationCounts": {
            "PRESERVE EXACTLY": 0,
            "PRESERVE EXACTLY - REPOSITION FOR ISOLATION": len(frame_order),
            "GENERATE NEW": 0,
            "REPLACE UNAPPROVED": 0,
        },
        "requiredSequences": REQUIRED_SEQUENCES,
        "physicalStates": states,
        "sourceRegions": [
            {
                "frame": zone["id"],
                "state": zone["state"],
                "stateFrameIndex": zone["stateFrameIndex"],
                "classification": "PRESERVE EXACTLY - REPOSITION FOR ISOLATION",
                "sourceOwnershipSelectionRegion": zone["selectionRegion"],
                "ownership": (
                    "reviewed pixel split at x=1160 for accepted merged fast-run bridge"
                    if zone["id"] in {"pan-charge-fast-run-04", "pan-charge-fast-run-05"}
                    else "all complete connected-alpha components whose bounding-box center is inside this reviewed region"
                ),
                "anchor": "preserve source-scale body ground contact or declared effect origin",
                "timing": "approved source order; runtime duration intentionally unset",
            }
            for zone in zones
        ],
    }
    BATCH_OUT.write_text(json.dumps(batch_manifest, indent=2) + "\n")

    for folder in (FRAMES_OUT, PREVIEWS_OUT):
        for stale in folder.glob("*"):
            if stale.is_file():
                stale.unlink()

    source_bytes = source.tobytes()
    zone_by_id = {zone["id"]: zone for zone in zones}
    images: dict[str, Image.Image] = {}
    records: dict[str, dict] = {}
    for frame_id in frame_order:
        owned = assignments[frame_id]
        visible_box = pixels_bbox(owned, source.width)
        source_rect = (
            max(0, visible_box[0] - SOURCE_PAD),
            max(0, visible_box[1] - SOURCE_PAD),
            min(source.width, visible_box[2] + SOURCE_PAD),
            min(source.height, visible_box[3] + SOURCE_PAD),
        )
        frame = Image.new("RGBA", (source_rect[2] - source_rect[0], source_rect[3] - source_rect[1]), (0, 0, 0, 0))
        frame_pixels = frame.load()
        for point in owned:
            source_y, source_x = divmod(point, source.width)
            offset = point * 4
            frame_pixels[source_x - source_rect[0], source_y - source_rect[1]] = tuple(source_bytes[offset : offset + 4])
        bbox = frame.getchannel("A").getbbox()
        if bbox is None or bbox[0] == 0 or bbox[1] == 0 or bbox[2] == frame.width or bbox[3] == frame.height:
            raise RuntimeError(f"visible pixel touches extracted frame boundary: {frame_id}")
        destination = FRAMES_OUT / f"{frame_id}.png"
        frame.save(destination, format="PNG", compress_level=9, optimize=False)
        images[frame_id] = frame
        state_id = zone_by_id[frame_id]["state"]
        anchor_type, pivot = frame_anchor(state_id, frame)
        records[frame_id] = {
            "state": state_id,
            "stateFrameIndex": zone_by_id[frame_id]["stateFrameIndex"],
            "classification": "PRESERVE EXACTLY - REPOSITION FOR ISOLATION",
            "sourceOwnershipSelectionRegion": zone_by_id[frame_id]["selectionRegion"],
            "sourceRect": [source_rect[0], source_rect[1], frame.width, frame.height],
            "sourceVisibleBounds": list(visible_box),
            "frameFile": str(destination.relative_to(OUTPUT)),
            "frameSize": list(frame.size),
            "visibleBoundsInFrame": list(bbox),
            "pivotType": anchor_type,
            "pivotInFrame": pivot,
            "effectOwnership": "integrated-with-emitter-frame" if state_id in ACTOR_STATES else "standalone-effect-or-reference-sprite",
            "timing": {
                "stateFrameIndex": zone_by_id[frame_id]["stateFrameIndex"],
                "durationMs": None,
                "status": "approved source order; runtime timing not promoted",
            },
            "frameRgbaSha256": raw_sha(frame),
            "visiblePixelSha256": visible_pixel_sha(frame),
            "visiblePixelCount": len(owned),
        }

    ordered_images = [(frame_id, images[frame_id]) for frame_id in frame_order]
    placements, atlas_size = pack_frames(ordered_images)
    atlas = Image.new("RGBA", atlas_size, (0, 0, 0, 0))
    for placement in placements:
        frame_id = placement["id"]
        art_x, art_y, _width, _height = placement["artRect"]
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
        draw.text((x + 1, y), f"{index:03d} {placement['id']}", fill=(255, 255, 255, 255), font=font, stroke_width=1, stroke_fill=(0, 0, 0, 255))
    contact.save(CONTACT_OUT, format="PNG", compress_level=9, optimize=False)

    for sequence_name, sequence in REQUIRED_SEQUENCES.items():
        render_preview(sequence_name, sequence["orderedFrames"], images, records)

    manifest = {
        "assetName": "boss-pizza-rat-king-isolated",
        "canonId": "boss.level-03.pizza-rat-king",
        "status": "artwork-approved",
        "approval": {
            "approvedBy": "project-owner",
            "approvedOn": "2026-08-13",
            "scope": "Level 3 Pizza Rat King isolated artwork package",
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
            "readingOrder": "physical state order then approved frame index",
        },
        "sourcePixelScale": 1,
        "outputPixelScale": 1,
        "states": states,
        "requiredSequences": REQUIRED_SEQUENCES,
        "frames": records,
        "operationCounts": batch_manifest["operationCounts"],
        "coverage": {
            "sourceVisiblePixelCount": source_visible_count,
            "extractedVisiblePixelCount": sum(record["visiblePixelCount"] for record in records.values()),
            "visiblePixelsOmitted": 0,
            "visiblePixelsDuplicated": 0,
        },
        "provenance": {
            "method": "reviewed connected-alpha ownership masks with one reviewed overlap seam, plus lossless source-scale relocation",
            "aiGenerationUsed": False,
            "resizingUsed": False,
            "redrawingUsed": False,
            "filteringUsed": False,
            "rotationUsed": False,
            "runtimePromotionUsed": False,
            "rebuildCommand": "python3 tools/asset_pipeline/build_boss_pizza_rat_king_isolated.py",
            "verifyCommand": "python3 tools/verify/check_boss_pizza_rat_king_isolated.py",
        },
    }
    MANIFEST_OUT.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {len(records)} isolated approved frames/support sprites")
    print(f"atlas {atlas.width}x{atlas.height}; visible pixels {source_visible_count} assigned exactly once")


if __name__ == "__main__":
    main()
