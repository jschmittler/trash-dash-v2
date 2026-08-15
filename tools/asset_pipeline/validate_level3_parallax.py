#!/usr/bin/env python3
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "public/assets/backgrounds"
STAGES = ("restaurant-alley", "rainy-downtown-avenue", "rooftop-run", "subway-maintenance-tunnels", "construction-site-finale")
LAYERS = ("far", "middle", "close")

errors = []
expected = {f"level3-{stage}-{layer}.png" for stage in STAGES for layer in LAYERS}
actual = {path.name for path in ASSETS.glob("level3-*.png")}
if actual != expected:
    errors.append(f"file set differs: missing={sorted(expected-actual)} extra={sorted(actual-expected)}")

for name in sorted(expected):
    path = ASSETS / name
    if not path.exists():
        continue
    with Image.open(path) as image:
        if image.format != "PNG": errors.append(f"{name}: not PNG")
        if image.size != (1320, 540): errors.append(f"{name}: size {image.size}")
        alpha_channel = image.convert("RGBA").getchannel("A")
        alpha = list(alpha_channel.get_flattened_data() if hasattr(alpha_channel, "get_flattened_data") else alpha_channel.getdata())
        values = set(alpha)
        if "-far.png" in name:
            if values != {255}: errors.append(f"{name}: far not fully opaque")
        else:
            if not values.issubset({0, 255}): errors.append(f"{name}: alpha not binary: {sorted(values)}")
            transparent = alpha.count(0) / len(alpha)
            opaque = alpha.count(255) / len(alpha)
            if transparent < 0.20 or opaque < 0.01:
                errors.append(f"{name}: not meaningful object alpha ({transparent=:.3f}, {opaque=:.3f})")
        print(f"{name}: {image.size[0]}x{image.size[1]} alpha={sorted(values)}")

if errors:
    for error in errors: print(f"FAIL: {error}")
    raise SystemExit(1)
print("Level 3 static parallax validation: PASS")
