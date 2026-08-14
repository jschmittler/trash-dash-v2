from __future__ import annotations

import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from tools.verify.validate_design_library import validate


class DesignLibraryValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.manifests = self.root / "docs/design/trash-dash/manifests"
        self.manifests.mkdir(parents=True)
        self.write_tsv(
            self.manifests / "LIBRARY_PRE_MIGRATION_INVENTORY.tsv",
            ["path", "size", "sha256", "git_state", "category", "destination", "disposition", "stable_id", "aliases"],
            [],
        )
        self.write_tsv(
            self.manifests / "LIBRARY_MIGRATION_MAP.tsv",
            ["old_path", "new_path", "stable_id", "sha256", "disposition", "category", "aliases"],
            [],
        )
        (self.root / "docs/design/trash-dash/library").mkdir(parents=True)
        self.write_catalog([])

    def tearDown(self) -> None:
        self.temporary.cleanup()

    @staticmethod
    def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
        with path.open("w", encoding="utf-8", newline="") as stream:
            writer = csv.DictWriter(stream, fieldnames=fields, delimiter="\t", lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)

    def write_catalog(self, assets: list[dict]) -> None:
        (self.manifests / "library-catalog.json").write_text(
            json.dumps({"schema": "trash-dash-v2-library-catalog-v1", "assets": assets}), encoding="utf-8"
        )

    def add_asset(self, relative: str, asset_id: str = "asset.one") -> dict:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"source")
        return {
            "id": asset_id,
            "canonicalPath": relative,
            "sha256": hashlib.sha256(b"source").hexdigest(),
            "runtimeStatus": "not-runtime",
        }

    def test_active_legacy_reference_fails(self) -> None:
        (self.root / "AGENTS.md").write_text(
            "Use docs/design/trash-dash/reference/characters", encoding="utf-8"
        )
        failures = validate(self.root)
        self.assertTrue(any("active legacy path" in failure for failure in failures))

    def test_package_historical_reference_is_allowed(self) -> None:
        package = self.root / "docs/design/trash-dash/packages/imported-source/README.md"
        package.parent.mkdir(parents=True)
        package.write_text("Original: docs/design/trash-dash/reference/characters", encoding="utf-8")
        self.assertEqual(validate(self.root), [])

    def test_missing_and_duplicate_catalog_records_fail(self) -> None:
        asset = self.add_asset("docs/design/trash-dash/library/gameplay/items/sprites/item.png")
        duplicate = dict(asset)
        duplicate["canonicalPath"] = "docs/design/trash-dash/library/gameplay/items/sprites/missing.png"
        self.write_catalog([asset, duplicate])
        failures = validate(self.root)
        self.assertTrue(any("duplicate canonical ID" in failure for failure in failures))
        self.assertTrue(any("missing catalog path" in failure for failure in failures))

    def test_uncataloged_asset_and_import_sidecar_fail(self) -> None:
        library = self.root / "docs/design/trash-dash/library"
        (library / "loose.png").write_bytes(b"loose")
        (library / "loose.png.import").write_text("metadata", encoding="utf-8")
        failures = validate(self.root)
        self.assertTrue(any("uncataloged library file" in failure for failure in failures))
        self.assertTrue(any("design metadata present" in failure for failure in failures))


if __name__ == "__main__":
    unittest.main()
