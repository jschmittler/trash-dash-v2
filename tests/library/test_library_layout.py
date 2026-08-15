from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.library.library_layout import map_legacy_path


class LibraryLayoutTests(unittest.TestCase):
    def test_role_specific_character_mapping(self) -> None:
        trashy = map_legacy_path(
            "docs/design/trash-dash/reference/main-characters/sprites/trashy-regular-approved.png"
        )
        self.assertEqual(
            trashy.new_path,
            "docs/design/trash-dash/library/characters/heroes/trashy/sprites/reference/trashy-regular-approved.png",
        )
        boss = map_legacy_path(
            "docs/design/trash-dash/reference/characters/level-03/sprites/boss-pizza-rat-king.png"
        )
        self.assertEqual(
            boss.new_path,
            "docs/design/trash-dash/library/characters/bosses/pizza-rat-king/sprites/reference/boss-pizza-rat-king.png",
        )
        enemy = map_legacy_path(
            "docs/design/trash-dash/reference/characters/level-03/sprites/subway-roach.png"
        )
        self.assertEqual(
            enemy.new_path,
            "docs/design/trash-dash/library/characters/enemies/level-03/sprites/reference/subway-roach.png",
        )

    def test_foreground_sources_do_not_collapse(self) -> None:
        approved = map_legacy_path(
            "docs/design/trash-dash/reference/foreground-assets/level-01/foreground-gameplay-assets.png"
        )
        imported = map_legacy_path(
            "docs/design/trash-dash/reference/levels/level-01/references/foreground-gameplay-assets.png"
        )
        self.assertEqual(
            approved.new_path,
            "docs/design/trash-dash/library/environments/foreground/level-01/foreground-gameplay-assets.png",
        )
        self.assertEqual(
            imported.new_path,
            "docs/design/trash-dash/packages/imported-source/trashy/levels/level-01/references/foreground-gameplay-assets.png",
        )
        self.assertNotEqual(approved.new_path, imported.new_path)

    def test_mixed_gameplay_tiles_are_explicit(self) -> None:
        layout = map_legacy_path(
            "docs/design/trash-dash/reference/gameplay-tiles/concepts/trash_dash_stadium_nightfall_layout.png"
        )
        self.assertEqual(
            layout.new_path,
            "docs/design/trash-dash/library/environments/blueprints/level-06/trash_dash_stadium_nightfall_layout.png",
        )

    def test_metadata_is_removed(self) -> None:
        metadata = map_legacy_path("docs/design/trash-dash/reference/characters/.DS_Store")
        self.assertIsNone(metadata.new_path)
        self.assertEqual(metadata.disposition, "generated-metadata-removed")


if __name__ == "__main__":
    unittest.main()
