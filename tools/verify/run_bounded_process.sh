#!/usr/bin/env bash
set -euo pipefail

bounded_process_pid=""
bounded_process_reaped=false
bounded_process_status=""
bounded_process_absence_confirmed=false
bounded_process_grace_attempts="${TRASH_DASH_PROCESS_GRACE_ATTEMPTS:-20}"
bounded_process_poll_seconds="${TRASH_DASH_PROCESS_POLL_SECONDS:-0.1}"
bounded_process_startup_delay="${TRASH_DASH_PROCESS_STARTUP_DELAY_SECONDS:-2}"

bounded_process_validate_settings() {
	if [[ ! "$bounded_process_grace_attempts" =~ ^[1-9][0-9]?$|^100$ ]]; then
		printf 'Invalid process grace attempts: %s\n' "$bounded_process_grace_attempts" >&2
		return 1
	fi
	if [[ ! "$bounded_process_poll_seconds" =~ ^(0|0\.[0-9]+|[1-5](\.[0-9]+)?)$ ]]; then
		printf 'Invalid process poll seconds: %s\n' "$bounded_process_poll_seconds" >&2
		return 1
	fi
	if [[ ! "$bounded_process_startup_delay" =~ ^(0|0\.[0-9]+|[1-4](\.[0-9]+)?|5(\.0+)?)$ ]]; then
		printf 'Invalid process startup delay: %s\n' "$bounded_process_startup_delay" >&2
		return 1
	fi
}

bounded_process_poll_until_absent() {
	local attempt=0
	while [[ "$attempt" -lt "$bounded_process_grace_attempts" ]]; do
		if ! kill -0 "$bounded_process_pid" 2>/dev/null; then
			bounded_process_absence_confirmed=true
			return 0
		fi
		sleep "$bounded_process_poll_seconds"
		attempt=$((attempt + 1))
	done
	return 1
}

bounded_process_reap() {
	if [[ -z "$bounded_process_pid" || "$bounded_process_reaped" == true ]]; then
		return
	fi
	if [[ "$bounded_process_absence_confirmed" != true ]]; then
		printf 'Refusing to wait before exact PID absence is confirmed: %s\n' \
			"$bounded_process_pid" >&2
		return 1
	fi
	set +e
	wait "$bounded_process_pid"
	bounded_process_status=$?
	set -e
	bounded_process_reaped=true
}

bounded_process_cleanup() {
	if [[ -z "$bounded_process_pid" || "$bounded_process_reaped" == true ]]; then
		return 0
	fi
	local forced_kill=false
	if kill -0 "$bounded_process_pid" 2>/dev/null; then
		kill -TERM "$bounded_process_pid" 2>/dev/null || true
		if ! bounded_process_poll_until_absent; then
			forced_kill=true
			kill -KILL "$bounded_process_pid" 2>/dev/null || true
			if ! bounded_process_poll_until_absent; then
				printf 'Package process remains after bounded KILL poll: %s\n' \
					"$bounded_process_pid" >&2
				return 1
			fi
		fi
	else
		bounded_process_absence_confirmed=true
	fi
	bounded_process_reap || return 1
	if kill -0 "$bounded_process_pid" 2>/dev/null; then
		printf 'Package process remains after cleanup: %s\n' "$bounded_process_pid" >&2
		return 1
	fi
	if [[ "$forced_kill" == true ]]; then
		printf 'Cleanup process fallback: KILL (PID %s absent)\n' "$bounded_process_pid" >&2
		return 1
	fi
	printf 'Cleanup process: PASS (PID %s absent)\n' "$bounded_process_pid" >&2
	return 0
}

run_bounded_process() {
	if [[ "$#" -lt 2 ]]; then
		echo "Usage: tools/verify/run_bounded_process.sh <log-file> <command> [args...]" >&2
		return 64
	fi
	bounded_process_validate_settings || return 64
	local log_file="$1"
	shift
	if [[ "$log_file" != /* || -L "$log_file" || ! -d "$(dirname "$log_file")" ]]; then
		printf 'Process log must be an absolute path under an existing non-symlink parent: %s\n' \
			"$log_file" >&2
		return 64
	fi
	if [[ -L "$(dirname "$log_file")" ]]; then
		printf 'Process log parent cannot be a symlink: %s\n' "$(dirname "$log_file")" >&2
		return 64
	fi

	bounded_process_pid=""
	bounded_process_reaped=false
	bounded_process_status=""
	bounded_process_absence_confirmed=false
	LC_ALL=C LANG=C /usr/bin/perl -e \
		'$SIG{INT} = "DEFAULT"; $SIG{TERM} = "DEFAULT"; exec {$ARGV[0]} @ARGV or die "exec failed: $!\n"' \
		"$@" > "$log_file" 2>&1 &
	bounded_process_pid=$!
	printf 'Package PID: %s\n' "$bounded_process_pid"
	sleep "$bounded_process_startup_delay"
	if ! kill -0 "$bounded_process_pid" 2>/dev/null; then
		bounded_process_absence_confirmed=true
		bounded_process_reap || return 1
		printf 'Package exited before SIGINT with status %s\n' "$bounded_process_status" >&2
		return 1
	fi

	kill -INT "$bounded_process_pid"
	if bounded_process_poll_until_absent; then
		bounded_process_reap || return 1
		if [[ "$bounded_process_status" -ne 130 ]]; then
			printf 'Package did not exit cleanly after SIGINT: %s\n' \
				"$bounded_process_status" >&2
			return 1
		fi
		printf 'Process cleanup: PASS (PID %s absent, expected SIGINT exit 130)\n' \
			"$bounded_process_pid"
		return 0
	fi

	printf 'Package ignored SIGINT within bounded grace: %s\n' "$bounded_process_pid" >&2
	kill -TERM "$bounded_process_pid" 2>/dev/null || true
	if bounded_process_poll_until_absent; then
		bounded_process_reap || return 1
		printf 'Forced process fallback: TERM (PID %s absent, status %s)\n' \
			"$bounded_process_pid" \
			"$bounded_process_status" >&2
		return 1
	fi

	kill -KILL "$bounded_process_pid" 2>/dev/null || true
	if ! bounded_process_poll_until_absent; then
		printf 'Package process remains after bounded KILL poll: %s\n' \
			"$bounded_process_pid" >&2
		return 1
	fi
	bounded_process_reap || return 1
	printf 'Forced process fallback: KILL (PID %s absent, status %s)\n' \
		"$bounded_process_pid" \
		"$bounded_process_status" >&2
	return 1
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
	bounded_process_exit_cleanup() {
		local original_status=$?
		trap - EXIT INT TERM
		local cleanup_status=0
		bounded_process_cleanup || cleanup_status=$?
		if [[ "$cleanup_status" -ne 0 ]]; then
			exit "$cleanup_status"
		fi
		exit "$original_status"
	}
	trap bounded_process_exit_cleanup EXIT
	trap 'exit 130' INT
	trap 'exit 143' TERM
	run_bounded_process "$@"
fi
