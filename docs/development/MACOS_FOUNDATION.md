# macOS Foundation Development Guide

This repository currently provides a macOS-only Godot foundation shell. Use Godot `4.7.1.stable.official.a13da4feb` Standard with matching macOS export templates, plus Git, ripgrep, `unzip`, `lipo`, and `shasum`.

The scripts use `godot` by default. To select the accepted executable explicitly for one command:

```bash
TRASH_DASH_GODOT_BIN=/opt/homebrew/bin/godot tools/verify/run_tests.sh
```

`TRASH_DASH_GODOT_BIN` must name the Standard executable. The scripts reject Mono, development, custom, and every version other than the exact accepted build.

## Focused commands

Run the static repository boundary check:

```bash
tools/verify/check_policy.sh
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

The aggregate labels are `Policy`, `Exact Godot version and headless import`, `Tests`, `Headless editor smoke`, `Fresh unsigned macOS export`, and `Bounded package process`. A successful run ends with `Local verification: PASS`; any failed stage stops the sequence and returns nonzero. Its validated temporary directory is removed automatically. The package is launched through a locale-stable signal-reset wrapper because non-interactive shells ignore `SIGINT` for asynchronous children; the wrapper immediately becomes the package process, so the recorded PID must be absent after the expected signal-derived wait status `130`. The aggregate script itself then exits `0`.

The diagnostic shell displays exactly five neutral labels:

1. `Trash Dash 2.0`
2. `macOS prototype foundation — FOUNDATION_READY`
3. `0.1.0-foundation (development)`
4. `960×540 / Compatibility`
5. `prototype content not loaded`

## Boundaries and non-claims

The ZIP is an unsigned local development artifact. Gatekeeper distribution behavior is not assessed, and it is not retained or uploaded as a release artifact. Apple-account hookup, Team configuration, certificates, signing, and notarization are deliberately deferred and must remain outside Git. The project owner's clean asset import and promotion pass is also deferred.

Passing these commands is not a gameplay pass, asset pass, audio pass, human traversal pass, signing/notarization pass, or release pass. Windows, Android, iOS, Linux, web, CI, store work, gameplay, and production asset/audio implementation remain outside this foundation task. The broader scaffold visual gate remains `INCOMPLETE` until the final package is directly inspected at every required window size; even those presentation checks do not establish gameplay or release readiness.
