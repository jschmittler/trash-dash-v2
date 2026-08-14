#!/usr/bin/env python3
"""Apply the approved Trash Dash design-library reorganization safely."""
from __future__ import annotations

import argparse
import csv
import hashlib
import shutil
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREFLIGHT = ROOT / "docs/design/trash-dash/manifests/LIBRARY_PRE_MIGRATION_INVENTORY.tsv"

ENEMY_LEVELS = {
    "mosquito": "01", "opossum-pilfer": "01", "pigeon": "01", "snake": "01", "spider": "01",
    "bee": "02", "dog": "02", "moth-dustwing": "02", "skunk": "02", "squirrel": "02",
    "alley-cat-burglar": "03", "sewer-rat-courier": "03", "subway-roach": "03", "traffic-cone-crab": "03",
    "beaker-slime": "04", "clipboard-hamster": "04", "mop-bot-3000": "04", "phase-gecko": "04",
    "asteroid-armadillo": "05", "rocket-roach": "05", "satellite-hermit-crab": "05", "vacuum-jelly": "05",
    "baserunning-beaver": "06", "clobbering-cub": "06", "sliding-seagull": "06", "windup-weasel": "06",
}
BOSSES = {
    "boss-trash-dash": "trash-dash",
    "boss-brutus-bin-hound": "brutus-bin-hound",
    "boss-pizza-rat-king": "pizza-rat-king",
    "boss-project-opossum": "project-opossum",
    "boss-galactogobbler": "galactogobbler",
    "boss-diamond-don": "diamond-don",
}


@dataclass(frozen=True)
class CopyOperation:
    source: str
    destination: str
    category: str


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def rows() -> list[dict[str, str]]:
    with PREFLIGHT.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


def batch_for(category: str) -> str:
    if category.endswith("manual") or category == "game-manual":
        return "manuals"
    if category.startswith(("hero-", "boss-", "enemy-")):
        return "characters"
    if category in {"background", "foreground", "blueprint", "blueprints", "concepts", "environment-concept", "prop", "tiles", "trashy-generation", "trashy-references"}:
        return "environments"
    if category.startswith("gameplay-") or category == "reward":
        return "gameplay"
    if category == "interface-powerup":
        return "interface"
    if category.startswith("package-") or category.endswith("package") or category.startswith("trashy-"):
        return "packages"
    if category == "metadata":
        return "metadata"
    return "support"


def copy_operations() -> list[CopyOperation]:
    base = "docs/design/trash-dash/character-animation/phase-05-codex-integration"
    operations: list[CopyOperation] = []
    for hero in ("trashy", "jimothy"):
        for variant in ("regular", "powered"):
            filename = f"{hero}-{variant}-approved.png"
            operations.append(CopyOperation(
                f"{base}/phase-01-approved-main-characters/atlases/{filename}",
                f"docs/design/trash-dash/library/characters/heroes/{hero}/sprites/animation-source/{filename}",
                "characters",
            ))
    enemy_sources = [
        ("phase-02/final", name) for name in (
            "mosquito", "opossum-pilfer", "pigeon", "snake", "spider", "bee", "dog", "moth-dustwing", "skunk", "squirrel"
        )
    ] + [
        ("phase-03-variable/final", name) for name in ENEMY_LEVELS if name not in {
            "mosquito", "opossum-pilfer", "pigeon", "snake", "spider", "bee", "dog", "moth-dustwing", "skunk", "squirrel"
        }
    ]
    for phase, name in enemy_sources:
        filename = f"{name}-transparent.png"
        operations.append(CopyOperation(
            f"{base}/{phase}/{filename}",
            f"docs/design/trash-dash/library/characters/enemies/level-{ENEMY_LEVELS[name]}/sprites/animation-source/{filename}",
            "characters",
        ))
    for source_name, identity in BOSSES.items():
        filename = f"{source_name}-transparent.png"
        operations.append(CopyOperation(
            f"{base}/phase-04-bosses/final/{filename}",
            f"docs/design/trash-dash/library/characters/bosses/{identity}/sprites/animation-source/{filename}",
            "characters",
        ))

    powerups = "docs/design/trash-dash/powerups/trash-dash-hd-powerups-v1"
    for relative in (
        "assets/powerups/taco-kite-powerups-clean-chroma.png",
        "assets/overlays/taco-power-overlay-clean-8frame.png",
        "assets/overlays/kite-power-overlay-clean-8frame.png",
    ):
        operations.append(CopyOperation(
            f"{powerups}/{relative}",
            f"docs/design/trash-dash/library/gameplay/powerups/sprites/animation-source/{Path(relative).name}",
            "gameplay",
        ))
    for filename in (
        "powerups-branded-reference.png",
        "kite-power-overlay-branded-reference.png",
        "taco-power-overlay-branded-reference.png",
    ):
        operations.append(CopyOperation(
            f"{powerups}/reference/{filename}",
            f"docs/design/trash-dash/library/gameplay/powerups/concepts/{filename}",
            "gameplay",
        ))

    ui = "docs/design/trash-dash/ui-kit/trash-dash-hd-remake-ui-kit-codex-handoff-v0.3"
    for filename in (
        "00-overall-ui-kit.png", "01-buttons-tabs.png", "02-panels-containers.png",
        "03-hud-notifications-alerts.png", "04-results-character-select.png",
    ):
        operations.append(CopyOperation(
            f"{ui}/reference/concept-boards/{filename}",
            f"docs/design/trash-dash/library/interface/concepts/{filename}",
            "interface",
        ))
    for filename in (
        "phase-01-buttons-tabs.png", "phase-02-panels-containers.png",
        "phase-03-hud-notifications-alerts.png", "phase-04-results-character-select.png",
    ):
        operations.append(CopyOperation(
            f"{ui}/source-sheets/{filename}",
            f"docs/design/trash-dash/library/interface/source-sheets/{filename}",
            "interface",
        ))
    operations.extend([
        CopyOperation(f"{ui}/tokens/ui.tokens.json", "docs/design/trash-dash/library/interface/tokens/ui.tokens.json", "interface"),
        CopyOperation(f"{ui}/tokens/motion.tokens.json", "docs/design/trash-dash/library/interface/tokens/motion.tokens.json", "interface"),
        CopyOperation(f"{ui}/reference/motion/ui-motion-reference.png", "docs/design/trash-dash/library/interface/motion/ui-motion-reference.png", "interface"),
    ])
    return operations


def inspect_move(row: dict[str, str], apply: bool) -> str:
    old = ROOT / row["path"]
    destination_text = row["destination"]
    expected = row["sha256"]
    if row["disposition"] == "generated-metadata-removed":
        if old.exists():
            if sha256(old) != expected:
                raise RuntimeError(f"metadata hash changed before removal: {row['path']}")
            if apply:
                old.unlink()
            return "remove"
        return "done"
    if not destination_text:
        raise RuntimeError(f"missing destination: {row['path']}")
    destination = ROOT / destination_text
    if old.resolve() == destination.resolve():
        if not old.is_file() or sha256(old) != expected:
            raise RuntimeError(f"retained file changed: {row['path']}")
        return "done"
    if old.is_file():
        if sha256(old) != expected:
            raise RuntimeError(f"source hash changed: {row['path']}")
        if destination.exists() and sha256(destination) != expected:
            raise RuntimeError(f"refusing non-identical destination: {destination_text}")
        if apply:
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not destination.exists():
                old.replace(destination)
            else:
                old.unlink()
        return "move"
    if destination.is_file() and sha256(destination) == expected:
        return "done"
    raise RuntimeError(f"source and destination missing: {row['path']} -> {destination_text}")


def inspect_copy(operation: CopyOperation, apply: bool) -> str:
    source = ROOT / operation.source
    destination = ROOT / operation.destination
    if not source.is_file():
        # Package may already have moved.
        package_source = operation.source.replace(
            "docs/design/trash-dash/character-animation/", "docs/design/trash-dash/packages/character-animation/"
        ).replace(
            "docs/design/trash-dash/ui-kit/", "docs/design/trash-dash/packages/ui-kit/"
        ).replace(
            "docs/design/trash-dash/powerups/", "docs/design/trash-dash/packages/powerups/"
        )
        source = ROOT / package_source
    if not source.is_file():
        raise RuntimeError(f"missing package copy source: {operation.source}")
    expected = sha256(source)
    if destination.exists():
        if sha256(destination) != expected:
            raise RuntimeError(f"refusing non-identical copied destination: {operation.destination}")
        return "done"
    if apply:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        if sha256(destination) != expected:
            raise RuntimeError(f"copy hash mismatch: {operation.destination}")
    return "copy"


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--batch", required=True, choices=["characters", "environments", "gameplay", "interface", "manuals", "packages", "metadata", "support"])
    args = parser.parse_args()
    apply = bool(args.apply)
    selected = [row for row in rows() if batch_for(row["category"]) == args.batch]
    actions = {"move": 0, "copy": 0, "remove": 0, "done": 0}
    for row in selected:
        action = inspect_move(row, apply)
        actions[action] += 1
    for operation in copy_operations():
        if operation.category == args.batch:
            action = inspect_copy(operation, apply)
            actions[action] += 1
    verb = "APPLIED" if apply else "CHECKED"
    print(f"{verb} {args.batch}: " + ", ".join(f"{key}={value}" for key, value in actions.items()))


if __name__ == "__main__":
    main()
