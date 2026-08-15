#!/usr/bin/env bash

godot_log_project_root=""
godot_log_directory=""
godot_log_engine_file=""
godot_log_output_file=""
godot_log_lock_directory=""
godot_log_lock_held=false

prepare_godot_log_directory() {
	if [[ "$#" -ne 1 ]]; then
		echo "Usage: prepare_godot_log_directory <project-root>" >&2
		return 64
	fi
	local requested_root="$1"
	if [[ ! -d "$requested_root" || -L "$requested_root" ]]; then
		printf 'Godot project root must be an existing non-symlink directory: %s\n' \
			"$requested_root" >&2
		return 64
	fi
	local canonical_root
	canonical_root="$(cd "$requested_root" && pwd -P)" || return 64
	if [[ ! -f "$canonical_root/project.godot" || -L "$canonical_root/project.godot" ]]; then
		printf 'Godot project root does not contain a regular project.godot: %s\n' \
			"$canonical_root" >&2
		return 64
	fi
	local requested_log_directory="$canonical_root/.codex/godot-logs"
	if [[ -L "$canonical_root/.codex" || -L "$requested_log_directory" ]]; then
		printf 'Godot log path cannot contain a symbolic-link boundary: %s\n' \
			"$requested_log_directory" >&2
		return 64
	fi
	if ! mkdir -p -- "$requested_log_directory"; then
		printf 'Cannot create project-local Godot log directory: %s\n' \
			"$requested_log_directory" >&2
		return 73
	fi
	local canonical_log_directory
	canonical_log_directory="$(cd "$requested_log_directory" && pwd -P)" || return 73
	if [[ "$canonical_log_directory" != "$canonical_root/.codex/godot-logs" ]]; then
		printf 'Godot log directory escaped the project workspace: %s\n' \
			"$canonical_log_directory" >&2
		return 73
	fi
	local write_probe="$canonical_log_directory/.codex-write-probe-$$"
	if ! (umask 077 && : > "$write_probe"); then
		printf 'Godot log directory is not writable: %s\n' \
			"$canonical_log_directory" >&2
		return 73
	fi
	if ! rm -- "$write_probe"; then
		printf 'Cannot clean Godot log write probe: %s\n' "$write_probe" >&2
		return 73
	fi
	godot_log_project_root="$canonical_root"
	godot_log_directory="$canonical_log_directory"
	godot_log_lock_directory="$canonical_log_directory/.process-lock"
	return 0
}

prepare_godot_log_files() {
	if [[ "$#" -ne 2 ]]; then
		echo "Usage: prepare_godot_log_files <project-root> <purpose>" >&2
		return 64
	fi
	local requested_root="$1"
	local purpose="$2"
	if [[ ! "$purpose" =~ ^[a-z0-9][a-z0-9._-]*$ ]]; then
		printf 'Invalid Godot log purpose: %s\n' "$purpose" >&2
		return 64
	fi
	prepare_godot_log_directory "$requested_root" || return $?
	godot_log_engine_file="$godot_log_directory/$purpose.log"
	godot_log_output_file="$godot_log_directory/$purpose.output.log"
	for log_file in "$godot_log_engine_file" "$godot_log_output_file"; do
		if [[ -L "$log_file" ]]; then
			printf 'Godot log file cannot be a symbolic link: %s\n' "$log_file" >&2
			return 64
		fi
		if ! (umask 077 && : > "$log_file"); then
			printf 'Cannot write project-local Godot log file: %s\n' "$log_file" >&2
			return 73
		fi
	done
	return 0
}

acquire_godot_process_lock() {
	if [[ -z "$godot_log_lock_directory" ]]; then
		echo "Godot log directory must be prepared before acquiring its process lock" >&2
		return 64
	fi
	if ! mkdir -- "$godot_log_lock_directory" 2>/dev/null; then
		printf 'Another Codex-initiated Godot process may already be active; lock exists: %s\n' \
			"$godot_log_lock_directory" >&2
		return 75
	fi
	printf '%s\n' "$$" > "$godot_log_lock_directory/owner-pid"
	godot_log_lock_held=true
}

release_godot_process_lock() {
	if [[ "$godot_log_lock_held" != true ]]; then
		return 0
	fi
	if [[ ! -d "$godot_log_lock_directory" || -L "$godot_log_lock_directory" ]]; then
		printf 'Godot process lock cannot be safely released: %s\n' \
			"$godot_log_lock_directory" >&2
		return 1
	fi
	if [[ -f "$godot_log_lock_directory/owner-pid" ]] \
		&& [[ "$(sed -n '1p' "$godot_log_lock_directory/owner-pid")" != "$$" ]]; then
		printf 'Godot process lock ownership changed unexpectedly: %s\n' \
			"$godot_log_lock_directory" >&2
		return 1
	fi
	rm -f -- "$godot_log_lock_directory/owner-pid"
	rmdir -- "$godot_log_lock_directory"
	godot_log_lock_held=false
}
