#!/usr/bin/env python3
"""Mechanically retarget active repository consumers to the type-first library."""
from __future__ import annotations

import csv
from pathlib import Path

from reorganize_design_library import copy_operations

ROOT = Path(__file__).resolve().parents[2]
MAP = ROOT / "docs/design/trash-dash/manifests/LIBRARY_MIGRATION_MAP.tsv"
TEXT_SUFFIXES = {".md", ".txt", ".json", ".tsv", ".yaml", ".yml", ".py", ".sh", ".gd", ".ts", ".cfg"}


def target_files() -> list[Path]:
    files = [ROOT / "AGENTS.md", ROOT / "README.md", ROOT / ".gitattributes", ROOT / ".gitignore"]
    for relative in (
        ".skills",
        "assets/generated",
        "docs/architecture",
        "docs/migration",
        "docs/design/trash-dash/manuals",
        "tools/asset_pipeline",
        "tools/verify",
    ):
        base = ROOT / relative
        if base.is_dir():
            files.extend(path for path in base.rglob("*") if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES)
    excluded = {
        ROOT / "tools/verify/validate_design_library.py",
    }
    return sorted({path for path in files if path.is_file() and path not in excluded})


def replacements() -> list[tuple[str, str]]:
    with MAP.open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream, delimiter="\t"))
    values: dict[str, str] = {
        row["old_path"]: row["new_path"]
        for row in rows
        if row["new_path"] and row["old_path"] != row["new_path"]
    }
    # Active extraction/build consumers should use canonical library copies,
    # not their package-preserved source locations.
    for operation in copy_operations():
        values[operation.source] = operation.destination
    values.update({
        "docs/design/trash-dash/docs/game/bosses/": "docs/design/trash-dash/manuals/bosses/",
        "docs/design/trash-dash/docs/game/enemy-canon/": "docs/design/trash-dash/manuals/enemies/",
        "docs/design/trash-dash/docs/game/LEVEL_LAYOUT_GUIDANCE.md": "docs/design/trash-dash/manuals/levels/LEVEL_LAYOUT_GUIDANCE.md",
        "docs/design/trash-dash/docs/game/levels.md": "docs/design/trash-dash/manuals/levels/levels.md",
        "docs/design/trash-dash/docs/game/enemies.md": "docs/design/trash-dash/manuals/enemies/legacy-enemies.md",
        "docs/design/trash-dash/character-animation/": "docs/design/trash-dash/packages/character-animation/",
        "docs/design/trash-dash/ui-kit/": "docs/design/trash-dash/packages/ui-kit/",
        "docs/design/trash-dash/powerups/": "docs/design/trash-dash/packages/powerups/",
        "docs/design/trash-dash/reference/": "docs/design/trash-dash/library/",
    })
    return sorted(values.items(), key=lambda item: len(item[0]), reverse=True)


def main() -> None:
    pairs = replacements()
    changed = 0
    replacements_count = 0
    for path in target_files():
        try:
            before = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        after = before
        for old, new in pairs:
            count = after.count(old)
            if count:
                replacements_count += count
                after = after.replace(old, new)
        if after != before:
            path.write_text(after, encoding="utf-8")
            changed += 1
    print(f"ACTIVE REFERENCES: {replacements_count} replacements across {changed} files")


if __name__ == "__main__":
    main()
