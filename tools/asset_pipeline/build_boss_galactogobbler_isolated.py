#!/usr/bin/env python3
"""Losslessly isolate and repack the approved Galactogobbler atlas.

Every opaque source pixel is assigned exactly once to a reviewed rectangular
ownership zone. The builder preserves source RGBA values at 1:1 scale, adds
transparent extraction gutters, and composes EMERGE, RETREAT, and DEFEAT from
approved physical frames only. It never generates or redraws artwork.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/generated/boss-galactogobbler-isolated"
FRAMES_OUT = OUTPUT / "frames"
PREVIEWS_OUT = OUTPUT / "previews"
SOURCE = ROOT / "docs/design/trash-dash/library/characters/bosses/galactogobbler/sprites/animation-source/boss-galactogobbler-transparent.png"
CANON = ROOT / "docs/design/trash-dash/library/characters/bosses/galactogobbler/sprites/reference/boss-galactogobbler.png"
ATTACHED_COPY = Path("/Users/jamesschmittler/Desktop/boss-galactogobbler-transparent.png")
ATLAS_OUT = OUTPUT / "boss-galactogobbler-isolated.png"
CONTACT_OUT = OUTPUT / "contact-sheet.png"
MANIFEST_OUT = OUTPUT / "manifest.json"
BATCH_OUT = OUTPUT / "batch-manifest.json"
AUDIT_OUT = OUTPUT / "source-audit.json"
SPEC_OUT = OUTPUT / "immutable-generation-specification.md"
REPORT_OUT = OUTPUT / "validation-report.md"
APPROVAL_OUT = OUTPUT / "APPROVAL.md"

SOURCE_SIZE = (1536, 1024)
CANON_SIZE = (1448, 1086)
SOURCE_SHA256 = "3a030409a4ee38c38ece7137f4a5f6484b629b12ec9dcc9760e8ecd18015f15a"
CANON_SHA256 = "9c1896aa4b61bed52586e4b1df3dbeca002e3edb09da536ab17945332284ace4"
SOURCE_PAD = 2
GUTTER = 8
MAX_ATLAS_WIDTH = 2048


def file_sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def raw_sha(image: Image.Image) -> str:
    return hashlib.sha256(image.convert("RGBA").tobytes()).hexdigest()


def source_pixel_sha(source: Image.Image, points: list[int]) -> str:
    digest = hashlib.sha256()
    rgba = source.convert("RGBA").tobytes()
    for point in sorted(points):
        y, x = divmod(point, source.width)
        offset = point * 4
        digest.update(x.to_bytes(2, "big"))
        digest.update(y.to_bytes(2, "big"))
        digest.update(rgba[offset : offset + 4])
    return digest.hexdigest()


def center_splits(left: int, right: int, centers: list[int]) -> list[int]:
    return [left] + [(a + b) // 2 for a, b in zip(centers, centers[1:])] + [right]


def add_group(
    zones: list[dict],
    state: str,
    bounds: tuple[int, int, int, int],
    centers: list[int],
    role: str = "actor-with-integrated-effects",
) -> None:
    left, top, right, bottom = bounds
    splits = center_splits(left, right, centers)
    for index in range(len(centers)):
        zones.append(
            {
                "id": f"{state}-{index:02d}",
                "state": state,
                "stateFrameIndex": index,
                "selectionRegion": [splits[index], top, splits[index + 1], bottom],
                "role": role,
            }
        )


def reviewed_zones() -> list[dict]:
    zones: list[dict] = [
        {
            "id": "intro-annular-form-00",
            "state": "intro-annular-form",
            "stateFrameIndex": 0,
            "selectionRegion": [0, 0, 380, 295],
            "role": "actor-with-integrated-orbit-debris",
        }
    ]
    add_group(zones, "idle-hover", (380, 0, 1295, 85), [428, 543, 646, 758, 897, 1008, 1114, 1224])
    add_group(zones, "inhale-telegraph", (380, 85, 1295, 155), [429, 532, 644, 756, 877, 993, 1104, 1223])
    add_group(zones, "suction-pull-attack", (380, 155, 1295, 225), [422, 538, 650, 765, 905, 1028, 1134, 1248])
    add_group(zones, "core-shot", (380, 225, 1295, 295), [416, 538, 661, 774, 892, 1013, 1136])
    add_group(zones, "spit-attack", (0, 295, 1295, 352), [200, 485, 655, 790, 950, 1120, 1230])
    add_group(zones, "armadillo-launch-toss", (0, 352, 1295, 410), [70, 180, 300, 420, 530, 640, 760, 880, 1005, 1140, 1240])
    add_group(zones, "rocket-roach-summon", (0, 410, 1295, 470), [88, 205, 330, 445, 570, 690, 805, 915, 1035, 1165, 1260])
    add_group(zones, "gravity-reversal-phase", (0, 470, 1295, 530), [92, 212, 403, 546, 652, 788, 932, 1074, 1228])
    add_group(zones, "enraged-attack-loop", (0, 530, 1295, 590), [72, 194, 274, 420, 598, 724, 836, 970, 1094, 1223])
    add_group(zones, "hit-react", (0, 590, 1295, 645), [66, 178, 304, 452, 568, 706, 844, 948, 1048, 1152, 1248])
    add_group(zones, "shell-crack-progression", (0, 645, 1295, 708), [66, 183, 297, 423, 550, 688, 814, 926, 1050, 1176, 1273])
    add_group(zones, "stunned-vulnerable", (0, 708, 1295, 756), [72, 220, 386, 504, 619, 743, 871, 988, 1112, 1224])
    add_group(zones, "defeat-collapse", (0, 756, 1316, 815), [55, 165, 275, 385, 495, 605, 715, 825, 935, 1045, 1155, 1270], "integrated-rubble-collapse-effect")
    add_group(zones, "vulnerable-alien", (0, 815, 1295, 873), [70, 180, 304, 410, 534, 644, 744, 862, 961, 1060, 1148, 1235])
    zones[-1]["additionalSelectionRegions"] = [[1295, 815, 1316, 850]]
    add_group(zones, "black-bag-reconstitution", (0, 873, 1290, 1005), [61, 164, 278, 386, 496, 600, 704, 810, 910, 1010, 1110, 1208], "actor-associated-bag-form")

    add_group(zones, "prop-harness-upper", (1295, 91, 1536, 144), [1328, 1382, 1434, 1481], "standalone-support-sprite")
    add_group(zones, "prop-harness-middle-a", (1295, 144, 1536, 193), [1330, 1376, 1428, 1482], "standalone-support-sprite")
    add_group(zones, "prop-harness-middle-b", (1295, 193, 1536, 243), [1331, 1389, 1438, 1484], "standalone-support-sprite")
    add_group(zones, "prop-harness-lower", (1295, 243, 1536, 290), [1324, 1369, 1413, 1451, 1470, 1483], "standalone-support-sprite")
    add_group(zones, "cosmic-junk-chunk", (1295, 290, 1536, 360), [1320, 1360, 1395, 1430, 1465, 1500], "standalone-effect-sprite")
    add_group(zones, "suction-ring", (1295, 360, 1536, 435), [1328, 1362, 1404, 1447, 1484, 1506], "standalone-effect-sprite")
    add_group(zones, "glowing-mouth-core", (1295, 435, 1536, 495), [1333, 1372, 1410, 1450, 1501], "standalone-effect-sprite")
    add_group(zones, "gravity-reversal-aura", (1295, 495, 1536, 575), [1329, 1410, 1490], "standalone-effect-sprite")
    add_group(zones, "rocket-roach-trail", (1295, 575, 1536, 640), [1320, 1356, 1382, 1425, 1476], "standalone-effect-sprite")
    add_group(zones, "asteroid-debris-spark", (1295, 640, 1536, 730), [1348, 1378, 1402, 1440, 1468, 1505], "standalone-effect-sprite")
    add_group(zones, "glowing-trash-canister", (1316, 760, 1536, 830), [1339, 1384, 1427, 1468, 1508], "standalone-support-sprite")
    add_group(zones, "orbiting-harness-junk-a", (1290, 850, 1536, 905), [1312, 1344, 1372, 1403, 1439, 1472, 1504], "standalone-support-sprite")
    add_group(zones, "orbiting-harness-junk-b", (1290, 905, 1536, 950), [1310, 1349, 1382, 1414, 1448, 1480, 1506], "standalone-support-sprite")
    add_group(zones, "orbiting-harness-junk-c", (1290, 950, 1536, 990), [1320, 1336, 1368, 1396, 1425, 1451, 1474, 1506], "standalone-support-sprite")
    return zones


STATE_META = {
    "intro-annular-form": (False, "approved dramatic annular shell reveal"),
    "idle-hover": (True, "approved active armored hover loop"),
    "inhale-telegraph": (False, "approved suction anticipation"),
    "suction-pull-attack": (False, "approved gravity-pull progression"),
    "core-shot": (False, "approved core charge and discharge"),
    "spit-attack": (False, "approved gravity-orb emitter and travel envelopes"),
    "armadillo-launch-toss": (False, "approved shell-and-debris toss progression"),
    "rocket-roach-summon": (False, "approved summon and burst interaction"),
    "gravity-reversal-phase": (False, "approved gravity aura phase progression"),
    "enraged-attack-loop": (True, "approved enraged attack vocabulary"),
    "hit-react": (False, "approved ordered hit reactions"),
    "shell-crack-progression": (False, "approved three-stage mass shedding"),
    "stunned-vulnerable": (False, "approved core-exposed vulnerable progression"),
    "defeat-collapse": (False, "approved shell-burst rubble progression"),
    "vulnerable-alien": (False, "approved living alien and canister expressions"),
    "black-bag-reconstitution": (False, "approved emblem-bag sequence; function remains TBD"),
    "prop-harness-upper": (False, "approved standalone prop library"),
    "prop-harness-middle-a": (False, "approved standalone prop library"),
    "prop-harness-middle-b": (False, "approved standalone prop library"),
    "prop-harness-lower": (False, "approved standalone prop library"),
    "cosmic-junk-chunk": (False, "approved standalone debris library"),
    "suction-ring": (False, "approved standalone ring effects"),
    "glowing-mouth-core": (False, "approved standalone core effects"),
    "gravity-reversal-aura": (False, "approved standalone gravity effects"),
    "rocket-roach-trail": (False, "approved standalone summon trails"),
    "asteroid-debris-spark": (False, "approved standalone meteor debris"),
    "glowing-trash-canister": (False, "approved standalone canister variants"),
    "orbiting-harness-junk-a": (False, "approved standalone orbiting parts"),
    "orbiting-harness-junk-b": (False, "approved standalone orbiting parts"),
    "orbiting-harness-junk-c": (False, "approved standalone orbiting parts"),
}


REQUIRED_SEQUENCES = {
    "emerge": {
        "classification": "EXISTS - COMPLETE",
        "orderedFrames": [
            "black-bag-reconstitution-11", "black-bag-reconstitution-10", "black-bag-reconstitution-09",
            "black-bag-reconstitution-07", "black-bag-reconstitution-00", "vulnerable-alien-00",
            "defeat-collapse-11", "defeat-collapse-09", "defeat-collapse-07", "defeat-collapse-05",
            "defeat-collapse-03", "defeat-collapse-01", "shell-crack-progression-10",
            "shell-crack-progression-07", "shell-crack-progression-04", "shell-crack-progression-00",
            "idle-hover-00",
        ],
        "startState": "approved nearly dispersed emblem-bag state",
        "intermediateMotion": "approved bag, living alien/canister, rubble, gravity reassembly, and shell restoration artwork",
        "endState": "idle-hover-00 active armored state",
        "continuity": "canonical bag/reconstitution vocabulary resolves to approved active idle; no new mechanism",
        "loop": False,
    },
    "retreat": {
        "classification": "EXISTS - COMPLETE",
        "orderedFrames": [
            "idle-hover-00", "shell-crack-progression-00", "shell-crack-progression-04",
            "shell-crack-progression-07", "shell-crack-progression-10", "defeat-collapse-01",
            "defeat-collapse-03", "defeat-collapse-05", "defeat-collapse-07", "defeat-collapse-09",
            "defeat-collapse-11", "vulnerable-alien-00", "black-bag-reconstitution-00",
            "black-bag-reconstitution-07", "black-bag-reconstitution-09", "black-bag-reconstitution-10",
            "black-bag-reconstitution-11",
        ],
        "startState": "idle-hover-00 active armored state",
        "intermediateMotion": "intentional gravity recall through approved shell, rubble, alien/canister, and emblem-bag states",
        "endState": "approved nearly dispersed emblem-bag inactive/exit state",
        "continuity": "active shell intentionally withdraws through canonical reconstitution vocabulary and remains capable of return",
        "loop": False,
    },
    "defeat": {
        "classification": "EXISTS - COMPLETE",
        "orderedFrames": [
            "hit-react-00", "hit-react-03", "hit-react-06", "hit-react-10",
            "shell-crack-progression-00", "shell-crack-progression-03", "shell-crack-progression-06",
            "shell-crack-progression-10", "stunned-vulnerable-00", "stunned-vulnerable-03",
            "stunned-vulnerable-06", "stunned-vulnerable-09", "defeat-collapse-00",
            "defeat-collapse-02", "defeat-collapse-04", "defeat-collapse-06", "defeat-collapse-08",
            "defeat-collapse-10", "defeat-collapse-11", "vulnerable-alien-00",
        ],
        "startState": "approved armored hit reaction",
        "intermediateMotion": "approved mass shedding, core exposure, shell burst, and rubble dissipation",
        "endState": "approved living lavender alien visibly identifiable beside the cyan canister",
        "continuity": "loss reads through approved shell destruction while preserving the living exact character and canister",
        "loop": False,
    },
}


def states_from_zones(zones: list[dict]) -> list[dict]:
    order: list[str] = []
    frames: dict[str, list[str]] = {}
    for zone in zones:
        if zone["state"] not in frames:
            order.append(zone["state"])
            frames[zone["state"]] = []
        frames[zone["state"]].append(zone["id"])
    states = []
    for state in order:
        loop, progression = STATE_META[state]
        states.append(
            {
                "id": state,
                "orderedFrames": frames[state],
                "frameCount": len(frames[state]),
                "loop": loop,
                "progression": progression,
                "timing": {
                    "basis": "approved-source-order",
                    "durationMs": None,
                    "status": "UNSET / NOT PROMOTED; runtime timing intentionally not invented",
                },
            }
        )
    return states


def assign_visible_pixels(source: Image.Image, zones: list[dict]) -> dict[str, list[int]]:
    width, height = source.size
    alpha = source.getchannel("A").tobytes()
    owner = [-1] * (width * height)
    assignments = {zone["id"]: [] for zone in zones}
    for zone_index, zone in enumerate(zones):
        regions = [zone["selectionRegion"], *zone.get("additionalSelectionRegions", [])]
        for left, top, right, bottom in regions:
            if not (0 <= left < right <= width and 0 <= top < bottom <= height):
                raise RuntimeError(f"invalid zone geometry: {zone['id']}")
            for y in range(top, bottom):
                row = y * width
                for x in range(left, right):
                    point = row + x
                    if not alpha[point]:
                        continue
                    if owner[point] != -1:
                        raise RuntimeError(f"visible source pixel multiply owned at {(x, y)}")
                    owner[point] = zone_index
                    assignments[zone["id"]].append(point)
    missing = [point for point, value in enumerate(alpha) if value and owner[point] == -1]
    if missing:
        examples = [divmod(point, width)[::-1] for point in missing[:12]]
        raise RuntimeError(f"{len(missing)} visible source pixels unassigned; examples {examples}")
    empty = [frame_id for frame_id, points in assignments.items() if not points]
    if empty:
        raise RuntimeError(f"reviewed zones without visible pixels: {empty}")
    return assignments


def pixels_bbox(points: list[int], width: int) -> tuple[int, int, int, int]:
    xs, ys = [], []
    for point in points:
        y, x = divmod(point, width)
        xs.append(x)
        ys.append(y)
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def largest_component_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    width, height = image.size
    alpha = image.getchannel("A").tobytes()
    visible = bytearray(1 if value else 0 for value in alpha)
    visited = bytearray(width * height)
    largest: tuple[int, tuple[int, int, int, int]] | None = None
    for start, is_visible in enumerate(visible):
        if not is_visible or visited[start]:
            continue
        stack = [start]
        visited[start] = 1
        count = 0
        min_x, min_y, max_x, max_y = width, height, 0, 0
        while stack:
            point = stack.pop()
            y, x = divmod(point, width)
            count += 1
            min_x, min_y = min(min_x, x), min(min_y, y)
            max_x, max_y = max(max_x, x), max(max_y, y)
            for neighbor_y in range(max(0, y - 1), min(height - 1, y + 1) + 1):
                row = neighbor_y * width
                for neighbor_x in range(max(0, x - 1), min(width - 1, x + 1) + 1):
                    neighbor = row + neighbor_x
                    if visible[neighbor] and not visited[neighbor]:
                        visited[neighbor] = 1
                        stack.append(neighbor)
        candidate = (count, (min_x, min_y, max_x + 1, max_y + 1))
        if largest is None or candidate[0] > largest[0]:
            largest = candidate
    if largest is None:
        raise RuntimeError("cannot anchor empty frame")
    return largest[1]


def frame_anchor(zone: dict, frame: Image.Image) -> tuple[str, list[int]]:
    bbox = frame.getchannel("A").getbbox()
    if bbox is None:
        raise RuntimeError("cannot anchor empty frame")
    if zone["role"] in {"standalone-effect-sprite", "integrated-rubble-collapse-effect"}:
        return "effect-bottom-center", [round((bbox[0] + bbox[2] - 1) / 2), bbox[3] - 1]
    body = largest_component_bbox(frame)
    return "body-or-object-ground-contact", [round((body[0] + body[2] - 1) / 2), body[3] - 1]


def pack_frames(frame_images: list[tuple[str, Image.Image]]) -> tuple[list[dict], tuple[int, int]]:
    placements: list[dict] = []
    x = y = row_height = 0
    for frame_id, image in frame_images:
        cell_width, cell_height = image.width + GUTTER * 2, image.height + GUTTER * 2
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
    rendered: list[Image.Image] = []
    for frame_id in frame_ids:
        canvas = Image.new("RGBA", (left + right, top + bottom), (0, 0, 0, 0))
        pivot_x, pivot_y = records[frame_id]["pivotInFrame"]
        canvas.alpha_composite(images[frame_id], (left - pivot_x, top - pivot_y))
        rendered.append(canvas)
    rendered[0].save(
        PREVIEWS_OUT / f"{name}.gif",
        save_all=True,
        append_images=rendered[1:],
        duration=150,
        loop=0,
        disposal=2,
        transparency=0,
    )


def immutable_specification() -> str:
    return """# Galactogobbler Immutable Generation Specification

Execution: `EXECUTE: boss-galactogobbler`  
Contract: `docs/design/trash-dash/manuals/bosses/BOSSFIX.md`, reread in full immediately before execution
Specification status: immutable for this execution batch

## Identity

- Boss: Galactogobbler, Hoarder of Worlds (`boss.level-05.galactogobbler`).
- Canonical visual authority: `docs/design/trash-dash/library/characters/bosses/galactogobbler/sprites/reference/boss-galactogobbler.png`.
- Accepted transparent atlas: `docs/design/trash-dash/library/characters/bosses/galactogobbler/sprites/animation-source/boss-galactogobbler-transparent.png`.
- Locked: small lavender-to-deep-violet alien; bulbous hairless head; two enormous glossy black-purple oval eyes; tiny nostrils; wide subordinate-to-maw mouth; compact limbs and rounded fingers; cyan luminous cylindrical canister; nearly spherical asteroid/electronics/cosmic-garbage shell; circular aperture; orbiting scraps; curious, hungry, frightened, uncertain, intelligent affect.
- Locked effects: violet/lavender/magenta-white/cyan/deep near-black gravity, portals, orbit paths, rubble, meteors with limited orange-yellow heat, black tied emblem bags, canister light, smoke, wire, machinery, and reassembly effects already present in the accepted atlas.

## Animation

- EMERGE: 17 approved references; dispersed emblem-bag state -> bag/body reveal -> approved rubble and shell reassembly -> active idle.
- RETREAT: 17 approved references; active idle -> intentional shell recall -> alien/canister -> emblem-bag inactive/exit state. It is reversible and does not end in a defeat hold.
- DEFEAT: 20 approved references; hit -> mass shedding -> exposed core -> shell burst/rubble -> living alien beside cyan canister.
- Every sequence uses references to isolated approved physical sprites; no pixels are duplicated in the atlas.
- Timing is `UNSET / NOT PROMOTED`; runtime cadence and event frames are intentionally not invented before approval.

## Rendering

- Preserve the accepted perspective, source scale, lighting, shading, texture, palette, alpha, and ground/contact relationships exactly.
- Source and output pixel scale are 1:1. No resize, rotation, redraw, retouch, filtering, cleanup, or resampling is permitted.
- Output is transparent RGBA with manifest-defined variable rectangles and 8 transparent atlas-gutter pixels on every side, in addition to 2 transparent extraction-padding pixels.
- Actor/object pivots use the largest owned connected component's bottom center. Effect/rubble pivots use the complete visible envelope's bottom center.
- Crowded source rows are resolved by reviewed rectangular ownership partitions. Those partitions are layout-only isolation seams; every original visible RGBA pixel is retained exactly once.

## Restrictions and generation scope

- `GENERATE NEW = 0`; `REPLACE UNAPPROVED = 0`.
- Every physical output is `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`.
- Do not add a giant eyeball, tentacles, spacesuit, clean sphere, rock-only shell, missing alien/core, demon characterization, cockpit, green poison, conventional fire magic, primary blue lightning, weapons, anatomy, markings, damage, or costume elements.
- Do not permanently explain the emblem-bag function.
- Do not promote, register, or copy any output into `assets/runtime/`.
"""


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    FRAMES_OUT.mkdir(parents=True, exist_ok=True)
    PREVIEWS_OUT.mkdir(parents=True, exist_ok=True)

    if not SOURCE.exists() or not CANON.exists() or not ATTACHED_COPY.exists():
        raise RuntimeError("required approved source input is missing")
    if file_sha(SOURCE) != SOURCE_SHA256 or file_sha(ATTACHED_COPY) != SOURCE_SHA256:
        raise RuntimeError("accepted atlas or attached copy changed")
    if file_sha(CANON) != CANON_SHA256:
        raise RuntimeError("canonical visual authority changed")

    source = Image.open(SOURCE).convert("RGBA")
    canonical = Image.open(CANON)
    if source.size != SOURCE_SIZE or canonical.size != CANON_SIZE:
        raise RuntimeError("approved input dimensions changed")
    alpha_values = set(source.getchannel("A").tobytes())
    if alpha_values != {0, 255}:
        raise RuntimeError("accepted atlas must contain hard transparent and opaque alpha only")

    zones = reviewed_zones()
    states = states_from_zones(zones)
    assignments = assign_visible_pixels(source, zones)
    frame_order = [frame_id for state in states for frame_id in state["orderedFrames"]]
    source_visible_count = sum(1 for alpha in source.getchannel("A").tobytes() if alpha)
    assigned_count = sum(len(assignments[frame_id]) for frame_id in frame_order)
    if assigned_count != source_visible_count:
        raise RuntimeError("visible source coverage is not exactly one-to-one")

    source_bytes = source.tobytes()
    zone_by_id = {zone["id"]: zone for zone in zones}
    images: dict[str, Image.Image] = {}
    records: dict[str, dict] = {}
    for frame_id in frame_order:
        zone = zone_by_id[frame_id]
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
        anchor_type, pivot = frame_anchor(zone, frame)
        destination = FRAMES_OUT / f"{frame_id}.png"
        images[frame_id] = frame
        records[frame_id] = {
            "state": zone["state"],
            "stateFrameIndex": zone["stateFrameIndex"],
            "classification": "PRESERVE EXACTLY - REPOSITION FOR ISOLATION",
            "sourceOwnershipSelectionRegion": zone["selectionRegion"],
            "sourceOwnershipAdditionalSelectionRegions": zone.get("additionalSelectionRegions", []),
            "sourceRect": [source_rect[0], source_rect[1], frame.width, frame.height],
            "sourceVisibleBounds": list(visible_box),
            "frameFile": str(destination.relative_to(OUTPUT)),
            "frameSize": list(frame.size),
            "visibleBoundsInFrame": list(bbox),
            "pivotType": anchor_type,
            "pivotInFrame": pivot,
            "effectOwnership": zone["role"],
            "timing": {
                "stateFrameIndex": zone["stateFrameIndex"],
                "durationMs": None,
                "status": "UNSET / NOT PROMOTED; approved source order only",
            },
            "sourceVisiblePixelSha256": source_pixel_sha(source, owned),
            "frameRgbaSha256": raw_sha(frame),
            "visiblePixelCount": len(owned),
        }

    placements, atlas_size = pack_frames([(frame_id, images[frame_id]) for frame_id in frame_order])
    for placement in placements:
        frame_id = placement["id"]
        records[frame_id]["cellRect"] = placement["cellRect"]
        records[frame_id]["artRect"] = placement["artRect"]
        records[frame_id]["pivotInCell"] = [
            GUTTER + records[frame_id]["pivotInFrame"][0],
            GUTTER + records[frame_id]["pivotInFrame"][1],
        ]

    # Contract stage order: specification and full pre-assembly batch manifest
    # are committed before any physical frame or atlas file is written.
    SPEC_OUT.write_text(immutable_specification())
    audit = {
        "boss": "Galactogobbler, Hoarder of Worlds",
        "canonId": "boss.level-05.galactogobbler",
        "canonicalBoard": {"path": str(CANON.relative_to(ROOT)), "sha256": file_sha(CANON), "size": list(canonical.size), "mode": canonical.mode},
        "acceptedTransparentAtlas": {
            "path": str(SOURCE.relative_to(ROOT)), "sha256": file_sha(SOURCE), "attachedCopySha256": file_sha(ATTACHED_COPY),
            "size": list(source.size), "mode": "RGBA", "visibleBounds": list(source.getchannel("A").getbbox()),
            "visiblePixelCount": source_visible_count, "opaquePixelCount": source_visible_count,
            "transparentPixelCount": source.width * source.height - source_visible_count, "partialAlphaPixelCount": 0,
        },
        "sequenceAudit": REQUIRED_SEQUENCES,
        "defects": {
            "missingOrIncompleteAnimations": False,
            "crossFrameSpriteOrEffectOverlap": True,
            "neighboringFrameBleedRisk": True,
            "visiblePixelsTouchingAcceptedAtlasBoundary": False,
            "ambiguousDetachedEffectOwnershipBeforeManifest": True,
            "insufficientTransparentGutters": True,
            "missingEmergeFrames": False, "missingRetreatFrames": False, "missingDefeatFrames": False,
        },
        "resolution": "approved-only sequence composition plus reviewed rectangular ownership-mask extraction and variable-cell repack; no artwork generation",
    }
    AUDIT_OUT.write_text(json.dumps(audit, indent=2) + "\n")
    batch_manifest = {
        "boss": "Galactogobbler, Hoarder of Worlds",
        "execution": "EXECUTE: boss-galactogobbler",
        "status": "immutable-pre-assembly-manifest",
        "originalSheetDimensions": list(source.size),
        "updatedSheetDimensions": list(atlas_size),
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
                "frame": frame_id,
                "state": records[frame_id]["state"],
                "stateFrameIndex": records[frame_id]["stateFrameIndex"],
                "classification": records[frame_id]["classification"],
                "sourceOwnershipSelectionRegion": records[frame_id]["sourceOwnershipSelectionRegion"],
                "sourceOwnershipAdditionalSelectionRegions": records[frame_id]["sourceOwnershipAdditionalSelectionRegions"],
                "completeSourceVisibleBounds": records[frame_id]["sourceVisibleBounds"],
                "outputCellRect": records[frame_id]["cellRect"],
                "outputArtRect": records[frame_id]["artRect"],
                "ownership": records[frame_id]["effectOwnership"],
                "anchor": records[frame_id]["pivotType"],
                "timing": records[frame_id]["timing"]["status"],
            }
            for frame_id in frame_order
        ],
    }
    BATCH_OUT.write_text(json.dumps(batch_manifest, indent=2) + "\n")

    for folder in (FRAMES_OUT, PREVIEWS_OUT):
        for stale in folder.glob("*"):
            if stale.is_file():
                stale.unlink()
    for frame_id, frame in images.items():
        frame.save(FRAMES_OUT / f"{frame_id}.png", format="PNG", compress_level=9, optimize=False)

    atlas = Image.new("RGBA", atlas_size, (0, 0, 0, 0))
    for placement in placements:
        frame_id = placement["id"]
        art_x, art_y, _width, _height = placement["artRect"]
        atlas.paste(images[frame_id], (art_x, art_y))
    atlas.save(ATLAS_OUT, format="PNG", compress_level=9, optimize=False)

    contact = Image.new("RGBA", atlas.size, (42, 45, 48, 255))
    draw = ImageDraw.Draw(contact)
    tile = 16
    for y in range(0, contact.height, tile):
        for x in range(0, contact.width, tile):
            if (x // tile + y // tile) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill=(56, 60, 64, 255))
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
        "assetName": "boss-galactogobbler-isolated",
        "canonId": "boss.level-05.galactogobbler",
        "status": "artwork-approved",
        "approval": {
            "approvedBy": "project-owner",
            "approvedOn": "2026-08-13",
            "scope": "Level 5 Galactogobbler isolated artwork package, manifest-defined rectangles, and approved-only EMERGE, RETREAT, and DEFEAT sequences",
            "runtimePromotionAuthorized": False,
        },
        "canonicalFacing": "screen-right where directional",
        "approvedSource": str(SOURCE.relative_to(ROOT)),
        "approvedSourceSha256": file_sha(SOURCE),
        "canonicalVisualAuthority": str(CANON.relative_to(ROOT)),
        "canonicalVisualSha256": file_sha(CANON),
        "sheet": {
            "file": str(ATLAS_OUT.relative_to(ROOT)), "size": list(atlas.size), "mode": "RGBA",
            "background": "transparent", "layout": "manifest-defined-variable-rectangles",
            "gutterPixels": GUTTER, "readingOrder": "physical state order then approved source order",
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
            "method": "reviewed rectangular ownership masks plus lossless source-scale relocation",
            "aiGenerationUsed": False, "resizingUsed": False, "redrawingUsed": False,
            "filteringUsed": False, "rotationUsed": False, "runtimePromotionUsed": False,
            "rebuildCommand": "python3 tools/asset_pipeline/build_boss_galactogobbler_isolated.py",
            "verifyCommand": "python3 tools/verify/check_boss_galactogobbler_isolated.py",
        },
    }
    MANIFEST_OUT.write_text(json.dumps(manifest, indent=2) + "\n")
    APPROVAL_OUT.write_text(
        "# Galactogobbler Artwork Approval\n\n"
        "Status: **ARTWORK APPROVED**\n\n"
        "The project owner approved the Level 5 Galactogobbler isolated artwork package on 2026-08-13.\n\n"
        "Approval covers the complete transparent sheet, 224 extracted frames and support/effect sprites, "
        "manifest-defined variable rectangles and pivots, boundary-labeled contact sheet, and the approved-only "
        "EMERGE, RETREAT, and DEFEAT sequences.\n\n"
        "Runtime promotion, engine registration, gameplay integration, collision, timing, encounter changes, "
        "real-runtime traversal, and the V2 release gate remain separate work and are not authorized by this approval.\n"
    )
    REPORT_OUT.write_text(
        "# Galactogobbler Bossfix Validation\n\n"
        "Status: `PENDING INDEPENDENT VERIFICATION`\n\n"
        "The deterministic build completed with exact one-to-one visible-pixel coverage. "
        "Run `python3 tools/verify/check_boss_galactogobbler_isolated.py` to populate the final seven-test result.\n"
    )
    print(f"wrote {len(records)} isolated approved frames/support sprites")
    print(f"atlas {atlas.width}x{atlas.height}; visible pixels {source_visible_count} assigned exactly once")
    print("artwork generated: 0; artwork replaced: 0; runtime promotion: 0")


if __name__ == "__main__":
    main()
