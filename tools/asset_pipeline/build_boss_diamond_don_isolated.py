#!/usr/bin/env python3
"""Losslessly isolate and repack the approved Diamond Don atlas.

Every opaque source pixel is assigned exactly once to a reviewed rectangular
ownership zone. No artwork is generated, altered, resampled, or promoted.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "assets/generated/boss-diamond-don-isolated"
FRAMES_OUT = OUTPUT / "frames"
PREVIEWS_OUT = OUTPUT / "previews"
SOURCE = ROOT / "docs/design/trash-dash/character-animation/phase-05-codex-integration/phase-04-bosses/final/boss-diamond-don-transparent.png"
CANON = ROOT / "docs/design/trash-dash/reference/characters/level-06/sprites/boss-diamond-don.png"
ATTACHED_COPY = Path("/Users/jamesschmittler/Desktop/boss-diamond-don-transparent.png")
ATLAS_OUT = OUTPUT / "boss-diamond-don-isolated.png"
CONTACT_OUT = OUTPUT / "contact-sheet.png"
MANIFEST_OUT = OUTPUT / "manifest.json"
BATCH_OUT = OUTPUT / "batch-manifest.json"
AUDIT_OUT = OUTPUT / "source-audit.json"
SPEC_OUT = OUTPUT / "immutable-generation-specification.md"
REPORT_OUT = OUTPUT / "validation-report.md"
APPROVAL_OUT = OUTPUT / "APPROVAL.md"

SOURCE_SIZE = (1536, 1024)
CANON_SIZE = (1448, 1086)
SOURCE_SHA256 = "7376000f332ef2ee4d58602b0843018c908ccbb0cd014fefb8e38d3704252bb8"
CANON_SHA256 = "f6132b478842f9cf6a5d54b32072e3ac1027aad3b1835350b40be680b483f5ac"
FRAME_PAD = 2
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


def add_splits(
    zones: list[dict],
    state: str,
    top: int,
    bottom: int,
    splits: list[int],
    role: str = "actor-with-integrated-approved-effects",
) -> None:
    for index, (left, right) in enumerate(zip(splits, splits[1:])):
        zones.append(
            {
                "id": f"{state}-{index:02d}",
                "state": state,
                "stateFrameIndex": index,
                "selectionRegion": [left, top, right, bottom],
                "role": role,
            }
        )


def reviewed_zones() -> list[dict]:
    zones: list[dict] = [
        {
            "id": "canonical-hero-00",
            "state": "canonical-hero",
            "stateFrameIndex": 0,
            "selectionRegion": [0, 0, 230, 278],
            "additionalSelectionRegions": [[230, 0, 260, 145]],
            "role": "actor-with-integrated-bat-tail-and-ground-contact",
        }
    ]

    add_splits(zones, "idle-swagger", 0, 145, [260, 379, 503, 633, 769, 916])
    add_splits(zones, "taunt-point", 0, 145, [916, 1057, 1194, 1341, 1536], "actor-with-integrated-coin-baseball-and-violet-accents")
    add_splits(zones, "walk", 145, 278, [230, 327, 427, 530, 634, 744, 890])
    add_splits(zones, "run", 145, 278, [890, 1085, 1295, 1536], "actor-with-integrated-dust")

    add_splits(zones, "windup-punch", 278, 422, [0, 142, 287, 452, 610], "actor-with-integrated-dirty-shockwave")
    add_splits(zones, "bat-swing-heavy", 278, 422, [610, 757, 1245, 1536], "actor-with-integrated-bat-arc-rubble-and-detached-bat-impact")

    add_splits(zones, "baseball-throw", 422, 557, [0, 140, 282, 550], "actor-with-integrated-baseball-speed-streak")
    add_splits(zones, "command-summon", 422, 557, [550, 700], "actor-with-integrated-skull-command-effect")
    add_splits(zones, "curse-reveal", 422, 557, [700, 1050], "inseparable-approved-command-curse-cluster-with-violet-green-skulls")
    add_splits(zones, "minion-command", 422, 557, [1050, 1168, 1270], "actor-with-integrated-minion-hat-and-curse-motif")
    add_splits(zones, "summoned-minion", 422, 557, [1270, 1334, 1400], "standalone-summoned-minion-with-mine-motif")
    add_splits(zones, "command-finish", 422, 557, [1400, 1536], "actor-with-integrated-summoned-figures")

    add_splits(zones, "inhale-telegraph-spin", 557, 690, [0, 210, 420, 700], "actor-with-integrated-spin-arc-baseball-and-speed-streak")
    add_splits(zones, "curse-phase", 557, 690, [700, 900, 1110, 1330, 1536], "actor-with-integrated-violet-green-curse-smoke")

    add_splits(zones, "hit-react", 690, 833, [0, 165, 285, 450, 630], "actor-with-integrated-yellow-stars-and-approved-overlap")
    add_splits(zones, "armor-damage-progression", 690, 833, [630, 825, 1020, 1195, 1330, 1536], "actor-bust-with-approved-damage-state-and-violet-sparks")

    add_splits(zones, "prop-bat", 833, 935, [0, 180], "standalone-battered-spiked-bat")
    add_splits(zones, "prop-baseball", 833, 935, [180, 280], "standalone-dirty-red-stitched-baseball")
    add_splits(zones, "prop-coins", 833, 935, [280, 410], "standalone-gold-coin-stack")
    add_splits(zones, "prop-chain-padlock", 833, 935, [410, 520], "standalone-gold-chain-and-padlock")
    add_splits(zones, "defeat-recovery", 833, 935, [520, 705, 945, 1150, 1330, 1536], "actor-with-integrated-hat-bat-baseball-rubble-dust-and-defeat-effects")

    add_splits(zones, "dust-cloud", 935, 1024, [0, 38, 73, 108, 145, 183, 235], "standalone-dust-effect")
    add_splits(zones, "black-spin-arc", 935, 1024, [235, 330], "standalone-black-spin-effect")
    add_splits(zones, "yellow-stun-stars", 935, 1024, [330, 430], "standalone-yellow-star-effect")
    add_splits(zones, "dirty-debris-spray", 935, 1024, [430, 545], "standalone-dirty-debris-effect")
    add_splits(zones, "dirty-rubble-shockwave", 935, 1024, [545, 695], "standalone-dirty-rubble-shockwave")
    add_splits(zones, "violet-rubble-shockwave", 935, 1024, [695, 860], "standalone-violet-rubble-shockwave")
    add_splits(zones, "violet-curse-smoke", 935, 1024, [860, 1065], "standalone-violet-curse-smoke")
    add_splits(zones, "skull-motif", 935, 1024, [1065, 1145], "standalone-violet-green-skull-motif")
    add_splits(zones, "baseball-speed-streak", 935, 1024, [1145, 1260], "standalone-baseball-speed-streak")
    add_splits(zones, "curse-effect", 935, 1024, [1260, 1345], "standalone-violet-green-curse-effect")
    add_splits(zones, "skull-mine", 935, 1024, [1345, 1435, 1536], "standalone-violet-green-skull-mine")
    return zones


STATE_META = {
    "canonical-hero": (False, "approved large identity reference with bat and full tail"),
    "idle-swagger": (True, "approved active heavyweight idle and bat-grip progression"),
    "taunt-point": (False, "approved signature pointing and baseball/coin command sequence"),
    "walk": (True, "approved swagger walk"),
    "run": (True, "approved stomping run with dust"),
    "windup-punch": (False, "approved physical windup and dirty impact progression"),
    "bat-swing-heavy": (False, "approved sweep, overhead slam, rubble, and bat impact"),
    "baseball-throw": (False, "approved pitch and pale speed streak"),
    "command-summon": (False, "approved command gesture and skull motif"),
    "curse-reveal": (False, "approved violet-green curse reveal"),
    "minion-command": (False, "approved minion direction with detached hat and curse motifs"),
    "summoned-minion": (False, "approved summoned figures and mine motifs"),
    "command-finish": (False, "approved final pointing command with summoned figures"),
    "inhale-telegraph-spin": (False, "approved lean, black spin arc, pitch, and streak progression"),
    "curse-phase": (True, "approved smoky violet-green enraged loop"),
    "hit-react": (False, "approved hit reactions, yellow stars, and source-integrated overlap"),
    "armor-damage-progression": (False, "approved unchanged source damage-state busts"),
    "prop-bat": (False, "approved standalone battered spiked bat"),
    "prop-baseball": (False, "approved standalone baseball"),
    "prop-coins": (False, "approved standalone coin stack"),
    "prop-chain-padlock": (False, "approved standalone chain and padlock"),
    "defeat-recovery": (False, "approved stunned, prone, exhausted, and softened post-defeat progression"),
    "dust-cloud": (False, "approved standalone dust progression"),
    "black-spin-arc": (False, "approved standalone black spin arc"),
    "yellow-stun-stars": (False, "approved standalone stun stars"),
    "dirty-debris-spray": (False, "approved standalone dirty debris spray"),
    "dirty-rubble-shockwave": (False, "approved standalone physical shockwave"),
    "violet-rubble-shockwave": (False, "approved standalone cursed shockwave"),
    "violet-curse-smoke": (False, "approved standalone curse smoke"),
    "skull-motif": (False, "approved standalone skull motif"),
    "baseball-speed-streak": (False, "approved standalone baseball and streak"),
    "curse-effect": (False, "approved standalone curse symbol"),
    "skull-mine": (False, "approved standalone skull mines"),
}


REQUIRED_SEQUENCES = {
    "emerge": {
        "classification": "EXISTS - COMPLETE",
        "orderedFrames": [
            "curse-effect-00", "skull-motif-00", "curse-phase-03", "curse-phase-02",
            "curse-phase-01", "curse-phase-00", "curse-reveal-00", "command-summon-00",
            "idle-swagger-00",
        ],
        "startState": "approved detached violet-green curse symbol",
        "intermediateMotion": "approved skull motif, curse smoke, materialized cursed body, command pose, and settling gesture",
        "endState": "idle-swagger-00 active heavyweight stance",
        "continuity": "approved curse vocabulary materializes the exact boss and resolves to active idle",
        "loop": False,
    },
    "retreat": {
        "classification": "EXISTS - COMPLETE",
        "orderedFrames": [
            "idle-swagger-00", "command-summon-00", "curse-reveal-00",
            "curse-phase-00", "curse-phase-01", "curse-phase-02", "curse-phase-03",
            "skull-motif-00", "curse-effect-00",
        ],
        "startState": "idle-swagger-00 active heavyweight stance",
        "intermediateMotion": "intentional approved command and curse withdrawal without hit, fall, or exhaustion frames",
        "endState": "approved detached violet-green curse symbol inactive/exit state",
        "continuity": "active boss intentionally withdraws through reversible canonical curse vocabulary",
        "loop": False,
    },
    "defeat": {
        "classification": "EXISTS - COMPLETE",
        "orderedFrames": [
            "hit-react-00", "hit-react-01", "hit-react-02", "hit-react-03",
            "defeat-recovery-00", "defeat-recovery-01", "defeat-recovery-02",
            "defeat-recovery-03", "defeat-recovery-04",
        ],
        "startState": "approved hit reaction with yellow stars",
        "intermediateMotion": "approved stagger, collapse, prone hold, rubble settling, kneel, and exhausted recovery",
        "endState": "approved softened seated Diamond Don, visibly identifiable with hat, clothing, tail, accessories, baseball material, and separated equipment",
        "continuity": "approved loss progression ends on the exact living identifiable boss without gore or invented damage",
        "loop": False,
    },
}


def states_from_zones(zones: list[dict]) -> list[dict]:
    order: list[str] = []
    grouped: dict[str, list[str]] = {}
    for zone in zones:
        if zone["state"] not in grouped:
            order.append(zone["state"])
            grouped[zone["state"]] = []
        grouped[zone["state"]].append(zone["id"])
    return [
        {
            "id": state,
            "orderedFrames": grouped[state],
            "frameCount": len(grouped[state]),
            "loop": STATE_META[state][0],
            "progression": STATE_META[state][1],
            "timing": {
                "basis": "approved-source-order",
                "durationMs": None,
                "status": "UNSET / NOT PROMOTED; runtime timing intentionally not invented",
            },
        }
        for state in order
    ]


def assign_visible_pixels(source: Image.Image, zones: list[dict]) -> dict[str, list[int]]:
    width, height = source.size
    alpha = source.getchannel("A").tobytes()
    owner = [-1] * (width * height)
    assignments = {zone["id"]: [] for zone in zones}
    for zone_index, zone in enumerate(zones):
        for left, top, right, bottom in [zone["selectionRegion"], *zone.get("additionalSelectionRegions", [])]:
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
    xs: list[int] = []
    ys: list[int] = []
    for point in points:
        y, x = divmod(point, width)
        xs.append(x)
        ys.append(y)
    return min(xs), min(ys), max(xs) + 1, max(ys) + 1


def largest_component_bbox(image: Image.Image) -> tuple[int, int, int, int]:
    width, height = image.size
    visible = bytearray(1 if value else 0 for value in image.getchannel("A").tobytes())
    visited = bytearray(width * height)
    largest: tuple[int, tuple[int, int, int, int]] | None = None
    for start, is_visible in enumerate(visible):
        if not is_visible or visited[start]:
            continue
        stack = [start]
        visited[start] = 1
        count = 0
        min_x = min_y = 1 << 30
        max_x = max_y = 0
        while stack:
            point = stack.pop()
            y, x = divmod(point, width)
            count += 1
            min_x, min_y = min(min_x, x), min(min_y, y)
            max_x, max_y = max(max_x, x), max(max_y, y)
            for ny in range(max(0, y - 1), min(height - 1, y + 1) + 1):
                for nx in range(max(0, x - 1), min(width - 1, x + 1) + 1):
                    neighbor = ny * width + nx
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
    if zone["role"].startswith("standalone"):
        return "complete-envelope-bottom-center", [round((bbox[0] + bbox[2] - 1) / 2), bbox[3] - 1]
    body = largest_component_bbox(frame)
    return "largest-owned-component-ground-contact", [round((body[0] + body[2] - 1) / 2), body[3] - 1]


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
    return """# Diamond Don Immutable Generation Specification

Execution: `EXECUTE: boss-diamond-don`  
Contract: `docs/design/trash-dash/docs/game/bosses/BOSSFIX.md`, reread in full immediately before execution  
Specification status: immutable for this execution batch

## Identity

- Boss: The Diamond Don (`boss.level-06-secret.diamond-don`).
- Canonical visual authority: `docs/design/trash-dash/reference/characters/level-06/sprites/boss-diamond-don.png`.
- Accepted extraction source: `docs/design/trash-dash/character-animation/phase-05-codex-integration/phase-04-bosses/final/boss-diamond-don-transparent.png`.
- Locked: towering upright heavyweight charcoal/deep-gray raccoon; black mask; lighter muzzle and cheeks; pale yellow-green reflective eyes; broad black nose; enormous ringed tail; low black fedora/trilby; dirty off-white/gray pinstriped baseball shirt; distressed ambiguous `06`; charcoal armor; layered belts, brown straps, gold buckles/chains; armored gloves; dark trousers; black boots; battered reinforced spiked dark-brown wooden bat; huge forearms, round belly, short powerful legs, wide plantigrade stance; smug controlled theatrical kingpin affect.
- Locked effects: dirty gray-brown shockwaves/rubble, black arcs, pale baseball streaks, yellow stars, smoky violet curse with acid-green accents, skull motifs, subtle green gauntlet indicators, approved baseballs/coins/chains/padlock/dust/mines/minions/hat/bat/detached props/defeat effects.

## Animation

- EMERGE: 9 approved-only references; detached curse symbol -> skull motif -> curse smoke/body materialization -> command settle -> active idle.
- RETREAT: 9 approved-only references; active idle -> intentional command -> curse dematerialization -> detached inactive/exit symbol. No hit, fall, prone, or exhaustion art is used.
- DEFEAT: 9 approved-only references; hit/stagger -> collapse -> prone hold -> rubble settling -> exhausted softened seated post-defeat boss.
- All three classify `EXISTS - COMPLETE`; generation and replacement counts are zero.
- Runtime timing is `UNSET / NOT PROMOTED`; 150 ms GIF cadence is review-only and not gameplay metadata.

## Rendering

- Preserve perspective, scale, lighting, shading, texture, palette, alpha, body/prop relationships, and source order exactly.
- Source/output pixel scale is 1:1. No resize, resampling, rotation, redraw, retouch, cleanup, filtering, or style conversion.
- Output is transparent RGBA with manifest-defined variable rectangles, two pixels of transparent frame padding, and eight transparent atlas-gutter pixels on every side.
- Actor pivots use the largest owned connected component's bottom center; standalone effects/props use the complete visible envelope's bottom center.
- Reviewed rectangular ownership partitions resolve crowded source rows and the right-edge contact while assigning every visible source RGBA pixel exactly once.

## Restrictions and generation scope

- Every physical item is `PRESERVE EXACTLY - REPOSITION FOR ISOLATION`.
- `GENERATE NEW = 0`; `REPLACE UNAPPROVED = 0`.
- Do not add ordinary proportions, a slender body/small tail, clean white suit, crown, cigar, firearm, gold bat, replacement sleeve number, blue/red replacement magic, mascot affect, weapons, anatomy, markings, costume, or damage.
- Do not promote, register, or copy any output into `assets/runtime/`.
"""


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    FRAMES_OUT.mkdir(parents=True, exist_ok=True)
    PREVIEWS_OUT.mkdir(parents=True, exist_ok=True)

    for path in (SOURCE, CANON, ATTACHED_COPY):
        if not path.is_file():
            raise RuntimeError(f"required approved source input is missing: {path}")
    if file_sha(SOURCE) != SOURCE_SHA256 or file_sha(ATTACHED_COPY) != SOURCE_SHA256:
        raise RuntimeError("accepted atlas or attached copy changed")
    if file_sha(CANON) != CANON_SHA256:
        raise RuntimeError("canonical visual authority changed")

    source = Image.open(SOURCE).convert("RGBA")
    canonical = Image.open(CANON)
    if source.size != SOURCE_SIZE or canonical.size != CANON_SIZE:
        raise RuntimeError("approved input dimensions changed")
    if set(source.getchannel("A").tobytes()) != {0, 255}:
        raise RuntimeError("accepted atlas must contain binary alpha only")

    zones = reviewed_zones()
    states = states_from_zones(zones)
    assignments = assign_visible_pixels(source, zones)
    frame_order = [frame_id for state in states for frame_id in state["orderedFrames"]]
    source_visible_count = sum(1 for alpha in source.getchannel("A").tobytes() if alpha)
    if sum(len(assignments[frame_id]) for frame_id in frame_order) != source_visible_count:
        raise RuntimeError("visible source coverage is not exactly one-to-one")

    source_bytes = source.tobytes()
    zone_by_id = {zone["id"]: zone for zone in zones}
    images: dict[str, Image.Image] = {}
    records: dict[str, dict] = {}
    for frame_id in frame_order:
        zone = zone_by_id[frame_id]
        owned = assignments[frame_id]
        visible_box = pixels_bbox(owned, source.width)
        frame = Image.new(
            "RGBA",
            (visible_box[2] - visible_box[0] + FRAME_PAD * 2, visible_box[3] - visible_box[1] + FRAME_PAD * 2),
            (0, 0, 0, 0),
        )
        frame_pixels = frame.load()
        for point in owned:
            source_y, source_x = divmod(point, source.width)
            offset = point * 4
            frame_pixels[source_x - visible_box[0] + FRAME_PAD, source_y - visible_box[1] + FRAME_PAD] = tuple(source_bytes[offset : offset + 4])
        bbox = frame.getchannel("A").getbbox()
        if bbox is None or bbox[0] <= 0 or bbox[1] <= 0 or bbox[2] >= frame.width or bbox[3] >= frame.height:
            raise RuntimeError(f"visible pixel touches extracted frame boundary: {frame_id}")
        pivot_type, pivot = frame_anchor(zone, frame)
        destination = FRAMES_OUT / f"{frame_id}.png"
        images[frame_id] = frame
        records[frame_id] = {
            "state": zone["state"],
            "stateFrameIndex": zone["stateFrameIndex"],
            "classification": "PRESERVE EXACTLY - REPOSITION FOR ISOLATION",
            "sourceOwnershipSelectionRegion": zone["selectionRegion"],
            "sourceOwnershipAdditionalSelectionRegions": zone.get("additionalSelectionRegions", []),
            "sourceVisibleBounds": list(visible_box),
            "frameFile": str(destination.relative_to(OUTPUT)),
            "frameSize": list(frame.size),
            "visibleBoundsInFrame": list(bbox),
            "transparentFramePaddingPixels": FRAME_PAD,
            "sourceToFrameOffset": [FRAME_PAD - visible_box[0], FRAME_PAD - visible_box[1]],
            "pivotType": pivot_type,
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

    # Bossfix stages 3 and 4 are written before physical frame/atlas assembly.
    SPEC_OUT.write_text(immutable_specification())
    audit = {
        "boss": "The Diamond Don",
        "canonId": "boss.level-06-secret.diamond-don",
        "canonicalBoard": {
            "path": str(CANON.relative_to(ROOT)),
            "sha256": file_sha(CANON),
            "size": list(canonical.size),
            "mode": canonical.mode,
        },
        "acceptedTransparentAtlas": {
            "path": str(SOURCE.relative_to(ROOT)),
            "sha256": file_sha(SOURCE),
            "attachedCopySha256": file_sha(ATTACHED_COPY),
            "size": list(source.size),
            "mode": "RGBA",
            "visibleBounds": list(source.getchannel("A").getbbox()),
            "visiblePixelCount": source_visible_count,
            "opaquePixelCount": source_visible_count,
            "transparentPixelCount": source.width * source.height - source_visible_count,
            "partialAlphaPixelCount": 0,
        },
        "sequenceAudit": REQUIRED_SEQUENCES,
        "defects": {
            "missingOrIncompleteAnimations": False,
            "crossFrameSpriteOrEffectOverlap": True,
            "neighboringFrameBleedRisk": True,
            "visiblePixelsTouchingAcceptedAtlasBoundary": True,
            "ambiguousBatOwnershipBeforeManifest": True,
            "ambiguousBaseballOwnershipBeforeManifest": True,
            "ambiguousRubbleShockwaveOwnershipBeforeManifest": True,
            "ambiguousCurseSkullMineMinionOwnershipBeforeManifest": True,
            "ambiguousCoinChainStarDustHatAndDetachedPropOwnershipBeforeManifest": True,
            "insufficientTransparentGutters": True,
            "missingEmergeFrames": False,
            "missingRetreatFrames": False,
            "missingDefeatFrames": False,
        },
        "resolution": "approved-only sequence composition plus reviewed rectangular ownership extraction and variable-cell repack; no artwork generation",
    }
    AUDIT_OUT.write_text(json.dumps(audit, indent=2) + "\n")
    batch_manifest = {
        "boss": "The Diamond Don",
        "execution": "EXECUTE: boss-diamond-don",
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

    for stale in FRAMES_OUT.glob("*.png"):
        stale.unlink()
    for stale in PREVIEWS_OUT.glob("*.gif"):
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
        draw.text(
            (x + 1, y),
            f"{index:03d} {placement['id']}",
            fill=(255, 255, 255, 255),
            font=font,
            stroke_width=1,
            stroke_fill=(0, 0, 0, 255),
        )
    contact.save(CONTACT_OUT, format="PNG", compress_level=9, optimize=False)

    for sequence_name, sequence in REQUIRED_SEQUENCES.items():
        render_preview(sequence_name, sequence["orderedFrames"], images, records)

    manifest = {
        "assetName": "boss-diamond-don-isolated",
        "canonId": "boss.level-06-secret.diamond-don",
        "status": "artwork-approved",
        "approval": {
            "status": "ARTWORK APPROVED",
            "approvedBy": "project-owner",
            "approvedOn": "2026-08-13",
            "scope": "Level 6 Diamond Don isolated artwork package, manifest-defined rectangles, and approved-only EMERGE, RETREAT, and DEFEAT sequences",
            "runtimePromotionAuthorized": False,
        },
        "canonicalFacing": "screen-right where directional",
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
            "readingOrder": "physical state order then approved source order",
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
            "aiGenerationUsed": False,
            "resizingUsed": False,
            "redrawingUsed": False,
            "retouchingUsed": False,
            "filteringUsed": False,
            "rotationUsed": False,
            "runtimePromotionUsed": False,
            "rebuildCommand": "python3 tools/asset_pipeline/build_boss_diamond_don_isolated.py",
            "verifyCommand": "python3 tools/verify/check_boss_diamond_don_isolated.py",
        },
    }
    MANIFEST_OUT.write_text(json.dumps(manifest, indent=2) + "\n")
    APPROVAL_OUT.write_text(
        "# Diamond Don Artwork Approval\n\n"
        "Status: **ARTWORK APPROVED**\n\n"
        "The project owner approved the Level 6 Diamond Don isolated artwork package on 2026-08-13. "
        "Approval covers the complete transparent sheet, 78 extracted frames/support sprites, manifest-defined "
        "variable rectangles and pivots, boundary-labeled contact sheet, and approved-only EMERGE, RETREAT, "
        "and DEFEAT sequences.\n\n"
        "No artwork was generated, replaced, redrawn, resized, retouched, filtered, rotated, or promoted. "
        "Runtime registration, timing, collision, gameplay integration, traversal, target-resolution capture, "
        "and V2 runtime release remain unauthorized.\n"
    )
    REPORT_OUT.write_text(
        "# Diamond Don Bossfix Validation\n\n"
        "Status: `PENDING INDEPENDENT VERIFICATION`\n\n"
        "Run `python3 tools/verify/check_boss_diamond_don_isolated.py` to populate the seven-test result.\n"
    )
    print(f"wrote {len(records)} isolated approved frames/support sprites")
    print(f"atlas {atlas.width}x{atlas.height}; visible pixels {source_visible_count} assigned exactly once")
    print("artwork generated: 0; artwork replaced: 0; runtime promotion: 0")
    print("ARTWORK APPROVED - RUNTIME PROMOTION NOT AUTHORIZED")


if __name__ == "__main__":
    main()
