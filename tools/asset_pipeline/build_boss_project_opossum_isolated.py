#!/usr/bin/env python3
"""Losslessly isolate and repack the approved Project O.P.O.S.S.U.M. atlas.

Every nontransparent source pixel is assigned exactly once to a reviewed
logical frame or support sprite. Approved pixels remain at source scale and
are only relocated into manifest-defined variable rectangles with transparent
gutters. EMERGE, RETREAT, and DEFEAT use approved art only.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "docs/design/trash-dash/manuals/bosses/BOSSFIX.md"
OUTPUT = ROOT / "assets/generated/boss-project-opossum-isolated"
FRAMES_OUT = OUTPUT / "frames"
PREVIEWS_OUT = OUTPUT / "previews"
SOURCE = (
    ROOT
    / "docs/design/trash-dash/library/characters/bosses/project-opossum/sprites/animation-source/boss-project-opossum-transparent.png"
)
CANON = ROOT / "docs/design/trash-dash/library/characters/bosses/project-opossum/sprites/reference/boss-project-opossum.png"
DESKTOP_COPY = Path("/Users/jamesschmittler/Desktop/boss-project-opossum-transparent.png")
ATLAS_OUT = OUTPUT / "boss-project-opossum-isolated.png"
CONTACT_OUT = OUTPUT / "contact-sheet.png"
MANIFEST_OUT = OUTPUT / "manifest.json"
BATCH_OUT = OUTPUT / "batch-manifest.json"
AUDIT_OUT = OUTPUT / "source-audit.json"
SPEC_OUT = OUTPUT / "immutable-generation-specification.md"

SOURCE_SIZE = (1536, 1024)
CANON_SIZE = (1448, 1086)
SOURCE_PAD = 2
GUTTER = 8
MAX_ATLAS_WIDTH = 2048


def names(prefix: str, count: int) -> list[str]:
    return [f"{prefix}-{index:02d}" for index in range(count)]


# These reviewed selection regions partition every visible source component.
# They are ownership zones, not output crop rectangles. Detached sparks,
# debris, portals, warning marks, and smoke belong to the zone containing the
# center of their complete connected-alpha component.
ZONE_GROUPS = [
    ("idle-stand", (0, 0, 1536, 89), [0, 230, 420, 610, 800, 1000, 1200, 1536], names("idle-stand", 7)),
    ("walk-heavy-movement", (0, 89, 1536, 171), [0, 185, 390, 590, 790, 980, 1150, 1330, 1536], names("walk-heavy-movement", 8)),
    ("charge-test-startup", (0, 171, 1536, 244), [0, 195, 375, 525, 670, 835, 985, 1170, 1340, 1536], names("charge-test-startup", 9)),
    ("fast-charge", (0, 244, 1536, 311), [0, 215, 395, 575, 760, 930, 1090, 1265, 1536], names("fast-charge", 8)),
    ("crash-into-barrier", (0, 311, 1536, 392), [0, 220, 410, 600, 780, 950, 1140, 1335, 1536], names("crash-into-barrier", 8)),
    ("stunned-after-crash", (0, 392, 1536, 461), [0, 210, 395, 595, 800, 990, 1175, 1536], names("stunned-after-crash", 7)),
    ("phase-shift-fake-charge", (0, 461, 1536, 528), [0, 190, 345, 475, 625, 775, 900, 1015, 1125, 1240, 1536], names("phase-shift-fake-charge", 10)),
    ("suction-pulse-attack", (0, 528, 1536, 606), [0, 210, 440, 655, 870, 1220, 1536], names("suction-pulse-attack", 6)),
    ("enraged-rapid-alternating-charges", (0, 606, 1536, 671), [0, 220, 415, 705, 765, 950, 1140, 1340, 1536], names("enraged-rapid-alternating-charges", 8)),
    ("hit-react", (0, 671, 1536, 735), [0, 220, 405, 620, 800, 960, 1140, 1536], names("hit-react", 7)),
    ("containment-alarm-state", (0, 735, 1536, 814), [0, 220, 395, 610, 780, 960, 1160, 1536], names("containment-alarm-state", 7)),
    ("final-reveal-playing-possum", (0, 814, 1536, 895), [0, 180, 375, 535, 710, 850, 1005, 1170, 1360, 1536], names("final-reveal-playing-possum", 9)),
    ("props-rig-core", (0, 895, 115, 1024), [0, 115], ["prop-rig-core-00"]),
    ("props-harness-upper", (115, 895, 600, 955), [115, 195, 230, 280, 320, 380, 430, 485, 535, 600], names("prop-harness-upper", 9)),
    ("props-harness-lower", (115, 955, 600, 1024), [115, 200, 265, 300, 335, 375, 420, 475, 520, 550, 600], names("prop-harness-lower", 10)),
    ("effects-library-upper", (600, 895, 1536, 978), [600, 760, 815, 940, 1040, 1135, 1220, 1295, 1340, 1405, 1470, 1536], names("effect-library-upper", 11)),
    ("effects-library-lower", (600, 978, 1536, 1024), [600, 700, 760, 815, 850, 885, 925, 970, 1020, 1060, 1100, 1160, 1200, 1240, 1280, 1325, 1350, 1390, 1420, 1450, 1536], names("effect-library-lower", 20)),
]


STATE_META = {
    "idle-stand": (True, "approved wary idle and asynchronous harness activity"),
    "walk-heavy-movement": (True, "approved ordered heavy quadrupedal scuttle"),
    "charge-test-startup": (False, "approved charge anticipation progression"),
    "fast-charge": (True, "approved low right-facing sprint with dust and speed streaks"),
    "crash-into-barrier": (False, "approved barrier collision and cyan electrical impact"),
    "stunned-after-crash": (False, "approved slack collapse, stars, smoke, and deployed device"),
    "phase-shift-fake-charge": (False, "approved visible-to-cyan phase displacement progression"),
    "suction-pulse-attack": (False, "approved gravity ring buildup through large aperture"),
    "enraged-rapid-alternating-charges": (False, "approved alternating charges and dust transition"),
    "hit-react": (False, "approved hit reactions with stun stars and sparks"),
    "containment-alarm-state": (False, "approved warning, overload smoke, and alarm progression"),
    "final-reveal-playing-possum": (False, "approved de-armored reveal through playing-possum rest"),
    "props-rig-core": (False, "standalone approved rig reference sprite"),
    "props-harness-upper": (False, "standalone approved harness component references"),
    "props-harness-lower": (False, "standalone approved harness component references"),
    "effects-library-upper": (False, "standalone approved electricity, barrier, gravity, dust, debris, and smoke effects"),
    "effects-library-lower": (False, "standalone approved debris, spark, and ground-fragment effects"),
}


ACTOR_STATES = {
    "idle-stand",
    "walk-heavy-movement",
    "charge-test-startup",
    "fast-charge",
    "crash-into-barrier",
    "stunned-after-crash",
    "phase-shift-fake-charge",
    "suction-pulse-attack",
    "enraged-rapid-alternating-charges",
    "hit-react",
    "containment-alarm-state",
    "final-reveal-playing-possum",
}


REQUIRED_SEQUENCES = {
    "emerge": {
        "sourceClassification": "MISSING",
        "classification": "EXISTS - COMPLETE (ASSEMBLED FROM APPROVED ART)",
        "orderedFrames": [
            "suction-pulse-attack-05",
            "phase-shift-fake-charge-08",
            "phase-shift-fake-charge-07",
            "phase-shift-fake-charge-05",
            "phase-shift-fake-charge-04",
            "idle-stand-00",
        ],
        "startState": "approved large gravity aperture without a duplicate body",
        "intermediateMotion": "approved cyan phase silhouettes resolve into the exact harnessed boss",
        "endState": "idle-stand-00 active boss state",
        "continuity": "canonical gravity/phase vocabulary resolves naturally to active idle",
        "loop": False,
    },
    "retreat": {
        "sourceClassification": "MISSING",
        "classification": "EXISTS - COMPLETE (ASSEMBLED FROM APPROVED ART)",
        "orderedFrames": [
            "idle-stand-00",
            "phase-shift-fake-charge-04",
            "phase-shift-fake-charge-05",
            "phase-shift-fake-charge-07",
            "phase-shift-fake-charge-08",
            "suction-pulse-attack-05",
        ],
        "startState": "idle-stand-00 active boss state",
        "intermediateMotion": "approved body phases into cyan displacement silhouettes",
        "endState": "approved gravity aperture after intentional withdrawal",
        "continuity": "active idle withdraws through canonical phase/portal mechanics without defeat imagery",
        "loop": False,
    },
    "defeat": {
        "sourceClassification": "EXISTS - INCOMPLETE (HARNESS-BREAK ROW ABSENT FROM ACCEPTED TRANSPARENT ATLAS)",
        "classification": "EXISTS - COMPLETE (ASSEMBLED FROM APPROVED ART)",
        "orderedFrames": [
            "hit-react-00",
            "hit-react-03",
            "stunned-after-crash-00",
            "stunned-after-crash-05",
            "containment-alarm-state-06",
            "effect-library-upper-00",
            *names("final-reveal-playing-possum", 9),
        ],
        "startState": "approved hit reaction in the complete harness",
        "intermediateMotion": "approved stun and overload pass through an approved electrical transition into the full ordered de-armored reveal",
        "endState": "final-reveal-playing-possum-08, the exact approved opossum resting non-graphically",
        "continuity": "hit to stun to overload to the complete approved reveal/playing-possum progression",
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


def assign_pixels(components: list[dict], zones: list[dict]) -> dict[str, list[int]]:
    assignments = {zone["id"]: [] for zone in zones}
    for component in components:
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


def frame_anchor(state_id: str, frame_id: str, frame: Image.Image) -> tuple[str, list[int]]:
    bbox = frame.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("cannot anchor empty frame")
    effect_only_actor_exceptions = {
        "suction-pulse-attack-05",
        "enraged-rapid-alternating-charges-03",
    }
    if state_id in ACTOR_STATES and frame_id not in effect_only_actor_exceptions:
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
    rendered = []
    for frame_id in frame_ids:
        canvas = Image.new("RGBA", (left + right, top + bottom), (0, 0, 0, 0))
        pivot_x, pivot_y = records[frame_id]["pivotInFrame"]
        canvas.alpha_composite(images[frame_id], (left - pivot_x, top - pivot_y))
        # Reserve palette index 255 exclusively for transparency. Pillow's
        # implicit RGBA-to-GIF conversion can otherwise turn transparent
        # regions opaque black when later frames use different palettes.
        paletted = canvas.convert("RGB").quantize(colors=255, method=Image.Quantize.MEDIANCUT)
        palette = paletted.getpalette()[: 255 * 3] + [0, 0, 0]
        paletted.putpalette(palette)
        transparent_mask = canvas.getchannel("A").point(lambda alpha: 255 if alpha == 0 else 0)
        paletted.paste(255, mask=transparent_mask)
        paletted.info["transparency"] = 255
        rendered.append(paletted)
    rendered[0].save(
        PREVIEWS_OUT / f"{name}.gif",
        save_all=True,
        append_images=rendered[1:],
        duration=140,
        loop=0,
        disposal=2,
        transparency=255,
    )


def immutable_specification() -> str:
    return """# Project O.P.O.S.S.U.M. Immutable Generation Specification

Execution: `EXECUTE: boss-project-opossum`  
Contract: `docs/design/trash-dash/manuals/bosses/BOSSFIX.md`, reread in full immediately before execution
Specification status: immutable for this execution batch

## Identity

- Boss: Project O.P.O.S.S.U.M. (`boss.level-04.project-opossum`).
- Canonical visual authority: `docs/design/trash-dash/library/characters/bosses/project-opossum/sprites/reference/boss-project-opossum.png`.
- Accepted transparent atlas: `docs/design/trash-dash/library/characters/bosses/project-opossum/sprites/animation-source/boss-project-opossum-transparent.png`.
- Locked: giant long broad low-slung charcoal/deep-gray quadrupedal opossum; sharply tapered pale gray-white face and dark eye patches; small pink-centered round ears; tiny dark/red-reflective eyes; pink nose and narrow clawed feet; long naked pink-purple dark-ringed tail; bulky improvised gunmetal laboratory harness with circular housings, copper coils, hoses, clamps, red/blue wiring, blue energy cells, warning lights, patched panels, aerials, sparks, and the prominent red top beacon.
- Host intent remains wary, anxious, intelligent, and defensive; the malfunctioning rig is the aggressor.

## Animation

- EMERGE: 6 approved frame references; gravity aperture -> cyan phase silhouettes -> exact harnessed boss -> active idle.
- RETREAT: 6 approved frame references; active idle -> exact harnessed boss -> cyan phase silhouettes -> gravity aperture. It contains no injured, unconscious, or defeated pose.
- DEFEAT: 15 approved frame references; hit -> stun -> overload -> approved electric transition -> all 9 approved de-armored reveal/playing-possum frames. It ends with the exact approved recognizable biological opossum resting non-graphically.
- The accepted transparent atlas has no named EMERGE/RETREAT rows and omits the branded board's harness-break row. No generation is necessary because approved portal, phase, hit, stun, overload, electricity, and full reveal states compose complete meanings without new art.
- Pose order inside every approved physical state remains unchanged. Runtime timing remains `UNSET / NOT PROMOTED`.

## Rendering

- Three-quarter side profile, canonical facing screen-right.
- Source and output scale: exactly 1:1; no resize, rotation, redraw, retouch, filter, or resampling.
- Preserve approved RGBA values, dimensions, internal registration, logical anchors, ground contact, palette, shading, texture, equipment, anatomy, facing, and effects language.
- Output: transparent RGBA PNG, manifest-defined variable rectangles, 8 transparent atlas-gutter pixels on every side in addition to transparent extraction padding.
- Actor pivot: largest connected body component ground contact. Standalone effect pivot: visible-envelope bottom center.
- Detached components are assigned wholly to one reviewed actor/effect rectangle; every visible source pixel is assigned exactly once.

## Restrictions and generation scope

- `GENERATE NEW = 0`; `REPLACE UNAPPROVED = 0`.
- Every physical sprite/support operation is `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`.
- No image generation is used. No rat anatomy, furry tail, upright stance, sleek armor, replacement face, missing beacon, biological magic, new weapon, marking, damage, costume element, acronym expansion, or sadistic host portrayal may be introduced.
- No runtime promotion, registration, collision, encounter, or gameplay edit is authorized.
"""


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    FRAMES_OUT.mkdir(parents=True, exist_ok=True)
    PREVIEWS_OUT.mkdir(parents=True, exist_ok=True)

    # Contract stages: immutable spec and batch inventory precede assembly.
    SPEC_OUT.write_text(immutable_specification())

    if not CONTRACT.exists() or not SOURCE.exists() or not CANON.exists() or not DESKTOP_COPY.exists():
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
    assignments = assign_pixels(components, zones)
    frame_order = [frame_id for state in states for frame_id in state["orderedFrames"]]
    source_visible_count = sum(1 for alpha in source.getchannel("A").tobytes() if alpha)
    assigned_visible_count = sum(len(assignments[frame_id]) for frame_id in frame_order)
    if source_visible_count != assigned_visible_count:
        raise RuntimeError("visible source coverage is not exactly one-to-one")
    all_assigned = [point for frame_id in frame_order for point in assignments[frame_id]]
    if len(all_assigned) != len(set(all_assigned)):
        raise RuntimeError("a visible source pixel was assigned more than once")

    audit = {
        "boss": "Project O.P.O.S.S.U.M.",
        "canonId": "boss.level-04.project-opossum",
        "executionContract": {
            "path": str(CONTRACT.relative_to(ROOT)),
            "sha256": file_sha(CONTRACT),
        },
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
            "byteIdenticalToDesktopCopy": True,
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
            "missingOrIncompleteNamedAnimations": True,
            "crossFrameRectangularEnvelopeOverlap": True,
            "neighboringFrameBleedRisk": True,
            "visiblePixelsTouchingAcceptedAtlasBoundary": False,
            "ambiguousDetachedEffectOwnershipBeforeManifest": True,
            "insufficientTransparentGutters": True,
            "missingNamedEmergeRow": True,
            "missingNamedRetreatRow": True,
            "harnessBreakDefeatRowAbsentFromAcceptedTransparentAtlas": True,
            "requiredSequenceArtProvenMissingAfterApprovedAssembly": False,
        },
        "resolution": "approved-frame sequence composition plus reviewed connected-alpha ownership extraction and variable-cell repack; no artwork generation",
    }
    AUDIT_OUT.write_text(json.dumps(audit, indent=2) + "\n")

    batch_manifest = {
        "boss": "Project O.P.O.S.S.U.M.",
        "execution": "EXECUTE: boss-project-opossum",
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
                "ownership": "all complete connected-alpha components whose bounding-box center is inside this reviewed region",
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
        anchor_type, pivot = frame_anchor(state_id, frame_id, frame)
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
            "effectOwnership": (
                "integrated-with-emitter-frame"
                if state_id in ACTOR_STATES and anchor_type == "body-ground-contact"
                else "standalone-effect-or-reference-sprite"
            ),
            "timing": {
                "stateFrameIndex": zone_by_id[frame_id]["stateFrameIndex"],
                "durationMs": None,
                "status": "approved source order; runtime timing not promoted",
            },
            "frameRgbaSha256": raw_sha(frame),
            "visiblePixelSha256": visible_pixel_sha(frame),
            "visiblePixelCount": len(owned),
        }

    placements, atlas_size = pack_frames([(frame_id, images[frame_id]) for frame_id in frame_order])
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
        "assetName": "boss-project-opossum-isolated",
        "canonId": "boss.level-04.project-opossum",
        "status": "artwork-approved",
        "approval": {
            "approvedBy": "project-owner",
            "approvedOn": "2026-08-13",
            "scope": "Level 4 Project O.P.O.S.S.U.M. isolated artwork package",
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
            "method": "reviewed connected-alpha ownership masks plus lossless source-scale relocation",
            "aiGenerationUsed": False,
            "resizingUsed": False,
            "redrawingUsed": False,
            "filteringUsed": False,
            "rotationUsed": False,
            "runtimePromotionUsed": False,
            "rebuildCommand": "python3 tools/asset_pipeline/build_boss_project_opossum_isolated.py",
            "verifyCommand": "python3 tools/verify/check_boss_project_opossum_isolated.py",
        },
    }
    MANIFEST_OUT.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"wrote {len(records)} isolated approved frames/support sprites")
    print(f"atlas {atlas.width}x{atlas.height}; visible pixels {source_visible_count} assigned exactly once")


if __name__ == "__main__":
    main()
