#!/usr/bin/env bash

godot_diagnostic_pattern='(^|[[:space:]])(SCRIPT ERROR|ERROR|WARNING|FATAL|PANIC):|ObjectDB instances leaked|Resources still in use at exit|orphan StringName|RID allocations leaked|handle_crash:|Program crashed'

check_godot_diagnostics() {
	if [[ "$#" -ne 2 ]]; then
		echo "Usage: check_godot_diagnostics <stage-name> <log-file>" >&2
		return 64
	fi
	local stage_name="$1"
	local log_file="$2"
	if ! command -v rg >/dev/null 2>&1; then
		echo "Godot diagnostic dependency error: required command not found: rg" >&2
		return 65
	fi
	if [[ ! -f "$log_file" ]]; then
		printf 'Godot stage log is missing for %s: %s\n' "$stage_name" "$log_file" >&2
		return 66
	fi
	local had_errexit=false
	case $- in
		*e*) had_errexit=true ;;
	esac
	local diagnostic_matches=""
	local diagnostic_status=0
	set +e
	diagnostic_matches="$(LC_ALL=C LANG=C rg -n -i -- "$godot_diagnostic_pattern" "$log_file")"
	diagnostic_status=$?
	if [[ "$had_errexit" == true ]]; then
		set -e
	fi
	if [[ "$diagnostic_status" -gt 1 ]]; then
		printf 'Godot diagnostic scan failed for %s with status %s\n' \
			"$stage_name" \
			"$diagnostic_status" >&2
		return 67
	fi
	if [[ "$diagnostic_status" -eq 0 ]]; then
		printf '%s\n' "$diagnostic_matches" >&2
		printf 'Godot stage diagnostic failure: %s\n' "$stage_name" >&2
		return 68
	fi
	return 0
}

run_godot_stage() {
	if [[ "$#" -lt 3 ]]; then
		echo "Usage: run_godot_stage <stage-name> <log-file> <command> [args...]" >&2
		return 64
	fi
	local stage_name="$1"
	local log_file="$2"
	shift 2
	local log_parent
	log_parent="$(dirname "$log_file")"
	if [[ "$log_file" != /* || ! -d "$log_parent" || -L "$log_parent" || -L "$log_file" ]]; then
		printf 'Godot stage log must use an absolute path under an existing non-symlink parent: %s\n' \
			"$log_file" >&2
		return 64
	fi
	local had_errexit=false
	case $- in
		*e*) had_errexit=true ;;
	esac
	local command_status=0
	set +e
	"$@" > "$log_file" 2>&1
	command_status=$?
	if [[ "$had_errexit" == true ]]; then
		set -e
	fi
	cat "$log_file"
	local diagnostic_result=0
	set +e
	check_godot_diagnostics "$stage_name" "$log_file"
	diagnostic_result=$?
	if [[ "$had_errexit" == true ]]; then
		set -e
	fi
	if [[ "$diagnostic_result" -ne 0 ]]; then
		return "$diagnostic_result"
	fi
	return "$command_status"
}
