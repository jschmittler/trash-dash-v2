#!/usr/bin/env python3
"""Declarative path authority for the Trash Dash design library migration."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

DESIGN_REL = Path("docs/design/trash-dash")

Disposition = Literal[
    "canonical-moved",
    "package-preserved",
    "archive",
    "generated-metadata-removed",
]

BOSSES = {
    "01": "trash-dash",
    "02": "brutus-bin-hound",
    "03": "pizza-rat-king",
    "04": "project-opossum",
    "05": "galactogobbler",
    "06": "diamond-don",
}

GAMEPLAY_TILE_DESTINATIONS = {
    "trash_dash_forest_level_blueprint.png": "environments/blueprints/level-01",
    "trash_dash_moonlit_neighborhood_blueprint.png": "environments/blueprints/level-02",
    "trash_dash_level_2_concept_board.png": "environments/concepts/level-02",
    "trash_dash_space_center_level_4.png": "environments/concepts/level-04",
    "trash_dash_orbital_junkyard_concepts.png": "environments/concepts/level-05",
    "trash_dash_stadium_nightfall_layout.png": "environments/blueprints/level-06",
    "trash_dash_suburban_night_sprite_atlas.png": "environments/tiles/level-02",
    "trash_dash_level_3_sprite_sheet.png": "environments/tiles/level-03",
    "trash_dash_level_4_sprite_sheet.png": "environments/tiles/level-04",
    "trash_dash_orbital_junkyard_sprite_sheet.png": "environments/tiles/level-05",
}


@dataclass(frozen=True)
class MappingRecord:
    old_path: str
    new_path: str | None
    stable_id: str | None
    disposition: Disposition
    category: str
    aliases: tuple[str, ...] = ()


def _repo_path(relative: Path) -> str:
    return (DESIGN_REL / relative).as_posix()


def _library(relative: str | Path) -> str:
    return _repo_path(Path("library") / relative)


def _manual(relative: str | Path) -> str:
    return _repo_path(Path("manuals") / relative)


def _package(relative: str | Path) -> str:
    return _repo_path(Path("packages") / relative)


def _canonical(old: str, destination: str, category: str, aliases: tuple[str, ...] = ()) -> MappingRecord:
    relative = Path(destination).relative_to(DESIGN_REL / "library")
    stem = relative.with_suffix("").as_posix().replace("/", ".")
    return MappingRecord(old, destination, f"library.{stem}", "canonical-moved", category, aliases)


def map_legacy_path(repo_relative: str) -> MappingRecord:
    """Return the approved destination for one current repository path."""
    source = Path(repo_relative)
    try:
        relative = source.relative_to(DESIGN_REL)
    except ValueError as exc:
        raise ValueError(f"outside design tree: {repo_relative}") from exc

    if source.name == ".DS_Store" or source.suffix == ".import":
        return MappingRecord(repo_relative, None, None, "generated-metadata-removed", "metadata")

    parts = relative.parts
    if not parts:
        raise ValueError(f"cannot map design root: {repo_relative}")

    if parts[0] == "archive":
        return MappingRecord(repo_relative, repo_relative, None, "archive", "archive")

    if parts[0] == "reference":
        return _map_reference(repo_relative, relative)

    package_roots = {
        "character-animation": "character-animation",
        "ui-kit": "ui-kit",
        "powerups": "powerups",
        "multipart": "multipart",
    }
    if parts[0] in package_roots:
        destination = _package(Path(package_roots[parts[0]]) / Path(*parts[1:]))
        return MappingRecord(repo_relative, destination, None, "package-preserved", f"package-{parts[0]}")

    if parts[0] == "docs":
        return _map_docs(repo_relative, relative)

    # Root documentation and authority manifests retain their path.
    return MappingRecord(repo_relative, repo_relative, None, "canonical-moved", "design-support")


def _map_reference(old: str, relative: Path) -> MappingRecord:
    parts = relative.parts
    area = parts[1]

    if area == "main-characters":
        kind, filename = parts[2], parts[3]
        hero = "trashy" if filename.startswith("trashy-") else "jimothy"
        branch = Path("characters/heroes") / hero / kind
        if kind == "sprites":
            branch /= "reference"
        return _canonical(old, _library(branch / filename), f"hero-{kind}")

    if area == "characters":
        level, kind, filename = parts[2], parts[3], parts[4]
        number = level.removeprefix("level-")
        if filename.startswith("boss-") or (kind == "concepts" and filename == "boss.png"):
            branch = Path("characters/bosses") / BOSSES[number] / kind
            if kind == "sprites":
                branch /= "reference"
            return _canonical(old, _library(branch / filename), f"boss-{kind}")
        branch = Path("characters/enemies") / level / kind
        if kind == "sprites":
            branch /= "reference"
        aliases = ("squirrel",) if filename == "squirel.png" else ()
        return _canonical(old, _library(branch / filename), f"enemy-{kind}", aliases)

    if area == "environments":
        level, filename = parts[2], parts[3]
        return _canonical(old, _library(Path("environments/backgrounds") / level / filename), "background")

    if area == "foreground-assets":
        level, filename = parts[2], parts[3]
        return _canonical(old, _library(Path("environments/foreground") / level / filename), "foreground")

    if area == "level-layouts":
        filename = parts[-1]
        level = "level-" + filename.split("-", 2)[1]
        return _canonical(old, _library(Path("environments/blueprints") / level / filename), "blueprint")

    if area == "gameplay-tiles":
        filename = parts[-1]
        destination = GAMEPLAY_TILE_DESTINATIONS.get(filename)
        if destination is None:
            raise ValueError(f"unclassified gameplay tile: {old}")
        return _canonical(old, _library(Path(destination) / filename), destination.split("/")[1])

    if area == "levels":
        level, kind, filename = parts[2], parts[3], parts[4]
        if kind == "blueprints":
            return _canonical(old, _library(Path("environments/blueprints") / level / filename), "blueprint")
        if kind == "concepts":
            return _canonical(old, _library(Path("environments/concepts") / level / filename), "environment-concept")
        if kind == "props":
            return _canonical(old, _library(Path("environments/props") / level / filename), "prop")
        if kind == "tilesheets":
            return _canonical(old, _library(Path("environments/tiles") / level / filename), "tiles")
        if kind == "specs":
            destination = _manual(Path("levels") / level / filename)
            return MappingRecord(old, destination, f"manual.levels.{level}.{Path(filename).stem}", "canonical-moved", "level-manual")
        if kind in {"generation", "references"}:
            destination = _package(Path("imported-source/trashy/levels") / level / kind / filename)
            return MappingRecord(old, destination, None, "package-preserved", f"trashy-{kind}")
        raise ValueError(f"unclassified imported level path: {old}")

    if area == "items":
        kind, filename = parts[2], parts[3]
        item_type = "powerups" if filename.startswith("powerups-") else "items"
        branch = Path("gameplay") / item_type / kind
        if item_type == "powerups":
            branch /= "reference"
        return _canonical(old, _library(branch / filename), f"gameplay-{item_type}")

    if area == "rewards":
        kind, filename = parts[2], parts[3]
        return _canonical(old, _library(Path("gameplay/rewards") / kind / filename), "reward")

    if area == "ui-powerups":
        kind, filename = parts[2], parts[3]
        branch = "interface/concepts/powerup-splashes" if kind == "concepts" else "interface/source-sheets/powerup-splashes"
        return _canonical(old, _library(Path(branch) / filename), "interface-powerup")

    raise ValueError(f"unclassified reference path: {old}")


def _map_docs(old: str, relative: Path) -> MappingRecord:
    parts = relative.parts
    if parts[1] == "integration":
        destination = _package(Path("imported-source/master-bundle/integration") / Path(*parts[2:]))
        return MappingRecord(old, destination, None, "package-preserved", "integration-package")
    if parts[1] == "prompts":
        destination = _package(Path("imported-source/master-bundle/prompts") / Path(*parts[2:]))
        return MappingRecord(old, destination, None, "package-preserved", "prompt-package")
    if parts[1] != "game":
        raise ValueError(f"unclassified docs path: {old}")

    tail = Path(*parts[2:])
    if tail.parts[0] == "bosses":
        destination = _manual(Path("bosses") / Path(*tail.parts[1:]))
        return MappingRecord(old, destination, f"manual.bosses.{tail.stem}", "canonical-moved", "boss-manual")
    if tail.parts[0] == "enemy-canon":
        if len(tail.parts) > 1 and tail.parts[1] == "reference-art":
            destination = _package(Path("imported-source/trashy/enemy-canon") / Path(*tail.parts[1:]))
            return MappingRecord(old, destination, None, "package-preserved", "enemy-reference-package")
        destination = _manual(Path("enemies") / Path(*tail.parts[1:]))
        return MappingRecord(old, destination, f"manual.enemies.{tail.stem}", "canonical-moved", "enemy-manual")

    manual_destinations = {
        "APPROVED_ASSET_POLICY.md": "APPROVED_ASSET_POLICY.md",
        "DECISIONS.md": "DECISIONS.md",
        "APPROVED_MAIN_CHARACTERS.md": "characters/APPROVED_MAIN_CHARACTERS.md",
        "MAIN_CHARACTERS.md": "characters/MAIN_CHARACTERS.md",
        "ITEMS_POWERUPS_UI_REWARDS.md": "gameplay/ITEMS_POWERUPS_UI_REWARDS.md",
        "LEVEL_LAYOUT_GUIDANCE.md": "levels/LEVEL_LAYOUT_GUIDANCE.md",
        "levels.md": "levels/levels.md",
        "foreground-assets.md": "environments/foreground-assets.md",
        "enemies.md": "enemies/legacy-enemies.md",
    }
    destination = manual_destinations.get(tail.as_posix())
    if destination is None:
        raise ValueError(f"unclassified game manual: {old}")
    return MappingRecord(old, _manual(destination), f"manual.{Path(destination).stem}", "canonical-moved", "game-manual")


def build_mapping(root: Path) -> list[MappingRecord]:
    design = root / DESIGN_REL
    records = [
        map_legacy_path(path.relative_to(root).as_posix())
        for path in sorted(design.rglob("*"))
        if path.is_file()
    ]
    old_paths = [record.old_path for record in records]
    if len(old_paths) != len(set(old_paths)):
        raise ValueError("duplicate legacy paths in mapping")
    destinations = [record.new_path for record in records if record.new_path]
    conflicts = {item for item in destinations if destinations.count(item) > 1}
    if conflicts:
        raise ValueError(f"destination collisions: {sorted(conflicts)}")
    return records


def mapping_by_old_path(root: Path) -> dict[str, MappingRecord]:
    return {record.old_path: record for record in build_mapping(root)}
