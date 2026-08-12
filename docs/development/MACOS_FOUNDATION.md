# macOS Foundation Development Guide

This repository currently provides a macOS-only Godot foundation shell. Use Godot `4.7.1.stable.official.a13da4feb` Standard with matching macOS export templates, plus Git, ripgrep, `unzip`, `lipo`, and `shasum`.

The scripts use `godot` by default. To select the accepted executable explicitly for one command:

```bash
TRASH_DASH_GODOT_BIN=/opt/homebrew/bin/godot tools/verify/run_tests.sh
```

`TRASH_DASH_GODOT_BIN` must name the Standard executable. The scripts reject Mono, development, custom, and every version other than the exact accepted build.

## Codex Godot log safety

Before every Godot process, repository automation resolves the project root
containing `project.godot`, creates and write-tests
`<project-root>/.codex/godot-logs/`, and acquires a project-local process lock.
Every Godot invocation—including version checks and the packaged smoke—receives
an explicit purpose-specific `--log-file` in that directory. Captured terminal
output is stored beside the engine log as `<purpose>.output.log`.

Do not invoke Godot directly from Codex automation. Use
`tools/verify/run_tests.sh`, `tools/verify/export_macos.sh`, or the shared
`run_godot_stage` helper in `tools/verify/godot_diagnostics.sh`. Never point
Godot logs at `user://`, `~/Library/`, a temporary export directory, or any
path outside this writable project workspace. Automated import, validation,
script, export, and smoke processes must be headless; only an explicit visual
QA session may open an interactive window.

If a Godot stage exits nonzero, the helper reports the exact command, status,
engine-log path, and output-log path. Stop and inspect those logs before any
further Godot launch. Do not retry automatically. The project lock rejects a
second automated Godot process while one is already active.

## Focused commands

Run the static repository boundary check:

```bash
tools/verify/check_policy.sh
```

Run the bounded policy and exact-PID process regression fixtures:

```bash
tools/verify/test_shell_contracts.sh
```

Run the complete dependency-free GDScript suite:

```bash
tools/verify/run_tests.sh
```

Export and inspect an unsigned Universal 2 package into an explicit empty directory outside the repository:

```bash
output_dir="$(mktemp -d /private/tmp/trash-dash-foundation-export.XXXXXX)"
tools/verify/export_macos.sh "$output_dir"
```

The export command reports the clean source revision, package path, byte size, SHA-256, ZIP integrity, and `arm64 x86_64` architecture proof. The caller owns the explicit export directory and decides when to remove it.

## Full local verification

```bash
tools/verify/verify_local.sh
```

The aggregate labels are `Policy`, `Exact Godot version and headless import`, `Tests`, `Headless editor smoke`, `Fresh unsigned macOS export`, and `Bounded package process`. The policy stage includes deterministic shell-contract fixtures. The test stage first proves the runner's intentional failure path exits `1` with one deterministic message, then runs the real suite. Every Godot import, probe, test, editor, export, and package-smoke log is checked by the same status-aware diagnostic gate; a zero-exit stage still fails when it emits a real Godot warning or error, while the normal Godot banner and informational renderer lines remain allowed. A successful run ends with `Local verification: PASS`; any failed stage stops the sequence and returns nonzero. Its validated temporary directory is removed automatically. The package is launched through a locale-stable signal-reset wrapper because non-interactive shells ignore `SIGINT` for asynchronous children; the wrapper immediately becomes the package process. The verifier sends `SIGINT`, polls for a short bounded grace, then conditionally sends exact-PID `SIGTERM` and `SIGKILL` fallbacks. Any fallback is a verification failure. A child is reaped only after exact-PID absence is confirmed; if the bounded post-`SIGKILL` poll still cannot confirm absence, the verifier returns failure without calling blocking `wait`. A passing run requires the PID absent after signal-derived wait status `130`. Aggregate `INT`/`TERM` traps use the same conditional cleanup before deleting the validated directory.

The diagnostic shell displays exactly five neutral labels:

1. `Trash Dash 2.0`
2. `macOS prototype foundation — FOUNDATION_READY`
3. `0.1.0-foundation (development)`
4. `960×540 / Compatibility`
5. `prototype content not loaded`

## Boundaries and non-claims

The ZIP is an unsigned local development artifact: this project applies no valid project signing identity and performs no notarization. The packaged application may still inherit a non-valid ad-hoc or template signature blob, so “unsigned” does not mean every signature byte is literally absent. Gatekeeper distribution behavior is not assessed, and the package is not retained or uploaded as a release artifact. Apple-account hookup, Team configuration, certificates, signing, and notarization are deliberately deferred and must remain outside Git. The project owner's clean asset import and promotion pass is also deferred.

Passing these commands is not a gameplay pass, asset pass, audio pass, human traversal pass, signing/notarization pass, or release pass. Windows, Android, iOS, Linux, web, CI, store work, gameplay, and production asset/audio implementation remain outside this foundation task. The broader scaffold visual gate remains `INCOMPLETE` until the final package is directly inspected at every required window size; even those presentation checks do not establish gameplay or release readiness.
