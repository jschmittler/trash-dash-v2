#!/usr/bin/env python3
"""Build and validate Secret Level 6 parallax PNGs from independent masters."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SET = ROOT / "assets/generated/level6-parallax"
SOURCES = SET / "sources"
PROCESSED = SET / "processed"
QA = SET / "qa/composites"
TARGET = (1320, 540)
CAMERA = (960, 540)
STAGES = (
    "entryway",
    "concessions",
    "stadium-seats",
    "outfield",
    "infield-boss-arena",
)
LAYERS = ("far", "middle", "close")
CHROMA = (255, 0, 255)


def contain_nearest(source: Image.Image) -> Image.Image:
    """Center a source without distortion, using nearest-neighbor resampling only."""
    source = source.convert("RGBA")
    scale = min(TARGET[0] / source.width, TARGET[1] / source.height)
    size = (round(source.width * scale), round(source.height * scale))
    resized = source.resize(size, Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", TARGET, (0, 0, 0, 0))
    offset = ((TARGET[0] - size[0]) // 2, (TARGET[1] - size[1]) // 2)
    canvas.alpha_composite(resized, offset)
    return canvas


def binary_key(image: Image.Image) -> Image.Image:
    """Remove generated #FF00FF plus a conservative four-pixel matte fringe."""
    pixels = image.load()
    keyed: set[tuple[int, int]] = set()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]
            is_key = (
                not a
                or (r >= 185 and b >= 150 and g <= 115 and r >= g * 1.55 and b >= g * 1.35)
            )
            if is_key:
                keyed.add((x, y))
                pixels[x, y] = (0, 0, 0, 0)
            else:
                pixels[x, y] = (r, g, b, 255)

    frontier = set(keyed)
    for _ in range(4):
        remove: set[tuple[int, int]] = set()
        for x, y in frontier:
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if not (0 <= nx < image.width and 0 <= ny < image.height):
                    continue
                if (nx, ny) in keyed:
                    continue
                r, g, b, a = pixels[nx, ny]
                magenta_fringe = (
                    a
                    and r >= 70
                    and b >= 70
                    and g <= 105
                    and max(r, b) >= g * 1.45
                    and abs(r - b) <= 120
                )
                if magenta_fringe:
                    remove.add((nx, ny))
        for x, y in remove:
            pixels[x, y] = (0, 0, 0, 0)
        keyed.update(remove)
        frontier = remove

    # Despill any remaining purple/magenta-dominant contour colors without
    # softening or changing alpha. Work outward from transparent pixels only.
    frontier = set(keyed)
    visited = set(keyed)
    for _ in range(3):
        next_frontier: set[tuple[int, int]] = set()
        for x, y in frontier:
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if not (0 <= nx < image.width and 0 <= ny < image.height):
                    continue
                if (nx, ny) in visited:
                    continue
                r, g, b, a = pixels[nx, ny]
                if not a:
                    continue
                magenta_dominant = r >= 35 and b >= 45 and g * 1.25 <= max(r, b)
                if magenta_dominant:
                    pixels[nx, ny] = (min(r, g + 5), g, min(b, max(g + 22, 48)), 255)
                visited.add((nx, ny))
                next_frontier.add((nx, ny))
        frontier = next_frontier
    return image


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def analyze(stage: str, layer: str, source: Path, output: Path, image: Image.Image) -> dict:
    alpha = image.getchannel("A")
    histogram = alpha.histogram()
    transparent = histogram[0]
    opaque = histogram[255]
    partial = sum(histogram[1:255])
    visible_chroma = sum(
        1
        for r, g, b, a in image.get_flattened_data()
        if a and r >= 185 and b >= 150 and g <= 115 and r >= g * 1.55 and b >= g * 1.35
    )
    return {
        "stage": stage,
        "layer": layer,
        "source": str(source.relative_to(ROOT)),
        "source_sha256": sha256(source),
        "output": str(output.relative_to(ROOT)),
        "dimensions": list(image.size),
        "sha256": sha256(output),
        "alpha_values": sorted(set(alpha.get_flattened_data())),
        "opaque_pixels": opaque,
        "transparent_pixels": transparent,
        "partial_alpha_pixels": partial,
        "opaque_coverage": round(opaque / (TARGET[0] * TARGET[1]), 6),
        "transparency_percentage": round(transparent * 100 / (TARGET[0] * TARGET[1]), 3),
        "visible_chroma_pixels": visible_chroma,
    }


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    records: list[dict] = []
    composites: list[dict] = []

    for stage in STAGES:
        layers: dict[str, Image.Image] = {}
        for layer in LAYERS:
            source = SOURCES / f"level6-{stage}-{layer}-source.png"
            output = PROCESSED / f"level6-{stage}-{layer}.png"
            image = contain_nearest(Image.open(source))
            if layer == "far":
                sample_x = min(max((TARGET[0] - image.getbbox()[2]) // 2, 0), TARGET[0] - 1) if image.getbbox() else 0
                fill = image.getpixel((sample_x, 0))[:3]
                background = Image.new("RGBA", TARGET, (*fill, 255))
                background.alpha_composite(image)
                image = background
            else:
                image = binary_key(image)
            image.save(output, optimize=True)
            records.append(analyze(stage, layer, source, output, image))
            layers[layer] = image

        composite = layers["far"].copy()
        composite.alpha_composite(layers["middle"])
        composite.alpha_composite(layers["close"])
        left = (TARGET[0] - CAMERA[0]) // 2
        composite_path = QA / f"{stage}-960x540.png"
        composite.crop((left, 0, left + CAMERA[0], CAMERA[1])).save(composite_path, optimize=True)
        composites.append(
            {
                "stage": stage,
                "output": str(composite_path.relative_to(ROOT)),
                "dimensions": list(CAMERA),
                "sha256": sha256(composite_path),
            }
        )

    failures: list[str] = []
    if len(records) != 15:
        failures.append(f"expected 15 processed records, found {len(records)}")
    if len(composites) != 5:
        failures.append(f"expected 5 composites, found {len(composites)}")
    for record in records:
        label = record["output"]
        if record["dimensions"] != list(TARGET):
            failures.append(f"bad dimensions: {label}")
        if record["partial_alpha_pixels"]:
            failures.append(f"partial alpha: {label}")
        if record["layer"] == "far":
            if record["transparent_pixels"] or record["alpha_values"] != [255]:
                failures.append(f"far not fully opaque: {label}")
        else:
            if any(value not in (0, 255) for value in record["alpha_values"]):
                failures.append(f"moving layer alpha not binary: {label}")
            if record["visible_chroma_pixels"]:
                failures.append(f"visible chroma: {label}")
        if record["layer"] == "close" and record["transparency_percentage"] < 75:
            failures.append(f"close transparency below 75%: {label}")

    report = {
        "schema_version": 1,
        "status": "asset-stage-validated" if not failures else "asset-stage-failed",
        "runtime_size": list(TARGET),
        "camera_size": list(CAMERA),
        "stage_ids": {"source": "manifest-derived", "values": list(STAGES)},
        "parallax_speeds": {"far": 0.018, "middle": 0.055, "close": 0.13},
        "processing": "centered aspect-preserving nearest-neighbor contain; local #FF00FF removal; four-pixel conservative boundary contraction; three-pixel navy boundary despill; strict binary alpha",
        "records": records,
        "composites": composites,
        "failures": failures,
    }
    (SET / "validation-report.json").write_text(json.dumps(report, indent=2) + "\n")
    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    main()
