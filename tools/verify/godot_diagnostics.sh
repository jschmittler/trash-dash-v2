#!/usr/bin/env bash

godot_diagnostics_script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
. "$godot_diagnostics_script_dir/godot_log_safety.sh"

godot_diagnostic_pattern='(^|[[:space:]])(SCRIPT ERROR|ERROR|WARNING|FATAL|PANIC):|ObjectDB instances leaked|Resources still in use at exit|orphan StringName|RID allocations leaked|handle_crash:|Program crashed'

check_godot_diagnostics() {
	if [[ "$#" -lt 2 ]]; then
		echo "Usage: check_godot_diagnostics <stage-name> <log-file> [log-file...]" >&2
		return 64
	fi
	local stage_name="$1"
	shift
	if ! command -v rg >/dev/null 2>&1; then
		echo "Godot diagnostic dependency error: required command not found: rg" >&2
		return 65
	fi
	local log_file
	for log_file in "$@"; do
		if [[ ! -f "$log_file" ]]; then
			printf 'Godot stage log is missing for %s: %s\n' "$stage_name" "$log_file" >&2
			return 66
		fi
	done
	local had_errexit=false
	case $- in
	*e*) had_errexit=true ;;
	esac
	local diagnostic_matches=""
	local diagnostic_status=0
	set +e
	diagnostic_matches="$(LC_ALL=C LANG=C rg -n -i -- "$godot_diagnostic_pattern" "$@")"
	diagnostic_status=$?
	if [[ "$had_errexit" == true ]]; then
		set -e
	fi
	if [[ "$diagnostic_status" -gt 1 ]]; then
		printf 'Godot diagnostic scan failed for %s with status %s\n' \
			"$stage_name" "$diagnostic_status" >&2
		return 67
	fi
	if [[ "$diagnostic_status" -eq 0 ]]; then
		printf '%s\n' "$diagnostic_matches" >&2
		printf 'Godot stage diagnostic failure: %s\n' "$stage_name" >&2
		return 68
	fi
	return 0
}

print_godot_failure() {
	local stage_name="$1"
	local status="$2"
	shift 2
	printf 'Godot stage exited nonzero: %s (status %s)\n' "$stage_name" "$status" >&2
	printf 'Godot command:' >&2
	printf ' %q' "$@" >&2
	printf '\nGodot engine log: %s\nGodot output log: %s\n' \
		"$godot_log_engine_file" "$godot_log_output_file" >&2
}

run_godot_stage() {
	if [[ "$#" -lt 4 ]]; then
		echo "Usage: run_godot_stage <project-root> <stage-name> <purpose> <godot-command> [args...]" >&2
		return 64
	fi
	local project_root="$1"
	local stage_name="$2"
	local purpose="$3"
	local godot_command="$4"
	shift 4
	prepare_godot_log_files "$project_root" "$purpose" || return $?
	acquire_godot_process_lock || return $?
	local had_errexit=false
	case $- in
	*e*) had_errexit=true ;;
	esac
	local command_status=0
	set +e
	"$godot_command" --log-file "$godot_log_engine_file" "$@" \
		> "$godot_log_output_file" 2>&1
	command_status=$?
	if [[ "$had_errexit" == true ]]; then
		set -e
	fi
	local release_status=0
	release_godot_process_lock || release_status=$?
	cat "$godot_log_output_file"
	local diagnostic_result=0
	set +e
	check_godot_diagnostics \
		"$stage_name" "$godot_log_engine_file" "$godot_log_output_file"
	diagnostic_result=$?
	if [[ "$had_errexit" == true ]]; then
		set -e
	fi
	if [[ "$release_status" -ne 0 ]]; then
		return "$release_status"
	fi
	if [[ "$diagnostic_result" -ne 0 ]]; then
		return "$diagnostic_result"
	fi
	if [[ "$command_status" -ne 0 ]]; then
		print_godot_failure \
			"$stage_name" "$command_status" \
			"$godot_command" --log-file "$godot_log_engine_file" "$@"
	fi
	return "$command_status"
}
