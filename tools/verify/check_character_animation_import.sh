#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)"
repo_root="$(CDPATH= cd -- "$script_dir/../.." && pwd -P)"
import_root="$repo_root/docs/design/trash-dash/packages/character-animation/phase-05-codex-integration"
inventory="$import_root/CANONICAL_IMPORT_INVENTORY.json"
catalog="$repo_root/docs/design/trash-dash/manifests/library-catalog.json"

fail() {
  printf 'Character animation import: FAIL: %s\n' "$*" >&2
  exit 1
}

for command_name in cmp cut dirname file find git jq shasum sort tr wc; do
  command -v "$command_name" >/dev/null 2>&1 || fail "required command is unavailable: $command_name"
done

[ -d "$import_root" ] || fail "import root is missing: $import_root"
[ -f "$inventory" ] || fail "inventory is missing: $inventory"
[ -f "$catalog" ] || fail "library catalog is missing: $catalog"

for required_file in \
  "$import_root/README.md" \
  "$import_root/ASSET_MAP.md" \
  "$import_root/CODEX_IMPORT_AND_INTEGRATION_PROMPT.md" \
  "$import_root/FRAME_METADATA_SCHEMA.json" \
  "$import_root/run-manifest.json" \
  "$import_root/qa/SHA256SUMS" \
  "$import_root/phase-01-approved-main-characters/manifest.json" \
  "$import_root/phase-02/run-manifest.json" \
  "$import_root/phase-03-variable/run-manifest.json" \
  "$import_root/phase-04-bosses/run-manifest.json"; do
  [ -f "$required_file" ] || fail "required handoff file is missing: ${required_file#"$repo_root/"}"
done

for json_file in \
  "$inventory" \
  "$import_root/FRAME_METADATA_SCHEMA.json" \
  "$import_root/run-manifest.json" \
  "$import_root/phase-01-approved-main-characters/manifest.json" \
  "$import_root/phase-02/run-manifest.json" \
  "$import_root/phase-03-variable/run-manifest.json" \
  "$import_root/phase-04-bosses/run-manifest.json"; do
  jq empty "$json_file" >/dev/null || fail "invalid JSON: ${json_file#"$repo_root/"}"
done

jq -e '
  .format_version == 1 and
  .handoff == "phase-05-codex-integration" and
  .status == "import-audited" and
  .runtime_extraction_started == false and
  .canonical_atlas_count == 36 and
  (.assets | length) == 36 and
  ([.assets[].asset_id] | unique | length) == 36 and
  ([.assets[].approved_atlas] | unique | length) == 36 and
  ([.assets[] | select(.asset_class == "playable_character")] | length) == 4 and
  ([.assets[] | select(.asset_class == "common_enemy")] | length) == 26 and
  ([.assets[] | select(.asset_class == "boss")] | length) == 6
' "$inventory" >/dev/null || fail "inventory shape, counts, or uniqueness is invalid"

expected_ids='alley-cat-burglar
asteroid-armadillo
baserunning-beaver
beaker-slime
bee
boss-brutus-bin-hound
boss-diamond-don
boss-galactogobbler
boss-pizza-rat-king
boss-project-opossum
boss-trash-dash
clipboard-hamster
clobbering-cub
dog
jimothy-powered
jimothy-regular
mop-bot-3000
mosquito
moth-dustwing
opossum-pilfer
phase-gecko
pigeon
rocket-roach
satellite-hermit-crab
sewer-rat-courier
skunk
sliding-seagull
snake
spider
squirrel
subway-roach
traffic-cone-crab
trashy-powered
trashy-regular
vacuum-jelly
windup-weasel'
actual_ids="$(jq -r '.assets[].asset_id' "$inventory" | LC_ALL=C sort)"
[ "$actual_ids" = "$expected_ids" ] || fail "canonical ID set does not match ASSET_MAP.md"

jq -r '.assets[] | [
  .asset_id,
  .approved_atlas,
  .approved_atlas_sha256,
  (.width | tostring),
  (.height | tostring),
  .source_reference,
  (.imported_source_reference // "")
] | @tsv' "$inventory" |
while IFS="$(printf '\t')" read -r asset_id atlas_rel expected_hash expected_width expected_height source_rel imported_source_rel; do
  case "$atlas_rel" in
    /*|*../*) fail "$asset_id has unsafe approved-atlas path: $atlas_rel" ;;
  esac
  case "$source_rel" in
    /*|*../*) fail "$asset_id has unsafe source-reference path: $source_rel" ;;
  esac

  atlas="$import_root/$atlas_rel"
  current_source_rel="$(jq -r --arg legacy "$source_rel" '
    [.assets[] | select(.aliases | index($legacy)) | .canonicalPath]
    | unique
    | if length == 1 then .[0] else empty end
  ' "$catalog")"
  [ -n "$current_source_rel" ] || fail "$asset_id source reference does not resolve uniquely through the library catalog: $source_rel"
  source="$repo_root/$current_source_rel"
  [ -f "$atlas" ] || fail "$asset_id approved atlas is missing: $atlas_rel"
  [ -f "$source" ] || fail "$asset_id source reference is missing: $source_rel"

  case "$expected_hash" in
    *[!0-9a-f]*|'') fail "$asset_id has an invalid SHA-256 value" ;;
  esac
  [ "${#expected_hash}" -eq 64 ] || fail "$asset_id SHA-256 is not 64 characters"
  actual_hash="$(LC_ALL=C LANG=C shasum -a 256 "$atlas" | cut -d ' ' -f 1)"
  [ "$actual_hash" = "$expected_hash" ] || fail "$asset_id atlas hash mismatch"

  file_description="$(file "$atlas")"
  case "$file_description" in
    *"PNG image data, $expected_width x $expected_height, 8-bit/color RGBA"*) ;;
    *) fail "$asset_id is not the expected alpha-capable PNG size: $file_description" ;;
  esac

  filter_attr="$(git -C "$repo_root" check-attr filter -- "$atlas")"
  case "$filter_attr" in
    *': filter: lfs') ;;
    *) fail "$asset_id atlas is not covered by Git LFS: $filter_attr" ;;
  esac

  if [ -n "$imported_source_rel" ]; then
    case "$imported_source_rel" in
      /*|*../*) fail "$asset_id has unsafe imported-source path: $imported_source_rel" ;;
    esac
    imported_source="$import_root/$imported_source_rel"
    [ -f "$imported_source" ] || fail "$asset_id imported source is missing: $imported_source_rel"
    cmp -s "$imported_source" "$source" || fail "$asset_id imported source conflicts with repository reference"
  fi
done

imported_source_count=0
for imported_source in \
  "$import_root"/phase-02/source-pack/characters/*/sprites/*.png \
  "$import_root"/phase-03-variable/source-pack/characters/*/sprites/*.png \
  "$import_root"/phase-04-bosses/source/*/*.png; do
  [ -f "$imported_source" ] || fail "expected imported branded source glob did not resolve"
  imported_source_count=$((imported_source_count + 1))
  source_name="${imported_source##*/}"
  repository_source="$(find "$repo_root/docs/design/trash-dash/library/characters" -type f -name "$source_name" -print)"
  [ -n "$repository_source" ] || fail "no repository reference resolves for imported source: $source_name"
  [ "$(printf '%s\n' "$repository_source" | wc -l | tr -d ' ')" -eq 1 ] || fail "multiple repository references resolve for imported source: $source_name"
  cmp -s "$imported_source" "$repository_source" || fail "imported branded source conflicts with repository reference: $source_name"
done
[ "$imported_source_count" -eq 38 ] || fail "expected 38 imported branded-source instances, got $imported_source_count"

printf 'Character animation import: PASS (36/36 canonical atlases)\n'
