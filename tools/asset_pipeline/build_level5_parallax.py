#!/usr/bin/env python3
"""Build and validate Level 5 parallax PNGs from independent source generations."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SET = ROOT / "assets/generated/level5-parallax"
SOURCES = SET / "sources"
PROCESSED = SET / "processed"
QA = SET / "qa/composites"
TARGET = (1320, 540)
STAGES = (
    "low-earth-orbit",
    "satellite-graveyard",
    "nebula-asteroid-mine",
    "abandoned-alien-station",
    "intergalactic-junk-world",
)


def contain_nearest(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    scale = min(TARGET[0] / image.width, TARGET[1] / image.height)
    size = (round(image.width * scale), round(image.height * scale))
    resized = image.resize(size, Image.Resampling.NEAREST)
    canvas = Image.new("RGBA", TARGET, (0, 0, 0, 0))
    canvas.alpha_composite(resized, ((TARGET[0] - size[0]) // 2, (TARGET[1] - size[1]) // 2))
    return canvas


def binary_key(image: Image.Image) -> Image.Image:
    px = image.load()
    keyed = set()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, _ = px[x, y]
            # Generated plates use a flat saturated magenta key with small edge variation.
            is_key = r >= 190 and b >= 150 and g <= 105 and r >= g * 1.7 and b >= g * 1.45
            if is_key:
                keyed.add((x, y))
                px[x, y] = (0, 0, 0, 0)
            else:
                px[x, y] = (r, g, b, 255)

    # Remove only magenta-dominant matte pixels directly touching the keyed field.
    # This contracts the generated antialiased fringe without eroding navy contours.
    frontier = keyed
    for _ in range(2):
        remove = set()
        for x, y in frontier:
            for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
                if not (0 <= nx < image.width and 0 <= ny < image.height) or (nx, ny) in keyed:
                    continue
                r, g, b, a = px[nx, ny]
                magenta_matte = a and r >= 70 and b >= 70 and g <= 90 and abs(r - b) <= 105 and max(r, b) >= g * 1.65
                if magenta_matte:
                    remove.add((nx, ny))
        for point in remove:
            px[point[0], point[1]] = (0, 0, 0, 0)
        keyed.update(remove)
        frontier = remove
    return image


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    QA.mkdir(parents=True, exist_ok=True)
    records = []
    for stage in STAGES:
        layers = {}
        for layer in ("far", "middle", "close"):
            source = SOURCES / f"level5-{stage}-{layer}-source.png"
            output = PROCESSED / f"level5-{stage}-{layer}.png"
            image = contain_nearest(Image.open(source))
            if layer == "far":
                # Opaque letterbox fill sampled from the quiet upper-left source pixel.
                bg = Image.new("RGBA", TARGET, (*image.getpixel((0, 0))[:3], 255))
                bg.alpha_composite(image)
                image = bg
            else:
                image = binary_key(image)
            image.save(output, optimize=True)
            alpha = image.getchannel("A")
            counts = alpha.histogram()
            opaque = counts[255]
            transparent = counts[0]
            partial = sum(counts[1:255])
            magenta = (
                sum(1 for r, g, b, a in image.getdata() if a and r >= 190 and b >= 150 and g <= 105)
                if layer != "far"
                else 0
            )
            record = {
                "stage": stage,
                "layer": layer,
                "source": str(source.relative_to(ROOT)),
                "output": str(output.relative_to(ROOT)),
                "dimensions": list(image.size),
                "sha256": sha(output),
                "alpha_values": sorted(set(alpha.getdata())),
                "opaque_pixels": opaque,
                "transparent_pixels": transparent,
                "partial_alpha_pixels": partial,
                "opaque_coverage": round(opaque / (TARGET[0] * TARGET[1]), 6),
                "visible_magenta_pixels": magenta,
            }
            records.append(record)
            layers[layer] = image

        comp = layers["far"].copy()
        comp.alpha_composite(layers["middle"])
        comp.alpha_composite(layers["close"])
        # Centered internal-camera preview, preserving source pixels and aspect.
        left = (TARGET[0] - 960) // 2
        comp.crop((left, 0, left + 960, 540)).save(QA / f"{stage}-960x540.png", optimize=True)

    report = {
        "schema_version": 1,
        "status": "asset-stage-validated",
        "runtime_size": list(TARGET),
        "parallax_speeds": {"far": 0.018, "middle": 0.055, "close": 0.13},
        "processing": "centered aspect-preserving nearest-neighbor contain; local magenta removal; binary alpha",
        "records": records,
    }
    (SET / "validation-report.json").write_text(json.dumps(report, indent=2) + "\n")

    failures = []
    if len(records) != 15:
        failures.append("expected exactly 15 records")
    for item in records:
        if item["dimensions"] != [1320, 540]:
            failures.append(f"bad dimensions: {item['output']}")
        if item["partial_alpha_pixels"]:
            failures.append(f"partial alpha: {item['output']}")
        if item["visible_magenta_pixels"]:
            failures.append(f"visible chroma: {item['output']}")
        if item["layer"] == "far" and item["transparent_pixels"]:
            failures.append(f"far transparency: {item['output']}")
        if item["layer"] == "close" and item["transparent_pixels"] / (1320 * 540) < 0.75:
            failures.append(f"close transparency below 75%: {item['output']}")
    if failures:
        raise SystemExit("\n".join(failures))


if __name__ == "__main__":
    main()
