#!/usr/bin/env bash
set -euo pipefail

PACKAGE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_REPO="${1:-}"
ASSET_ROOT="${ASSET_ROOT:-public/assets}"
FORCE="${FORCE:-0}"
INCLUDE_REFERENCES="${INCLUDE_REFERENCES:-0}"

if [[ -z "$TARGET_REPO" ]]; then
  echo "Usage: $0 /path/to/trash-dash-hd-remake"
  echo "Optional env: ASSET_ROOT=src/assets FORCE=1 INCLUDE_REFERENCES=1"
  exit 1
fi

if [[ ! -d "$TARGET_REPO" ]]; then
  echo "Target repo does not exist: $TARGET_REPO" >&2
  exit 1
fi

DEST="$TARGET_REPO/$ASSET_ROOT/trash-dash/powerups"
mkdir -p "$DEST/items" "$DEST/overlays"

copy_file() {
  local src="$1"
  local dst="$2"
  if [[ -e "$dst" && "$FORCE" != "1" ]]; then
    echo "skip  $dst (already exists; set FORCE=1 to overwrite)"
    return
  fi
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
  echo "copy  $dst"
}

copy_file "$PACKAGE_DIR/assets/powerups/taco-kite-powerups-clean-chroma.png" \
          "$DEST/items/taco-kite-powerups-clean-chroma.png"
copy_file "$PACKAGE_DIR/assets/overlays/taco-power-overlay-clean-8frame.png" \
          "$DEST/overlays/taco-power-overlay-clean-8frame.png"
copy_file "$PACKAGE_DIR/assets/overlays/kite-power-overlay-clean-8frame.png" \
          "$DEST/overlays/kite-power-overlay-clean-8frame.png"
copy_file "$PACKAGE_DIR/manifest.json" "$DEST/manifest.json"
copy_file "$PACKAGE_DIR/CODEX_IMPORT.md" "$DEST/CODEX_IMPORT.md"

if [[ "$INCLUDE_REFERENCES" == "1" ]]; then
  mkdir -p "$DEST/reference"
  for ref in "$PACKAGE_DIR"/reference/*.png; do
    copy_file "$ref" "$DEST/reference/$(basename "$ref")"
  done
fi

cat <<EOF

Trash Dash power-up assets imported to:
  $DEST

Next step for Codex:
  Read $DEST/CODEX_IMPORT.md and $DEST/manifest.json, then integrate the assets into the existing game architecture.
EOF
