# Godot Native Foundation Spike Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove that one isolated Godot 4 project can satisfy Trash Dash 2.0's Windows, macOS, landscape iOS, and landscape Android foundation contracts without allowing disposable spike gameplay into `main` history.

**Architecture:** Execute all spike code on an unmerged `spike/native-foundation` worktree branch under `spike/native-foundation/`. The spike uses typed GDScript, Godot Resources, scenes, and a dependency-free headless test runner. After the user reviews the results, retain only approved evidence and infrastructure decisions on `main`, then remove the worktree and delete the spike branch.

**Tech Stack:** Current stable Godot 4 Standard build; typed GDScript; Compatibility renderer; Godot headless CLI; Xcode; OpenJDK 17; Android SDK/ADB; Git and Git LFS; shell export scripts; Windows, macOS, iOS, and Android development exports.

## Global Constraints

- Read `AGENTS.md`, `.skills/README.md`, `.skills/rendering-asset-integrity/SKILL.md`, `.skills/animation/SKILL.md`, `.skills/environment-placement/SKILL.md`, `.skills/overlap-prevention/SKILL.md`, `.skills/visual-qa/SKILL.md`, and `.skills/v2_release_gate/SKILL.md` before spike work.
- The sibling V1 repository is read-only. Do not copy V1 code, level files, spawn tables, runtime atlases, or runtime art.
- The spike branch must never be merged into `main`.
- The spike project lives only at `spike/native-foundation/` on the spike branch.
- Use a fixed 960×540 logical viewport, fixed 16:9 field of view, letterboxing, nearest-neighbor texture filtering, and safe-area-aware UI.
- Required launch targets are Windows/Steam, macOS/Steam, iOS/App Store, and Android/Google Play. Linux and web are out of scope.
- Desktop keyboard and mobile landscape touch are required. Controllers are nonblocking.
- Save data is local and versioned. Cloud synchronization is out of scope.
- Approved reference files are immutable inputs. Derived spike files live under `spike/native-foundation/assets/generated/` and may not be promoted to root `assets/runtime/`.
- Signing credentials, certificates, provisioning profiles, keystores, Apple team IDs, and store credentials never enter Git.
- A missing physical device or signing identity produces `CANNOT VERIFY`, never a fabricated `PASS`.

---

### Task 1: Create the isolated spike worktree and audit native toolchains

**Files:**
- Create on spike branch: `spike/native-foundation/TOOLCHAIN.md`
- Create on spike branch: `spike/native-foundation/evidence/toolchain.json`
- Do not modify: V1 or production `src/`, `assets/runtime/`, `data/`, `scenes/`, and `scripts/`

**Interfaces:**
- Consumes: approved engine decision in `docs/architecture/ENGINE_DECISION.md`.
- Produces: an isolated `spike/native-foundation` branch/worktree and exact tool versions consumed by every later task.

- [ ] **Step 1: Confirm `main` is clean and synchronized**

Run:

```bash
git status --short --branch
git fetch origin main
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
```

Expected: clean status and identical local/remote commit IDs. If `main` is ahead, push reviewed documentation before creating the worktree.

- [ ] **Step 2: Create a disposable worktree**

Run:

```bash
spike_worktree=$(mktemp -d /private/tmp/trash-dash-v2-native-spike.XXXXXX)
git worktree add -b spike/native-foundation "$spike_worktree" main
test -f "$spike_worktree/AGENTS.md"
printf '%s\n' "$spike_worktree"
```

Expected: Git reports a new `spike/native-foundation` branch. Record the printed absolute path in the session; every later command runs from that worktree.

- [ ] **Step 3: Install the stable Godot Standard build**

Run on macOS:

```bash
brew install --cask godot
godot --version
```

Expected: a stable Godot 4 version without `mono`, `dev`, `beta`, or `rc` in the version string. Install matching export templates through Godot's template manager before Task 8.

- [ ] **Step 4: Audit Apple and Android prerequisites**

Run:

```bash
xcode-select -p
xcodebuild -version
/usr/libexec/java_home -v 17
adb version
xcrun devicectl list devices
adb devices -l
```

Expected on the current machine before remediation: command-line tools selected instead of full Xcode, no Java 17 runtime, and no `adb`. Install full Xcode from Apple, accept its license, select `/Applications/Xcode.app`, install OpenJDK 17, and install Android Studio/SDK Platform Tools. Re-run until `xcodebuild`, Java 17, and `adb` report versions. Device lists may be empty, but that limitation must be recorded.

- [ ] **Step 5: Record machine-readable tool evidence**

Generate `spike/native-foundation/evidence/toolchain.json` from command output rather than hand-entered version strings:

```bash
mkdir -p spike/native-foundation/evidence
spike_godot_version=$(godot --version | tr -d '\n')
spike_xcode_version=$(xcodebuild -version | paste -sd ' ' -)
spike_java_home=$(/usr/libexec/java_home -v 17)
spike_adb_version=$(adb version | head -1)
spike_android_devices=$(adb devices | awk 'NR > 1 && $2 == "device" {print $1}' | jq -R . | jq -s .)
spike_ios_devices=$(xcrun devicectl list devices --json-output /private/tmp/trash-dash-spike-ios-devices.json >/dev/null 2>&1 && jq '[.result.devices[]?.identifier]' /private/tmp/trash-dash-spike-ios-devices.json || printf '[]')
jq -n \
  --arg godot "$spike_godot_version" \
  --arg xcode "$spike_xcode_version" \
  --arg java_home "$spike_java_home" \
  --arg adb "$spike_adb_version" \
  --argjson android_devices "$spike_android_devices" \
  --argjson ios_devices "$spike_ios_devices" \
  '{
    godot: {version: $godot, build: "standard"},
    xcode: {version: $xcode, developer_dir: "/Applications/Xcode.app/Contents/Developer"},
    java: {major: 17, home: $java_home},
    android: {adb_version: $adb, connected_devices: $android_devices},
    ios: {connected_devices: $ios_devices},
    renderer_candidate: "gl_compatibility"
  }' > spike/native-foundation/evidence/toolchain.json
jq empty spike/native-foundation/evidence/toolchain.json
```

Create `TOOLCHAIN.md` with the same exact values, installation commands, and any unavailable devices.

- [ ] **Step 6: Commit the isolated toolchain baseline**

Run from the spike worktree:

```bash
git add spike/native-foundation/TOOLCHAIN.md spike/native-foundation/evidence/toolchain.json
git commit -m "spike: record native export toolchains"
```

---

### Task 2: Scaffold the Godot spike and dependency-free test harness

**Files:**
- Create: `spike/native-foundation/project.godot`
- Create: `spike/native-foundation/scenes/main.tscn`
- Create: `spike/native-foundation/scripts/main.gd`
- Create: `spike/native-foundation/tests/assertions.gd`
- Create: `spike/native-foundation/tests/test_case.gd`
- Create: `spike/native-foundation/tests/run_all.gd`
- Create: `spike/native-foundation/tests/test_boot.gd`

**Interfaces:**
- Consumes: exact Godot version recorded in Task 1.
- Produces: `godot --headless --path spike/native-foundation --script res://tests/run_all.gd`, returning 0 only when all test methods pass.

- [ ] **Step 1: Write the failing boot test**

Create `tests/test_boot.gd`:

```gdscript
extends "res://tests/test_case.gd"

func test_project_contract() -> void:
    assert_equal(ProjectSettings.get_setting("display/window/size/viewport_width"), 960)
    assert_equal(ProjectSettings.get_setting("display/window/size/viewport_height"), 540)
    assert_equal(ProjectSettings.get_setting("rendering/renderer/rendering_method"), "gl_compatibility")
    assert_equal(ProjectSettings.get_setting("rendering/textures/default_filters/use_nearest_mipmap_filter"), false)
```

- [ ] **Step 2: Create the minimal assertion and runner interfaces**

`tests/test_case.gd` exposes `assert_true(value: bool, message := "")`, `assert_false(value: bool, message := "")`, `assert_equal(actual: Variant, expected: Variant, message := "")`, and `assert_near(actual: float, expected: float, tolerance: float, message := "")`. Each failed assertion appends a message to `failures: Array[String]`.

`tests/run_all.gd` extends `SceneTree`, instantiates these scripts in order, calls every method beginning with `test_`, prints failures, and exits with `quit(1)` when any failure exists:

```gdscript
extends SceneTree

const TEST_SCRIPTS: Array[Script] = [
    preload("res://tests/test_boot.gd"),
]

func _initialize() -> void:
    var failed := 0
    for test_script in TEST_SCRIPTS:
        var test_case = test_script.new()
        for method in test_case.get_method_list():
            var method_name := StringName(method.name)
            if String(method_name).begins_with("test_"):
                test_case.call(method_name)
        failed += test_case.failures.size()
        for failure in test_case.failures:
            printerr(failure)
    quit(1 if failed > 0 else 0)
```

- [ ] **Step 3: Run the test before project configuration**

Run:

```bash
godot --headless --path spike/native-foundation --script res://tests/run_all.gd
```

Expected: nonzero exit because the required project settings do not exist yet.

- [ ] **Step 4: Create the minimal project and main scene**

Set these values in `project.godot`:

```ini
[application]
config/name="Trash Dash Native Foundation Spike"
run/main_scene="res://scenes/main.tscn"

[display]
window/size/viewport_width=960
window/size/viewport_height=540
window/size/window_width_override=1280
window/size/window_height_override=720
window/stretch/mode="canvas_items"
window/handheld/orientation=6

[rendering]
renderer/rendering_method="gl_compatibility"
renderer/rendering_method.mobile="gl_compatibility"
textures/default_filters/use_nearest_mipmap_filter=false
textures/canvas_textures/default_texture_filter=0
```

Create a `Node` root named `Main` in `main.tscn` and attach `scripts/main.gd` with an empty typed `_ready() -> void` method.

- [ ] **Step 5: Run the test and boot smoke**

Run:

```bash
godot --headless --path spike/native-foundation --script res://tests/run_all.gd
godot --headless --path spike/native-foundation --editor --quit
```

Expected: both commands exit 0 with no parse or resource errors.

- [ ] **Step 6: Commit the tested scaffold**

```bash
git add spike/native-foundation/project.godot spike/native-foundation/scenes spike/native-foundation/scripts spike/native-foundation/tests
git commit -m "spike: scaffold tested Godot project"
```

---

### Task 3: Prove display policy, landscape gating, and platform-neutral actions

**Files:**
- Create: `spike/native-foundation/scripts/core/display_policy.gd`
- Create: `spike/native-foundation/scripts/core/input_router.gd`
- Create: `spike/native-foundation/scripts/ui/touch_controls.gd`
- Create: `spike/native-foundation/scenes/ui/touch_controls.tscn`
- Create: `spike/native-foundation/scenes/ui/orientation_gate.tscn`
- Create: `spike/native-foundation/tests/test_display_policy.gd`
- Create: `spike/native-foundation/tests/test_input_router.gd`
- Modify: `spike/native-foundation/tests/run_all.gd`
- Modify: `spike/native-foundation/project.godot`

**Interfaces:**
- Produces `DisplayPolicy.content_rect(window_size: Vector2i) -> Rect2i`, `DisplayPolicy.is_landscape(window_size: Vector2i) -> bool`, `InputRouter.set_virtual_action(action: StringName, pressed: bool) -> void`, `InputRouter.is_action_pressed(action: StringName) -> bool`, and `InputRouter.clear_all() -> void`.
- Touch buttons call only `InputRouter.set_virtual_action`; gameplay reads only `InputRouter` actions.

- [ ] **Step 1: Write display-policy tests**

Test exact expectations:

```gdscript
func test_content_rect_preserves_fixed_field_of_view() -> void:
    assert_equal(DisplayPolicy.content_rect(Vector2i(1920, 1080)), Rect2i(0, 0, 1920, 1080))
    assert_equal(DisplayPolicy.content_rect(Vector2i(2436, 1125)), Rect2i(218, 0, 2000, 1125))
    assert_equal(DisplayPolicy.content_rect(Vector2i(1280, 800)), Rect2i(0, 40, 1280, 720))

func test_orientation_gate() -> void:
    assert_true(DisplayPolicy.is_landscape(Vector2i(844, 390)))
    assert_false(DisplayPolicy.is_landscape(Vector2i(390, 844)))
```

- [ ] **Step 2: Write input lifecycle tests**

Verify `move_left`, `move_right`, `jump`, `dash`, `action`, and `pause`. Assert virtual press/hold/release behavior and assert `clear_all()` releases every action after focus loss or pause.

- [ ] **Step 3: Run tests to verify failure**

```bash
godot --headless --path spike/native-foundation --script res://tests/run_all.gd
```

Expected: parse/load failure for missing `DisplayPolicy` and `InputRouter`.

- [ ] **Step 4: Implement display and input modules**

`DisplayPolicy.content_rect()` computes the largest centered 16:9 integer rectangle inside the physical window. It never modifies the logical 960×540 world. `InputRouter` merges Godot `Input` actions with a `Dictionary[StringName, bool]` of virtual touch actions and emits `action_changed(action, pressed)`.

Add keyboard defaults in `project.godot`: A/Left, D/Right, Space, Shift, E, Escape. Create safe-area-aware touch buttons anchored inside the viewport content rectangle and an orientation gate that pauses the tree when height exceeds width.

- [ ] **Step 5: Run headless tests and interactive resize checks**

```bash
godot --headless --path spike/native-foundation --script res://tests/run_all.gd
godot --path spike/native-foundation --resolution 1280x720
godot --path spike/native-foundation --resolution 844x390
godot --path spike/native-foundation --resolution 390x844
```

Expected: tests exit 0; landscape windows show the same field of view; portrait shows the rotate-device gate and does not advance gameplay.

- [ ] **Step 6: Commit display/input proof**

```bash
git add spike/native-foundation/project.godot spike/native-foundation/scripts/core spike/native-foundation/scripts/ui spike/native-foundation/scenes/ui spike/native-foundation/tests
git commit -m "spike: prove fixed display and unified input"
```

---

### Task 4: Prove typed level data, independent collision, and camera states

**Files:**
- Create: `spike/native-foundation/scripts/world/level_definition.gd`
- Create: `spike/native-foundation/scripts/world/support_definition.gd`
- Create: `spike/native-foundation/scripts/world/level_validator.gd`
- Create: `spike/native-foundation/scripts/world/camera_controller.gd`
- Create: `spike/native-foundation/data/levels/spike_level.tres`
- Create: `spike/native-foundation/scenes/levels/spike_level.tscn`
- Create: `spike/native-foundation/tests/test_level_validator.gd`
- Create: `spike/native-foundation/tests/test_camera_controller.gd`
- Modify: `spike/native-foundation/tests/run_all.gd`

**Interfaces:**
- `SupportDefinition`: `id: StringName`, `bounds: Rect2`, `kind: StringName`.
- `LevelDefinition`: `id: StringName`, `world_bounds: Rect2`, `supports: Array[SupportDefinition]`, `boss_arena: Rect2`.
- `LevelValidator.validate(level: LevelDefinition) -> Array[String]`.
- `CameraController` states: `FOLLOW`, `TRANSITION`, `ARENA_LOCK`, `DEFEAT_RELEASE`, `CHECKPOINT_RECOVERY`.
- `CameraController.step(target_x: float, delta: float) -> float`.

- [ ] **Step 1: Write failing level-contract tests**

Test one valid level with `ground-main` at `Rect2(0, 468, 2400, 72)` and a boss arena at `Rect2(1440, 0, 960, 540)`. Add invalid fixtures for duplicate IDs, zero-sized support geometry, support outside world bounds, and an arena outside world bounds. Assert exact error strings.

- [ ] **Step 2: Write failing camera-state tests**

Assert follow clamping in a 2400px world, monotonic transition into camera X 1440, locked arena X 1440, no release before `begin_defeat_release()`, and checkpoint recovery to X 960.

- [ ] **Step 3: Run tests to verify failure**

```bash
godot --headless --path spike/native-foundation --script res://tests/run_all.gd
```

Expected: missing resource/controller failures.

- [ ] **Step 4: Implement resources, validator, and state machine**

Use typed `Resource` classes for level/support data. Build terrain visuals with `Polygon2D`/`ColorRect` and physics with separate `StaticBody2D` plus `CollisionShape2D` nodes. Visual rectangles and collision shapes must be created from different fields even when their coordinates temporarily agree.

Implement the camera state machine without reading scene-tree globals. `step()` receives target X and delta; arena/checkpoint methods receive explicit coordinates.

- [ ] **Step 5: Create the synthetic composed level scene**

The scene contains one 2400px ground support, one raised platform with visible support posts, one player-shaped `CharacterBody2D`, one camera, one checkpoint marker, and an empty boss runway/arena. It contains no V1 level layout, spawn table, enemy, boss, or production art.

- [ ] **Step 6: Run tests and traverse the synthetic scene**

```bash
godot --headless --path spike/native-foundation --script res://tests/run_all.gd
godot --path spike/native-foundation
```

Expected: tests exit 0; keyboard/touch moves the test body; the camera follows, locks at the synthetic arena, and releases only after the explicit defeat signal; collision overlay is visibly independent from art.

- [ ] **Step 7: Commit level/camera proof**

```bash
git add spike/native-foundation/scripts/world spike/native-foundation/data/levels spike/native-foundation/scenes/levels spike/native-foundation/tests
git commit -m "spike: prove level contracts and camera lifecycle"
```

---

### Task 5: Prove deterministic source-sheet derivation and stable animation

**Files:**
- Create: `spike/native-foundation/tools/extract_trashy_idle.py`
- Create: `spike/native-foundation/assets/generated/trashy-idle-spike.png`
- Create: `spike/native-foundation/assets/generated/trashy-idle-spike.json`
- Create: `spike/native-foundation/scripts/rendering/animation_definition.gd`
- Create: `spike/native-foundation/tests/test_animation_contract.gd`
- Modify: `spike/native-foundation/scenes/levels/spike_level.tscn`
- Modify: `spike/native-foundation/tests/run_all.gd`

**Interfaces:**
- Input: `docs/design/trash-dash/reference/main-characters/sprites/trashy-regular-approved.png` (1086×1448, approved reference).
- Output manifest fields: source SHA-256, output SHA-256, frame rectangles, visible bounds, bottom-center anchors, canonical display height, FPS, and loop mode.
- `AnimationDefinition.validate() -> Array[String]`.

- [ ] **Step 1: Write the failing animation-contract test**

Assert that the generated manifest contains four `idle` frames, every source rectangle is positive and inside the 1086×1448 source, all output cells have the same dimensions, anchors share one baseline, destination scaling is uniform, FPS is 6, loop mode is `loop`, and source SHA-256 equals `770aa14d05d0e2db32c1948a58a2db5053500bf6c9a23812a81ecc74d2d764d6`.

- [ ] **Step 2: Run the test to verify failure**

```bash
godot --headless --path spike/native-foundation --script res://tests/run_all.gd
```

Expected: missing generated manifest.

- [ ] **Step 3: Implement the deterministic extraction tool**

The script must accept only `--source`, `--output`, and `--manifest`. It extracts the four visually audited `IDLE / STAND` poses from the first animation row, removes the presentation background without altering opaque body pixels, measures connected visible-alpha bounds, places each pose on an equal transparent cell using a common bottom-center anchor, writes a horizontal PNG strip with nearest-neighbor-safe pixels, and emits sorted JSON. It must reject captions, separators, edge-touching alpha, and any source hash other than the approved value.

Run:

```bash
python3 spike/native-foundation/tools/extract_trashy_idle.py \
  --source docs/design/trash-dash/reference/main-characters/sprites/trashy-regular-approved.png \
  --output spike/native-foundation/assets/generated/trashy-idle-spike.png \
  --manifest spike/native-foundation/assets/generated/trashy-idle-spike.json
```

- [ ] **Step 4: Inspect native output and runtime registration**

Create a contact-sheet view at 100% and 400%. Register the generated strip as `SpriteFrames` at 6 FPS with nearest filtering and a stable bottom-center offset. Collision remains the synthetic player's independent `CollisionShape2D`.

- [ ] **Step 5: Run deterministic and runtime checks**

Run the extractor twice and compare both output hashes. Then run:

```bash
godot --headless --path spike/native-foundation --script res://tests/run_all.gd
godot --path spike/native-foundation
```

Expected: identical output hashes; four complete silhouettes; no caption/background contamination, edge bleed, scale pop, anchor jitter, or collision resizing during animation.

- [ ] **Step 6: Commit the spike-only pipeline proof**

```bash
git add spike/native-foundation/tools spike/native-foundation/assets/generated spike/native-foundation/scripts/rendering spike/native-foundation/scenes/levels spike/native-foundation/tests
git commit -m "spike: prove deterministic animation derivation"
```

---

### Task 6: Prove versioned local saves and audio lifecycle

**Files:**
- Create: `spike/native-foundation/autoload/save_service.gd`
- Create: `spike/native-foundation/autoload/audio_service.gd`
- Create: `spike/native-foundation/scripts/core/save_codec.gd`
- Create: `spike/native-foundation/tests/test_save_codec.gd`
- Create: `spike/native-foundation/tests/test_audio_service.gd`
- Create: `spike/native-foundation/assets/generated/spike-tone.wav`
- Modify: `spike/native-foundation/project.godot`
- Modify: `spike/native-foundation/tests/run_all.gd`

**Interfaces:**
- `SaveCodec.CURRENT_VERSION := 1`.
- `SaveCodec.defaults() -> Dictionary` returns `{"version": 1, "high_score": 0, "best_time_ms": 0, "muted": false}`.
- `SaveCodec.decode(text: String) -> Dictionary` returns `{ok, data, error}`.
- `SaveService.save_atomic(data: Dictionary) -> Error` writes a temporary file then renames it.
- `AudioService` exposes `set_muted(bool)`, `pause_all()`, `resume_all()`, and `switch_music(stream: AudioStream, fade_seconds: float)`.

- [ ] **Step 1: Write failing save tests**

Cover defaults, valid version 1 input, rejected unknown versions, rejected wrong field types, missing fields filled from defaults, corrupt JSON preservation, and atomic replacement that never exposes a partial destination.

- [ ] **Step 2: Write failing audio ownership tests**

Use injected fake players to verify mute, pause/resume, replacement cancellation, disposal of the outgoing stream, and no duplicate owned player after a switch.

- [ ] **Step 3: Run tests to verify failure**

```bash
godot --headless --path spike/native-foundation --script res://tests/run_all.gd
```

Expected: missing save/audio implementations.

- [ ] **Step 4: Implement save and audio services**

Add only `SaveService` and `AudioService` as autoloads. Keep JSON schema logic in `SaveCodec` so it remains headless-testable. Generate a one-second nonmusical sine tone for lifecycle testing; do not copy or approve V1 music.

- [ ] **Step 5: Run tests and interactive lifecycle checks**

```bash
godot --headless --path spike/native-foundation --script res://tests/run_all.gd
godot --path spike/native-foundation
```

Expected: tests exit 0; mute/pause/resume and scene transitions do not leak or duplicate audio; corrupt save exercise retains a `.corrupt-YYYYMMDDTHHMMSSZ` copy and restores defaults.

- [ ] **Step 6: Commit persistence/audio proof**

```bash
git add spike/native-foundation/autoload spike/native-foundation/scripts/core spike/native-foundation/tests spike/native-foundation/assets/generated/spike-tone.wav spike/native-foundation/project.godot
git commit -m "spike: prove local saves and audio ownership"
```

---

### Task 7: Add export presets and reproducible build commands

**Files:**
- Create: `spike/native-foundation/export_presets.cfg`
- Create: `spike/native-foundation/tools/export_all.sh`
- Create: `spike/native-foundation/.gitignore`
- Create: `spike/native-foundation/evidence/export-matrix.json`

**Interfaces:**
- Export preset names are exactly `Windows Desktop`, `macOS`, `Android`, and `iOS`.
- `export_all.sh OUTPUT_DIRECTORY` exits nonzero if any required unsigned development export fails.

- [ ] **Step 1: Create secret-safe export presets**

Configure Windows x86_64 `.exe`, macOS Universal 2 `.zip`, Android ARM64 debug `.apk` plus release `.aab` configuration, and iOS Xcode project export. Use application identifier `com.jschmittler.trashdash.spike`. Leave signing identities and passwords unset. Ensure no secret fields contain values.

- [ ] **Step 2: Create the export script**

The script validates one output directory argument and runs:

```bash
godot --headless --path spike/native-foundation --export-debug "Windows Desktop" "$output_dir/windows/trash-dash-spike.exe"
godot --headless --path spike/native-foundation --export-debug "macOS" "$output_dir/macos/trash-dash-spike.zip"
godot --headless --path spike/native-foundation --export-debug "Android" "$output_dir/android/trash-dash-spike.apk"
godot --headless --path spike/native-foundation --export-debug "iOS" "$output_dir/ios/trash-dash-spike.zip"
```

It removes no directories and refuses `/`, the repository root, or an existing nonempty output directory.

- [ ] **Step 3: Ignore build products and credential files**

Ignore `build/`, `.godot/`, generated Xcode/Gradle directories, keystores, provisioning profiles, certificates, and local export credentials inside the spike directory. Keep `export_presets.cfg` tracked only after confirming it contains no secrets.

- [ ] **Step 4: Run all headless checks and exports**

```bash
godot --headless --path spike/native-foundation --script res://tests/run_all.gd
spike/native-foundation/tools/export_all.sh /private/tmp/trash-dash-v2-spike-build
```

Expected: tests exit 0 and all four unsigned development export artifacts exist. If iOS or Android tooling blocks export, record the exact command/output as `CANNOT VERIFY` and resolve the toolchain rather than weakening the target matrix.

- [ ] **Step 5: Record export evidence and commit**

`export-matrix.json` records each preset, artifact path, byte size, SHA-256, command, exit code, and tool version. Then:

```bash
git add spike/native-foundation/export_presets.cfg spike/native-foundation/tools/export_all.sh spike/native-foundation/.gitignore spike/native-foundation/evidence/export-matrix.json
git commit -m "spike: prove native export presets"
```

---

### Task 8: Run desktop/mobile smoke tests and visual evidence

**Files:**
- Create: `spike/native-foundation/scripts/core/evidence_capture.gd`
- Create: `spike/native-foundation/evidence/runtime/`
- Create: `spike/native-foundation/evidence/runtime-matrix.json`
- Create on `main` only after review: `docs/superpowers/reports/2026-08-11-godot-native-foundation-spike.md`

**Interfaces:**
- `EvidenceCapture.capture(label: StringName) -> Error` saves the 960×540 viewport plus JSON metadata containing physical window size, content rectangle, camera state, input source, and scene ID.
- Runtime matrix statuses are only `PASS`, `FAIL`, `INCOMPLETE`, or `CANNOT VERIFY`.

- [ ] **Step 1: Capture required desktop cases**

On macOS, capture 1280×720 and 1440×900 normal traversal, 1280×800 letterboxing, keyboard press/hold/release, checkpoint recovery, arena lock/release, animation transition, mute/pause/resume, and corrupt-save recovery. Run the Windows build on a Windows machine or VM and repeat 1280×720 keyboard traversal and save/audio smoke checks.

- [ ] **Step 2: Capture required Android cases**

Run:

```bash
adb install -r /private/tmp/trash-dash-v2-spike-build/android/trash-dash-spike.apk
adb shell am start -n com.jschmittler.trashdash.spike/com.godot.game.GodotApp
adb exec-out screencap -p > spike/native-foundation/evidence/runtime/android-landscape.png
```

Exercise landscape touch press/hold/release, focus interruption, pause, letterboxing/safe areas, traversal, animation, camera lock/release, and local-save relaunch. Record device model, OS version, resolution, and result.

- [ ] **Step 3: Capture required iOS cases**

Open the exported Xcode project, select a physical iPhone or iPad, set a local development team outside Git, build and run. Exercise the same landscape touch, safe-area, traversal, animation, camera, audio, and save cases. Capture a device screenshot and record model, OS version, resolution, and result. The iOS simulator may support diagnostics but cannot replace the required physical-device result.

- [ ] **Step 4: Run the V2 release gate as a spike assessment**

Apply `.skills/v2_release_gate/SKILL.md` but label the artifact `SPIKE`, not production-ready content. Static fixtures cannot satisfy real traversal. Any unavailable platform remains `CANNOT VERIFY` and blocks acceptance of that platform proof.

- [ ] **Step 5: Commit branch-only evidence**

```bash
git add spike/native-foundation/scripts/core/evidence_capture.gd spike/native-foundation/evidence
git commit -m "spike: record native runtime evidence"
```

---

### Task 9: Review results, retain decisions on `main`, and destroy spike code

**Files:**
- Create on `main`: `docs/superpowers/reports/2026-08-11-godot-native-foundation-spike.md`
- Modify on `main` only if evidence supports changes: `docs/architecture/ENGINE_DECISION.md`
- Modify on `main`: `docs/migration/V2_BUILD_PLAN.md`
- Delete: spike worktree and `spike/native-foundation` branch after explicit user approval

**Interfaces:**
- Consumes: complete branch-only toolchain, test, export, and runtime evidence.
- Produces: a main-branch report with no spike code or generated spike asset in history.

- [ ] **Step 1: Present the spike report for approval**

The report contains exact tool versions, every test command/count, renderer findings, display/input/camera/collision/animation/save/audio findings, export artifact hashes, device matrix, screenshots, release-gate outcomes, unresolved failures, and a recommendation to accept, revise, or reject the foundation.

Stop and obtain explicit user approval before cleanup or main-branch documentation changes.

- [ ] **Step 2: Write only approved evidence to `main`**

Switch to the primary V2 worktree on `main`. Use `apply_patch` to create the report from reviewed evidence; do not cherry-pick spike commits or copy the `spike/` directory. Update the engine decision only for evidence-backed renderer/toolchain changes. Mark the V2 build-plan spike task complete only if every required platform proof is accepted.

- [ ] **Step 3: Verify `main` contains no spike implementation**

Run:

```bash
git status --short --branch
git ls-files 'spike/**'
git log main --all-match --oneline -- spike/native-foundation
```

Expected: no tracked `spike/**` files and no spike implementation commits reachable from `main`.

- [ ] **Step 4: Commit and push reviewed documentation**

```bash
git add docs/superpowers/reports/2026-08-11-godot-native-foundation-spike.md docs/architecture/ENGINE_DECISION.md docs/migration/V2_BUILD_PLAN.md
git commit -m "docs: record Godot native foundation spike"
git push origin main
```

- [ ] **Step 5: Remove the exact validated worktree and branch**

Resolve the absolute spike worktree path with `git worktree list`. Confirm it contains `/private/tmp/trash-dash-v2-native-spike.` and is registered to `spike/native-foundation`. Then run:

```bash
spike_worktree=$(git worktree list --porcelain | awk '
  $1 == "worktree" {candidate = $2}
  $1 == "branch" && $2 == "refs/heads/spike/native-foundation" {print candidate}
')
test -n "$spike_worktree"
case "$spike_worktree" in
  /private/tmp/trash-dash-v2-native-spike.*) ;;
  *) printf 'Refusing unexpected worktree: %s\n' "$spike_worktree" >&2; exit 1 ;;
esac
git worktree remove "$spike_worktree"
git branch -D spike/native-foundation
git worktree prune
```

Do not substitute an unvalidated path. The branch deletion is authorized only after the reviewed report is safely committed to `main`.

- [ ] **Step 6: Perform final clean-room verification**

Verify clean `main`, synchronized `origin/main`, zero `spike/**` tracked files, unchanged V1 status/HEAD, 113 intact LFS references, no archive imports, no production gameplay, and a report that distinguishes every `PASS`, `FAIL`, `INCOMPLETE`, and `CANNOT VERIFY` result.
