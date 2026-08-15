#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
cd "$repo_root"

if ! command -v rg >/dev/null 2>&1; then
	echo "policy dependency error: required command not found: rg" >&2
	exit 1
fi

if ! tracked_files="$(git ls-files)"; then
	echo "policy dependency error: git ls-files failed" >&2
	exit 1
fi

RG_MATCHES=""
capture_rg_input() {
	local pattern="$1"
	local input="$2"
	local mode="${3:-match}"
	local rg_status=0
	set +e
	if [[ "$mode" == "invert" ]]; then
		RG_MATCHES="$(printf '%s\n' "$input" | rg -v -- "$pattern")"
		rg_status=$?
	else
		RG_MATCHES="$(printf '%s\n' "$input" | rg -- "$pattern")"
		rg_status=$?
	fi
	set -e
	if [[ "$rg_status" -gt 1 ]]; then
		printf 'policy dependency error: rg failed with status %s for pattern %s\n' \
			"$rg_status" \
			"$pattern" >&2
		exit 1
	fi
	if [[ "$rg_status" -eq 1 ]]; then
		RG_MATCHES=""
	fi
}

reject_tracked_paths() {
	local rule="$1"
	local pattern="$2"
	local exception_pattern="${3:-}"
	local matches=""
	capture_rg_input "$pattern" "$tracked_files"
	matches="$RG_MATCHES"
	if [[ -n "$matches" && -n "$exception_pattern" ]]; then
		capture_rg_input "$exception_pattern" "$matches" "invert"
		matches="$RG_MATCHES"
	fi
	if [[ -z "$matches" ]]; then
		return
	fi
	while IFS= read -r matched_file; do
		printf '%s: %s\n' "$matched_file" "$rule" >&2
	done <<< "$matches"
	printf 'policy violation: %s\n' "$rule" >&2
	exit 1
}

reject_content() {
	local rule="$1"
	local pattern="$2"
	shift 2
	local matches=""
	local rg_status=0
	set +e
	matches="$(rg -H -n -i -- "$pattern" "$@")"
	rg_status=$?
	set -e
	if [[ "$rg_status" -gt 1 ]]; then
		printf 'policy dependency error: rg failed with status %s for rule %s\n' \
			"$rg_status" \
			"$rule" >&2
		exit 1
	fi
	if [[ "$rg_status" -eq 1 ]]; then
		return
	fi
	printf '%s\n' "$matches" >&2
	printf 'policy violation: %s\n' "$rule" >&2
	exit 1
}

reject_tracked_paths \
	"tracked generated output" \
	'(^|/)(\.godot|\.import|export|exports|logs?)(/|$)|\.(log|import)$'
reject_tracked_paths \
	"tracked generated output" \
	'(^|/)build(/|$)' \
	'^src/core/build(/|$)'
reject_tracked_paths \
	"tracked credential, certificate, profile, or keystore" \
	'(^|/)(credentials?|secrets?)([._/-]|$)|\.(keystore|jks|p12|pfx|pem|cer|crt|profile|mobileprovision|provisionprofile)$' \
	'^docs/design/trash-dash/library/'
reject_tracked_paths \
	"tracked generated UID cache" \
	'(^|/)(uid_cache\.bin|global_script_class_cache\.cfg)$'

capture_rg_input '^(assets|scenes|src)/' "$tracked_files"
production_scope_files="$RG_MATCHES"
unexpected_production_paths=""
while IFS= read -r production_file; do
	if [[ -z "$production_file" ]]; then
		continue
	fi
	case "$production_file" in
		assets/generated/* \
		| assets/runtime/.gitkeep \
		| scenes/bootstrap/bootstrap.tscn \
		| src/actors/.gitkeep \
		| src/core/.gitkeep \
		| src/core/bootstrap/bootstrap_controller.gd \
		| src/core/bootstrap/foundation_status.gd \
		| src/core/bootstrap/project_settings_adapter.gd \
		| src/core/bootstrap/startup_validator.gd \
		| src/core/build/build_identity.gd \
		| src/core/display/display_policy.gd \
		| src/core/input/input_map_adapter.gd \
		| src/core/input/input_map_contract.gd \
		| src/core/input/input_remap_service.gd \
		| src/core/schema/animation_manifest.gd \
		| src/core/schema/animation_manifest_validator.gd \
		| src/core/schema/animation_state_ref.gd \
		| src/core/schema/animation_state_ref_validator.gd \
		| src/core/schema/asset_ref.gd \
		| src/core/schema/asset_ref_validator.gd \
		| src/core/schema/collision_geometry.gd \
		| src/core/schema/collision_geometry_validator.gd \
		| src/core/schema/encounter.gd \
		| src/core/schema/encounter_validator.gd \
		| src/core/schema/render_object_ref.gd \
		| src/core/schema/render_object_ref_validator.gd \
		| src/core/schema/rendering_layer.gd \
		| src/core/services/audio_service.gd \
		| src/core/services/live_scene_transition_service.gd \
		| src/core/services/runtime_state_service.gd \
		| src/core/services/save_settings_service.gd \
		| src/core/services/scene_transition_service.gd \
		| src/core/services/service_registry.gd \
		| src/core/services/service_result.gd \
		| src/core/services/unavailable_audio_service.gd \
		| src/core/services/unavailable_runtime_state_service.gd \
		| src/core/services/unavailable_save_settings_service.gd \
		| src/core/services/unavailable_scene_transition_service.gd \
		| src/core/time/fixed_step_clock.gd \
		| src/gameplay/.gitkeep \
		| src/levels/.gitkeep \
		| src/rendering/.gitkeep \
		| src/ui/.gitkeep \
		| src/ui/bootstrap/bootstrap_view.gd \
		| src/world/.gitkeep)
			;;
		*)
			unexpected_production_paths+="${production_file}"$'\n'
			;;
	esac
done <<< "$production_scope_files"
unexpected_production_paths="${unexpected_production_paths%$'\n'}"
if [[ -n "$unexpected_production_paths" ]]; then
	while IFS= read -r matched_file; do
		printf '%s: path is outside the macOS foundation production allowlist\n' \
			"$matched_file" >&2
	done <<< "$unexpected_production_paths"
	echo "policy violation: unexpected production path" >&2
	exit 1
fi

capture_rg_input '^tests/' "$tracked_files"
unexpected_test_paths="$RG_MATCHES"
if [[ -n "$unexpected_test_paths" ]]; then
	capture_rg_input \
		'^tests/run_all\.gd$|^tests/(gameplay|support|unit|visual)/(\.gitkeep|[^/]+\.gd)$|^tests/library/[^/]+\.py$' \
		"$unexpected_test_paths" \
		"invert"
	unexpected_test_paths="$RG_MATCHES"
fi
if [[ -n "$unexpected_test_paths" ]]; then
	while IFS= read -r matched_file; do
		printf '%s: unexpected tracked test path\n' "$matched_file" >&2
	done <<< "$unexpected_test_paths"
	echo "policy violation: unexpected tracked test path" >&2
	exit 1
fi

capture_rg_input '^tools/verify/' "$tracked_files"
unexpected_verify_paths="$RG_MATCHES"
if [[ -n "$unexpected_verify_paths" ]]; then
	capture_rg_input \
		'^tools/verify/(check_policy|check_character_animation_import|check_powerup_source_import|run_tests|export_macos|verify_local|run_bounded_process|test_shell_contracts|godot_diagnostics|godot_log_safety)\.sh$|^tools/verify/[^/]+\.py$' \
		"$unexpected_verify_paths" \
		"invert"
	unexpected_verify_paths="$RG_MATCHES"
fi
if [[ -n "$unexpected_verify_paths" ]]; then
	while IFS= read -r matched_file; do
		printf '%s: unexpected tracked verification path\n' "$matched_file" >&2
	done <<< "$unexpected_verify_paths"
	echo "policy violation: unexpected tracked verification path" >&2
	exit 1
fi

capture_rg_input \
	'^(project\.godot|export_presets\.cfg|scenes/|src/|docs/development/)' \
	"$tracked_files"
scan_files=()
while IFS= read -r tracked_file; do
	if [[ -n "$tracked_file" ]]; then
		scan_files+=("$tracked_file")
	fi
done <<< "$RG_MATCHES"

capture_rg_input \
	'^(project\.godot|export_presets\.cfg|scenes/|src/)' \
	"$tracked_files"
production_scan_files=()
while IFS= read -r tracked_file; do
	if [[ -n "$tracked_file" ]]; then
		production_scan_files+=("$tracked_file")
	fi
done <<< "$RG_MATCHES"

if [[ "${#production_scan_files[@]}" -gt 0 ]]; then
	reject_content \
		"production credential or signing assignment" \
		'^[[:space:]]*((var|const)[[:space:]]+)?[[:alnum:]_./-]*(team[_ /-]?id|api[_ /-]?token|token|password|private[_ /-]?key|certificate|profile|identity|pem)[[:alnum:]_./ -]*[[:space:]]*:?=[[:space:]]*[\x22\x27]' \
		"${production_scan_files[@]}"
	reject_content \
		"production private-key or certificate material" \
		'-----BEGIN[[:space:]]+((RSA|EC|OPENSSH)[[:space:]]+)?(PRIVATE KEY|CERTIFICATE)-----|(Developer ID Application|Developer ID Installer|Apple Development|Apple Distribution):[[:space:]]|[\x22\x27][^\x22\x27]+\.(p12|pfx|pem|cer|crt|mobileprovision|provisionprofile)[\x22\x27]' \
		"${production_scan_files[@]}"
fi

if [[ "${#scan_files[@]}" -gt 0 ]]; then
	reject_content \
		"sibling V1 source reference" \
		'(\.\./)+trash-dash/|/trash-dash/' \
		"${scan_files[@]}"
	reject_content \
		"archive source reference" \
		'archive/' \
		"${scan_files[@]}"
	reject_content \
		"deleted spike or fixture resource reference" \
		'spike/native-foundation|res://[^"[:space:]]*(spike|fixture)' \
		"${scan_files[@]}"
	reject_content \
		"concept or reference-sheet runtime resource" \
		'res://[^"[:space:]]*(concept|reference|sprite[-_]?sheet)' \
		"${scan_files[@]}"
	reject_content \
		"absolute user path" \
		'/Users/|/home/|(^|[^[:alnum:]_])[[:alpha:]]:[/\\]' \
		"${scan_files[@]}"
fi

reject_content \
	"deferred export platform preset" \
	'^(name|platform)="(Windows Desktop|Android|iOS|Linux|Web)"' \
	export_presets.cfg
reject_content \
	"credential or secret-looking export assignment" \
	'^[^=]*(team[_ -]?id|certificate|identity|password|provisioning[_ -]?profile|secret|token|api[_ -]?key|private[_ -]?key)[^=]*=' \
	export_presets.cfg
reject_content \
	"production autoload" \
	'^\[autoload\]' \
	project.godot

shell_files=(
	tools/verify/check_policy.sh
	tools/verify/check_character_animation_import.sh
	tools/verify/check_powerup_source_import.sh
	tools/verify/run_tests.sh
	tools/verify/export_macos.sh
	tools/verify/godot_diagnostics.sh
	tools/verify/godot_log_safety.sh
	tools/verify/verify_local.sh
	tools/verify/run_bounded_process.sh
	tools/verify/test_shell_contracts.sh
)
existing_shell_files=()
for shell_file in "${shell_files[@]}"; do
	if [[ -f "$shell_file" ]]; then
		if ! bash -n "$shell_file"; then
			printf '%s: invalid shell syntax\n' "$shell_file" >&2
			exit 1
		fi
		existing_shell_files+=("$shell_file")
	fi
done
if [[ "${#existing_shell_files[@]}" -gt 0 ]]; then
	# Split literal command names so this policy's own data does not resemble an
	# executable statement when check_policy.sh is included in the source scan.
	forbidden_command='(code''sign|notary''tool|al''tool|xc''run|xcode''build|cu''rl|wg''et|sc''p|rs''ync|su''do|osa''script|security[[:space:]]+(find-''identity|find-''certificate)|git[[:space:]]+(cl''ean|res''et|check''out))'
	execution_prefix='(^[[:space:]]*|[;&|][[:space:]]*|[$][(][[:space:]]*|^[[:space:]]*(if|elif|while|until)[[:space:]]+!?[[:space:]]*|^[[:space:]]*(then|do)[[:space:]]+|^[[:space:]]*![[:space:]]*)'
	reject_content \
		"signing, notarization, upload, credential-discovery, or broad Git command" \
		"${execution_prefix}${forbidden_command}([;&|)[:space:]]|$)" \
		"${existing_shell_files[@]}"
	reject_content \
		"unbounded recursive removal" \
		'(^[[:space:]]*|[;&|][[:space:]]*|[$][(][[:space:]]*)rm[[:space:]]+(-[^[:space:]]*r[^[:space:]]*f|-rf|-fr)([[:space:]]|$)' \
		"${existing_shell_files[@]}"
fi

python3 tools/verify/validate_design_library.py
python3 tools/verify/audit_canonical_assets.py

echo "Policy: PASS"
