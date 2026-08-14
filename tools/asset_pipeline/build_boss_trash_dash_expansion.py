#!/usr/bin/env python3
"""Build the canon-locked Trash Dash boss animation expansion."""

from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE_ATLAS = Path("/Users/jamesschmittler/Desktop/boss-trash-dash-transparent.png")
CANON_BOARD = ROOT / "docs/design/trash-dash/reference/characters/level-01/sprites/boss-trash-dash.png"
BOSS_BIBLE = ROOT / "docs/design/trash-dash/docs/game/bosses/README.md"
BOSS_CANON = ROOT / "docs/design/trash-dash/docs/game/bosses/TRASH_DASH.md"
OUTPUT_DIR = ROOT / "assets/generated/boss-trash-dash-expansion"
OUTPUT_CELLS = OUTPUT_DIR / "cells"
OUTPUT_SHEET = OUTPUT_DIR / "boss-trash-dash-expanded.png"
OUTPUT_MANIFEST = OUTPUT_DIR / "manifest.json"

ORIGINAL_SIZE = (1536, 1024)
EXPANDED_SIZE = (1536, 1280)
CELL_SIZE = 128
SOURCE_TOP = 960
SOURCE_BASELINE = 1072
CELL_BASELINE = 112

# Each entry declares the authored 128px lane origin plus the tight canonical
# action rectangle inside the presentation board. The rectangle removes only
# labels, dividers, and neighboring poses; placement remains relative to its
# original lane origin, so registration is not independently centered.
FRAME_SPECS = {
    "emerge_01": {"lane": (650, SOURCE_TOP), "include": (672, 1014, 738, 1073)},
    "emerge_02": {"lane": (735, SOURCE_TOP), "include": (744, 1005, 824, 1073)},
    "emerge_03": {"lane": (820, SOURCE_TOP), "include": (832, 1002, 924, 1073)},
    "retreat_01": {"lane": (930, SOURCE_TOP), "include": (948, 1034, 1028, 1073)},
    "retreat_02": {"lane": (1025, SOURCE_TOP), "include": (1038, 1037, 1107, 1073)},
    "retreat_03": {"lane": (1115, SOURCE_TOP), "include": (1132, 1040, 1212, 1073)},
    "defeat_01": {"lane": (0, SOURCE_TOP), "include": (24, 990, 126, 1073)},
    "defeat_02": {"lane": (110, SOURCE_TOP), "include": (126, 997, 224, 1073)},
    "defeat_03": {"lane": (220, SOURCE_TOP), "include": (232, 995, 326, 1073)},
    "defeat_04": {"lane": (325, SOURCE_TOP), "include": (337, 987, 412, 1073)},
    "defeat_05": {"lane": (410, SOURCE_TOP), "include": (419, 993, 508, 1073)},
    "defeat_06": {"lane": (500, SOURCE_TOP), "include": (510, 986, 577, 1073)},
    "defeat_07": {"lane": (575, SOURCE_TOP), "include": (580, 1000, 657, 1073)},
}

DESTINATIONS = {
    "emerge_01": (0, 1024),
    "emerge_02": (128, 1024),
    "emerge_03": (256, 1024),
    "retreat_01": (384, 1024),
    "retreat_02": (512, 1024),
    "retreat_03": (640, 1024),
    "defeat_01": (0, 1152),
    "defeat_02": (128, 1152),
    "defeat_03": (256, 1152),
    "defeat_04": (384, 1152),
    "defeat_05": (512, 1152),
    "defeat_06": (640, 1152),
    "defeat_07": (768, 1152),
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def components(mask: np.ndarray) -> list[list[tuple[int, int]]]:
    height, width = mask.shape
    visited = np.zeros_like(mask, dtype=bool)
    groups: list[list[tuple[int, int]]] = []
    for y in range(height):
        for x in range(width):
            if not mask[y, x] or visited[y, x]:
                continue
            queue = deque([(y, x)])
            visited[y, x] = True
            points: list[tuple[int, int]] = []
            while queue:
                cy, cx = queue.popleft()
                points.append((cy, cx))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if (
                        0 <= ny < height
                        and 0 <= nx < width
                        and mask[ny, nx]
                        and not visited[ny, nx]
                    ):
                        visited[ny, nx] = True
                        queue.append((ny, nx))
            groups.append(points)
    return groups


def dilate(mask: np.ndarray) -> np.ndarray:
    padded = np.pad(mask, 1)
    return np.logical_or.reduce(
        [
            padded[dy : dy + mask.shape[0], dx : dx + mask.shape[1]]
            for dy in range(3)
            for dx in range(3)
        ]
    )


def erode(mask: np.ndarray) -> np.ndarray:
    padded = np.pad(mask, 1, constant_values=True)
    return np.logical_and.reduce(
        [
            padded[dy : dy + mask.shape[0], dx : dx + mask.shape[1]]
            for dy in range(3)
            for dx in range(3)
        ]
    )


def extract_native_cell(
    board: np.ndarray,
    source_x: int,
    source_y: int,
    include: tuple[int, int, int, int],
) -> Image.Image:
    rgb = board[source_y : source_y + CELL_SIZE, source_x : source_x + CELL_SIZE].copy()
    # The board matte is neutral gray and contiguous with the crop boundary.
    # Flood only those neutral pixels from the outer edge. The boss/effects are
    # enclosed by their canonical dark outline or are chromatic, so their exact
    # RGB pixels remain untouched even when interior sack values are also gray.
    channel_spread = rgb.max(axis=2).astype(int) - rgb.min(axis=2).astype(int)
    brightness = rgb.mean(axis=2)
    neutral_matte = (channel_spread <= 10) & (brightness >= 55) & (brightness <= 175)
    # Seal single-pixel antialias gaps before the flood, preventing the neutral
    # matte from leaking into valid enclosed slate-gray sack interiors.
    visual_barrier = dilate(~neutral_matte)
    floodable = ~visual_barrier
    background = np.zeros(neutral_matte.shape, dtype=bool)
    queue: deque[tuple[int, int]] = deque()
    for x in range(CELL_SIZE):
        for y in (0, CELL_SIZE - 1):
            if floodable[y, x] and not background[y, x]:
                background[y, x] = True
                queue.append((y, x))
    for y in range(CELL_SIZE):
        for x in (0, CELL_SIZE - 1):
            if floodable[y, x] and not background[y, x]:
                background[y, x] = True
                queue.append((y, x))
    while queue:
        y, x = queue.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if (
                0 <= ny < CELL_SIZE
                and 0 <= nx < CELL_SIZE
                and floodable[ny, nx]
                and not background[ny, nx]
            ):
                background[ny, nx] = True
                queue.append((ny, nx))
    # Contract the temporary seal back to the original contour envelope.
    candidate = erode(~background)

    retained = candidate.copy()
    include_left, include_top, include_right, include_bottom = include
    local_left = include_left - source_x
    local_top = include_top - source_y
    local_right = include_right - source_x
    local_bottom = include_bottom - source_y
    allowed = np.zeros_like(retained)
    allowed[local_top:local_bottom, local_left:local_right] = True
    retained &= allowed
    # Retain art connected to the authored ground band. Preserve approved detached
    # chartreuse droplets/debris when they are clearly non-neutral action pixels.
    cleaned = np.zeros_like(retained)
    for group in components(retained):
        ys = np.array([point[0] for point in group])
        xs = np.array([point[1] for point in group])
        colors = rgb[ys, xs].astype(int)
        chroma = (colors.max(axis=1) - colors.min(axis=1)).mean()
        grounded = ys.max() >= CELL_BASELINE - 4
        approved_detached = len(group) >= 2 and chroma >= 18 and ys.min() >= 42
        if len(group) >= 2 and (grounded or approved_detached):
            for y, x in group:
                cleaned[y, x] = True
    retained = cleaned
    retained[:, :1] = False
    retained[:, -1:] = False
    alpha = (retained * 255).astype(np.uint8)
    return Image.fromarray(np.dstack([rgb, alpha]), "RGBA")


def visible_bounds(cell: Image.Image) -> list[int]:
    box = cell.getchannel("A").getbbox()
    if box is None:
        raise RuntimeError("Canonical extraction produced an empty frame")
    return [box[0], box[1], box[2] - box[0], box[3] - box[1]]


def main() -> None:
    OUTPUT_CELLS.mkdir(parents=True, exist_ok=True)
    source = Image.open(SOURCE_ATLAS).convert("RGBA")
    if source.size != ORIGINAL_SIZE:
        raise RuntimeError(f"Unexpected approved atlas size: {source.size}")
    board = np.array(Image.open(CANON_BOARD).convert("RGB"))

    expanded = Image.new("RGBA", EXPANDED_SIZE, (0, 0, 0, 0))
    # Unmasked paste preserves all RGBA bytes, including hidden RGB beneath alpha 0.
    expanded.paste(source, (0, 0))

    frames: dict[str, dict[str, object]] = {}
    for name, spec in FRAME_SPECS.items():
        source_x, source_y = spec["lane"]
        include = spec["include"]
        cell = extract_native_cell(board, source_x, source_y, include)
        cell_path = OUTPUT_CELLS / f"{name}.png"
        cell.save(cell_path, optimize=False)
        destination = DESTINATIONS[name]
        expanded.paste(cell, destination, cell)
        frames[name] = {
            "canonicalSourceRect": [source_x, source_y, CELL_SIZE, CELL_SIZE],
            "canonicalIncludedArtRect": list(include),
            "sheetRect": [destination[0], destination[1], CELL_SIZE, CELL_SIZE],
            "derivedCell": str(cell_path.relative_to(ROOT)),
            "visibleBounds": visible_bounds(cell),
            "pivot": [source_x + CELL_SIZE // 2, SOURCE_BASELINE],
            "groundBaselineInCell": CELL_BASELINE,
            "scaleApplied": 1,
            "horizontalRegistration": "preserved_from_canonical_source_lane",
        }

    expanded.save(OUTPUT_SHEET, optimize=False)
    if expanded.crop((0, 0, *ORIGINAL_SIZE)).tobytes() != source.tobytes():
        raise RuntimeError("PRESERVE EXACTLY validation failed")

    manifest = {
        "assetName": "boss-trash-dash-canon-repair",
        "canonId": "boss.level-01.trash-dash",
        "status": "generated-awaiting-user-approval",
        "sourcePath": str(SOURCE_ATLAS),
        "canonicalVisualAuthority": str(CANON_BOARD.relative_to(ROOT)),
        "canonicalBossBible": str(BOSS_BIBLE.relative_to(ROOT)),
        "canonicalBossFile": str(BOSS_CANON.relative_to(ROOT)),
        "sourceSha256": sha256(SOURCE_ATLAS),
        "canonicalVisualSha256": sha256(CANON_BOARD),
        "originalSheetSize": list(ORIGINAL_SIZE),
        "expandedSheetSize": list(EXPANDED_SIZE),
        "preserveExactlyRect": [0, 0, *ORIGINAL_SIZE],
        "cellSize": [CELL_SIZE, CELL_SIZE],
        "canonicalFacing": "right",
        "sourcePixelScale": 1,
        "runtimeScale": 1,
        "anchor": "canonical_source_ground_baseline",
        "alpha": "binary-transparent",
        "sampling": "nearest-neighbor",
        "readingOrder": "manifest-defined_left_to_right",
        "frames": frames,
        "states": {
            "emerge": {
                "orderedFrames": ["emerge_01", "emerge_02", "emerge_03"],
                "fps": 8,
                "loop": False,
                "interruptible": False,
                "completion": "transition_to_idle",
            },
            "retreat": {
                "orderedFrames": ["retreat_01", "retreat_02", "retreat_03"],
                "fps": 8,
                "loop": False,
                "interruptible": False,
                "completion": "hold_hidden_inactive",
            },
            "defeat": {
                "orderedFrames": [f"defeat_{index:02d}" for index in range(1, 8)],
                "fps": 10,
                "loop": False,
                "interruptible": False,
                "completion": "hold_canonical_refuse_heap_and_release_arena",
            },
        },
        "collisionPolicy": "independent_state_data_not_alpha_bounds",
        "runtimePromotion": "not_performed",
        "provenance": {
            "method": "native-size deterministic background-to-alpha separation from approved canonical board",
            "aiGenerationUsed": False,
            "resizingUsed": False,
            "independentCenteringUsed": False,
            "edgeRepaintingUsed": False,
            "rebuildCommand": "python3 tools/asset_pipeline/build_boss_trash_dash_expansion.py",
        },
    }
    OUTPUT_MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n")
    print(OUTPUT_SHEET)
    print(OUTPUT_MANIFEST)


if __name__ == "__main__":
    main()
