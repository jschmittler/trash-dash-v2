"""Focused regression tests for Level 1 parallax normalization primitives."""

from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("level1_parallax", ROOT / "tools/asset_pipeline/process_level1_parallax.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Level1ParallaxProcessingTests(unittest.TestCase):
    def test_far_plate_is_center_cropped_nearest_and_opaque(self) -> None:
        source = Image.new("RGBA", (1000, 200), (20, 40, 60, 7))
        source.putpixel((500, 100), (250, 200, 150, 19))
        output = MODULE.crop_far_to_runtime(source)
        self.assertEqual((1320, 540), output.size)
        self.assertEqual({255}, set(output.getchannel("A").get_flattened_data()))
        self.assertIn((250, 200, 150, 255), set(output.get_flattened_data()))

    def test_moving_plate_fits_without_nonuniform_scaling(self) -> None:
        source = Image.new("RGBA", (200, 100), (255, 0, 255, 255))
        ImageDraw.Draw(source).rectangle((80, 10, 119, 89), fill=(10, 20, 30, 255))
        fitted = MODULE.fit_moving_plate(source)
        output = MODULE.remove_boundary_connected_magenta(fitted)
        self.assertEqual((1320, 540), output.size)
        self.assertIn(0, set(output.getchannel("A").get_flattened_data()))
        self.assertIn(255, set(output.getchannel("A").get_flattened_data()))
        self.assertEqual(216, output.getbbox()[2] - output.getbbox()[0])
        self.assertEqual(432, output.getbbox()[3] - output.getbbox()[1])

    def test_boundary_key_removal_preserves_enclosed_violet_detail(self) -> None:
        source = Image.new("RGBA", (9, 9), (255, 0, 255, 255))
        ImageDraw.Draw(source).rectangle((2, 2, 6, 6), fill=(25, 25, 25, 255))
        source.putpixel((4, 4), (110, 85, 145, 255))
        result = MODULE.remove_boundary_connected_magenta(source)
        self.assertEqual((0, 0, 0, 0), result.getpixel((0, 0)))
        self.assertEqual((110, 85, 145, 255), result.getpixel((4, 4)))


if __name__ == "__main__":
    unittest.main()
