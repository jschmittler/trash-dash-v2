#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
cd "$repo_root"

tracked_files="$(git ls-files)"

reject_tracked_paths() {
	local rule="$1"
	local pattern="$2"
	local matches=""
	if matches="$(printf '%s\n' "$tracked_files" | rg "$pattern")"; then
		while IFS= read -r matched_file; do
			printf '%s: %s\n' "$matched_file" "$rule" >&2
		done <<< "$matches"
		printf 'policy violation: %s\n' "$rule" >&2
		exit 1
	fi
}

reject_content() {
	local rule="$1"
	local pattern="$2"
	shift 2
	local matches=""
	if matches="$(rg -n -i -- "$pattern" "$@")"; then
		printf '%s\n' "$matches" >&2
		printf 'policy violation: %s\n' "$rule" >&2
		exit 1
	fi
}

reject_tracked_paths \
	"tracked generated output" \
	'(^|/)(\.godot|\.import)(/|$)|^(build|export|exports|logs?)/|\.(log|import)$'
reject_tracked_paths \
	"tracked credential, certificate, profile, or keystore" \
	'(^|/)(credentials?|secrets?)([._-]|$)|\.(keystore|jks|p12|pfx|pem|cer|crt|profile|mobileprovision|provisionprofile)$'
reject_tracked_paths \
	"tracked generated UID cache" \
	'(^|/)(uid_cache\.bin|global_script_class_cache\.cfg)$'

restricted_scope_matches="$(
	printf '%s\n' "$tracked_files" \
		| rg '^(assets/runtime|src/actors|src/gameplay|src/levels|src/rendering|src/world)/' \
		| rg -v '/\.gitkeep$' \
		|| true
)"
if [[ -n "$restricted_scope_matches" ]]; then
	while IFS= read -r matched_file; do
		printf '%s: production content root must remain empty\n' "$matched_file" >&2
	done <<< "$restricted_scope_matches"
	echo "policy violation: production content root must remain empty" >&2
	exit 1
fi

unexpected_test_paths="$(
	printf '%s\n' "$tracked_files" \
		| rg '^tests/' \
		| rg -v '^tests/run_all\.gd$|^tests/(gameplay|support|unit|visual)/(\.gitkeep|[^/]+\.gd)$' \
		|| true
)"
if [[ -n "$unexpected_test_paths" ]]; then
	while IFS= read -r matched_file; do
		printf '%s: unexpected tracked test path\n' "$matched_file" >&2
	done <<< "$unexpected_test_paths"
	echo "policy violation: unexpected tracked test path" >&2
	exit 1
fi

unexpected_verify_paths="$(
	printf '%s\n' "$tracked_files" \
		| rg '^tools/verify/' \
		| rg -v '^tools/verify/(check_policy|run_tests|export_macos|verify_local)\.sh$' \
		|| true
)"
if [[ -n "$unexpected_verify_paths" ]]; then
	while IFS= read -r matched_file; do
		printf '%s: unexpected tracked verification path\n' "$matched_file" >&2
	done <<< "$unexpected_verify_paths"
	echo "policy violation: unexpected tracked verification path" >&2
	exit 1
fi

scan_files=()
while IFS= read -r tracked_file; do
	if [[ -n "$tracked_file" ]]; then
		scan_files+=("$tracked_file")
	fi
done < <(
	printf '%s\n' "$tracked_files" \
		| rg '^(project\.godot|export_presets\.cfg|scenes/|src/|docs/development/)' \
		|| true
)

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
	tools/verify/run_tests.sh
	tools/verify/export_macos.sh
	tools/verify/verify_local.sh
)
existing_shell_files=()
for shell_file in "${shell_files[@]}"; do
	if [[ -f "$shell_file" ]]; then
		existing_shell_files+=("$shell_file")
	fi
done
if [[ "${#existing_shell_files[@]}" -gt 0 ]]; then
	reject_content \
		"signing, notarization, upload, credential-discovery, or broad Git command" \
		'(^|[;&|[:space:]])(codesign|notarytool|altool|xcrun|xcodebuild|curl|wget|scp|rsync|sudo|osascript)([;&|[:space:]]|$)|security[[:space:]]+(find-identity|find-certificate)|git[[:space:]]+(clean|reset|checkout)' \
		"${existing_shell_files[@]}"
	reject_content \
		"unbounded recursive removal" \
		'rm[[:space:]]+(-[^[:space:]]*r[^[:space:]]*f|-rf|-fr)([[:space:]]|$)' \
		"${existing_shell_files[@]}"
fi

echo "Policy: PASS"
