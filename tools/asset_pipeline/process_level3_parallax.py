#!/usr/bin/env python3
from pathlib import Path
import colorsys

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "assets/generated/level3-parallax/source-masters"
PROCESSED = ROOT / "assets/generated/level3-parallax/processed"
RUNTIME = ROOT / "public/assets/backgrounds"
STAGES = (
    "restaurant-alley",
    "rainy-downtown-avenue",
    "rooftop-run",
    "subway-maintenance-tunnels",
    "construction-site-finale",
)
LAYERS = ("far", "middle", "close")
TARGET = (1320, 540)


def center_crop_to_target_aspect(image: Image.Image) -> Image.Image:
    source_width, source_height = image.size
    target_aspect = TARGET[0] / TARGET[1]
    source_aspect = source_width / source_height
    if source_aspect > target_aspect:
        crop_width = round(source_height * target_aspect)
        left = (source_width - crop_width) // 2
        return image.crop((left, 0, left + crop_width, source_height))
    crop_height = round(source_width / target_aspect)
    top = (source_height - crop_height) // 2
    return image.crop((0, top, source_width, top + crop_height))


def hard_key_magenta(image: Image.Image) -> Image.Image:
    rgba = image.convert("RGBA")
    output = []
    pixels = rgba.get_flattened_data() if hasattr(rgba, "get_flattened_data") else rgba.getdata()
    for red, green, blue, _alpha in pixels:
        distance = ((255 - red) ** 2 + green**2 + (255 - blue) ** 2) ** 0.5
        magenta_dominant = (
            red >= 90
            and blue >= 90
            and green * 1.55 < min(red, blue)
            and abs(red - blue) <= 105
        )
        hue, saturation, value = colorsys.rgb_to_hsv(red / 255, green / 255, blue / 255)
        magenta_hue = 0.78 <= hue <= 0.96 and saturation >= 0.30 and value >= 0.18
        if (distance <= 150 and red >= 115 and blue >= 115 and green <= 145) or magenta_dominant or magenta_hue:
            output.append((0, 0, 0, 0))
        else:
            output.append((red, green, blue, 255))
    rgba.putdata(output)
    return rgba


def main() -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    RUNTIME.mkdir(parents=True, exist_ok=True)
    for stage in STAGES:
        for layer in LAYERS:
            source_path = SOURCE / f"level3-{stage}-{layer}-source.png"
            output_name = f"level3-{stage}-{layer}.png"
            with Image.open(source_path) as source_image:
                cropped = center_crop_to_target_aspect(source_image)
                resized = cropped.resize(TARGET, Image.Resampling.NEAREST)
                result = resized.convert("RGB") if layer == "far" else hard_key_magenta(resized)
                result.save(PROCESSED / output_name, optimize=False)
                result.save(RUNTIME / output_name, optimize=False)


if __name__ == "__main__":
    main()
