# macOS Production Boundary Scaffold Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a clean-room Godot 4.7.1 diagnostic shell that proves the production macOS MVP boundaries without gameplay or runtime assets.

**Architecture:** A contract-first bootstrap scene composes pure build, display, input, startup, and service boundaries and renders an immutable foundation status. Dependency-free GDScript tests plus local shell verification prove the project and one unsigned Universal 2 macOS export; unfinished services fail explicitly without side effects.

**Tech Stack:** Godot 4.7.1 Standard, typed GDScript, Compatibility renderer, Godot text scenes/resources, POSIX `bash`, macOS `unzip`/`lipo`/`shasum`, Git.

## Global Constraints

- Work only in V2; the sibling V1 repository stays read-only and unchanged.
- Reimplement from approved contracts; copy no spike/V1 implementation, fixtures, evidence, or concept-derived runtime assets.
- Use fixed 960×540, `canvas_items` + `keep`, centered 16:9 letterboxing, nearest filtering, and Compatibility.
- Configure exactly `move_left`, `move_right`, `jump`, `dash`, `action`, `pause` with A/Left, D/Right, Space, Shift, E, Escape.
- Target macOS only. Add no deferred-platform preset/code, touch UI, portrait gate, gameplay, actors, levels, camera, runtime art, animation, music, SFX, menu, or operational service.
- Add no autoload. Bootstrap owns its registry.
- Unavailable services are deterministic, side-effect free, and return `ERR_UNAVAILABLE` or `ServiceResult.unavailable()`.
- Commit no credentials, signing material, Team ID, password, secret entitlement, store SDK, or absolute local path.
- Use dependency-free local verification; CI is deferred.
- Package output is ephemeral; report revision, size, SHA-256, ZIP integrity, and Mach-O architectures without claiming store readiness or byte reproducibility.
- Visual status stays `INCOMPLETE` until direct inspection at every required window shape.

## File Map

```text
project.godot / export_presets.cfg       Production settings and one macOS preset
scenes/bootstrap/bootstrap.tscn          Only startup scene
src/core/build/                          Immutable build identity
src/core/display/                        Pure display policy
src/core/input/                          Input-map contract
src/core/services/                       Four contracts, unavailable implementations, registry
src/core/bootstrap/                      Status, settings adapter, validator, controller
src/ui/bootstrap/                        Label presentation adapter
tests/support/ and tests/run_all.gd      Dependency-free test framework
tests/unit/ and tests/gameplay/           Pure and scene contract suites
tools/verify/                            Policy, test, export, aggregate scripts
docs/development/MACOS_FOUNDATION.md     Operator guide and explicit boundaries
```

---
+
### Task 1: Project Contract and Dependency-Free Test Harness

**Files:**
- Create: `.gitignore`
- Create: `project.godot`
- Create: `scenes/bootstrap/bootstrap.tscn` (minimal parseable root; completed in Task 4)
- Create: `tests/support/test_case.gd`
- Create: `tests/support/runner_probe_case.gd`
- Create: `tests/run_all.gd`
- Create: `tests/unit/test_project_contract.gd`
- Create: `tests/unit/test_test_runner.gd`

**Interfaces:**
- Consumes: Godot `ProjectSettings`, `InputMap`, `InputEventKey`, `SceneTree`.
- Produces: `TestCase.assert_true(value: bool, message: String)`, `assert_equal(actual: Variant, expected: Variant, message: String)`, `fail(message: String)`, `failure_count() -> int`, `failure_messages() -> PackedStringArray`; runner `--suite=<file-stem>` and `--probe-pass|--probe-fail` modes.

- [ ] **Step 1: Create a parseable minimal project and failing contract test**

Start `project.godot` with only `config_version=5` and `application/config/name="Trash Dash 2.0"`. Create a minimal `bootstrap.tscn` containing only a full-rect `Control` named `Bootstrap`; Task 4 will drive its diagnostic hierarchy from RED to GREEN. Implement `TestCase` as a typed `RefCounted` with a private ordered `PackedStringArray`. Add this test:

```gdscript
extends "res://tests/support/test_case.gd"

const REQUIRED_ACTIONS := {
    &"move_left": [KEY_A, KEY_LEFT],
    &"move_right": [KEY_D, KEY_RIGHT],
    &"jump": [KEY_SPACE],
    &"dash": [KEY_SHIFT],
    &"action": [KEY_E],
    &"pause": [KEY_ESCAPE],
}

func test_settings_are_exact() -> void:
    assert_equal(ProjectSettings.get_setting("application/run/main_scene"), "res://scenes/bootstrap/bootstrap.tscn", "main scene")
    assert_true(ResourceLoader.exists("res://scenes/bootstrap/bootstrap.tscn"), "main scene resource")
    assert_equal(ProjectSettings.get_setting("display/window/size/viewport_width"), 960, "width")
    assert_equal(ProjectSettings.get_setting("display/window/size/viewport_height"), 540, "height")
    assert_equal(ProjectSettings.get_setting("display/window/stretch/mode"), "canvas_items", "stretch")
    assert_equal(ProjectSettings.get_setting("display/window/stretch/aspect"), "keep", "aspect")
    assert_equal(ProjectSettings.get_setting("rendering/renderer/rendering_method"), "gl_compatibility", "renderer")
    assert_equal(ProjectSettings.get_setting("rendering/textures/canvas_textures/default_texture_filter"), 0, "nearest")

func test_actions_have_exact_physical_defaults() -> void:
    for action: StringName in REQUIRED_ACTIONS:
        assert_true(InputMap.has_action(action), "missing action: %s" % action)
        var keys: Array[Key] = []
        for event: InputEvent in InputMap.action_get_events(action):
            if event is InputEventKey:
                keys.append((event as InputEventKey).physical_keycode)
        assert_equal(keys, REQUIRED_ACTIONS[action], "defaults: %s" % action)
```

In the same test, load `project.godot` with `ConfigFile`, get `get_section_keys("input")`, sort them, and compare them with the six sorted required action names. This rejects an accidental seventh project-defined action without confusing Godot's built-in `ui_*` actions with project configuration.

- [ ] **Step 2: Implement the runner and capture RED**

`tests/run_all.gd` extends `SceneTree`, defers one process frame, instantiates an explicit ordered `Array[Script]`, sorts each case's `test_` methods, and executes every method as `await test_case.call(method_name)` (Godot 4 resumes immediately for synchronous results). It collects messages, frees cases, waits one teardown frame, prints a deterministic summary, and exits 1 on failures. `runner_probe_case.gd` provides one intentional failure string. `test_test_runner.gd` proves two failed assertions retain order and yield count 2.

The runner core is:

```gdscript
func _initialize() -> void:
    call_deferred("_run")

func _run() -> void:
    await process_frame
    var failures := PackedStringArray()
    for case_script: Script in _selected_scripts():
        var test_case: RefCounted = case_script.new()
        for method_name: StringName in _sorted_test_methods(test_case):
            await test_case.call(method_name)
        failures.append_array(test_case.call("failure_messages"))
    await process_frame
    for failure: String in failures:
        printerr(failure)
    quit(0 if failures.is_empty() else 1)

func _sorted_test_methods(test_case: RefCounted) -> Array[StringName]:
    var names: Array[StringName] = []
    for method: Dictionary in test_case.get_method_list():
        var method_name := StringName(method["name"])
        if String(method_name).begins_with("test_"):
            names.append(method_name)
    names.sort()
    return names
```

`_selected_scripts()` returns the explicit list, filters by a single optional `--suite=<file-stem>`, and returns only `runner_probe_case.gd` for a probe flag. Unknown suites or simultaneous probe/suite flags print one usage error and exit 2.

Run: `godot --headless --path . --script res://tests/run_all.gd`

Expected: exit 1 with missing settings/action failures, not a parser crash.

- [ ] **Step 3: Fill the accepted project settings and actions**

Use:

```ini
[application]
config/name="Trash Dash 2.0"
config/version="0.1.0-foundation"
run/main_scene="res://scenes/bootstrap/bootstrap.tscn"

[display]
window/size/viewport_width=960
window/size/viewport_height=540
window/size/window_width_override=1280
window/size/window_height_override=720
window/stretch/mode="canvas_items"
window/stretch/aspect="keep"

[rendering]
renderer/rendering_method="gl_compatibility"
renderer/rendering_method.mobile="gl_compatibility"
textures/canvas_textures/default_texture_filter=0
textures/default_filters/use_nearest_mipmap_filter=false
```

Define the six `InputEventKey` action resources in the dictionary order above using these Godot 4.7.1 `physical_keycode` values: A `65`, Left `4194319`, D `68`, Right `4194321`, Space `32`, Shift `4194325`, E `69`, Escape `4194305`. Keep each action's `deadzone=0.5`; never add raw gameplay polling. Ignore `.godot/`, `.import/`, root build/export output, logs, macOS metadata, keystores, profiles, and certificates; do not ignore source `.uid` sidecars globally.

- [ ] **Step 4: Prove runner and project GREEN**

Run:

```bash
godot --headless --path . --script res://tests/run_all.gd --probe-pass
godot --headless --path . --script res://tests/run_all.gd --probe-fail
godot --headless --path . --script res://tests/run_all.gd
```

Expected: probe-pass 0; probe-fail 1 with `intentional runner probe failure`; the full suite exits 0 and the minimal main scene loads without warnings.

- [ ] **Step 5: Commit**

```bash
git add .gitignore project.godot scenes/bootstrap/bootstrap.tscn tests/support tests/run_all.gd tests/unit/test_project_contract.gd tests/unit/test_test_runner.gd
git commit -m "feat: establish Godot project contract"
```

---

### Task 2: Pure Build, Status, Display, and Input Boundaries

**Files:**
- Create: `src/core/build/build_identity.gd`
- Create: `src/core/bootstrap/foundation_status.gd`
- Create: `src/core/display/display_policy.gd`
- Create: `src/core/input/input_map_contract.gd`
- Create: `tests/unit/test_core_contracts.gd`
- Modify: `tests/run_all.gd`

**Interfaces:**
- Consumes: Task 1 project settings and action map.
- Produces: `BuildIdentity.development() -> BuildIdentity` and getters; `FoundationStatus.ready(identity)` / `error(identity, messages)` and getters; `DisplayPolicy.content_rect(physical_size: Vector2i) -> Rect2i`, `is_mobile_ui_enabled(platform_name: StringName, has_mobile_feature: bool) -> bool`; `InputMapContract.validate_current() -> PackedStringArray` and `validate_actions(actual: Dictionary) -> PackedStringArray`.

- [ ] **Step 1: Write the failing pure-contract suite**

Preload each proposed module explicitly and add:

```gdscript
func test_content_rects_are_centered() -> void:
    assert_equal(DisplayPolicy.content_rect(Vector2i(1280, 720)), Rect2i(0, 0, 1280, 720), "16:9")
    assert_equal(DisplayPolicy.content_rect(Vector2i(1440, 900)), Rect2i(0, 45, 1440, 810), "1440x900")
    assert_equal(DisplayPolicy.content_rect(Vector2i(1280, 800)), Rect2i(0, 40, 1280, 720), "1280x800")
    assert_equal(DisplayPolicy.content_rect(Vector2i(390, 844)), Rect2i(0, 312, 390, 219), "portrait desktop")
    assert_equal(DisplayPolicy.content_rect(Vector2i.ZERO), Rect2i(), "zero")

func test_identity_and_status_are_immutable_values() -> void:
    var identity := BuildIdentity.development()
    assert_equal(identity.version(), "0.1.0-foundation", "version")
    assert_equal(identity.revision(), "development", "revision")
    var source := PackedStringArray(["first"])
    var status := FoundationStatus.error(identity, source)
    source.append("mutated")
    assert_equal(status.messages(), PackedStringArray(["first"]), "copy input")
    assert_equal(status.state(), FoundationStatus.State.FOUNDATION_ERROR, "state")

func test_desktop_policy_has_no_mobile_ui() -> void:
    assert_equal(DisplayPolicy.is_mobile_ui_enabled(&"macOS", false), false, "macOS")
    assert_equal(DisplayPolicy.is_mobile_ui_enabled(&"Android", false), false, "feature absent")
    assert_equal(DisplayPolicy.is_mobile_ui_enabled(&"Android", true), true, "future query")

func test_current_input_map_is_valid() -> void:
    assert_equal(InputMapContract.validate_current(), PackedStringArray(), "input map")
```

Add the suite to the ordered runner.

- [ ] **Step 2: Run focused RED**

Run: `godot --headless --path . --script res://tests/run_all.gd --suite=test_core_contracts`

Expected: exit 1 with missing preload/resource errors for the four modules.

- [ ] **Step 3: Implement typed value objects and pure policies**

Give each public value/contract script a unique `class_name` so its own static factories can have concrete return types. Still use explicit preload aliases such as `const BuildIdentityType := preload(...)` for every cross-file parse dependency; do not depend on editor cache registration to resolve neighboring scripts. Private fields have getters only; arrays are duplicated on input and output; constructors assert nonempty version/revision.

Implement exact rectangle math:

```gdscript
static func content_rect(physical_size: Vector2i) -> Rect2i:
    if physical_size.x <= 0 or physical_size.y <= 0:
        return Rect2i()
    var width: int = physical_size.x
    var height: int = width * 9 / 16
    if height > physical_size.y:
        height = physical_size.y
        width = height * 16 / 9
    return Rect2i((physical_size.x - width) / 2, (physical_size.y - height) / 2, width, height)
```

`FoundationStatus.ready()` must store state `FOUNDATION_READY`, title `Trash Dash 2.0`, subtitle `macOS prototype foundation`, logical size `Vector2i(960, 540)`, renderer `Compatibility`, content `prototype content not loaded`, and no messages.

`InputMapContract` owns the exact ordered action dictionary. `validate_actions` returns ordered messages `missing input action: <name>` or `input defaults mismatch: <name>`. `validate_current` adapts `InputMap` to that pure helper; neither polls pressed state.

- [ ] **Step 4: Add negative cases and run GREEN**

Add tests for 1×1, odd, wide, tall, missing/mismatched action dictionaries, copied output messages, ready/error factories, and identity text containing no absolute path.

Run:

```bash
godot --headless --path . --script res://tests/run_all.gd --suite=test_core_contracts
godot --headless --path . --script res://tests/run_all.gd
```

Expected: focused and full suites exit 0 with no warnings.

- [ ] **Step 5: Commit**

```bash
git add src/core/build src/core/bootstrap/foundation_status.gd src/core/display src/core/input tests/unit/test_core_contracts.gd tests/run_all.gd
git commit -m "feat: define foundation runtime contracts"
```

---

### Task 3: Service Contracts and Explicit Unavailable Composition

**Files:**
- Create: `src/core/services/service_result.gd`
- Create: `src/core/services/save_settings_service.gd`
- Create: `src/core/services/audio_service.gd`
- Create: `src/core/services/scene_transition_service.gd`
- Create: `src/core/services/runtime_state_service.gd`
- Create: `src/core/services/unavailable_save_settings_service.gd`
- Create: `src/core/services/unavailable_audio_service.gd`
- Create: `src/core/services/unavailable_scene_transition_service.gd`
- Create: `src/core/services/unavailable_runtime_state_service.gd`
- Create: `src/core/services/service_registry.gd`
- Create: `tests/unit/test_service_registry.gd`
- Modify: `tests/run_all.gd`

**Interfaces:**
- Consumes: typed `RefCounted` only; no scene tree, filesystem, audio server, or scene switching.
- Produces: `ServiceResult.unavailable(service_id: StringName)`, `error() -> Error`, `value() -> Variant`; four base contracts with `service_id()` and narrow methods; `ServiceRegistry.unavailable()`, typed getters, `missing_service_ids() -> Array[StringName]`, `is_complete() -> bool`.

Contract methods:
- `SaveSettingsService.load_settings() -> ServiceResult` and `save_settings(settings: Dictionary) -> Error`.
- `AudioService.play_music(track_id: StringName) -> Error`, `stop_music() -> Error`, `set_muted(muted: bool) -> Error`.
- `SceneTransitionService.change_scene(scene_path: String) -> Error`.
- `RuntimeStateService.read_state(key: StringName) -> ServiceResult` and `write_state(key: StringName, value: Variant) -> Error`.

- [ ] **Step 1: Write failing registry/unavailable tests**

```gdscript
func test_unavailable_registry_is_complete() -> void:
    var registry := ServiceRegistry.unavailable()
    assert_true(registry.is_complete(), "registry complete")
    assert_equal(registry.missing_service_ids(), [], "no missing IDs")

func test_unavailable_services_fail_without_state_change() -> void:
    var registry := ServiceRegistry.unavailable()
    assert_equal(registry.save_settings().load_settings().error(), ERR_UNAVAILABLE, "load")
    assert_equal(registry.save_settings().save_settings({"muted": true}), ERR_UNAVAILABLE, "save")
    assert_equal(registry.audio().play_music(&"foundation"), ERR_UNAVAILABLE, "play")
    assert_equal(registry.audio().set_muted(true), ERR_UNAVAILABLE, "mute")
    assert_equal(registry.scenes().change_scene("res://never.tscn"), ERR_UNAVAILABLE, "scene")
    assert_equal(registry.runtime_state().write_state(&"phase", "changed"), ERR_UNAVAILABLE, "state")
    assert_equal(registry.runtime_state().read_state(&"phase").value(), null, "no value")
```

Also test exact stable IDs `save_settings`, `audio`, `scene_transition`, `runtime_state`, repeated-call determinism, and construction with one null service reporting that ID only.

- [ ] **Step 2: Run focused RED**

Run: `godot --headless --path . --script res://tests/run_all.gd --suite=test_service_registry`

Expected: exit 1 with missing service preloads.

- [ ] **Step 3: Implement base contracts, result, unavailable services, and registry**

Base methods must return `ERR_UNAVAILABLE`/`ServiceResult.unavailable(service_id())` rather than assert, print success, or touch engine singletons. Unavailable subclasses override only `service_id()` when inherited behavior is sufficient.

`ServiceResult` copies dictionary/array values before storing and returning them and exposes no mutator. `ServiceRegistry` constructor accepts the four typed base services for tests; `unavailable()` constructs all four unavailable implementations.

Use this result/factory shape (with explicit preload aliases for every referenced type):

```gdscript
# service_result.gd
extends RefCounted
class_name ServiceResult
var _error: Error
var _value: Variant

func _init(error_code: Error, stored_value: Variant) -> void:
    _error = error_code
    _value = stored_value.duplicate(true) if stored_value is Dictionary or stored_value is Array else stored_value

static func unavailable(_service_id: StringName) -> ServiceResult:
    return new(ERR_UNAVAILABLE, null)

func error() -> Error:
    return _error

func value() -> Variant:
    if _value is Dictionary or _value is Array:
        return _value.duplicate(true)
    return _value

# service_registry.gd
extends RefCounted
class_name ServiceRegistry

static func unavailable() -> ServiceRegistry:
    return new(
        UnavailableSaveSettingsService.new(),
        UnavailableAudioService.new(),
        UnavailableSceneTransitionService.new(),
        UnavailableRuntimeStateService.new()
)
```

Each factory returns its script's concrete `class_name`. Callers preload the script as an explicit `*Type` alias before using that type in fields, parameters, getters, or operational methods; this keeps clean-cache parsing independent of global-class discovery order.

- [ ] **Step 4: Prove no engine side effects and GREEN**

Snapshot `get_tree().root.get_child_count()`, `AudioServer.get_bus_count()`, and `ResourceLoader.exists("user://settings.json")` before repeated unavailable calls; assert identical values afterward. Do not create/delete a user save as part of the test.

Run focused service tests twice, then full tests. Expected: all exit 0; no leak, audio, filesystem, or scene-change diagnostic.

- [ ] **Step 5: Commit**

```bash
git add src/core/services tests/unit/test_service_registry.gd tests/run_all.gd
git commit -m "feat: add explicit unavailable services"
```

---


### Task 4: Startup Validator and Diagnostic Bootstrap Scene

**Files:**
- Create: `src/core/bootstrap/project_settings_adapter.gd`
- Create: `src/core/bootstrap/startup_validator.gd`
- Create: `src/core/bootstrap/bootstrap_controller.gd`
- Create: `src/ui/bootstrap/bootstrap_view.gd`
- Modify: `scenes/bootstrap/bootstrap.tscn`
- Create: `tests/unit/test_startup_validator.gd`
- Create: `tests/gameplay/test_bootstrap_scene.gd`
- Modify: `tests/run_all.gd`

**Interfaces:**
- Consumes: `BuildIdentity`, `FoundationStatus`, `InputMapContract`, `ServiceRegistry`.
- Produces: `ProjectSettingsAdapter.get_value(key: StringName) -> Variant`; `StartupValidator.validate(settings, input_messages: PackedStringArray, registry: ServiceRegistry) -> PackedStringArray`; `BootstrapController.configure(registry: ServiceRegistry, settings: ProjectSettingsAdapter, identity: BuildIdentity) -> void` before tree entry; `BootstrapView.present(status: FoundationStatus) -> void`.

- [ ] **Step 1: Write failing validator and scene tests**

A fake settings adapter backed by a dictionary must prove exact ordered errors:

```gdscript
const EXPECTED_ERRORS := PackedStringArray([
    "viewport width must be 960",
    "viewport height must be 540",
    "stretch mode must be canvas_items",
    "stretch aspect must be keep",
    "renderer must be gl_compatibility",
    "default texture filtering must be nearest",
    "missing input action: jump",
    "missing service: audio",
])

func test_valid_contract_has_no_errors() -> void:
    assert_equal(StartupValidator.validate(valid_settings(), PackedStringArray(), ServiceRegistry.unavailable()), PackedStringArray(), "valid")

func test_failures_are_ordered() -> void:
    assert_equal(StartupValidator.validate(invalid_settings(), PackedStringArray(["missing input action: jump"]), incomplete_registry()), EXPECTED_ERRORS, "order")
```

Scene tests load `res://scenes/bootstrap/bootstrap.tscn`, assert the exact node paths from the design, add it to a live root, await two frames, assert controller state `FOUNDATION_READY` and exact five label strings, then queue-free it and await teardown.

- [ ] **Step 2: Run focused RED**

Run validator and bootstrap suites separately. Expected: both exit 1 for missing preloads/scene; no unrelated suite failure is accepted as the RED evidence.

- [ ] **Step 3: Implement the pure validator and adapter**

`ProjectSettingsAdapter` is the only production wrapper around `ProjectSettings.get_setting`. The validator checks, in this fixed order: width, height, stretch mode, stretch aspect, renderer, nearest filter, supplied input messages, registry missing IDs. Prototype content being unavailable is expected and is not an error.

Use stable messages shown in the test. The validator must never print, quit, mutate settings, or consult OS state.

```gdscript
static func validate(settings: RefCounted, input_messages: PackedStringArray, registry: RefCounted) -> PackedStringArray:
    var errors := PackedStringArray()
    _require_equal(errors, settings.get_value(&"display/window/size/viewport_width"), 960, "viewport width must be 960")
    _require_equal(errors, settings.get_value(&"display/window/size/viewport_height"), 540, "viewport height must be 540")
    _require_equal(errors, settings.get_value(&"display/window/stretch/mode"), "canvas_items", "stretch mode must be canvas_items")
    _require_equal(errors, settings.get_value(&"display/window/stretch/aspect"), "keep", "stretch aspect must be keep")
    _require_equal(errors, settings.get_value(&"rendering/renderer/rendering_method"), "gl_compatibility", "renderer must be gl_compatibility")
    _require_equal(errors, settings.get_value(&"rendering/textures/canvas_textures/default_texture_filter"), 0, "default texture filtering must be nearest")
    errors.append_array(input_messages)
    for service_id: StringName in registry.missing_service_ids():
        errors.append("missing service: %s" % service_id)
    return errors
```

- [ ] **Step 4: Implement bootstrap controller, view, and scene**

The scene hierarchy is exact:

```text
Bootstrap (Control; bootstrap_controller.gd)
└── SafeMargin (MarginContainer; bootstrap_view.gd)
    └── StatusColumn (VBoxContainer)
        ├── ProjectTitle (Label)
        ├── FoundationStatus (Label)
        ├── BuildIdentity (Label)
        ├── RuntimePolicy (Label)
        └── ContentStatus (Label)
```

Root and containers use full-rect anchors and theme constants; no script sets pixel positions. On `_ready()` the controller uses configured dependencies or creates the unavailable registry, real adapter, and development identity, validates, constructs ready/error status, and calls the view. It exposes `foundation_state() -> FoundationStatus.State` only for diagnostics/tests.

```gdscript
func _ready() -> void:
    var registry := _configured_registry if _configured_registry != null else ServiceRegistry.unavailable()
    var settings := _configured_settings if _configured_settings != null else ProjectSettingsAdapter.new()
    var identity := _configured_identity if _configured_identity != null else BuildIdentity.development()
    var errors := StartupValidator.validate(settings, InputMapContract.validate_current(), registry)
    _status = FoundationStatus.ready(identity) if errors.is_empty() else FoundationStatus.error(identity, errors)
    _view.present(_status)
```

`BootstrapView.present` formats only:
- `Trash Dash 2.0`
- `macOS prototype foundation — FOUNDATION_READY` or `FOUNDATION_ERROR`
- `0.1.0-foundation (development)`
- `960×540 / Compatibility`
- `prototype content not loaded`, followed by ordered error lines only when invalid.

- [ ] **Step 5: Run clean-cache GREEN and lifecycle checks**

Run:

```bash
godot --headless --path . --editor --quit
godot --headless --path . --script res://tests/run_all.gd --suite=test_startup_validator
godot --headless --path . --script res://tests/run_all.gd --suite=test_bootstrap_scene
godot --headless --path . --script res://tests/run_all.gd
godot --headless --path . --editor --quit
```

Expected: all exit 0 with no parse, resource, missing-node, leak, orphan StringName, or ObjectDB warning. Confirm `project.godot` has no `[autoload]` section.

- [ ] **Step 6: Commit**

```bash
git add scenes/bootstrap src/core/bootstrap src/ui/bootstrap tests/unit/test_startup_validator.gd tests/gameplay/test_bootstrap_scene.gd tests/run_all.gd
git commit -m "feat: add diagnostic foundation bootstrap"
```

---

### Task 5: Local Policy, macOS Export Proof, and Developer Guide

**Files:**
- Create: `export_presets.cfg`
- Create: `tools/verify/check_policy.sh`
- Create: `tools/verify/run_tests.sh`
- Create: `tools/verify/export_macos.sh`
- Create: `tools/verify/verify_local.sh`
- Create: `docs/development/MACOS_FOUNDATION.md`
- Modify: `tests/unit/test_project_contract.gd`

**Interfaces:**
- Consumes: clean Task 4 project at exact Git revision and environment variable `TRASH_DASH_GODOT_BIN`, defaulting to `godot`.
- Produces: `tools/verify/check_policy.sh`, `run_tests.sh`, `export_macos.sh <empty-output-dir>`, and `verify_local.sh`; one preset named `macOS`; terminal evidence for revision, package size/SHA, ZIP integrity, and `arm64 x86_64`.

- [ ] **Step 1: Write failing export/policy contract tests**

Extend the project test to parse `export_presets.cfg` as text and assert:
- exactly one `[preset.0]` and no `[preset.1]`;
- `name="macOS"` and `platform="macOS"`;
- signing and notarization enum values are disabled;
- no `Windows Desktop`, Android, iOS, Linux, or Web preset strings;
- no Team ID, certificate, password, provisioning profile, absolute user path, or secret-looking assignment.

Create `check_policy.sh` first with an intentional `exit 1` and run it to capture RED.

- [ ] **Step 2: Add the single secret-safe macOS preset**

Use Godot 4.7.1-valid macOS keys:

```ini
[preset.0]
name="macOS"
platform="macOS"
runnable=true
advanced_options=false
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter=""
exclude_filter=""
export_path=""
script_export_mode=2

[preset.0.options]
binary_format/architecture="universal"
codesign/codesign=0
notarization/notarization=0
application/bundle_identifier="com.trashdash.foundation"
application/short_version="0.1.0"
application/version="0.1.0"
application/copyright=""
application/copyright_localized={}
application/icon=""
```

Before GREEN, compare every key with the installed 4.7.1 preset generated by Godot or official local documentation; replace any invalid key rather than suppressing exporter warnings.

- [ ] **Step 3: Implement bounded policy and test scripts**

`check_policy.sh` resolves the repository from its own path, uses `git ls-files`, and fails on:
- tracked `.godot/`, `.import/`, `build/`, `exports/`, logs, credentials, certificates, profiles, keystores, or generated UID-cache files;
- runtime/config references to sibling V1, `archive/`, deleted spike resources, concept/reference sheets, deferred platform presets, `/Users/`, `/home/`, or drive-letter paths;
- new files beneath runtime asset, actor, gameplay, level, rendering, or world roots beyond already-empty keep markers.

Limit forbidden-reference content scanning to `project.godot`, `export_presets.cfg`, `scenes/`, `src/`, and `docs/development/`. Tests and policy scripts necessarily contain forbidden fixtures/patterns; separately constrain their tracked paths and inspect their shell commands. Design/reference documentation is intentionally allowed to describe V1 and concepts.

The script begins with strict mode and explicit roots; every rejected match prints its file and rule:

```bash
#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
cd "$repo_root"
tracked_files="$(git ls-files)"
if printf '%s\n' "$tracked_files" | rg '(^|/)(\.godot|\.import|build|exports)(/|$)'; then
  echo "policy violation: tracked generated output" >&2
  exit 1
fi
```

`run_tests.sh` executes exact-version validation then `godot --headless --path <root> --script res://tests/run_all.gd`. Version validation must require exact output `4.7.1.stable.official.a13da4feb`, reject `.mono`/dev/custom builds, and report that the Standard executable was selected.

- [ ] **Step 4: Implement safe fresh export verification**

`export_macos.sh` accepts exactly one explicit output directory, rejects root/workspace/nonempty directories, creates only that directory, exports `trash-dash-foundation-macos.zip`, then runs:

```bash
unzip -t "$package"
unzip -q "$package" -d "$extract_dir"
lipo -archs "$extract_dir/Trash Dash 2.0.app/Contents/MacOS/Trash Dash 2.0"
shasum -a 256 "$package"
```

It prints the clean `git rev-parse HEAD`, byte size, SHA-256, and architectures. It never signs, notarizes, uploads, edits presets, or recursively deletes user paths.

`verify_local.sh` runs policy → headless import → tests → headless editor smoke → export into `mktemp -d` → bounded direct executable launch. Capture the exact child PID, send `SIGINT` after at most five seconds, wait for it, accept only Godot's clean exit, verify the PID is absent, and clean only the validated temp directory via a trap.

- [ ] **Step 5: Document commands and boundary language**

`MACOS_FOUNDATION.md` records prerequisites, `TRASH_DASH_GODOT_BIN` override, focused/full commands, expected diagnostic labels, output fields, unsigned-package limitation, Apple-account hookup deferral, asset-import deferral, and the exact non-claims: no gameplay pass, asset pass, audio pass, human traversal pass, signing/notarization pass, or release pass.

- [ ] **Step 6: Commit the verification implementation**

```bash
git add export_presets.cfg tools/verify docs/development/MACOS_FOUNDATION.md tests/unit/test_project_contract.gd
git commit -m "build: verify unsigned macOS foundation"
```

- [ ] **Step 7: Run final automated verification from clean HEAD**

From a clean worktree run policy, import, full tests twice, editor smoke, and `verify_local.sh`. Expected: all commands exit 0, test output is warning/leak-free, ZIP passes integrity, executable reports both `x86_64` and `arm64`, bounded package process is absent, and no output is tracked.

Run `git diff --check`, require `git status --short` to be empty, and verify the sibling V1 revision is unchanged from the pre-task capture. If a defect is found, add a narrowly scoped fix commit and restart this step from a clean HEAD; do not reuse earlier package evidence.

- [ ] **Step 8: Perform direct diagnostic-shell inspection**

Launch the fresh package at 1280×720, 1440×900, 1280×800, and 390×844. Inspect that all five neutral labels are readable, the FOV is stable, bars are centered, there is no touch UI, and no sprite/art exists. Record observation as `PASS` only for those presentation checks; retain overall scaffold visual status `INCOMPLETE` if any window or direct inspection cannot be completed.

- [ ] **Step 9: Confirm inspection created no source changes**

Run `git status --short` and require empty output. Retain screenshots/logs only in the verified temporary evidence directory for the current review; do not commit package or capture output as production source.

---

## Final Review Gate

- [ ] Map every acceptance criterion in the approved design to a command/test above.
- [ ] Confirm commits contain infrastructure only and no concept-derived/runtime asset bytes.
- [ ] Confirm no autoload or deferred-platform preset exists.
- [ ] Confirm `git status --short` is empty and `git diff --check HEAD^..HEAD` passes.
- [ ] Report exact Godot version, commit, test results, package identity, architecture proof, process cleanup, V1 revision, and honest visual status.
- [ ] Stop before gameplay, asset import, Apple signing hookup, CI, or store work.

+
