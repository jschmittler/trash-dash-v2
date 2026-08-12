#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)"
repo_root="$(CDPATH= cd -- "$script_dir/../.." && pwd -P)"
package_root="$repo_root/docs/design/trash-dash/powerups/trash-dash-hd-powerups-v1"

fail() {
	printf 'Power-up source import: FAIL: %s\n' "$*" >&2
	exit 1
}

for command_name in file git jq shasum; do
	command -v "$command_name" >/dev/null 2>&1 || fail "required command is unavailable: $command_name"
done

for required_file in \
	"$package_root/README.md" \
	"$package_root/CODEX_IMPORT.md" \
	"$package_root/manifest.json" \
	"$package_root/checksums.sha256" \
	"$package_root/scripts/import_powerups.sh" \
	"$package_root/IMPORT_AUDIT.md"; do
	[[ -f "$required_file" ]] || fail "required package file is missing: ${required_file#"$repo_root/"}"
done

jq empty "$package_root/manifest.json" || fail "manifest is invalid JSON"
jq -e '
	.package == "trash-dash-hd-powerups" and
	.version == "1.0.0" and
	.status == "approved" and
	.runtimeAssets.powerupItems.dimensions == {"width": 2172, "height": 724} and
	.runtimeAssets.powerupItems.rowSplitY == 362 and
	.runtimeAssets.powerupItems.rows.taco.frameCount == 11 and
	.runtimeAssets.powerupItems.rows.kite.frameCount == 11 and
	(.runtimeAssets.powerupItems.rows.taco.xCuts | length) == 12 and
	(.runtimeAssets.powerupItems.rows.kite.xCuts | length) == 12 and
	.runtimeAssets.pickupOverlays.taco.grid == {"columns": 4, "rows": 2, "frameWidth": 384, "frameHeight": 512} and
	.runtimeAssets.pickupOverlays.kite.grid == {"columns": 4, "rows": 2, "frameWidth": 384, "frameHeight": 512} and
	.runtimeAssets.pickupOverlays.taco.frameCount == 8 and
	.runtimeAssets.pickupOverlays.kite.frameCount == 8 and
	(.referenceOnly | length) == 3
' "$package_root/manifest.json" >/dev/null || fail "manifest contract is incomplete or changed"

(
	cd "$package_root"
	LC_ALL=C LANG=C shasum -a 256 -c checksums.sha256
) >/dev/null || fail "package checksum verification failed"

check_png() {
	local relative_path="$1"
	local expected_description="$2"
	local full_path="$package_root/$relative_path"
	[[ -f "$full_path" ]] || fail "PNG is missing: $relative_path"
	local description
	description="$(file "$full_path")"
	case "$description" in
		*"$expected_description"*) ;;
		*) fail "PNG contract mismatch for $relative_path: $description" ;;
	esac
	local filter_attribute
	filter_attribute="$(git -C "$repo_root" check-attr filter -- "$full_path")"
	case "$filter_attribute" in
		*': filter: lfs') ;;
		*) fail "PNG is not covered by Git LFS: $relative_path" ;;
	esac
}

check_png "assets/powerups/taco-kite-powerups-clean-chroma.png" "PNG image data, 2172 x 724, 8-bit/color RGB, non-interlaced"
check_png "assets/overlays/taco-power-overlay-clean-8frame.png" "PNG image data, 1536 x 1024, 8-bit/color RGBA, non-interlaced"
check_png "assets/overlays/kite-power-overlay-clean-8frame.png" "PNG image data, 1536 x 1024, 8-bit/color RGBA, non-interlaced"
check_png "reference/powerups-branded-reference.png" "PNG image data, 1448 x 1086, 8-bit/color RGBA, non-interlaced"
check_png "reference/taco-power-overlay-branded-reference.png" "PNG image data, 1448 x 1086, 8-bit/color RGB, non-interlaced"
check_png "reference/kite-power-overlay-branded-reference.png" "PNG image data, 1448 x 1086, 8-bit/color RGB, non-interlaced"

printf 'Power-up source import: PASS (3 working sources, 3 references)\n'
